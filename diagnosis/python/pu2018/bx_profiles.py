# Standard imports
import os
import ROOT

# RootTools
from RootTools.core.standard import *

# Samples
directory = "/afs/hephy.at/data/rschoefbeck02/postProcessed/flat_jet_trees/v6/"
dm_2018 = Sample.fromDirectory( "DoubleMuon", os.path.join( directory, "DoubleMuon_Run2018C-17Sep2018-v1_MINIAOD" ), isData = True)
#from JetMET.diagnosis.pu2018.samples import *

# define TProfiles
#bx_thresholds  = [i for i in range(3000)]
#prefix = ''
bx_thresholds  = [i for i in range(500)]
prefix = 'zoomed_'

variables = [ 
#    [ "HFsumPt",  "all_3p1_5p1_sumPt+all_m5p1_m3p1_sumPt", None, 700, .9],
#    [ "PhEnEndCapSumPt",  "ga_m3p1_m2p5_sumPt+ga_2p5_3p1_sumPt", None, 25, .9],
#    [ "NhEnEndCapSumPt",  "nh_m3p1_m2p5_sumPt+nh_2p5_3p1_sumPt", None, 35, .9],
    [ "PhEnBarrelSumPt",  "ga_m1p5_1p5_sumPt", None, 100, .9],
    [ "NhEnBarrelSumPt",  "nh_m1p5_1p5_sumPt", None, 70, .9],
#    [ "MET", "met_pt", 50, 100, .9 ],
#    [ "nVert",  "nVert", 40, 40,.9 ],
#    [ "nVertAll",  "nVertAll", 40, 40,.9],
]


dm_2018.reduceFiles( to = -1 )

selectionString = "Flag_goodVertices&&Flag_globalSuperTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_BadPFMuonFilter&&Flag_BadChargedCandidateFilter&&Flag_eeBadScFilter"

for name, variable, threshold_low, threshold_high, minimum in variables:

    th_string_low  = "" if threshold_low is None  else "&&%s<%f"% ( variable, threshold_low )
    th_string_high = "" if threshold_high is None else "&&%s>=%f"% ( variable, threshold_high )
    inclusive = dm_2018.get1DHistoFromDraw( "bx", bx_thresholds, selectionString = selectionString+th_string_low,  binningIsExplicit = True )
    tail      = dm_2018.get1DHistoFromDraw( "bx", bx_thresholds, selectionString = selectionString+th_string_high, binningIsExplicit = True )

    inclusive.legendText = "all" if threshold_low is None  else "%s < %i"% ( name, threshold_low ) 
    tail.legendText      = "all" if threshold_high is None  else "%s #geq %i"% ( name, threshold_high ) 

    #inclusive.style = styles.lineStyle( ROOT.kRed ) 
    #tail     .style = styles.errorStyle( ROOT.kBlack ) 
    inclusive.style = styles.lineStyle( ROOT.kBlue ) 
    tail     .style = styles.lineStyle( ROOT.kRed ) 

    plot = Plot.fromHisto( name = prefix+name, histos = [ [inclusive], [tail] ], texX = "BX", texY = None)
    plotting.draw(plot, 
        #ratio = {},
        widths = {'x_width':1300, 'y_width':600},
        yRange=(minimum, 'auto'),  
        legend      = [0.15,0.76,0.40,0.90],
        plot_directory = "/afs/hephy.at/user/r/rschoefbeck/www/JetMET/BX/",
        logX = False, logY = True, copyIndexPHP = True,
        )
