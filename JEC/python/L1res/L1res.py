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
argParser.add_argument('--small',                                   action='store_true',     help='Run only on a small subset of the data?', default = True)
#argParser.add_argument('--overwrite',                               action='store_true',     help='Overwrite?')
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
def draw1DPlots(plots, dataMCScale):
  for log in [ False, True ]:
    plot_directory_ = os.path.join(plot_directory, ("log" if log else "lin") )
    for plot in plots:
      #if not max(l[0].GetMaximum() for l in plot.histos): continue # Empty plot
      p_drawObjects = map( lambda l:tex.DrawLatex(*l), getattr(plot, "drawObjects", [] ) )
      plotting.draw(plot,
        plot_directory = plot_directory_,
        #ratio          = {'yRange':(0.6,1.4)} if len(plot.stack)>=2 else None,
        logX = False, logY = log, sorting = False,
        yRange         = (0.0003, "auto") if log else (0, "auto"),
        #scaling        = {0:1} if len(plot.stack)==2 else {},
        legend         = [ (0.15,0.91-0.035*5,0.95,0.91), 2 ],
        drawObjects    = drawObjects( dataMCScale , lumi ) + p_drawObjects
      )

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
    ( "filter",  getFilterCut( positiveWeight = False, badMuonFilters = "Moriond2017" ) ),  
]

for s in samples:   
    s.addSelectionString( "&&".join(c[1] for c in selection))
    if args.small:
        s.reduceFiles( to = 1 )

## relevant branches:
#nOffset nOffset/I
#Offset_e_lost   Component e_lost for offset density
#Offset_e_all    Component e_all for offset density
#Offset_e_unm    Component e_unm for offset density
#Offset_e_ch Component e_ch for offset density
#Offset_e_nh Component e_nh for offset density
#Offset_e_ph Component e_ph for offset density
#Offset_e_ele    Component e_ele for offset density
#Offset_e_mu Component e_mu for offset density
#Offset_e_hhf    Component e_hhf for offset density
#Offset_e_ehf    Component e_ehf for offset density
#Offset_et_all   Component et_all for offset density
#Offset_e_rms    Component e_rms for offset density

colors = [ j+1 for j in range(0,9) ] + [ j+31 for j in range(9,18) ]
texNames = {
    'Offset_e_ch':"charged", 
    'Offset_e_nh':"neutrals", 
    'Offset_e_ph':"photons"
}

# Eta thresholds (need to be aligned with ntuple production step)
from JetMET.JEC.L1res.thresholds import offset_eta_thresholds 

# rather awkward way to use TTree Draw

binning_int = [ len(offset_eta_thresholds) - 1, 0, len(offset_eta_thresholds) - 1 ]
histos = []
for i_offset, offset in enumerate(["Offset_e_ch", "Offset_e_nh", "Offset_e_ph"]):

    logger.info( "Draw: Obtain offset histo %s for sample %s", offset, mc.name )

    # make histo with x-axis being the fixed-size vector index Iteration$ that counts from 0 to size-1
    h       = mc.get1DHistoFromDraw("Iteration$", binning = binning_int, weightString = offset)

    # make new histogram with same number of bins but proper eta thresholds
    h_eta   = ROOT.TH1D(h.GetName()+'_eta', h.GetTitle(), len(offset_eta_thresholds)-1, array.array('d', offset_eta_thresholds) )
    for i in range( h.GetNbinsX() + 1 ):
        h_eta.SetBinContent(i, h.GetBinContent( i ) )
        h_eta.SetBinError(i,   h.GetBinError( i ) )

    # divide by nEvents
    h_eta.Scale(1./h.GetEntries())
    h_eta.legendText = texNames[offset] if texNames.has_key(offset) else offset 
    h_eta.style  = styles.lineStyle(colors[i_offset], errors = True )
    histos.append( [h_eta] )

plot = Plot.fromHisto(name = "Offsets_energy_draw", histos = histos, texX = "#eta", texY = "Offset energy" )
draw1DPlots( [plot], 1. )


# using event loop

#
# Read variables
#
variables = [
        "evt/l", "run/I", "lumi/I", 
        "nOffset/I", "Offset[e_lost/F,e_all/F,e_unm/F,e_ch/F,e_nh/F,e_ph/F,e_ele/F,e_mu/F,e_hhf/F,e_ehf/F,et_all/F,e_rms/F]"
    ]

#
# Execution sequence
#

sequence = []

def offsetStuff( event, sample ):
    # Add here any calculations you might want to do in the loop

    #print event.evt, event.nOffset

    # dummy
    event.dummy = event.nOffset

    return

sequence.append( offsetStuff )

max_events = 500 if args.small else None

histos = {}

offsets = ["Offset_e_ch", "Offset_e_nh", "Offset_e_ph"]

# to speed up filling enumerate eta bins
eta_bins = [ (i, 0.5*(offset_eta_thresholds[i]+offset_eta_thresholds[i+1])) for i in xrange( len(offset_eta_thresholds)-1) ]

for sample in samples:

    # Make ROOT histos
    histos[sample.name] = { offset:  
        ROOT.TH1D( '%s_%s_eta' % (sample.name, offset), '%s_%s_eta' % (sample.name, offset), 
                   len(offset_eta_thresholds)-1, array.array('d', offset_eta_thresholds) )  for offset in offsets }

    # TreeReader for sample
    reader = sample.treeReader( 
        variables = map( TreeVariable.fromString, variables ) , 
        selectionString = "1"
        )
    logger.info( "Loop: Obtain offset histos %s for sample %s", ','.join(offsets), sample.name )

    reader.start()

    
    count = 0
    while reader.run():

        for bin_i, bin_eta in eta_bins: 
            for offset in offsets:
                # Fill histogram with the Offset energy in the bin bin_i/bin_eta
                histos[sample.name][offset].Fill( bin_eta, getattr( reader.event, offset )[bin_i] )

        count+=1
        if max_events is not None and max_events>0 and count>=max_events:break


    # divide by nEvents
    for i_offset, offset in enumerate( offsets ):
        h = histos[sample.name][offset] 
        h.Scale(1./count)
        h.legendText = texNames[offset] if texNames.has_key(offset) else offset 
        h.style  = styles.lineStyle(colors[i_offset], errors = True )

plot = Plot.fromHisto(name = "Offsets_energy_loop", 
    histos = [ [ histos[mc.name][offset] ] for offset in offsets ], 
    texX = "#eta", texY = "Offset energy" )

draw1DPlots( [ plot ], 1. )
