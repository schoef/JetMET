#!/bin/sh

python L2res_skim.py --targetDir=/afs/hephy.at/data/rschoefbeck02/postProcessed/L2res --sample=JetHT_Run2016B_18Apr --nJobs=5 --job=$1 &
python L2res_skim.py --targetDir=/afs/hephy.at/data/rschoefbeck02/postProcessed/L2res --sample=JetHT_Run2016C_18Apr --nJobs=5 --job=$1 &
python L2res_skim.py --targetDir=/afs/hephy.at/data/rschoefbeck02/postProcessed/L2res --sample=JetHT_Run2016D_18Apr --nJobs=5 --job=$1 &
python L2res_skim.py --targetDir=/afs/hephy.at/data/rschoefbeck02/postProcessed/L2res --sample=JetHT_Run2016E_18Apr --nJobs=5 --job=$1 &
python L2res_skim.py --targetDir=/afs/hephy.at/data/rschoefbeck02/postProcessed/L2res --sample=JetHT_Run2016F_18Apr --nJobs=5 --job=$1 &
python L2res_skim.py --targetDir=/afs/hephy.at/data/rschoefbeck02/postProcessed/L2res --sample=JetHT_Run2016G_18Apr --nJobs=5 --job=$1 &
python L2res_skim.py --targetDir=/afs/hephy.at/data/rschoefbeck02/postProcessed/L2res --sample=JetHT_Run2016H_18Apr --nJobs=5 --job=$1 &
