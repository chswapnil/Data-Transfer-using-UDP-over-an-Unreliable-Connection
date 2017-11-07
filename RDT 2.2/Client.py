#Author Name: Swapnil Chaughule
#Author Email: SwapnilSuresh_Chaughule@student.uml.edu

import socket
import sys
import binascii
import json


#Code for the method of checksum

def check(methoddata):
    din = binascii.b2a_hex(methoddata)
    variable = int(din,16)
    variable1 = variable>>8
    variable2 = variable1 & variable & 0xffff
    return variable2


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
            print "loop1 is broken"
            break
    while True:
        loop1 = loop1+1
        if loop2==1 and messagestr[loop1-1] != "|":
            checksm = checksm+messagestr[loop1-1]
        else:
            loop3=1
            print "loop 2 is broken"
            break
    while True:
        loop1 = loop1+1
        if loop1-1<length:
            datastr = datastr + messagestr[loop1-1]
            #print "data is "+datastr
        else:
            print "loop 3 is broken"
            break
    sequence = int(sequencestr)
    print "sequence is "+sequencestr
    methcksm = int(checksm)
    print "checksum is "+checksm
    packetdata = binascii.a2b_hex(datastr)
    print "end degeneration"
    return sequence,methcksm,packetdata



#Code for the method of generate

def generate(sequence, methcksm, packetdata):
    sequencestr = str(sequence)
    checksm = str(methcksm)
    datastr = binascii.b2a_hex(packetdata)
    messagestr = sequencestr+"|"+checksm+"|"+datastr
    #print messagestr
    print "end generation"
    return messagestr



#Code for initializing

clientname = socket.gethostname()
port = 11090
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.bind((clientname, 11091))
print "Client is ready"
i = 0
filename = "ClientImg.jpg"#Name of the image to transfer
f = open(filename , "rb")
seq = 0
j=0


#Code to send the file

print "We are at the sending end code"
while True :
    if j==0:
        data1 = f.read(1024)
        print "packet has been read"
    if not data1:
        message="!@#$%";clientsocket.sendto(message, (clientname, port));print "main loop is broken";break
    cksm = check(data1)
    print "checksum is implemented"
    message = generate(seq, cksm, data1)
    clientsocket.sendto(message, (clientname, port))
    if not data1:
        print "There is no data in packet";break
    print "packet has been sent and waiting for acknowlegement"
    ackmessage, serveraddr = clientsocket.recvfrom(2500)
    print "acknowledgement has been recieved"
    seqrcv,cksmrcv,ack = degenerate(ackmessage)
    cksm = check(ack)
    print "checksum for receiever"
    if cksm == cksmrcv and seq == seqrcv:
        j=0
        seq = seqrcv^1
        print "inside if loop"
    else:
        j=1
        print "inside else loop"
    i=i+1
    print i

f.close()
print "file closed"
print "loop 1 count " , i



#Code to send the decision

print "Do you want to recieve another image. Press(Yes/No)"
data2 = raw_input()
clientsocket.sendto(data2, (clientname, port))



#Code to receive the file

if(data2 == "Yes" or data2 == "yes" or data2 == "Y" or data2 == "y") :
    f = open("serversideimage1.jpg", "wb")
    print "In if loop"
    i = 0
    while True :
        message, serveraddr = clientsocket.recvfrom(2500)
        if message == "!@#$%":
            print"loop broken";break
        seqrcv , cksmrcv, data1 = degenerate(message)
        print " list has been converted and data is converted back to binary"
        cksm = check(data1)
        if cksm == cksmrcv and seq == seqrcv:
            f.write(data1)
            print"packet recieved is uncorrupted"
            print "checksum is going to get implemented"
            cksm = check(binascii.a2b_hex('1234'))
            message = generate(seqrcv, cksm, binascii.a2b_hex('1234'))
            clientsocket.sendto(message,(clientname,port))
            print "uncorrupted ack sent"
            seq = seqrcv^1
            print "sequence is flipped",seq,seqrcv
        else:
            cksm = check(binascii.a2b_hex('1234'))
            print "corruptd cksm"
            message = generate(seqrcv^1, cksm, binascii.a2b_hex('1234'))
            clientsocket.sendto(message,(clientname,port))
            print "corrupted ack sent"
        i=i+1
        print i
        
    f.close()
    print "File closed"
    print "loop 2 count ", i
clientsocket.close()
#print serveraddrs
print "Socket closed"

