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

directory = "/afs/hephy.at/data/cms01/hem/v2"
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
#    [ "all_m3p2_m1p3_HEMphi_met*cos(all_m3p2_m1p3_HEMphi_metPhi)", "all_m3p2_m1p3_HEMphi_MEx", []],
#    [ "all_m3p2_m1p3_noHEMphi_met*cos(all_m3p2_m1p3_noHEMphi_metPhi)", "all_m3p2_m1p3_noHEMphi_MEx", []],
#    [ "all_m3p2_m1p3_HEMphi_met*sin(all_m3p2_m1p3_HEMphi_metPhi)", "all_m3p2_m1p3_HEMphi_MEy", []],
#    [ "all_m3p2_m1p3_noHEMphi_met*sin(all_m3p2_m1p3_noHEMphi_metPhi)", "all_m3p2_m1p3_noHEMphi_MEy", []],
#    [ "all_1p3_3p2_HEMphi_met*cos(all_1p3_3p2_HEMphi_metPhi)", "all_1p3_3p2_HEMphi_MEx", []],
#    [ "all_1p3_3p2_noHEMphi_met*cos(all_1p3_3p2_noHEMphi_metPhi)", "all_1p3_3p2_noHEMphi_MEx", []],
#    [ "all_1p3_3p2_HEMphi_met*sin(all_1p3_3p2_HEMphi_metPhi)", "all_1p3_3p2_HEMphi_MEy", []],
#    [ "all_1p3_3p2_noHEMphi_met*sin(all_1p3_3p2_noHEMphi_metPhi)", "all_1p3_3p2_noHEMphi_MEy", []],

    [ "nh_m3p2_m1p3_HEMphi_met*cos(nh_m3p2_m1p3_HEMphi_metPhi)", "nh_m3p2_m1p3_HEMphi_MEx", []],
    [ "nh_m3p2_m1p3_noHEMphi_met*cos(nh_m3p2_m1p3_noHEMphi_metPhi)", "nh_m3p2_m1p3_noHEMphi_MEx", []],
    [ "nh_m3p2_m1p3_HEMphi_met*sin(nh_m3p2_m1p3_HEMphi_metPhi)", "nh_m3p2_m1p3_HEMphi_MEy", []],
    [ "nh_m3p2_m1p3_noHEMphi_met*sin(nh_m3p2_m1p3_noHEMphi_metPhi)", "nh_m3p2_m1p3_noHEMphi_MEy", []],
    [ "nh_1p3_3p2_HEMphi_met*cos(nh_1p3_3p2_HEMphi_metPhi)", "nh_1p3_3p2_HEMphi_MEx", []],
    [ "nh_1p3_3p2_noHEMphi_met*cos(nh_1p3_3p2_noHEMphi_metPhi)", "nh_1p3_3p2_noHEMphi_MEx", []],
    [ "nh_1p3_3p2_HEMphi_met*sin(nh_1p3_3p2_HEMphi_metPhi)", "nh_1p3_3p2_HEMphi_MEy", []],
    [ "nh_1p3_3p2_noHEMphi_met*sin(nh_1p3_3p2_noHEMphi_metPhi)", "nh_1p3_3p2_noHEMphi_MEy", []],
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
selectionString += "&&(mll>20)"

#selectionString += "&&mll>20&&Sum$(jet_pt>30)>=2"

quantiles = [0.001,  0.05, 0.31, 0.5, 0.68, 0.95, 0.999]
colors    = [ROOT.kOrange, ROOT.kGreen, ROOT.kBlue, ROOT.kBlack,  ROOT.kBlue, ROOT.kGreen,  ROOT.kOrange]

for variable, name, lines in variables:
    # Get inclusive histogam
    #binning_y = [i/2. for i in range(-160,160)]
    binning_y = [i/2. for i in range(-40,40)]
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

    h_prehem.style = styles.lineStyle( ROOT.kBlue )
    h_hem.style = styles.lineStyle( ROOT.kRed )

    # 1D plot
    plot = Plot.fromHisto( name = '1D_'+name, histos = [ [h_prehem], [h_hem] ], texX = name, texY = "Number of Events")
    #plot = Plot.fromHisto( name = '1D_'+name, histos = [ [h_prehem] ], texX = name, texY = "Number of Events")
    
    q_lines = []
    for i_threshold in range(len(quantiles)):
        q_lines.append( ROOT.TLine( thresholds_hem[i_threshold], 0, thresholds_hem[i_threshold], 0.5) )
        q_lines[-1].SetLineColor( colors[ i_threshold ] )
        q_lines.append( ROOT.TLine( thresholds_prehem[i_threshold], 0, thresholds_prehem[i_threshold], 0.5) )
        q_lines[-1].SetLineColor( colors[ i_threshold ] )
        q_lines[-1].SetLineStyle( 2 )
        #h_inclusive.Rebin( 6 ) 

#    left  = thresholds_prehem[0]
#    right = thresholds_prehem[-1]
#    dx   = right - left
#    mean = 0.5*(left+right)
#
#    #for h in [ h_hem, h_prehem]:
#    for h in [ h_prehem]:
#        h.GetXaxis().SetRangeUser( mean - 0.7*dx, mean + 0.7*dx )

    plotting.draw(plot, 
        #ratio = {},
        legend      = ( [0.15, 0.80, 0.70, 0.90], 3 ),
        plot_directory = os.path.join( plot_directory, "JetMET/HEM", sample.name ),
        logX = False, logY = False, copyIndexPHP = True,
        drawObjects = q_lines,
        )

# OBJ: TBranch   evt evt/l : 0 at: 0x274ed40
# OBJ: TBranch   run run/I : 0 at: 0x2757470
# OBJ: TBranch   lumi    lumi/I : 0 at: 0x27598c0
# OBJ: TBranch   nVert   nVert/I : 0 at: 0x2759df0
# OBJ: TBranch   nVertAll    nVertAll/I : 0 at: 0x275a320
# OBJ: TBranch   bx  bx/I : 0 at: 0x275a850
# OBJ: TBranch   njet    njet/I : 0 at: 0x275ad80
# OBJ: TBranch   jet_pt  jet_pt[njet]/F : 0 at: 0x275b2b0
# OBJ: TBranch   jet_genPt   jet_genPt[njet]/F : 0 at: 0x275d7d0
# OBJ: TBranch   jet_genEta  jet_genEta[njet]/F : 0 at: 0x275de70
# OBJ: TBranch   jet_genPhi  jet_genPhi[njet]/F : 0 at: 0x275e570
# OBJ: TBranch   jet_rawPt   jet_rawPt[njet]/F : 0 at: 0x275ec70
# OBJ: TBranch   jet_eta jet_eta[njet]/F : 0 at: 0x275f340
# OBJ: TBranch   jet_phi jet_phi[njet]/F : 0 at: 0x275f9e0
# OBJ: TBranch   jet_chHEF   jet_chHEF[njet]/F : 0 at: 0x2760080
# OBJ: TBranch   jet_neHEF   jet_neHEF[njet]/F : 0 at: 0x2760750
# OBJ: TBranch   jet_phEF    jet_phEF[njet]/F : 0 at: 0x2760e20
# OBJ: TBranch   jet_eEF jet_eEF[njet]/F : 0 at: 0x27614f0
# OBJ: TBranch   jet_muEF    jet_muEF[njet]/F : 0 at: 0x2761b90
# OBJ: TBranch   jet_HFHEF   jet_HFHEF[njet]/F : 0 at: 0x2762260
# OBJ: TBranch   jet_HFEMEF  jet_HFEMEF[njet]/F : 0 at: 0x2762930
# OBJ: TBranch   jet_chHMult jet_chHMult[njet]/F : 0 at: 0x2763030
# OBJ: TBranch   jet_neHMult jet_neHMult[njet]/F : 0 at: 0x2763730
# OBJ: TBranch   jet_phMult  jet_phMult[njet]/F : 0 at: 0x2763e30
# OBJ: TBranch   jet_eMult   jet_eMult[njet]/F : 0 at: 0x2764530
# OBJ: TBranch   jet_muMult  jet_muMult[njet]/F : 0 at: 0x2764c00
# OBJ: TBranch   jet_HFHMult jet_HFHMult[njet]/F : 0 at: 0x2765300
# OBJ: TBranch   jet_HFEMMult    jet_HFEMMult[njet]/F : 0 at: 0x2765a00
# OBJ: TBranch   met_pt  met_pt/F : 0 at: 0x2766100
# OBJ: TBranch   met_phi met_phi/F : 0 at: 0x2766630
# OBJ: TBranch   mll mll/F : 0 at: 0x2766b60
# OBJ: TBranch   fixedGridRhoFastjetAll  fixedGridRhoFastjetAll/F : 0 at: 0x2767090
# OBJ: TBranch   Flag_goodVertices   Flag_goodVertices/I : 0 at: 0x2767680
# OBJ: TBranch   Flag_globalSuperTightHalo2016Filter Flag_globalSuperTightHalo2016Filter/I : 0 at: 0x2767c70
# OBJ: TBranch   Flag_HBHENoiseFilter    Flag_HBHENoiseFilter/I : 0 at: 0x27682a0
# OBJ: TBranch   Flag_HBHENoiseIsoFilter Flag_HBHENoiseIsoFilter/I : 0 at: 0x2768890
# OBJ: TBranch   Flag_EcalDeadCellTriggerPrimitiveFilter Flag_EcalDeadCellTriggerPrimitiveFilter/I : 0 at: 0x2768e80
# OBJ: TBranch   Flag_BadPFMuonFilter    Flag_BadPFMuonFilter/I : 0 at: 0x5c31c00
# OBJ: TBranch   Flag_BadChargedCandidateFilter  Flag_BadChargedCandidateFilter/I : 0 at: 0x5c321f0
# OBJ: TBranch   Flag_eeBadScFilter  Flag_eeBadScFilter/I : 0 at: 0x5c327f0
# OBJ: TBranch   ga_m5p1_m3p2_HEMphi_met ga_m5p1_m3p2_HEMphi_met/F : 0 at: 0x5c32de0
# OBJ: TBranch   ga_m5p1_m3p2_HEMphi_sumPt   ga_m5p1_m3p2_HEMphi_sumPt/F : 0 at: 0x5c333d0
# OBJ: TBranch   ga_m5p1_m3p2_HEMphi_metPhi  ga_m5p1_m3p2_HEMphi_metPhi/F : 0 at: 0x5c339c0
# OBJ: TBranch   ch_m5p1_m3p2_HEMphi_met ch_m5p1_m3p2_HEMphi_met/F : 0 at: 0x5c33fb0
# OBJ: TBranch   ch_m5p1_m3p2_HEMphi_sumPt   ch_m5p1_m3p2_HEMphi_sumPt/F : 0 at: 0x5c345a0
# OBJ: TBranch   ch_m5p1_m3p2_HEMphi_metPhi  ch_m5p1_m3p2_HEMphi_metPhi/F : 0 at: 0x5c34b90
# OBJ: TBranch   nh_m5p1_m3p2_HEMphi_met nh_m5p1_m3p2_HEMphi_met/F : 0 at: 0x5c35180
# OBJ: TBranch   nh_m5p1_m3p2_HEMphi_sumPt   nh_m5p1_m3p2_HEMphi_sumPt/F : 0 at: 0x5c35770
# OBJ: TBranch   nh_m5p1_m3p2_HEMphi_metPhi  nh_m5p1_m3p2_HEMphi_metPhi/F : 0 at: 0x5c35d60
# OBJ: TBranch   all_m5p1_m3p2_HEMphi_met    all_m5p1_m3p2_HEMphi_met/F : 0 at: 0x5c36350
# OBJ: TBranch   all_m5p1_m3p2_HEMphi_sumPt  all_m5p1_m3p2_HEMphi_sumPt/F : 0 at: 0x5c36940
# OBJ: TBranch   all_m5p1_m3p2_HEMphi_metPhi all_m5p1_m3p2_HEMphi_metPhi/F : 0 at: 0x5c36f30
# OBJ: TBranch   ga_m5p1_m3p2_noHEMphi_met   ga_m5p1_m3p2_noHEMphi_met/F : 0 at: 0x5c37520
# OBJ: TBranch   ga_m5p1_m3p2_noHEMphi_sumPt ga_m5p1_m3p2_noHEMphi_sumPt/F : 0 at: 0x5c37b10
# OBJ: TBranch   ga_m5p1_m3p2_noHEMphi_metPhi    ga_m5p1_m3p2_noHEMphi_metPhi/F : 0 at: 0x5c38100
# OBJ: TBranch   ch_m5p1_m3p2_noHEMphi_met   ch_m5p1_m3p2_noHEMphi_met/F : 0 at: 0x5c386f0
# OBJ: TBranch   ch_m5p1_m3p2_noHEMphi_sumPt ch_m5p1_m3p2_noHEMphi_sumPt/F : 0 at: 0x5c38ce0
# OBJ: TBranch   ch_m5p1_m3p2_noHEMphi_metPhi    ch_m5p1_m3p2_noHEMphi_metPhi/F : 0 at: 0x5c392d0
# OBJ: TBranch   nh_m5p1_m3p2_noHEMphi_met   nh_m5p1_m3p2_noHEMphi_met/F : 0 at: 0x5c398c0
# OBJ: TBranch   nh_m5p1_m3p2_noHEMphi_sumPt nh_m5p1_m3p2_noHEMphi_sumPt/F : 0 at: 0x5c39eb0
# OBJ: TBranch   nh_m5p1_m3p2_noHEMphi_metPhi    nh_m5p1_m3p2_noHEMphi_metPhi/F : 0 at: 0x5c3a4a0
# OBJ: TBranch   all_m5p1_m3p2_noHEMphi_met  all_m5p1_m3p2_noHEMphi_met/F : 0 at: 0x5c3aa90
# OBJ: TBranch   all_m5p1_m3p2_noHEMphi_sumPt    all_m5p1_m3p2_noHEMphi_sumPt/F : 0 at: 0x5c3b080
# OBJ: TBranch   all_m5p1_m3p2_noHEMphi_metPhi   all_m5p1_m3p2_noHEMphi_metPhi/F : 0 at: 0x5c3b670
# OBJ: TBranch   ga_m5p1_m3p2_all_met    ga_m5p1_m3p2_all_met/F : 0 at: 0x5c3bc60
# OBJ: TBranch   ga_m5p1_m3p2_all_sumPt  ga_m5p1_m3p2_all_sumPt/F : 0 at: 0x5c3c250
# OBJ: TBranch   ga_m5p1_m3p2_all_metPhi ga_m5p1_m3p2_all_metPhi/F : 0 at: 0x5c3c840
# OBJ: TBranch   ch_m5p1_m3p2_all_met    ch_m5p1_m3p2_all_met/F : 0 at: 0x5c3ce30
# OBJ: TBranch   ch_m5p1_m3p2_all_sumPt  ch_m5p1_m3p2_all_sumPt/F : 0 at: 0x5c3d420
# OBJ: TBranch   ch_m5p1_m3p2_all_metPhi ch_m5p1_m3p2_all_metPhi/F : 0 at: 0x5c3da10
# OBJ: TBranch   nh_m5p1_m3p2_all_met    nh_m5p1_m3p2_all_met/F : 0 at: 0x5c3e000
# OBJ: TBranch   nh_m5p1_m3p2_all_sumPt  nh_m5p1_m3p2_all_sumPt/F : 0 at: 0x5c3e5f0
# OBJ: TBranch   nh_m5p1_m3p2_all_metPhi nh_m5p1_m3p2_all_metPhi/F : 0 at: 0x5c3ebe0
# OBJ: TBranch   all_m5p1_m3p2_all_met   all_m5p1_m3p2_all_met/F : 0 at: 0x5c3f1d0
# OBJ: TBranch   all_m5p1_m3p2_all_sumPt all_m5p1_m3p2_all_sumPt/F : 0 at: 0x5c3f7c0
# OBJ: TBranch   all_m5p1_m3p2_all_metPhi    all_m5p1_m3p2_all_metPhi/F : 0 at: 0x5c3fdb0
# OBJ: TBranch   ga_m3p2_m1p3_HEMphi_met ga_m3p2_m1p3_HEMphi_met/F : 0 at: 0x5c403a0
# OBJ: TBranch   ga_m3p2_m1p3_HEMphi_sumPt   ga_m3p2_m1p3_HEMphi_sumPt/F : 0 at: 0x5c40990
# OBJ: TBranch   ga_m3p2_m1p3_HEMphi_metPhi  ga_m3p2_m1p3_HEMphi_metPhi/F : 0 at: 0x5c40f80
# OBJ: TBranch   ch_m3p2_m1p3_HEMphi_met ch_m3p2_m1p3_HEMphi_met/F : 0 at: 0x5c41570
# OBJ: TBranch   ch_m3p2_m1p3_HEMphi_sumPt   ch_m3p2_m1p3_HEMphi_sumPt/F : 0 at: 0x5c41b60
# OBJ: TBranch   ch_m3p2_m1p3_HEMphi_metPhi  ch_m3p2_m1p3_HEMphi_metPhi/F : 0 at: 0x5c42150
# OBJ: TBranch   nh_m3p2_m1p3_HEMphi_met nh_m3p2_m1p3_HEMphi_met/F : 0 at: 0x5c42740
# OBJ: TBranch   nh_m3p2_m1p3_HEMphi_sumPt   nh_m3p2_m1p3_HEMphi_sumPt/F : 0 at: 0x5c42d30
# OBJ: TBranch   nh_m3p2_m1p3_HEMphi_metPhi  nh_m3p2_m1p3_HEMphi_metPhi/F : 0 at: 0x5c43320
# OBJ: TBranch   all_m3p2_m1p3_HEMphi_met    all_m3p2_m1p3_HEMphi_met/F : 0 at: 0x5c43910
# OBJ: TBranch   all_m3p2_m1p3_HEMphi_sumPt  all_m3p2_m1p3_HEMphi_sumPt/F : 0 at: 0x5c43f00
# OBJ: TBranch   all_m3p2_m1p3_HEMphi_metPhi all_m3p2_m1p3_HEMphi_metPhi/F : 0 at: 0x5c444f0
# OBJ: TBranch   ga_m3p2_m1p3_noHEMphi_met   ga_m3p2_m1p3_noHEMphi_met/F : 0 at: 0x5c44ae0
# OBJ: TBranch   ga_m3p2_m1p3_noHEMphi_sumPt ga_m3p2_m1p3_noHEMphi_sumPt/F : 0 at: 0x5c450d0
# OBJ: TBranch   ga_m3p2_m1p3_noHEMphi_metPhi    ga_m3p2_m1p3_noHEMphi_metPhi/F : 0 at: 0x5c456c0
# OBJ: TBranch   ch_m3p2_m1p3_noHEMphi_met   ch_m3p2_m1p3_noHEMphi_met/F : 0 at: 0x5c45cb0
# OBJ: TBranch   ch_m3p2_m1p3_noHEMphi_sumPt ch_m3p2_m1p3_noHEMphi_sumPt/F : 0 at: 0x5c462a0
# OBJ: TBranch   ch_m3p2_m1p3_noHEMphi_metPhi    ch_m3p2_m1p3_noHEMphi_metPhi/F : 0 at: 0x5c46890
# OBJ: TBranch   nh_m3p2_m1p3_noHEMphi_met   nh_m3p2_m1p3_noHEMphi_met/F : 0 at: 0x5c46e80
# OBJ: TBranch   nh_m3p2_m1p3_noHEMphi_sumPt nh_m3p2_m1p3_noHEMphi_sumPt/F : 0 at: 0x5c47470
# OBJ: TBranch   nh_m3p2_m1p3_noHEMphi_metPhi    nh_m3p2_m1p3_noHEMphi_metPhi/F : 0 at: 0x5c47a60
# OBJ: TBranch   all_m3p2_m1p3_noHEMphi_met  all_m3p2_m1p3_noHEMphi_met/F : 0 at: 0x5c48050
# OBJ: TBranch   all_m3p2_m1p3_noHEMphi_sumPt    all_m3p2_m1p3_noHEMphi_sumPt/F : 0 at: 0x5c48640
# OBJ: TBranch   all_m3p2_m1p3_noHEMphi_metPhi   all_m3p2_m1p3_noHEMphi_metPhi/F : 0 at: 0x5c48c30
# OBJ: TBranch   ga_m3p2_m1p3_all_met    ga_m3p2_m1p3_all_met/F : 0 at: 0x5c49220
# OBJ: TBranch   ga_m3p2_m1p3_all_sumPt  ga_m3p2_m1p3_all_sumPt/F : 0 at: 0x5c49810
# OBJ: TBranch   ga_m3p2_m1p3_all_metPhi ga_m3p2_m1p3_all_metPhi/F : 0 at: 0x5c49e00
# OBJ: TBranch   ch_m3p2_m1p3_all_met    ch_m3p2_m1p3_all_met/F : 0 at: 0x5c4a3f0
# OBJ: TBranch   ch_m3p2_m1p3_all_sumPt  ch_m3p2_m1p3_all_sumPt/F : 0 at: 0x5c4a9e0
# OBJ: TBranch   ch_m3p2_m1p3_all_metPhi ch_m3p2_m1p3_all_metPhi/F : 0 at: 0x5c4afd0
# OBJ: TBranch   nh_m3p2_m1p3_all_met    nh_m3p2_m1p3_all_met/F : 0 at: 0x5c4b5c0
# OBJ: TBranch   nh_m3p2_m1p3_all_sumPt  nh_m3p2_m1p3_all_sumPt/F : 0 at: 0x5c4bbb0
# OBJ: TBranch   nh_m3p2_m1p3_all_metPhi nh_m3p2_m1p3_all_metPhi/F : 0 at: 0x5c4c1a0
# OBJ: TBranch   all_m3p2_m1p3_all_met   all_m3p2_m1p3_all_met/F : 0 at: 0x5c4c790
# OBJ: TBranch   all_m3p2_m1p3_all_sumPt all_m3p2_m1p3_all_sumPt/F : 0 at: 0x5c4cd80
# OBJ: TBranch   all_m3p2_m1p3_all_metPhi    all_m3p2_m1p3_all_metPhi/F : 0 at: 0x5c4d370
# OBJ: TBranch   ga_m1p3_1p3_HEMphi_met  ga_m1p3_1p3_HEMphi_met/F : 0 at: 0x5c4d960
# OBJ: TBranch   ga_m1p3_1p3_HEMphi_sumPt    ga_m1p3_1p3_HEMphi_sumPt/F : 0 at: 0x5c4df50
# OBJ: TBranch   ga_m1p3_1p3_HEMphi_metPhi   ga_m1p3_1p3_HEMphi_metPhi/F : 0 at: 0x5c4e540
# OBJ: TBranch   ch_m1p3_1p3_HEMphi_met  ch_m1p3_1p3_HEMphi_met/F : 0 at: 0x5c4eb30
# OBJ: TBranch   ch_m1p3_1p3_HEMphi_sumPt    ch_m1p3_1p3_HEMphi_sumPt/F : 0 at: 0x5c4f120
# OBJ: TBranch   ch_m1p3_1p3_HEMphi_metPhi   ch_m1p3_1p3_HEMphi_metPhi/F : 0 at: 0x5c4f710
# OBJ: TBranch   nh_m1p3_1p3_HEMphi_met  nh_m1p3_1p3_HEMphi_met/F : 0 at: 0x5c4fd00
# OBJ: TBranch   nh_m1p3_1p3_HEMphi_sumPt    nh_m1p3_1p3_HEMphi_sumPt/F : 0 at: 0x5c502f0
# OBJ: TBranch   nh_m1p3_1p3_HEMphi_metPhi   nh_m1p3_1p3_HEMphi_metPhi/F : 0 at: 0x5c508e0
# OBJ: TBranch   all_m1p3_1p3_HEMphi_met all_m1p3_1p3_HEMphi_met/F : 0 at: 0x5c50ed0
# OBJ: TBranch   all_m1p3_1p3_HEMphi_sumPt   all_m1p3_1p3_HEMphi_sumPt/F : 0 at: 0x5c514c0
# OBJ: TBranch   all_m1p3_1p3_HEMphi_metPhi  all_m1p3_1p3_HEMphi_metPhi/F : 0 at: 0x5c51ab0
# OBJ: TBranch   ga_m1p3_1p3_noHEMphi_met    ga_m1p3_1p3_noHEMphi_met/F : 0 at: 0x5c520a0
# OBJ: TBranch   ga_m1p3_1p3_noHEMphi_sumPt  ga_m1p3_1p3_noHEMphi_sumPt/F : 0 at: 0x5c52660
# OBJ: TBranch   ga_m1p3_1p3_noHEMphi_metPhi ga_m1p3_1p3_noHEMphi_metPhi/F : 0 at: 0x5c52c50
# OBJ: TBranch   ch_m1p3_1p3_noHEMphi_met    ch_m1p3_1p3_noHEMphi_met/F : 0 at: 0x5c53240
# OBJ: TBranch   ch_m1p3_1p3_noHEMphi_sumPt  ch_m1p3_1p3_noHEMphi_sumPt/F : 0 at: 0x5c53830
# OBJ: TBranch   ch_m1p3_1p3_noHEMphi_metPhi ch_m1p3_1p3_noHEMphi_metPhi/F : 0 at: 0x5c53e20
# OBJ: TBranch   nh_m1p3_1p3_noHEMphi_met    nh_m1p3_1p3_noHEMphi_met/F : 0 at: 0x5c54410
# OBJ: TBranch   nh_m1p3_1p3_noHEMphi_sumPt  nh_m1p3_1p3_noHEMphi_sumPt/F : 0 at: 0x5c54a00
# OBJ: TBranch   nh_m1p3_1p3_noHEMphi_metPhi nh_m1p3_1p3_noHEMphi_metPhi/F : 0 at: 0x5c54ff0
# OBJ: TBranch   all_m1p3_1p3_noHEMphi_met   all_m1p3_1p3_noHEMphi_met/F : 0 at: 0x5c555e0
# OBJ: TBranch   all_m1p3_1p3_noHEMphi_sumPt all_m1p3_1p3_noHEMphi_sumPt/F : 0 at: 0x5c55bd0
# OBJ: TBranch   all_m1p3_1p3_noHEMphi_metPhi    all_m1p3_1p3_noHEMphi_metPhi/F : 0 at: 0x5c561c0
# OBJ: TBranch   ga_m1p3_1p3_all_met ga_m1p3_1p3_all_met/F : 0 at: 0x5c567b0
# OBJ: TBranch   ga_m1p3_1p3_all_sumPt   ga_m1p3_1p3_all_sumPt/F : 0 at: 0x5c56da0
# OBJ: TBranch   ga_m1p3_1p3_all_metPhi  ga_m1p3_1p3_all_metPhi/F : 0 at: 0x5c57390
# OBJ: TBranch   ch_m1p3_1p3_all_met ch_m1p3_1p3_all_met/F : 0 at: 0x5c57980
# OBJ: TBranch   ch_m1p3_1p3_all_sumPt   ch_m1p3_1p3_all_sumPt/F : 0 at: 0x5c57f70
# OBJ: TBranch   ch_m1p3_1p3_all_metPhi  ch_m1p3_1p3_all_metPhi/F : 0 at: 0x5c58580
# OBJ: TBranch   nh_m1p3_1p3_all_met nh_m1p3_1p3_all_met/F : 0 at: 0x5c58b90
# OBJ: TBranch   nh_m1p3_1p3_all_sumPt   nh_m1p3_1p3_all_sumPt/F : 0 at: 0x5c591a0
# OBJ: TBranch   nh_m1p3_1p3_all_metPhi  nh_m1p3_1p3_all_metPhi/F : 0 at: 0x5c597b0
# OBJ: TBranch   all_m1p3_1p3_all_met    all_m1p3_1p3_all_met/F : 0 at: 0x5c59dc0
# OBJ: TBranch   all_m1p3_1p3_all_sumPt  all_m1p3_1p3_all_sumPt/F : 0 at: 0x5c5a3d0
# OBJ: TBranch   all_m1p3_1p3_all_metPhi all_m1p3_1p3_all_metPhi/F : 0 at: 0x5c5a9e0
# OBJ: TBranch   ga_1p3_3p2_HEMphi_met   ga_1p3_3p2_HEMphi_met/F : 0 at: 0x5c5aff0
# OBJ: TBranch   ga_1p3_3p2_HEMphi_sumPt ga_1p3_3p2_HEMphi_sumPt/F : 0 at: 0x5c5b600
# OBJ: TBranch   ga_1p3_3p2_HEMphi_metPhi    ga_1p3_3p2_HEMphi_metPhi/F : 0 at: 0x5c5bc10
# OBJ: TBranch   ch_1p3_3p2_HEMphi_met   ch_1p3_3p2_HEMphi_met/F : 0 at: 0x5c5c220
# OBJ: TBranch   ch_1p3_3p2_HEMphi_sumPt ch_1p3_3p2_HEMphi_sumPt/F : 0 at: 0x5c5c830
# OBJ: TBranch   ch_1p3_3p2_HEMphi_metPhi    ch_1p3_3p2_HEMphi_metPhi/F : 0 at: 0x5c5ce40
# OBJ: TBranch   nh_1p3_3p2_HEMphi_met   nh_1p3_3p2_HEMphi_met/F : 0 at: 0x5c5d450
# OBJ: TBranch   nh_1p3_3p2_HEMphi_sumPt nh_1p3_3p2_HEMphi_sumPt/F : 0 at: 0x5c5da60
# OBJ: TBranch   nh_1p3_3p2_HEMphi_metPhi    nh_1p3_3p2_HEMphi_metPhi/F : 0 at: 0x5c5e070
# OBJ: TBranch   all_1p3_3p2_HEMphi_met  all_1p3_3p2_HEMphi_met/F : 0 at: 0x5c5e680
# OBJ: TBranch   all_1p3_3p2_HEMphi_sumPt    all_1p3_3p2_HEMphi_sumPt/F : 0 at: 0x5c5ec90
# OBJ: TBranch   all_1p3_3p2_HEMphi_metPhi   all_1p3_3p2_HEMphi_metPhi/F : 0 at: 0x5c5f2a0
# OBJ: TBranch   ga_1p3_3p2_noHEMphi_met ga_1p3_3p2_noHEMphi_met/F : 0 at: 0x5c5f8b0
# OBJ: TBranch   ga_1p3_3p2_noHEMphi_sumPt   ga_1p3_3p2_noHEMphi_sumPt/F : 0 at: 0x5c5fec0
# OBJ: TBranch   ga_1p3_3p2_noHEMphi_metPhi  ga_1p3_3p2_noHEMphi_metPhi/F : 0 at: 0x5c604d0
# OBJ: TBranch   ch_1p3_3p2_noHEMphi_met ch_1p3_3p2_noHEMphi_met/F : 0 at: 0x5c60ae0
# OBJ: TBranch   ch_1p3_3p2_noHEMphi_sumPt   ch_1p3_3p2_noHEMphi_sumPt/F : 0 at: 0x5c610f0
# OBJ: TBranch   ch_1p3_3p2_noHEMphi_metPhi  ch_1p3_3p2_noHEMphi_metPhi/F : 0 at: 0x5c61700
# OBJ: TBranch   nh_1p3_3p2_noHEMphi_met nh_1p3_3p2_noHEMphi_met/F : 0 at: 0x5c61d10
# OBJ: TBranch   nh_1p3_3p2_noHEMphi_sumPt   nh_1p3_3p2_noHEMphi_sumPt/F : 0 at: 0x5c62320
# OBJ: TBranch   nh_1p3_3p2_noHEMphi_metPhi  nh_1p3_3p2_noHEMphi_metPhi/F : 0 at: 0x5c62930
# OBJ: TBranch   all_1p3_3p2_noHEMphi_met    all_1p3_3p2_noHEMphi_met/F : 0 at: 0x5c62f40
# OBJ: TBranch   all_1p3_3p2_noHEMphi_sumPt  all_1p3_3p2_noHEMphi_sumPt/F : 0 at: 0x5c63550
# OBJ: TBranch   all_1p3_3p2_noHEMphi_metPhi all_1p3_3p2_noHEMphi_metPhi/F : 0 at: 0x5c63b60
# OBJ: TBranch   ga_1p3_3p2_all_met  ga_1p3_3p2_all_met/F : 0 at: 0x5c64170
# OBJ: TBranch   ga_1p3_3p2_all_sumPt    ga_1p3_3p2_all_sumPt/F : 0 at: 0x5c64780
# OBJ: TBranch   ga_1p3_3p2_all_metPhi   ga_1p3_3p2_all_metPhi/F : 0 at: 0x5c64d90
# OBJ: TBranch   ch_1p3_3p2_all_met  ch_1p3_3p2_all_met/F : 0 at: 0x5c653a0
# OBJ: TBranch   ch_1p3_3p2_all_sumPt    ch_1p3_3p2_all_sumPt/F : 0 at: 0x5c659b0
# OBJ: TBranch   ch_1p3_3p2_all_metPhi   ch_1p3_3p2_all_metPhi/F : 0 at: 0x5c65fc0
# OBJ: TBranch   nh_1p3_3p2_all_met  nh_1p3_3p2_all_met/F : 0 at: 0x5c665d0
# OBJ: TBranch   nh_1p3_3p2_all_sumPt    nh_1p3_3p2_all_sumPt/F : 0 at: 0x5c66be0
# OBJ: TBranch   nh_1p3_3p2_all_metPhi   nh_1p3_3p2_all_metPhi/F : 0 at: 0x5c671f0
# OBJ: TBranch   all_1p3_3p2_all_met all_1p3_3p2_all_met/F : 0 at: 0x5c67800
# OBJ: TBranch   all_1p3_3p2_all_sumPt   all_1p3_3p2_all_sumPt/F : 0 at: 0x5c67e10
# OBJ: TBranch   all_1p3_3p2_all_metPhi  all_1p3_3p2_all_metPhi/F : 0 at: 0x5c68420
# OBJ: TBranch   ga_3p2_5p1_HEMphi_met   ga_3p2_5p1_HEMphi_met/F : 0 at: 0x5c68a30
# OBJ: TBranch   ga_3p2_5p1_HEMphi_sumPt ga_3p2_5p1_HEMphi_sumPt/F : 0 at: 0x5c69040
# OBJ: TBranch   ga_3p2_5p1_HEMphi_metPhi    ga_3p2_5p1_HEMphi_metPhi/F : 0 at: 0x401d580
# OBJ: TBranch   ch_3p2_5p1_HEMphi_met   ch_3p2_5p1_HEMphi_met/F : 0 at: 0x401db90
# OBJ: TBranch   ch_3p2_5p1_HEMphi_sumPt ch_3p2_5p1_HEMphi_sumPt/F : 0 at: 0x401e1a0
# OBJ: TBranch   ch_3p2_5p1_HEMphi_metPhi    ch_3p2_5p1_HEMphi_metPhi/F : 0 at: 0x401e7b0
# OBJ: TBranch   nh_3p2_5p1_HEMphi_met   nh_3p2_5p1_HEMphi_met/F : 0 at: 0x401edc0
# OBJ: TBranch   nh_3p2_5p1_HEMphi_sumPt nh_3p2_5p1_HEMphi_sumPt/F : 0 at: 0x401f3d0
# OBJ: TBranch   nh_3p2_5p1_HEMphi_metPhi    nh_3p2_5p1_HEMphi_metPhi/F : 0 at: 0x401f9e0
# OBJ: TBranch   all_3p2_5p1_HEMphi_met  all_3p2_5p1_HEMphi_met/F : 0 at: 0x401fff0
# OBJ: TBranch   all_3p2_5p1_HEMphi_sumPt    all_3p2_5p1_HEMphi_sumPt/F : 0 at: 0x3f67350
# OBJ: TBranch   all_3p2_5p1_HEMphi_metPhi   all_3p2_5p1_HEMphi_metPhi/F : 0 at: 0x3f67960
# OBJ: TBranch   ga_3p2_5p1_noHEMphi_met ga_3p2_5p1_noHEMphi_met/F : 0 at: 0x3f67f70
# OBJ: TBranch   ga_3p2_5p1_noHEMphi_sumPt   ga_3p2_5p1_noHEMphi_sumPt/F : 0 at: 0x3f68580
# OBJ: TBranch   ga_3p2_5p1_noHEMphi_metPhi  ga_3p2_5p1_noHEMphi_metPhi/F : 0 at: 0x3f68b90
# OBJ: TBranch   ch_3p2_5p1_noHEMphi_met ch_3p2_5p1_noHEMphi_met/F : 0 at: 0x3f691a0
# OBJ: TBranch   ch_3p2_5p1_noHEMphi_sumPt   ch_3p2_5p1_noHEMphi_sumPt/F : 0 at: 0x3f697b0
# OBJ: TBranch   ch_3p2_5p1_noHEMphi_metPhi  ch_3p2_5p1_noHEMphi_metPhi/F : 0 at: 0x5c75130
# OBJ: TBranch   nh_3p2_5p1_noHEMphi_met nh_3p2_5p1_noHEMphi_met/F : 0 at: 0x5c75630
# OBJ: TBranch   nh_3p2_5p1_noHEMphi_sumPt   nh_3p2_5p1_noHEMphi_sumPt/F : 0 at: 0x5c75c40
# OBJ: TBranch   nh_3p2_5p1_noHEMphi_metPhi  nh_3p2_5p1_noHEMphi_metPhi/F : 0 at: 0x5c76250
# OBJ: TBranch   all_3p2_5p1_noHEMphi_met    all_3p2_5p1_noHEMphi_met/F : 0 at: 0x5c76860
# OBJ: TBranch   all_3p2_5p1_noHEMphi_sumPt  all_3p2_5p1_noHEMphi_sumPt/F : 0 at: 0x5c76e70
# OBJ: TBranch   all_3p2_5p1_noHEMphi_metPhi all_3p2_5p1_noHEMphi_metPhi/F : 0 at: 0x5c77480
# OBJ: TBranch   ga_3p2_5p1_all_met  ga_3p2_5p1_all_met/F : 0 at: 0x5c77a90
# OBJ: TBranch   ga_3p2_5p1_all_sumPt    ga_3p2_5p1_all_sumPt/F : 0 at: 0x5c780a0
# OBJ: TBranch   ga_3p2_5p1_all_metPhi   ga_3p2_5p1_all_metPhi/F : 0 at: 0x5c786b0
# OBJ: TBranch   ch_3p2_5p1_all_met  ch_3p2_5p1_all_met/F : 0 at: 0x5c78cc0
# OBJ: TBranch   ch_3p2_5p1_all_sumPt    ch_3p2_5p1_all_sumPt/F : 0 at: 0x5c792d0
# OBJ: TBranch   ch_3p2_5p1_all_metPhi   ch_3p2_5p1_all_metPhi/F : 0 at: 0x5c798e0
# OBJ: TBranch   nh_3p2_5p1_all_met  nh_3p2_5p1_all_met/F : 0 at: 0x5c79ef0
# OBJ: TBranch   nh_3p2_5p1_all_sumPt    nh_3p2_5p1_all_sumPt/F : 0 at: 0x5c7a500
# OBJ: TBranch   nh_3p2_5p1_all_metPhi   nh_3p2_5p1_all_metPhi/F : 0 at: 0x5c7ab10
# OBJ: TBranch   all_3p2_5p1_all_met all_3p2_5p1_all_met/F : 0 at: 0x5c7b120
# OBJ: TBranch   all_3p2_5p1_all_sumPt   all_3p2_5p1_all_sumPt/F : 0 at: 0x5c7b730
# OBJ: TBranch   all_3p2_5p1_all_metPhi  all_3p2_5p1_all_metPhi/F : 0 at: 0x5c7bd40
# OBJ: TBranch   ga_all_HEMphi_met   ga_all_HEMphi_met/F : 0 at: 0x5c7c350
# OBJ: TBranch   ga_all_HEMphi_sumPt ga_all_HEMphi_sumPt/F : 0 at: 0x5c7c960
# OBJ: TBranch   ga_all_HEMphi_metPhi    ga_all_HEMphi_metPhi/F : 0 at: 0x5c7cf70
# OBJ: TBranch   ch_all_HEMphi_met   ch_all_HEMphi_met/F : 0 at: 0x5c7d580
# OBJ: TBranch   ch_all_HEMphi_sumPt ch_all_HEMphi_sumPt/F : 0 at: 0x5c7db90
# OBJ: TBranch   ch_all_HEMphi_metPhi    ch_all_HEMphi_metPhi/F : 0 at: 0x5c7e1a0
# OBJ: TBranch   nh_all_HEMphi_met   nh_all_HEMphi_met/F : 0 at: 0x5c7e7b0
# OBJ: TBranch   nh_all_HEMphi_sumPt nh_all_HEMphi_sumPt/F : 0 at: 0x5c7edc0
# OBJ: TBranch   nh_all_HEMphi_metPhi    nh_all_HEMphi_metPhi/F : 0 at: 0x5c7f3d0
# OBJ: TBranch   all_all_HEMphi_met  all_all_HEMphi_met/F : 0 at: 0x5c7f9e0
# OBJ: TBranch   all_all_HEMphi_sumPt    all_all_HEMphi_sumPt/F : 0 at: 0x5c7fff0
# OBJ: TBranch   all_all_HEMphi_metPhi   all_all_HEMphi_metPhi/F : 0 at: 0x5c80600
# OBJ: TBranch   ga_all_noHEMphi_met ga_all_noHEMphi_met/F : 0 at: 0x5c80c10
# OBJ: TBranch   ga_all_noHEMphi_sumPt   ga_all_noHEMphi_sumPt/F : 0 at: 0x5c81220
# OBJ: TBranch   ga_all_noHEMphi_metPhi  ga_all_noHEMphi_metPhi/F : 0 at: 0x5c81830
# OBJ: TBranch   ch_all_noHEMphi_met ch_all_noHEMphi_met/F : 0 at: 0x5c81e40
# OBJ: TBranch   ch_all_noHEMphi_sumPt   ch_all_noHEMphi_sumPt/F : 0 at: 0x5c82450
# OBJ: TBranch   ch_all_noHEMphi_metPhi  ch_all_noHEMphi_metPhi/F : 0 at: 0x5c82a60
# OBJ: TBranch   nh_all_noHEMphi_met nh_all_noHEMphi_met/F : 0 at: 0x5c83070
# OBJ: TBranch   nh_all_noHEMphi_sumPt   nh_all_noHEMphi_sumPt/F : 0 at: 0x5c83680
# OBJ: TBranch   nh_all_noHEMphi_metPhi  nh_all_noHEMphi_metPhi/F : 0 at: 0x5c83c90
# OBJ: TBranch   all_all_noHEMphi_met    all_all_noHEMphi_met/F : 0 at: 0x5c842a0
# OBJ: TBranch   all_all_noHEMphi_sumPt  all_all_noHEMphi_sumPt/F : 0 at: 0x5c848b0
# OBJ: TBranch   all_all_noHEMphi_metPhi all_all_noHEMphi_metPhi/F : 0 at: 0x5c84ec0
# OBJ: TBranch   ga_all_all_met  ga_all_all_met/F : 0 at: 0x5c854d0
# OBJ: TBranch   ga_all_all_sumPt    ga_all_all_sumPt/F : 0 at: 0x5c85a50
# OBJ: TBranch   ga_all_all_metPhi   ga_all_all_metPhi/F : 0 at: 0x5c86060
# OBJ: TBranch   ch_all_all_met  ch_all_all_met/F : 0 at: 0x5c86670
# OBJ: TBranch   ch_all_all_sumPt    ch_all_all_sumPt/F : 0 at: 0x5c86bf0
# OBJ: TBranch   ch_all_all_metPhi   ch_all_all_metPhi/F : 0 at: 0x5c87200
# OBJ: TBranch   nh_all_all_met  nh_all_all_met/F : 0 at: 0x5c87810
# OBJ: TBranch   nh_all_all_sumPt    nh_all_all_sumPt/F : 0 at: 0x5c87d90
# OBJ: TBranch   nh_all_all_metPhi   nh_all_all_metPhi/F : 0 at: 0x5c883a0
# OBJ: TBranch   all_all_all_met all_all_all_met/F : 0 at: 0x5c889b0
# OBJ: TBranch   all_all_all_sumPt   all_all_all_sumPt/F : 0 at: 0x5c88f90
# OBJ: TBranch   all_all_all_metPhi  all_all_all_metPhi/F : 0 at: 0x5c895a0

