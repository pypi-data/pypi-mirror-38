from time import sleep
from struct import pack

from serial import Serial


c = Serial('/dev/ttyACM0', 9600)
sleep(1)

c.write(pack('B', 0xff))
l = c.readline().decode('utf-8')
print(l)
l = c.readline().decode('utf-8')
print(l)
l = c.readline().decode('utf-8')
print(l)
l = c.readline().decode('utf-8')
print(l)
