from random import *
from math import *
from time import *
from os import path
from pprint import *

currentTime=strftime("%b%d%Y_%Hh%Mm", localtime())

fieldSize=[32,32,16,16,8]
rangeData=[]
dirPathName='./ACLRuleSet/'
FileName='acl2_10k'

fop=open(FileName,'r')
tempData=fop.readlines()
#print('readline=',tempData)
fop.close()
tuple5=[] #5 tuples with range extension    
for i in range(len(tempData)):
    #print(i)
    tuple5.append([])
    rangeData.append([])
    localTemp=tempData[i].replace('@','').split('\t')
 #   print('LocalTemp=',localTemp)
    srcAddr=localTemp[0].split('/')[0].split('.')
  #  print('Source=',srcAddr)
    srcMask=localTemp[0].split('/')[1]
   # print('SourceMask=',srcMask)
    dstAddr=localTemp[1].split('/')[0].split('.')
    #print('Dst=',dstAddr)
    dstMask=localTemp[1].split('/')[1]
    #print('DstMask=',dstMask)
    srcRang=localTemp[2].split(' : ')
   # print('SrcRange=',srcRang)
    rangeData[i].append(srcRang)
    dstRang=localTemp[3].split(' : ')
   # print('DstRange=',dstRang)
    rangeData[i].append(dstRang)
    protocol=int(localTemp[4].split('/')[0],16)
    #print ('protocol=',protocol)
    prtMask=int(localTemp[4].split('/')[1],16)
    #print('PrtMask=',prtMask)
    #Source Address
    srcAddrString=''
    saLen=len(srcAddr)
    #print('saLen=',saLen)
    for j in range(saLen):
        temp=bin(int(srcAddr[j]))[2:]
        tLen=len(temp)
        if tLen<8:
            temp='0'*(8-tLen)+temp
        srcAddrString=srcAddrString+temp
    for j in range(int(srcMask),32):
        srcAddrString=srcAddrString[0:j]+'*'+srcAddrString[(j+1):]           
    tuple5[i].append(srcAddrString)
    #Destination Address
    dstAddrString=''
    daLen=len(dstAddr)
    for j in range(daLen):
        temp=bin(int(dstAddr[j]))[2:]
        tLen=len(temp)
        if tLen<8:
            temp='0'*(8-tLen)+temp
        dstAddrString=dstAddrString+temp
    for j in range(int(dstMask),32):
        dstAddrString=dstAddrString[0:j]+'*'+dstAddrString[(j+1):]            
    tuple5[i].append(dstAddrString)
    #Source Port
    if srcRang[0]==srcRang[1]:
        temp=bin(int(srcRang[1]))[2:]
        tLen=len(temp)
        srcRangStr='0'*(fieldSize[2]-tLen)+temp
        tuple5[i].append(srcRangStr)
    else:
        temp0=bin(int(srcRang[0]))[2:]
        temp1=bin(int(srcRang[1]))[2:]
        tLen0=len(temp0)
        tLen1=len(temp1)           
        if tLen0==tLen1:
            xorValue=int(srcRang[0])^int(srcRang[1])
            tLen2=len(bin(xorValue)[2:])
            srcRangStr='0'*(fieldSize[2]-tLen1)+temp1[:(tLen1-tLen2)]+'*'*tLen2
        else:    
            srcRangStr='0'*(fieldSize[2]-tLen1)+'*'*tLen1
        tuple5[i].append(srcRangStr)
    #Destination Port 
    if dstRang[0]==dstRang[1]:
        temp=bin(int(dstRang[1]))[2:]
        tLen=len(temp)
        dstRangStr='0'*(fieldSize[3]-tLen)+temp
        tuple5[i].append(dstRangStr)
    else:
        temp0=bin(int(dstRang[0]))[2:]
        temp1=bin(int(dstRang[1]))[2:]
        tLen0=len(temp0)
        tLen1=len(temp1)
        if tLen0==tLen1:
            xorValue=int(dstRang[0])^int(dstRang[1])
            tLen2=len(bin(xorValue)[2:])
            dstRangStr='0'*(fieldSize[3]-tLen1)+temp1[:(tLen1-tLen2)]+'*'*tLen2
        else:    
            dstRangStr='0'*(fieldSize[3]-tLen1)+'*'*tLen1
        tuple5[i].append(dstRangStr)
    # Protocol
    prtStr=bin(protocol)[2:]
    tLen=len(prtStr)
    if tLen<fieldSize[4]:
        prtStr='0'*(fieldSize[4]-tLen)+prtStr
    for j in range(prtMask,fieldSize[4]):
        prtStr=prtStr[0:j]+'*'+prtStr[(j+1):]       
    tuple5[i].append(prtStr)

#print (tuple5)
filename = 'acl2_10k_binary.txt'

with open(filename, mode="w") as outfile:  # also, tried mode="rb"
    for s in tuple5:
        outfile.write("%s\n" % s)
