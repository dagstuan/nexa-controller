#!/usr/bin/python

import pigpio
import time

def cbf(g, L, t):
   message = "gpio=" + str(g) + " level=" + str(L) + " at " + str(t)
   print(message)

#pigpio.start()
pi = pigpio.pi()

cb = pi.callback(17, pigpio.EITHER_EDGE, cbf)

time.sleep(60)

cb.cancel()

pi.stop()
