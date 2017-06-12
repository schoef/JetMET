#!/usr/bin/env python
''' Analysis script for L2 residual / offset 
'''
#
# Standard imports and batch mode
#
import ROOT
ROOT.gROOT.SetBatch(True)

import itertools
import os
import array
import pickle

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
argParser.add_argument('--era',                action='store',      default='Run2016',       nargs='?', choices=['Run2016', 'Run2016BCD', 'Run2016EFearly', 'Run2016FlateG', 'Run2016H'], help="era" )
argParser.add_argument('--small',                                   action='store_true',     help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--overwrite',                               action='store_true',     help='Overwrite results.pkl?')
argParser.add_argument('--plot_directory',     action='store',      default='JEC/L1res',     help="subdirectory for plots")
args = argParser.parse_args()

#
# Logger
#
import JetMET.tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

if args.small:
    args.plot_directory += '_small'

plot_directory = os.path.join( user_plot_directory, args.plot_directory )

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

## Formatting for 1D plots
#def draw1DPlots(plots, dataMCScale):
#  for log in [ True]:
#    plot_directory_ = os.path.join(plot_directory, ("log" if log else "") )
#    for plot in plots:
#      #if not max(l[0].GetMaximum() for l in plot.histos): continue # Empty plot
#      p_drawObjects = map( lambda l:tex.DrawLatex(*l), getattr(plot, "drawObjects", [] ) )
#
#      plotting.draw(plot,
#        plot_directory = plot_directory_,
#        #ratio          = {'yRange':(0.6,1.4)} if len(plot.stack)>=2 else None,
#        logX = False, logY = log, sorting = False,
#        yRange         = (0.0003, "auto") if log else (0.001, "auto"),
#        #scaling        = {0:1} if len(plot.stack)==2 else {},
#        legend         = [ (0.15,0.91-0.035*5,0.95,0.91), 2 ],
#        drawObjects    = drawObjects( dataMCScale , lumi ) + p_drawObjects
#      )
#
## Formatting for 1D plots
#def drawPtResponse(plots, dataMCScale):
#  for log in [ True]:
#    plot_directory_ = os.path.join(plot_directory, ("log" if log else "") )
#    for plot in plots:
#      #if not max(l[0].GetMaximum() for l in plot.histos): continue # Empty plot
#      p_drawObjects = map( lambda l:tex.DrawLatex(*l), getattr(plot, "drawObjects", [] ) )
#      p_drawObjects.append( tex.DrawLatex( 0.20, 0.75, "using Gaussian fit" if args.useFit else "using mean of histogram" ) )
#
#      plotting.draw(plot,
#        plot_directory = plot_directory_,
#        ratio          = {'yRange':(0.9,1.1)} ,
#        logX = True, logY = False, sorting = False,
#        yRange         = (0.5, 1.5),
#        #scaling        = {0:1} if len(plot.stack)==2 else {},
#        legend         = [ (0.15,0.91-0.035*2,0.95,0.91), 2 ],
#        drawObjects    = drawObjects( dataMCScale , lumi ) + p_drawObjects
#      )


from JetMET.JEC.samples.L1res_master import *

if args.era == 'Run2016':
    data = ZeroBias_Run2016
elif args.era == 'Run2016BCD':
    data = ZeroBias_Run2016BCD
elif args.era == 'Run2016EFearly':
    data = ZeroBias_Run2016EFearly
elif args.era == 'Run2016FlateG':
    data = ZeroBias_Run2016FlateG
elif args.era == 'Run2016H':
    data = ZeroBias_Run2016H

mc = SingleNeutrino
samples = [ mc, data ]

selection = [
]

for s in samples:   
    s.addSelectionString( "&&".join(c[1] for c in selection))
    if args.small:
        s.reduceFiles( to = 1 )

# Add trigger selection to data
data.addSelectionString( getFilterCut( isData = False, badMuonFilters = "Moriond2017" ) ) # always apply MC version. Data version has 'weight>0' which is not for master ntuples

colors = [ j+1 for j in range(0,9) ] + [ j+31 for j in range(9,18) ]

#h[var][s.name] = ROOT.TH3D( "h_%s_%s"%( var, s.name), "h_%s_%s"%(var, s.name),\
#        len(thresholds) - 1, array.array('d', thresholds), 
#        len(eta_thresholds)-1, array.array('d', eta_thresholds), 
#        len(pt_avg_thresholds) - 1, array.array('d', pt_avg_thresholds)  
#    )
#
#weight_ = "("+s.selectionString+")*("+s.combineWithSampleWeight(weightString)+")"
#varString_ = pt_binning_variable+":Jet_eta[probe_jet_index]:%s>>h_%s_%s"%( var, var, s.name )
#
#logger.info("Using %s %s", varString_, weight_ ) 
#s.chain.Draw( varString_, weight_, 'goff')
#
