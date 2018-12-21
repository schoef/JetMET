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

# samples
from JetMET.response.jet_response_2017_EE.samples import *

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO',  nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--small',              action='store_true', help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--maxEvents',          action='store',      type=int, default=-1, help='Maximum number of events')
argParser.add_argument('--maxFiles',           action='store',      type=int, default=-1, help='Maximum number of files')
argParser.add_argument('--overwrite',          action='store_true', help='overwrite?')
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

output_directory = os.path.join(skim_ntuple_directory, args.targetDir, "merged_RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9") 
output_filename =  os.path.join(output_directory, 'jets.root') 
if not os.path.exists( output_directory ): 
    os.makedirs( output_directory )
    logger.info( "Created output directory %s", output_directory )

samples = [ { 'prefix':name, 'sample':dataset } for name, dataset in \
  [
    ( "GTv1_SRPFoff_NoPU"    ,   RelVal_QCD_flat_GTv1_SRPFoff_NoPU),
    ( "GTv1_SRPFoff_PUpmx25ns",  RelVal_QCD_flat_GTv1_SRPFoff_PUpmx25ns),
    ( "GTv2_SRPFoff_NoPU"    ,   RelVal_QCD_flat_GTv2_SRPFoff_NoPU),
    ( "GTv2_SRPFoff_PUpmx25ns",  RelVal_QCD_flat_GTv2_SRPFoff_PUpmx25ns),
    ( "GTv2_SRPFon_NoPU"     ,   RelVal_QCD_flat_GTv2_SRPFon_NoPU),
    ( "GTv2_SRPFon_PUpmx25ns",   RelVal_QCD_flat_GTv2_SRPFon_PUpmx25ns),
 ] ]

variables_firstsample =  [ "evt/l", "run/I", "lumi/I" ]
variables_persample   =  [ "nVert/I", "genPt/F", "rawPt/F", "eta/F", "phi/F", "chHEF/F", "neHEF/F", "phEF/F", "eEF/F", "muEF/F", "HFHEF/F", "HFEMEF/F" ]

jet_vars = [ s.split('/')[0] for s in variables_persample]

for sample in samples:
    # Make fwlite reader
    sample['reader'] = sample['sample'].treeReader( variables = map( TreeVariable.fromString, variables_firstsample + variables_persample) )

default_key = lambda event: ( event.run, event.lumi, event.evt, event.genPt )
reader = MultiReader( *[ (sample['reader'], default_key) for sample in samples ] )

maker_variables = variables_firstsample + sum( [[ sample['prefix']+'_'+var for var in variables_persample] for sample in samples ], [] )

if not os.path.exists( output_filename ) or args.overwrite:
    # Maker
    tmp_dir     = ROOT.gDirectory
    output_file = ROOT.TFile( output_filename, 'recreate')
    output_file.cd()
    maker =    TreeMaker( sequence = [], variables = map( TreeVariable.fromString, maker_variables ), treeName = "jets")
    tmp_dir.cd()
else:
    raise IOError( "File %s exists!" % output_filename )

reader.start()
maker.start()

counter = -1 

while reader.run():
    counter += 1
    if args.maxEvents>0 and counter>=args.maxEvents: break

    if counter%100==0: logger.info("At event %i.", counter)

    first_reader = reader.readers[0]
   
    # convinience
    jet_out = maker.event 

    # Global variables
    # run, lumi, event
    for attr in [ "run", "lumi", "evt"]:
        setattr( jet_out, attr, getattr( first_reader.event, attr) )

    # Variables that get a prefix 
    for s in samples:
        # Convinience
        r = s['reader']

        # nVert
        setattr(jet_out, s['prefix']+'_nVert', r.event.nVert )

        # jet variables
        for jet_var in jet_vars:
            setattr( jet_out, s['prefix']+'_'+jet_var, getattr( r.event, jet_var ) )

    # fill ntuple
    maker.run()        
    
output_file.cd()
maker.tree.Write()
output_file.Close()

logger.info( "Written file %s", output_filename)
