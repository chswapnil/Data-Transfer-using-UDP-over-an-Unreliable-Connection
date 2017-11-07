#Author Name: Swapnil Chaughule
#Author Email: SwapnilSuresh_Chaughule@student.uml.edu

import socket
import binascii
import sys
import time
import os

#Code for the method to corrupt the data

def corruptor(datatobecorrupted):
    datacorrupt = binascii.b2a_hex(datatobecorrupted)#converts binary to hexadecimal ascii
    corrupteddata = int(datacorrupt,16) + 0xaf35#corrupting data here
    corrupteddatastr = hex(corrupteddata)
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
    corrupt = binascii.a2b_hex(corrupteddatastr)#converts hexadecimal ascii to binary
    return corrupt


#Code for the method of checksum

def check(methoddata):
    din = binascii.b2a_hex(methoddata)
    print len(din)
    length = len(din)-1
    #print "length dive",length/1234
    strdin = ""
    i = 1
    while True:
        if i >= length :
            break
        strdin = strdin + din[i]
        #print strdin
        i = i+2
        #print "i is",i
    variable = int(strdin,16)
    variable1 = variable>>4
    variable1 = variable1 + variable
    variable2 = variable1 & 0xffff
    return variable2

#Code for the method of degeneration

def degenerate(messagestr):
    print "degeneration"
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
    sequence = int(sequencestr)
    #print "sequence is "+sequencestr
    methcksm = int(checksm)
    #print "checksum is "+checksm
    packetdata = binascii.a2b_hex(datastr)
    print "end degeneration"
    return sequence,methcksm,packetdata



#Code for the method of generate

def generate(sequence, methcksm, packetdata):
    print"in generation"
    sequencestr = str(sequence)
    checksm = str(methcksm)
    datastr = binascii.b2a_hex(packetdata)
    messagestr = sequencestr+"|"+checksm+"|"+datastr
    #print messagestr
    print "end generation"
    return messagestr



#Code for initialzing

servername = socket.gethostname()#getting the host machine name
routerport = 11179
port = 11180
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#creating socket object
serversocket.bind((servername, routerport))#binding the socket object
serversocket.settimeout(5)#setting the timeout value of 10 seconds
print"Server is ready to recieve"
i = 0
filename = "ServerImg.jpg"
p = open('Client_sent_Img.jpg', "wb")#opening a blank writable file in a variable 
seq = 0
j=0
corrutnumb = 0
previousmessage = ""
duplication = 0
delay = 1
inputdatatype = ""
#time.sleep(3)

#Code to recieve
print "Do you want to recieve"
inputdatattype = raw_input()



#Code to recieve the file


while True :
    try:
        message, routeraddress = serversocket.recvfrom(1030)#recieving data from the sender
    except:
        print "message has been lost and server timedout"
        cksm = check(binascii.b2a_hex('1234'))
        message = generate(seq^1, cksm, binascii.b2a_hex('1234'))
        serversocket.sendto(message,routeraddress)
    else:
        
        print "message size is",sys.getsizeof(message)#get the size of the message in bytes
        if message == "!@#$%":
            print"loop broken";break
        seqrcv , cksmrcv, data1 = degenerate(message)#separating the message respective data
        print seqrcv 
        print cksmrcv
        if message == previousmessage:#checking for duplication
            print "duplicate packet recieved"
            duplication = 1
            cksm = check(binascii.b2a_hex('1234'))#calling checking
            message = generate(seqrcv, cksm, binascii.b2a_hex('1234'))
            print "message size is",sys.getsizeof(message)
            serversocket.sendto(message,routeraddress)#sending data to the sender
        else:
            duplication = 0
        #print " list has been converted and data is converted back to binary"
        cksm = check(data1)
        print "cksm before if else loop",cksm
        previousmessage = message
        if cksm == cksmrcv and seq == seqrcv and duplication == 0:
            p.write(data1)
            print"packet recieved is uncorrupted"
            print "checksum is going to get implemented"
            cksm = check(binascii.b2a_hex('1234'))
            message = generate(seqrcv, cksm, binascii.b2a_hex('1234'))
            print "message size is",sys.getsizeof(message)
            print seqrcv
            print cksm
            serversocket.sendto(message,routeraddress)
            print "uncorrupted ack sent"
            seq = seqrcv^1#flipping the sequence number
            print "sequence is flipped",seq," sequence is recieved ",seqrcv
        elif duplication == 0:
            cksm = check(binascii.b2a_hex('1234'))
            print "corruptd cksm"
            message = generate(seqrcv^1, cksm, binascii.b2a_hex('1234'))
            print "ackmessage send size is",sys.getsizeof(message)
            print seqrcv^1
            print cksm
            serversocket.sendto(message,routeraddress)
            print "corrupted ack sent"
        i=i+1
        if i == 50:
            break
        print i

print "file recieved"
p.close()#closing the file
print "file closed"
print "loop 1 count " , i



serversocket.close()#closing the socket
print "Socket closed"
