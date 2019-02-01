''' Samples for EE test
'''

#Standard imports
import os

# RootTools
from RootTools.core.standard import *

# JetMET
from JetMET.tools.user import skim_ntuple_directory

# samples
skim_directory = os.path.join( skim_ntuple_directory, "flat_jet_trees/v3")

ref_noPU      = Sample.fromDirectory("ref", texName = "ref_noPU", treeName = "jets", directory = os.path.join( skim_directory, "QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8_RunIIFall17MiniAODv2-NoPU_12Apr2018_94X_mc2017_realistic_v14-v1_MINIAODSIM"))
ref           = Sample.fromDirectory("ref", texName = "ref", treeName = "jets", directory = os.path.join( skim_directory, "QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_MINIAODSIM"))

QCD_flat_AB_v01        = Sample.fromDirectory("QCD_flat_AB_v01",        texName = "AB",   treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13_CMSSW_10_4_0_pre2-PU25ns_103X_mc2017_realistic_v2_AB_v01_HS_rsb-v1_MINIAODSIM"))
QCD_flat_AC_v01        = Sample.fromDirectory("QCD_flat_AC_v01",        texName = "1#sigma",   treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13_CMSSW_10_4_0_pre2-PU25ns_103X_mc2017_realistic_v2_AC_v01_HS-v1_MINIAODSIM"))
QCD_flat_AC_2sigma_v01 = Sample.fromDirectory("QCD_flat_AC_2sigma_v01", texName = "2#sigma", treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13_CMSSW_10_4_0_pre2-PU25ns_103X_mc2017_realistic_v2_AC_2sigma_v01_HS-v1_MINIAODSIM"))
QCD_flat_AC_3sigma_v01 = Sample.fromDirectory("QCD_flat_AC_3sigma_v01", texName = "3#sigma", treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13_CMSSW_10_4_0_pre2-PU25ns_103X_mc2017_realistic_v2_AC_3sigma_v01_HS-v1_MINIAODSIM"))
QCD_flat_AC_4sigma_v01 = Sample.fromDirectory("QCD_flat_AC_4sigma_v01", texName = "4#sigma", treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13_CMSSW_10_4_0_pre2-PU25ns_103X_mc2017_realistic_v2_AC_4sigma_v01_HS-v1_MINIAODSIM"))

QCD_flat_noPU_AB_v01        = Sample.fromDirectory("QCD_flat_noPU_AB_v01",        texName = "AB",   treeName = "jets", directory = os.path.join( skim_directory,      "RelValQCD_FlatPt_15_3000HS_13_CMSSW_10_4_0_pre2-103X_mc2017_realistic_v2_AB_v01_HS-v1_MINIAODSIM"))
QCD_flat_noPU_AC_v01        = Sample.fromDirectory("QCD_flat_noPU_AC_v01",        texName = "1#sigma",   treeName = "jets", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13_CMSSW_10_4_0_pre2-103X_mc2017_realistic_v2_AC_v01_HS-v1_MINIAODSIM"))
QCD_flat_noPU_AC_2sigma_v01 = Sample.fromDirectory("QCD_flat_noPU_AC_2sigma_v01", texName = "2#sigma", treeName = "jets", directory = os.path.join( skim_directory,   "RelValQCD_FlatPt_15_3000HS_13_CMSSW_10_4_0_pre2-103X_mc2017_realistic_v2_AC_2sigma_v01_HS_rsb-v1_MINIAODSIM"))
QCD_flat_noPU_AC_3sigma_v01 = Sample.fromDirectory("QCD_flat_noPU_AC_3sigma_v01", texName = "3#sigma", treeName = "jets", directory = os.path.join( skim_directory,   "RelValQCD_FlatPt_15_3000HS_13_CMSSW_10_4_0_pre2-103X_mc2017_realistic_v2_AC_3sigma_v01_HS_rsb-v1_MINIAODSIM"))
QCD_flat_noPU_AC_4sigma_v01 = Sample.fromDirectory("QCD_flat_noPU_AC_4sigma_v01", texName = "4#sigma", treeName = "jets", directory = os.path.join( skim_directory,   "RelValQCD_FlatPt_15_3000HS_13_CMSSW_10_4_0_pre2-103X_mc2017_realistic_v2_AC_4sigma_v01_HS_rsb-v1_MINIAODSIM"))

