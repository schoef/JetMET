''' FWLite example
'''
# Standard imports
import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *

small = True

# example file
#events = Events(['root://cms-xrd-global.cern.ch//store/mc/RunIIFall17MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/100000/5E223529-88AE-E811-994D-001E67792872.root'])
events = Events(['root://cms-xrd-global.cern.ch//store/data/Run2018B/DoubleMuon/MINIAOD/26Sep2018-v1/110000/9CBB049D-FFA1-4C46-B593-53EDC16344EF.root'])

#vector<CTPPSLocalTrackLite>           "ctppsLocalTrackLiteProducer"   ""                "RECO"    

# RECO
edmCollections = { 
'lt':{'type':'vector<CTPPSLocalTrackLite>', 'label': ( "ctppsLocalTrackLiteProducer" ) },
   }

# add handles
for k, v in edmCollections.iteritems():
    v['handle'] = Handle(v['type'])

nevents = 1 if small else events.size()

for i in range(nevents):
  events.to(i)

  eaux  = events.eventAuxiliary()

  # run/lumi/event
  run   = eaux.run()
  event = eaux.event()
  lumi  = eaux.luminosityBlock()

  #read all products as specifed in edmCollections
  products = {}
  for k, v in edmCollections.iteritems():
    events.getByLabel(v['label'], v['handle'])
    products[k] = v['handle'].product()

  print run,lumi,event
  print products['lt'].size()
  for lt in products['lt']:
    print lt 


#  #print RecHits
#  for i, cl in enumerate(products["clusterHCAL"]):
#    print "cluster   n %i E %3.2f"%(i, cl.energy())
#  #for i, rh in enumerate(products["caloRecHits"]):
#  #  print "caloRechit n %i E %3.2f"%(i, rh.energy())
