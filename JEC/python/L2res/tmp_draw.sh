#!/bin/sh
python response_draw.py --era=Run2016H --triggers=PFJet --phEF=0.5 &
python response_draw.py --era=Run2016H --triggers=PFJet --phEF=0.6 &
python response_draw.py --era=Run2016H --triggers=PFJet --phEF=0.7 &
python response_draw.py --era=Run2016H --triggers=PFJet --phEF=0.8 &
python response_draw.py --era=Run2016H --triggers=PFJet --phEF=0.9 &
python response_draw.py --era=Run2016H --triggers=PFJet --phEF=0.99 &

