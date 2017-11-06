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
argParser.add_argument('--triggers',           action='store',      default='noTriggers',    nargs='?', choices=['DiPFJetAve', 'DiPFJetAve_HFJEC', 'PFJet', 'exclPFJet', 'exclDiPFJetAve', 'exclDiPFJetAveHFJEC', 'noTriggers'], help="trigger suite" )
argParser.add_argument('--ptBin',              action='store',      default=(163, 230),      type = int,    nargs=2,  help="tag jet pt bin" )
argParser.add_argument('--etaSign',            action='store',      default=0             ,  type = int,    choices = [-1,0,+1], help="sign of probe jet eta." )
argParser.add_argument('--era',                action='store',      default='Run2016H',      nargs='?', choices=['Run2016', 'Run2016BCD', 'Run2016EFearly', 'Run2016FlateG', 'Run2016H', 'Run2016_18Apr', 'Run2016BCD_18Apr', 'Run2016EFearly_18Apr', 'Run2016FlateG_18Apr', 'Run2016H_18Apr', 'Run2016B_07Aug17', 'Run2016C_07Aug17', 'Run2016F_07Aug17', 'Run2016G_07Aug17', 'Run2016H_07Aug17'], help="era" )
argParser.add_argument('--small',                                   action='store_true',     help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--cleaned',                                 action='store_true',     help='Apply jet cleaning in data')#, default = True)
argParser.add_argument('--bad',                                     action='store_true',     help='Cut on phEF*pT>300')#, default = True)
argParser.add_argument('--plot_directory',     action='store',      default='JEC/L2res_2D_v11',     help="subdirectory for plots")
args = argParser.parse_args()

if args.cleaned:
    args.plot_directory += '_cleaned'
if args.bad:
    args.plot_directory += '_bad'
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

## Formatting for 1D plots
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
elif args.era == 'Run2016_18Apr':
    data = JetHT_Run2016_18Apr
elif args.era == 'Run2016BCD_18Apr':
    data = JetHT_Run2016BCD_18Apr
elif args.era == 'Run2016EFearly_18Apr':
    data = JetHT_Run2016EFearly_18Apr
elif args.era == 'Run2016FlateG_18Apr':
    data = JetHT_Run2016FlateG_18Apr
elif args.era == 'Run2016H_18Apr':
    data = JetHT_Run2016H_18Apr
elif args.era == 'Run2016B_07Aug17':
    data = JetHT_Run2016B_07Aug17
elif args.era == 'Run2016C_07Aug17':
    data = JetHT_Run2016C_07Aug17
elif args.era == 'Run2016F_07Aug17':
    data = JetHT_Run2016F_07Aug17
elif args.era == 'Run2016G_07Aug17':
    data = JetHT_Run2016G_07Aug17
elif args.era == 'Run2016H_07Aug17':
    data = JetHT_Run2016H_07Aug17

if args.triggers == 'noTriggers':
    triggers = []
elif args.triggers=='DiPFJetAve':
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

samples = data

from JetMET.JEC.L2res.jet_cleaning import jet_cleaning
if len(triggers)>0:
    data.addSelectionString( "("+"||".join(triggers)+")")
if args.cleaned:
    data.addSelectionString( jet_cleaning )

selection = [
#   ("btb", "cos(Jet_phi[tag_jet_index] - Jet_phi[probe_jet_index]) < cos(2.7)"),
#   ("a30", "alpha<0.3"), 
("EGM", "A>0.4&&Jet_phEF[probe_jet_index]>0.8")
]
if args.bad:
    selection.append( ("bad", "Jet_phEF[probe_jet_index]*Jet_pt[probe_jet_index]>250") )

#tag_jet_bin = (163, 230)
#probe_jet_abs_eta_bin = (2.853, 2.964 )
tag_jet_bin             = tuple(args.ptBin)
if args.etaSign   == -1:
    probe_jet_eta_string = "-Jet_eta[probe_jet_index]"
    eta_string           = "negeta"
    eta_tex_string       = "#eta<0"
elif args.etaSign == +1:
    probe_jet_eta_string = "Jet_eta[probe_jet_index]"
    eta_string           = "poseta"
    eta_tex_string       = "#eta>0"
elif args.etaSign ==  0:
    probe_jet_eta_string = "abs(Jet_eta[probe_jet_index])"
    eta_string           = "alleta"
    eta_tex_string       = "(both endcaps)"

# kinematic selection on tag & probe jet
kinSelectionString = "%f<Jet_pt[tag_jet_index]&&Jet_pt[tag_jet_index]<%f "% ( tag_jet_bin[0], tag_jet_bin[1] )
logger.info( "Jet selection: %s", kinSelectionString )

data.addSelectionString( "&&".join(c[1] for c in selection))
data.addSelectionString( kinSelectionString )
if args.small:
    data.reduceFiles( to = 1 )

#colors = [ j+1 for j in range(0,9) ] + [ j+31 for j in range(9,18) ]

variableString = "1/sinh(%s)*sin(Jet_phi[probe_jet_index]):1/sinh(%s)*cos(Jet_phi[probe_jet_index])" % ( probe_jet_eta_string, probe_jet_eta_string )
weightString   = "met_chsPt*weight*(%s>0)"%probe_jet_eta_string

logger.info( "Get plot with %s, and weight %s", variableString, weightString )

h_data    = data.get2DHistoFromDraw(variableString = variableString, binning = [60, -0.3, 0.3, 60, -0.3, 0.3], weightString=weightString) 

circles = [ ROOT.TArc(0,0,1./sinh(eta)) for eta in [2.5, 3] ] 
for c in circles:
    c.SetFillStyle(0)

plot = Plot2D.fromHisto( name = '2D_%s_pt_%i_%i' % ( eta_string, tag_jet_bin[0], tag_jet_bin[1]), 
#    [ [ h_MC ] ] + histos_data, texX = texX, texY = "Number of Events" 
    histos = [[ h_data ]], texX = "X (/Z)", texY = "Y (/Z)" 
    )
plot.drawObjects = circles
plot.drawObjects += [ 
    (0.17, 0.86, args.era + ' ' + eta_tex_string),
    (0.17, 0.81, '%i #leq p_{T,tag} < %i'% tag_jet_bin ),
    (0.59, 0.41, '|#eta| = 3' ),
    (0.65, 0.35, '|#eta| = 2.5' ),
]
 
draw2DPlots( [plot], 1.)
