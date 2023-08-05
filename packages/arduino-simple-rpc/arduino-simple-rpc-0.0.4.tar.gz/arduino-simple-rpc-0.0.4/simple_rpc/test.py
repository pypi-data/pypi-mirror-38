from time import sleep

from serial import Serial


c = Serial('/dev/ttyACM0')
sleep(1)

c.write(chr(0xff))
l = str(c.readline())

print(l)
