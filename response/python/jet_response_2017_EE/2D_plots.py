# standard imports
import os
import ROOT
import uuid
import array

# RootTools
from RootTools.core.standard import *

# JetMET
from JetMET.tools.user import skim_ntuple_directory
from JetMET.tools.user import plot_directory

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
#argParser.add_argument('--small',              action='store_true', help='Run only on a small subset of the data?')#, default = True)
#argParser.add_argument('--overwrite',          action='store_true', help='overwrite?')#, default = True)
argParser.add_argument('--plot_directory',     action='store',      default='EE_2017')
args = argParser.parse_args()
 
#
# Logger
#
import JetMET.tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

# samples
from JetMET.response.jet_response_2017_EE.samples import *

# Interpret samples
sample = merged_RelValQCD_FlatPt_15_3000HS_13UP17_CMSSW_9_2_9
    
color = [ROOT.kBlue, ROOT.kBlack, ROOT.kRed, ROOT.kGreen, ROOT.kMagenta]

plot_directory = os.path.join( plot_directory, args.plot_directory + "2D")

genPt_bins = [
    (15, 20),
    (20, 30),
    (30, 40),
    (40, 50), 
    (50, -1)
]

absEta_bins = [
    (0, 1.3), 
    (1.3, 2), 
    (2, 2.5), 
    (2.5, 2.75), 
    (2.75, 3), 
]

# "GTv1_SRPFoff_NoPU", "GTv1_SRPFoff_PUpmx25ns", "GTv2_SRPFoff_NoPU", "GTv2_SRPFoff_PUpmx25ns", "GTv2_SRPFon_NoPU", "GTv2_SRPFon_PUpmx25ns"

PU_x = "NoPU"
GT_x = "GTv2"
SR_x = "SRPFoff"

PU_y = "NoPU"
GT_y = "GTv2"
SR_y = "SRPFon"

x = "%s_%s_%s" % ( GT_x, SR_x, PU_x )
y = "%s_%s_%s" % ( GT_y, SR_y, PU_y )


for var, binning1D in [\
    [ 'phEF',  [50,0,0.5] ],
    [ 'rawPt', [40,0,120] ],

        ]:
    fm = {'x':x, 'y':y, 'var':var}

    fm['var_x'] = "{x}_{var}".format(**fm)
    fm['var_y'] = "{y}_{var}".format(**fm)


    var_string = "{var_y}:{var_x}".format(**fm)
    #selectionString = "abs({x}_eta)>2.75&&abs({x}_eta)<3&&{x}_genPt>50&&{x}_genPt<100".format(**fm)
    selectionString = "abs({x}_eta)>2.75&&abs({x}_eta)<3&&{x}_phEF-{y}_phEF>-999".format(**fm)
    print repr(var_string),",", repr(selectionString)
 
    h_2D = sample.get2DHistoFromDraw( "{var_y}:{var_x}".format(**fm), binning1D*2, selectionString = selectionString ) 

    plot2D = Plot2D.fromHisto(name = "{x}_vs_{y}_{var}".format(**fm), histos = [[h_2D]], texX = "{var} for {x}".format(**fm), texY = "{var} for {y}".format(**fm) )
    plotting.draw2D(plot2D, plot_directory = plot_directory, logY = False, logX = False, logZ = True)

