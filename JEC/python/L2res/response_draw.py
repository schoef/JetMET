#!/usr/bin/env python
''' Analysis script for L3 residuals (Z balancing) 
'''
#
# Standard imports and bateh mode
#
import ROOT
ROOT.gROOT.SetBatch(True)

# RooFit
ROOT.gSystem.Load("libRooFit.so")
ROOT.gSystem.Load("libRooFitCore.so")
ROOT.gROOT.SetStyle("Plain") # Not sure this is needed
ROOT.gSystem.SetIncludePath( "-I$ROOFITSYS/include/" )

import itertools
import os
import array
import pickle

from math                                import sqrt, cos, sin, pi, atan2
from RootTools.core.standard             import *
from JetMET.tools.user                   import plot_directory as user_plot_directory
from JetMET.tools.helpers                import deltaPhi, deltaR

# Gaussian (Roo-)Fit
from JetMET.JEC.L2res.helpers            import gaussianFit

# Object selection
from JetMET.tools.objectSelection        import getFilterCut, getJets, jetVars

#
# Arguments
# 
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging" )
argParser.add_argument('--triggers',           action='store',      default='DiPFJetAve',    nargs='?', choices=['DiPFJetAve', 'DiPFJetAve_HFJEC', 'PFJet'], help="trigger suite" )
argParser.add_argument('--ptBinningVar',       action='store',      default='ave',           nargs='?', choices=['ave', 'tag'], help="jet pT binning variable (pT avg or pT tag)" )
argParser.add_argument('--era',                action='store',      default='Run2016',       nargs='?', choices=['Run2016', 'Run2016BCD', 'Run2016EFearly', 'Run2016FlateG', 'Run2016H'], help="era" )
argParser.add_argument('--phEF',               action='store',      default= -1,             type=float, help="max phEF in probe jet" )
argParser.add_argument('--small',                                   action='store_true',     help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--cleaned',                                 action='store_true',     help='Apply jet cleaning in data')#, default = True)
argParser.add_argument('--skipResponsePlots',                       action='store_true',     help='Skip A/B plots?')#, default = True)
argParser.add_argument('--overwrite',                               action='store_true',     help='Overwrite results.pkl?')
argParser.add_argument('--useFit',                                  action='store_true',     help='Use a fit to determine the response')#, default= True
argParser.add_argument('--metOverSumET',                            action='store_true',     help='add MET/sumET<0.2 cut')#, default= True
argParser.add_argument('--plot_directory',     action='store',      default='JEC/L2res_v4',  help="subdirectory for plots")
args = argParser.parse_args()

if args.ptBinningVar == 'tag':
    args.plot_directory += '_tagJetPtBin'
    pt_binning_variable = 'Jet_pt[tag_jet_index]'
    pt_binning_legendText = 'p_{T,tag} '
else:
    pt_binning_legendText = 'p_{T,avg} '
    pt_binning_variable = "pt_avg"

if args.phEF>0:
    args.plot_directory += '_phEF%i' % ( 100*args.phEF )

if args.cleaned:
    args.plot_directory += '_cleaned'
if args.metOverSumET:
    args.plot_directory += '_metOverSumET'
if args.small:
    args.plot_directory += '_small'

plot_directory = os.path.join( user_plot_directory, args.plot_directory, args.era, args.triggers )

# Lumi for MC
lumi = 35.9
# DrawLatex objects for plots
tex = ROOT.TLatex()
tex.SetNDC()
tex.SetTextSize(0.04)
tex.SetTextAlign(11) # align right
def drawObjects( dataMCScale, lumi ):
    lines = [
      #(0.15, 0.95, args.era), 
      (0.15, 0.95, '%s (13 TeV)'% ( args.era ) ),
    ]
    return [tex.DrawLatex(*l) for l in lines] 

# Formatting for 1D plots
def draw1DPlots(plots, dataMCScale):
  for log in [ True]:
    plot_directory_ = os.path.join(plot_directory, ("log" if log else "") )
    for plot in plots:
      #if not max(l[0].GetMaximum() for l in plot.histos): continue # Empty plot
      p_drawObjects = map( lambda l:tex.DrawLatex(*l), getattr(plot, "drawObjects", [] ) )

      plotting.draw(plot,
        plot_directory = plot_directory_,
        #ratio          = {'yRange':(0.6,1.4)} if len(plot.stack)>=2 else None,
        logX = False, logY = log, sorting = False,
        yRange         = (0.0003, "auto") if log else (0.001, "auto"),
        #scaling        = {0:1} if len(plot.stack)==2 else {},
        legend         = [ (0.15,0.91-0.035*5,0.95,0.91), 2 ],
        drawObjects    = drawObjects( dataMCScale , lumi ) + p_drawObjects
      )

# Formatting for 1D plots
def drawPtResponse(plots, dataMCScale):
  for log in [ True]:
    plot_directory_ = os.path.join(plot_directory, ("log" if log else "") )
    for plot in plots:
      #if not max(l[0].GetMaximum() for l in plot.histos): continue # Empty plot
      p_drawObjects = map( lambda l:tex.DrawLatex(*l), getattr(plot, "drawObjects", [] ) )
      p_drawObjects.append( tex.DrawLatex( 0.20, 0.75, "using Gaussian fit" if args.useFit else "using mean of histogram" ) )

      plotting.draw(plot,
        plot_directory = plot_directory_,
        ratio          = {'yRange':(0.9,1.1)} ,
        logX = True, logY = False, sorting = False,
        yRange         = (0.5, 1.5),
        #scaling        = {0:1} if len(plot.stack)==2 else {},
        legend         = [ (0.15,0.91-0.035*2,0.95,0.91), 2 ],
        drawObjects    = drawObjects( dataMCScale , lumi ) + p_drawObjects
      )

#
# Logger
#
import JetMET.tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)


from JetMET.JEC.samples.L2res_skim import *

if args.era == 'Run2016':
    data = JetHT_Run2016
elif args.era == 'Run2016BCD':
    data = JetHT_Run2016BCD
elif args.era == 'Run2016EFearly':
    data = JetHT_Run2016EFearly
elif args.era == 'Run2016FlateG':
    data = JetHT_Run2016FlateG
elif args.era == 'Run2016H':
    data = JetHT_Run2016H


if args.triggers=='DiPFJetAve':
    triggers = [ 
        "HLT_DiPFJetAve40",
        "HLT_DiPFJetAve60",
        "HLT_DiPFJetAve80",
        "HLT_DiPFJetAve140",
        "HLT_DiPFJetAve200",
        "HLT_DiPFJetAve260",
        "HLT_DiPFJetAve320",
        "HLT_DiPFJetAve400",
        "HLT_DiPFJetAve500",
    ]
elif args.triggers == 'PFJet':
    triggers = [
        "HLT_PFJet40",
        "HLT_PFJet60",
        "HLT_PFJet80",
        "HLT_PFJet140",
        "HLT_PFJet200",
        "HLT_PFJet260",
        "HLT_PFJet320",
        "HLT_PFJet400",
        "HLT_PFJet450",
        "HLT_PFJet500",
    ]
elif args.triggers == 'DiPFJetAve_HFJEC':
    triggers = [
        "HLT_DiPFJetAve60_HFJEC",
        "HLT_DiPFJetAve80_HFJEC",
        "HLT_DiPFJetAve100_HFJEC",
        "HLT_DiPFJetAve160_HFJEC",
        "HLT_DiPFJetAve220_HFJEC",
        "HLT_DiPFJetAve300_HFJEC",
    ]
else:
    triggers = [ args.triggers ]

mc = QCD_Pt
samples = [ mc, data ]

selection = [
   ("tgb", "abs(Jet_eta[tag_jet_index])<1.3"),
   ("btb", "cos(Jet_phi[tag_jet_index] - Jet_phi[probe_jet_index]) < cos(2.7)"),
   ("a30", "alpha<0.3"), 
]

if args.phEF>0:
    selection.append( ("phEFprobe", "abs(Jet_phEF[probe_jet_index])<%f" % args.phEF ) )
if args.metOverSumET:
    selection.append( ("MOSET", "met_chsPt/chsSumPt<0.2" ) )

for s in samples:   
    s.addSelectionString( "&&".join(c[1] for c in selection))
    if args.small:
        s.reduceFiles( to = 1 )

# Add trigger selection to data
data.addSelectionString( "("+"||".join(triggers)+")")
if args.cleaned:
    from JetMET.JEC.L2res.jet_cleaning import jet_cleaning
    data.addSelectionString( jet_cleaning )
    mc.addSelectionString( jet_cleaning )


#colors = [ ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta, ROOT.kOrange, ROOT.kViolet,  ROOT.kCyan, ROOT.kOrange - 1, ROOT.kViolet - 1, ROOT.kCyan + 3]
colors = [ j+1 for j in range(0,9) ] + [ j+31 for j in range(9,18) ]

from JetMET.JEC.L2res.thresholds import pt_avg_thresholds, pt_avg_bins, eta_thresholds, abs_eta_thresholds

thresholds = [-1.2+x*2.4/96. for x in range(97)]

weightString  = "weight"

results_file        = os.path.join( plot_directory, 'results.pkl' )

h = {}
p = {}

if os.path.exists( results_file ) and not args.overwrite:
    h, p = pickle.load( file (results_file ) )
    logger.info( "Loaded %s", results_file )
else: 
    for var in [ "A", "B" ]:
        h[var] = {}
        p[var] = {}
        for s in samples:
            logger.info( "Make TH3D for sample %s and variable %s", s.name, var )
            h[var][s.name] = ROOT.TH3D( "h_%s_%s"%( var, s.name), "h_%s_%s"%(var, s.name),\
                    len(thresholds) - 1, array.array('d', thresholds), 
                    len(eta_thresholds)-1, array.array('d', eta_thresholds), 
                    len(pt_avg_thresholds) - 1, array.array('d', pt_avg_thresholds)  
                )

            weight_ = "("+s.selectionString+")*("+s.combineWithSampleWeight(weightString)+")"
            varString_ = pt_binning_variable+":Jet_eta[probe_jet_index]:%s>>h_%s_%s"%( var, var, s.name )

            logger.info("Using %s %s", varString_, weight_ ) 
            s.chain.Draw( varString_, weight_, 'goff')
            
            #logger.info( "Make TProfile2D for sample %s and variable %s", s.name, var )
            #p[var][s.name] = ROOT.TProfile2D( "p_%s_%s"%( var, s.name ), "p_%s_%s"%( var, s.name ),\
            #        len(eta_thresholds)-1, array.array('d', eta_thresholds), 
            #        len(pt_avg_thresholds) - 1, array.array('d', pt_avg_thresholds)  
            #    )
            #s.chain.Draw(pt_binning_variable+":Jet_eta[probe_jet_index]:%s>>p_%s,%s"%( var, var, s.name ),  "("+s.selectionString+")*("+s.combineWithSampleWeight(weightString)+")", 'goff')

    if not os.path.exists(os.path.dirname( results_file )): os.makedirs( os.path.dirname( results_file ) ) 
    pickle.dump( ( h, p ), file( results_file, 'w' ) )
    logger.info( "Written %s", results_file )

# Make all the projections
# x ... A,B
# y ... eta
# z ... pt_avg
projections          = {} # Used to store projections of TH3D
for var in [ "A", "B" ]:
    projections[var]          = {}
    for s in samples:
        projections[var][s.name] = {'neg_eta':{}, 'pos_eta':{}, 'abs_eta':{}}
        for i_aeta in range(len(abs_eta_thresholds)-1):
            eta_bin     = tuple(abs_eta_thresholds[i_aeta:i_aeta+2])
            neg_eta_bin = (-eta_bin[1], -eta_bin[0])
            bin_y       = h[var][s.name].GetYaxis().FindBin( 0.5*sum(eta_bin)  ) 
            neg_bin_y   = h[var][s.name].GetYaxis().FindBin( 0.5*sum(neg_eta_bin)  ) 

            projections[var][s.name]['neg_eta'][eta_bin] = {}
            projections[var][s.name]['pos_eta'][eta_bin] = {}
            projections[var][s.name]['abs_eta'][eta_bin] = {}

            for i_pt_avg in range(len(pt_avg_thresholds)-1):
                pt_avg_bin = tuple(pt_avg_thresholds[i_pt_avg:i_pt_avg+2])
                bin_z      = h[var][s.name].GetZaxis().FindBin( 0.5*sum(pt_avg_bin)  ) 
                projections[var][s.name]['abs_eta'][eta_bin][pt_avg_bin] = h[var][s.name].ProjectionX("abs_%s_%s_%i_%i" % ( s.name, var, bin_y, bin_z ) , bin_y, bin_y, bin_z, bin_z)
                projections[var][s.name]['pos_eta'][eta_bin][pt_avg_bin] = h[var][s.name].ProjectionX("pos_%s_%s_%i_%i" % ( s.name, var, bin_y, bin_z ) , bin_y, bin_y, bin_z, bin_z)
                projections[var][s.name]['neg_eta'][eta_bin][pt_avg_bin] = h[var][s.name].ProjectionX("neg_%s_%s_%i_%i" % ( s.name, var, neg_bin_y, bin_z ) , neg_bin_y, neg_bin_y, bin_z, bin_z)
                projections[var][s.name]['abs_eta'][eta_bin][pt_avg_bin].Add( projections[var][s.name]['neg_eta'][eta_bin][pt_avg_bin] ) 


            if not args.skipResponsePlots:
                for sign in ['neg_eta', 'pos_eta', 'abs_eta']:
                    histos = []
                    for i_pt_avg_bin, pt_avg_bin in enumerate(pt_avg_bins):
                        histos.append( projections[var][s.name][sign][eta_bin][pt_avg_bin].Clone())
                        histos[-1].style = styles.lineStyle( colors[ i_pt_avg_bin ] ) 
                        histos[-1].legendText = "%i #leq %s < %i" % ( pt_avg_bin[0], pt_binning_legendText, pt_avg_bin[1] )

                        # Normalize to 1
                        integral = histos[-1].Integral()
                        if integral>0: histos[-1].Scale(1./integral)

                    if sign    == 'pos_eta':
                        eta_tex_string       = "%4.3f #leq #eta < %4.3f" % ( eta_bin ) 
                    elif sign  == 'abs_eta':
                        eta_tex_string       = "%4.3f #leq |#eta| < %4.3f" % ( eta_bin ) 
                    elif sign  == 'neg_eta':
                        eta_tex_string       = "%4.3f #leq #eta < %4.3f" % ( -eta_bin[1], -eta_bin[0] ) 

                    name = "%s_%s_%s_%i_%i" % ( s.name.replace('_'+args.era, ''), var, sign, 1000*eta_bin[0], 1000*eta_bin[1] )
                    plot = Plot.fromHisto( name, [ [histo] for histo in histos], texX = var, texY = "Number of Events" )    
                    plot.drawObjects  = [ (0.2, 0.65, eta_tex_string ) ]
                    plot.drawObjects += [ (0.75, 0.95, '%s-symmetry' % var ) ]
                    draw1DPlots( [plot], 1.)


response_results_file    = os.path.join( plot_directory, 'response_results.pkl' )
if os.path.exists( response_results_file ):
    response = pickle.load( response_results_file )
    logger.info( 'Loaded response results from %s', response_results_file )
else:
    response = {} # results
    for var in [ "A", "B" ]:
        response[var] = {}
        for s in samples:
            response[var][s.name] = {}
            for i_aeta in range(len(abs_eta_thresholds)-1):

                eta_bin = tuple(abs_eta_thresholds[i_aeta:i_aeta+2])
                response[var][s.name][eta_bin] \
                        = {k:ROOT.TH1D('rel_corr_'+k, 'rel_corr_'+k, len(pt_avg_thresholds) - 1, array.array('d', pt_avg_thresholds)) for k in ['neg_eta', 'pos_eta', 'abs_eta']}

                for sign in [ 'neg_eta', 'pos_eta', 'abs_eta' ]:
                    for i_pt_avg_bin, pt_avg_bin in enumerate(pt_avg_bins):

                        # make life easy
                        shape = projections[var][s.name][sign][eta_bin][pt_avg_bin]
                        h     = response[var][s.name][eta_bin][sign]

                        if (args.useFit):
                            mean_asymmetry, mean_asymmetry_error = gaussianFit( 
                                shape               = shape,
                                isData              = s.name == data.name,
                                var_name            = "%s-symmetry" % var, 
                                fit_plot_directory  = os.path.join( plot_directory, 'fit'), 
                                fit_filename        = "fitresult_%s_%s_%i_%i_pt_%i_%i_%s" % ( var, sign, 1000*eta_bin[0], 1000*eta_bin[1], pt_avg_bin[0], pt_avg_bin[1], s.name ) 
                                )

                        else:
                            mean_asymmetry        = shape.GetMean()           
                            mean_asymmetry_error  = shape.GetMeanError() 

                        mean_response = (1 + mean_asymmetry)/(1 - mean_asymmetry)
                        mean_response_error = 2.*mean_asymmetry_error/(1 - mean_asymmetry)**2 # f(x) = (1+x)/(1-x) -> f'(x) = 2/(x-1)**2

                        if mean_response_error/mean_response<0.1:
                        
                            h.SetBinContent( h.FindBin( 0.5*sum(pt_avg_bin) ), mean_response ) 
                            h.SetBinError  ( h.FindBin( 0.5*sum(pt_avg_bin) ), mean_response_error ) 

                    response[var][s.name][eta_bin][sign].style = styles.lineStyle( 
                        color = ROOT.kBlack if s.name == data.name else ROOT.kRed,
                        dashed = (var == 'A'),
                        errors = True
                        )
                    response[var][s.name][eta_bin][sign].legendText = s.name + "( %s )" % ("Bal." if var=='A' else "MPF")

    pickle.dump( response, file(response_results_file, 'w') ) 
    logger.info( 'Written response results to %s', response_results_file )

for i_aeta in range(len(abs_eta_thresholds)-1):

    eta_bin = tuple(abs_eta_thresholds[i_aeta:i_aeta+2])

    for sign in [ 'neg_eta', 'pos_eta', 'abs_eta' ]:
        
        name = "response_%s_%s_%i_%i" % ( "fit" if args.useFit else "mean", sign, 1000*eta_bin[0], 1000*eta_bin[1] )
        plot = Plot.fromHisto( name, 
            [ 
              [response['B'][mc.name][eta_bin][sign]] , 
              [response['B'][data.name][eta_bin][sign]], 
              [response['A'][mc.name][eta_bin][sign]] , 
              [response['A'][data.name][eta_bin][sign]] 
            ], 
            texX = pt_binning_legendText, texY = "response" ) 
        drawPtResponse( [plot], 1.)

