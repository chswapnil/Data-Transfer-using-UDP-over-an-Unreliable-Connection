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
    print "edn degeneration"
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

servername = socket.gethostname()
port = 11091
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversocket.bind((servername, 11090))
print"Server is ready to recieve"
i = 0
p = open('clientsideimage1.jpg', "wb")
seq = 0
j=0

#Code to recieve the file

while True :
    message, clientaddr = serversocket.recvfrom(2500)
    if message == "!@#$%":
        print"loop broken";break
    seqrcv , cksmrcv, data1 = degenerate(message)
    print " list has been converted and data is converted back to binary"
    cksm = check(data1)
    if cksm == cksmrcv and seq == seqrcv:
        p.write(data1)
        print"packet recieved is uncorrupted"
        print "checksum is going to get implemented"
        cksm = check(binascii.a2b_hex('1234'))
        message = generate(seqrcv, cksm, binascii.a2b_hex('1234'))
        serversocket.sendto(message,(servername,port))
        print "uncorrupted ack sent"
        seq = seqrcv^1
        print "sequence is flipped",seq,seqrcv
    else:
        cksm = check(binascii.a2b_hex('1234'))
        print "corruptd cksm"
        message = generate(seqrcv^1, cksm, binascii.a2b_hex('1234'))
        serversocket.sendto(message,(servername,port))
        print "corrupted ack sent"
    i=i+1
    print i

print "file recieved"
p.close()
print "file closed"
print "loop 1 count " , i



#Code to recieve the decision

data2, clientaddr = serversocket.recvfrom(10240)
print data2 + " is the clients decision to recieve the file"
print clientaddr


#Code to send the file

if (data2 == "Yes" or data2 == "yes" or data2 == "Y" or data2 == "y") :
    filename = "ServerImg.jpg"
    print filename + " is the name of the file the client wants to recieve"
    print "Sending file"
    i = 0
    p = open(filename, "rb")
    while True :
        if j==0:
            data1 = p.read(1024)
            print "packet has been read"
        if not data1:
            message="!@#$%";serversocket.sendto(message, (servername, port));print "main loop is broken";break
        cksm = check(data1)
        print "checksum is implemented"
        message = generate(seq, cksm, data1)
        serversocket.sendto(message, (servername, port))
        if not data1:
            print "There is no data in packet";break
        print "packet has been sent and waiting for acknowlegement"
        ackmessage, clientaddr = serversocket.recvfrom(2500)
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
    p.close()
    print "file closed"
    print "loop 2 count ", i
serversocket.close()
print "Socket closed"
    



