#Author Name: Swapnil Suresh Chaughule
#Author Email: SwapnilSuresh_Chaughule@student.uml.edu

import socket
import binascii
import time
import threading
import random
import json
import sys

#Definition of class

class myThread(threading.Thread):
    def __init__(self,method,name):
        threading.Thread.__init__(self, target = method)
        self.name = name
        self.start()
        print "Thread initiated by "+name

#Definition of methods


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


#Code to collect the file

def collector():
    global name
    global window
    clooper = 0
    fvar = open(name,"wb")
    while True:
        if clooper>=len(window):
            print "loop is breaking"
            break
        fvar.write(window[clooper])
        #print "written"
        clooper = clooper + 1
    fvar.close()
    print "file closed"


    
#Code for the get pack and send pack

def servergetsend():
    global machinesocket
    global machinename
    global machineport
    global window
    global windowbase
    global message
    global corrupt
    global inputdata
    i = 0
    sendmypacket = 1
    same = 0
    while True:
        same = 0
        sendmypacket = 1
        #print "value of i is ",i
        ackcksm = check(binascii.a2b_hex("1234"))
        #print "\n\n"
        message,address = machinesocket.recvfrom(20000)
        #print "message of size ",sys.getsizeof(message)
        if message == "!@#$%":
            print message
            print "loop broken"
            collector()
            break
        seq,cksmrcv,data = degenerate(message)
        #print "seq recv is ", seq
        #print "cksm recv is ", cksmrcv
        cksm = check(data)
        #print "cksm expected is", cksm
        #print "seq expected is ", windowbase
        '''if seq< windowbase and cksm == cksmrcv:
            print "windowbase when seq no equal",windowbase
            message = generate(seq, ackcksm, binascii.a2b_hex("1234"))
            machinesocket.sendto(message, (machinename, machineport))
            print "ack sent for previous"
            same = 1'''
        '''if seq > windowbase and cksmrcv == cksm and same == 0:
            message = generate(windowbase, ackcksm, binascii.a2b_hex("1234"))
            machinesocket.sendto(message,(machinename,machineport))'''
        if seq == windowbase and cksm == cksmrcv:
            if i==len(corrupt):
                i = 0
            if inputdata == "2" and corrupt[i]==seq:
                ackcksm = 1234567890
                i = i + 1
                #print "-----Ack error-----"
            if inputdata == "4" and corrupt[i]==seq:
                sendmypacket = 0
                #print "-----Ack loss-----"
                i = i + 1
            message = generate(windowbase, ackcksm, binascii.a2b_hex("1234"))
            if sendmypacket == 1:
                machinesocket.sendto(message,(machinename,machineport))
                #print "ack sent"
            windowbase = seq + 1
            window.append(data)
        #else:
            #print "Data packet error or Ack error or something is wrong"
            
            


#Code for initialization

machinename = socket.gethostname()
machineport = 5057
omachineport = 5056
machinesocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#socket object is initialised
machinesocket.bind((machinename, omachineport))#binds to the port
#machinesocket.settimeout(3)#setting a timeout value
print "Server is ready"
window = []
windowbase = 0
windowend = 4
flag = 0
dp = 1
message = ""
ackmessage = ""
breaker = 0
lock = threading.Lock()
name = "Clientsidefile.jpg"#Name of the Image recived



#Code for main
inputdata, address = machinesocket.recvfrom(2000)
error, address = machinesocket.recvfrom(5000)
corrupt = json.loads(error)
print corrupt
time.sleep(2)

thread1 = myThread(servergetsend,"Thread-1")




