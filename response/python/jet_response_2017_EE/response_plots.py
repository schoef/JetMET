# standard imports
import os
import ROOT
import uuid
import array
import copy

# RootTools
from RootTools.core.standard import *

# JetMET
from JetMET.tools.user import skim_ntuple_directory
from JetMET.tools.user import plot_directory

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
#argParser.add_argument('--small',              action='store_true', help='Run only on a small subset of the data?')#, default = True)
#argParser.add_argument('--overwrite',          action='store_true', help='overwrite?')#, default = True)
argParser.add_argument('--samples',            type = str,          nargs = '+', default = ["RelVal_QCD_flat_GTv2_SRPFon_PUpmx25ns", "RelVal_QCD_flat_GTv2_SRPFon_PUpmx25ns_ZeroN"], help='Which samples? ')
argParser.add_argument('--plot_directory',     action='store',      default='EE_2017_ZeroN')
args = argParser.parse_args()

#
# Logger
#
import JetMET.tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

# samples
from JetMET.response.jet_response_2017_EE.samples import *
from JetMET.response.jet_response_2017_EE.helpers import *


def scale_resolution_from_profile( profile ):
    scale       = profile.ProjectionX()
    resolution  = profile.ProjectionX("_px","C=E") 
    resolution.Divide( scale )

    return scale, resolution

def eta_scale_resolution( chain, selection = "(1)"):
    ''' Get Scale plot vs. eta '''
    hname = 'p_'+uuid.uuid4().hex
    profile = ROOT.TProfile( hname, hname, 30, 0, 3, "S")
    chain.Draw( "rawPt/genPt:abs(eta)>>"+hname, selection )

    return scale_resolution_from_profile( profile )

def eta_frac( chain, frac, selection = "(1)"):
    ''' Get fraction plot vs. eta '''
    hname = 'p_'+uuid.uuid4().hex
    profile = ROOT.TProfile( hname, hname, 30, 0, 3, "S")
    chain.Draw( frac+":abs(eta)>>"+hname, selection )

    return profile.ProjectionX()

def pt_frac( chain, frac, selection = "(1)"):
    ''' Get fraction plot vs. pt '''
    pt_thresholds = [10**(x/10.) for x in range(11,31)]

    hname = 'p_'+uuid.uuid4().hex
    profile = ROOT.TProfile( hname, hname, len(pt_thresholds)-1, array.array('d', pt_thresholds), "S")
    chain.Draw( frac+":genPt>>"+hname, selection )

    return profile.ProjectionX()


def pt_scale_resolution( chain, selection = "(1)"):
    ''' Get Scale plot vs. pt '''

    pt_thresholds = [10**(x/10.) for x in range(11,31)]

    hname = 'p_'+uuid.uuid4().hex
    profile = ROOT.TProfile( hname, hname, len(pt_thresholds)-1, array.array('d', pt_thresholds), "S")
    chain.Draw( "rawPt/genPt:genPt>>"+hname, selection )

    return scale_resolution_from_profile( profile )

def responseShape_1D( chain, selection = "(1)"):
    ''' Get Scale plot vs. pt '''

    #thresholds = [10**(x/10.) for x in range(11,31)]

    hname = 'p_'+uuid.uuid4().hex
    h = ROOT.TH1D( hname, hname, 50,0,1.5)
    chain.Draw( "rawPt/genPt>>"+hname, selection )
    return h

def varShape_1D( chain, var, binning, selection = "(1)"):
    ''' Get Scale plot vs. pt '''

    #thresholds = [10**(x/10.) for x in range(11,31)]

    hname = 'p_'+uuid.uuid4().hex
    h = ROOT.TH1D( hname, hname, *binning)
    #print (hname, hname, binning)
    #print var+">>"+hname, selection
    chain.Draw( var+">>"+hname, selection )
    return h


def nVert_scale_resolution( chain, selection = "(1)"):
    ''' Get Scale plot vs. pt '''

    hname = 'p_'+uuid.uuid4().hex
    profile = ROOT.TProfile( hname, hname, 50, 0, 50, "S")
    chain.Draw( "rawPt/genPt:nVert>>"+hname, selection )

    return scale_resolution_from_profile( profile )

# Interpret samples
samples = map( eval, args.samples )

if len(samples) == 2:
    ratio_h = [0,1]
elif len(samples)==3:
    ratio_h = [1,2]
else:
    ratio_h = None 

color = [ROOT.kBlue, ROOT.kBlack, ROOT.kRed, ROOT.kGreen, ROOT.kMagenta]

genPt_bins = [
    (15, 20),
#    (20, 30),
#    (30, 40),
    (40, 50), 
#    (50, 60),
    (100, 120)
]

absEta_bins = [
    #(1.7, 2.1), 
    (0, 1.3), 
    (1.3, 2), 
    (2, 2.5), 
    (2.5, 2.75), 
    (2.75, 3), 
]

# response shape plots 1D
for name, var, binning, texX, logY in [\
    [ "responseShapes", "rawPt/genPt", [50, 0, 1.5], "gen jet p_{T}", False],
    [ "phEF", "phEF", [50, 0, 1], "photon EF", True],
    [ "phEF", "phEF", [50, 0, 1], "photon EF", False],
    ]: 
    for i_absEta_bin, absEta_bin in enumerate( absEta_bins ):
        responseShape_histos        = []
        for i_genPt_bin, genPt_bin in enumerate( genPt_bins ):
            for i_s, s in enumerate(samples):
                responseShape               = varShape_1D( s.chain, var, binning, cut_string( "genPt", genPt_bin )+"&&"+cut_string( "abs(eta)", absEta_bin ))
                responseShape.legendText    = (s.texName+", "+pt_tex_string("p_{T,gen.}", genPt_bin)).replace( "GT","").replace( "SR@PF ", "")#.replace( "NoPU,", "").replace( "PU,", "")
                responseShape.style         = styles.lineStyle( color[i_genPt_bin], dotted = ('v1' in s.name), dashed = ( 'ZeroN' in s.name))
                responseShape_histos.append( [responseShape] )

        for histo in responseShape_histos:
            h = histo[0]
            if h.Integral()>0:
                h.Scale(1./h.Integral())

        logY_str = "_logY" if logY else ""
        jetResponsePlot = Plot.fromHisto(name = (name+"_eta_%3.2f_%3.2f"%absEta_bin) +logY_str , histos = responseShape_histos, texX = texX , texY = "" )
        plotting.draw(jetResponsePlot, plot_directory = os.path.join( plot_directory, args.plot_directory), ratio = None, logY = logY, logX = False, 
            yRange=(0.001, 9) if logY else 'auto',  
            legend      = ([0.15,0.7,0.90,0.90], len(samples)),
            )

### PHEF Plots 
#for var in ["phEF", "neHEF", "phMult"]:
##for var in [ "phMult"]:
#    pt_frac_histos  = {genPt_bin:[] for genPt_bin in genPt_bins}
#    eta_frac_histos = {absEta_bin:[] for absEta_bin in absEta_bins}
#    for i_s, s in enumerate(samples):
#        # Plots vs. eta
#        frac_histos        = []
#        for i_genPt_bin, genPt_bin in enumerate( genPt_bins ):
#            frac               = eta_frac( s.chain, var, cut_string( "genPt", genPt_bin ))
#            frac.legendText    = pt_tex_string("p_{T,gen.}", genPt_bin)
#            frac.style         = styles.lineStyle( color[i_genPt_bin])
#            frac_histos.append( [frac] )
#
#            frac2 = copy.deepcopy(frac)
#            frac2.legendText = s.texName 
#            frac2.style      = styles.lineStyle( color[i_s])
#            pt_frac_histos[genPt_bin].append( [frac2] )
#
#        jetResponsePlot = Plot.fromHisto(name = "absEta_%s_%s"%(var, s.name), histos = frac_histos, texX = "gen jet #eta" , texY = "<%s>"%var )
#        plotting.draw(jetResponsePlot, plot_directory = os.path.join( plot_directory, args.plot_directory), ratio = None, logY = False, logX = False, 
#            yRange = (0, 0.5) if 'Mult' not in var else (0, 15 ),  
#            legend = [0.60,0.92-0.05*len(frac_histos),0.99,0.88])
#
#        # Plots vs. pt
#        frac_histos        = []
#        for i_absEta_bin, absEta_bin in enumerate( absEta_bins ):
#            frac               = pt_frac( s.chain, var, cut_string( "abs(eta)", absEta_bin ))
#            frac.legendText    = eta_tex_string("|#eta|", absEta_bin)
#            frac.style         = styles.lineStyle( color[i_absEta_bin])
#            frac_histos.append( [frac] )
#
#            frac2 = copy.deepcopy(frac)
#            frac2.legendText = s.texName 
#            frac2.style      = styles.lineStyle( color[i_s])
#            eta_frac_histos[absEta_bin].append( [frac2] )
#
#        jetResponsePlot = Plot.fromHisto(name = "pt_frac_"+s.name, histos = frac_histos, texX = "gen jet p_{T}" , texY = "<%s>"%var )
#        plotting.draw(jetResponsePlot, plot_directory = os.path.join( plot_directory, args.plot_directory), ratio = None, logY = False, logX = True, 
#            yRange=(0, 0.5) if 'Mult' not in var else (0, 15 ),  
#            legend = [0.15,0.42-0.05*len(frac_histos),0.48,0.38])
#
#    for i_genPt_bin, genPt_bin in enumerate( genPt_bins ):
#        jetResponsePlot = Plot.fromHisto(name = "absEta_"+var+"_pt_%i_%i"%genPt_bin, histos = pt_frac_histos[genPt_bin], texX = "gen jet #eta" , texY = "<%s>"%var )
#        plotting.draw(jetResponsePlot, plot_directory = os.path.join( plot_directory, args.plot_directory), ratio = {'den':0, 'num':ratio_h, 'texY':'ratio'}, logY = False, logX = False,
#            yRange=(0, 0.5) if 'Mult' not in var else (0, 15 ),  
#            legend = [0.15,0.92-0.05*len(pt_frac_histos[genPt_bin]),0.48,0.88])
#
#    for i_absEta_bin, absEta_bin in enumerate( absEta_bins ):
#        jetResponsePlot = Plot.fromHisto(name = "pt_"+var+"_eta_%3.2f_%3.2f"%absEta_bin, histos = eta_frac_histos[absEta_bin], texX = "gen jet p_{T}" , texY = "<%s>"%var )
#        plotting.draw(jetResponsePlot, plot_directory = os.path.join( plot_directory, args.plot_directory), ratio = {'den':0, 'num':ratio_h, 'texY':'ratio'}, logY = False, logX = True,
#            yRange=(0, 0.5) if 'Mult' not in var else (0, 15 ),  
#            legend = [0.60,0.42-0.05*len(eta_frac_histos[absEta_bin]),0.95,0.42])
#
# Scale and resolution vs. eta
pt_scale_histos  = {genPt_bin:[] for genPt_bin in genPt_bins}
eta_scale_histos = {absEta_bin:[] for absEta_bin in absEta_bins}
pt_resolution_histos  = {genPt_bin:[] for genPt_bin in genPt_bins}
eta_resolution_histos = {absEta_bin:[] for absEta_bin in absEta_bins}
for i_s, s in enumerate(samples):
    scale_histos        = []
    resolution_histos   = []
    for i_genPt_bin, genPt_bin in enumerate( genPt_bins ):
        scale, resolution   = eta_scale_resolution( s.chain, cut_string( "genPt", genPt_bin ))
        scale.legendText    = pt_tex_string("p_{T,gen.}", genPt_bin)
        scale.style         = styles.lineStyle( color[i_genPt_bin])
        scale_histos.append( [scale] )

        scale2 = copy.deepcopy(scale)
        scale2.legendText = s.texName 
        scale2.style      = styles.lineStyle( color[i_s])
        pt_scale_histos[genPt_bin].append( [scale2] )

        resolution.legendText    = pt_tex_string("p_{T,gen.}", genPt_bin)
        resolution.style         = styles.lineStyle( color[i_genPt_bin])
        resolution_histos.append( [resolution] )

        resolution2 = copy.deepcopy(resolution)
        resolution2.legendText = s.texName 
        resolution2.style      = styles.lineStyle( color[i_s])
        pt_resolution_histos[genPt_bin].append( [resolution2] )

    jetResponsePlot = Plot.fromHisto(name = "absEta_scale_"+s.name, histos = scale_histos, texX = "gen jet #eta" , texY = "<response>" )
    plotting.draw(jetResponsePlot, plot_directory = os.path.join( plot_directory, args.plot_directory), ratio = None, logY = False, logX = False, 
        yRange=(0.5, 1.2),  
        legend = [0.50,0.92-0.05*len(scale_histos),0.92,0.88])

    jetResolutionPlot = Plot.fromHisto(name = "absEta_resolution_"+s.name, histos = resolution_histos, texX = "gen jet #eta" , texY = "RMS/<response>" )
    plotting.draw(jetResolutionPlot, plot_directory = os.path.join( plot_directory, args.plot_directory), ratio = None, logY = False, logX = False, 
        yRange=(0, .49),  
        legend = [0.50,0.92-0.05*len(resolution_histos),0.92,0.88])

    # Plots vs. pT
    scale_histos        = []
    resolution_histos   = []
    for i_absEta_bin, absEta_bin in enumerate( absEta_bins ):
        scale, resolution   = pt_scale_resolution( s.chain, cut_string( "abs(eta)", absEta_bin ))
        scale.legendText    = eta_tex_string("|#eta|", absEta_bin)
        scale.style         = styles.lineStyle( color[i_absEta_bin])
        scale_histos.append( [scale] )

        scale2 = copy.deepcopy(scale)
        scale2.legendText = s.texName 
        scale2.style      = styles.lineStyle( color[i_s])
        eta_scale_histos[absEta_bin].append( [scale2] )

        resolution.legendText    = eta_tex_string("|#eta|", absEta_bin)
        resolution.style         = styles.lineStyle( color[i_absEta_bin])
        resolution_histos.append( [resolution] )

        resolution2 = copy.deepcopy(resolution)
        resolution2.legendText = s.texName 
        resolution2.style      = styles.lineStyle( color[i_s])
        eta_resolution_histos[absEta_bin].append( [resolution2] )

    jetResponsePlot = Plot.fromHisto(name = "pt_scale_"+s.name, histos = scale_histos, texX = "gen jet p_{T}" , texY = "<response>" )
    plotting.draw(jetResponsePlot, plot_directory = os.path.join( plot_directory, args.plot_directory), ratio = None, logY = False, logX = True, 
        yRange=(0.5, 1.2),  
        legend = [0.50,0.92-0.05*len(scale_histos),0.92,0.88])

    jetResolutionPlot = Plot.fromHisto(name = "pt_resolution_"+s.name, histos = resolution_histos, texX = "gen jet p_{T}" , texY = "RMS/<response>" )
    plotting.draw(jetResolutionPlot, plot_directory = os.path.join( plot_directory, args.plot_directory), ratio = None, logY = False, logX = True, 
        yRange=(0, .49),  
        legend = [0.50,0.92-0.05*len(resolution_histos),0.92,0.88])

# scale in pt bins
for i_genPt_bin, genPt_bin in enumerate( genPt_bins ):
    jetResponsePlot = Plot.fromHisto(name = "absEta_response_pt_%i_%i"%genPt_bin, histos = pt_scale_histos[genPt_bin], texX = "gen jet #eta" , texY = "<response>" )
    plotting.draw(jetResponsePlot, plot_directory = os.path.join( plot_directory, args.plot_directory), ratio = {'den':0, 'num':ratio_h, 'texY':'ratio'}, logY = False, logX = False,
        yRange=(0.5, 1.2),
        legend = [0.50,0.92-0.05*len(pt_scale_histos[genPt_bin]),0.92,0.88])

# scale in eta bins
for i_absEta_bin, absEta_bin in enumerate( absEta_bins ):
    jetResponsePlot = Plot.fromHisto(name = "pt_response_eta_%3.2f_%3.2f"%absEta_bin, histos = eta_scale_histos[absEta_bin], texX = "gen jet p_{T}" , texY = "<response>" )
    plotting.draw(jetResponsePlot, plot_directory = os.path.join( plot_directory, args.plot_directory), ratio = {'den':0, 'num':ratio_h, 'texY':'ratio'}, logY = False, logX = True,
        yRange=(0.5, 1.2),
        legend = [0.15,0.92-0.05*len(eta_scale_histos[absEta_bin]),0.48,0.88])

# resolution in pt bins
for i_genPt_bin, genPt_bin in enumerate( genPt_bins ):
    jetResolutionPlot = Plot.fromHisto(name = "absEta_resolution_pt_%i_%i"%genPt_bin, histos = pt_resolution_histos[genPt_bin], texX = "gen jet #eta" , texY = "RMS/<response>" )
    plotting.draw(jetResolutionPlot, plot_directory = os.path.join( plot_directory, args.plot_directory), ratio = {'den':0, 'num':ratio_h, 'texY':'ratio'}, logY = False, logX = False,
        yRange=(0, 0.5),
        legend = [0.50,0.92-0.05*len(pt_resolution_histos[genPt_bin]),0.92,0.88])

# resolution in eta bins
for i_absEta_bin, absEta_bin in enumerate( absEta_bins ):
    jetResolutionPlot = Plot.fromHisto(name = "pt_resolution_eta_%3.2f_%3.2f"%absEta_bin, histos = eta_resolution_histos[absEta_bin], texX = "gen jet p_{T}" , texY = "RMS/<response>" )
    plotting.draw(jetResolutionPlot, plot_directory = os.path.join( plot_directory, args.plot_directory), ratio = {'den':0, 'num':ratio_h, 'texY':'ratio'}, logY = False, logX = True,
        yRange=(0, 0.5),
        legend = [0.15,0.92-0.05*len(eta_resolution_histos[absEta_bin]),0.48,0.88])

# Make plot
for s in samples:
    # Plots vs. nVert
    scale_histos        = []
    resolution_histos   = []
    for i_genPt_bin, genPt_bin in enumerate( genPt_bins ):
        scale, resolution   = nVert_scale_resolution( s.chain, cut_string( "genPt", genPt_bin )+"&&"+cut_string( "abs(eta)", (2.5, 3.)) )
        scale.legendText    = pt_tex_string("p_{T,gen.}", genPt_bin)+ " 2.5<#eta<3"
        scale.style         = styles.lineStyle( color[i_genPt_bin])
        scale_histos.append( [scale] )

        resolution.legendText    = pt_tex_string("p_{T,gen.}", genPt_bin)
        resolution.style         = styles.lineStyle( color[i_genPt_bin])
        resolution_histos.append( [resolution] )

    jetResponsePlot = Plot.fromHisto(name = "nVert_scale_"+s.name, histos = scale_histos, texX = "nVert" , texY = "<response>" )
    plotting.draw(jetResponsePlot, plot_directory = os.path.join( plot_directory, args.plot_directory), ratio = None, logY = False, logX = False, 
        yRange=(0.5, 1.2),  
        legend = [0.50,0.42-0.05*len(scale_histos),0.92,0.38])

    jetResolutionPlot = Plot.fromHisto(name = "nVert_resolution_"+s.name, histos = resolution_histos, texX = "nVert" , texY = "RMS/<response>" )
    plotting.draw(jetResolutionPlot, plot_directory = os.path.join( plot_directory, args.plot_directory), ratio = None, logY = False, logX = False, 
        yRange=(0, .49),  
        legend = [0.50,0.92-0.05*len(resolution_histos),0.92,0.88])

