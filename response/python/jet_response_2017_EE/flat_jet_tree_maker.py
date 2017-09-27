#!/usr/bin/env python
''' Analysis script for gen plots
'''
#
# Standard imports and batch mode
#
import ROOT, os
ROOT.gROOT.SetBatch(True)
import itertools
from math                                import sqrt, cos, sin, pi, acos
import imp

#RootTools
from RootTools.core.standard             import *

#JetMET
from JetMET.tools.user                   import skim_ntuple_directory
from JetMET.tools.helpers                import deltaR2, jetID, vertexID

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--small',              action='store_true', help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--maxEvents',          action='store',      type=int, default=-1, help='Maximum number of events')
argParser.add_argument('--maxFiles',           action='store',      type=int, default=-1, help='Maximum number of files')
argParser.add_argument('--overwrite',          action='store_true', help='overwrite?')#, default = True)
argParser.add_argument('--targetDir',          action='store',      default='flat_jet_trees/v1')
argParser.add_argument('--sample',             action='store',      default='/RelValNuGun/CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies-v1/MINIAODSIM')
args = argParser.parse_args()
 
#
# Logger
#
import JetMET.tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

if args.small: 
    args.targetDir += "_small"

sample_name = args.sample.lstrip('/').replace('/','_')
if args.small:
    maxN = 1
elif args.maxFiles>0:
    maxN = args.maxFiles
else:
    maxN = -1 

sample = FWLiteSample.fromDAS( sample_name, args.sample, maxN = maxN ) 

if args.maxFiles > 0:
    sample.files = sample.files[:args.maxFiles]

output_directory = os.path.join(skim_ntuple_directory, args.targetDir, sample.name) 
output_filename =  os.path.join(output_directory, sample.name + '.root') 
if not os.path.exists( output_directory ): 
    os.makedirs( output_directory )
    logger.info( "Created output directory %s", output_directory )

products = {
#    'gp':{'type':'vector<reco::GenParticle>', 'label':("genParticles")},
#    'jets':{'type':'vector<reco::GenJet>', 'label':("ak4GenJets")},
#    'genMET':{'type':'vector<reco::GenMET>', 'label':("genMetTrue")},
     'jets': {'type':'vector<pat::Jet>', 'label': ("slimmedJets")},
     'vertices':{'type':'vector<reco::Vertex>', 'label':('offlineSlimmedPrimaryVertices')},
}

reader = sample.fwliteReader( products = products )

new_variables =  [ "evt/l", "run/I", "lumi/I", "nVert/I" ] 
new_variables += [ "genPt/F", "genEta/F", "genPhi/F", "rawPt/F", "eta/F", "phi/F", "chHEF/F", "neHEF/F", "phEF/F", "eEF/F", "muEF/F", "HFHEF/F", "HFEMEF/F" ]

if not os.path.exists( output_filename ) or args.overwrite:
    # Maker
    tmp_dir     = ROOT.gDirectory
    output_file = ROOT.TFile( output_filename, 'recreate')
    output_file.cd()
    maker =    TreeMaker( sequence = [], variables = map( TreeVariable.fromString, new_variables ), treeName = "jets")
    tmp_dir.cd()
else:
    raise IOError( "File %s exists!" % output_filename )

# Filler for data struct of maker
def jet_filler(struct, jet):

    gen_jet = jet.genJet()

    struct.genPt  =  gen_jet.pt()  if gen_jet else float('nan')
    struct.genEta =  gen_jet.eta() if gen_jet else float('nan')
    struct.genPhi =  gen_jet.phi() if gen_jet else float('nan')
    struct.rawPt  =  jet.correctedJet("Uncorrected").pt()
    for name, func in [
        ("eta",   "eta"),
        ("phi",   "phi"),
        ("chHEF", "chargedHadronEnergyFraction"),
        ("neHEF", "neutralHadronEnergyFraction"),
        ("phEF",  "photonEnergyFraction"),
        ("eEF",   "electronEnergyFraction"),
        ("muEF",  "muonEnergyFraction"),
        ("HFHEF", "HFHadronEnergyFraction"),
        ("HFEMEF","HFEMEnergyFraction"),
        ]:
            setattr(struct, name, getattr(jet, func)() )
    return

reader.start()
maker.start()

counter = -1 

while reader.run():
    counter += 1
    if args.maxEvents>0 and counter>=args.maxEvents: break

    if counter%100==0: logger.info("At event %i.", counter)

    jets      = filter( jetID, reader.products['jets'] )
    vertices  = filter( vertexID, reader.products['vertices'] )

    for jet in jets:
        # convinience
        jet_out = maker.event 
        # run, lumi, event
        jet_out.run, jet_out.lumi, jet_out.evt = reader.evt
        # nvert
        jet_out.nVert = len(vertices)
        # jet quantities
        jet_filler( jet_out, jet )
        # fill ntuple
        maker.run()        

output_file.cd()
maker.tree.Write()
output_file.Close()

logger.info( "Written file %s", output_filename)
