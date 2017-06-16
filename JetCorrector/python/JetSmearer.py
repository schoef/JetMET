''' JEC on the fly
'''
# Standard imports
import os
import tarfile
import ROOT
import bisect
import random 
from math import sqrt

# Logging

import logging
logger = logging.getLogger(__name__)

from JetMET.tools.helpers import wget

class JetSmearer:

    data_directory   = "$CMSSW_BASE/src/JetMET/JetCorrector/data/jer"
    downloadurl      = "https://raw.githubusercontent.com/cms-jet/JRDatabase/master/textFiles"

    parametrization = "{1 JetEta 0 None ScaleFactor}"

    def __init__( self, era, flavor ):

        # Resolution
        res_filename = "%s_PtResolution_%s.txt" % ( era, flavor ) 
        res_txtfile  = os.path.expandvars( os.path.join( self.data_directory, res_filename ) )

        # Scale factor
        sf_filename = "%s_SF_%s.txt" % ( era, flavor ) 
        sf_txtfile  = os.path.expandvars( os.path.join( self.data_directory, sf_filename ) )

        # Do we have the txt files?
        if not os.path.exists( res_txtfile ):
            logger.info( "Resolution txt file %s not found.", res_txtfile )
            source = self.downloadurl+'/%s/%s' % ( era, res_filename )
            logger.info( "Downloading from %s.", source )
            wget( source, res_txtfile )
        if not os.path.exists( sf_txtfile ):
            logger.info( "SF txt file %s not found.", sf_txtfile )
            source = self.downloadurl+'/%s/%s' % ( era, sf_filename )
            logger.info( "Downloading from %s.", source )
            wget( source, sf_txtfile )

        self.sf_data = []

        # read the SF file. 
        self.read_SF_txtfile(   sf_txtfile )
        # load resolution file and make jet resolution object
        self.make_resolution_object( res_txtfile )
    
    def make_resolution_object( self, txtfile ):
        try:
            self.resolution_object = ROOT.JME.JetResolutionObject( txtfile )
        except TypeError:
            logger.warning( "Problem with %s", txtfile )
            raise TypeError

        self.p                 = ROOT.JME.JetParameters()

    def get_jet_resolution( self, pt, eta, rho ):
        ''' Evaluate JER for a jet. Return None if outside the boundaries defined by the txt file
        '''
        self.p.setJetPt( pt )
        self.p.setJetEta( eta )
        self.p.setRho( rho )
        record = self.resolution_object.getRecord(self.p)
        if record: return self.resolution_object.evaluateFormula( record, self.p )

    def read_SF_txtfile( self, txtfile ):
        ''' Read manually the txt file for SF. Didn't work with the JetResolutionObject
            Only supports ( & checks) single variable eta binning. 
            Returns boundary value if outside boundary.
        '''

        with open( txtfile ) as f:
            content = [l.strip() for l in f.readlines()]
            if not content[0] == self.parametrization:
                raise NotImplementedError( "JER SF file %s does not start with '%s' but with '%s'" % ( txtfile, self.parametrization, content[0] ) )
            for line in content[1:]:
                eta_min, eta_max, nn , sf, sf_low, sf_high = map( float, line.split() )  
                self.sf_data.append( [ eta_min, eta_max, sf, sf_low, sf_high] )

            logger.debug( "Loaded %i SF from file %s", len(self.sf_data), txtfile )

            self.eta_thresholds = [ c[0] for c in self.sf_data[1:] ] 
    
    def get_SF(self, eta):
        ''' Evaluate the JER SF
        '''
        n = bisect.bisect_left( self.eta_thresholds, eta )
        return self.sf_data[n][2:]

    def scaling_correction( self, pt, mcPt, eta, rho):
        ''' Get JER varied pt values according to the scaling recipe
        '''
        jer = self.get_jet_resolution( pt, eta, rho )
        sf  = self.get_SF( eta )
        if jer is not None and abs(pt-mcPt) < 3*pt*jer:
            return self.__scaling_correction( pt, mcPt, sf )
        else:
            return [ 1 for s in sf ]

    @staticmethod
    def __scaling_correction( pt, mcPt, sf) :
        return [ max(0, 1 + (s - 1)*(1 - mcPt/(1.0*pt))) for s in sf ]

    def stochastic_correction( self, pt, eta, rho ):
        ''' Get JER varied pt values according to the stochastic recipe
        '''
        jer  = self.get_jet_resolution( pt, eta, rho )
        sf   = self.get_SF( eta )
        return self.__stochastic_correction( pt, jer, sf )

    @staticmethod
    def __stochastic_correction( pt, jer, sf ):
        if jer is not None: 
            rand = random.gauss(0, jer)
            return [ (1 + rand*sqrt(max(0, s**2 - 1))) for s in sf ] 
        else:
            return [ 1 for s in sf ]

    def hybrid_correction( self, pt, mcPt, eta, rho ):
        ''' Get JER varied pt values according to the hybrid recipe
        '''
        jer  = self.get_jet_resolution( pt, eta, rho )
        sf   = self.get_SF( eta )

        #logger.debug( "Jet pt %3.2f mcPt %3.2f, eta %3.2f rho %3.2f. JER %4.3f SF %r", pt, mcPt, eta, rho, jer, sf )
        if jer is not None:
            if abs(pt-mcPt) < 3*pt*jer:
                #logger.debug( "Doing scaling")
                return self.__scaling_correction( pt, mcPt, sf )
            else:
                #logger.debug( "Doing stochastic")
                return self.__stochastic_correction( pt, jer, sf )
        else:
            return [ 1 for s in sf ]

    def delete( self ):
        ''' I don't know why this is needed and why it needs to be called before exit.
            Destructur segfaults on exit. Doing nothing segfaults on exit.
        '''
        if self.resolution_object: self.resolution_object.__destruct__()
