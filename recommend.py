__author__ = 'LiGe'
#encoding:utf-8
from numpy import *
from numpy import linalg as la

import math

def ecludSim(inA, inB):
    return 1.0/(1.0+la.norm(inA-inB))

def pearsSim1(inA, inB):
    if len(inA)<3:return 1.0
    return 0.5+0.5*corrcoef(inA,inB,rowvar=0)[0][1]

def cosSim(inA, inB):
    num=float(inA.T*inB)
    denom=la.norm(inA)*la.norm(inB)
    return 0.5+0.5*(num/denom)


def standEst(dataMat, user, simMeas, item,unrateditems):
    n=shape(dataMat)[1]
    m=shape(dataMat)[0]
    simTotal=0.0
    ratSimTotal=0.0
    similarity=0.0
    for j in range(n):
        if j not in unrateditems:
            userRating=dataMat[user,j]
            if userRating==0:continue
            overLap=nonzero(logical_and(dataMat[:,item].A>0,dataMat[:,j].A>0))[0]
            #print overLaps
            if len(overLap)==0:
                similarity=0
            else:
                #similarity=simMeas(dataMat[overLap,item],dataMat[overLap,j])
                similarity=float(len(overLap))/float(m)
            simTotal+=similarity
            #ratSimTotal+=similarity*userRating
    if simTotal==0:return 0
    #print ratSimTotal
    return float(simTotal)/float(n-len(unrateditems)+1)


def svdEst(dataMat, user, simMeas, item):
    n=shape(dataMat)[1]
    simTotal=0.0
    ratSimTotal=0.0
    U, Sigma, VT=la.svd(dataMat)
    Sig4=mat(eye(4)*Sigma[:4])
    xformedItems=dataMat.T*U[:,:4]*Sig4.I
    for j in range(n):
        userRating=dataMat[user,j]
        if userRating==0 or j==item:continue
        similarity=simMeas(xformedItems[item,:].T,xformedItems[j,:].T)
        simTotal+=similarity
        ratSimTotal+=similarity*userRating
    if simTotal==0:return 0
    return ratSimTotal/simTotal

def recommend(dataMat, user, N=3, simMeas=ecludSim, estMethod=standEst):
    unratedItems=nonzero(dataMat[user,:].A==0)[1]
    if len(unratedItems)==0: return None
    itemScores=[]
    for item in unratedItems:
        estimatedScore=estMethod(dataMat, user, simMeas, item,unratedItems)
        itemScores.append((item, estimatedScore))
    return sorted(itemScores, key=lambda jj:jj[1], reverse=True)[:N]

if __name__ == '__main__':
    myData=matrix()
   #print myData
    myMat=mat(myData)
    print myMat
    f=open('result.txt','w+')
    print "svdEst"
    result=list()
    for i in range(0,10000):
        unratedItems=nonzero(myMat[i,:].A==0)[1]
        number=10000-len(unratedItems)
        number=number/4
        result.append(recommend(myMat,i,number,cosSim,standEst))
        print i
    print result
    s=result.join('\n')
    f.write(s)
    f.close()


