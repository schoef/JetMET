''' FWLite example
'''
# Standard imports
import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *

from math import atan, sin, sqrt, log , exp, tan, asin

from RootTools.core.standard import * 

small = True

collection='pfrechits'

#2016 MC
events_2016_MC   = Events(['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/SingleNeutrino/AODSIM/PUMoriond17_magnetOff_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/0006AA18-32B3-E611-806C-001E67DFF4F6.root'])
events_2017_MC   = Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_3_0_pre1/RelValNuGun/GEN-SIM-RECO/PUpmx25ns_92X_upgrade2017_realistic_v7-v1/00000/14A49577-9561-E711-A501-0CC47A78A2F6.root'])
events_2016_data = Events(['root://cms-xrd-global.cern.ch//store/data/Run2016H/ZeroBias/AOD/PromptReco-v2/000/282/037/00000/080C0CFD-7A89-E611-AC65-02163E011D59.root'])
events_2017_data = Events(['root://cms-xrd-global.cern.ch//store/data/Run2017B/ZeroBias/AOD/PromptReco-v1/000/297/723/00000/061EEF62-E25E-E711-975D-02163E0143BC.root'])
events_2017_MC_forECALStudies = Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_2_9/RelValNuGun/GEN-SIM-RECO/PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies-v1/00000/0002061F-E393-E711-A12C-0025905A48BA.root'])
events_2017_noSRPF=Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_2_9/RelValQCD_FlatPt_15_3000HS_13/GEN-SIM-RECO/PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies_HS_PF16-v1/00000/00461C42-EE9C-E711-B3E3-0CC47A7C3450.root'])
# RECO

if collection.startswith('ph'):
    edmCollections = { 
        'pf': { 'label': ( "particleFlow"), 'type':"vector<reco::PFCandidate>" },
       }
elif collection.endswith('pfrechits'):
    edmCollections = { 
    'pfrechits':{'type':'vector<reco::PFRecHit> ', 'label': ("particleFlowRecHitECAL", "Cleaned", "RECO") }
       }
elif collection.endswith('rechits'):
    edmCollections = { 
    'rechits':{'label':('reducedEcalRecHitsEE'), 'type':'edm::SortedCollection<EcalRecHit,edm::StrictWeakOrdering<EcalRecHit> >' },    
       }

theta_max = 2*atan(exp(-1.479))
h={}

for name, events in [ 
    ['2016_MC',   events_2016_MC],
    ['2016_data', events_2016_data],
    ['2017_MC',   events_2017_MC],
    ['2017_data', events_2017_data],
    ['2017_MC_forECALSt', events_2017_MC_forECALStudies],
#    ['2017_MC_noSRPF', events_2017_noSRPF],
    ]:

    print "At", name

    # add handles
    for k, v in edmCollections.iteritems():
        v['handle'] = Handle(v['type'])

    nevents = 1000 if small else events.size()

    if collection.startswith('ph'): 
        h[name] = ROOT.TH1F("gamma","gamma",50,0,50)
    else:
        h[name] = ROOT.TH1F("gamma","gamma",40,0,20)

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
        
        if collection.startswith('ph'):
            photons = [ p for p in products['pf'] if p.pdgId()==22 ]
            #print len(filter(lambda p:abs(p.eta())>2.5, photons))
            for p in photons:
                en = p.rawEcalEnergy() if collection.endswith('raw') else p.energy()
                if abs(p.eta())>2.5:
                    h[name].Fill( en )
        elif collection == 'rechits':
            rechits = [ p for p in products[collection]  ]
            for p in rechits:
                o=ROOT.EEDetId(p.detid())

                ix = o.ix() - 50.5 # from https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/DQMOffline/JetMET/src/ECALRecHitAnalyzer.cc#L253-L255
                iy = o.iy() - 50.5

                ir    = sqrt(ix**2 + iy**2)/50.5 # normalize to 1
                theta = asin(ir*sin(theta_max))  # scale 
                eta   = -log(tan(theta/2))*o.zside() 
                if abs(eta)>2.5:
                    h[name].Fill(p.energy())
        elif collection == 'pfrechits':
            rechits = [ p for p in products[collection]  ]
            for p in rechits:
                o=ROOT.EEDetId(p.detId())

                ix = o.ix() - 50.5 # from https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/DQMOffline/JetMET/src/ECALRecHitAnalyzer.cc#L253-L255
                iy = o.iy() - 50.5

                ir    = sqrt(ix**2 + iy**2)/50.5 # normalize to 1
                theta = asin(ir*sin(theta_max))  # scale 
                eta   = -log(tan(theta/2))*o.zside() 
                if abs(eta)>2.5:
                    h[name].Fill(p.energy())

h['2016_MC'].legendText = "2016 MC"
h['2016_MC'].style = styles.lineStyle(ROOT.kBlack)
h['2016_data'].legendText = "2016 data"
h['2016_data'].style = styles.lineStyle(ROOT.kBlue)
h['2017_MC'].legendText = "2017 MC"
h['2017_MC'].style = styles.lineStyle(ROOT.kGreen)
h['2017_data'].legendText = "2017 data"
h['2017_data'].style = styles.lineStyle(ROOT.kRed)
h['2017_MC_forECALSt'].legendText = "2017 MC (new)"
h['2017_MC_forECALSt'].style = styles.lineStyle(ROOT.kMagenta)
#h['2017_MC_noSRPF'].legendText = "2017 MC (noSRPF)"
#h['2017_MC_noSRPF'].style = styles.lineStyle(ROOT.kBlue)

histos = [[h[x]] for x in ['2016_MC','2016_data','2017_MC','2017_data', '2017_MC_forECALSt']]
#histos = [[h[x]] for x in ['2017_MC','2017_data', '2017_MC_noSRPF']]
p = Plot.fromHisto(collection, histos=histos, texX = "PF rechit energy") 

plotting.draw(
    p, 
    plot_directory = "/afs/hephy.at/user/r/rschoefbeck/www/etc/",
)
