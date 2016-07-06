#!/usr/bin/python
import ntplib

from time import ctime
from datetime import datetime

import subprocess
import json
import csv

import time

def GetCurrentTime ():
    ntpClient = ntplib.NTPClient()

    response = ntpClient.request('europe.pool.ntp.org', version=3)

    timeString = ctime(response.tx_time)

    return datetime.strptime(timeString, "%a %b %d %H:%M:%S %Y")

#PATH = '/home/pi/Pinger/'
PATH = '/home/toby/Documents/Projects/Pingers/'

try:
	ID = int(open(PATH + 'ID.txt', 'r').readline())

except:
	ID = 1

	with open(PATH + 'ID.txt', 'w') as f:
			f.write(str(ID))


csvFile = open(PATH + 'csvFile.csv', 'wt')
writer = csv.writer(csvFile)

writer.writerow( ('Timestamp', 'Ping', 'Upload Speed (Mbit/s)', 'Download Speed (Mbit/s)') )

csvFile.close()

while True:
    try:
    	csvFile = open(PATH + 'csvFile.csv', 'a')
    	
    	writer = csv.writer(csvFile)
    	
        currentTime = GetCurrentTime()

        proc = subprocess.Popen(['python', PATH + 'pyspeedtest/pyspeedtest.py', '-f', 'json'], stdout=subprocess.PIPE)

        JsonOut = proc.stdout.read()

        pingRecordJSON = json.loads(JsonOut)
        
        uploadSpeed = (pingRecordJSON['upload'] / 1024) / 1024
        downloadSpeed = (pingRecordJSON['download'] / 1024) / 1024
        
        writer.writerow( (currentTime, pingRecordJSON['ping'], uploadSpeed, downloadSpeed) )
        print('writing...')
        csvFile.close()
        
        time.sleep(6)

    except:
        time.sleep(5)
