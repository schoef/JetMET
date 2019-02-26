# RootTools
from RootTools.core.standard import *

# standard imports
import os

directory = "/afs/hephy.at/data/rschoefbeck02/postProcessed/flat_jet_trees/v4/"

dy_2018 = Sample.fromDirectory( "DY",         os.path.join( directory, "DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM" ) )
dm_2018 = Sample.fromDirectory( "DoubleMuon", os.path.join( directory, "DoubleMuon_Run2018C-17Sep2018-v1_MINIAOD" ), isData = True)

#RelVal_DoubleMuon_Run2018B = Sample.fromDirectory( "RelVal_DoubleMuon_Run2018B", os.path.join( directory, "DoubleMuon_CMSSW_10_4_0_patch1-104X_dataRun2_Candv1_L1JEC_offset_RelVal_doubMu2018B-v1_MINIAOD" ) )
#RelVal_DoubleMuon_Run2018D = Sample.fromDirectory( "RelVal_DoubleMuon_Run2018D", os.path.join( directory, "DoubleMuon_CMSSW_10_4_0_patch1-104X_dataRun2_Candv1_L1JEC_offset_RelVal_doubMu2018D-v1_MINIAOD" ) )
#RelVal_DoubleMuon_Run2018D_Ref = Sample.fromDirectory( "RelVal_DoubleMuon_Run2018D_Ref", os.path.join( directory, "DoubleMuon_CMSSW_10_4_0-103X_dataRun2_PromptLike_v6_RelVal_doubMu2018D-v1_MINIAOD" ) )

