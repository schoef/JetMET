# Standard imports
import os
import ROOT
import array

# RootTools
from RootTools.core.standard import *

# Samples
#directory = "/afs/hephy.at/data/rschoefbeck02/postProcessed/flat_jet_trees/v6/"
#sample = Sample.fromDirectory( "DoubleMuon", os.path.join( directory, "DoubleMuon_Run2018C-17Sep2018-v1_MINIAOD" ), isData = True)
from JetMET.diagnosis.pu2018.samples import *
from JetMET.tools.user import plot_directory
sample = RelVal_DoubleMuon_Run2018D_Ref

#
# Logger
#
import JetMET.tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   'INFO', logFile = None)
logger_rt = logger_rt.get_logger('INFO', logFile = None)

# define TProfiles
#bx_thresholds  = [i for i in range(3000)]
#prefix = ''
bx_thresholds  = [i for i in range(500)]
prefix = 'zoomed_'

common = [
      (0.15, 0.95, 'Run2018C (13 TeV)'), 
]

variables = [ 
    [ "ChBarrelSumPt",  "ch_m1p5_1p5_sumPt",                      [(0.7, 0.85, "sumPt(PF ch) |#eta|<1.5")]],
    [ "NhEnBarrelSumPt",  "nh_m1p5_1p5_sumPt",                      [(0.7, 0.85, "sumPt(PF nh) |#eta|<1.5")]],
    [ "PhEnEC1SumPt",  "ga_m2p5_m1p5_sumPt+ga_1p5_2p5_sumPt",                      [(0.7, 0.85, "sumPt(PF #gamma) 1.5<|#eta|<2.5")]],
    [ "NhEnEC1SumPt",  "nh_m2p5_m1p5_sumPt+nh_1p5_2p5_sumPt",                      [(0.7, 0.85, "sumPt(PF nh) 1.5<|#eta|<2.5")]],
    [ "PhEnEC2SumPt",  "ga_m3p1_m2p5_sumPt+ga_2p5_3p1_sumPt",    [(0.7, 0.85, "sumPt(PF #gamma) 2.5<|#eta|<3.1")]],
    [ "NhEnEC2SumPt",  "nh_m3p1_m2p5_sumPt+nh_2p5_3p1_sumPt",    [(0.7, 0.85, "sumPt(PF nh) 2.5<|#eta|<3.1")]],
    [ "MET", "met_pt",                                              [(0.7, 0.85, "MET")]],
    [ "nVert",  "nVert",                                            [(0.7, 0.85, "vertex multiplicity (clean)")]],
    [ "nVertAll",  "nVertAll",                                      [(0.7, 0.85, "vertex multiplicity (all)")]],
    [ "HFsumPt",  "all_3p1_5p1_sumPt+all_m5p1_m3p1_sumPt",          [(0.7, 0.85, "sumPt(HF)")]],
]

def drawObjects( extra ):
    tex = ROOT.TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.04)
    tex.SetTextAlign(11) # align right
    lines = common + extra 
    return [tex.DrawLatex(*l) for l in lines] 

quantiles = [0, 0.31, 0.5, 0.68, 0.95, 0.99, 0.999]
colors    = [ROOT.kBlack, ROOT.kMagenta, ROOT.kBlue, ROOT.kMagenta, ROOT.kGreen, ROOT.kRed, ROOT.kOrange]


sample.reduceFiles( to = -1 )

selectionString = "Flag_goodVertices&&Flag_globalSuperTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_BadPFMuonFilter&&Flag_BadChargedCandidateFilter&&Flag_eeBadScFilter"

for name, variable, lines in variables:
    # Get inclusive histogam
    binning_y = [i/2. for i in range(6000)]
    h_inclusive = sample.get1DHistoFromDraw( variable, binning_y, selectionString = selectionString,  binningIsExplicit = True )

    # obtain quantiles
    thresholds = array.array('d', [ROOT.Double()] * len(quantiles) )
    h_inclusive.GetQuantiles( len(quantiles), thresholds, array.array('d', quantiles) )

    # 1D plot
    plot_inclusive = Plot.fromHisto( name = prefix+'1D_'+name, histos = [ [h_inclusive] ], texX = name, texY = "Number of Events")
    
    q_lines = []
    for i_threshold, threshold in enumerate(thresholds):
        q_lines.append( ROOT.TLine( threshold, 0, threshold, 1.2*h_inclusive.GetMaximum()) )
        q_lines[-1].SetLineColor( colors[ i_threshold ] )
        #h_inclusive.Rebin( 6 ) 
        h_inclusive.GetXaxis().SetRangeUser( 0 , 2*thresholds[-1] )
 
    plotting.draw(plot_inclusive, 
        #ratio = {},
        legend      = ( [0.15, 0.80, 0.70, 0.90], 3 ),
        plot_directory = os.path.join( plot_directory, "JetMET/BX_quantiles", sample.name ),
        logX = False, logY = True, copyIndexPHP = True,
        drawObjects = q_lines,
        )

    h_quantiles = {}

    for i_quantile, quantile in enumerate(quantiles):
        h_quantiles[quantile] = sample.get1DHistoFromDraw( 'bx', bx_thresholds, selectionString = selectionString+"&&%s>=%f"% ( variable, thresholds[i_quantile]) ,  binningIsExplicit = True ) 
        h_quantiles[quantile].style = styles.lineStyle( colors[i_quantile] )
        h_quantiles[quantile].legendText = "#geq %3.1f ( %3.1f "%( thresholds[i_quantile], 100*quantiles[i_quantile]) + "% )"

    plot = Plot.fromHisto( name = prefix+name, histos = [ [h_quantiles[quantile]] for quantile in quantiles ], texX = "BX", texY = "Number of Events")

    plotting.draw(plot, 
        #ratio = {},
        widths = {'x_width':1300, 'y_width':600},
        #yRange=(0, maximum),  
        legend      = ( [0.15, 0.80, 0.70, 0.90], 3 ),
        plot_directory = os.path.join( plot_directory, "JetMET/BX_quantiles", sample.name ),
        logX = False, logY = True, copyIndexPHP = True,
        drawObjects = drawObjects( lines )
        )
