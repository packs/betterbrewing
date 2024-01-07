#!/usr/bin/env python

import os
import glob
import time
import datetime
import argparse

parser = argparse.ArgumentParser(description='Reads temperature from external temperature probe.')
parser.add_argument('-s', '--short', action='store_true', dest='short', help='Only print numeric temperature.')
parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', help='Print more status messages.')
parser.set_defaults(verbose=False)
parser.set_defaults(short=False)
options = parser.parse_args()


def read_temp(decimals = 1, sleeptime = 3):

    """Reads the temperature from a 1-wire device"""

    device = glob.glob("/sys/bus/w1/devices/" + "28*")[0] + "/w1_slave"
    try:
        timepoint = datetime.datetime.now()
        with open(device, "r") as f:
            lines = f.readlines()
        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            lines = read_temp_raw()
        timepassed = (datetime.datetime.now() - timepoint).total_seconds()
        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp = round(float(temp_string) / 1000.0, decimals)
            if options.short:
                print(str(temp))
            else:
                print(time.strftime("%d/%m/%y@%H:%M:%S - ")+str(temp)+" C")
            time.sleep(sleeptime-timepassed)
            timepoint = datetime.datetime.now()
    except:
        print('ERROR: Unable to read temperature.') 

if __name__ == "__main__":
    read_temp()

