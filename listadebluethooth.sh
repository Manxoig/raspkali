#usa rfkill hay q tenerlo instalaado
# apt-get install bluez bluetooth blueman
#apt-get install bluetooth bluez bluez-tools rfkill rfcomm
# por si presenta problemas
#escrito por Manxoig
#buscame en comoyporque.net


echo ".- -- .- / ... ..- .- .-.-."
echo ""
#evitar problemas por bloqueos
rfkill list
rfkill unblock all
#/etc/init.d/bluetooth status -l
#ver si esta el proceso
echo ""
echo "INICIANDO PROCESO"
systemctl start bluetooth
bluetoothctl power on
echo ""
echo "Buscando bluetooth"
hcitool scan
#echo "escribe default-agent" #default-agent esto va denotr el bluetoothctl ver como se hace
bluetoolhctl defaul-agent
#echo "Escribe scan on" #escribe scan on 
#echo "buscar en la lista tu dispositivo"
# primero hay q emparejar
#print ingresar las mac del dispostivo 
bluetoolhctl pair  2D:61:D3:BD:ED:DF
# colocarlo como dispositivo de confianza
bluetoolhctl trust  2D:61:D3:BD:ED:DF
#luego hay q conectarlo
bluetoolhctl connect  2D:61:D3:BD:ED:DF
# este comando es el super importante para q salga en el mixer de audio
dmesg |grep bluetooth
#bluetoothctl
echo ""
echo ".- -- .- / ... ..- .- .-.-."







#version 2
hciconfig hci0 up
