''' Study PU in 2018 
'''
# Standard imports
import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *

small = False

events = Events(['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/80000/7C0E1EEF-9780-9841-98AD-8C40A5515234.root'])

# Use 'edmDumpEventContent <file>' to list all products. Then, make a simple dictinary as below for the products you want to read.
# These are the PF rechit collections:
#vector<reco::PFRecHit>                "particleFlowRecHitECAL"    "Cleaned"         "reRECO"   
#vector<reco::PFRecHit>                "particleFlowRecHitHBHE"    "Cleaned"         "reRECO"   
#vector<reco::PFRecHit>                "particleFlowRecHitHF"      "Cleaned"         "reRECO"   
#vector<reco::PFRecHit>                "particleFlowRecHitHO"      "Cleaned"         "reRECO"   
#vector<reco::PFRecHit>                "particleFlowRecHitPS"      "Cleaned"         "reRECO" 

# miniAOD
edmCollections = {

    'fixedGridRhoAll':                          {'read':'ana','type':'double', 'label': ("fixedGridRhoAll", "", "RECO")},
    'fixedGridRhoFastjetAll':                   {'read':'ana','type':'double', 'label': ("fixedGridRhoFastjetAll", "", "RECO")},
    'fixedGridRhoFastjetAllCalo':               {'read':'ana','type':'double', 'label': ("fixedGridRhoFastjetAllCalo", "", "RECO")},
    'fixedGridRhoFastjetCentral':               {'read':'ana','type':'double', 'label': ("fixedGridRhoFastjetCentral", "", "RECO")},
    'fixedGridRhoFastjetCentralCalo':           {'read':'ana','type':'double', 'label': ("fixedGridRhoFastjetCentralCalo", "", "RECO")},
    'fixedGridRhoFastjetCentralChargedPileUp':  {'read':'ana','type':'double', 'label': ("fixedGridRhoFastjetCentralChargedPileUp", "", "RECO")},
    'fixedGridRhoFastjetCentralNeutral':        {'read':'ana','type':'double', 'label': ("fixedGridRhoFastjetCentralNeutral", "", "RECO")},
    'met':                                      {'read':'sel','type':'vector<pat::MET>', 'label': ("slimmedMETs", "", "PAT")},
    'pf':                                       {'read':'ana','type':'vector<pat::PackedCandidate>', 'label': ("packedPFCandidates", "", "PAT")},
    'muon':                                     {'read':'sel','type':'vector<pat::Muon>', 'label': ("slimmedMuons", "", "PAT")},

}

# add handles
for k, v in edmCollections.iteritems():
    v['handle'] = Handle(v['type'])

nevents = 1 if small else events.size()

def relIso03( p ):
    # https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/muons_cff.py#L112
    return (p.pfIsolationR03().sumChargedHadronPt + max(p.pfIsolationR03().sumNeutralHadronEt + p.pfIsolationR03().sumPhotonEt - p.pfIsolationR03().sumPUPt/2,0.0))/p.pt()

for i in range(nevents):

    if i%1000==0: print "At %i/%i" %( i, nevents )
    events.to(i)
  
    eaux  = events.eventAuxiliary()
  
    # run/lumi/event
    run   = eaux.run()
    event = eaux.event()
    lumi  = eaux.luminosityBlock()
  
    #read th products needed for event selection 
    products = {}
    for k, v in edmCollections.iteritems():
        if v['read']!='sel': continue
        events.getByLabel(v['label'], v['handle'])
        products[k] = v['handle'].product()

    # event selection  
    #if products['met'][0].pt()<=100: continue 

    muons = filter( lambda p:p.pt()>15 and abs(p.eta())<2.4 and p.CutBasedIdMedium and relIso03(p)<0.2, products['muon'] )
  
    if len(muons)<2: continue

    # read all the rest
    for k, v in edmCollections.iteritems():
        if v['read']=='ana': continue
        events.getByLabel(v['label'], v['handle'])
        products[k] = v['handle'].product()

    break



#  #print RecHits
#  for i, cl in enumerate(products["clusterHCAL"]):
#    print "cluster   n %i E %3.2f"%(i, cl.energy())
#  #for i, rh in enumerate(products["caloRecHits"]):
#  #  print "caloRechit n %i E %3.2f"%(i, rh.energy())
