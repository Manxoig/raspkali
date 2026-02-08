# python script
# autor : Santiago Crespo
# no funcionan en kali

import commands
temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
print 'Temp.CPU =>' + str(temp)
tempgpu = commands.getoutput('/opt/vc/bin/vcgencmd measure_temp' ).replace('temp=', '' ).replace('C', '')
print 'Temp.GPU =>' + str(tempgpu)

# NO FUNCIONA EN KALI  
# solo el de  cpu funcionan
