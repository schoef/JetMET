#!/bin/sh

python occ2d_draw.py --era=Run2016BCD_18Apr     --etaSign=+1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016EFearly_18Apr --etaSign=+1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016FlateG_18Apr  --etaSign=+1   --ptBin 150 500 &
python occ2d_draw.py --era=Run2016H_18Apr       --etaSign=+1   --ptBin 150 500 &
python occ2d_draw.py --era=Run2016BCD_18Apr     --etaSign=-1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016EFearly_18Apr --etaSign=-1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016FlateG_18Apr  --etaSign=-1   --ptBin 150 500 &
python occ2d_draw.py --era=Run2016H_18Apr       --etaSign=-1   --ptBin 150 500 &
python occ2d_draw.py --era=Run2016BCD_18Apr     --cleaned --etaSign=+1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016EFearly_18Apr --cleaned --etaSign=+1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016FlateG_18Apr  --cleaned --etaSign=+1   --ptBin 150 500 &
python occ2d_draw.py --era=Run2016H_18Apr       --cleaned --etaSign=+1   --ptBin 150 500 &
python occ2d_draw.py --era=Run2016BCD_18Apr     --cleaned --etaSign=-1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016EFearly_18Apr --cleaned --etaSign=-1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016FlateG_18Apr  --cleaned --etaSign=-1   --ptBin 150 500 &
python occ2d_draw.py --era=Run2016H_18Apr       --cleaned --etaSign=-1   --ptBin 150 500 &
python occ2d_draw.py --era=Run2016BCD_18Apr     --bad --etaSign=+1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016EFearly_18Apr --bad --etaSign=+1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016FlateG_18Apr  --bad --etaSign=+1   --ptBin 150 500 &
python occ2d_draw.py --era=Run2016H_18Apr       --bad --etaSign=+1   --ptBin 150 500 &
python occ2d_draw.py --era=Run2016BCD_18Apr     --bad --etaSign=-1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016EFearly_18Apr --bad --etaSign=-1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016FlateG_18Apr  --bad --etaSign=-1   --ptBin 150 500 &
python occ2d_draw.py --era=Run2016H_18Apr       --bad --etaSign=-1   --ptBin 150 500 &
python occ2d_draw.py --era=Run2016BCD_18Apr     --bad --cleaned --etaSign=+1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016EFearly_18Apr --bad --cleaned --etaSign=+1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016FlateG_18Apr  --bad --cleaned --etaSign=+1   --ptBin 150 500 &
python occ2d_draw.py --era=Run2016H_18Apr       --bad --cleaned --etaSign=+1   --ptBin 150 500 &
python occ2d_draw.py --era=Run2016BCD_18Apr     --bad --cleaned --etaSign=-1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016EFearly_18Apr --bad --cleaned --etaSign=-1   --ptBin 150 500  &
python occ2d_draw.py --era=Run2016FlateG_18Apr  --bad --cleaned --etaSign=-1   --ptBin 150 500 &
python occ2d_draw.py --era=Run2016H_18Apr       --bad --cleaned --etaSign=-1   --ptBin 150 500 &
