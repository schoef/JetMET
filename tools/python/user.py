import os

if os.environ['USER'] in ['schoef', 'rschoefbeck', 'schoefbeck']:
    # caches
    cache_directory = "/afs/hephy.at/data/rschoefbeck01/JetMET/caches/"
    # master ntuple
    master_ntuple_directory = "/afs/hephy.at/data/rschoefbeck01/cmgTuples/"
    # skim ntuple
    #skim_ntuple_directory = "/afs/hephy.at/data/rschoefbeck02/postProcessed/"
    skim_ntuple_directory = "/afs/hephy.at/data/cms01"
    # Where the plots go
    plot_directory      = "/afs/hephy.at/user/r/rschoefbeck/www/"
    #plot_directory      = "/afs/cern.ch/work/s/schoef/www/"
elif os.environ['USER'] in ['spandey']:

    plot_directory      = "XXX"

elif os.environ['USER'] in [ 'zdemirag']:

    plot_directory       = "/afs/cern.ch/user/z/zdemirag/www/JetMET/"
