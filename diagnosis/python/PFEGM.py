''' FWLite example
'''
# Standard imports
import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *

from math import atan, sin, sqrt, log , exp, tan, asin

small = True

collection='rechits'

#2016 MC
events = Events(['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/SingleNeutrino/AODSIM/PUMoriond17_magnetOff_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/0006AA18-32B3-E611-806C-001E67DFF4F6.root'])
filename = "MC_%s_2016"%collection

#2017MC
#events = Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_3_0_pre1/RelValNuGun/GEN-SIM-RECO/PUpmx25ns_92X_upgrade2017_realistic_v7-v1/00000/14A49577-9561-E711-A501-0CC47A78A2F6.root'])
#filename = "MC_%s_2017"%collection

#2016 data
#events = Events(['root://cms-xrd-global.cern.ch//store/data/Run2016H/ZeroBias/AOD/PromptReco-v2/000/282/037/00000/080C0CFD-7A89-E611-AC65-02163E011D59.root'])
#filename = "Data_%s_2016"%collection

#2017 data
#events = Events(['root://cms-xrd-global.cern.ch//store/data/Run2017B/ZeroBias/AOD/PromptReco-v1/000/297/723/00000/061EEF62-E25E-E711-975D-02163E0143BC.root'])
#filename = "Data_%s_2017"%collection

# RECO
edmCollections = { 
    'pf': { 'label': ( "particleFlow"), 'type':"vector<reco::PFCandidate>" },
#    'rechits':{ 'label':("particleFlowRecHitECAL","Cleaned","RECO"), 'type':'vector<reco::PFRecHit>'},
    'rechits':{'label':('reducedEcalRecHitsEE'), 'type':'edm::SortedCollection<EcalRecHit,edm::StrictWeakOrdering<EcalRecHit> >' },    

   }

# add handles
for k, v in edmCollections.iteritems():
    v['handle'] = Handle(v['type'])

theta_max = 2*atan(exp(-1.479))
nevents = 1000 if small else events.size()

h = ROOT.TH2F("gamma","gamma",104,-5.2,5.2,50,0,25)


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
    
    if collection=='ph':
        photons = [ p for p in products['pf'] if p.pdgId()==22 ]
        for p in photons:
            h.Fill( p.eta(), p.energy() )
    elif collection=='rechits':
        rechits = [ p for p in products['rechits']  ]
        for p in rechits:
            o=ROOT.EEDetId(p.detid())

            ix = o.ix() - 50.5 # from https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/DQMOffline/JetMET/src/ECALRecHitAnalyzer.cc#L253-L255
            iy = o.iy() - 50.5

            ir    = sqrt(ix**2 + iy**2)/50.5 # normalize to 1
            theta = asin(ir*sin(theta_max))  # scale 
            eta   = -log(tan(theta/2))*o.zside() 

            h.Fill( eta, p.energy() )


c1 = ROOT.TCanvas()
h.Draw('COLZ')
c1.SetLogz()
c1.Print('/afs/hephy.at/user/r/rschoefbeck/www/etc/%s.png'%filename)
