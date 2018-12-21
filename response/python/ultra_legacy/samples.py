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

QCD_flat_AB_v01        = Sample.fromDirectory("QCD_flat_AB_v01",        texName = "AB",   directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13_CMSSW_10_4_0_pre2-PU25ns_103X_mc2017_realistic_v2_AB_v01_HS_rsb-v1_MINIAODSIM"))
QCD_flat_AC_v01        = Sample.fromDirectory("QCD_flat_AC_v01",        texName = "AC",   directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13_CMSSW_10_4_0_pre2-PU25ns_103X_mc2017_realistic_v2_AC_v01_HS-v1_MINIAODSIM"))
QCD_flat_AC_2sigma_v01 = Sample.fromDirectory("QCD_flat_AC_2sigma_v01", texName = "AC_2", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13_CMSSW_10_4_0_pre2-PU25ns_103X_mc2017_realistic_v2_AC_2sigma_v01_HS-v1_MINIAODSIM"))
QCD_flat_AC_3sigma_v01 = Sample.fromDirectory("QCD_flat_AC_3sigma_v01", texName = "AC_3", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13_CMSSW_10_4_0_pre2-PU25ns_103X_mc2017_realistic_v2_AC_3sigma_v01_HS-v1_MINIAODSIM"))
QCD_flat_AC_4sigma_v01 = Sample.fromDirectory("QCD_flat_AC_4sigma_v01", texName = "AC_4", directory = os.path.join( skim_directory, "RelValQCD_FlatPt_15_3000HS_13_CMSSW_10_4_0_pre2-PU25ns_103X_mc2017_realistic_v2_AC_4sigma_v01_HS-v1_MINIAODSIM"))
