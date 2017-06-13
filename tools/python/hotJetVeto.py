''' Hot jet Id based on Mikkos map sent on June 7th 2017th to 'eta/phi jet veto' 
'''
#Standard imports
import ROOT
import os
from math import pi

# helpers
from JetMET.tools.helpers import getObjFromFile

# Logging
import logging
logger = logging.getLogger(__name__)

class hotJetVeto:
    def __init__( self, filename = "$CMSSW_BASE/src/JetMET/tools/data/hotJets/hotJets.root", hot_jet_map = "h2jet", threshold = 0):

        self.hotmap = getObjFromFile( os.path.expandvars( filename ), hot_jet_map ) 
        self.threshold = 5
 
    def passVeto( self, eta, phi ):

        if abs(eta)>5.2 or abs(phi)>pi: return True

        return self.hotmap.GetBinContent( self.hotmap.FindBin( eta, phi ) ) < self.threshold 
