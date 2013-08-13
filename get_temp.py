#!  /usr/bin/python
## ----------------------
## Lecture temperature
## ----------------------

import os
import sys
import glob
import time

## Normalement pas besoin 
## chargement au boot
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

## Quelques variables
base_dir = '/sys/bus/w1/devices/'
devices = glob.glob(base_dir + '28*')

TPS_DEV = 0.5
MAX_READ = 5
ERROR = -99

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

## Lecture de la temperature
def read_temp(file):
    nb = 0
    while True:
        lines = read_temp_raw(file)
        if lines:
            ## Si le CRC est bon 
            if lines[0].find('YES'):
                nb = 0
                ## La on a tout bon
                ## Normalement ya 2 lignes
                if len(lines) == 2:
                    eq = lines[1].find('t=')
                    temp_string = lines[1][eq+2:]
                    temp_c = float(temp_string) / 1000.0
                    if temp_c != -0.062:
                        return temp_c
                    else:
                        continue
                else:
                    return ERROR
            else:
                ## On incremente et on recommande
                nb += 1
                time.sleep(1)
                if nb > MAX_READ:
                    return ERROR
        else:
            ## Probleme on arrive pas a lire
            ## ON sort avec une valeur 
            return ERROR
    
## On lit tout les peripheriques
def read_all():
    all_dev = []
    for dev in devices:
        all_dev.append( read_temp(dev + '/w1_slave') )
        time.sleep(TPS_DEV)
    return all_dev
        


def main(arg):
    DEVICE = 0
    if len(arg) > 1:
        if arg[1] == '2':
            DEVICE = 1

    ## On lit tout
    capteurs = read_all()
    ## Mode Reel
    print capteurs[DEVICE]
    ## Mode test
    #print "%2.2f" % 35

if __name__ == '__main__':
    main(sys.argv)
