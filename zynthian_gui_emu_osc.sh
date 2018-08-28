#!/bin/bash


ZYNTHIAN_REAL_DIR=$1

cd $ZYNTHIAN_REAL_DIR/zynthian-emuface
source ../zynthian-sys/scripts/zynthian_envars.sh



export DISPLAY_WIDTH="480"
export DISPLAY_HEIGHT="320"
export ZYNTHIAN_AUBIONOTES=1
export ZYNTHIAN_TOUCHOSC=1
export ZYNTHIAN_WIRING_LAYOUT="EMULATOR"
export ZYNTHIAN_UI_FONT_FAMILY="Audiowide"
export ZYNTHIAN_UI_FONT_SIZE="14"
export ZYNTHIAN_UI_ENABLE_CURSOR="0"
export ZYNTHIAN_LOG_LEVEL=10
#export ZYNTHIAN_MY_DATA_DIR=/home/jfrey/Bidouilles/zynthian/zynthian-my-data/

export ZYNTHIAN_DATA_DIR=$ZYNTHIAN_REAL_DIR/zynthian-data/
export ZYNTHIAN_MY_DATA_DIR=$2

echo "toto"
echo $3
cd ../zynthian-ui
exec ./zynthian_gui.py $3
