#!/usr/bin/env python
''' Analysis script for the sanity of the third jet. 
'''
#
# Standard imports and batch mode
#
import ROOT
ROOT.gROOT.SetBatch(True)
import itertools
import os

from math                                import sqrt, cos, sin, pi, atan2, sinh
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
argParser.add_argument('--sample',             action='store',      default='Run2016H',      nargs='?', choices=['QCD_Pt', 'Run2016', 'Run2016BCD', 'Run2016EFearly', 'Run2016FlateG', 'Run2016H', 'Run2016_18Apr', 'Run2016BCD_18Apr', 'Run2016EFearly_18Apr', 'Run2016FlateG_18Apr', 'Run2016H_18Apr'], help="sample?" )
argParser.add_argument('--pt',                 action='store',      default='low',           nargs='?', choices=['low', 'high'], help="pt bin" )
argParser.add_argument('--small',                                   action='store_true',     help='Run only on a small subset of the data?', default = True)
argParser.add_argument('--uncleaned',                               action='store_true',     help='Dont apply jet cleaning in data')#, default = True)
argParser.add_argument('--plot_directory',     action='store',      default='JEC/L2res_sanity_v8',     help="subdirectory for plots")
args = argParser.parse_args()

if not args.uncleaned:
    args.plot_directory += '_cleaned'
if args.small:
    args.plot_directory += '_small'

plot_directory = os.path.join( user_plot_directory, args.plot_directory, args.sample )

# DrawLatex objects for plots
tex = ROOT.TLatex()
tex.SetNDC()
tex.SetTextSize(0.04)
tex.SetTextAlign(11) # align right
def drawObjects( dataMCScale ):
    lines = [
      #(0.15, 0.95, args.sample), 
      (0.65, 0.95, args.sample )
    ]
    return [tex.DrawLatex(*l) for l in lines] 

## Formatting for 2D plots
def draw2DPlots(plots, dataMCScale):
  for log in [ True, False]:
    plot_directory_ = os.path.join(plot_directory, ("log" if log else "lin") )
    for plot in plots:
      draw_obj = getattr(plot, "drawObjects", [])
      p_drawObjects = []
      for o in draw_obj:
        if type(o)==tuple:
            p_drawObjects.append( tex.DrawLatex(*o) )
        else:
            p_drawObjects.append( o )
      plotting.draw2D(plot,
        plot_directory = plot_directory_,
        logX = False, logY = False,
        drawObjects    = drawObjects( dataMCScale ) + p_drawObjects 
      )

# Formatting for 1D plots
def draw1DPlots(plots, dataMCScale):
  for log in [ False ]:
    plot_directory_ = os.path.join(plot_directory, ("log" if log else "lin") )
    for plot in plots:
      #if not max(l[0].GetMaximum() for l in plot.histos): continue # Empty plot
      #p_drawObjects = map( lambda l:tex.DrawLatex(*l), getattr(plot, "drawObjects", [] ) )
      p_drawObjects = getattr(plot, "drawObjects", [] ) 
      plotting.draw(plot,
        plot_directory = plot_directory_,
        #ratio          = {'yRange':(0.6,1.4)} if len(plot.stack)>=2 else None,
        logX = False, logY = log, sorting = False,
        #yRange         = (0.5, 1.5) ,
        #scaling        = {0:1} if len(plot.stack)==2 else {},
        legend         = [ (0.15,0.91-0.05*len(plot.histos)/2,0.95,0.91), 2 ],
        drawObjects    = drawObjects( dataMCScale ) + p_drawObjects
      )

#
# Logger
#
import JetMET.tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)


from JetMET.JEC.samples.L2res_skim import *

if args.sample == 'Run2016':
    sample = JetHT_Run2016
elif args.sample == 'Run2016BCD':
    sample = JetHT_Run2016BCD
elif args.sample == 'Run2016EFearly':
    sample = JetHT_Run2016EFearly
elif args.sample == 'Run2016FlateG':
    sample = JetHT_Run2016FlateG
elif args.sample == 'Run2016H':
    sample = JetHT_Run2016H
elif args.sample == 'QCD_Pt':
    sample = QCD_Pt

samples = [ sample ] 

for s in samples:
    s.setSelectionString( "(1)" )

from JetMET.JEC.L2res.jet_cleaning import jet_cleaning
if not args.uncleaned:
    sample.addSelectionString( jet_cleaning )

selection = [
   ("btb", "cos(Jet_phi[tag_jet_index] - Jet_phi[probe_jet_index]) < cos(2.7)"),
#   ("tagJet", "Jet_pt[tag_jet_index]>50&&Jet_pt[tag_jet_index]<100"),
#   ("a30", "alpha<0.3"),
]
if args.pt=='high':
    selection.append( ("tagJet", "Jet_pt[tag_jet_index]>250") )
    if 'Run' not in args.sample: sample.addSelectionString( "HLT_PFJet200" )
elif args.pt=='low':   
    selection.append( ("tagJet", "Jet_pt[tag_jet_index]>50&&Jet_pt[tag_jet_index]<100") )
    if 'Run' not in args.sample: sample.addSelectionString( "HLT_PFJet40" )

sample.addSelectionString( "&&".join(c[1] for c in selection))
if args.small:
    sample.reduceFiles( to = 1 )

## alpha vs. probe jet eta
#weightString   = "weight"
#variableString = "alpha:Jet_eta[probe_jet_index]"
#binning = [52, -5.2, 5.2, 40, 0, 1] 
#logger.info( "Get plot with %s, and weight '%s' and sample selection %s", variableString, weightString, sample.selectionString )
#h    = sample.get2DHistoFromDraw(variableString = variableString, binning = binning, weightString=weightString) 
#plot = Plot2D.fromHisto( name = ( '2D_pt_%s_alpha_vs_probe_jet_eta'%args.pt ), 
#    histos = [[ h ]], texY = "#alpha", texX = "#eta(probe jet)" 
#    )
#draw2DPlots( [plot], 1.)
#
## dphi(2,3)  vs. probe jet eta
#weightString   = "weight&&(third_jet_index>0)"
#variableString = "cos(Jet_phi[probe_jet_index] - Jet_phi[third_jet_index]):Jet_eta[probe_jet_index]"
#binning = [52, -5.2, 5.2, 40, -1, 1] 
#logger.info( "Get plot with %s, and weight '%s' and sample selection %s", variableString, weightString, sample.selectionString )
#h    = sample.get2DHistoFromDraw(variableString = variableString, binning = binning, weightString=weightString) 
#plot = Plot2D.fromHisto( name = ( '2D_pt_%s_dPhiJet23_vs_eta_probe_jet'%args.pt ), 
#    histos = [[ h ]], texY = "cos(#Delta#phi(j_{2},j_{3}))", texX = "#eta(probe jet)" 
#    )
#draw2DPlots( [plot], 1.)

# minDphi(ETmiss,1,2,3)  vs. probe jet eta
weightString   = "weight"
variableString = "MaxIf$(abs(cos(met_chsPhi - Jet_phi)), Jet_pt>30&&Iteration$<5)"
binning = [ 40, 0, 1] 
logger.info( "Get plot with %s, and weight '%s' and sample selection %s", variableString, weightString, sample.selectionString )
h    = sample.get1DHistoFromDraw(variableString = variableString, binning = binning, weightString=weightString) 
plot = Plot.fromHisto( name = ( '1D_pt_%s_maxCosdPhiMETJets'%args.pt ), 
    histos = [[ h ]], texX = "max cos(|#Delta#phi(MET, jets)|)", texY = "Events" 
    )
draw1DPlots( [plot], 1.)

weightString   = "weight"
variableString = "MaxIf$(abs(cos(met_chsPhi - Jet_phi)), Jet_pt>30&&Iteration$<5):Jet_eta[probe_jet_index]"
binning = [52, -5.2, 5.2, 40, 0, 1] 
logger.info( "Get plot with %s, and weight '%s' and sample selection %s", variableString, weightString, sample.selectionString )
h2D    = sample.get2DHistoFromDraw(variableString = variableString, binning = binning, weightString=weightString) 
plot2D = Plot2D.fromHisto( name = ( '2D_pt_%s_maxCosdPhiMETJets_vs_eta_probe_jet'%args.pt ), 
    histos = [[ h2D ]], texY = "max cos(|#Delta#phi(MET, jets)|)", texX = "#eta(probe jet)" 
    )
draw2DPlots( [plot2D], 1.)

## extra activity beyond the third jet
#weightString   = "weight&&(third_jet_index>0)"
#variableString = "cos(Jet_phi[probe_jet_index] - Jet_phi[third_jet_index]):Jet_eta[probe_jet_index]"
#binning = [52, -5.2, 5.2, 40, -1, 1] 
#logger.info( "Get plot with %s, and weight '%s' and sample selection %s", variableString, weightString, sample.selectionString )
#h    = sample.get2DHistoFromDraw(variableString = variableString, binning = binning, weightString=weightString) 
#plot = Plot2D.fromHisto( name = ( '2D_pt_%s_dPhiJet23_vs_eta_probe_jet'%args.pt ), 
#    histos = [[ h ]], texY = "cos(#Delta#phi(j_{2},j_{3}))", texX = "#eta(probe jet)" 
#    )
#draw2DPlots( [plot], 1.)
