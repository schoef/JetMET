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
##corrector_old     = JetCorrector.fromTarBalls( [(1, 'Fall17_17Nov2017F_V32_DATA') ], correctionLevels = correction_levels_data ) # 
#corrector_old_das = JetCorrector.fromTarBalls( [(1, 'Summer16_23Sep2016HV4_DATA') ], correctionLevels = correction_levels_data ) #this is what's used in prompt reco
#corrector_new     = JetCorrector.fromTarBalls( [(1, 'Autumn18_RunD_V8_DATA') ], correctionLevels = correction_levels_data )

corrector_old_das = JetCorrector.fromTarBalls( [(1, 'Fall17_17Nov2017B_V6_DATA') ], correctionLevels = correction_levels_data ) #this is what's used in prompt reco
corrector_new     = JetCorrector.fromTarBalls( [(1, 'Fall17_17Nov2017B_V32_DATA') ], correctionLevels = correction_levels_data )

# products  
products = { 
    'jets':{'type':'vector<pat::Jet>', 'label': ( "slimmedJets" )},
    'mets':{'type':'vector<pat::MET>',  'label':( "slimmedMETs" )},
    'rho': {'type':'double', 'label': ("fixedGridRhoFastjetAll")},
    'pf':  {'type':'vector<pat::PackedCandidate>', 'label': ("packedPFCandidates")}, 
   }

# sample  
#sample = FWLiteSample.fromFiles("test", files = ['file:/afs/hephy.at/data/dspitzbart01/event_0.root'])
#sample = FWLiteSample.fromFiles("test", files = ['file:/afs/hephy.at/work/r/rschoefbeck/CMS/tmp/CMSSW_10_2_9/src/StopsDilepton/plots/plotsRobert/tails/2018_mumu_lepSel-POGMetSig12-njet1-btag1p-relIso0.12-looseLeptonVeto-mll20-dPhiJet0-dPhiJet1/tmp_DoubleMuon_Run2018D-PromptReco-v2_MINIAOD.root'])

#2018D
#sample = FWLiteSample.fromFiles("test", files = ['root://cms-xrd-global.cern.ch//store/data/Run2018D/DoubleMuon/MINIAOD/PromptReco-v2/000/322/106/00000/DC6DE7DE-ACB2-E811-815C-FA163E0F815B.root'])
#2017 test
sample = FWLiteSample.fromFiles("test", files = ['file:dm_2017B_31Mar.root'] )
# Event loop
r = sample.fwliteReader( products = products )
r.start()
while r.run():
#    try:
#        if not r.run(): break
#    except:
#        print "Smth wrong in this event!", r.evt
#        r.position+=1
#        continue

    shift_x, shift_y = 0., 0.
    for j in r.event.jets:
#        print "pt (mAOD) % 7.5f pt(Uncorr) % 7.5f pT recorr(new) % 7.5f pT recorr(old,DAS) % 7.5f" %( 
#                j.pt(), 
#                j.correctedJet("Uncorrected").pt(),
#                j.correctedJet("Uncorrected").pt()*corrector_new.correction( j.correctedJet("Uncorrected").pt(), j.eta(), j.jetArea(), r.event.rho[0], r.event.run ), 
##                j.correctedJet("Uncorrected").pt()*corrector_old.correction( j.correctedJet("Uncorrected").pt(), j.eta(), j.jetArea(), r.event.rho[0], r.event.run ), 
#                j.correctedJet("Uncorrected").pt()*corrector_old_das.correction( j.correctedJet("Uncorrected").pt(), j.eta(), j.jetArea(), r.event.rho[0], r.event.run ), 
#            )
#        print j.pt(), j.correctedJet("Uncorrected").pt(), j.electronEnergyFraction(), j.photonEnergyFraction()

        if j.electronEnergyFraction()+j.photonEnergyFraction()<0.9:

            pt_raw   = j.correctedJet("Uncorrected").pt() 
            mu_ef    = j.muonEnergyFraction()
            phi      = j.phi()
            jec      = corrector_new.correction( (1-mu_ef)*pt_raw, j.eta(), j.jetArea(), r.event.rho[0], r.event.run )
            #shift_x += j.correctedJet("Uncorrected").p)t()*cos(j.correctedJet("Uncorrected").phi()) - j.pt()*cos(j.phi())
            #shift_y += j.correctedJet("Uncorrected").pt()*sin(j.correctedJet("Uncorrected").phi()) - j.pt()*sin(j.phi())
            cor_pt   = mu_ef*pt_raw+jec*(1-mu_ef)*pt_raw
            if jec*pt_raw*(1-mu_ef)>15:
                shift_x  += (pt_raw - cor_pt)*cos(phi)
                shift_y  += (pt_raw - cor_pt)*sin(phi)
                print "CORRECT WITH: jet pt (raw) % 7.5f muEF % 7.5f jec % 7.5f cor_pt % 7.5f" %( pt_raw, mu_ef, jec, cor_pt )

    m = r.event.mets[0]
   
    met_type1_px = m.uncorPt()*cos(m.uncorPhi()) + shift_x
    met_type1_py = m.uncorPt()*sin(m.uncorPhi()) + shift_y
    met_type1 = sqrt( met_type1_px**2 + met_type1_py**2)

    MEx = sum( [ -p.px() for p in r.event.pf ] )   
    MEy = sum( [ -p.py() for p in r.event.pf ] )   
    rawMET_recalc = sqrt( MEx**2 + MEy**2 ) 
    print "%i:%i:%i MET(raw) % 7.5f MET(raw, recalc) % 7.5f MET (mAOD) % 7.5f MET (uncorr) % 7.5f myMET % 7.5f" % (r.evt[0], r.evt[1], r.evt[2], m.uncorPt(), rawMET_recalc, m.pt(), m.uncorPt(), met_type1)
