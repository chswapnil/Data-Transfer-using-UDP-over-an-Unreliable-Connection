#Author Name: Swapnil Chaughule
#Author Email: SwapnilSuresh_Chaughule@student.uml.edu

import socket
import binascii
import sys
import time
import os

#Code for the method to corrupt the data

def corruptor(datatobecorrupted):
    datacorrupt = binascii.b2a_hex(datatobecorrupted)#converts data from binary to ascii in hex
    corrupteddata = int(datacorrupt,16) + 0xaf35
    corrupteddatastr = hex(corrupteddata) #converts integer to hexadecimal in string
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



#Code for initializing

clientname = socket.gethostname()#gets the name of the host machine
port = 11178

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#socket object is initialised
#clientsocket.bind((clientname, routerclientport))#binds to the port
clientsocket.settimeout(5)#setting a timeout value
print "Client is ready"
i = 0
filename = "ClientImg.jpg"
f = open(filename , "rb")#opening a file in a variable
seq = 0
j=0
corruptnumb = "0"


#Code for corruption
print "Do you want to start"
inputdatatype = raw_input()#taking a raw input for the options given
#time.sleep(1)


#Code to send the file


print "We are at the sending end code"
while True :
    if j==0:
        data1 = f.read(498)#reads the data in binary and stores in a variable
        print "packet has been read"
    if not data1:
        message="!@#$%";clientsocket.sendto(message, (clientname, port));print "main loop is broken";break
    cksm = check(data1)#checksum in implement on the data
    print "checksum is implemented"
    print seq
    print cksm
    message = generate(seq, cksm, data1)#calling this function to get a string message
    print "message size is",sys.getsizeof(message)#printing the size of the variable in bytes
    clientsocket.sendto(message, (clientname, port))
    print "packet has been sent and waiting for acknowlegement"
    try:
        ackmessage, routeraddress = clientsocket.recvfrom(1024)#waiting for acknowledgement
        print "ACK recieved"
    except:#if timedout the program raises an exception which is catched here
        print "Client timedout and no ACK recieved"
        j = 1
    else:
        print "ackmessage size is",sys.getsizeof(ackmessage)
        print "acknowledgement has been recieved"
        seqrcv,cksmrcv,ack = degenerate(ackmessage)#separating the string message into a data
        print "rec cksm ",cksmrcv
        cksm = check(ack)
        print "send cksm ",cksm
        if cksm == cksmrcv and seq == seqrcv:
            j=0
            seq = seqrcv^1#flipping the sequence number
            print "sequence has been changed"
        else:
            j=1
            print "sequence is the same"
    i=i+1
    if i == 50:
        break
    print i


f.close()#closing the file
print "file closed"
print "loop 1 count " , i
#os.remove(filename)



clientsocket.close()#closing the socket
#print serveraddrs
print "Socket closed"

