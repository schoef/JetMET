# Standard importts
import os
import ROOT
ROOT.gROOT.SetBatch(True)

# RooFit
ROOT.gSystem.Load("libRooFit.so")
ROOT.gSystem.Load("libRooFitCore.so")
ROOT.gROOT.SetStyle("Plain") # Not sure this is needed
ROOT.gSystem.SetIncludePath( "-I$ROOFITSYS/include/" )

# Logging
import logging
logger = logging.getLogger(__name__)

def gaussianFit( shape, var_name, fit_plot_directory, fit_filename):
    ''' Gaussian fit from Zeynep
    '''

    logger.info( "Performing a gaussian fit to get the mean" )
    # declare the observable mean, and import the histogram to a RooDataHist
    asymmetry   = ROOT.RooRealVar(var_name, var_name,-10,10) ;
    dh          = ROOT.RooDataHist("datahistshape","datahistshape",ROOT.RooArgList(asymmetry),ROOT.RooFit.Import(shape)) ;
    
    # plot the data hist with error from sum of weighted events
    frame       = asymmetry.frame(ROOT.RooFit.Title(var_name))
    if s.name == data.name:
        logger.debug( "Settings for data with Poisson error bars" )
        dh.plotOn(frame,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
    else:
        logger.debug( "Settings for mc with SumW2 error bars" )
        dh.plotOn(frame,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2)) ;

    # create a simple gaussian pdf
    gauss_mean  = ROOT.RooRealVar("mean","mean",0,-1.2,1.2)
    gauss_sigma = ROOT.RooRealVar("sigma","sigma",0.1,0,2)
    gauss       = ROOT.RooGaussian("gauss","gauss",asymmetry,gauss_mean,gauss_sigma) 
    
    # now do the fit and extract the parameters with the correct error
    if s.name == data.name:                            
        gauss.fitTo(dh,ROOT.RooFit.Save(),ROOT.RooFit.Range(dh.mean(asymmetry)-2*dh.sigma(asymmetry),dh.mean(asymmetry)+2*dh.sigma(asymmetry)))
    else:
        gauss.fitTo(dh,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(True),ROOT.RooFit.Range(dh.mean(asymmetry)-2*dh.sigma(asymmetry),dh.mean(asymmetry)+2*dh.sigma(asymmetry)))

    gauss.plotOn(frame)

    argset_fit = ROOT.RooArgSet(gauss_mean,gauss_sigma)
    gauss.paramOn(frame,ROOT.RooFit.Format("NELU",ROOT.RooFit.AutoPrecision(1)),ROOT.RooFit.Layout(0.55)) 
    frame.SetMaximum(frame.GetMaximum()*1.2)

    # add chi2 info
    chi2_text = ROOT.TPaveText(0.3,0.8,0.4,0.9,"BRNDC")
    chi2_text.AddText("#chi^{2} fit = %s" %round(frame.chiSquare(6),2))
    chi2_text.SetTextSize(0.04)
    chi2_text.SetTextColor(2)
    chi2_text.SetShadowColor(0)
    chi2_text.SetFillColor(0)
    chi2_text.SetLineColor(0)
    frame.addObject(chi2_text)

    ## Dummy I don't know how to save them without hacking / butchering the code.
    c = ROOT.TCanvas()
    frame.Draw()
    if not os.path.exists(fit_plot_directory): os.makedirs(fit_plot_directory)
    c.SaveAs(os.path.join( fit_plot_directory, fit_filename+".pdf"))
    c.SaveAs(os.path.join( fit_plot_directory, fit_filename+".png"))

    mean_asymmetry        = gauss_mean.getVal()
    mean_asymmetry_error  = shape.GetMeanError()

    return mean_asymmetry, mean_asymmetry_error 
