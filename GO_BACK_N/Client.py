#Author Name: Swapnil Chaughule
#Author Email: SwapnilSuresh_Chaughule@student.uml.edu

import socket
import binascii
import time
import threading
import random
import json
import sys
#aCK ERROR SHOULD ALWAYS BE LESS THAN 5%
#Definition of class

class myThread(threading.Thread):
    def __init__(self,method,name):
        threading.Thread.__init__(self, target = method)
        self.name = name
        self.start()
        print "Thread initiated by "+name
        


#Definitions of methods


#Code for the method of checksum

def check(methoddata):
    din = binascii.b2a_hex(methoddata)
    #print len(din)
    length = len(din)-1
    #print "length dive",length/1234
    strdin = ""#initializes a blank string variable
    i = 1
    while True:
        if i >= length :
            break
        strdin = strdin + din[i]
        #print strdin
        i = i+2
        #print "i is",i
    variable = int(strdin,16)
    variable1 = variable>>4#operation for checksum
    variable1 = variable1 + variable#operation for checksum
    variable2 = variable1 & 0xffff#operation for getting only last 16 bits
    return variable2#returns the value of checksum


#Code for the method of degeneration

def degenerate(messagestr):
    length = len(messagestr)
    loop1 =0
    loop2= 0
    loop3 =0
    sequencestr = ""
    checksm = ""
    datastr = ""
    while True:
        loop1 = loop1+1
        if messagestr[loop1-1] != "|":
            sequencestr = sequencestr+messagestr[loop1-1]
        else:
            loop2=1
            #print "loop1 is broken"
            break
    while True:
        loop1 = loop1+1
        if loop2==1 and messagestr[loop1-1] != "|":
            checksm = checksm+messagestr[loop1-1]
        else:
            loop3=1
            #print "loop 2 is broken"
            break
    while True:
        loop1 = loop1+1
        if loop1-1<length:
            datastr = datastr + messagestr[loop1-1]
            #print "data is "+datastr
        else:
            #print "loop 3 is broken"
            break
    sequence = int(sequencestr)#converts string into integers
    #print "sequence is "+sequencestr
    methcksm = int(checksm)#converts string into integer
    #print "checksum is "+checksm
    packetdata = binascii.a2b_hex(datastr)#converts ascii hexadecimal to binary
    #print "end degeneration"
    return sequence,methcksm,packetdata#returns the value of sequence number,checksum and packet data



#Code for the method of generate

def generate(sequence, methcksm, packetdata):
    sequencestr = str(sequence)#converts integer to string
    checksm = str(methcksm)#converts integer to string
    datastr = binascii.b2a_hex(packetdata)
    messagestr = sequencestr+"|"+checksm+"|"+datastr#Add all the strings together with the separator "|"
    #print messagestr
    #print "end generation"
    return messagestr#returns the string 


#Code to spilt the file

def spliter(name):
    fvar = open(name,"rb")
    wtemp = []
    loopcount = 0
    while True:
        dtemp = fvar.read(500)
        if not dtemp:
            break
        wtemp.append(dtemp)
        loopcount = loopcount+1
    print "length of window is ",len(wtemp)
    fvar.close()
    return wtemp

#Code to decide which packet to corrupt

def corruptor(vstr):
    global window
    vint = int(vstr)
    packeterror = (vint*len(window))/100
    wtemp = []
    if packeterror<=0:
        wtemp = [0xffffff]
        return wtemp
    clooper1 = 0
    clooper2 = 0
    while clooper1<=packeterror-1:
        wtemp.append(random.randrange(0,len(window)-1))
        while clooper2<clooper1:
            if wtemp[clooper1] == wtemp[clooper2]:
                del wtemp[clooper1]
                clooper1 = clooper1 - 1
            clooper2 = clooper2 + 1
        clooper1 = clooper1 + 1
        clooper2 = 0
    wtemp.sort()
    print wtemp
    return wtemp









#Code to send the data
def clientgosend():
    global machinesocket
    global machinename
    global machineport
    global window
    global windowbase
    global windowend
    global windowsize
    global flag
    global lastsentpack
    global corrupt
    global inputdata
    global sendmypacket
    lastsentpack = 0
    
    i = 0
    #print "L out",lastsentpack
    while True:
        #print "thread alivne sender", threading.active_count()
        sendmypacket = 1
        if lastsentpack<= windowend and flag == 1 and lastsentpack<len(window):
            #print "last sent pack ", lastsentpack
            cksm = check(window[lastsentpack])
            if inputdata == "3" and corrupt[i]==lastsentpack:
                cksm = 0
                i = i + 1
                if i == len(corrupt):
                    i = 0
                #print "error in the packet ",lastsentpack
            message = generate(lastsentpack,cksm,window[lastsentpack])
            if inputdata == "5" and corrupt[i]==lastsentpack:
                sendmypacket = 0
                i = i + 1
                if i == len(corrupt):
                    i = 0
                #print "packet dropped for ",lastsentpack
            if sendmypacket == 1:
                #print "packet size ",sys.getsizeof(message)
                with lock:
                    machinesocket.sendto(message,(machinename,machineport))
                #print "packet sent"
                #print lastsentpack
                #print cksm
            lastsentpack = lastsentpack + 1
        if windowbase == len(window) and lastsentpack == len(window):
            print "sender broken"
            break


#Code to get the data
def clientgoget():
    global machinesocket
    global window
    global windowbase
    global windowend
    global windowsize
    global inputdata
    global corrupt
    global flag
    global lastsentpack
    global sendmypacket
    global start
    seq = 0
    while True:
        try:
            ackmsg,address = machinesocket.recvfrom(2500)
        except:
            #print "socket timedout"
            with lock:
                lastsentpack = windowbase
                flag = 1
        else:
            with lock:
                flag = 0
            seq,cksmrcv,ack = degenerate(ackmsg)
            cksm = check(ack)
            if seq>=windowbase and cksm == cksmrcv:
                #print "ack recieved for ",seq
                with lock:
                    windowbase = seq + 1
                    windowend = windowsize + windowbase
                #print "window end ",windowend
                #print "window base ",windowbase
#Author: Swapnil Chaughule
                if windowend>=len(window):
                    windowend = len(window)-1
                flag = 1
            else:
                #print "timeout or error in packet "
                with lock:
                    windowbase = seq
                    lastsentpack = windowbase
                    flag = 1
        #print "threads alive ",threading.active_count()
        if seq == len(window)-1:
            with lock:
                sendmypacket = 0
                #print "sendmypacket ",sendmypacket
                #print "reciever break"
                machinesocket.sendto("!@#$%",(machinename,machineport))
                machinesocket.close()
                end = time.time()
                print "time to implement is ",end-start
                break
                




    


#Initialization of variables

machinename = socket.gethostname()#gets the name of the host machine
machineport = 5056
omachineport = 5057
machinesocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#socket object is initialised
machinesocket.bind((machinename, omachineport))#binds to the port
machinesocket.settimeout(0.6)#setting a timeout value
print "Client is ready"
window = []
windowbase = 0
strsize = raw_input("Enter window size")
windowsize = int(strsize)-1
windowend = windowsize
slider = windowend - windowbase
flag = 1
lastsentpack = -1
lock = threading.Lock()
name = "ClientImg7.jpg"#Name of the image 
corrupt = []
sendmypacket = 1
#Code to make the decision
inputdata = raw_input("Option 1 - normal operation or Option 2 - Ack packet error or Option 3 - Data packet error or Option 4 - Ack packet loss or Option 5 - Data packet loss/n")
#inputdata = "1"

#Code for main

window = spliter(name)
print "window read"
if inputdata != "1":
    machinesocket.sendto(inputdata,(machinename,machineport))
    percentage = raw_input("Enter percentage of error/n")
    corrupt = corruptor(percentage)
    machinesocket.sendto(json.dumps(corrupt),(machinename,machineport))
    time.sleep(2)
else:
    machinesocket.sendto(inputdata,(machinename,machineport))
    corrupt = [0xffffff]
    machinesocket.sendto(json.dumps(corrupt),(machinename,machineport))
    time.sleep(2)

start = time.time()
print "Start time is ",start

thread1 = myThread(clientgosend,"Thread-1")
thread2 = myThread(clientgoget,"Thread-2")
