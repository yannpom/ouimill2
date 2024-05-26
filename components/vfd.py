#!/usr/bin/env python

import linuxcnc, hal, time, math, minimalmodbus

vfd = hal.component("vfd")

vfd.newpin("infreq",      hal.HAL_FLOAT, hal.HAL_IN)

vfd.newpin("n",           hal.HAL_FLOAT, hal.HAL_OUT)
vfd.newpin("lost",        hal.HAL_FLOAT, hal.HAL_OUT)
vfd.newpin("outfreq",     hal.HAL_FLOAT, hal.HAL_OUT)
vfd.newpin("outcurrent",  hal.HAL_FLOAT, hal.HAL_OUT)
vfd.newpin("outpower",    hal.HAL_FLOAT, hal.HAL_OUT)
vfd.newpin("outvoltage",  hal.HAL_FLOAT, hal.HAL_OUT)
vfd.newpin("temperature", hal.HAL_FLOAT, hal.HAL_OUT)
vfd.newpin("stopped",     hal.HAL_BIT,   hal.HAL_OUT)
vfd.newpin("running",     hal.HAL_BIT,   hal.HAL_OUT)

spindle = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
#spindle.serial.baudrate = 4800

lost = 0

def readLoop(i, a, b):
    global lost
    while True:
        try:
            v = i.read_register(a, b)
            return v 
        except IOError:
            vfd['lost'] += 1
            lost += 1
        except ValueError:
            vfd['lost'] += 1
            lost += 1

vfd.ready()

n = 0

try:
    while True:
        while True:
            infreq1 = readLoop(spindle, 0, 2)
            infreq2 = math.floor(vfd['infreq'])
            if not infreq1 == infreq2:
                try:
                    vfd['stopped'] = False
                    vfd['running'] = not vfd['stopped']
                    spindle.write_register(0, infreq2, 2)
                except:
                    vfd['lost'] += 1
                    lost += 1
            else:
                break

        vfd['outfreq'] = readLoop(spindle, 57, 2)
        vfd['stopped'] = (vfd['outfreq'] == 0)
        vfd['running'] = not vfd['stopped']

        vfd['outvoltage'] = readLoop(spindle, 60, 0)
        if vfd['outfreq'] > 50 and vfd['outvoltage']:
            vfd['outcurrent'] = readLoop(spindle, 61, 1)
            vfd['outpower'] = vfd['outcurrent'] * vfd['outvoltage'] * math.sqrt(3)
            #vfd['outpower'] = readLoop(spindle, 61, 0)
            #vfd['outcurrent'] = vfd['outpower'] / math.sqrt(3) / vfd['outvoltage']
        else:
            vfd['outpower'] = 0
            vfd['outcurrent'] = 0
        
        vfd['temperature'] = readLoop(spindle, 62, 0)
       
        n += 1

        vfd['n'] = n




except KeyboardInterrupt:
    raise SystemExit

