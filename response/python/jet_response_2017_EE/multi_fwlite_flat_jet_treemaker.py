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
from JetMET.tools.user                   import skim_ntuple_directory, cache_directory
from JetMET.tools.helpers                import deltaR2, jetID, vertexID

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='DEBUG',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--small',              action='store_true', help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--maxEvents',          action='store',      type=int, default=-1, help='Maximum number of events')
argParser.add_argument('--maxFiles',           action='store',      type=int, default=-1, help='Maximum number of files')
argParser.add_argument('--overwrite',          action='store_true', help='overwrite?')#, default = True)
argParser.add_argument('--targetDir',          action='store',      default='flat_jet_trees/v1')
args = argParser.parse_args()

if args.small:
    maxN = 1
elif args.maxFiles>0:
    maxN = args.maxFiles
else:
    maxN = -1 
 
#
# Logger
#
import JetMET.tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

if args.small: 
    args.targetDir += "_small"

output_directory = os.path.join(skim_ntuple_directory, args.targetDir, "ECAL_merged") 
output_filename =  os.path.join(output_directory, 'jets.root') 
if not os.path.exists( output_directory ): 
    os.makedirs( output_directory )
    logger.info( "Created output directory %s", output_directory )

samples = [ { 'prefix':name, 'fwlite':FWLiteSample.fromDAS( name, dataset, dbFile = os.path.join( cache_directory, 'fwlite_cache.db' )) } for name, dataset in \
  [
    ( "GTv2_SRPFon_noPU",       "/RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF17-v1/MINIAODSIM" ),
    ( "GTv2_SRPFon_PUpmx25ns",  "/RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF17-v1/MINIAODSIM" ),
    ( "GTv1_SRPFoff_noPU",      "/RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-92X_upgrade2017_realistic_v10_HS1M_PF16-v1/MINIAODSIM" ),
    ( "GTv1_SRPFoff_PUpmx25ns", "/RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_v10_HS1M_PF16-v1/MINIAODSIM" ),
    ( "GTv2_SRPFoff_noPU",      "/RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF16-v1/MINIAODSIM" ),
    ( "GTv2_SRPFoff_PUpmx25ns", "/RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF16-v1/MINIAODSIM" ),
 ] ]

products = {
#    'gp':{'type':'vector<reco::GenParticle>', 'label':("genParticles")},
#    'jets':{'type':'vector<reco::GenJet>', 'label':("ak4GenJets")},
#    'genMET':{'type':'vector<reco::GenMET>', 'label':("genMetTrue")},
     'jets': {'type':'vector<pat::Jet>', 'label': ("slimmedJets")},
     'vertices':{'type':'vector<reco::Vertex>', 'label':('offlineSlimmedPrimaryVertices')},
}


for sample in samples:
    before = len( sample['fwlite'].files )
    sample['fwlite'].files = sample['fwlite'].files[:maxN]
    if maxN > 0: logger.info( "Reduce number of files from %i to %i", before, len( sample['fwlite'].files ) )

    # Make fwlite reader
    sample['reader'] = sample['fwlite'].fwliteReader( products = products )

default_key = lambda event: ( event.run, event.lumi, event.evt )
reader = MultiReader( *[ (sample['reader'], default_key) for sample in samples ] )

variables_firstsample =  [ "evt/l", "run/I", "lumi/I" ]
variables_persample   =  [ "nVert/I" ] 
variables_perjet      =  [ "genPt/F", "rawPt/F", "eta/F", "phi/F", "chHEF/F", "neHEF/F", "phEF/F", "eEF/F", "muEF/F", "HFHEF/F", "HFEMEF/F" ]

variables = variables_firstsample + sum( [[ sample['prefix']+'_'+var for var in variables_persample + variables_perjet] for sample in samples ], [] )

if not os.path.exists( output_filename ) or args.overwrite:
    # Maker
    tmp_dir     = ROOT.gDirectory
    output_file = ROOT.TFile( output_filename, 'recreate')
    output_file.cd()
    maker =    TreeMaker( sequence = [], variables = map( TreeVariable.fromString, variables ), treeName = "jets")
    tmp_dir.cd()
else:
    raise IOError( "File %s exists!" % output_filename )

def get_jet_dict(jet):
    ''' Get jet dict from slimmedJet
    '''

    jet_dict = {}
    jet_dict['genPt'] = jet.genJet().pt() if jet.genJet() else None

    jet_dict['rawPt'] =  jet.correctedJet("Uncorrected").pt()
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
            jet_dict[name] = getattr(jet, func)()

    return jet_dict

reader.start()
maker.start()

counter = -1 

key = lambda jet: jet['genPt']

def intersect_keys( new_jets, intersected_keys = None):

    new_jet_keys = set({key(j) for j in new_jets if key(j)})
    if intersected_keys is None: 
        return new_jet_keys
    else: 
        return intersected_keys.intersection(new_jet_keys)
        
jet_vars = None
while reader.run():
    counter += 1
    if args.maxEvents>0 and counter>=args.maxEvents: break

    if counter%100==0: logger.info("At event %i.", counter)

    first_reader = reader.readers[0]

    # Get jets (keep track of those keys which appear in each event)
    jet_keys = None
    jets = {}
    for r in reader.readers:
        jets_ = map( get_jet_dict, filter( jetID, r.event.jets ) )
        jet_keys = intersect_keys( jets_, jet_keys) 

        if len(jets_)>0 and jet_vars is None: 
            jet_vars = jets_[0].keys()

        jets[r.sample.name] = {key(j):j for j in jets_ }

    # copy evt info
    jet_keys = list(jet_keys)
    jet_keys.sort()
   
    for jet_key in reversed(jet_keys): 
        # convinience
        jet_out = maker.event 

        # Global variables
        # run, lumi, event
        for attr in [ "run", "lumi", "evt"]:
            setattr( jet_out, attr, getattr( first_reader.event, attr) )

        # Variables that get a prefix 
        for r in reader.readers:
            # nVert
            setattr(jet_out, r.sample.name+'_nVert', len(filter( vertexID, r.event.vertices )) )
            # jet variables
            for jet_var in jet_vars:
                setattr( jet_out, r.sample.name+'_'+jet_var, jets[r.sample.name][jet_key][jet_var] )

        # fill ntuple
        maker.run()        

output_file.cd()
maker.tree.Write()
output_file.Close()

logger.info( "Written file %s", output_filename)
