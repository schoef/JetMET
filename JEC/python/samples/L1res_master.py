import os

#Hard coded EOS location
L1res_master_directory = "/eos/cms/store/group/phys_jetmet/schoef/L1res/"

# RootTools
from RootTools.core.standard import *

# Logging
import logging
logger = logging.getLogger(__name__)

# MC
SingleNeutrino       =  Sample.fromCMGOutput( "SingleNeutrino",       L1res_master_directory, chunkString="SingleNeutrino" )

# Data

ZeroBias_Run2016B =     Sample.fromCMGOutput( "ZeroBias_Run2016B",    L1res_master_directory, chunkString="ZeroBias_Run2016B-03Feb2017_ver2-v2" )
ZeroBias_Run2016C =     Sample.fromCMGOutput( "ZeroBias_Run2016C",    L1res_master_directory, chunkString="ZeroBias_Run2016C-03Feb2017-v1" )
ZeroBias_Run2016D =     Sample.fromCMGOutput( "ZeroBias_Run2016D",    L1res_master_directory, chunkString="ZeroBias_Run2016D-03Feb2017-v1" )
ZeroBias_Run2016E =     Sample.fromCMGOutput( "ZeroBias_Run2016E",    L1res_master_directory, chunkString="ZeroBias_Run2016E-03Feb2017-v1" )
ZeroBias_Run2016F =     Sample.fromCMGOutput( "ZeroBias_Run2016F",    L1res_master_directory, chunkString="ZeroBias_Run2016F-03Feb2017-v1" )
ZeroBias_Run2016G =     Sample.fromCMGOutput( "ZeroBias_Run2016G",    L1res_master_directory, chunkString="ZeroBias_Run2016G-03Feb2017-v1" )
ZeroBias_Run2016H_v2 =  Sample.fromCMGOutput( "ZeroBias_Run2016H_v2", L1res_master_directory, chunkString="ZeroBias_Run2016H-03Feb2017_ver2-v1" )
ZeroBias_Run2016H_v3 =  Sample.fromCMGOutput( "ZeroBias_Run2016H_v3", L1res_master_directory, chunkString="ZeroBias_Run2016H-03Feb2017_ver3-v1" )

# combinations
ZeroBias_Run2016BCD     = Sample.combine("ZeroBias_Run2016BCD", [ZeroBias_Run2016B, ZeroBias_Run2016C, ZeroBias_Run2016D])
ZeroBias_Run2016EFearly = Sample.combine("ZeroBias_Run2016EFearly", [ZeroBias_Run2016E, ZeroBias_Run2016F])
ZeroBias_Run2016EFearly.setSelectionString("run<=278801")
ZeroBias_Run2016Fearly  = Sample.combine("ZeroBias_Run2016Fearly", [ ZeroBias_Run2016F])
ZeroBias_Run2016Fearly.setSelectionString("run<=278801")
ZeroBias_Run2016Flate   = Sample.combine("ZeroBias_Run2016Flate",  [ ZeroBias_Run2016F])
ZeroBias_Run2016Flate.setSelectionString("run>=278802")
ZeroBias_Run2016FlateG  = Sample.combine("ZeroBias_Run2016FlateG", [ZeroBias_Run2016F, ZeroBias_Run2016G])
ZeroBias_Run2016FlateG.setSelectionString("run>=278802")
ZeroBias_Run2016H       = Sample.combine("ZeroBias_Run2016H", [ZeroBias_Run2016H_v2, ZeroBias_Run2016H_v3])
ZeroBias_Run2016        = Sample.combine("ZeroBias_Run2016", [ZeroBias_Run2016B, ZeroBias_Run2016C, ZeroBias_Run2016D, ZeroBias_Run2016E, ZeroBias_Run2016F, ZeroBias_Run2016G, ZeroBias_Run2016H_v2, ZeroBias_Run2016H_v3] )
