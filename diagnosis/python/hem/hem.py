# Standard imports
import os
import ROOT
import array

# RootTools
from RootTools.core.standard import *

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--small',              action='store_true', help='Run only on a small subset of the data?')#, default = True)
#argParser.add_argument('--maxEvents',          action='store',      type=int, default=-1, help='Maximum number of events')
#argParser.add_argument('--maxFiles',           action='store',      type=int, default=-1, help='Maximum number of files')
args = argParser.parse_args()

# Samples
#directory = "/afs/hephy.at/data/rschoefbeck02/postProcessed/flat_jet_trees/v6/"
#sample = Sample.fromDirectory( "DoubleMuon", os.path.join( directory, "DoubleMuon_Run2018C-17Sep2018-v1_MINIAOD" ), isData = True)
from JetMET.tools.user import plot_directory

directory = "/afs/hephy.at/data/rschoefbeck02/postProcessed/flat_jet_trees/v9/"
sample = Sample.fromDirectory( "DoubleMuon", os.path.join( directory, "DoubleMuon_Run2018C-17Sep2018-v1_MINIAOD" ), isData = True)

#
# Logger
#
import JetMET.tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   'INFO', logFile = None)
logger_rt = logger_rt.get_logger('INFO', logFile = None)

tex_common = [
      (0.15, 0.95, 'Run2018C (13 TeV)'), 
]

variables = [ 
    [ "ChBarrelSumPt",  "ch_m1p5_1p5_sumPt",                      [(0.7, 0.85, "sumPt(PF ch) |#eta|<1.5")]],
    [ "HFsumPt",  "all_3p1_5p1_sumPt+all_m5p1_m3p1_sumPt",          [(0.7, 0.85, "sumPt(HF)")]],
]

def drawObjects( extra ):
    tex = ROOT.TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.04)
    tex.SetTextAlign(11) # align right
    lines = tex_common + extra 
    return [tex.DrawLatex(*l) for l in lines] 

if args.small: sample.reduceFiles( to = 1 )

selectionString = "Flag_goodVertices&&Flag_globalSuperTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_BadPFMuonFilter&&Flag_BadChargedCandidateFilter&&Flag_eeBadScFilter"

quantiles = [0, 0.31, 0.5, 0.68, 0.95, 0.99, 0.999]
colors    = [ROOT.kBlack, ROOT.kMagenta, ROOT.kBlue, ROOT.kMagenta, ROOT.kGreen, ROOT.kRed, ROOT.kOrange]

for name, variable, lines in variables:
    # Get inclusive histogam
    binning_y = [i/2. for i in range(6000)]
    h_inclusive = sample.get1DHistoFromDraw( variable, binning_y, selectionString = selectionString,  binningIsExplicit = True )

    # obtain quantiles
    thresholds = array.array('d', [ROOT.Double()] * len(quantiles) )
    h_inclusive.GetQuantiles( len(quantiles), thresholds, array.array('d', quantiles) )

    # 1D plot
    plot_inclusive = Plot.fromHisto( name = '1D_'+name, histos = [ [h_inclusive] ], texX = name, texY = "Number of Events")
    
    q_lines = []
    for i_threshold, threshold in enumerate(thresholds):
        q_lines.append( ROOT.TLine( threshold, 0, threshold, 1.2*h_inclusive.GetMaximum()) )
        q_lines[-1].SetLineColor( colors[ i_threshold ] )
        #h_inclusive.Rebin( 6 ) 
        h_inclusive.GetXaxis().SetRangeUser( 0 , 2*thresholds[-1] )
 
    plotting.draw(plot_inclusive, 
        #ratio = {},
        legend      = ( [0.15, 0.80, 0.70, 0.90], 3 ),
        plot_directory = os.path.join( plot_directory, "JetMET/HEM", sample.name ),
        logX = False, logY = True, copyIndexPHP = True,
        drawObjects = q_lines,
        )
