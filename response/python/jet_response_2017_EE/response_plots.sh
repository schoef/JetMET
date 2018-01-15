#!/bin/sh
#python response_plots.py --plot_directory EE_2017       --samples RelVal_QCD_flat_GTv1_SRPFoff_PUpmx25ns RelVal_QCD_flat_GTv2_SRPFoff_PUpmx25ns RelVal_QCD_flat_GTv2_SRPFon_PUpmx25ns &
#python response_plots.py --plot_directory EE_2017_NoPU  --samples RelVal_QCD_flat_GTv1_SRPFoff_NoPU RelVal_QCD_flat_GTv2_SRPFoff_NoPU RelVal_QCD_flat_GTv2_SRPFon_NoPU &

#python response_plots.py --plot_directory EE_2017_ZeroN --samples RelVal_QCD_flat_GTv2_SRPFon_PUpmx25ns RelVal_QCD_flat_GTv2_SRPFon_PUpmx25ns_ZeroN & 
#python response_plots.py --plot_directory EE_2017_ZeroN_NoPU_SRPFoff --samples RelVal_QCD_flat_GTv2_SRPFoff_NoPU RelVal_QCD_flat_GTv2_SRPFoff_NoPU_ZeroN & 

python response_plots.py --plot_directory EE_2017_NoPU_interpolated  --samples RelVal_QCD_flat_GTv1_SRPFoff_NoPU RelVal_QCD_flat_GTv2_SRPFoff_NoPU RelVal_QCD_flat_GTv2_SRPFon_NoPU RelVal_QCD_flat_GTv2_SRPF50_NoPU RelVal_QCD_flat_GTv2_SRPF70_NoPU RelVal_QCD_flat_GTv2_SRPF90_NoPU 
