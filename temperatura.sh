#!/bin/bash
 # Shell script: temp.sh
 # Autor: Santiago Crespo
 # modificado por manxoig
 cpu=$(cat /sys/class/thermal/thermal_zone0/temp)
 echo "$(date) @ $(hostname)"
 echo "-------------------------------------------"
 echo "Temp.CPU => $((cpu/1000))'Cº"
# echo "Temp.GPU => $(/opt/vc/bin/vcgencmd measure_temp)"
 echo "-------------------------------------------"
 
#esto se ejecuta en el  la pc 
