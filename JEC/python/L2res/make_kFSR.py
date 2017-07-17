#!/usr/bin/env python
''' Analysis script for evaluating kFSR
'''
#
# Standard imports and bateh mode
#
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.LoadMacro("$CMSSW_BASE/src/RootTools/plot/scripts/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.gStyle.SetOptFit(0)


import os
import array
import pickle
import uuid
from math import sqrt

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
argParser.add_argument('--logLevel',           action='store',      default='INFO',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging" )
argParser.add_argument('--triggers',           action='store',      default='exclDiPFJetAveHFJEC',      nargs='?', choices=['DiPFJetAve', 'DiPFJetAve_HFJEC', 'PFJet', 'exclDiPFJetAveHFJEC', 'exclDiPFJetAve', 'exclPFJet'], help="trigger suite" )
argParser.add_argument('--era',                action='store',      default='Run2016H',      nargs='?', choices=['Run2016', 'Run2016BCD', 'Run2016EFearly', 'Run2016FlateG', 'Run2016H'], help="era" )
argParser.add_argument('--overwrite',                               action='store_true',     help='Overwrite results.pkl?', default=True)
argParser.add_argument('--input_directory',    action='store',      default='JEC/L2res_v10_jer_cleaned',  help="subdirectory for results.pkl")
argParser.add_argument('--plot_directory',     action='store',      default='JEC/L2res_v10_jer_cleaned',  help="subdirectory for plots")
argParser.add_argument('--useFit',                                  action='store_true',     help='Use a fit to determine the response', default= True )
args = argParser.parse_args()

plot_directory  = os.path.join( user_plot_directory, args.plot_directory, args.triggers, args.era, 'kFSR')

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

alpha_values      = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
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

    if pt_avg_bin[0] not in pt_avg_thresholds: raise ValueError( "pt bin %r does not align with thresholds %r" %( pt_avg_bin, pt_avg_thresholds ))
    if pt_avg_bin[1] not in pt_avg_thresholds: raise ValueError( "pt bin %r does not align with thresholds %r" %( pt_avg_bin, pt_avg_thresholds ))
    if eta_bin[0] not in eta_thresholds: raise ValueError( "eta bin %r does not align with thresholds %r" %( eta_bin, eta_thresholds ))
    if eta_bin[1] not in eta_thresholds: raise ValueError( "eta bin %r does not align with thresholds %r" %( eta_bin, eta_thresholds ))

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

mc_name, data_name  = ['QCD_Pt', 'JetHT_%s'%args.era]
sample_names        = [mc_name, data_name]

#alpha_thresholds = [0] + [alpha_values[0]-0.025] + [0.5*(alpha_values[i]+alpha_values[i+1]) for i in range( len(alpha_values)-1) ] + [ alpha_values[-1] + 0.025 ] #FIXME

def make_kFSR_plot( extrapolation_results, response_values, filename ):
    ROOT.setTDRStyle()
    ROOT.gStyle.SetOptFit(0)
    c1 = ROOT.TCanvas()
    c1.SetBottomMargin(0.13)
    c1.SetLeftMargin(0.15)
    c1.SetTopMargin(0.07)
    c1.SetRightMargin(0.05)

    h=ROOT.TH1F('tmp','tmp',100,0,.5)

    h.GetXaxis().SetTitle( "#alpha" )
    h.GetYaxis().SetTitle( "response" )
    h.Draw()

    vals=[]

    draw_graphs         = []
    draw_shaded_graphs  = []
    draw_funcs          = []

    legend = ROOT.TLegend(0.15,0.91-0.05*2,0.95,0.91)
    legend.SetNColumns(2)

    for var in ['A', 'B']:

        for sample in sample_names:
            t     = extrapolation_results[var][sample]['tgraph']
            legend.AddEntry( t, "%s ( %s )"% ( sample, "p_{T}bal" if var=='A' else "MPF" ))
            vals += [ t.GetY()[n] for n in range(t.GetN()) ] # for y range

            draw_graphs.append( t )
            funcs = [f for f in t.GetListOfFunctions() ]# + extrapolation_results[var][sample]['quantile_functions'].values()
            for f in funcs:
                f.SetLineWidth( 1 )

            t.SetFillStyle( 0 )
            t.SetFillColor( 0 )
            if var=='A':
                t.SetLineStyle( ROOT.kDashed )
                for f in funcs:
                    f.SetLineStyle( ROOT.kDashed )
            if sample == mc_name:
                t.SetLineColor( ROOT.kRed )
                t.SetMarkerColor( ROOT.kRed )
                for f in funcs:
                    f.SetLineColor( ROOT.kRed )
            else:
                t.SetLineColor( ROOT.kBlack )
                t.SetMarkerColor( ROOT.kBlack )
                for f in funcs:
                    f.SetLineColor( ROOT.kBlack )

            # colors = [ ROOT.kBlue, ROOT.kGreen ]
            quantils = extrapolation_results[var][sample]['quantile_functions'].keys()
            quantils.sort()
            quantils.reverse()
            f_low, f_high = [ extrapolation_results[var][sample]['quantile_functions'][k] for k in quantils ]

            n = 10
            x_min, x_max = 0, 5
            x_vals = [ x_min + i*(x_max-x_min)/(n-1.) for i in range(n) ]

            x_data = x_vals + list(reversed(x_vals))
            y_data = [ f_low.Eval( x ) for x in x_vals ]
            y_data +=[ f_high.Eval( x ) for x in reversed(x_vals) ]

            x_data += [x_data[0]]
            y_data += [y_data[0]]

            t_gr = ROOT.TGraph(
                    len(x_data),
                    array.array('d', x_data ),
                    array.array('d', y_data )
                )
            t_gr.SetFillStyle(3001)
            t_gr.SetFillColor(ROOT.kRed if sample == mc_name else ROOT.kBlue)
            draw_shaded_graphs.append( t_gr )


    for g in draw_shaded_graphs:
        g.Draw('LF')
    for g in draw_graphs:
        g.Draw('EPL')

    max_y = min( 1.4, 1 + 2* max([ v-1 for v in vals ] + [  0.02 ]))
    min_y = max( 0.7, 1 +1.5*min([ v-1 for v in vals ] + [ -0.02 ]))

    h.GetYaxis().SetRangeUser(min_y, max_y)

    legend.SetFillStyle(0)
    legend.SetShadowColor(ROOT.kWhite)
    legend.SetBorderSize(0)
    legend.Draw()

    #c1.Print( os.path.join( plot_directory, filename+'.pdf' ) )
    c1.Print( os.path.join( plot_directory, filename+'.png' ) )

    del c1

extrapolation_results = {}
response_values       = {}
kFSR                  = {}
for pt_avg_bin in [
    (51, 299),
    (51, 73),
    (73, 95),
    (95, 163),
    (163, 230),
    (230, 299),
    (299, 365),
    (365, 435),
    (435, 566),
    ]:

    extrapolation_results[ pt_avg_bin ] = {}
    response_values[ pt_avg_bin ]       = {}
    kFSR[ pt_avg_bin ]                  = {}

    for eta_bin in [
        (-5.191, -3.489),
        (-3.489, -3.139),
        (-3.139, -2.964),
        (-2.964, -2.5),
        (-2.5,   -2.172),
        (-2.172, -1.305),
        (-1.305, -0.783),
        (-0.783, -0.261),
        (-0.261,  0.0 ),
        (0.0,     0.261),
        (0.261,   0.783),
        (0.783,   1.305),
        (1.305,   2.172),
        (2.172,   2.5),
        (2.5,     2.964),
        (2.964,   3.139),
        (3.139,   3.489),
        (3.489,   5.191),
        ]:

        extrapolation_results[pt_avg_bin][eta_bin]  = {}
        kFSR[pt_avg_bin][eta_bin]                   = {}
        response_values[pt_avg_bin][eta_bin]        = {}

        for var in [ "A", "B" ]:

            extrapolation_results[pt_avg_bin][eta_bin][var] = {}
            kFSR[pt_avg_bin][eta_bin][var]                  = {}
            response_values[pt_avg_bin][eta_bin][var]                            = {}

            for sample_name in sample_names:
                response_values[pt_avg_bin][eta_bin][var][sample_name] = []
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

                    response_values[pt_avg_bin][eta_bin][var][sample_name].append( {'alpha':alpha, 'response':mean_response, 'response_error':mean_response_error } )
                    if alpha_ref_value == alpha:
                        ref_response        = mean_response
                        ref_response_error  = mean_response_error

                # make kFSR fit
                result = kFSRLinearFit( data = response_values[pt_avg_bin][eta_bin][var][sample_name] )
                # store results & reference
                extrapolation_results[pt_avg_bin][eta_bin][var][sample_name] = result
                # Interpret linear extrapolation to x=0 -> y=d as extrapolated response and store ref
                extrapolation_results[pt_avg_bin][eta_bin][var][sample_name].update( {
                    'resp_0':           result['d0'],
                    'resp_0_error':     result['d0_error'],
                    'resp_ref':         ref_response,
                    'resp_ref_error':   ref_response_error,
                } )

            # compute kFSR and kFSR_error
            res = extrapolation_results[pt_avg_bin][eta_bin][var]
            r_data = res[data_name]
            r_mc   = res[mc_name]
            kFSR[pt_avg_bin][eta_bin][var] = {
                'kFSR':       ( r_data['resp_0']/r_mc['resp_0']) / (r_data['resp_ref']/r_mc['resp_ref']),
                'kFSR_error': ( r_data['resp_0']/r_mc['resp_0']) / (r_data['resp_ref']/r_mc['resp_ref'])*
                                sqrt( r_data['resp_0_error']**2/r_data['resp_0']**2 + r_mc['resp_0_error']**2/r_mc['resp_0']**2 + r_data['resp_ref_error']**2/r_data['resp_ref']**2 + r_mc['resp_ref_error']**2/r_mc['resp_ref']**2 ),
            }

        make_kFSR_plot(
            extrapolation_results[pt_avg_bin][eta_bin],
            response_values[pt_avg_bin][eta_bin],
            filename  = "kFSR_extrapolation_eta_%i_%i_pt_%i_%i" % ( 1000*eta_bin[0], 1000*eta_bin[1], pt_avg_bin[0], pt_avg_bin[1] )

        )
