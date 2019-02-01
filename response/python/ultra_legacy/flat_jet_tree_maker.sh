#!/bin/sh

# noPU
python flat_jet_tree_maker.py --overwrite --maxFiles 10 --maxEvents 1000000 --sample /QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/RunIIFall17MiniAODv2-NoPU_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13/CMSSW_10_4_0_pre3-103X_mc2017_realistic_v2-v1/MINIAODSIM
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13/CMSSW_10_4_0_pre2-103X_mc2017_realistic_v2_AB_v01_HS-v1/MINIAODSIM
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13/CMSSW_10_4_0_pre2-103X_mc2017_realistic_v2_AC_v01_HS-v1/MINIAODSIM
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13/CMSSW_10_4_0_pre2-103X_mc2017_realistic_v2_AC_2sigma_v01_HS_rsb-v1/MINIAODSIM
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13/CMSSW_10_4_0_pre2-103X_mc2017_realistic_v2_AC_3sigma_v01_HS_rsb-v1/MINIAODSIM
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13/CMSSW_10_4_0_pre2-103X_mc2017_realistic_v2_AC_4sigma_v01_HS_rsb-v1/MINIAODSIM

# PU
python flat_jet_tree_maker.py --overwrite --maxFiles 10 --maxEvents 1000000 --sample /QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13/CMSSW_10_4_0_pre3-PU25ns_103X_mc2017_realistic_v2-v1/MINIAODSIM 
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13/CMSSW_10_4_0_pre2-PU25ns_103X_mc2017_realistic_v2_AB_v01_HS_rsb-v1/MINIAODSIM
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13/CMSSW_10_4_0_pre2-PU25ns_103X_mc2017_realistic_v2_AC_v01_HS-v1/MINIAODSIM
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13/CMSSW_10_4_0_pre2-PU25ns_103X_mc2017_realistic_v2_AC_2sigma_v01_HS-v1/MINIAODSIM
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13/CMSSW_10_4_0_pre2-PU25ns_103X_mc2017_realistic_v2_AC_3sigma_v01_HS-v1/MINIAODSIM
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13/CMSSW_10_4_0_pre2-PU25ns_103X_mc2017_realistic_v2_AC_4sigma_v01_HS-v1/MINIAODSIM
