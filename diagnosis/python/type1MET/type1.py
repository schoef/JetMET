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

#corrector_old     = JetCorrector.fromTarBalls( [(1, 'Fall17_17Nov2017F_V32_DATA') ], correctionLevels = correction_levels_data ) # 
corrector_old_das = JetCorrector.fromTarBalls( [(1, 'Summer16_23Sep2016HV4_DATA') ], correctionLevels = correction_levels_data ) #this is what's used in prompt reco
corrector_new     = JetCorrector.fromTarBalls( [(1, 'Autumn18_RunD_V8_DATA') ], correctionLevels = correction_levels_data )

# products  
products = { 
    'jets':{'type':'vector<pat::Jet>', 'label': ( "slimmedJets" )},
    'mets':{'type':'vector<pat::MET>',  'label':( "slimmedMETs" )},
    'rho': {'type':'double', 'label': ("fixedGridRhoFastjetAll")},
   }

# sample  
sample = FWLiteSample.fromFiles("test", files = ['file:/afs/hephy.at/data/dspitzbart01/event_0.root'])

# Event loop
r = sample.fwliteReader( products = products )
r.start()

while r.run():
    print r.evt

    shift_x, shift_y = 0., 0.
    for j in r.event.jets:
        print "pt (mAOD) % 7.5f pt(Uncorr) % 7.5f pT recorr(new) % 7.5f pT recorr(old,DAS) % 7.5f" %( 
                j.pt(), 
                j.correctedJet("Uncorrected").pt(),
                j.correctedJet("Uncorrected").pt()*corrector_new.correction( j.correctedJet("Uncorrected").pt(), j.eta(), j.jetArea(), r.event.rho[0], r.event.run ), 
#                j.correctedJet("Uncorrected").pt()*corrector_old.correction( j.correctedJet("Uncorrected").pt(), j.eta(), j.jetArea(), r.event.rho[0], r.event.run ), 
                j.correctedJet("Uncorrected").pt()*corrector_old_das.correction( j.correctedJet("Uncorrected").pt(), j.eta(), j.jetArea(), r.event.rho[0], r.event.run ), 
            )
        if j.pt()>15:
            shift_x += j.correctedJet("Uncorrected").pt()*cos(j.correctedJet("Uncorrected").phi()) - j.pt()*cos(j.phi())
            shift_y += j.correctedJet("Uncorrected").pt()*sin(j.correctedJet("Uncorrected").phi()) - j.pt()*sin(j.phi())

    m = r.event.mets[0]
   
    met_type1_px = m.uncorPt()*cos(m.uncorPhi()) + shift_x
    met_type1_py = m.uncorPt()*sin(m.uncorPhi()) + shift_y
    met_type1 = sqrt( met_type1_px**2 + met_type1_py**2)
    
    print "MET(raw) % 7.5f MET (mAOD) % 7.5f MET (uncorr) % 7.5f myMET % 7.5f" % (m.uncorPt(), m.pt(), m.uncorPt(), met_type1)
