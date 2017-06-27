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
        if jer is not None and mcPt>0 and abs(pt-mcPt) < 3*pt*jer:
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
            return [ (1 + rand*sqrt(max(0, s**2 - 1))) for s in sf ] #FIXME No protection against negative numbers 
        else:
            return [ 1 for s in sf ]

    def hybrid_correction( self, pt, mcPt, eta, rho ):
        ''' Get JER varied pt values according to the hybrid recipe
        '''
        jer  = self.get_jet_resolution( pt, eta, rho )
        sf   = self.get_SF( eta )

        #logger.debug( "Jet pt %3.2f mcPt %3.2f, eta %3.2f rho %3.2f. JER %4.3f SF %r", pt, mcPt, eta, rho, jer, sf )
        if jer is not None:
            if mcPt>0 and abs(pt-mcPt) < 3*pt*jer:
                #logger.debug( "Doing scaling")
                return self.__scaling_correction( pt, mcPt, sf )
            else:
                #logger.debug( "Doing stochastic")
                return self.__stochastic_correction( pt, jer, sf )
        else:
            return [ 1 for s in sf ]

    def delete( self ):
        ''' I don't know why this is needed and why it needs to be called before exit.
            Destructur segfaults on exit. Doing nothing segfaults on exit
            in call of JME::JetResolutionObject::Definition::~Definition()
        '''
        if self.resolution_object: self.resolution_object.__destruct__()

#5  0x0000000009f7dcc0 in ?? ()
#6  0x00007fbaf3913c9c in std::__shared_count<(__gnu_cxx::_Lock_policy)2>::~__shared_count() () from /cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_26/lib/slc6_amd64_gcc530/libDataFormatsProvena
#7  0x00007fbaf314b9c5 in JME::JetResolutionObject::Definition::~Definition() () from /cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_26/lib/slc6_amd64_gcc530/libCondFormatsJetMETObjects.so
#8  0x00007fbaf314a85f in ROOT::delete_JMEcLcLJetResolutionObject(void*) () from /cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_26/lib/slc6_amd64_gcc530/libCondFormatsJetMETObjects.so
#9  0x00007fbafef12891 in TClass::Destructor(void*, bool) () from /cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw-patch/CMSSW_8_0_26_patch1/external/slc6_amd64_gcc530/lib/libCore.so
#10 0x00007fbaff6d57af in PyROOT::op_dealloc_nofree(PyROOT::ObjectProxy*) () from /cvmfs/cms.cern.ch/slc6_amd64_gcc530/lcg/root/6.06.00-ikhhed6/lib/libPyROOT.so
#11 0x00007fbaff6d5869 in PyROOT::(anonymous namespace)::op_dealloc(PyROOT::ObjectProxy*) () from /cvmfs/cms.cern.ch/slc6_amd64_gcc530/lcg/root/6.06.00-ikhhed6/lib/libPyROOT.so
#12 0x00007fbb0591b802 in subtype_dealloc (self=0x7fbaf2f262f0) at Objects/typeobject.c:1030
#13 0x00007fbb058fadcb in dict_dealloc (mp=0x7fbaf32aac58) at Objects/dictobject.c:1010
#14 0x00007fbb058c7a4a in instance_dealloc (inst=0x7fbaf2f1e2d8) at Objects/classobject.c:681
#15 0x00007fbb058fb7b7 in insertdict_by_entry (value=0x7fbb05a31a80 <_Py_NoneStruct>, ep=0x9a0ec30, hash=-4239209804666570030, key=0x7fbaff74e1b0, mp=0x7fbb057cf168) at Objects/dictobject.c:519
#16 insertdict (mp=0x7fbb057cf168, key=0x7fbaff74e1b0, hash=-4239209804666570030, value=0x7fbb05a31a80 <_Py_NoneStruct>) at Objects/dictobject.c:556
#17 0x00007fbb058fd147 in dict_set_item_by_hash_or_entry (ep=0x0, value=0x7fbb05a31a80 <_Py_NoneStruct>, hash=<optimized out>, key=<optimized out>, op=0x7fbb057cf168) at Objects/dictobject.c:765
#18 PyDict_SetItem (op=opentry=0x7fbb057cf168, key=<optimized out>, value=valueentry=0x7fbb05a31a80 <_Py_NoneStruct>) at Objects/dictobject.c:818
#19 0x00007fbb05901324 in _PyModule_Clear (m=<optimized out>) at Objects/moduleobject.c:139
#20 0x00007fbb05982263 in PyImport_Cleanup () at Python/import.c:477
#21 0x00007fbb05993bfe in Py_Finalize () at Python/pythonrun.c:458
#22 0x00007fbb059aa01f in Py_Main (argc=<optimized out>, argv=<optimized out>) at Modules/main.c:665
#23 0x00000036f181ed1d in __libc_start_main () from /lib64/libc.so.6
#24 0x00000000004006b1 in _start ()
