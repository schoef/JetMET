''' Type-1 Check 
'''
#RootTools 
from RootTools.core.standard import *

# Logging
import JetMET.tools.logger as logger
logger    = logger.get_logger('INFO', logFile = None)
import RootTools.core.logger as logger_rt
logger_rt = logger_rt.get_logger('INFO', logFile = None)

# JECconfig
from JetMET.JetCorrector.JetCorrector import JetCorrector, correction_levels_data, correction_levels_mc

corrector_old = JetCorrector.fromTarBalls( [(1, 'Fall17_17Nov2017F_V32_DATA') ], correctionLevels = correction_levels_data )
corrector_new = JetCorrector.fromTarBalls( [(1, 'Autumn18_RunA_V8_DATA') ], correctionLevels = correction_levels_data )

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
    print "MET", r.event.mets[0].pt()
    for j in r.event.jets:
        print "pt (mAOD) % 6.3f pt(Uncorr) % 6.3f pT recorr(new) % 6.3f pT recorr(old) % 6.3f" %( 
                j.pt(), 
                j.correctedJet("Uncorrected").pt(),
                j.correctedJet("Uncorrected").pt()*corrector_new.correction( j.correctedJet("Uncorrected").pt(), j.eta(), j.jetArea(), r.event.rho[0], r.event.run ), 
                j.correctedJet("Uncorrected").pt()*corrector_old.correction( j.correctedJet("Uncorrected").pt(), j.eta(), j.jetArea(), r.event.rho[0], r.event.run ), 
            )
