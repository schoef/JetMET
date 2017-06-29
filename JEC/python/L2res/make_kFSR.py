#!/usr/bin/env python
''' Analysis script for evaluating kFSR
'''
#
# Standard imports and bateh mode
#
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptFit(0)

import os
import array
import pickle
import uuid

from RootTools.core.standard             import *
from JetMET.tools.user                   import plot_directory as user_plot_directory

# Gaussian (Roo-)Fit
from JetMET.JEC.L2res.GaussianFit        import GaussianFit
from JetMET.JEC.L2res.kFSRLinearFit      import kFSRLinearFit

#
# Arguments
# 
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='DEBUG',         nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging" )
argParser.add_argument('--triggers',           action='store',      default='exclDiPFJetAveHFJEC',      nargs='?', choices=['DiPFJetAve', 'DiPFJetAve_HFJEC', 'PFJet', 'exclDiPFJetAveHFJEC', 'exclDiPFJetAve', 'exclPFJet'], help="trigger suite" )
argParser.add_argument('--era',                action='store',      default='Run2016H',      nargs='?', choices=['Run2016', 'Run2016BCD', 'Run2016EFearly', 'Run2016FlateG', 'Run2016H'], help="era" )
argParser.add_argument('--overwrite',                               action='store_true',     help='Overwrite results.pkl?', default=True)
argParser.add_argument('--input_directory',    action='store',      default='JEC/L2res_v9_cleaned',  help="subdirectory for results.pkl")
argParser.add_argument('--plot_directory',     action='store',      default='JEC/L2res_v9_cleaned/kFSR',  help="subdirectory for plots")
argParser.add_argument('--useFit',                                  action='store_true',     help='Use a fit to determine the response', default= True )
args = argParser.parse_args()

plot_directory  = os.path.join( user_plot_directory, args.plot_directory, args.triggers)

# Lumi for MC
lumi = 35.9
# DrawLatex objects for plots
tex = ROOT.TLatex()
tex.SetNDC()
tex.SetTextSize(0.04)
tex.SetTextAlign(11) # align right
def drawObjects( dataMCScale, lumi ):
    lines = [
      #(0.15, 0.95, args.era), 
      (0.15, 0.95, '%s (13 TeV)'% ( args.era ) ),
    ]
    return [tex.DrawLatex(*l) for l in lines] 

# Formatting for 1D plots
def draw1DPlots(plots, dataMCScale):
  for log in [ False ]:
    plot_directory_ = os.path.join(plot_directory, ("log" if log else "") )
    for plot in plots:
      #if not max(l[0].GetMaximum() for l in plot.histos): continue # Empty plot
      #p_drawObjects = map( lambda l:tex.DrawLatex(*l), getattr(plot, "drawObjects", [] ) )
      p_drawObjects = getattr(plot, "drawObjects", [] ) 
      plotting.draw(plot,
        plot_directory = plot_directory_,
        #ratio          = {'yRange':(0.6,1.4)} if len(plot.stack)>=2 else None,
        logX = False, logY = log, sorting = False,
        yRange         = (0.95, 1.05) ,
        #scaling        = {0:1} if len(plot.stack)==2 else {},
        legend         = [ (0.15,0.91-0.05*len(plot.histos)/2,0.95,0.91), 2 ],
        drawObjects    = drawObjects( dataMCScale , lumi ) + p_drawObjects
      )

#
# Logger
#
import JetMET.tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

#colors = [ j+1 for j in range(0,9) ] + [ j+31 for j in range(9,18) ]

from JetMET.JEC.L2res.thresholds import pt_avg_thresholds, pt_avg_bins, eta_thresholds
pt_avg_bins       = [(pt_avg_thresholds[i], pt_avg_thresholds[i+1]) for i in range( len( pt_avg_thresholds ) -1 ) ]

alpha_values      = [0.1, 0.15, 0.25, 0.3, 0.35, 0.4, 0.45]
alpha_ref_value   = 0.3
 
response = {}
shape    = {}
for alpha in alpha_values:
    try:
        filename = os.path.join( user_plot_directory, args.input_directory, args.triggers, args.era, 'a%i'%(100*alpha), 'response_%s_results.pkl' % ("fit" if args.useFit else "mean") )
        response[alpha] = pickle.load( file( filename ))                                           
        logger.info( "Loaded file %s", filename )                                                  
    except IOError:                                                                                
        logger.info( "Could not load file %s", filename )                                          
    try:                                                                                           
        filename = os.path.join( user_plot_directory, args.input_directory, args.triggers, args.era, 'a%i'%(100*alpha), 'results.pkl' )
        shape[alpha] = pickle.load( file( filename ))[0]
        logger.info( "Loaded file %s", filename )
    except IOError:
        logger.info( "Could not load file %s", filename )
       
# x ... A,B
# y ... eta
# z ... pt_avg
def makeProjection( h, pt_avg_bin, eta_bin ):
    ''' Projects TH3D on a pt/eta bin
    '''
    # return if lower boundary > upper boundary
    if pt_avg_bin[0]>pt_avg_bin[1]: return
    if eta_bin[0]>eta_bin[1]: return

    if pt_avg_bin[0] not in pt_avg_thresholds: raise ValueError( "pt bin %r does not align with thresholds %r", pt_avg_bin, pt_avg_thresholds )
    if pt_avg_bin[1] not in pt_avg_thresholds: raise ValueError( "pt bin %r does not align with thresholds %r", pt_avg_bin, pt_avg_thresholds )
    if eta_bin[0] not in eta_thresholds: raise ValueError( "eta bin %r does not align with thresholds %r", eta_bin, eta_thresholds )
    if eta_bin[1] not in eta_thresholds: raise ValueError( "eta bin %r does not align with thresholds %r", eta_bin, eta_thresholds )
    
    result = None
 
    for i_eta in range(len(eta_thresholds)-1):

        eta_bin_ = tuple(eta_thresholds[i_eta:i_eta+2])
        # Is the current bin inside eta_bin?
        if not (eta_bin_[0]>=eta_bin[0] and eta_bin_[1]<=eta_bin[1]) : continue

        bin_y       = h.GetYaxis().FindBin( 0.5*sum(eta_bin) ) 

        for i_pt_avg in range(len(pt_avg_thresholds)-1):
            pt_avg_bin_ = tuple(pt_avg_thresholds[i_pt_avg:i_pt_avg+2])

            # Is the current pt inside pt_bin?
            if not (pt_avg_bin_[0]>=pt_avg_bin[0] and pt_avg_bin_[1]<=pt_avg_bin[1]) : continue
            bin_z      = h.GetZaxis().FindBin( 0.5*sum(pt_avg_bin)  ) 

            if result is None:
                result = h.ProjectionX(str(uuid.uuid1()) , bin_y, bin_y, bin_z, bin_z)
            else:
                result.Add( h.ProjectionX(str(uuid.uuid1()) , bin_y, bin_y, bin_z, bin_z))
            logger.info( "Added %r %r for %r %r", eta_bin_, pt_avg_bin_, eta_bin, pt_avg_bin )

    return result

mc_name, data_name  = ['QCD_Pt', 'JetHT_Run2016H']

#pt_avg_bin = (299,365)
pt_avg_bin = (51, 299)
#eta_bin    = (-0.261,0.261)
#eta_bin    = (2.5,3.139)
#eta_bin    = (3.839, 5.191)

alpha_thresholds = [0] + [alpha_values[0]-0.025] + [0.5*(alpha_values[i]+alpha_values[i+1]) for i in range( len(alpha_values)-1) ] + [ alpha_values[-1] + 0.025 ] #FIXME

extrapolation_results = {}
kFSR                  = {}
for pt_avg_bin in [ (51, 299) ]:

    extrapolation_results[ pt_avg_bin ] = {}
    kFSR[ pt_avg_bin ]                  = {}

    for eta_bin in [ 
    #    (-5.191, -3.489),
    #    (-3.489, -2.964),
    #    (-2.964, -2.5),
    #    (-2.5,   -2.172),
    #    (-2.172, -1.305),
    #    (-1.305, -0.783),
    #    (-0.783,  0.0),
    #    (0.0,     0.783),
        (0.783,   1.305),
    #    (1.305,   2.172),
    #    (2.172,   2.5),
    #    (2.5,     2.964),
    #    (2.964,   3.489),
    #    (3.139,   3.489),
    #    (3.489,   5.191),
        ]:

        extrapolation_results[pt_avg_bin][eta_bin]  = {}
        kFSR[pt_avg_bin][eta_bin]                   = {}
        response_values                             = {}

        for var in [ "A", "B" ]:

            extrapolation_results[pt_avg_bin][eta_bin][var] = {}
            kFSR[pt_avg_bin][eta_bin][var]                  = {}
            response_values[var]                            = {}

            for sample_name in sample_names:
                response_values[var][sample_name] = [] 
                isData = 'Run2016' in sample_name

                ref_response = None
                for alpha in alpha_values:
                    if not shape.has_key(alpha) : 
                        logger.debug( "Could not find alpha %3.2f for var %s sample %s. Available alpha values: %r. All alpha values: %r" % (alpha, var, sample_name, shape.keys(), alpha_values))
                        continue 

                    # get projection for pt and eta bin
                    proj = makeProjection( shape[alpha][var][sample_name], pt_avg_bin,  eta_bin )
                    
                    if (args.useFit):
                        mean_asymmetry, mean_asymmetry_error = GaussianFit( 
                            shape               = proj,
                            isData              = isData,
                            var_name            = "%s-symmetry" % var, 
                            fit_plot_directory  = os.path.join( plot_directory, 'fit'), 
                            fit_filename        = "fitresult_%s_a%i_%i_%i_pt_%i_%i_%s" % ( var, 100*alpha, 1000*eta_bin[0], 1000*eta_bin[1], pt_avg_bin[0], pt_avg_bin[1], sample_name ) 
                            )

                    else:
                        mean_asymmetry        = proj.GetMean()           
                        mean_asymmetry_error  = proj.GetMeanError() 

                    mean_response = (1 + mean_asymmetry)/(1 - mean_asymmetry)
                    mean_response_error = 2.*mean_asymmetry_error/(1 - mean_asymmetry)**2 # f(x) = (1+x)/(1-x) -> f'(x) = 2/(x-1)**2

                    logger.info( "sample %s var %s alpha %3.2f: mean response %5.4f +/- %5.4f asymmetry %5.4f +/- %5.4f", sample_name, var, alpha, mean_response, mean_response_error, mean_asymmetry, mean_asymmetry_error) 

                    response_values[var][sample_name].append( {'alpha':alpha, 'response':mean_response, 'response_error':mean_response_error } )
                    if alpha_ref_value == alpha:
                        ref_response        = mean_response
                        ref_response_error  = mean_response_error

                # make kFSR fit
                result = kFSRLinearFit( data = response_values[var][sample_name] )
                # store results & reference
                extrapolation_results[pt_avg_bin][eta_bin][var][sample_name] = result 
                extrapolation_results[pt_avg_bin][eta_bin][var][sample_name].update( {
                    'resp_0':           result['d0'], 
                    'resp_0_error':     result['d0_error'],
                    'resp_ref':         ref_response, 
                    'resp_ref_error':   ref_response_error,
                } )

            res = extrapolation_results[pt_avg_bin][eta_bin][var]
            kFSR[pt_avg_bin][eta_bin][var] = { 
                'kFSR':       res['QCD_pt']['resp_0'] / res['JetHT_Run2016H']['resp_0'] / res['QCD_pt']['resp_ref'] / res['JetHT_Run2016H']['resp_ref'],
#                'kFSR_error': res['QCD_pt']['resp_0'] / res['QCD_pt']['resp_ref']*sqrt( res['QCD_pt']['resp_0_error']**2 / res['QCD_pt']['resp_0'] + res['QCD_pt']['resp_0_error']**2 / res['QCD_pt']['resp_0'] ),
            }
