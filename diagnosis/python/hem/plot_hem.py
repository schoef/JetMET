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

directory = "/afs/hephy.at/data/cms01/flat_jet_trees/hem_v1"
sample = Sample.fromDirectory( "Run2018B", os.path.join( directory, "DoubleMuon_Run2018B-17Sep2018-v1_MINIAOD" ), isData = True)

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
    [ "nh_m3p2_m1p3_HEMphi_sumPt",  [(0.7, 0.85, "sumPt(PF nh) HEM")]],
#    [ "nh_1p3_3p2_HEMphi_sumPt",  [(0.7, 0.85, "sumPt(PF nh) HEM")]],
]

def drawObjects( extra ):
    tex = ROOT.TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.04)
    tex.SetTextAlign(11) # align right
    lines = tex_common + extra 
    return [tex.DrawLatex(*l) for l in lines] 

if args.small: sample.reduceFiles( to = 1 )

#selectionString = "Flag_goodVertices&&Flag_globalSuperTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_BadPFMuonFilter&&Flag_BadChargedCandidateFilter&&Flag_eeBadScFilter"
selectionString = "Flag_globalSuperTightHalo2016Filter"

selectionString += "&&mll>20&&Sum$(jet_pt>30&&abs(jet_eta)<2.4)>=2"

quantiles = [0.001, 0.01, 0.05, 0.31, 0.5, 0.68, 0.95, 0.99, 0.999]
colors    = [ROOT.kOrange, ROOT.kRed, ROOT.kGreen, ROOT.kBlue, ROOT.kBlack,  ROOT.kBlue, ROOT.kGreen, ROOT.kRed, ROOT.kOrange]

for variable, lines in variables:
    # Get inclusive histogam
    binning_y = [i/2. for i in range(-6000,6000)]
    h_hem    = sample.get1DHistoFromDraw( variable, binning_y, selectionString = selectionString+"&&run>=319077",  binningIsExplicit = True )
    h_prehem = sample.get1DHistoFromDraw( variable, binning_y, selectionString = selectionString+"&&run<319077",  binningIsExplicit = True )

    if h_hem.Integral()>0:
        h_hem.Scale(1./h_hem.Integral())
    if h_prehem.Integral()>0:
        h_prehem.Scale(1./h_prehem.Integral())

    # obtain quantiles
    thresholds_hem = array.array('d', [ROOT.Double()] * len(quantiles) )
    h_hem.GetQuantiles( len(quantiles), thresholds_hem, array.array('d', quantiles) )
    thresholds_prehem = array.array('d', [ROOT.Double()] * len(quantiles) )
    h_prehem.GetQuantiles( len(quantiles), thresholds_prehem, array.array('d', quantiles) )

    # 1D plot
    name = variable
    plot = Plot.fromHisto( name = '1D_'+name, histos = [ [h_hem], [h_prehem] ], texX = name, texY = "Number of Events")
    
    q_lines = []
    for i_threshold in range(len(quantiles)):
        q_lines.append( ROOT.TLine( thresholds_hem[i_threshold], 0, thresholds_hem[i_threshold], 1.2*h_hem.GetMaximum()) )
        q_lines[-1].SetLineColor( colors[ i_threshold ] )
        q_lines.append( ROOT.TLine( thresholds_prehem[i_threshold], 0, thresholds_prehem[i_threshold], 1.2*h_prehem.GetMaximum()) )
        q_lines[-1].SetLineColor( colors[ i_threshold ] )
        q_lines[-1].SetLineStyle( 2 )
        #h_inclusive.Rebin( 6 ) 
        #h_inclusive.GetXaxis().SetRangeUser( 0 , 2*thresholds_hem[-1] )

    plotting.draw(plot, 
        #ratio = {},
        legend      = ( [0.15, 0.80, 0.70, 0.90], 3 ),
        plot_directory = os.path.join( plot_directory, "JetMET/HEM", sample.name ),
        logX = False, logY = True, copyIndexPHP = True,
        drawObjects = q_lines,
        )

#evt/l
#run/I
#lumi/I
#nVert/I
#nVertAll/I
#closest_dz_good/F
#closest_dz_all/F
#bx/I
#njet/I
#jet_pt[njet]/F
#jet_genPt[njet]/F
#jet_genEta[njet]/F
#jet_genPhi[njet]/F
#jet_rawPt[njet]/F
#jet_eta[njet]/F
#jet_phi[njet]/F
#jet_chHEF[njet]/F
#jet_neHEF[njet]/F
#jet_phEF[njet]/F
#jet_eEF[njet]/F
#jet_muEF[njet]/F
#jet_HFHEF[njet]/F
#jet_HFEMEF[njet]/F
#jet_chHMult[njet]/F
#jet_neHMult[njet]/F
#jet_phMult[njet]/F
#jet_eMult[njet]/F
#jet_muMult[njet]/F
#jet_HFHMult[njet]/F
#jet_HFEMMult[njet]/F
#met_pt/F
#met_phi/F
#mll/F
#fixedGridRhoFastjetAll/F
#Flag_goodVertices/I
#Flag_globalSuperTightHalo2016Filter/I
#Flag_HBHENoiseFilter/I
#Flag_HBHENoiseIsoFilter/I
#Flag_EcalDeadCellTriggerPrimitiveFilter/I
#Flag_BadPFMuonFilter/I
#Flag_BadChargedCandidateFilter/I
#Flag_eeBadScFilter/I
#el_m3p2_m1p3_HEMphi_met/F
#el_m3p2_m1p3_HEMphi_sumPt/F
#el_m3p2_m1p3_HEMphi_metPhi/F
#mu_m3p2_m1p3_HEMphi_met/F
#mu_m3p2_m1p3_HEMphi_sumPt/F
#mu_m3p2_m1p3_HEMphi_metPhi/F
#ga_m3p2_m1p3_HEMphi_met/F
#ga_m3p2_m1p3_HEMphi_sumPt/F
#ga_m3p2_m1p3_HEMphi_metPhi/F
#ch_m3p2_m1p3_HEMphi_met/F
#ch_m3p2_m1p3_HEMphi_sumPt/F
#ch_m3p2_m1p3_HEMphi_metPhi/F
#nh_m3p2_m1p3_HEMphi_met/F
#nh_m3p2_m1p3_HEMphi_sumPt/F
#nh_m3p2_m1p3_HEMphi_metPhi/F
#HFh_m3p2_m1p3_HEMphi_met/F
#HFh_m3p2_m1p3_HEMphi_sumPt/F
#HFh_m3p2_m1p3_HEMphi_metPhi/F
#HFe_m3p2_m1p3_HEMphi_met/F
#HFe_m3p2_m1p3_HEMphi_sumPt/F
#HFe_m3p2_m1p3_HEMphi_metPhi/F
#all_m3p2_m1p3_HEMphi_met/F
#all_m3p2_m1p3_HEMphi_sumPt/F
#all_m3p2_m1p3_HEMphi_metPhi/F
#el_m3p2_m1p3_noHEMphi_met/F
#el_m3p2_m1p3_noHEMphi_sumPt/F
#el_m3p2_m1p3_noHEMphi_metPhi/F
#mu_m3p2_m1p3_noHEMphi_met/F
#mu_m3p2_m1p3_noHEMphi_sumPt/F
#mu_m3p2_m1p3_noHEMphi_metPhi/F
#ga_m3p2_m1p3_noHEMphi_met/F
#ga_m3p2_m1p3_noHEMphi_sumPt/F
#ga_m3p2_m1p3_noHEMphi_metPhi/F
#ch_m3p2_m1p3_noHEMphi_met/F
#ch_m3p2_m1p3_noHEMphi_sumPt/F
#ch_m3p2_m1p3_noHEMphi_metPhi/F
#nh_m3p2_m1p3_noHEMphi_met/F
#nh_m3p2_m1p3_noHEMphi_sumPt/F
#nh_m3p2_m1p3_noHEMphi_metPhi/F
#HFh_m3p2_m1p3_noHEMphi_met/F
#HFh_m3p2_m1p3_noHEMphi_sumPt/F
#HFh_m3p2_m1p3_noHEMphi_metPhi/F
#HFe_m3p2_m1p3_noHEMphi_met/F
#HFe_m3p2_m1p3_noHEMphi_sumPt/F
#HFe_m3p2_m1p3_noHEMphi_metPhi/F
#all_m3p2_m1p3_noHEMphi_met/F
#all_m3p2_m1p3_noHEMphi_sumPt/F
#all_m3p2_m1p3_noHEMphi_metPhi/F
#el_m3p2_m1p3_all_met/F
#el_m3p2_m1p3_all_sumPt/F
#el_m3p2_m1p3_all_metPhi/F
#mu_m3p2_m1p3_all_met/F
#mu_m3p2_m1p3_all_sumPt/F
#mu_m3p2_m1p3_all_metPhi/F
#ga_m3p2_m1p3_all_met/F
#ga_m3p2_m1p3_all_sumPt/F
#ga_m3p2_m1p3_all_metPhi/F
#ch_m3p2_m1p3_all_met/F
#ch_m3p2_m1p3_all_sumPt/F
#ch_m3p2_m1p3_all_metPhi/F
#nh_m3p2_m1p3_all_met/F
#nh_m3p2_m1p3_all_sumPt/F
#nh_m3p2_m1p3_all_metPhi/F
#HFh_m3p2_m1p3_all_met/F
#HFh_m3p2_m1p3_all_sumPt/F
#HFh_m3p2_m1p3_all_metPhi/F
#HFe_m3p2_m1p3_all_met/F
#HFe_m3p2_m1p3_all_sumPt/F
#HFe_m3p2_m1p3_all_metPhi/F
#all_m3p2_m1p3_all_met/F
#all_m3p2_m1p3_all_sumPt/F
#all_m3p2_m1p3_all_metPhi/F
#el_all_HEMphi_met/F
#el_all_HEMphi_sumPt/F
#el_all_HEMphi_metPhi/F
#mu_all_HEMphi_met/F
#mu_all_HEMphi_sumPt/F
#mu_all_HEMphi_metPhi/F
#ga_all_HEMphi_met/F
#ga_all_HEMphi_sumPt/F
#ga_all_HEMphi_metPhi/F
#ch_all_HEMphi_met/F
#ch_all_HEMphi_sumPt/F
#ch_all_HEMphi_metPhi/F
#nh_all_HEMphi_met/F
#nh_all_HEMphi_sumPt/F
#nh_all_HEMphi_metPhi/F
#HFh_all_HEMphi_met/F
#HFh_all_HEMphi_sumPt/F
#HFh_all_HEMphi_metPhi/F
#HFe_all_HEMphi_met/F
#HFe_all_HEMphi_sumPt/F
#HFe_all_HEMphi_metPhi/F
#all_all_HEMphi_met/F
#all_all_HEMphi_sumPt/F
#all_all_HEMphi_metPhi/F
#el_all_noHEMphi_met/F
#el_all_noHEMphi_sumPt/F
#el_all_noHEMphi_metPhi/F
#mu_all_noHEMphi_met/F
#mu_all_noHEMphi_sumPt/F
#mu_all_noHEMphi_metPhi/F
#ga_all_noHEMphi_met/F
#ga_all_noHEMphi_sumPt/F
#ga_all_noHEMphi_metPhi/F
#ch_all_noHEMphi_met/F
#ch_all_noHEMphi_sumPt/F
#ch_all_noHEMphi_metPhi/F
#nh_all_noHEMphi_met/F
#nh_all_noHEMphi_sumPt/F
#nh_all_noHEMphi_metPhi/F
#HFh_all_noHEMphi_met/F
#HFh_all_noHEMphi_sumPt/F
#HFh_all_noHEMphi_metPhi/F
#HFe_all_noHEMphi_met/F
#HFe_all_noHEMphi_sumPt/F
#HFe_all_noHEMphi_metPhi/F
#all_all_noHEMphi_met/F
#all_all_noHEMphi_sumPt/F
#all_all_noHEMphi_metPhi/F
#el_all_all_met/F
#el_all_all_sumPt/F
#el_all_all_metPhi/F
#mu_all_all_met/F
#mu_all_all_sumPt/F
#mu_all_all_metPhi/F
#ga_all_all_met/F
#ga_all_all_sumPt/F
#ga_all_all_metPhi/F
#ch_all_all_met/F
#ch_all_all_sumPt/F
#ch_all_all_metPhi/F
#nh_all_all_met/F
#nh_all_all_sumPt/F
#nh_all_all_metPhi/F
#HFh_all_all_met/F
#HFh_all_all_sumPt/F
#HFh_all_all_metPhi/F
#HFe_all_all_met/F
#HFe_all_all_sumPt/F
#HFe_all_all_metPhi/F
#all_all_all_met/F
#all_all_all_sumPt/F
#all_all_all_metPhi/F

