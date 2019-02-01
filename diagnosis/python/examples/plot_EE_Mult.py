''' FWLite example
'''
# Standard imports
import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *

from math import atan, sin, sqrt, log , exp, tan, asin

from RootTools.core.standard import * 

from JetMET.tools.helpers import deltaR

small = True

collection='pfclusters'

#2016 MC
#events_2016_MC   = Events(['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16DR80Premix/SingleNeutrino/AODSIM/PUMoriond17_magnetOff_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/0006AA18-32B3-E611-806C-001E67DFF4F6.root'])
#events_2017_MC   = Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_3_0_pre1/RelValNuGun/GEN-SIM-RECO/PUpmx25ns_92X_upgrade2017_realistic_v7-v1/00000/14A49577-9561-E711-A501-0CC47A78A2F6.root'])
#events_2016_data = Events(['root://cms-xrd-global.cern.ch//store/data/Run2016H/ZeroBias/AOD/PromptReco-v2/000/282/037/00000/080C0CFD-7A89-E611-AC65-02163E011D59.root'])
#events_2017_data = Events(['root://cms-xrd-global.cern.ch//store/data/Run2017B/ZeroBias/AOD/PromptReco-v1/000/297/723/00000/061EEF62-E25E-E711-975D-02163E0143BC.root'])
#events_2017_MC_forECALStudies = Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_2_9/RelValNuGun/GEN-SIM-RECO/PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies-v1/00000/0002061F-E393-E711-A12C-0025905A48BA.root'])
#events_2017_noSRPF=Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_2_9/RelValQCD_FlatPt_15_3000HS_13/GEN-SIM-RECO/PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies_HS_PF16-v1/00000/00461C42-EE9C-E711-B3E3-0CC47A7C3450.root'])
# RECO

#v2 GT and SR@PF on, PU
events_2017_v2_SRPFon_noPU  = Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_2_9/RelValQCD_FlatPt_15_3000HS_13UP17/GEN-SIM-RECO/92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF16-v1/00000/00A4CEC6-069F-E711-9A14-0CC47A745282.root'])
events_2017_v2_SRPFoff_noPU = Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_2_9/RelValQCD_FlatPt_15_3000HS_13UP17/GEN-SIM-RECO/92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF17-v1/00000/001CC2F1-C19D-E711-B63B-0CC47A7C346E.root'])
events_2017_v2_SRPFon_PU  = Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_2_9/RelValQCD_FlatPt_15_3000HS_13UP17/GEN-SIM-RECO/PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF16-v1/00000/00980477-5E9F-E711-BAEF-0242AC130002.root'])
events_2017_v2_SRPFoff_PU = Events(['root://cms-xrd-global.cern.ch//store/relval/CMSSW_9_2_9/RelValQCD_FlatPt_15_3000HS_13UP17/GEN-SIM-RECO/PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF17-v1/00000/00400DF5-819D-E711-A980-E0071B7A18F0.root'])

if collection.endswith('pfclusters'):
    edmCollections = { 
    'pfclusters':{'type':'vector<reco::PFCluster>', 'label': ("particleFlowClusterECAL" )},
    'jets':{'type':'vector<reco::PFJet>', 'label': ("ak4PFJetsCHS" )}
    }

theta_max = 2*atan(exp(-1.479))
h={}
p={}

for name, events in [ 
    ['2017_MC_v2_SRPFoff_noPU', events_2017_v2_SRPFoff_noPU],
    ['2017_MC_v2_SRPFon_noPU', events_2017_v2_SRPFon_noPU],
    ['2017_MC_v2_SRPFoff_PU', events_2017_v2_SRPFoff_PU],
    ['2017_MC_v2_SRPFon_PU', events_2017_v2_SRPFon_PU],
    ]:

    print "At", name

    # add handles
    for k, v in edmCollections.iteritems():
        v['handle'] = Handle(v['type'])

    nevents = 1000 if small else events.size()

    h[name] = ROOT.TH2F("nhits","nhits",60,-3,3,20,0,20)
    p[name] = ROOT.TProfile("nhits","nhits",60,-3,3)

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

        jets = [{'eta':j.eta(), 'phi':j.phi()} for j in products['jets'] if j.pt()>15] 
 
        for c in products[collection]:
            if min([999]+[deltaR({'eta':c.eta(),'phi':c.phi()}, j) for j in jets])<0.4:
                h[name].Fill(c.eta(), c.hitsAndFractions().size())
                p[name].Fill(c.eta(), c.hitsAndFractions().size())

    ROOT.gStyle.SetOptStat(0)
    c1 = ROOT.TCanvas()
    h[name].Draw('COLZ')
    c1.SetLogz()
    h[name].GetXaxis().SetTitle("pf cluster #eta")
    h[name].GetYaxis().SetTitle("rechit multiplicity")
    p[name].Draw('same')
    p[name].SetLineColor(ROOT.kRed)
    p[name].SetMarkerColor(ROOT.kRed)
    
    c1.Print('/afs/hephy.at/user/r/rschoefbeck/www/etc/pfclusters_matched_'+name+'.png') 
    del c1
 
#h['2016_MC'].legendText = "2016 MC"
#h['2016_MC'].style = styles.lineStyle(ROOT.kBlack)
#h['2016_data'].legendText = "2016 data"
#h['2016_data'].style = styles.lineStyle(ROOT.kBlue)
#h['2017_MC'].legendText = "2017 MC"
#h['2017_MC'].style = styles.lineStyle(ROOT.kGreen)
#h['2017_data'].legendText = "2017 data"
#h['2017_data'].style = styles.lineStyle(ROOT.kRed)
#h['2017_MC_forECALSt'].legendText = "2017 MC (new)"
#h['2017_MC_forECALSt'].style = styles.lineStyle(ROOT.kMagenta)
##h['2017_MC_noSRPF'].legendText = "2017 MC (noSRPF)"
##h['2017_MC_noSRPF'].style = styles.lineStyle(ROOT.kBlue)
#
#histos = [[h[x]] for x in ['2016_MC','2016_data','2017_MC','2017_data', '2017_MC_forECALSt']]
##histos = [[h[x]] for x in ['2017_MC','2017_data', '2017_MC_noSRPF']]
#p = Plot.fromHisto(collection, histos=histos, texX = "PF rechit energy") 
#
#plotting.draw(
#    p, 
#    plot_directory = "/afs/hephy.at/user/r/rschoefbeck/www/etc/",
#)
