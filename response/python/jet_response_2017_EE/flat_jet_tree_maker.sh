#!/bin/sh

## Relval
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13/CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies_HS_PF16-v1/MINIAODSIM

##10M, Moriond 17 (Summer 16), PU
#python flat_jet_tree_maker.py --overwrite --sample /QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_magnetOn_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM
##10M, Moriond 17 (Summer 16), no PU
##python flat_jet_tree_maker.py --overwrite --sample /QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIISummer16MiniAODv2-NoPU_magnetOn_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM
##1M, v2 GT and SR@PF on, noPU
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF17-v1/MINIAODSIM
##1M, v2 GT and SR@PF on, PU
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF17-v1/MINIAODSIM
##
###1M, v1 GT and SR@PF off, no PU
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-92X_upgrade2017_realistic_v10_HS1M_PF16-v1/MINIAODSIM
###1M, v1 GT and SR@PF off,PU
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_v10_HS1M_PF16-v1/MINIAODSIM
###1M, v2 GT and SR@PF off, no PU
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF16-v1/MINIAODSIM
##1M, v2 GT and SR@PF off,PU
#python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF16-v1/MINIAODSIM

# 0 noise

# v2 GT, SR@PF off, no PU, ZeroN
python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-92X_upgrade2017_realistic_forECALStudies_rms0p2887_HS1M_PF16-v1/MINIAODSIM
 
# v2 GT, SR@PF off, PU, ZeroN
##python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_forECALStudies_ZeroN_HS1M_PF16-v2/MINIAODSIM
# v2 GT, SR@PF on, PU, ZeroN
python flat_jet_tree_maker.py --overwrite --sample /RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_forECALStudies_rms0p2887_HS1M_PF17-v1/MINIAODSIM 

#python flat_jet_tree_maker.py --overwrite --sample /RelValNuGun_UP17/CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_forECALStudies_ZeroN_HS1M_PF16-v1/MINIAODSIM
