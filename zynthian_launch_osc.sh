#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"


ZYN_DIR=/home/jfrey/Bidouilles/zynthian/
ZYN_MY_DATA=/home/jfrey/Bidouilles/zynthian/zynthian-my-data/
ZYN_UI_SCRIPT=$DIR/zynthian_gui_emu_osc.sh
OSC_PORT=4567



$DIR/zynthian_oscface_full.py $ZYN_UI_SCRIPT $ZYN_DIR $ZYN_MY_DATA $OSC_PORT
