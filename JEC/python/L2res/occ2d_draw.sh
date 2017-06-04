#!/bin/sh

python cc2d_draw.py --era=Run2016BCD     --etaSign=+1   --ptBin 150, 500  &
python cc2d_draw.py --era=Run2016EFearly --etaSign=+1   --ptBin 150, 500  &
python cc2d_draw.py --era=Run2016FlateG  --etaSign=+1   --ptBin 150, 500 &
python cc2d_draw.py --era=Run2016H       --etaSign=+1   --ptBin 150, 500 &
python cc2d_draw.py --era=Run2016BCD     --etaSign=-1   --ptBin 150, 500  &
python cc2d_draw.py --era=Run2016EFearly --etaSign=-1   --ptBin 150, 500  &
python cc2d_draw.py --era=Run2016FlateG  --etaSign=-1   --ptBin 150, 500 &
python cc2d_draw.py --era=Run2016H       --etaSign=-1   --ptBin 150, 500 &
python cc2d_draw.py --era=Run2016BCD     --cleaned --etaSign=+1   --ptBin 150, 500  &
python cc2d_draw.py --era=Run2016EFearly --cleaned --etaSign=+1   --ptBin 150, 500  &
python cc2d_draw.py --era=Run2016FlateG  --cleaned --etaSign=+1   --ptBin 150, 500 &
python cc2d_draw.py --era=Run2016H       --cleaned --etaSign=+1   --ptBin 150, 500 &
python cc2d_draw.py --era=Run2016BCD     --cleaned --etaSign=-1   --ptBin 150, 500  &
python cc2d_draw.py --era=Run2016EFearly --cleaned --etaSign=-1   --ptBin 150, 500  &
python cc2d_draw.py --era=Run2016FlateG  --cleaned --etaSign=-1   --ptBin 150, 500 &
python cc2d_draw.py --era=Run2016H       --cleaned --etaSign=-1   --ptBin 150, 500 &
