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
argParser.add_argument('--logLevel',           action='store',      default='INFO',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging" )
argParser.add_argument('--triggers',           action='store',      default='DiPFJetAve',    nargs='?', choices=['DiPFJetAve', 'DiPFJetAve_HFJEC', 'PFJet'], help="trigger suite" )
argParser.add_argument('--era',                action='store',      default='Run2016',       nargs='?', choices=['Run2016', 'Run2016BCD', 'Run2016EFearly', 'Run2016FlateG', 'Run2016H'], help="era" )
argParser.add_argument('--small',                                   action='store_true',     help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--plot_directory',     action='store',      default='JEC/L2res_trigger',     help="subdirectory for plots")
args = argParser.parse_args()

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
      (0.45, 0.95, 'L=%3.1f fb{}^{-1} (13 TeV) Scale %3.2f'% ( lumi, dataMCScale ) )
    ]
    return [tex.DrawLatex(*l) for l in lines] 

# Formatting for 1D plots
def draw1DPlots(plots, dataMCScale):
  for log in [ True]:
    plot_directory_ = os.path.join(plot_directory, ("log" if log else "") )
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
        legend         = (0.55,0.91-0.035*10,0.95,0.91),
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

mc = QCD_Pt

samples = [mc, data]

selection = [
   ("btb", "cos(Jet_phi[tag_jet_index] - Jet_phi[probe_jet_index]) < cos(2.7)"),
   ("a30", "alpha<0.3"), 
]

for s in samples:   
    s.addSelectionString( "&&".join(c[1] for c in selection))
    if args.small:
        s.reduceFiles( to = 1 )

colors = [ ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta, ROOT.kOrange, ROOT.kViolet,  ROOT.kCyan, ROOT.kOrange - 1, ROOT.kViolet - 1, ROOT.kCyan + 3]

variableString = "pt_avg"
binning        = [100,0,1000]
weightString   = "weight"


h_MC =      mc.get1DHistoFromDraw(variableString = variableString, binning = binning, weightString=weightString+"*%f" % lumi )
h_data    = {t:data.get1DHistoFromDraw(variableString = variableString, binning = binning, weightString=weightString+"&& %s "% t) for t in triggers }
h_data_ps = {t:data.get1DHistoFromDraw(variableString = variableString, binning = binning, weightString="("+weightString+")*HLT_BIT_%s_v_Prescale * (%s==1) "% (t,t) ) for t in triggers }


h_MC.style = styles.lineStyle( ROOT.kBlack ) 
h_MC.legendText = "QCD Pt binned"
for i, t in enumerate( triggers ):
    h_data[t].style = styles.lineStyle( colors[ i ], dashed = True ) 
    #h_data[t].legendText = t 
    h_data_ps[t].style = styles.lineStyle( colors[ i ] ) 
    h_data_ps[t].legendText = t 

histos_data = [[h_data[t]] for t in triggers] +   [[h_data_ps[t]] for t in triggers]

plot = Plot.fromHisto( variableString, [ [ h_MC ] ] + histos_data, texX = "p_{T} avg. (GeV)", texY = "Number of Events" )    
draw1DPlots( [plot], 1.)
