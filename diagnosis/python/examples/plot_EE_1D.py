''' FWLite example
'''
# Standard imports
import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *

from math import atan, sin, sqrt, log , exp, tan, asin

from RootTools.core.standard import * 

small = True

collection  = 'rechits'
#texX        = "raw cluster energy"
texX        = "rechit energy"
prefix      = "origplot_goodruns"

#events_2016_MC   = Events(['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/SingleNeutrino/AODSIM/PUMoriond17_magnetOff_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/0006AA18-32B3-E611-806C-001E67DFF4F6.root'])
#events_2017_MC   = Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_3_0_pre1/RelValNuGun/GEN-SIM-RECO/PUpmx25ns_92X_upgrade2017_realistic_v7-v1/00000/14A49577-9561-E711-A501-0CC47A78A2F6.root'])
#events_2016_data = Events(['root://cms-xrd-global.cern.ch//store/data/Run2016H/ZeroBias/AOD/PromptReco-v2/000/282/037/00000/080C0CFD-7A89-E611-AC65-02163E011D59.root'])
#events_2017_data = Events(['root://cms-xrd-global.cern.ch//store/data/Run2017B/ZeroBias/AOD/PromptReco-v1/000/297/723/00000/061EEF62-E25E-E711-975D-02163E0143BC.root'])
#events_2017_MC_forECALStudies = Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_2_9/RelValNuGun/GEN-SIM-RECO/PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies-v1/00000/0002061F-E393-E711-A12C-0025905A48BA.root'])
#events_2017_noSRPF=Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_2_9/RelValQCD_FlatPt_15_3000HS_13/GEN-SIM-RECO/PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies_HS_PF16-v1/00000/00461C42-EE9C-E711-B3E3-0CC47A7C3450.root'])
#
#samples = [
#    ['2016_MC',   events_2016_MC, "2016 MC", styles.lineStyle(ROOT.kBlack)],
#    ['2016_data', events_2016_data, "2016 data", styles.lineStyle(ROOT.kBlue)],
#    ['2017_MC',   events_2017_MC, "2017 MC", styles.lineStyle(ROOT.kGreen)],
#    ['2017_data', events_2017_data, "2017 data",  styles.lineStyle(ROOT.kRed)],
#    ['2017_MC_forECALSt', events_2017_MC_forECALStudies, "2017 MC (new)", styles.lineStyle(ROOT.kMagenta)],
#]

# /ZeroBias/CMSSW_9_2_9-92X_dataRun2_2017Repro_v4_PF16rsb_RelVal_zb2017B-v1/RECO
events_ZB_Run2017B_297113_SRPFoff   = Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_2_9/ZeroBias/RECO/92X_dataRun2_2017Repro_v4_PF16rsb_RelVal_zb2017B-v1/10000/00149219-3FAE-E711-BE96-0025905B858C.root'])
events_ZB_Run2017B_297133_12Sep2017 = Events(['root://cms-xrd-global.cern.ch//store/data/Run2017B/ZeroBias/AOD/12Sep2017-v1/100000/0005EF83-EEA5-E711-A4AA-008CFA197D2C.root'])
# /ZeroBias/CMSSW_9_2_9-92X_dataRun2_2017Repro_v4_PF16rsb_RelVal_zb2017C-v1/RECO
events_ZB_Run2017C_300087_SRPFoff   = Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_2_9/ZeroBias/RECO/92X_dataRun2_2017Repro_v4_PF16rsb_RelVal_zb2017C-v1/10000/00833BED-39AE-E711-84AA-0CC47A4D7646.root'])
events_ZB_Run2017C_300087_12Sep2017 = Events(['root://cms-xrd-global.cern.ch//store/data/Run2017C/ZeroBias/AOD/12Sep2017-v1/00000/F6BA9A1D-62AA-E711-81BE-A0369FC5DF94.root'])
# /ZeroBias/CMSSW_9_2_9-92X_dataRun2_Prompt_v9_PF16rsb_RelVal_zb2017C-v1/RECO
#events_ZB_Run2017C_301480_SRPFoff    = Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_2_9/ZeroBias/RECO/92X_dataRun2_Prompt_v9_PF16rsb_RelVal_zb2017C-v1/10000/0271B00A-B2AE-E711-8991-0CC47A4D7604.root'])
#events_ZB_Run2017C_301480_PromptReco = Events(['root://cms-xrd-global.cern.ch//store/data/Run2017C/ZeroBias/AOD/PromptReco-v3/000/301/480/00000/3EBF21B7-D187-E711-BCB8-02163E0129B4.root'])
# /ZeroBias/CMSSW_9_2_9-92X_dataRun2_Prompt_v9_PF16rsb_RelVal_zb2017E-v1/RECO
events_ZB_Run2017E_304292_SRPFoff    = Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_2_9/ZeroBias/RECO/92X_dataRun2_Prompt_v9_PF16rsb_RelVal_zb2017E-v1/10000/00180AFD-07AE-E711-AC97-0025905B8562.root'])
events_ZB_Run2017E_304292_PromptReco = Events(['root://cms-xrd-global.cern.ch//store/data/Run2017E/ZeroBias/AOD/PromptReco-v1/000/304/292/00000/00BD7574-B5AA-E711-A4C0-02163E01A24F.root'])
samples = [
    [ 'B_297133_SRoff', events_ZB_Run2017B_297113_SRPFoff   , 'B 297133 SR@PF off', styles.lineStyle(ROOT.kBlue, dashed = False)], 
    [ 'B_297133_Ref'  , events_ZB_Run2017B_297133_12Sep2017 , 'B 297133 12Sep2017', styles.lineStyle(ROOT.kBlue, dashed = True)], 
    [ 'C_300087_SRoff', events_ZB_Run2017C_300087_SRPFoff   , 'C 300087 SR@PF off', styles.lineStyle(ROOT.kRed, dashed = False)], 
    [ 'C_300087_Ref',   events_ZB_Run2017C_300087_12Sep2017 , 'C 300087 12Sep2017', styles.lineStyle(ROOT.kRed, dashed = True)], 
#    [ 'C_301480_SRoff', events_ZB_Run2017C_301480_SRPFoff   , 'C 301480 SR@PF off', styles.lineStyle(ROOT.kGreen, dashed = False)], 
#    [ 'C_301480_Ref',   events_ZB_Run2017C_301480_PromptReco, 'C 301480 PromptReco',styles.lineStyle(ROOT.kGreen, dashed = True)], 
    [ 'E_304292_SRoff', events_ZB_Run2017E_304292_SRPFoff   , 'E 304292 SR@PF off', styles.lineStyle(ROOT.kMagenta, dashed = False)], 
    [ 'E_304292_Ref',   events_ZB_Run2017E_304292_PromptReco, 'E 304292 PromptReco',styles.lineStyle(ROOT.kMagenta, dashed = True)], 
]

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
elif collection.endswith('pfclusters'):
    edmCollections = { 
    'pfclusters':{'type':'vector<reco::PFCluster>', 'label': ("particleFlowClusterECAL" )}
    }

theta_max = 2*atan(exp(-1.479))
h={}

for name, events, legendText, style in samples:

    print "At", name

    # add handles
    for k, v in edmCollections.iteritems():
        v['handle'] = Handle(v['type'])

    nevents = 1000 if small else events.size()

    if collection.startswith('ph'): 
        h[name] = ROOT.TH1F("gamma","gamma",50,0,50)
    else:
        h[name] = ROOT.TH1F("gamma","gamma",40,0,20)

    h[name].style = style
    h[name].legendText = legendText

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
        #elif collection == 'pfclusters':
        #    break

    print "Counter", i
#
histos = [[h[x[0]]] for x in samples]
p = Plot.fromHisto(prefix+'_'+collection, histos=histos, texX = texX) 

plotting.draw(
    p, 
    plot_directory = "/afs/hephy.at/user/r/rschoefbeck/www/etc/",
)
