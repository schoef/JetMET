#!/usr/bin/env python

# standard imports
import ROOT
import sys
import os
import copy
import subprocess
import shutil
import random

from operator import mul
from math import sqrt, atan2, sin, cos

# RootTools
from RootTools.core.standard import *

# User specific
import JetMET.tools.user as user

# JetMET
import JetMET.tools.helpers as helpers
from JetMET.tools.objectSelection        import getFilterCut, getJets, jetVars

# Hot jet veto
from JetMET.tools.hotJetVeto import hotJetVeto
default_hotJetVeto = hotJetVeto()

# JEC on the fly, tarball configuration
from JetMET.JetCorrector.JetCorrector import JetCorrector
from JetMET.JetCorrector.JetSmearer   import JetSmearer

#from StopsDilepton.tools.objectSelection import getMuons, getElectrons, muonSelector, eleSelector, getGoodLeptons, getGoodAndOtherLeptons,  getGoodBJets, getGoodJets, isBJet, jetId, isBJet, getGoodPhotons, getGenPartsAll, multiIsoWPInt

# central configuration
targetLumi = 1000 #pb-1 Which lumi to normalize to

def get_parser():
    ''' Argument parser for post-processing module.
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser for cmgPostProcessing")

    argParser.add_argument('--logLevel', action='store', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], default='INFO', help="Log level for logging")
    argParser.add_argument('--overwrite', action='store_true', help="Overwrite existing output files, bool flag set to True  if used", default=False) 
    argParser.add_argument('--sample', action='store', type=str, default='QCD_Pt_600to800', help="List of samples to be processed as defined in L2res_master" )
    argParser.add_argument('--eventsPerJob', action='store', nargs='?', type=int, default=300000, help="Maximum number of events per job (Approximate!)." )
    argParser.add_argument('--nJobs', action='store', nargs='?', type=int, default=1, help="Maximum number of simultaneous jobs." )    
    argParser.add_argument('--job', action='store', nargs='*', type=int, default=[], help="Run only jobs i" )
    argParser.add_argument('--minNJobs', action='store', nargs='?', type=int, default=1, help="Minimum number of simultaneous jobs." )
    argParser.add_argument('--targetDir', action='store', nargs='?', type=str, default=user.skim_ntuple_directory, help="Name of the directory the post-processed files will be saved" ) #user.data_output_directory
    #argParser.add_argument('--version', action='store', nargs='?', type=str, default='V1', help="JEC version" )
    argParser.add_argument('--processingEra', action='store', nargs='?', type=str, default='v8', help="Name of the processing era" )
    argParser.add_argument('--skim', action='store', nargs='?', type=str, default='default', help="Skim conditions to be applied for post-processing" )
    argParser.add_argument('--small', action='store_true', help="Run the file on a small sample (for test purpose), bool flag set to True if used", default = False)
    return argParser

options = get_parser().parse_args()

# Logging
import JetMET.tools.logger as logger
logFile = '/tmp/%s_%s_%s_njob%s.txt'%(options.skim, options.sample, os.environ['USER'], str(0 if options.nJobs==1 else options.job[0]))
logger  = logger.get_logger(options.logLevel, logFile = logFile)

import RootTools.core.logger as logger_rt
logger_rt = logger_rt.get_logger(options.logLevel, logFile = None )

# JetCorrector config
Summer16_03Feb2017_DATA = \
[(1,      'Summer16_03Feb2017BCD_V2_DATA'),
 (276831, 'Summer16_03Feb2017EF_V2_DATA' ),
 (278802, 'Summer16_03Feb2017G_V2_DATA' ),
 (280919, 'Summer16_03Feb2017H_V2_DATA')]

Summer16_03Feb2017_MC = [(1, 'Summer16_03Feb2017_V1_MC') ]

correction_levels_data  = [ 'L1FastJet', 'L2Relative', 'L3Absolute' ] # No residuals! 
correction_levels_mc    = [ 'L1FastJet', 'L2Relative', 'L3Absolute' ]

jetCorrector_data    = JetCorrector.fromTarBalls( Summer16_03Feb2017_DATA, correctionLevels = correction_levels_data )
jetCorrector_mc      = JetCorrector.fromTarBalls( Summer16_03Feb2017_MC,   correctionLevels = correction_levels_mc )

jetCorrector_RC_data = JetCorrector.fromTarBalls( Summer16_03Feb2017_DATA, correctionLevels = [ 'L1RC'] )
jetCorrector_RC_mc   = JetCorrector.fromTarBalls( Summer16_03Feb2017_MC,   correctionLevels = [ 'L1RC'] )

# Flags 
defSkim = options.skim.lower().startswith('default')

# Skim condition
skimConds = []
if defSkim:
    skimConds.append( "nJet>=2&&0.5*(Jet_pt[0]+Jet_pt[1])>50" )
    skimConds.append( "Sum$(LepGood_pt>100&&abs(LepGood_relIso03<0.5))==0" )

#Samples: Load samples
maxN = 1 if options.small else None
from JetMET.JEC.samples.L2res_master import L2res_master
sample = Sample.combine( options.sample, samples = [ Sample.fromCMGOutput("%i"%i_sample, baseDirectory = path, maxN = maxN) for i_sample, path in enumerate( L2res_master[options.sample] ) ] )
logger.debug("Reading from CMG tuple %s which are %i files.", options.sample, len(sample.files) )
    
isData = 'Run2016' in sample.name 
isMC   =  not isData 

# JER smearing (don't forget to call delete() )
smearer_mc = JetSmearer("Spring16_25nsV10_MC", "AK4PFchs") if isMC else None

if isMC:
    from JetMET.tools.puReweighting import getReweightingFunction
    puRW        = getReweightingFunction(data="PU_Run2016_36000_XSecCentral", mc='Summer16')
    puRWDown    = getReweightingFunction(data="PU_Run2016_36000_XSecDown",    mc='Summer16')
    puRWUp      = getReweightingFunction(data="PU_Run2016_36000_XSecUp",      mc='Summer16')

if options.small: options.targetDir = os.path.join( options.targetDir, 'small' )
output_directory = os.path.join( options.targetDir, options.processingEra, options.skim, sample.name )

if os.path.exists(output_directory) and options.overwrite:
    if options.nJobs > 1:
        logger.warning( "NOT removing directory %s because nJobs = %i", output_directory, options.nJobs )
    else:
        logger.info( "Output directory %s exists. Deleting.", output_directory )
        shutil.rmtree(output_directory)

try:    #Avoid trouble with race conditions in multithreading
    os.makedirs(output_directory)
    logger.info( "Created output directory %s.", output_directory )
except:
    pass

#branches to be kept for data and MC
branchKeepStrings_DATAMC = [\
    "run", "lumi", "evt", "isData", "rho", "nVert",
    "met_*", "chsSumPt", 
#        "metNoHF_pt", "metNoHF_phi",
#        "puppiMet_pt","puppiMet_phi","puppiMet_sumEt","puppiMet_rawPt","puppiMet_rawPhi","puppiMet_rawSumEt",
    "Flag_*","HLT_*",
    "Jet_pt", "Jet_eta", "Jet_phi", "Jet_area", "Jet_id", "Jet_btagCSV", "Jet_rawPt", "Jet_chHEF", "Jet_neHEF", "Jet_phEF", "Jet_eEF", "Jet_muEF", "Jet_HFHEF", "Jet_HFEMEF", "Jet_chHMult", "Jet_neHMult", "Jet_phMult", "Jet_eMult", "Jet_muMult", "Jet_HFHMult", "Jet_HFEMMult", 
    "JetFailId_pt", "JetFailId_eta", "JetFailId_phi", "JetFailId_area", "JetFailId_id", "JetFailId_btagCSV", "JetFailId_rawPt", "JetFailId_chHEF", "JetFailId_neHEF", "JetFailId_phEF", "JetFailId_eEF", "JetFailId_muEF", "JetFailId_HFHEF", "JetFailId_HFEMEF", "JetFailId_chHMult", "JetFailId_neHMult", "JetFailId_phMult", "JetFailId_eMult", "JetFailId_muMult", "JetFailId_HFHMult", "JetFailId_HFEMMult", 
    "DiscJet_pt", "DiscJet_eta", "DiscJet_phi", "DiscJet_area", "DiscJet_id", "DiscJet_btagCSV", "DiscJet_rawPt", "DiscJet_chHEF", "DiscJet_neHEF", "DiscJet_phEF", "DiscJet_eEF", "DiscJet_muEF", "DiscJet_HFHEF", "DiscJet_HFEMEF", "DiscJet_chHMult", "DiscJet_neHMult", "DiscJet_phMult", "DiscJet_eMult", "DiscJet_muMult", "DiscJet_HFHMult", "DiscJet_HFEMMult",
    "LepGood_pt", "LepGood_eta", "LepGood_phi", "LepGood_pdgId", "LepGood_relIso03", "LepGood_dxy", "LepGood_dz",
]

#branches to be kept for data samples only
branchKeepStrings_DATA = []
#branches to be kept for MC samples only
branchKeepStrings_MC = [\
    "nTrueInt", "genWeight", "xsec",  "lheHTIncoming",
    "Jet_mcPt", "Jet_mcPhi", "Jet_mcEta",
    "JetFailId_mcPt", "JetFailId_mcPhi", "JetFailId_mcEta",
]

if isMC:
    jetMCInfo = ['mcMatchFlav/I', 'partonId/I', 'partonMotherId/I', 'mcPt/F', 'mcFlavour/I', 'hadronFlavour/I', 'mcMatchId/I', 'partonFlavour/I']
else:
    jetMCInfo = []

if isData:
    lumiScaleFactor=None
    branchKeepStrings = branchKeepStrings_DATAMC + branchKeepStrings_DATA
    from FWCore.PythonUtilities.LumiList import LumiList
    # Apply golden JSON
    json = '$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt'
    lumiList = LumiList(os.path.expandvars(json))
    logger.info( "Loaded json %s", json )
else:
    lumiScaleFactor = targetLumi/float(sample.normalization) 
    branchKeepStrings = branchKeepStrings_DATAMC + branchKeepStrings_MC

skimConds.append( getFilterCut( positiveWeight = False, badMuonFilters = "Moriond2017" ) ) # always apply MC version. Data version has 'weight>0' which isnot for master ntuples

jetVars = ['pt/F', 'rawPt/F', 'eta/F', 'phi/F', 'id/I', 'btagCSV/F', 'area/F'] + jetMCInfo
jetVarNames = [x.split('/')[0] for x in jetVars]

read_variables = map(TreeVariable.fromString, ['met_pt/F', 'met_phi/F', 'run/I', 'lumi/I', 'evt/l', 'nVert/I', 'rho/F', 'met_chsPt/F', 'met_chsPhi/F'] )
read_variables += [\
#    TreeVariable.fromString('nLepGood/I'),
#    VectorTreeVariable.fromString('LepGood[pt/F,eta/F,etaSc/F,phi/F,pdgId/I,tightId/I,miniRelIso/F,relIso03/F,sip3d/F,mediumMuonId/I,mvaIdSpring15/F,lostHits/I,convVeto/I,dxy/F,dz/F,jetPtRelv2/F,jetPtRatiov2/F,eleCutId_Spring2016_25ns_v1_ConvVetoDxyDz/I]'),
    TreeVariable.fromString('nJet/I'),
    VectorTreeVariable.fromString('Jet[%s]'% ( ','.join(jetVars) ) )
]


new_variables = [ 'weight/F']
if isMC:
    read_variables+= map( TreeVariable.fromString, [ 'nTrueInt/F', 'xsec/F', 'genWeight/F'] )
new_variables += [ "tag_jet_index/I", "probe_jet_index/I", "third_jet_index/I", 'Jet[pt_corr/F,pt_corr_jer/F,pt_jer_up/F,pt_corr_jer_down/F,isHot/I]' ]

for jer in ['', 'jer', 'jer_up', 'jer_down']:
    postfix = '' if jer == '' else '_'+jer
    new_variables += [\
        "B%s/F"%postfix, "A%s/F"%postfix, "pt_avg%s/F"%postfix, "chs_MEx_corr%s/F"%postfix, "chs_MEy_corr%s/F"%postfix, "chs_MEt_corr%s/F"%postfix, "chs_MEphi_corr%s/F"%postfix, "alpha%s/F"%postfix
    ]

if isData: new_variables.extend( ['jsonPassed/I'] )


# Define a reader
reader = sample.treeReader( \
    variables = read_variables ,
    selectionString = "&&".join(skimConds)
    )

null_jet = {key:float('nan') for key in jetVars}
null_jet['pt']         = 0
null_jet['pt_corr']    = 0
null_jet['pt_corr_RC'] = 0
null_jet['pt_corr_jer']     = 0
null_jet['pt_corr_jer_up']  = 0
null_jet['pt_corr_jer_down']= 0
null_jet['index'] = -1

def filler( event ):
    # shortcut
    r = reader.event
    if isMC:
        event.weight = r.xsec*lumiScaleFactor*r.genWeight if lumiScaleFactor is not None else 1
    else:
        event.weight = 1
    # lumi lists and vetos
    if isData:
        #event.vetoPassed  = vetoList.passesVeto(r.run, r.lumi, r.evt)
        event.jsonPassed  = lumiList.contains(r.run, r.lumi)
        # store decision to use after filler has been executed
        event.jsonPassed_ = event.jsonPassed

    # PU weight
    if isMC:
        event.reweightPU     = puRW       ( r.nTrueInt ) 
        event.reweightPUDown = puRWDown   ( r.nTrueInt ) 
        event.reweightPUUp   = puRWUp     ( r.nTrueInt ) 

    jets = getJets( r, jetColl="Jet", jetVars = jetVarNames)

    event.nJetGood = len(jets) 
    for iJet, j in enumerate(jets):
        # 'Corr' correction level: L1L2L3 L2res
        if isData:
            jet_corr_factor    =  jetCorrector_data.   correction( j['rawPt'], j['eta'], j['area'], r.rho, r.run )
            jet_corr_factor_RC =  jetCorrector_RC_data.correction( j['rawPt'], j['eta'], j['area'], r.rho, r.run )
        else:
            jet_corr_factor    =  jetCorrector_mc.     correction( j['rawPt'], j['eta'], j['area'], r.rho, r.run )  
            jet_corr_factor_RC =  jetCorrector_RC_mc.  correction( j['rawPt'], j['eta'], j['area'], r.rho, r.run )  

        # corrected jet
        j['pt_corr']    =  jet_corr_factor * j['rawPt'] 
        event.Jet_pt_corr[iJet] = j['pt_corr'] 
        event.Jet_isHot[iJet]   = not default_hotJetVeto.passVeto(eta = j['eta'], phi = j['phi'])

        # L1RC 
        j['pt_corr_RC'] =  jet_corr_factor_RC * j['rawPt'] 

        # JER
        if isData:
            jet_corr_factor_jer, jet_corr_factor_jer_up, jet_corr_factor_jer_down = (1., 1., 1.)
        else:
            jet_corr_factor_jer, jet_corr_factor_jer_up, jet_corr_factor_jer_down = smearer_mc.hybrid_correction( pt = j['pt_corr'], mcPt = j['mcPt'], eta = j['eta'], rho = r.rho ) 

        j['pt_corr_jer']        =  jet_corr_factor_jer      * j['pt_corr'] 
        j['pt_corr_jer_up']     =  jet_corr_factor_jer_up   * j['pt_corr'] 
        j['pt_corr_jer_down']   =  jet_corr_factor_jer_down * j['pt_corr'] 

        # keep correction factors for type-1 MET shifts below
        j['corr_jer']        =  jet_corr_factor_jer       
        j['corr_jer_up']     =  jet_corr_factor_jer_up    
        j['corr_jer_down']   =  jet_corr_factor_jer_down  

    tag_jet, probe_jet = jets[:2]

    # randomize if both are in barrel:
    if abs(tag_jet['eta'])<1.3 and abs(probe_jet['eta'])<1.3:
        if random.random()>0.5:
            tag_jet, probe_jet = probe_jet, tag_jet
    # tag jet in barrel
    if abs(tag_jet['eta'])>1.3 and abs(probe_jet['eta'])<1.3:
        tag_jet, probe_jet = probe_jet, tag_jet

    third_jet = jets[2] if len(jets)>=3 else null_jet    

    event.tag_jet_index     = tag_jet['index']
    event.probe_jet_index   = probe_jet['index']
    event.third_jet_index   = third_jet['index']

    for jer in ['', 'jer', 'jer_up', 'jer_down']:
        postfix = '' if jer == '' else '_'+jer
        pt_corr = 'pt_corr' + postfix

        # PT avg
        pt_avg      = 0.5*( tag_jet[pt_corr] + probe_jet[pt_corr] )
        setattr( event, "pt_avg"+postfix, pt_avg )

        setattr( event, 'alpha'+postfix,  third_jet[pt_corr]/pt_avg )
        setattr( event, 'A'+postfix,     (probe_jet[pt_corr] - tag_jet[pt_corr]) / (probe_jet[pt_corr] + tag_jet[pt_corr]) )

        # MET corrections
        good_jets = filter( lambda j:j[pt_corr] > 15, jets)

        # compute type-1 MET shifts for chs met L1L2L3 - L1RC 
        jer_corr = 1 if jer=='' else j['corr' + postfix]
        type1_met_shifts = \
                    {'px' : jer_corr*sum( ( j['pt_corr_RC'] - j['pt_corr'] )*cos(j['phi']) for j in good_jets), 
                     'py' : jer_corr*sum( ( j['pt_corr_RC'] - j['pt_corr'] )*sin(j['phi']) for j in good_jets) } 

        # chs MET 
        chs_MEx_corr = r.met_chsPt*cos(r.met_chsPhi) + type1_met_shifts['px']
        chs_MEy_corr = r.met_chsPt*sin(r.met_chsPhi) + type1_met_shifts['py']
        setattr( event, "chs_MEx_corr"+postfix, chs_MEx_corr )
        setattr( event, "chs_MEy_corr"+postfix, chs_MEy_corr )

        chs_MEt_corr    = sqrt(  chs_MEx_corr**2 + chs_MEy_corr**2 )
        chs_MEphi_corr  = atan2( chs_MEy_corr, chs_MEx_corr )
        setattr( event, "chs_MEt_corr"+postfix, chs_MEt_corr )
        setattr( event, "chs_MEphi_corr"+postfix, chs_MEphi_corr )

        # R(MPF)
        setattr( event, 
                 'B'+postfix,  
                 ( chs_MEx_corr*tag_jet[pt_corr]*cos(tag_jet['phi'])  + chs_MEy_corr*tag_jet[pt_corr]*sin(tag_jet['phi']) ) / tag_jet[pt_corr] / (tag_jet[pt_corr] + probe_jet[pt_corr])
            )

# Create a maker. Maker class will be compiled. 
treeMaker_parent = TreeMaker(
    sequence  = [ filler ],
    variables = [ TreeVariable.fromString(x) for x in new_variables ],
    treeName = "Events"
    )

# Split input in ranges
if options.nJobs>1:
    eventRanges = reader.getEventRanges( nJobs = options.nJobs )
else:
    eventRanges = reader.getEventRanges( maxNEvents = options.eventsPerJob, minJobs = options.minNJobs )

logger.info( "Splitting into %i ranges of %i events on average.",  len(eventRanges), (eventRanges[-1][1] - eventRanges[0][0])/len(eventRanges) )

#Define all jobs
jobs = [(i, eventRanges[i]) for i in range(len(eventRanges))]

filename, ext = os.path.splitext( os.path.join(output_directory, sample.name + '.root') )

clonedEvents = 0
convertedEvents = 0
outputLumiList = {}
for ievtRange, eventRange in enumerate( eventRanges ):

    if len(options.job)>0 and not ievtRange in options.job: continue

    logger.info( "Processing range %i/%i from %i to %i which are %i events.",  ievtRange, len(eventRanges), eventRange[0], eventRange[1], eventRange[1]-eventRange[0] )

    # Check whether file exists
    outfilename = filename+'_'+str(ievtRange)+ext
    if os.path.isfile(outfilename):
        logger.info( "Output file %s found.", outfilename)
        if not helpers.checkRootFile(outfilename, checkForObjects=["Events"]):
            logger.info( "File %s is broken. Overwriting.", outfilename)
        elif not options.overwrite:
            logger.info( "Skipping.")
            continue
        else:
            logger.info( "Overwriting.")

    tmp_directory = ROOT.gDirectory
    outputfile = ROOT.TFile.Open(outfilename, 'recreate')
    tmp_directory.cd()

    if options.small: 
        logger.info("Running 'small'. Not more than 10000 events") 
        nMaxEvents = eventRange[1]-eventRange[0]
        eventRange = ( eventRange[0], eventRange[0] +  min( [nMaxEvents, 10000] ) )

    # Set the reader to the event range
    reader.setEventRange( eventRange )

    clonedTree = reader.cloneTree( branchKeepStrings, newTreename = "Events", rootfile = outputfile )
    clonedEvents += clonedTree.GetEntries()
    # Clone the empty maker in order to avoid recompilation at every loop iteration
    maker = treeMaker_parent.cloneWithoutCompile( externalTree = clonedTree )

    maker.start()
    # Do the thing
    reader.start()

    while reader.run():
        maker.run()
        if isData:
            if maker.event.jsonPassed_:
                if reader.event.run not in outputLumiList.keys():
                    outputLumiList[reader.event.run] = set([reader.event.lumi])
                else:
                    if reader.event.lumi not in outputLumiList[reader.event.run]:
                        outputLumiList[reader.event.run].add(reader.event.lumi)

    convertedEvents += maker.tree.GetEntries()
    maker.tree.Write()
    outputfile.Close()
    logger.info( "Written %s", outfilename)

  # Destroy the TTree
    maker.clear()

logger.info( "Converted %i events of %i, cloned %i",  convertedEvents, reader.nEvents , clonedEvents )

# Avoid segfault
if not isData: smearer_mc.delete()

# Storing JSON file of processed events
if isData:
    jsonFile = filename+'.json'
    LumiList( runsAndLumis = outputLumiList ).writeJSON(jsonFile)
    logger.info( "Written JSON file %s",  jsonFile )

logger.info("Copying log file to %s", output_directory )
copyLog = subprocess.call(['cp', logFile, output_directory] )
if copyLog:
    logger.info( "Copying log from %s to %s failed", logFile, output_directory)
else:
    logger.info( "Successfully copied log file" )
    os.remove(logFile)
    logger.info( "Removed temporary log file" )

