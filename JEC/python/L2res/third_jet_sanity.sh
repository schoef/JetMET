#!/bin/sh

python third_jet_sanity.py $@ --pt low  --sample Run2016H &
python third_jet_sanity.py $@ --pt high --sample Run2016H &
python third_jet_sanity.py $@ --pt low  --sample QCD_Pt &
python third_jet_sanity.py $@ --pt high --sample QCD_Pt &
