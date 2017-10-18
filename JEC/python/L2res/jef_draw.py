#!/usr/bin/env python
''' Analysis script for L3 residuals (Z balancing) 
'''
#
# Standard imports and batch mode
#
import ROOT
ROOT.gROOT.SetBatch(True)
import itertools
import os

from math                                import sqrt, cos, sin, pi, atan2
from RootTools.core.standard             import *
from JetMET.tools.user                   import plot_directory as user_plot_directory
from JetMET.tools.helpers                import deltaPhi, deltaR

# Object selection
from JetMET.tools.objectSelection        import getFilterCut, getJets, jetVars

#
# Arguments
# 
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO',            nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging" )
argParser.add_argument('--triggers',           action='store',      default='exclDiPFJetAveHFJEC', nargs='?', choices=['DiPFJetAve', 'DiPFJetAve_HFJEC', 'PFJet', 'exclPFJet', 'exclDiPFJetAve', 'exclDiPFJetAveHFJEC'], help="trigger suite" )
argParser.add_argument('--observable',         action='store',      default='phEF',            nargs='?', choices=['phi', 'phEF', 'eEF', 'muEF', 'HFHEF', 'HFEMEF', 'chHEF', 'neHEF', 'phMult', 'eMult', 'muMult', 'HFHMult', 'HFEMMult', 'chHMult', 'neHMult'], help="Which jet observable?" )
argParser.add_argument('--ptBin',              action='store',      default=(163, 230),        type = int,    nargs=2,  help="tag jet pt bin" )
argParser.add_argument('--etaBin',             action='store',      default=(2.853, 2.964),    type = float,  nargs=2,  help="probe jet eta bin" )
argParser.add_argument('--etaSign',            action='store',      default=0             ,    type = int,    choices = [-1,0,+1], help="sign of probe jet eta." )
argParser.add_argument('--small',                                   action='store_true',       help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--cleaned',                                 action='store_true',       help='Apply jet cleaning in data')#, default = True)
argParser.add_argument('--bad',                                     action='store_true',       help='Cut on phEF*pT>300')#, default = True)
argParser.add_argument('--fraction',                                action='store_true',       help='plot energy fraction.')#, default = True)
argParser.add_argument('--plot_directory',     action='store',      default='JEC/L2res_jef_v11_07Aug17',  help="subdirectory for plots")
args = argParser.parse_args()

if args.cleaned:
    args.plot_directory += '_cleaned'
if args.bad:
    args.plot_directory += '_bad'
if args.small:
    args.plot_directory += '_small'

plot_directory = os.path.join( user_plot_directory, args.plot_directory, args.triggers )

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
      (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV) Scale %3.2f'% ( lumi, dataMCScale ) )
    ]
    return [tex.DrawLatex(*l) for l in lines] 

# simple helper to normalize histo
def normHisto( h ):
    integr = h.Integral()
    if integr>0:
        h.Scale(1./integr)


# Formatting for 1D plots
def draw1DPlots(plots, dataMCScale):
  for log in [ True, False]:
    plot_directory_ = os.path.join(plot_directory, ("log" if log else "lin") )
    for plot in plots:
      #if not max(l[0].GetMaximum() for l in plot.histos): continue # Empty plot
      p_drawObjects = map( lambda l:tex.DrawLatex(*l), getattr(plot, "drawObjects", [] ) )

      if hasattr( plot, "subdir"):
        plot_directory__ = os.path.join( plot_directory_, plot.subdir)
      else:
        plot_directory__ = plot_directory_

      plotting.draw(plot,
        plot_directory = plot_directory__,
        #ratio          = {'yRange':(0.6,1.4)} if len(plot.stack)>=2 else None,
        logX = False, logY = log, sorting = False,
        yRange         = (0.0003, "auto") if log else (0.001, "auto"),
        #scaling        = {0:1} if len(plot.stack)==2 else {},
        legend         = [ (0.15,0.91-0.035*5,0.95,0.91), 2],
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

data = [
#    JetHT_Run2016BCD,
#    JetHT_Run2016E,
#    JetHT_Run2016Fearly,
#    JetHT_Run2016Flate,
#    JetHT_Run2016G,
#    JetHT_Run2016H,
    JetHT_Run2016B,
    JetHT_Run2016C,
    JetHT_Run2016F,
    JetHT_Run2016G,
    JetHT_Run2016H,
]

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
elif args.triggers == 'exclPFJet':
    from JetMET.JEC.L2res.thresholds import exclPFJets
    triggers = [ exclPFJets ]
elif args.triggers == 'exclDiPFJetAve':
    from JetMET.JEC.L2res.thresholds import exclDiPFJetAve
    triggers = [ exclDiPFJetAve ]
elif args.triggers == 'exclDiPFJetAveHFJEC':
    from JetMET.JEC.L2res.thresholds import exclDiPFJetAveHFJEC
    triggers = [ exclDiPFJetAveHFJEC ]
else:
    triggers = [ args.triggers ]

#mc = QCD_Pt
#samples = [mc] +  data
samples = data

from JetMET.JEC.L2res.jet_cleaning import jet_cleaning
for s in data:
    s.addSelectionString( "("+"||".join(triggers)+")")
    if args.cleaned:
        s.addSelectionString( jet_cleaning )

selection = [
   ("btb", "cos(Jet_phi[tag_jet_index] - Jet_phi[probe_jet_index]) < cos(2.7)"),
   ("a30", "alpha<0.3"), 
]
if args.bad:
    selection.append( ("bad", "Jet_phEF[probe_jet_index]*Jet_pt[probe_jet_index]>250") )

#tag_jet_bin = (163, 230)
#probe_jet_abs_eta_bin = (2.853, 2.964 )
tag_jet_bin             = tuple(args.ptBin)
probe_jet_abs_eta_bin   = tuple(args.etaBin)
if args.etaSign   == -1:
    probe_jet_eta_cutstring = "-Jet_eta[probe_jet_index]"
    eta_string              = "negeta"
elif args.etaSign == +1:
    probe_jet_eta_cutstring = "Jet_eta[probe_jet_index]"
    eta_string              = "poseta"
elif args.etaSign ==  0:
    probe_jet_eta_cutstring = "abs(Jet_eta[probe_jet_index])"
    eta_string              = "abseta"

# kinematic selection on tag & probe jet
kinSelectionString = "%f<Jet_pt[tag_jet_index]&&Jet_pt[tag_jet_index]<%f&& %s > %f && %s < %f"% ( tag_jet_bin[0], tag_jet_bin[1], probe_jet_eta_cutstring, probe_jet_abs_eta_bin[0], probe_jet_eta_cutstring, probe_jet_abs_eta_bin[1] )
logger.info( "Jet selection: %s", kinSelectionString )

for s in samples:   
    s.addSelectionString( "&&".join(c[1] for c in selection))
    s.addSelectionString( kinSelectionString )
    if args.small:
        s.reduceFiles( to = 1 )

colors = [ j+1 for j in range(0,9) ] + [ j+31 for j in range(9,18) ]

variableString = "Jet_%s"%args.observable
weightString   = "weight"

if args.observable.endswith('EF'):
    if args.fraction:
        drawString     = "%s[probe_jet_index]" % variableString
        binning        = [30,0,1]
        texX           = args.observable
    else:
        drawString     = "%s[probe_jet_index]*Jet_pt[probe_jet_index]" % variableString
        binning        = [30,0,2*tag_jet_bin[1]]
        texX           = args.observable + "\cdot p_{T}"
elif args.observable.endswith('Mult'):
    binning        = [20,0,20]
    drawString     = "%s[probe_jet_index]" % variableString
    texX = args.observable
elif args.observable == 'phi':
    drawString     = "%s[probe_jet_index]" % variableString
    binning        = [90,-pi,pi]
    texX           = args.observable

#h_MC =      mc.get1DHistoFromDraw(variableString = drawString, binning = binning, weightString = weightString )
#normHisto(h_MC)

h_data    = {s.name:s.get1DHistoFromDraw(variableString = drawString, binning = binning, weightString=weightString) for s in data }

#h_MC.style = styles.lineStyle( ROOT.kBlack ) 
#h_MC.legendText = "QCD Pt binned"
for i, s in enumerate( data ):
    h_data[s.name].style = styles.lineStyle( colors[ i ], dashed = False ) 
    h_data[s.name].legendText = s.name
    normHisto(h_data[s.name])

histos_data = [[h_data[s.name]] for s in data] 

f_postfix = '_frac' if args.fraction else ''

plot = Plot.fromHisto( variableString+f_postfix+'_pt_%i_%i_%s_%i_%i' % ( tag_jet_bin[0], tag_jet_bin[1], eta_string, 1000*probe_jet_abs_eta_bin[0], 1000*probe_jet_abs_eta_bin[1]), 
#    [ [ h_MC ] ] + histos_data, texX = texX, texY = "Number of Events" 
    histos_data, texX = texX, texY = "Number of Events" 
    )
      
if args.etaSign == 0:
    eta_string = "|#eta_{probe}|"
elif args.etaSign == 1:
    eta_string = "#eta_{probe}"
elif args.etaSign == -1:
    eta_string = "-#eta_{probe}"

plot.drawObjects = [ 
    (0.55, 0.7, '%i #leq < p_{T,tag} < %i'% tag_jet_bin ),
    (0.55, 0.65, '%4.3f #leq %s < %4.3f'% ( probe_jet_abs_eta_bin[0], eta_string, probe_jet_abs_eta_bin[1] ) ),
]
 
draw1DPlots( [plot], 1.)
