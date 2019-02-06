#!/usr/bin/env python
''' Analysis script for gen plots
'''
#
# Standard imports and batch mode
#
import ROOT, os
ROOT.gROOT.SetBatch(True)
import itertools
from math                                import sqrt, cos, sin, pi, acos, atan2
import imp

#RootTools
from RootTools.core.standard             import *

#JetMET
from JetMET.tools.user                   import skim_ntuple_directory, cache_directory
from JetMET.tools.helpers                import deltaR2, jetID, vertexID, checkRootFile

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--small',              action='store_true', help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--maxEvents',          action='store',      type=int, default=-1, help='Maximum number of events')
argParser.add_argument('--maxFiles',           action='store',      type=int, default=-1, help='Maximum number of files')
argParser.add_argument('--minNVert',           action='store',      type=int, default=-1, help="minimum number of good vertices")
argParser.add_argument('--targetDir',          action='store',      default='flat_jet_trees/v6')
argParser.add_argument('--sample',             action='store',      default='/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM')
argParser.add_argument('--nJobs',              action='store',      nargs='?', type=int, default=1,  help="Maximum number of simultaneous jobs.")
argParser.add_argument('--job',                action='store',      nargs='?', type=int, default=0,  help="Run only job i")
argParser.add_argument('--overwrite',          action='store_true', help='overwrite?')#, default = True)
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

sample = FWLiteSample.fromDAS( sample_name, args.sample, maxN = maxN, dbFile = os.path.join( cache_directory, 'fwlite_cache.db' ))  
output_directory = os.path.join(skim_ntuple_directory, args.targetDir, sample.name) 

# Run only job number "args.job" from total of "args.nJobs"
if args.nJobs>1:
    n_files_before = len(sample.files)
    sample = sample.split(args.nJobs)[args.job]
    n_files_after  = len(sample.files)
    logger.info( "Running job %i/%i over %i files from a total of %i.", args.job, args.nJobs, n_files_after, n_files_before)

output_filename =  os.path.join(output_directory, sample.name + '.root') 

if 'Run2018' in sample.name:
    from FWCore.PythonUtilities.LumiList import LumiList
    json = '$CMSSW_BASE/src/JetMET/diagnosis/python/pu2018/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
    lumiList = LumiList(os.path.expandvars(json))
else:
    lumiList = None

if args.maxFiles > 0:
    sample.files = sample.files[:args.maxFiles]

if not os.path.exists( output_directory ): 
    os.makedirs( output_directory )
    logger.info( "Created output directory %s", output_directory )

products = {
     'muon':                                     {'skip':False,'type':'vector<pat::Muon>', 'label': ("slimmedMuons")},
     'vertices':                                 {'skip':False, 'type':'vector<reco::Vertex>', 'label':('offlineSlimmedPrimaryVertices')},
}
extra_products = {
     'jets':                                     {'skip':True, 'type':'vector<pat::Jet>', 'label': ("slimmedJets")},
     'fixedGridRhoAll':                          {'skip':True,'type':'double', 'label': ("fixedGridRhoAll", "", "RECO")},
     'fixedGridRhoFastjetAll':                   {'skip':True,'type':'double', 'label': ("fixedGridRhoFastjetAll", "", "RECO")},
     'fixedGridRhoFastjetAllCalo':               {'skip':True,'type':'double', 'label': ("fixedGridRhoFastjetAllCalo", "", "RECO")},
     'fixedGridRhoFastjetCentral':               {'skip':True,'type':'double', 'label': ("fixedGridRhoFastjetCentral", "", "RECO")},
     'fixedGridRhoFastjetCentralCalo':           {'skip':True,'type':'double', 'label': ("fixedGridRhoFastjetCentralCalo", "", "RECO")},
     'fixedGridRhoFastjetCentralChargedPileUp':  {'skip':True,'type':'double', 'label': ("fixedGridRhoFastjetCentralChargedPileUp", "", "RECO")},
     'fixedGridRhoFastjetCentralNeutral':        {'skip':True,'type':'double', 'label': ("fixedGridRhoFastjetCentralNeutral", "", "RECO")},
     'met':                                      {'skip':True,'type':'vector<pat::MET>', 'label': ("slimmedMETs")},
     'pf':                                       {'skip':True,'type':'vector<pat::PackedCandidate>', 'label': ("packedPFCandidates")},
     'triggerResults':                           {'skip':True,'type':'edm::TriggerResults', 'label':("TriggerResults")},
}
products.update( extra_products )


reader = sample.fwliteReader( products = products )

new_variables =  [ "evt/l", "run/I", "lumi/I", "nVert/I", "nVertAll/I", "closest_dz_good/F", "closest_dz_all/F", "bx/I"] 
new_variables += [ "jet[pt/F,genPt/F,genEta/F,genPhi/F,rawPt/F,eta/F,phi/F,chHEF/F,neHEF/F,phEF/F,eEF/F,muEF/F,HFHEF/F,HFEMEF/F,chHMult/F,neHMult/F,phMult/F,eMult/F,muMult/F,HFHMult/F,HFEMMult/F]"]
new_variables += [ "met_pt/F", "met_phi/F"]
new_variables += [ "fixedGridRhoAll/F", "fixedGridRhoFastjetAll/F", "fixedGridRhoFastjetAllCalo/F", "fixedGridRhoFastjetCentral/F", "fixedGridRhoFastjetCentralCalo/F", "fixedGridRhoFastjetCentralChargedPileUp/F", "fixedGridRhoFastjetCentralNeutral/F" ]

filters = ["Flag_goodVertices", "Flag_globalSuperTightHalo2016Filter", "Flag_HBHENoiseFilter", "Flag_HBHENoiseIsoFilter", "Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_BadPFMuonFilter", "Flag_BadChargedCandidateFilter", "Flag_eeBadScFilter"]
for f in filters:
    new_variables.append( "%s/I"%f )

eta_bins_ = [ ( -5.1, -3.1), (-3.1, -2.5), (-2.5, -1.5), (-1.5, 1.5), (1.5, 2.5), (2.5, 3.1), (3.1, 5.1) ] 
pf_types_ = [ ("el", 11), ("mu", 13), ("ga", 22), ("ch", 211), ("nh", 130), ("HFh", 1), ("HFe", 2) ]

def eta_selector( eta_bin ):
    def func( p ):
        eta = p.eta()
        return p.eta()>=eta_bin[0] and p.eta()<eta_bin[1]
    return func
def pf_selector( pf_type ):
    def func( p ):
        pdgId = p.pdgId()
        return abs(pdgId)==pf_type[1]
    return func

def str_name( eta_bin ):
    return str(eta_bin[0]).replace('-','m').replace('.', 'p')+'_'+str(eta_bin[1]).replace('-','m').replace('.', 'p')

def alwaysTrue( *args, **kwargs):
    return True

eta_bins = [ {'name':str_name(e), 'sel':eta_selector(e)} for e in eta_bins_]
eta_bins.append( {'name':'all', 'sel': alwaysTrue } )

pf_types = [ {'name':p[0],  'sel':pf_selector(p)}  for p in pf_types_]
pf_types.append( {'name':'all', 'sel': alwaysTrue} )

for eta_bin in eta_bins:
    for pf_type in pf_types:
        for var in ['met/F', 'sumPt/F', 'metPhi/F', 'mult/I']:
            new_variables.append( '%s_%s_%s' % ( pf_type['name'], eta_bin['name'], var ) )

if not (os.path.exists( output_filename ) and checkRootFile( output_filename, ["Events"]))  or args.overwrite:
    # Maker
    tmp_dir     = ROOT.gDirectory
    output_file = ROOT.TFile( output_filename, 'recreate')
    output_file.cd()
    maker =    TreeMaker( sequence = [], variables = map( TreeVariable.fromString, new_variables ), treeName = "Events")
    tmp_dir.cd()
else:
    raise IOError( "File %s exists!" % output_filename )

# Filler for data struct of maker
def jet_filler(struct, jets):

    for i, jet in enumerate(jets):

        struct.njet = len(jets)
        struct.jet_pt    [i] =  jet.pt()

        gen_jet = jet.genJet()
        struct.jet_genPt [i] =  gen_jet.pt()  if gen_jet else float('nan')
        struct.jet_genEta[i] =  gen_jet.eta() if gen_jet else float('nan')
        struct.jet_genPhi[i] =  gen_jet.phi() if gen_jet else float('nan')
        struct.jet_rawPt [i] =  jet.correctedJet("Uncorrected").pt()
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
            ("chHMult", "chargedHadronMultiplicity"),
            ("neHMult", "neutralHadronMultiplicity"),
            ("phMult",  "photonMultiplicity"),
            ("eMult",   "electronMultiplicity"),
            ("muMult",  "muonMultiplicity"),
            ("HFHMult", "HFHadronMultiplicity"),
            ("HFEMMult","HFEMMultiplicity"),
            ]:
                getattr(struct, 'jet_'+name)[i] = getattr(jet, func)()
    return

def relIso03( p ):
    # https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/muons_cff.py#L112
    return (p.pfIsolationR03().sumChargedHadronPt + max(p.pfIsolationR03().sumNeutralHadronEt + p.pfIsolationR03().sumPhotonEt - p.pfIsolationR03().sumPUPt/2,0.0))/p.pt()

reader.start()
maker.start()

counter_read = -1 
counter_write = -1 

while reader.run():
    counter_read += 1
    if counter_read%100==0: logger.info("Reading event %i.", counter_read)

    maker.event.run, maker.event.lumi, maker.event.evt = reader.evt
    # json
    if lumiList is not None and not lumiList.contains(maker.event.run, maker.event.lumi): continue

    muons = filter( lambda p:p.pt()>15 and abs(p.eta())<2.4 and p.CutBasedIdMedium and relIso03(p)<0.2, reader.products['muon'] )
    if len(muons)<2: continue

    # Vertices
    maker.event.nVertAll = len( reader.products['vertices'] )
    vertices       = filter( vertexID, reader.products['vertices'] )
    maker.event.nVert    = len( vertices )
    maker.event.bx = reader.sample.events._event.bunchCrossing()

    if len ( vertices ) < args.minNVert:
        continue

    # read the rest of the stuff when selection is done
    for name in extra_products.keys():
        reader.readProduct( name ) 


    # require 1 good vertex
    if len(vertices)==0: continue

    leading_vertex = vertices[0]  
    maker.event.closest_dz_good = min( [abs( leading_vertex.z() - vertex.z() ) for vertex in vertices if vertex != leading_vertex ] )
    maker.event.closest_dz_all  = min( [abs( leading_vertex.z() - vertex.z() ) for vertex in reader.products['vertices'] if vertex != leading_vertex ] )

    # Jets
    jets      = filter( jetID, reader.products['jets'] )
    jet_filler( maker.event, jets )

    # MET
    maker.event.met_pt  = reader.products['met'][0].pt()
    maker.event.met_phi = reader.products['met'][0].phi()

    # Filters
    triggerResults = reader.products['triggerResults']
    triggerNames = reader.sample.events._event.triggerNames(triggerResults)
    for f in filters:
        setattr( maker.event, f, triggerResults.accept(triggerNames.triggerIndex(f)))

    # rhos
    maker.event.fixedGridRhoAll                   = reader.products['fixedGridRhoAll'][0]
    maker.event.fixedGridRhoFastjetAll            = reader.products['fixedGridRhoFastjetAll'][0]
    maker.event.fixedGridRhoFastjetAllCalo        = reader.products['fixedGridRhoFastjetAllCalo'][0]
    maker.event.fixedGridRhoFastjetCentral        = reader.products['fixedGridRhoFastjetCentral'][0]
    maker.event.fixedGridRhoFastjetCentralCalo    = reader.products['fixedGridRhoFastjetCentralCalo'][0]
    maker.event.fixedGridRhoFastjetCentralChargedPileUp = reader.products['fixedGridRhoFastjetCentralChargedPileUp'][0]
    maker.event.fixedGridRhoFastjetCentralNeutral = reader.products['fixedGridRhoFastjetCentralNeutral'][0]

    # pf Candidates
    pf = reader.products['pf']
    for eta_bin in eta_bins:
        particles_eta_bin = filter( eta_bin['sel'], pf )
        for pf_type in pf_types:

            name = pf_type['name']+'_'+eta_bin['name']
            particles_eta_bin_pf_type = filter( pf_type['sel'], particles_eta_bin )
            setattr( maker.event, name+'_sumPt',  sum( [p.pt() for p in particles_eta_bin_pf_type], 0.))
            setattr( maker.event, name+'_mult',   len( particles_eta_bin_pf_type ) )

            MEx = sum( [ -p.pt()*cos(p.phi()) for p in particles_eta_bin_pf_type], 0.)
            MEy = sum( [ -p.pt()*sin(p.phi()) for p in particles_eta_bin_pf_type], 0.)

            setattr( maker.event, name+'_met',     sqrt(MEx**2 + MEy**2 ) )
            setattr( maker.event, name+'_metPhi',  atan2( MEy, MEx ) )
                 
    # fill ntuple
    maker.run()        

    # Stop.
    counter_write += 1
    if args.maxEvents>0 and counter_write>=args.maxEvents: break

output_file.cd()
maker.tree.Write()
output_file.Close()

logger.info( "Written file %s", output_filename)
