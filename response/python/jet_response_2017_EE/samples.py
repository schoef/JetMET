''' Samples for EE test
'''

#Standard imports
import os

# RootTools
from RootTools.core.standard import *

# JetMET
from JetMET.tools.user import skim_ntuple_directory

# samples
skim_directory = os.path.join( skim_ntuple_directory, "flat_jet_trees/v1")

QCD_flat_Summer16_NoPU                  = Sample.fromDirectory("QCD_flat_Summer16_NoPU",                texName = "Summer16 noPU", treeName = "jets", directory = os.path.join( skim_directory, "QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8_RunIISummer16MiniAODv2-NoPU_magnetOn_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1_MINIAODSIM"))
QCD_flat_Summer16_PUMoriond17           = Sample.fromDirectory("QCD_flat_Summer16_PUMoriond17",         texName = "Summer16 PU", treeName = "jets", directory = os.path.join( skim_directory, "QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8_RunIISummer16MiniAODv2-PUMoriond17_magnetOn_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1_MINIAODSIM"))

merged_RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9 = Sample.fromDirectory("merged_RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9", treeName = "jets", directory = os.path.join( skim_directory, "merged_RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9")) 

skim_directory = os.path.join( skim_ntuple_directory, "flat_jet_trees/v3")

RelVal_QCD_flat_GTv1_SRPFoff_NoPU       = Sample.fromDirectory("RelVal_QCD_flat_GTv1_SRPFoff_NoPU",     texName = "GTv1 SR@PF off NoPU", treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9-92X_upgrade2017_realistic_v10_HS1M_PF16-v1_MINIAODSIM"))
RelVal_QCD_flat_GTv1_SRPFoff_PUpmx25ns  = Sample.fromDirectory("RelVal_QCD_flat_GTv1_SRPFoff_PUpmx25ns",texName = "GTv1 SR@PF off PU", treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_v10_HS1M_PF16-v1_MINIAODSIM"))

RelVal_QCD_flat_GTv2_SRPFoff_NoPU       = Sample.fromDirectory("RelVal_QCD_flat_GTv2_SRPFoff_NoPU",     texName = "SR@PF off NoPU", treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9-92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF16-v1_MINIAODSIM"))
RelVal_QCD_flat_GTv2_SRPFoff_PUpmx25ns  = Sample.fromDirectory("RelVal_QCD_flat_GTv2_SRPFoff_PUpmx25ns",texName = "SR@PF off PU", treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF16-v1_MINIAODSIM"))

RelVal_QCD_flat_GTv2_SRPFon_NoPU        = Sample.fromDirectory("RelVal_QCD_flat_GTv2_SRPFon_NoPU",      texName = "SR@PF on NoPU", treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9-92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF17-v1_MINIAODSIM"))
RelVal_QCD_flat_GTv2_SRPFon_PUpmx25ns   = Sample.fromDirectory("RelVal_QCD_flat_GTv2_SRPFon_PUpmx25ns", texName = "SR@PF on PU", treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF17-v1_MINIAODSIM"))


RelVal_QCD_flat_GTv2_SRPFoff_NoPU_ZeroN      = Sample.fromDirectory("RelVal_QCD_flat_GTv2_SRPFoff_noPU_ZeroN",      texName="SR@PF off NoPU ZN", treeName = "jets", directory = os.path.join( skim_directory, 'RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9-92X_upgrade2017_realistic_forECALStudies_ZeroN_HS1M_PF16-v1_MINIAODSIM'))
RelVal_QCD_flat_GTv2_SRPFoff_PUpmx25ns_ZeroN = Sample.fromDirectory("RelVal_QCD_flat_GTv2_SRPFoff_PUpmx25ns_ZeroN", texName="SR@PF off PU ZN", treeName = "jets", directory = os.path.join( skim_directory, 'RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_forECALStudies_ZeroN_HS1M_PF16-v2_MINIAODSIM'))
RelVal_QCD_flat_GTv2_SRPFon_PUpmx25ns_ZeroN  = Sample.fromDirectory("RelVal_QCD_flat_GTv2_SRPFon_PUpmx25ns_ZeroN",  texName="SR@PF on PU ZN", treeName = "jets", directory = os.path.join( skim_directory, 'RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_forECALStudies_ZeroN_HS1M_PF17-v1_MINIAODSIM'))


#skim_directory = os.path.join( skim_ntuple_directory, "flat_jet_trees/v1_small")
#
#RelVal_QCD_flat_GTv1_SRPFoff_NoPU       = Sample.fromDirectory("RelVal_QCD_flat_GTv1_SRPFoff_NoPU",     texName = "GTv1 SR@PF off NoPU", treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9-92X_upgrade2017_realistic_v10_HS1M_PF16-v1_MINIAODSIM"))
#RelVal_QCD_flat_GTv1_SRPFoff_PUpmx25ns  = Sample.fromDirectory("RelVal_QCD_flat_GTv1_SRPFoff_PUpmx25ns",texName = "GTv1 SR@PF off PU", treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_v10_HS1M_PF16-v1_MINIAODSIM"))
#
#RelVal_QCD_flat_GTv2_SRPFoff_NoPU       = Sample.fromDirectory("RelVal_QCD_flat_GTv2_SRPFoff_NoPU",     texName = "GTv2 SR@PF off NoPU", treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9-92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF16-v1_MINIAODSIM"))
#RelVal_QCD_flat_GTv2_SRPFoff_PUpmx25ns  = Sample.fromDirectory("RelVal_QCD_flat_GTv2_SRPFoff_PUpmx25ns",texName = "GTv2 SR@PF off PU", treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF16-v1_MINIAODSIM"))
#
#RelVal_QCD_flat_GTv2_SRPFon_NoPU        = Sample.fromDirectory("RelVal_QCD_flat_GTv2_SRPFon_NoPU",      texName = "GTv2 SR@PF on NoPU", treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9-92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF17-v1_MINIAODSIM"))
#RelVal_QCD_flat_GTv2_SRPFon_PUpmx25ns   = Sample.fromDirectory("RelVal_QCD_flat_GTv2_SRPFon_PUpmx25ns", texName = "GTv2 SR@PF on PU", treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF17-v1_MINIAODSIM"))
