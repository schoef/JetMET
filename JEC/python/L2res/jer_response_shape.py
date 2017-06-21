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
#argParser.add_argument('--trigger',            action='store',      default='DiPFJetAve',    nargs='?', help="trigger requirement" )
argParser.add_argument('--ptBin',              action='store',      default=(365, 435),      type = int,    nargs=2,  help="pt average bin" )
argParser.add_argument('--ptHatExp',           action='store',      default=None,            type = float,   help="exponent of reweighting in pt_avg" )
argParser.add_argument('--etaBin',             action='store',      default=(2.964, 3.139),   type = float,  nargs=2,  help="probe jet eta bin" )
argParser.add_argument('--etaSign',            action='store',      default=0             ,  type = int,    choices = [-1,0,+1], help="sign of probe jet eta." )
argParser.add_argument('--small',                                   action='store_true',     help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--plot_directory',     action='store',      default='JEC/L2res_jer_v8',     help="subdirectory for plots")
args = argParser.parse_args()

if args.ptHatExp is not None:
    args.plot_directory += '_ptHatExp%2.1f'%args.ptHatExp
if args.small:
    args.plot_directory += '_small'

plot_directory = os.path.join( user_plot_directory, args.plot_directory )

# DrawLatex objects for plots
tex = ROOT.TLatex()
tex.SetNDC()
tex.SetTextSize(0.04)
tex.SetTextAlign(11) # align right
def drawObjects( dataMCScale ):
    lines = [
      #(0.15, 0.95, args.era), 
      (0.8, 0.95, 'QCD Pt' )
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

mc = QCD_Pt_small

samples = [mc]
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
kinSelectionString = "%f<pt_avg&&pt_avg<%f&& %s > %f && %s < %f"% ( tag_jet_bin[0], tag_jet_bin[1], probe_jet_eta_cutstring, probe_jet_abs_eta_bin[0], probe_jet_eta_cutstring, probe_jet_abs_eta_bin[1] )
logger.info( "Jet selection: %s", kinSelectionString )

selection = [
   ("btb",          "cos(Jet_phi[tag_jet_index] - Jet_phi[probe_jet_index]) < cos(2.7)" ),
   ("a30",          "alpha<0.3" ), 
   ("tgb",          "abs(Jet_eta[tag_jet_index])<1.3" ),
   ("failIdVeto",   "Sum$(JetFailId_pt*(JetFailId_pt>30))<30" ),
   ("kinSelection",  kinSelectionString ) 
]

if args.small:
    mc.files = [ '/afs/hephy.at/data/rschoefbeck02/postProcessed/L2res/v8/default/QCD_Pt_470to600/QCD_Pt_470to600_0.root' ]
    #mc.reduceFiles( to = 1 )

colors = [ j+1 for j in range(0,9) ] + [ j+31 for j in range(9,18) ]

plots = [
    ( 'A', [50,-1,1]),
    ( 'B', [50,-1,1]),
    ( 'genBin', [50,args.ptBin[0]-100,args.ptBin[1]+100]),
    ( 'pt_avg', [50,args.ptBin[0]-50,args.ptBin[1]+50]),
]

h = {p[0]:{} for p in plots}

for i_jer, jer in enumerate( ['', 'jer', 'jer_up', 'jer_down'] ):

    postfix = '' if jer=='' else '_'+jer

    mc.setSelectionString( "(1)" )
    selectionString =  "&&".join(c[1] for c in selection)
    selectionString = selectionString.replace('pt_avg', 'pt_avg%s'%postfix)
    
    mc.addSelectionString( selectionString )
     
    weightString   = "weight"
    if args.ptHatExp is not None:
        weightString += "*(genBin/%4.1f)**(%2.1f)"%(0.5*sum(args.ptBin), args.ptHatExp)

    for var, binning in plots:

        logger.info( "Sample %s jer '%s' var '%s' weightString '%s'", mc.name, jer, var, weightString )
        var_string = "%s%s"%( var, postfix) if var in ['A', 'B', 'pt_avg'] else var
        h[var][jer] = mc.get1DHistoFromDraw(variableString = var_string, binning = binning, weightString=weightString )
        h[var][jer].legendText =  'nominal' if jer=='' else jer
        h[var][jer].legendText += " (%3.2f#pm%3.2f)"%( h[var][jer].GetMean(), h[var][jer].GetMeanError() ) 
        h[var][jer].style = styles.lineStyle( colors[ i_jer ] ) 

for var, binning in plots:
    histos = [[h[var][jer]] for jer in ['', 'jer', 'jer_up', 'jer_down']]


    name_str='%s_pt_%i_%i_eta_%i_%i'%( var, args.ptBin[0], args.ptBin[1], 1000*args.etaBin[0], 1000*args.etaBin[1])
    plot = Plot.fromHisto( name_str, histos, texX = var, texY = "Number of Events" )   
    plot.drawObjects = [
      (0.1, 0.95, eta_tex_string  ),
      (0.45, 0.95, "%i #leq p_{T} < %i"%tag_jet_bin ),
     ]
    draw1DPlots( [plot], 1.)
