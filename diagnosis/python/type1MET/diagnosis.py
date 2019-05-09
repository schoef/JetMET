''' Type-1 Check 
'''
# Standrd imports
from math import sqrt, atan2, cos, sin

# RootTools 
from RootTools.core.standard import *

# Logging
import JetMET.tools.logger as logger
logger    = logger.get_logger('INFO', logFile = None)
import RootTools.core.logger as logger_rt
logger_rt = logger_rt.get_logger('INFO', logFile = None)

# JECconfig
from JetMET.JetCorrector.JetCorrector import JetCorrector, correction_levels_data, correction_levels_mc

## Run2018D
#corrector_old     = JetCorrector.fromTarBalls( [(1, 'Fall17_17Nov2017F_V32_DATA') ], correctionLevels = correction_levels_data ) # 
# from DAS
corrector_orig     = JetCorrector.fromTarBalls( [(1, 'Summer16_23Sep2016HV4_DATA') ], correctionLevels = correction_levels_data )
corrector_orig_L1  = JetCorrector.fromTarBalls( [(1, 'Summer16_23Sep2016HV4_DATA') ], correctionLevels = ['L1FastJet'] )
# new JEC
corrector     = JetCorrector.fromTarBalls( [(1, 'Autumn18_RunD_V8_DATA') ], correctionLevels = correction_levels_data )
corrector_L1  = JetCorrector.fromTarBalls( [(1, 'Autumn18_RunD_V8_DATA') ], correctionLevels = ['L1FastJet'] )

#corrector = JetCorrector.fromTarBalls( [(1, 'Fall17_17Nov2017B_V6_DATA') ], correctionLevels = correction_levels_data ) #this is what's used in prompt reco
#corrector_new     = JetCorrector.fromTarBalls( [(1, 'Fall17_17Nov2017B_V32_DATA') ], correctionLevels = correction_levels_data )

# products  
products_original = { 
    'slimmedMETs':{'type':'vector<pat::MET>',  'label':( "slimmedMETs" )},
    'slimmedJets':{'type':'vector<pat::Jet>', 'label': ( "slimmedJets" )},
    'rho': {'type':'double', 'label': ("fixedGridRhoFastjetAll")},
    'pf':  {'type':'vector<pat::PackedCandidate>', 'label': ("packedPFCandidates")}, 
   }
products_rerun = { 
    'slimmedMETs'   :{'type':'vector<pat::MET>',  'label':( "slimmedMETs" )},
    'CorrMETData'   :{ 'type':'CorrMETData', 'label':("patPFMetT1T2Corr", "type1", "RERUN") },
    'cleanedPatJets':{'type':'vector<pat::Jet>', 'label': ( "cleanedPatJets" )},
    'patJets':{'type':'vector<pat::Jet>', 'label': ( "patJets" )},
    'basicJetsForMet':{'type':'vector<pat::Jet>', 'label': ( "basicJetsForMet" )},
    'slimmedJets':   {'type':'vector<pat::Jet>', 'label': ( "slimmedJets" )},
    'pf':            {'type':'vector<pat::PackedCandidate>', 'label': ("packedPFCandidates")}, 
   }

# sample  
#2018D, 1 event
#original = FWLiteSample.fromFiles("test", files = ['file:event_0.root'])
#rerun    = FWLiteSample.fromFiles("test", files = ['file:event_0_corMETMiniAOD.root'])
original = FWLiteSample.fromFiles("test", files = ['file:tail.root'])
rerun    = FWLiteSample.fromFiles("test", files = ['file:tail_corMETMiniAOD.root'])

# Event loop
r_original = original.fwliteReader( products = products_original )
r_rerun    = rerun.fwliteReader( products = products_rerun )
r_original.start()
r_rerun.start()
while r_original.run():
    r_rerun.run()

    ## compare raw METs

    # raw MET from PF in original sample
    MEx = sum( [ -p.px() for p in r_original.event.pf ] )   
    MEy = sum( [ -p.py() for p in r_original.event.pf ] )   
    rawMET_original_fromPF = sqrt( MEx**2 + MEy**2 ) 
    print "###### Compare RawMETs (orig/rerun/PF), corMetData (rerun) and type-1METs ##############"
    print "RawMET      original slimmedMETs.uncorPt  {:10.4f} (from PF: {:10.4f}) rerun: {:10.4f} px {:10.4f} py {:10.4f}".format( r_original.event.slimmedMETs[0].uncorPt(), rawMET_original_fromPF, r_rerun.event.slimmedMETs[0].uncorPt(), r_rerun.event.slimmedMETs[0].uncorPx(), r_rerun.event.slimmedMETs[0].uncorPy()) 
    print "Type-1 MET  original slimmedMETs.pt       {:10.4f}                       rerun: {:10.4f} px {:10.4f} py {:10.4f}".format( r_original.event.slimmedMETs[0].pt(), r_rerun.event.slimmedMETs[0].pt(), r_rerun.event.slimmedMETs[0].px(), r_rerun.event.slimmedMETs[0].py()) 

    type1_fromCorMetData = sqrt( (r_rerun.event.slimmedMETs[0].uncorPx() + r_rerun.event.CorrMETData.mex)**2 + (r_rerun.event.slimmedMETs[0].uncorPy() + r_rerun.event.CorrMETData.mey)**2 )
    print "Rerun CorMetData MEx {:6.4f} MEy {:6.4f}        type-1 MET CorMetData + RawMET: {:10.4f} (rerun was: {:10.4f})".format( r_rerun.event.CorrMETData.mex, r_rerun.event.CorrMETData.mey, type1_fromCorMetData,  r_rerun.event.slimmedMETs[0].pt())
    if abs(type1_fromCorMetData - r_rerun.event.slimmedMETs[0].pt()):
        print "CorMetData + RawMET = type1Met (rerun) are consistent."
    else:
        print "CorMetData + RawMET = type1Met (rerun) are INCONSISTENT."

    print "##################### Check basicJetsForMet ##################################"
    for i_jet, jet in enumerate(r_rerun.event.basicJetsForMet):
        uncor_pt = jet.correctedJet("Uncorrected").pt()
        jec    = corrector   .correction( uncor_pt, jet.eta(), jet.jetArea(), r_original.event.rho[0], r_rerun.event.run )
        jec_L1 = corrector_L1.correction( uncor_pt, jet.eta(), jet.jetArea(), r_original.event.rho[0], r_rerun.event.run )
        print "cleanedPatJets     {:d} pt(Uncorrected) {:10.4} pt(L1FastJet) {:10.4} pt(Corrected) {:10.4}".format( i_jet, uncor_pt, jet.correctedJet("L1FastJet").pt(), jet.pt() )
        print "offline corrected                               pt(L1FastJet) {:10.4} pt(Corrected) {:10.4}".format( uncor_pt*jec_L1, uncor_pt*jec  )
    print "##################### Check cleanedPatJets ##################################"
    for i_jet, jet in enumerate(r_rerun.event.cleanedPatJets):
        uncor_pt = jet.correctedJet("Uncorrected").pt()
        jec    = corrector   .correction( uncor_pt, jet.eta(), jet.jetArea(), r_original.event.rho[0], r_rerun.event.run )
        jec_L1 = corrector_L1.correction( uncor_pt, jet.eta(), jet.jetArea(), r_original.event.rho[0], r_rerun.event.run )
        print "cleanedPatJets     {:d} pt(Uncorrected) {:10.4} pt(L1FastJet) {:10.4} pt(Corrected) {:10.4}".format( i_jet, uncor_pt, jet.correctedJet("L1FastJet").pt(), jet.pt() )
        print "offline corrected                               pt(L1FastJet) {:10.4} pt(Corrected) {:10.4}".format( uncor_pt*jec_L1, uncor_pt*jec  )
    print "##################### Check slimmedJets ##################################"
    for i_jet, jet in enumerate(r_rerun.event.slimmedJets):
        uncor_pt = jet.correctedJet("Uncorrected").pt()
        jec    = corrector_orig   .correction( uncor_pt, jet.eta(), jet.jetArea(), r_original.event.rho[0], r_rerun.event.run )
        jec_L1 = corrector_orig_L1.correction( uncor_pt, jet.eta(), jet.jetArea(), r_original.event.rho[0], r_rerun.event.run )
        print "slimmedJets        {:d} pt(Uncorrected) {:10.4} pt(L1FastJet) {:10.4} pt(Corrected) {:10.4}  muEF {:10.4f}".format( i_jet, uncor_pt, jet.correctedJet("L1FastJet").pt(), jet.pt(), jet.muonEnergyFraction())
        print "offline corrected                               pt(L1FastJet) {:10.4} pt(Corrected) {:10.4}".format( uncor_pt*jec_L1, uncor_pt*jec  )

    print "##################### Compare CorMetData and cleanPatJets ##################################"
    # type1 jet selection in PFJetMETcorrInputProducerT.h
    # https://github.com/cms-sw/cmssw/blob/CMSSW_10_2_X/JetMETCorrections/Type1MET/interface/PFJetMETcorrInputProducerT.h#L188
    # FIRST check EMF < 0.9, THEN subtract muon momentum from jets
    shift_px, shift_py = 0., 0.
    for i_jet, jet in enumerate(r_rerun.event.cleanedPatJets):
        # check EMF
        if jet.chargedEmEnergyFraction() + jet.neutralEmEnergyFraction()>0.9:
            print "Not using jet {:d} with pt {:10.4} for type-1 because it fails EMF<0.9".format( i_jet, jet.pt() )
            continue

        rawJetp4 = jet.correctedJet("Uncorrected").p4()

        # subtract muons (Global | SA) 4 momentum
        for p_ in jet.getJetConstituents():
            p = p_.get()
            if abs(p.pdgId())==13 and ( p.isGlobalMuon() or p.isStandAloneMuon() ):
                print "Jet {:d}: subtract muon with pt {:10.4} from rawJetp4 with pt {:10.4}".format( i_jet, p.pt(), rawJetp4.pt())
                rawJetp4 -= p.p4()

        rawJetPt = rawJetp4.pt()
        # Evaluate JEC at the non-mu subtracted raw momentum. This looks different PFJetMETcorrInputProducerT, however, Mathieu back-corrected the missing muon in PATJetCorrExtractor
        # Note further that JEC are evaluated at the eta of the subtracted jet
        jec    = corrector   .correction( jet.correctedJet("Uncorrected").pt(), jet.eta(), jet.jetArea(), r_original.event.rho[0], r_rerun.event.run )
        jec_L1 = corrector_L1.correction( jet.correctedJet("Uncorrected").pt(), jet.eta(), jet.jetArea(), r_original.event.rho[0], r_rerun.event.run )

        # check pt 
        if jec*rawJetPt>15:
            shift_px += (jec_L1*rawJetPt - jec*rawJetPt)*cos(rawJetp4.phi())
            shift_py += (jec_L1*rawJetPt - jec*rawJetPt)*sin(rawJetp4.phi())
        else:
            print "Not using the next one (jec*rawJetPt = {:6.4}):".format( rawJetPt )

        print "Rerun: cleanedPatJets: {:d}: pt(cor) {:10.4} shift_x = L1 - L1L2L3 becomes {:10.4} - {:10.4} = {:10.4}".format( i_jet, jet.pt(), jec_L1*rawJetPt*cos(rawJetp4.phi()), jec*rawJetPt*cos(rawJetp4.phi()), (jec_L1*rawJetPt - jec*rawJetPt)*cos(rawJetp4.phi())) 
        print "                       {:d}:                    shift_y = L1 - L1L2L3 becomes {:10.4} - {:10.4} = {:10.4} pt@JEC {:10.4}".format( i_jet, jec_L1*rawJetPt*sin(rawJetp4.phi()), jec*rawJetPt*sin(rawJetp4.phi()), (jec_L1*rawJetPt - jec*rawJetPt)*sin(rawJetp4.phi()), rawJetPt) 
        
    print "rerun cleanedPatJets give shifts: {:10.4},{:10.4} in corMEtData it was: {:10.4},{:10.4}".format( shift_px, shift_py, r_rerun.event.CorrMETData.mex, r_rerun.event.CorrMETData.mey ) 
    print "rerun recalculated MET from shifts: {:6.4}".format( sqrt( (shift_px + r_rerun.event.slimmedMETs[0].uncorPx())**2 + ( shift_py + r_rerun.event.slimmedMETs[0].uncorPy() )**2 ) )

    break
