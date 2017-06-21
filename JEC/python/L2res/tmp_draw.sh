#!/bin/sh

python make_L2res_results.py --alpha=0.30 --useFit --cleaned --era=Run2016H --triggers=DiPFJetAve & 
python make_L2res_results.py --alpha=0.30 --useFit --jer jer --cleaned --era=Run2016H --triggers=DiPFJetAve &
