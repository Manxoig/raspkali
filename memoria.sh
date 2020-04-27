#!/bin/bash
#tipo de shell 2

echo ""
 echo "Otros datos del sistema"
 echo "-------------------------------------------"
# echo "CPU $(vcgencmd measure_clock arm)'Hz"
# echo "CPU $(vcgencmd measure_volts core)"
 echo "Memoria repartida entre el sistema y la gpu:"
# echo "Sistema "
vcgencmd get_mem arm
# echo "GPU"
# vcgencmd get_mem gpu
 echo "-------------------------------------------"
 echo "Memoria libre"
 free -h
 echo "-------------------------------------------"
