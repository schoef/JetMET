import os

from RootTools.core.standard import *

from JetMET.tools.user import skim_ntuple_directory

sub_directory = "L2res/v11_03FebV6/default/" #FIXME

JetHT_Run2016B    = Sample.fromDirectory("JetHT_Run2016B", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016B"))
JetHT_Run2016C    = Sample.fromDirectory("JetHT_Run2016C", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016C"))
JetHT_Run2016D    = Sample.fromDirectory("JetHT_Run2016D", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016D"))
JetHT_Run2016E    = Sample.fromDirectory("JetHT_Run2016E", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016E"))
JetHT_Run2016F    = Sample.fromDirectory("JetHT_Run2016F", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016F"))
JetHT_Run2016G    = Sample.fromDirectory("JetHT_Run2016G", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016G"))
JetHT_Run2016H_v2 = Sample.fromDirectory("JetHT_Run2016H_v2", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016H_v2"))
JetHT_Run2016H_v3 = Sample.fromDirectory("JetHT_Run2016H_v3", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016H_v3"))

JetHT_Run2016BCD     = Sample.combine("JetHT_Run2016BCD", [JetHT_Run2016B, JetHT_Run2016C, JetHT_Run2016D])
JetHT_Run2016E       = Sample.combine("JetHT_Run2016E", [JetHT_Run2016E])
JetHT_Run2016EFearly = Sample.combine("JetHT_Run2016EFearly", [JetHT_Run2016E, JetHT_Run2016F])
JetHT_Run2016EFearly.setSelectionString("run<=278801")
JetHT_Run2016Fearly  = Sample.combine("JetHT_Run2016Fearly", [ JetHT_Run2016F])
JetHT_Run2016Fearly.setSelectionString("run<=278801")
JetHT_Run2016Flate   = Sample.combine("JetHT_Run2016Flate",  [ JetHT_Run2016F])
JetHT_Run2016Flate.setSelectionString("run>=278802")
JetHT_Run2016FlateG  = Sample.combine("JetHT_Run2016FlateG", [JetHT_Run2016F, JetHT_Run2016G])
JetHT_Run2016FlateG.setSelectionString("run>=278802")
JetHT_Run2016H       = Sample.combine("JetHT_Run2016H", [JetHT_Run2016H_v2, JetHT_Run2016H_v3])
JetHT_Run2016        = Sample.combine("JetHT_Run2016", [JetHT_Run2016B, JetHT_Run2016C, JetHT_Run2016D, JetHT_Run2016E, JetHT_Run2016F, JetHT_Run2016G, JetHT_Run2016H_v2, JetHT_Run2016H_v3] )

sub_directory_07Aug17 = "L2res/v11/default/"
JetHT_Run2016B_07Aug17 = Sample.fromDirectory("JetHT_Run2016B_07Aug17", os.path.join( skim_ntuple_directory, sub_directory_07Aug17, "JetHT_Run2016B_07Aug17"))
JetHT_Run2016C_07Aug17 = Sample.fromDirectory("JetHT_Run2016C_07Aug17", os.path.join( skim_ntuple_directory, sub_directory_07Aug17, "JetHT_Run2016C_07Aug17"))
#JetHT_Run2016D_07Aug17 = Sample.fromDirectory("JetHT_Run2016D_07Aug17", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016D_07Aug17"))
#JetHT_Run2016E_07Aug17 = Sample.fromDirectory("JetHT_Run2016E_07Aug17", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016E_07Aug17"))
JetHT_Run2016F_07Aug17 = Sample.fromDirectory("JetHT_Run2016F_07Aug17", os.path.join( skim_ntuple_directory, sub_directory_07Aug17, "JetHT_Run2016F_07Aug17"))
JetHT_Run2016G_07Aug17 = Sample.fromDirectory("JetHT_Run2016G_07Aug17", os.path.join( skim_ntuple_directory, sub_directory_07Aug17, "JetHT_Run2016G_07Aug17"))
JetHT_Run2016H_07Aug17 = Sample.fromDirectory("JetHT_Run2016H_07Aug17", os.path.join( skim_ntuple_directory, sub_directory_07Aug17, "JetHT_Run2016H_07Aug17"))


#JetHT_Run2016B_18Apr = Sample.fromDirectory("JetHT_Run2016B_18Apr", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016B_18Apr"))
#JetHT_Run2016C_18Apr = Sample.fromDirectory("JetHT_Run2016C_18Apr", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016C_18Apr"))
#JetHT_Run2016D_18Apr = Sample.fromDirectory("JetHT_Run2016D_18Apr", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016D_18Apr"))
#JetHT_Run2016E_18Apr = Sample.fromDirectory("JetHT_Run2016E_18Apr", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016E_18Apr"))
#JetHT_Run2016F_18Apr = Sample.fromDirectory("JetHT_Run2016F_18Apr", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016F_18Apr"))
#JetHT_Run2016G_18Apr = Sample.fromDirectory("JetHT_Run2016G_18Apr", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016G_18Apr"))
#JetHT_Run2016H_18Apr = Sample.fromDirectory("JetHT_Run2016H_18Apr", os.path.join( skim_ntuple_directory, sub_directory, "JetHT_Run2016H_18Apr"))
#
#JetHT_Run2016BCD_18Apr     = Sample.combine("JetHT_Run2016BCD_18Apr", [JetHT_Run2016B_18Apr, JetHT_Run2016C_18Apr, JetHT_Run2016D_18Apr])
#JetHT_Run2016E_18Apr       = Sample.combine("JetHT_Run2016E_18Apr", [JetHT_Run2016E_18Apr])
#JetHT_Run2016EFearly_18Apr = Sample.combine("JetHT_Run2016EFearly_18Apr", [JetHT_Run2016E_18Apr, JetHT_Run2016F_18Apr])
#JetHT_Run2016EFearly_18Apr.setSelectionString("run<=278801")
#JetHT_Run2016Fearly_18Apr  = Sample.combine("JetHT_Run2016Fearly_18Apr", [ JetHT_Run2016F_18Apr])
#JetHT_Run2016Fearly_18Apr.setSelectionString("run<=278801")
#JetHT_Run2016Flate_18Apr   = Sample.combine("JetHT_Run2016Flate_18Apr",  [ JetHT_Run2016F_18Apr])
#JetHT_Run2016Flate_18Apr.setSelectionString("run>=278802")
#JetHT_Run2016FlateG_18Apr  = Sample.combine("JetHT_Run2016FlateG_18Apr", [JetHT_Run2016F_18Apr, JetHT_Run2016G_18Apr])
#JetHT_Run2016FlateG_18Apr.setSelectionString("run>=278802")
#JetHT_Run2016H_18Apr       = Sample.combine("JetHT_Run2016H_18Apr", [JetHT_Run2016H_18Apr])
#JetHT_Run2016_18Apr        = Sample.combine("JetHT_Run2016_18Apr", [JetHT_Run2016B_18Apr, JetHT_Run2016C_18Apr, JetHT_Run2016D_18Apr, JetHT_Run2016E_18Apr, JetHT_Run2016F_18Apr, JetHT_Run2016G_18Apr, JetHT_Run2016H_18Apr] )

sub_directory = "L2res/v11/default/" #FIXME

QCD_Pt_50to80     = Sample.fromDirectory("QCD_Pt_50to80", os.path.join( skim_ntuple_directory, sub_directory, "QCD_Pt_50to80"))
QCD_Pt_80to120    = Sample.fromDirectory("QCD_Pt_80to120", os.path.join( skim_ntuple_directory, sub_directory, "QCD_Pt_80to120"))
QCD_Pt_120to170   = Sample.fromDirectory("QCD_Pt_120to170", os.path.join( skim_ntuple_directory, sub_directory, "QCD_Pt_120to170"))
QCD_Pt_170to300   = Sample.fromDirectory("QCD_Pt_170to300", os.path.join( skim_ntuple_directory, sub_directory, "QCD_Pt_170to300"))
QCD_Pt_300to470   = Sample.fromDirectory("QCD_Pt_300to470", os.path.join( skim_ntuple_directory, sub_directory, "QCD_Pt_300to470"))
QCD_Pt_470to600   = Sample.fromDirectory("QCD_Pt_470to600", os.path.join( skim_ntuple_directory, sub_directory, "QCD_Pt_470to600"))
QCD_Pt_600to800   = Sample.fromDirectory("QCD_Pt_600to800", os.path.join( skim_ntuple_directory, sub_directory, "QCD_Pt_600to800"))
QCD_Pt_800to1000  = Sample.fromDirectory("QCD_Pt_800to1000", os.path.join( skim_ntuple_directory, sub_directory, "QCD_Pt_800to1000"))
QCD_Pt_1000to1400 = Sample.fromDirectory("QCD_Pt_1000to1400", os.path.join( skim_ntuple_directory, sub_directory, "QCD_Pt_1000to1400"))
QCD_Pt_1400to1800 = Sample.fromDirectory("QCD_Pt_1400to1800", os.path.join( skim_ntuple_directory, sub_directory, "QCD_Pt_1400to1800"))
QCD_Pt_1800to2400 = Sample.fromDirectory("QCD_Pt_1800to2400", os.path.join( skim_ntuple_directory, sub_directory, "QCD_Pt_1800to2400"))
QCD_Pt_2400to3200 = Sample.fromDirectory("QCD_Pt_2400to3200", os.path.join( skim_ntuple_directory, sub_directory, "QCD_Pt_2400to3200"))
QCD_Pt_3200toInf  = Sample.fromDirectory("QCD_Pt_3200toInf", os.path.join( skim_ntuple_directory, sub_directory, "QCD_Pt_3200toInf"))

qcd_samples = [ QCD_Pt_50to80, QCD_Pt_80to120, QCD_Pt_120to170, QCD_Pt_170to300, QCD_Pt_300to470, QCD_Pt_470to600, QCD_Pt_600to800, QCD_Pt_800to1000, QCD_Pt_1000to1400, QCD_Pt_1400to1800, QCD_Pt_1800to2400, QCD_Pt_2400to3200, QCD_Pt_3200toInf] 

QCD_Pt = Sample.combine( "QCD_Pt", qcd_samples )

QCD_Pt_small = Sample.fromFiles( "QCD_Pt_small", files = [s.files[0] for s in qcd_samples] )
