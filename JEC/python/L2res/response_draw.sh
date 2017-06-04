#!/bin/sh
#python response_draw.py  --ptBinningVar=tag --era=Run2016 --triggers=PFJet
#python response_draw.py  --ptBinningVar=tag --era=Run2016 --triggers=DiPFJetAve_HFJEC
#python response_draw.py  --ptBinningVar=tag --era=Run2016 --triggers=DiPFJetAve
#python response_draw.py  --ptBinningVar=tag --era=Run2016BCD --triggers=PFJet
#python response_draw.py  --ptBinningVar=tag --era=Run2016BCD --triggers=DiPFJetAve_HFJEC
#python response_draw.py  --ptBinningVar=tag --era=Run2016BCD --triggers=DiPFJetAve
#python response_draw.py  --ptBinningVar=tag --era=Run2016EFearly --triggers=PFJet
#python response_draw.py  --ptBinningVar=tag --era=Run2016EFearly --triggers=DiPFJetAve_HFJEC
#python response_draw.py  --ptBinningVar=tag --era=Run2016EFearly --triggers=DiPFJetAve
#python response_draw.py  --ptBinningVar=tag --era=Run2016FlateG --triggers=PFJet
#python response_draw.py  --ptBinningVar=tag --era=Run2016FlateG --triggers=DiPFJetAve_HFJEC
#python response_draw.py  --ptBinningVar=tag --era=Run2016FlateG --triggers=DiPFJetAve
#python response_draw.py  --ptBinningVar=tag --era=Run2016H --triggers=PFJet
#python response_draw.py  --ptBinningVar=tag --era=Run2016H --triggers=DiPFJetAve_HFJEC
#python response_draw.py  --ptBinningVar=tag --era=Run2016H --triggers=DiPFJetAve

python response_draw.py --cleaned --era=Run2016 --triggers=PFJet &
python response_draw.py --cleaned --era=Run2016BCD --triggers=PFJet &
python response_draw.py --cleaned --era=Run2016EFearly --triggers=PFJet &
python response_draw.py --cleaned --era=Run2016FlateG --triggers=PFJet &
python response_draw.py --cleaned --era=Run2016H --triggers=PFJet &

python response_draw.py --cleaned --era=Run2016 --triggers=DiPFJetAve &
python response_draw.py --cleaned --era=Run2016BCD --triggers=DiPFJetAve &
python response_draw.py --cleaned --era=Run2016FlateG --triggers=DiPFJetAve &
python response_draw.py --cleaned --era=Run2016EFearly --triggers=DiPFJetAve &
python response_draw.py --cleaned --era=Run2016H --triggers=DiPFJetAve &

python response_draw.py --cleaned --era=Run2016 --triggers=DiPFJetAve_HFJEC &
python response_draw.py --cleaned --era=Run2016BCD --triggers=DiPFJetAve_HFJEC &
python response_draw.py --cleaned --era=Run2016EFearly --triggers=DiPFJetAve_HFJEC &
python response_draw.py --cleaned --era=Run2016FlateG --triggers=DiPFJetAve_HFJEC &
python response_draw.py --cleaned --era=Run2016H --triggers=DiPFJetAve_HFJEC &

#python response_draw.py  --era=Run2016 --triggers=PFJet &
#python response_draw.py  --era=Run2016BCD --triggers=PFJet &
#python response_draw.py  --era=Run2016FlateG --triggers=PFJet &
#python response_draw.py  --era=Run2016H --triggers=PFJet &
#python response_draw.py  --era=Run2016EFearly --triggers=PFJet &

#python response_draw.py  --era=Run2016 --triggers=PFJet --phEF=0.6 &
#python response_draw.py  --era=Run2016BCD --triggers=PFJet --phEF=0.6 &
#python response_draw.py  --era=Run2016FlateG --triggers=PFJet --phEF=0.6 &
#python response_draw.py  --era=Run2016H --triggers=PFJet --phEF=0.6 &
#python response_draw.py  --era=Run2016EFearly --triggers=PFJet --phEF=0.6 &

#python response_draw.py  --era=Run2016 --triggers=DiPFJetAve_HFJEC &
#python response_draw.py  --era=Run2016 --triggers=DiPFJetAve &
#python response_draw.py  --era=Run2016BCD --triggers=DiPFJetAve_HFJEC &
#python response_draw.py  --era=Run2016BCD --triggers=DiPFJetAve &
#python response_draw.py  --era=Run2016EFearly --triggers=DiPFJetAve_HFJEC &
#python response_draw.py  --era=Run2016EFearly --triggers=DiPFJetAve &
#python response_draw.py  --era=Run2016FlateG --triggers=DiPFJetAve_HFJEC &
#python response_draw.py  --era=Run2016FlateG --triggers=DiPFJetAve &
#python response_draw.py  --era=Run2016H --triggers=DiPFJetAve_HFJEC &
#python response_draw.py  --era=Run2016H --triggers=DiPFJetAve &
