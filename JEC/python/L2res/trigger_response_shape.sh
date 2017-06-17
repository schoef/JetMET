#!/bin/sh
python trigger_response_shape.py $@ --variable A --trigger=PFJet --era  Run2016H &
python trigger_response_shape.py $@ --variable A --trigger=DiPFJetAve --era  Run2016H &
python trigger_response_shape.py $@ --variable A --trigger=DiPFJetAve_HFJEC --era  Run2016H &
python trigger_response_shape.py $@ --variable B --trigger=PFJet --era  Run2016H &
python trigger_response_shape.py $@ --variable B --trigger=DiPFJetAve --era  Run2016H &
python trigger_response_shape.py $@ --variable B --trigger=DiPFJetAve_HFJEC --era  Run2016H &
