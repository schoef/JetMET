# Standard imports
from RootTools.core.standard import *

# Samples
from JetMET.diagnosis.pu2018.samples import *

# define TProfiles
nvtx_thresholds = [2*i for i in range(51)]
rho_thresholds  = [2*i for i in range(33)]

variables = [ 
    [ "nVert", "nVert", nvtx_thresholds],
    [ "HF_sumPt", "all_3p1_5p1_sumPt+all_m5p1_m3p1_sumPt", [50*i for i in range(41)]],
#    [ "nVertAll", "nVertAll", nvtx_thresholds],
#    [ "mu_met", "mu_all_met", [5*i for i in range(41)]],
#    [ "rhoAll", "fixedGridRhoAll", rho_thresholds],
#    [ "rhoFastjetAll", "fixedGridRhoFastjetAll", rho_thresholds],
#    [ "rhoFastjetAllCalo", "fixedGridRhoFastjetAllCalo", rho_thresholds],
#    [ "rhoFastjetCentral", "fixedGridRhoFastjetCentral", rho_thresholds],
#    [ "rhoFastjetCentralCalo", "fixedGridRhoFastjetCentralCalo", rho_thresholds],
#    [ "rhoFastjetCentralChargedPileUp", "fixedGridRhoFastjetCentralChargedPileUp", rho_thresholds],
#    [ "rhoFastjetCentralNeutral", "fixedGridRhoFastjetCentralNeutral", rho_thresholds],

  [ "HFh_m5p1_m3p1_met", "HFh_m5p1_m3p1_met", [4*i for i in range(41)]],
  [ "HFh_m5p1_m3p1_sumPt", "HFh_m5p1_m3p1_sumPt", [16*i for i in range(41)]],
  [ "HFh_m5p1_m3p1_mult", "HFh_m5p1_m3p1_mult", [12*i for i in range(41)]],
  [ "HFe_m5p1_m3p1_met", "HFe_m5p1_m3p1_met", [2*i for i in range(41)]],
  [ "HFe_m5p1_m3p1_sumPt", "HFe_m5p1_m3p1_sumPt", [4*i for i in range(41)]],
  [ "HFe_m5p1_m3p1_mult", "HFe_m5p1_m3p1_mult", [6*i for i in range(41)]],
  [ "all_m5p1_m3p1_met", "all_m5p1_m3p1_met", [20*i for i in range(41)]],
  [ "all_m5p1_m3p1_sumPt", "all_m5p1_m3p1_sumPt", [40*i for i in range(41)]],
  [ "all_m5p1_m3p1_mult", "all_m5p1_m3p1_mult", [30*i for i in range(41)]],
  [ "el_m3p1_m2p5_met", "el_m3p1_m2p5_met", [2*i for i in range(41)]],
  [ "el_m3p1_m2p5_sumPt", "el_m3p1_m2p5_sumPt", [4*i for i in range(41)]],
  [ "el_m3p1_m2p5_mult", "el_m3p1_m2p5_mult", [1*i for i in range(11)]],
  [ "mu_m3p1_m2p5_met", "mu_m3p1_m2p5_met", [2*i for i in range(41)]],
  [ "mu_m3p1_m2p5_sumPt", "mu_m3p1_m2p5_sumPt", [4*i for i in range(41)]],
  [ "mu_m3p1_m2p5_mult", "mu_m3p1_m2p5_mult", [1*i for i in range(21)]],
  [ "ga_m3p1_m2p5_met", "ga_m3p1_m2p5_met", [2*i for i in range(41)]],
  [ "ga_m3p1_m2p5_sumPt", "ga_m3p1_m2p5_sumPt", [4*i for i in range(41)]],
  [ "ga_m3p1_m2p5_mult", "ga_m3p1_m2p5_mult", [3*i for i in range(41)]],
  [ "ch_m3p1_m2p5_met", "ch_m3p1_m2p5_met", [2*i for i in range(41)]],
  [ "ch_m3p1_m2p5_sumPt", "ch_m3p1_m2p5_sumPt", [4*i for i in range(41)]],
  [ "ch_m3p1_m2p5_mult", "ch_m3p1_m2p5_mult", [3*i for i in range(41)]],
  [ "nh_m3p1_m2p5_met", "nh_m3p1_m2p5_met", [2*i for i in range(41)]],
  [ "nh_m3p1_m2p5_sumPt", "nh_m3p1_m2p5_sumPt", [4*i for i in range(41)]],
  [ "nh_m3p1_m2p5_mult", "nh_m3p1_m2p5_mult", [3*i for i in range(41)]],
  [ "all_m3p1_m2p5_met", "all_m3p1_m2p5_met", [20*i for i in range(41)]],
  [ "all_m3p1_m2p5_sumPt", "all_m3p1_m2p5_sumPt", [40*i for i in range(41)]],
  [ "all_m3p1_m2p5_mult", "all_m3p1_m2p5_mult", [30*i for i in range(41)]],
  [ "el_m2p5_m1p5_met", "el_m2p5_m1p5_met", [2*i for i in range(41)]],
  [ "el_m2p5_m1p5_sumPt", "el_m2p5_m1p5_sumPt", [4*i for i in range(41)]],
  [ "el_m2p5_m1p5_mult", "el_m2p5_m1p5_mult", [1*i for i in range(11)]],
  [ "mu_m2p5_m1p5_met", "mu_m2p5_m1p5_met", [2*i for i in range(41)]],
  [ "mu_m2p5_m1p5_sumPt", "mu_m2p5_m1p5_sumPt", [4*i for i in range(41)]],
  [ "mu_m2p5_m1p5_mult", "mu_m2p5_m1p5_mult", [1*i for i in range(21)]],
  [ "ga_m2p5_m1p5_met", "ga_m2p5_m1p5_met", [2*i for i in range(41)]],
  [ "ga_m2p5_m1p5_sumPt", "ga_m2p5_m1p5_sumPt", [4*i for i in range(41)]],
  [ "ga_m2p5_m1p5_mult", "ga_m2p5_m1p5_mult", [3*i for i in range(41)]],
  [ "ch_m2p5_m1p5_met", "ch_m2p5_m1p5_met", [4*i for i in range(41)]],
  [ "ch_m2p5_m1p5_sumPt", "ch_m2p5_m1p5_sumPt", [40*i for i in range(41)]],
  [ "ch_m2p5_m1p5_mult", "ch_m2p5_m1p5_mult", [30*i for i in range(41)]],
  [ "nh_m2p5_m1p5_met", "nh_m2p5_m1p5_met", [2*i for i in range(41)]],
  [ "nh_m2p5_m1p5_sumPt", "nh_m2p5_m1p5_sumPt", [4*i for i in range(41)]],
  [ "nh_m2p5_m1p5_mult", "nh_m2p5_m1p5_mult", [3*i for i in range(41)]],
  [ "all_m2p5_m1p5_met", "all_m2p5_m1p5_met", [20*i for i in range(41)]],
  [ "all_m2p5_m1p5_sumPt", "all_m2p5_m1p5_sumPt", [40*i for i in range(41)]],
  [ "all_m2p5_m1p5_mult", "all_m2p5_m1p5_mult", [30*i for i in range(41)]],
  [ "el_m1p5_1p5_met", "el_m1p5_1p5_met", [2*i for i in range(41)]],
  [ "el_m1p5_1p5_sumPt", "el_m1p5_1p5_sumPt", [4*i for i in range(41)]],
  [ "el_m1p5_1p5_mult", "el_m1p5_1p5_mult", [3*i for i in range(41)]],
  [ "mu_m1p5_1p5_met", "mu_m1p5_1p5_met", [2*i for i in range(41)]],
  [ "mu_m1p5_1p5_sumPt", "mu_m1p5_1p5_sumPt", [4*i for i in range(41)]],
  [ "mu_m1p5_1p5_mult", "mu_m1p5_1p5_mult", [1*i for i in range(21)]],
  [ "ga_m1p5_1p5_met", "ga_m1p5_1p5_met", [4*i for i in range(41)]],
  [ "ga_m1p5_1p5_sumPt", "ga_m1p5_1p5_sumPt", [10*i for i in range(41)]],
  [ "ga_m1p5_1p5_mult", "ga_m1p5_1p5_mult", [10*i for i in range(41)]],
  [ "ch_m1p5_1p5_met", "ch_m1p5_1p5_met", [4*i for i in range(41)]],
  [ "ch_m1p5_1p5_sumPt", "ch_m1p5_1p5_sumPt", [40*i for i in range(41)]],
  [ "ch_m1p5_1p5_mult", "ch_m1p5_1p5_mult", [30*i for i in range(41)]],
  [ "nh_m1p5_1p5_met", "nh_m1p5_1p5_met", [2*i for i in range(41)]],
  [ "nh_m1p5_1p5_sumPt", "nh_m1p5_1p5_sumPt", [4*i for i in range(41)]],
  [ "nh_m1p5_1p5_mult", "nh_m1p5_1p5_mult", [3*i for i in range(41)]],
  [ "all_m1p5_1p5_met", "all_m1p5_1p5_met", [20*i for i in range(41)]],
  [ "all_m1p5_1p5_sumPt", "all_m1p5_1p5_sumPt", [40*i for i in range(41)]],
  [ "all_m1p5_1p5_mult", "all_m1p5_1p5_mult", [30*i for i in range(41)]],
  [ "el_1p5_2p5_met", "el_1p5_2p5_met", [2*i for i in range(41)]],
  [ "el_1p5_2p5_sumPt", "el_1p5_2p5_sumPt", [4*i for i in range(41)]],
  [ "el_1p5_2p5_mult", "el_1p5_2p5_mult", [1*i for i in range(11)]],
  [ "mu_1p5_2p5_met", "mu_1p5_2p5_met", [2*i for i in range(41)]],
  [ "mu_1p5_2p5_sumPt", "mu_1p5_2p5_sumPt", [4*i for i in range(41)]],
  [ "mu_1p5_2p5_mult", "mu_1p5_2p5_mult", [1*i for i in range(21)]],
  [ "ga_1p5_2p5_met", "ga_1p5_2p5_met", [2*i for i in range(41)]],
  [ "ga_1p5_2p5_sumPt", "ga_1p5_2p5_sumPt", [4*i for i in range(41)]],
  [ "ga_1p5_2p5_mult", "ga_1p5_2p5_mult", [3*i for i in range(41)]],
  [ "ch_1p5_2p5_met", "ch_1p5_2p5_met", [4*i for i in range(41)]],
  [ "ch_1p5_2p5_sumPt", "ch_1p5_2p5_sumPt", [40*i for i in range(41)]],
  [ "ch_1p5_2p5_mult", "ch_1p5_2p5_mult", [30*i for i in range(41)]],
  [ "nh_1p5_2p5_met", "nh_1p5_2p5_met", [2*i for i in range(41)]],
  [ "nh_1p5_2p5_sumPt", "nh_1p5_2p5_sumPt", [4*i for i in range(41)]],
  [ "nh_1p5_2p5_mult", "nh_1p5_2p5_mult", [3*i for i in range(41)]],
  [ "all_1p5_2p5_met", "all_1p5_2p5_met", [20*i for i in range(41)]],
  [ "all_1p5_2p5_sumPt", "all_1p5_2p5_sumPt", [40*i for i in range(41)]],
  [ "all_1p5_2p5_mult", "all_1p5_2p5_mult", [30*i for i in range(41)]],
  [ "el_2p5_3p1_met", "el_2p5_3p1_met", [2*i for i in range(41)]],
  [ "el_2p5_3p1_sumPt", "el_2p5_3p1_sumPt", [4*i for i in range(41)]],
  [ "el_2p5_3p1_mult", "el_2p5_3p1_mult", [1*i for i in range(11)]],
  [ "mu_2p5_3p1_met", "mu_2p5_3p1_met", [2*i for i in range(41)]],
  [ "mu_2p5_3p1_sumPt", "mu_2p5_3p1_sumPt", [4*i for i in range(41)]],
  [ "mu_2p5_3p1_mult", "mu_2p5_3p1_mult", [1*i for i in range(21)]],
  [ "ga_2p5_3p1_met", "ga_2p5_3p1_met", [2*i for i in range(41)]],
  [ "ga_2p5_3p1_sumPt", "ga_2p5_3p1_sumPt", [4*i for i in range(41)]],
  [ "ga_2p5_3p1_mult", "ga_2p5_3p1_mult", [3*i for i in range(41)]],
  [ "ch_2p5_3p1_met", "ch_2p5_3p1_met", [2*i for i in range(41)]],
  [ "ch_2p5_3p1_sumPt", "ch_2p5_3p1_sumPt", [4*i for i in range(41)]],
  [ "ch_2p5_3p1_mult", "ch_2p5_3p1_mult", [3*i for i in range(41)]],
  [ "nh_2p5_3p1_met", "nh_2p5_3p1_met", [2*i for i in range(41)]],
  [ "nh_2p5_3p1_sumPt", "nh_2p5_3p1_sumPt", [4*i for i in range(41)]],
  [ "nh_2p5_3p1_mult", "nh_2p5_3p1_mult", [3*i for i in range(41)]],
  [ "all_2p5_3p1_met", "all_2p5_3p1_met", [20*i for i in range(41)]],
  [ "all_2p5_3p1_sumPt", "all_2p5_3p1_sumPt", [40*i for i in range(41)]],
  [ "all_2p5_3p1_mult", "all_2p5_3p1_mult", [30*i for i in range(41)]],
  [ "HFh_3p1_5p1_met", "HFh_3p1_5p1_met", [4*i for i in range(41)]],
  [ "HFh_3p1_5p1_sumPt", "HFh_3p1_5p1_sumPt", [16*i for i in range(41)]],
  [ "HFh_3p1_5p1_mult", "HFh_3p1_5p1_mult", [12*i for i in range(41)]],
  [ "HFe_3p1_5p1_met", "HFe_3p1_5p1_met", [2*i for i in range(41)]],
  [ "HFe_3p1_5p1_sumPt", "HFe_3p1_5p1_sumPt", [4*i for i in range(41)]],
  [ "HFe_3p1_5p1_mult", "HFe_3p1_5p1_mult", [6*i for i in range(41)]],
  [ "all_3p1_5p1_met", "all_3p1_5p1_met", [20*i for i in range(41)]],
  [ "all_3p1_5p1_sumPt", "all_3p1_5p1_sumPt", [40*i for i in range(41)]],
  [ "all_3p1_5p1_mult", "all_3p1_5p1_mult", [30*i for i in range(41)]],
  [ "el_all_met", "el_all_met", [2*i for i in range(41)]],
  [ "el_all_sumPt", "el_all_sumPt", [4*i for i in range(41)]],
  [ "el_all_mult", "el_all_mult", [1*i for i in range(11)]],
  [ "mu_all_met", "mu_all_met", [2*i for i in range(41)]],
  [ "mu_all_sumPt", "mu_all_sumPt", [4*i for i in range(41)]],
  [ "mu_all_mult", "mu_all_mult", [1*i for i in range(21)]],
  [ "ga_all_met", "ga_all_met", [2*i for i in range(41)]],
  [ "ga_all_sumPt", "ga_all_sumPt", [4*i for i in range(41)]],
  [ "ga_all_mult", "ga_all_mult", [3*i for i in range(41)]],
  [ "ch_all_met", "ch_all_met", [4*i for i in range(41)]],
  [ "ch_all_sumPt", "ch_all_sumPt", [40*i for i in range(41)]],
  [ "ch_all_mult", "ch_all_mult", [30*i for i in range(41)]],
  [ "nh_all_met", "nh_all_met", [2*i for i in range(41)]],
  [ "nh_all_sumPt", "nh_all_sumPt", [4*i for i in range(41)]],
  [ "nh_all_mult", "nh_all_mult", [3*i for i in range(41)]],
  [ "HFh_all_met", "HFh_all_met", [2*i for i in range(41)]],
  [ "HFh_all_sumPt", "HFh_all_sumPt", [4*i for i in range(41)]],
  [ "HFh_all_mult", "HFh_all_mult", [3*i for i in range(41)]],
  [ "HFe_all_met", "HFe_all_met", [2*i for i in range(41)]],
  [ "HFe_all_sumPt", "HFe_all_sumPt", [4*i for i in range(41)]],
  [ "HFe_all_mult", "HFe_all_mult", [6*i for i in range(41)]],
  [ "all_all_met", "all_all_met", [20*i for i in range(41)]],
  [ "all_all_sumPt", "all_all_sumPt", [40*i for i in range(41)]],
  [ "all_all_mult", "all_all_mult", [30*i for i in range(41)]],
]


#selectionString = "met_pt>150"
selectionString = "nVert>40"
sample = dm_2018
#dy_2018.reduceFiles( to = 1 )
prefix = sample.name
#profile = ROOT.TProfile("response", "response", len(pt_thresholds)-1, array.array('d', pt_thresholds) )
for i_var, ( name1, expr1, thresholds1) in enumerate(variables[:1]):
    for name2, expr2, thresholds2 in variables[i_var+1:]:
        h_2D = sample.get2DHistoFromDraw( expr2+":"+expr1, [ thresholds1, thresholds2], selectionString = selectionString, binningIsExplicit = True ) 

        plotting.draw2D(
            plot = Plot2D.fromHisto(name = "%s_%s"%( name1, name2), histos = [[h_2D]], texX = name1, texY = name2),
            plot_directory = "/afs/hephy.at/user/r/rschoefbeck/www/JetMET/PU2018_2_nVert40/"+sample.name,
            logX = False, logY = False, logZ = True, copyIndexPHP = True,
        )
