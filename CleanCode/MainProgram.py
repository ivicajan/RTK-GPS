import socket
import base64
from pyrtcm import RTCMReader
import serial
import time
import string 
import pynmea2
import csv
import threading
import queue
from multiprocessing import Process
import datetime


# This program runs the board, recevive correct and raw data, together with original log
# Input Value: roundName, stands for the specifica run name and naming the log file using that.
# Expected Output: logFile & oriLogFile, can be process later using the LogProcess.py
# Side Effects: rtkLocationFile, gpsLocationFile, which is useless but kept here because I have no time to fine-tune these

# Tips: set searil port to be dev/tty0 for use on rapsberry pi.



roundName='13'
q=queue.Queue(1)


rtcmWave=''
newRtcmWave=True
ggaData=''
newGgaData=False
finish=0
clearStack=True


def processdata(linedata):
    begin=0
    end=0
    for index in range(len(linedata)):
        if linedata[index]=='$':
            if linedata[index:index+5]!='$GNRMC':
                return linedata[index:]
            else:
                begin=index
        if linedata[index]=='V' and linedata[index+1]=='*' and begin!=0:
            end=index+4
            return linedata[begin:end]
    return ''


def processdata2(linedata):
    for index in range(len(linedata)):
        if linedata[index]=='$':
            if linedata[index:index+6]=='$GNRMC' or linedata[index:index+6]=='$GNGGA':
                return linedata[index:]
    return ''


def inject():
    global rtcmWave
    global finish
    global ggaData
    global newGgaData
    global newRtcmWave
    global clearStack
    init=False
    server='ntrip.data.gnss.ga.gov.au'
    port=2101
    username='chenxinhu2000@gmail.com'
    password='Hu11221314/'
    mountpoint='SALT00AUS0'
    dummyNMEA='NMEA2.00'
    pwd = base64.b64encode("{}:{}".format(username, password).encode('ascii'))
    pwd = pwd.decode('ascii')
    header = \
    "GET /{} HTTP/1.1\r\n".format(mountpoint) + \
    "Host: {}\r\n".format(server) + \
    "Ntrip-Version: Ntrip/2.0\r\n" + \
    "User-Agent: ntrip.py/0.1\r\n" + \
    "Connection: close\r\n" + \
    "Authorization: Basic {}\r\n\r\n".format(pwd)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, int(port)))
    s.send(header.encode('ascii'))
    init=False
    #print("Waiting answer...\n")
    data = s.recv(2048).decode('ascii')
    print(data)
    #dummyHeader = \
    #"Ntrip-GGA: {}\r\n".format(dummyNMEA)
    #fData=open('./rtcm1.txt','wb')
    beginTime=datetime.datetime.now()
    while finish==0:
        currentTime=datetime.datetime.now()
        diffTime=currentTime-beginTime
        if newGgaData and not init:
            print(ggaData.encode('utf-8'))
            s.send(ggaData.encode('utf-8'))
            init=True
        if init and diffTime.seconds>180:
            beginTime=currentTime
            dummyHeader = \
                "Ntrip-GGA: {}\r\n".format(ggaData)
            print(ggaData.encode('utf-8'))
            newGgaData=False
            #print(ggaData.encode('utf-8'))            
            s.send(ggaData.encode('utf-8'))
        data = s.recv(4096)
        #fData.write(data)
        #print(len(data))
        if clearStack:
            rtcmWave=data
            clearStack=False
        else:
            rtcmWave=data+rtcmWave
        newRtcmWave=True
    s.close()

def serialConnect():
    global rtcmWave
    global finish
    global ggaData
    global newGgaData
    global newRtcmWave
    global clearStack
    MyCom = serial.Serial("COM5",9600,timeout=0.5)
    data_ccc = 0
    f1 = open('./data/rtkOutput'+roundName+'.csv', 'w',newline = '')
    f2 = open('./data/gpsOutput'+roundName+'.csv', 'w',newline = '')
    f3 =open('./data/log'+roundName+'.txt','w',newline = '')
    f4=open('./data/oriLog'+roundName+'.txt','wb')
    #fData=open('./rtcm2.txt','wb')

    writer1 = csv.writer(f1)
    writer1.writerow(['lat','lng'])
    writer2 = csv.writer(f2)
    writer2.writerow(['lat','lng'])
    flag=1
    while True:
    #result = RTCMReader.parse(data)
        if rtcmWave!='' and newRtcmWave==True:
            MyCom.write(rtcmWave)
            #fData.write(rtcmWave)
            #print(rtcmWave)
            newRtcmWave=False
            clearStack=True
        newdata=MyCom.readline()
        f4.write(newdata)
        f3.write(newdata.decode('gbk',errors="ignore"))
        #newdata=newdata[:-2]
        newdata=newdata.decode('gbk', errors="ignore")
        newdata=processdata2(newdata)
        if newdata[0:6]=="$GNRMC":
            if flag==1:
                newmsg=pynmea2.parse(newdata)
                lat=newmsg.latitude
                lng=newmsg.longitude
                gps="Latitude=" +str(lat) + "and Longitude=" +str(lng)
                #print('count: '+str(data_ccc))
                print(gps)
                data_ccc = data_ccc+1
                writer1.writerow([lat,lng])
                flag=0
            else:
                flag=1
                newmsg=pynmea2.parse(newdata)
                lat=newmsg.latitude
                lng=newmsg.longitude
                gps="Latitude=" +str(lat) + "and Longitude=" +str(lng)
                #print('count: '+str(data_ccc))
                print(gps)
                data_ccc = data_ccc+1
                writer2.writerow([lat,lng])
            print(data_ccc)
        if newdata[0:6]=="$GNGGA":
            ggaData=newdata
            newGgaData=True
        if data_ccc >= 200:
            break
    MyCom.close()
    f1.close()
    f2.close()
    f3.close()
    finish=1




if __name__=="__main__":

    t1 = threading.Thread(target=inject)
    t2 = threading.Thread(target=serialConnect)
    t1.start()
    t2.start()


