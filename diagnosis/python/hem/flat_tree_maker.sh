#!/bin/sh
python flat_tree_maker.py --overwrite --sample  /DoubleMuon/Run2018C-17Sep2018-v1/MINIAOD  #SPLIT300
python flat_tree_maker.py --overwrite --sample  /DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM #SPLIT300

#python flat_tree_maker.py --overwrite  --sample /DoubleMuon/CMSSW_10_4_0_patch1-104X_dataRun2_Candv1_L1JEC_offset_RelVal_doubMu2018D-v1/MINIAOD #SPLIT11
#python flat_tree_maker.py --overwrite  --sample /DoubleMuon/CMSSW_10_4_0_patch1-104X_dataRun2_Candv1_L1JEC_offset_RelVal_doubMu2018B-v1/MINIAOD #SPLIT14
#python flat_tree_maker.py --overwrite  --sample  /DoubleMuon/CMSSW_10_4_0-103X_dataRun2_PromptLike_v6_RelVal_doubMu2018D-v1/MINIAOD  #SPLIT4
