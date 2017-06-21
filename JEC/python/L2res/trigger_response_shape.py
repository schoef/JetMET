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
argParser.add_argument('--trigger',            action='store',      default='DiPFJetAve',    nargs='?', help="trigger requirement" )
argParser.add_argument('--variable',           action='store',      default='B',             choices = ['A', 'B'], nargs='?', help="variables" )
argParser.add_argument('--ptBin',              action='store',      default=(365, 435),      type = int,    nargs=2,  help="pt average bin" )
argParser.add_argument('--etaBin',             action='store',      default=(0., 0.261),     type = float,  nargs=2,  help="probe jet eta bin" )
argParser.add_argument('--etaSign',            action='store',      default=0             ,  type = int,    choices = [-1,0,+1], help="sign of probe jet eta." )
argParser.add_argument('--era',                action='store',      default='Run2016H',      nargs='?', choices=['Run2016', 'Run2016BCD', 'Run2016EFearly', 'Run2016FlateG', 'Run2016H'], help="era" )
argParser.add_argument('--small',                                   action='store_true',     help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--plot_directory',     action='store',      default='JEC/L2res_trigger_v8',     help="subdirectory for plots")
args = argParser.parse_args()

if args.small:
    args.plot_directory += '_small'

plot_directory = os.path.join( user_plot_directory, args.plot_directory, args.era, args.trigger )

# DrawLatex objects for plots
tex = ROOT.TLatex()
tex.SetNDC()
tex.SetTextSize(0.04)
tex.SetTextAlign(11) # align right
def drawObjects( dataMCScale ):
    lines = [
      #(0.15, 0.95, args.era), 
      (0.8, 0.95, args.era )
    ]
    return [tex.DrawLatex(*l) for l in lines] 

# Formatting for 1D plots
def draw1DPlots(plots, dataMCScale):
  for log in [ True]:
    plot_directory_ = os.path.join(plot_directory, ("log" if log else "") )
    for plot in plots:
      p_drawObjects = map( lambda l:tex.DrawLatex(*l), getattr(plot, "drawObjects", [] ) )
      plotting.draw(plot,
        plot_directory = plot_directory_,
        logX = False, logY = log, sorting = False,
        yRange         = (0.0003, "auto") if log else (0.001, "auto"),
        legend         = [ (0.15,0.91-0.025*len(plot.histos),0.95,0.91), 2],
        drawObjects    = drawObjects( dataMCScale ) + p_drawObjects  )
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

if args.trigger=='DiPFJetAve':
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
elif args.trigger == 'PFJet':
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
elif args.trigger == 'DiPFJetAve_HFJEC':
    triggers = [
        "HLT_DiPFJetAve60_HFJEC",
        "HLT_DiPFJetAve80_HFJEC",
        "HLT_DiPFJetAve100_HFJEC",
        "HLT_DiPFJetAve160_HFJEC",
        "HLT_DiPFJetAve220_HFJEC",
        "HLT_DiPFJetAve300_HFJEC",
    ]
else:
    triggers = [ args.trigger ]

mc = QCD_Pt

samples = [mc, data]
tag_jet_bin             = tuple(args.ptBin)
probe_jet_abs_eta_bin   = tuple(args.etaBin)
if args.etaSign   == -1:
    probe_jet_eta_cutstring = "-Jet_eta[probe_jet_index]"
    eta_string              = "negeta"
    eta_tex_string          = "-%4.3f #leq #eta < -%4.3f"% ( -args.etaBin[0], -args.etaBin[1]  )
elif args.etaSign == +1:
    probe_jet_eta_cutstring = "Jet_eta[probe_jet_index]"
    eta_string              = "poseta"
    eta_tex_string          = "%4.3f #leq #eta < %4.3f"%  probe_jet_abs_eta_bin 
elif args.etaSign ==  0:
    probe_jet_eta_cutstring = "abs(Jet_eta[probe_jet_index])"
    eta_string              = "abseta"
    eta_tex_string          = "%4.3f #leq |#eta| < %4.3f"% probe_jet_abs_eta_bin

# kinematic selection on tag & probe jet
kinSelectionString = "%i<pt_avg&&pt_avg<%i&& %s > %4.3f && %s < %4.3f"% ( tag_jet_bin[0], tag_jet_bin[1], probe_jet_eta_cutstring, probe_jet_abs_eta_bin[0], probe_jet_eta_cutstring, probe_jet_abs_eta_bin[1] )
logger.info( "Jet selection: %s", kinSelectionString )

selection = [
   ("btb",          "cos(Jet_phi[tag_jet_index] - Jet_phi[probe_jet_index]) < cos(2.7)" ),
   ("a30",          "alpha<0.3" ), 
   ("tgb",          "abs(Jet_eta[tag_jet_index])<1.3" ),
   ("failIdVeto",   "Sum$(JetFailId_pt*(JetFailId_pt>30))<30" ),
   ("kinSelection",  kinSelectionString ) 
]

for s in samples:   
    s.addSelectionString( "&&".join(c[1] for c in selection))
    if args.small:
        s.reduceFiles( to = 1 )

colors = [ j+1 for j in range(0,9) ] + [ j+31 for j in range(9,18) ]

variableString = args.variable
binning        = [50,-1,1]
weightString   = "weight"

#h_MC =      mc.get1DHistoFromDraw(variableString = variableString, binning = binning, weightString=weightString+"*%f" % lumi )
h_data    = {t:data.get1DHistoFromDraw(variableString = variableString, binning = binning, weightString=weightString+"&& %s "% t) for t in triggers }
#h_data_ps = {t:data.get1DHistoFromDraw(variableString = variableString, binning = binning, weightString="("+weightString+")*HLT_BIT_%s_v_Prescale * (%s==1) "% (t,t) ) for t in triggers }

#h_MC.style = styles.lineStyle( ROOT.kBlack ) 
#h_MC.legendText = "QCD Pt binned"
for i, t in enumerate( triggers ):
    h_data[t].style = styles.lineStyle( colors[ i ], dashed = False ) 
    #h_data[t].legendText = t 
    #h_data_ps[t].style = styles.lineStyle( colors[ i ] ) 
    h_data[t].legendText = t.replace('HLT_','')+" ( %3.2f #pm %2.2f ) " % ( h_data[t].GetMean(), h_data[t].GetMeanError() ) 
    integr = h_data[t].Integral()
    if integr>0: 
        h_data[t].Scale(1./integr) 

histos_data = []
for t in triggers:
    if h_data[t].GetEntries() > 50:
        histos_data.append( [ h_data[t] ] )

plot = Plot.fromHisto( variableString+'_pt_%i_%i_eta_%i_%i'%( args.ptBin[0], args.ptBin[1], 1000*args.etaBin[0], 1000*args.etaBin[1]), histos_data, texX = args.variable, texY = "Number of Events" )
plot.drawObjects = [
  (0.1, 0.95, eta_tex_string  ),
  (0.45, 0.95, "%i #leq p_{T} < %i"%tag_jet_bin ),
 ]

draw1DPlots( [plot], 1.)
