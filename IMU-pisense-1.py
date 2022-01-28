#from __future__ import division  # for py2.x compatibility
from pisense import SenseHAT, array
from colorzero import Color
from math import sqrt
from time import sleep
import sys

def movements(hatt):
    Imu=hatt.imu
    for reading in Imu: 
        delta_x = int(round(max(-1, min(1, -reading.accel.x))))
        delta_y = int(round(max(-1, min(1, reading.accel.y))))
#        delta_y = int(round(max(-1, min(1, reading.gyro.x))))
#        delta_x = int(round(max(-1, min(1, reading.gyro.y))))

#        delta_x = int(round(max(-1, min(1, reading.orient.x))))
#        delta_y = int(round(max(-1, min(1, reading.orient.y))))
        vec_acc=sqrt(reading.accel.x*reading.accel.x+reading.accel.y*reading.accel.y+reading.accel.z*reading.accel.z)

        print ("gyro X % 3.2f  Y % 3.2f  Z % 3.2f accel X % 3.2f  Y % 3.2f  Z % 3.2f vector % 3.2f "  % (reading.gyro.x,  reading.gyro.y, reading.gyro.z, reading.accel.x,  reading.accel.y, reading.accel.z, vec_acc), end="\r")
#        print ("accel X % 3.2f accel Y % 3.2f accel Z % 3.2f vector % 3.2f" % (reading.accel.x,  reading.accel.y, reading.accel.z, vec_acc), end="\r")
#        print ("rotation X % 3.2f rotation Y % 3.2f rotation Z % 3.2f vector % 3.2f" % (reading.orient.roll,  reading.orient.pitch, reading.orient.yaw, reading.orient), end="\r")
        if delta_x != 0 or delta_y != 0:
            yield -delta_x, delta_y
        if vec_acc > 2:
            print("\n\nZDERZENIE Z ZIEMIĄ\n\n")
            raise SystemExit
        E=hatt.stick.read(0.001)
        if E:
            if E.held and E.direction=='enter': 
                print("\n\nOK\n\n")
                raise SystemExit
        sleep(5/10)

def arrays(moves):
    a = array(Color('black'))  # blank screen
    x = y = 3
    a[y, x] = Color('white')
    yield a  # initial position
    for dx, dy in moves:
        a[y, x] = Color('black')
#        x = max(0, min(7, x + dx))
#        y = max(0, min(7, y + dy))  #stops at the edge
        x = (x + dx) % 8	#cycle acros the edge
        y = (y + dy) % 8   
        a[y, x] = Color('white')
        yield a
    a[y, x] = Color('black')
    yield a  # end with a blank display

def finito(dd):
    print('finito')
#    return sys.exit()  # enter exits  
#    sys.exit()
    raise SystemExit


with SenseHAT() as hat:
#    hat.stick.stream=True
#    hat.stick.when_enter=finito
    for a in arrays(movements(hat)):
        hat.screen.array = a




