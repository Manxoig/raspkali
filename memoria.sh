#!/bin/bash
#tipo de shell 2
#sudo apt-get install inxi -y

echo ""
echo ".- -- .- / ... ..- .- .-.-."
echo ""
echo "Otros datos del sistema"
echo "-------------------------------------------"
inxi -c
echo ""
lscpu | grep Byte 
lscpu | grep Model
lscpu | grep Hz
lscpu | grep Vulne 
lscpu | grep Architecture
#echo "CPU $(vcgencmd measure_clock arm)'Hz"
#echo "CPU $(vcgencmd measure_volts core)"
#echo "Memoria repartida entre el sistema y la gpu:"
echo ""
echo "Sistema "
uname -r
#vcgencmd get_mem arm
echo ""
#echo "GPU"
#vcgencmd get_mem gpu
echo "-------------------------------------------"
echo "Memoria libre"
free -h
echo "-------------------------------------------"
echo ""
echo ".- -- .- / ... ..- .- .-.-."
echo ""
