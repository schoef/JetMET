''' FWLiteReader example: Loop over a sample and write some data to a histogram.
'''
# Standard imports
import os
import logging
import ROOT
import array

#RootTools
from RootTools.core.standard import *

#Helper
import JetMET.tools.helpers as helpers

# argParser
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel', 
      action='store',
      nargs='?',
      choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'],
      default='INFO',
      help="Log level for logging"
)

args = argParser.parse_args()
logger = get_logger(args.logLevel, logFile = None)

max_events = -1
max_files = -1 


#prefix = 'EE_2017_ZeroN' 
###1M, v2 GT and SR@PF on, PU
#sample    = FWLiteSample.fromDAS( 'SRPFon PU', '/RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF17-v1/MINIAODSIM', maxN = max_files, dbFile = None) 
## v2 GT, SR@PF on, PU, ZeroN
#sample_ZN = FWLiteSample.fromDAS( 'SRPFon PU ZN', '/RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-PUpmx25ns_92X_upgrade2017_realistic_forECALStudies_rms0p2887_HS1M_PF17-v1/MINIAODSIM', maxN = max_files, dbFile = None)


prefix = 'EE_2017_ZeroN_NoPU_SRPFoff' 
##1M, v2 GT and SR@PF off,no PU
sample    = FWLiteSample.fromDAS( 'SRPFOff noPU',    '/RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-92X_upgrade2017_realistic_Candidate_forECALStudies_HS1M_PF16-v1/MINIAODSIM', maxN = max_files, dbFile = None )
# v2 GT, SR@PF off, no PU, ZeroN
sample_ZN = FWLiteSample.fromDAS( 'SRPFOff noPU ZN', '/RelValQCD_FlatPt_15_3000HS_13UP17/CMSSW_9_2_9-92X_upgrade2017_realistic_forECALStudies_rms0p2887_HS1M_PF16-v1/MINIAODSIM', maxN = max_files, dbFile = None )

samples = [sample, sample_ZN]

# define TProfiles
pt_bins      = [ (15,20), (40,50), (100,120) ]  
abs_eta_bins = [ (0,1.3), (1.3,2), (2,2.5), (2.5, 2.75), (2.75,3) ]
colors       = [ ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kMagenta ]

njet = {}
for s in samples:
    njet[s.name] = {} 
    for i_abs_eta_bin, abs_eta_bin in enumerate(abs_eta_bins):
        njet[s.name][abs_eta_bin] = {} 
        for i_pt_bin, pt_bin in enumerate(pt_bins):
            njet[s.name][abs_eta_bin][pt_bin]            = ROOT.TH1D("njet", "njet", 10,0,10 )
            njet[s.name][abs_eta_bin][pt_bin].style      = styles.lineStyle(colors[i_pt_bin], dashed = (s.name==sample_ZN.name), errors = True )
            njet[s.name][abs_eta_bin][pt_bin].legendText = "%s %i #geq p_{T} < %i"% ( (s.name,) + pt_bin )

products = {
    'jets':      {'type':'vector<pat::Jet>', 'label':("slimmedJets")},
    'genInfo':   {'type':' GenEventInfoProduct', 'label': "generator"},
    }

for sample in samples:
    r1 = sample.fwliteReader( products = products )
    r1.start()
    i=0
    while r1.run():
        id_jets = [ j.correctedJet("Uncorrected") for j in r1.products['jets'] if helpers.jetID( j )]
        njet_counter={abs_eta_bin:{pt_bin:0 for pt_bin in pt_bins} for abs_eta_bin in abs_eta_bins}
        for j in id_jets:
            abseta = abs(j.eta())
            pt     = j.pt()
            for i_abs_eta_bin, abs_eta_bin in enumerate(abs_eta_bins):
                if abseta>abs_eta_bin[0] and abseta<=abs_eta_bin[1]:
                    for i_pt_bin, pt_bin in enumerate(pt_bins):
                        if pt>pt_bin[0] and pt<=pt_bin[1]:
                            njet_counter[abs_eta_bin][pt_bin] +=1

        for i_abs_eta_bin, abs_eta_bin in enumerate(abs_eta_bins):
            for i_pt_bin, pt_bin in enumerate(pt_bins):
                njet[sample.name][abs_eta_bin][pt_bin].Fill( njet_counter[abs_eta_bin][pt_bin] )

        i+=1
        if max_events>0 and i>max_events: break

for i_abs_eta_bin, abs_eta_bin in enumerate(abs_eta_bins):
    histos  = sum( [ [ njet[sample.name][abs_eta_bin][pt_bin] for sample in samples] for  pt_bin in pt_bins], [])
    histos  = [[h] for h in histos ] 
    postfix = ("_max_events_%s_"%max_events if max_events is not None and max_events>0 else "")
    njetPlot = Plot.fromHisto( name = "njet"+postfix+"_abseta_%3.2f_%3.2f"%abs_eta_bin, histos = histos, texX = "number of jets" , texY = "Number of Events" )
    plotting.draw(njetPlot, plot_directory = "/afs/hephy.at/user/r/rschoefbeck/www/%s/"%prefix, ratio = None, logY = True, logX = False, legend = ( [0.15,0.92-0.05*len(pt_bins),0.92,0.88],len(samples)))
