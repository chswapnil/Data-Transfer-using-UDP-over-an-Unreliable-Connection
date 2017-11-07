#Author Name: Swapnil Chaughule
#Author Email: SwapnilSuresh_Chaughule@student.uml.edu

import socket
import random
import binascii
import time
import os


#Code for the method to corrupt the data

def corruptor(datatobecorrupted):
    datacorrupt = binascii.b2a_hex(datatobecorrupted)#converts data from binary to ascii in hex
    #print datacorrupt
    corrupteddata = int(datacorrupt,16) & 0xaf39
    corrupteddatastr = hex(corrupteddata) #converts integer to hexadecimal in string
    #print corrupteddatastr
    if corrupteddatastr[len(corrupteddatastr)-1] == "L":
        #print corrupteddatastr
        corrupteddatastr = corrupteddatastr[2:len(corrupteddatastr)-1]
        #print corrupteddatastr
        #print "consist of long"
    else:
        #print corrupteddatastr
        corrupteddatastr = corrupteddatastr[2:len(corrupteddatastr)]
        #print corrupteddatastr
        #print "doesnt has long in it"
    #print corrupteddatastr
    print len(corrupteddatastr)
    corrupt = binascii.a2b_hex(corrupteddatastr)#converts data from ascii hexadecimal to binary to 
    return corrupt #returns the value of corruptor where called


#Code for the method of checksum

def check(methoddata):
    din = binascii.b2a_hex(methoddata)
    print len(din)
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
    print "end degeneration"
    return sequence,methcksm,packetdata#returns the value of sequence number,checksum and packet data



#Code for the method of generate

def generate(sequence, methcksm, packetdata):
    sequencestr = str(sequence)#converts integer to string
    checksm = str(methcksm)#converts integer to string
    datastr = binascii.b2a_hex(packetdata)
    messagestr = sequencestr+"|"+checksm+"|"+datastr#Add all the strings together with the separator "|"
    #print messagestr
    print "end generation"
    return messagestr#returns the string 

#Code for random value
def decision(numb1,numb2,numb3):
    if numb1 <= 0:
        return 0
    temp = 0.0
    numb2 = numb2*100
    temp = numb2/numb1
    if temp < numb3:
        return 1
    else:
        return 0
    




#Code for initialization
routername = socket.gethostname()#gets the name of the host machine
clientport = 11178
port = 11179
router = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#socket object is initialised
router.bind((routername,clientport))

sequence = 0
cksm = 0
data = ""
ack = ""
perint = 1
inputdata = ""
nopc= 0
noac= 0
nopl= 0
noal= 0
psuc= 0
asuc= 0
pwol= 0
awol= 0
i=0
print "ROUTER IS READY TO BE USED"
print "Press 1-normal|Press 2-Ack loss|Press 3-Ack corrupt|Press 4-Packet corrupt|Press 5-Packet loss"
inputdata = raw_input()
if inputdata == "2" or inputdata == "3" or inputdata == "4" or inputdata == "5":
    print "Enter the percent of packets to be corrupted or lost"
    perstr = raw_input()
    perint = int(perstr)
    print "Percent is ",perint

while True:
    message, clientaddress = router.recvfrom(5000)
    if message == "!@#$%":
        router.sendto(message,(routername,port))
        print "router about to stop connection"
        break
    print "activator about to decide for packet"
    activator = decision(psuc,nopc,perint)
    if inputdata == "4" and activator == 1:
        print "corrupting packet"
        sequence,cksm,data = degenerate(message)
        data = corruptor(data)
        nopc = nopc + 1
        message = generate(sequence,cksm,data)
    else:
        psuc = psuc + 1
    activator = decision(pwol,nopl,perint)
    if inputdata == "5" and activator ==1:
        print "packet has been lost"
        nopl = nopl+1
    else:
        pwol = pwol + 1
        router.sendto(message,(routername,port))
    message, serveraddress = router.recvfrom(5000)
    print "activator about to decide for acknowledge"
    activator = decision(asuc,noac,perint)
    if inputdata == "3" and activator == 1:
        print "corrupting acknowledgement"
        sequence,cksm,ack = degenerate(message)
        ack = corruptor(ack)
        noac = noac + 1
        message = generate(sequence,cksm,ack)
    else:
        asuc = asuc + 1
    activator = decision(awol,noal,perint)
    if inputdata == "2" and activator == 1:
        print "acknowledgement has been lost"
        noal = noal+1
    else:
        awol = awol + 1
        router.sendto(message,clientaddress)
    i = i+1
    print "number of loop",i

print "percentage of packet loss ",((nopl*100)/pwol),"%"
print "percentage of packet corrupted ",((nopc*100)/psuc),"%"
print "percentage of acknowledgement loss ",((noal*100)/awol),"%"
print "percentage of acknowledgement uncorrupted ",((noac*100)/asuc),"%"
router.close()
