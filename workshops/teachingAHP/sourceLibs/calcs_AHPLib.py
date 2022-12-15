from asyncio import create_subprocess_shell
from operator import matmul
from platform import node

from statistics import mode
from symbol import factor
from tempfile import tempdir
from tkinter.messagebox import NO
import numpy as np
import pandas as pd
import copy as cp
import operator as op
from matplotlib import pyplot as plt
#based on Bill Adams initial pyanp calculations

def matrixRaise2Power(matrixIn,power,rescale=False):
    last = cp.deepcopy(matrixIn)
    nextm = cp.deepcopy(matrixIn)
    count=1
    while count < power:
        np.matmul(last, last, nextm)
        if rescale:
            mmax=np.max(nextm)
            if mmax!=0:
                factor=1/mmax
                np.multiply(nextm,factor,nextm)
        tmp = last
        last = nextm
        nextm = tmp
        count *= 2
    return last

def normalize(matrixIn):
    div = matrixIn.sum(axis=0)
    for i in range(len(div)):
        if div[i] == 0:
            div[i] = 1.0
    matrixOut=matrixIn/div
    return matrixOut

def calcStart(matrixIn):
    #By Bill Adams
    n=len(matrixIn)
    if n<=0:
        # no entries...so go with 1
        return 1
    epsilon=1/(20*n)
    small_entries=[]
    for row in matrixIn:
        for val in row:
            if(np.abs(val) <epsilon) and(val!=0):
                small_entries.append(np.abs(val))
    if len(small_entries) <=0:
        # no entries
        return 20*n*n+10
    avg_smalls=np.mean(small_entries)
    A=1/avg_smalls
    start_power=int(A) *n*n
    return start_power

def columnDistance(matrix1, matrix2, temp1=None,temp2=None,temp3=None):
    #column normalize matrix1 and 2 and calculate the distance, temps hold the normalized version of the vectors
    temp1=temp1 if temp1 is not None else cp.deepcopy(matrix1)
    temp2=temp2 if temp2 is not None else cp.deepcopy(matrix1)
    temp3=temp3 if temp3 is not None else cp.deepcopy(matrix1)
    div1=matrix1.max(axis=0)
    div2=matrix2.max(axis=0)
    for i in range(len(div1)):
        if div1[i]==0:
            div1[i]=1
        if div2[i] ==0:
            div2[i]=1
    np.divide(matrix1, div1, temp1)
    np.divide(matrix2, div2, temp2)
    np.subtract(temp1, temp2, temp3)
    np.absolute(temp3, temp3)
    return np.max(temp3)

def calcLimitANP(matrixIn,model=None,error=1e-10, max_iters=5000):
    
    #matrixIn scaled supermatrix
    size=len(matrixIn)
    difference=0.0
    start_power=calcStart(matrixIn)
    start=matrixRaise2Power(matrixIn,start_power,rescale=True)
    print("start pow",start_power)
    raised_big_power=matrixRaise2Power(matrixIn,size)

    #not a hierarchy
    if np.count_nonzero(raised_big_power)==0:
        print("Matrix is a  Hierarchy ")
        return calcHierarchy(matrixIn)
   
    tmp1=cp.deepcopy(matrixIn)
    tmp2=cp.deepcopy(matrixIn)
    tmp3=cp.deepcopy(matrixIn)

    pows=[start]
    for i in range(size-1):
        print(np.matmul(matrixIn, pows[-1]))
        pows.append(np.matmul(matrixIn, pows[-1]))
        difference=columnDistance(pows[-1], pows[-2], tmp1, tmp2, tmp3)
        if difference<error:
            # Already converged, done
            mysum=pows[-1].sum(axis=0)
            for i in range(len(mysum)):
                if mysum[i]==0:
                    mysum[i]=1
            if model is not None:
                    model.limitmatrix=cp.deepcopy(pows[-1] /mysum)
            return pows[-1] /mysum
    for count in range(max_iters):
        nextp=pows[0]
        np.matmul(pows[-1], matrixIn, nextp)
        for i in range(len(pows) -1):
            pows[i] =pows[i+1]
        pows[-1] =nextp
        # Check convergence
        for i in range(len(pows) -1):
            difference=columnDistance(pows[i], nextp, tmp1, tmp2, tmp3)
            if difference<error:
                mysum=nextp.sum(axis=0)
                for i in range(len(mysum)):
                    if mysum[i] ==0:
                        mysum[i] =1
                print("Count was "+str(count))
                if model is not None:
                    model.limitmatrix=cp.deepcopy(nextp/mysum)
                return nextp/mysum    
    raise ValueError("Did not converge")


def calcHierarchy(matrixIn,model=None):
    size=len(matrixIn)
    raised_big_power=matrixRaise2Power(matrixIn,size)
    #not a hierarchy
    if np.count_nonzero(raised_big_power)!=0:
        print("Matrix not a  Hierarchy ")
        return None
    #initialize
    total=cp.deepcopy(matrixIn)
    this_power=cp.deepcopy(matrixIn)
    next_power=cp.deepcopy(matrixIn)
    #raise to powers and sum up
    for i in range(size-2):
        np.matmul(this_power,matrixIn,next_power)
        np.add(total,next_power,total)
        temp=this_power
        this_power=next_power
        next_power=temp
    result=normalize(total)
    if model is not None:
        model.limitmatrix=cp.deepcopy(result)
    return result
def harkerFix(matrixIn):
    nrows = matrixIn.shape[0]
    ncols = matrixIn.shape[1]
    fixed = matrixIn.copy()
    for row in range(nrows):
        val = 1
        for col in range(ncols):
            if col != row and matrixIn[row,col]==0:
                val+=1
        fixed[row,row]=val
    return(fixed)
def priorityVector(matrixIn,harker=True,error:float = 1e-10):
    if matrixIn is None or matrixIn.shape==(0,0):
        # Eigen vector of the empty matrix is []
        return np.array([])
    if harker:
        matrixIn = harkerFix(matrixIn)
    size = matrixIn.shape[0]

    #Create our return value
    vec = np.ones([size])
    diff = 1
    while diff > error:
        nextv = np.matmul(matrixIn, vec)
        nextv = nextv/sum(nextv)
        diff = max(abs(nextv - vec))
        vec = nextv
   
    return(vec)

def nodeNameList(model):
    nodesAll=model.getNodeListFromClusters()
    nodeNum=len(nodesAll)
    nodeNames=[]
    for nodeCol in sorted(nodesAll, key=op.attrgetter('order')):
        nodeNames.append(nodeCol.name)
    return nodeNames
def pwcMatrixCol(model,nodeCol,nodeRow):
    pcMat=0
    for cluster in sorted( model.clusters, key=op.attrgetter('order')):
        for nodeFrom in sorted(cluster.nodes, key=op.attrgetter('order')): 
            connectedClusters=model.retAllClusterConnectionsFromNode(nodeFrom.name)
            for clusterPWC in sorted(connectedClusters, key=op.attrgetter('order')):
                pcMat=0
                for nodeA in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                    
                    if nodeFrom.nodeID==nodeCol.nodeID and nodeA.nodeID==nodeRow.nodeID:
                        return pcMat
                    if(nodeA in nodeFrom.connectedTo):
                        pcMat+=1
    return -1

def pwcMatrixRow(model,nodeCol,nodeRow):
    pcMatR=0
    for cluster in sorted( model.clusters, key=op.attrgetter('order')):
        for nodeFrom in sorted(cluster.nodes, key=op.attrgetter('order')): 
            connectedClusters=model.retAllClusterConnectionsFromNode(nodeFrom.name)
            for clusterPWC in sorted(connectedClusters, key=op.attrgetter('order')):
               
                for nodeA in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                    
                    if nodeFrom.nodeID==nodeCol.nodeID and nodeA.nodeID==nodeRow.nodeID:
                        return pcMatR
                pcMatR+=1

    return -1                   

def calcUnweightedSuperMatrix(model):
    nodesAll=model.getNodeListFromClusters()
    nodeNum=len(nodesAll)
    super=np.zeros([nodeNum,nodeNum])
    for matrixIn in model.all_pc_matrices:
        eigen=priorityVector(matrixIn)
        model.all_pr_vectors.append(eigen)
    
    col=0



    for nodeCol in sorted(nodesAll, key=op.attrgetter('order')):
        row=0

        for nodeRow in sorted(nodesAll, key=op.attrgetter('order')):
            if nodeRow in nodeCol.connectedTo:
                pwcR=pwcMatrixRow(model,nodeCol,nodeRow)
                pwcC=pwcMatrixCol(model,nodeCol,nodeRow)
                super[row][col]= model.all_pr_vectors[pwcR][pwcC]
            row+=1
        col+=1
        
    print(super)
    model.supermatrix=cp.deepcopy(super)
    return super
def calcWeightedSupermatrix(model):
    weight=normalize(model.supermatrix)
    model.weighted_supermatrix=cp.deepcopy(weight)
    return weight
def calcLimitingPriorities(supermatrixIn):
    size=len(supermatrixIn)
    raised_big_power=matrixRaise2Power(supermatrixIn,size)
    limiting=[]
    #not a hierarchy
    if np.count_nonzero(raised_big_power)!=0:
        print("Matrix not a  Hierarchy ")
        #calc limit matrix
    else:
        result=calcHierarchy(supermatrixIn)
        limiting=result[0:size,0]
    print(limiting)
    return limiting

def calcPrioritiesNormalizedByCluster(supermatrixIn,model):
    size=len(supermatrixIn)
    raised_big_power=matrixRaise2Power(supermatrixIn,size)
    limiting=[]
    nodesAll=model.getNodeListFromClusters()
    nodeNum=len(nodesAll)
    byCluster=np.zeros(nodeNum)
    #not a hierarchy
    if np.count_nonzero(raised_big_power)!=0:
        print("Matrix not a  Hierarchy ")
        #calc limit matrix
    else:
        result=calcHierarchy(supermatrixIn)
        limiting=result[0:size,0]
    
    nodesbefore=0
    
    for cluster in sorted(model.clusters, key=op.attrgetter('order')):
        
        i=0
        cl=0
        sum=0.000
        for node in sorted(cluster.nodes, key=op.attrgetter('order')):
            sum+=limiting[i+nodesbefore]
            # print("lim",limiting[i+nodesbefore],"--",i+nodesbefore)
            i+=1
        # print("sum",sum)
        i=0
        for node in sorted(cluster.nodes, key=op.attrgetter('order')):
            if sum!=0:
                # print("lim",limiting[i+nodesbefore])
                limiting[i+nodesbefore]=limiting[i+nodesbefore]/sum
                byCluster[i+nodesbefore]=limiting[i+nodesbefore]
    
                # print("lim",limiting[i+nodesbefore])
            i+=1
        nodesbefore+=len(cluster.nodes)
    # print(byCluster)  
      
    return byCluster  

def calcPrioritiesOfCluster(supermatrixIn,clusterName,model):
    size=len(supermatrixIn)
    raised_big_power=matrixRaise2Power(supermatrixIn,size)
    limiting=[]
   
    #not a hierarchy
    if np.count_nonzero(raised_big_power)!=0:
        print("Matrix not a  Hierarchy ")
        #calc limit matrix
    else:
        result=calcHierarchy(supermatrixIn)
        limiting=result[0:size,0]
    start=0
    for cluster in sorted(model.clusters, key=op.attrgetter('order')):
        if clusterName==cluster.name:
            sum=0.0
            i=0
            synth=np.zeros(len(cluster.nodes))
            for node in sorted(cluster.nodes, key=op.attrgetter('order')):
                sum+=limiting[start+i]
                # print(sum)
                i+=1
            row=0
            for node in sorted(cluster.nodes, key=op.attrgetter('order')):
                if sum!=0.0:
                    # print("!",limiting[row+start])
                    synth[row]=limiting[start+row]/sum
                    # print("@",synth[row])
                    row+=1
        start+=len(cluster.nodes)
    
    print("Synthesized results:",synth)
    return synth

def sensitivityCellSupermatrix(matrixIn,nodeNum):
    influence=np.arange(0.0, 1.1, 0.1)
    
    for i in range(0,len(influence)):
        working_matrix=cp.deepcopy(matrixIn)
        working_matrix[nodeNum][0]=influence[i]
        # print(working_matrix)
        # working_matrix=normalize(working_matrix)
        super=calcHierarchy(working_matrix)
        print(influence[i],"--",super[:,0])

def sensitivityCellSupermatrixShort(matrixIn,nodeNum,clusterName,model):
    influence=np.arange(0.0, 1.1, 0.1)
    points=[]
    for i in range(0,len(influence)):
        working_matrix=cp.deepcopy(matrixIn)
        working_matrix[nodeNum][0]=influence[i]
        # print(working_matrix)
        # working_matrix=normalize(working_matrix)
        super=calcHierarchy(working_matrix)
        # print(influence[i],"--",super[:,0])
        print(influence[i])
        points.append(calcPrioritiesOfCluster(super,clusterName,model))
    return points

def sensitivityCellSupermatrixPlot(matrixIn,nodeNum,clusterName,model):
    points=sensitivityCellSupermatrixShort(matrixIn,nodeNum,clusterName,model)
    plt.plot(points)
    plt.show()