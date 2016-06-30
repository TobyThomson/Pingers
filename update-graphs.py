#!/usr/bin/python
import ntplib

from time import ctime
from datetime import datetime

import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Figure, Data, Stream, YAxis

import subprocess
import json

import time

StreamTokens = [
    'mqhfnklozb',
    'f847i0shkm',
    'rrlc27u2jq',
    '1y6v3qogj0',
    '0tjvf1xc2f',
    '7xdgb02chb',
    '7ngv2yq357',
    'icbs0pcoth',
    '9qsn5pavk7',
    'e41e45ipiu',
    '2zuwv3ddwm',
    'jfu95pkqge',
    'w6wtx04s0e',
    'mftnt1w3g7',
    'fmbotsxq6y',
    'n112f5me7e',
    'f38dfsg1oc',
    '0y75y4r9ue',
    '8nrrhhxvnm',
    'mlwcv4tl7i',
    'wjdw9lep0k',
    'glmt7b0tyr',
    'bbzxvclvu7',
    'yqto99tfs2',
    '8d97d1al1k'
]

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

StreamTokens = StreamTokens[ID-1:ID+2]

py.sign_in('TobyThomson', '5wx0c1c6lz')

PlotTitle = 'Pinger ' + str(ID) + ' Data'

PingTrace = Scatter(
    x=[],
    y=[],
   stream=Stream(
        token=StreamTokens[0]
    ),
    name='Ping',
    yaxis='y'
)

DownloadTrace = Scatter(
    x=[],
    y=[],
    stream=Stream(
        token=StreamTokens[1]
    ),
    name='Download Speed',
    yaxis='y2'
)

UploadTrace = Scatter(
    x=[],
    y=[],
    stream=Stream(
        token=StreamTokens[2]
    ),
    name='Upload Speed',
    yaxis='y2'
)

PlotLayout = Layout(
    title=PlotTitle,
    yaxis=YAxis(
        title='Milliseconds'
    ),
    yaxis2=YAxis(
        title='Mbit/s',
        side='right',
        overlaying="y"
    )
)

PlotData = Data([PingTrace, DownloadTrace, UploadTrace])

PlotFigure = Figure(data=PlotData, layout=PlotLayout)

py.plot(PlotFigure, filename=PlotTitle, auto_open=False)

PingStream = py.Stream(StreamTokens[0])
PingStream.open()

DownloadStream = py.Stream(StreamTokens[1])
DownloadStream.open()

UploadStream = py.Stream(StreamTokens[2])
UploadStream.open()

while True:
    try:
        currentTime = GetCurrentTime()

        proc = subprocess.Popen(['python', PATH + 'pyspeedtest/pyspeedtest.py', '-f', 'json'], stdout=subprocess.PIPE)

        JSON = proc.stdout.read()

        pingRecordJSON = json.loads(JSON)

        downloadSpeed = (pingRecordJSON['download'] / 1024) / 1024
        uploadSpeed = (pingRecordJSON['upload'] / 1024) / 1024

        PingStream.write({'x': currentTime, 'y': pingRecordJSON['ping'] })
        DownloadStream.write({'x': currentTime, 'y': downloadSpeed })
        UploadStream.write({'x': currentTime, 'y': uploadSpeed })

        time.sleep(600)

    except:
        time.sleep(5)

PingStream.close()
DownloadStream.close()
UploadStream.close()
