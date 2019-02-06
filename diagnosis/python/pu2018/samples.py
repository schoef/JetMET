# RootTools
from RootTools.core.standard import *

# standard imports
import os

directory = "/afs/hephy.at/data/rschoefbeck02/postProcessed/flat_jet_trees/v4/"

dy_2018 = Sample.fromDirectory( "DY",         os.path.join( directory, "DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM" ) )
dm_2018 = Sample.fromDirectory( "DoubleMuon", os.path.join( directory, "DoubleMuon_Run2018C-17Sep2018-v1_MINIAOD" ), isData = True)
