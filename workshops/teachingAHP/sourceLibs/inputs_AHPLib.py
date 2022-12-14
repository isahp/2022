from calendar import c
from platform import node
from re import T
from statistics import mode
import pandas as pd
import operator as op
import numpy as np
from pkgutil import ImpImporter
import structs_AHPLib  as cdf_str
import calcs_AHPLib as cdf_calc
import csv

import xlsxwriter


def genFullQuest(model,keyword,verb=False):
    questnr=[]
    for cluster in sorted( model.clusters, key=op.attrgetter('order')): 

        for nodeFrom in sorted(cluster.nodes, key=op.attrgetter('order')): 
            
            connectedClusters=model.retAllClusterConnectionsFromNode(nodeFrom.name)
            for clusterPWC in sorted(connectedClusters, key=op.attrgetter('order')):
                i=0
                qset=[]
                # print("Nodes:\n",clusterPWC.nodes)
                for nodeA in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                    j=0
                    # print("NodeA: ",nodeA.nodeID)
                    for nodeB in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                        # print("NodeB: ",nodeB.nodeID)
                        if (nodeA.nodeID!= nodeB.nodeID) and (i<j) and (nodeA in nodeFrom.connectedTo) and (nodeB in nodeFrom.connectedTo):
                            # print("{}-{}".format(i,j))
                            quest="With respect to {}, which one is more {}: {} or {} ? By how much?".format(nodeFrom.name, keyword, nodeA.name, nodeB.name)
                            if verb:
                                print(quest)
                            qset.append(quest)
                        j+=1
                    i+=1
                questnr.append(qset)
                if verb:
                    print("---------------------------------------------------------------------------\n")
    return questnr
def genFirstLineAboveDiagQuest(model,keyword,verb=False):
    questnr=[]
    for cluster in sorted( model.clusters, key=op.attrgetter('order')): 

        for nodeFrom in sorted(cluster.nodes, key=op.attrgetter('order')): 
            
            connectedClusters=model.retAllClusterConnectionsFromNode(nodeFrom.name)
            for clusterPWC in sorted(connectedClusters, key=op.attrgetter('order')):
                i=0
                qset=[]
                # print("Nodes:\n",clusterPWC.nodes)
                for nodeA in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                    j=0
                    # print("NodeA: ",nodeA.name)
                    for nodeB in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                        # print("NodeB: ",nodeB.name)
                        # print("{}-{}".format(i,j),nodeA in nodeFrom.connectedTo,nodeB in nodeFrom.connectedTo)
                        if (nodeA.nodeID!= nodeB.nodeID) and ((i==0)or (i+1==j)) and (nodeA in nodeFrom.connectedTo) and (nodeB in nodeFrom.connectedTo):
                            
                            quest="With respect to {}, which one is more {}: {} or {} ? By how much?".format(nodeFrom.name, keyword, nodeA.name, nodeB.name)
                            if verb:
                                print(quest)
                            qset.append(quest)
                        j+=1
                    i+=1
                questnr.append(qset)
                if verb:
                    print("---------------------------------------------------------------------------\n")
    return questnr
def genFirstLineQuest(model,keyword,verb=False):
    questnr=[]
    for cluster in sorted( model.clusters, key=op.attrgetter('order')): 

        for nodeFrom in sorted(cluster.nodes, key=op.attrgetter('order')): 
            
            connectedClusters=model.retAllClusterConnectionsFromNode(nodeFrom.name)
            for clusterPWC in sorted(connectedClusters, key=op.attrgetter('order')):
                i=0
                qset=[]
                # print("Nodes:\n",clusterPWC.nodes)
                nodeA=clusterPWC.nodes[0]
                j=0
                # print("NodeA: ",nodeA.name)
                for nodeB in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                    # print("NodeB: ",nodeB.name)
                    # print("{}-{}".format(i,j),nodeA in nodeFrom.connectedTo,nodeB in nodeFrom.connectedTo)
                    if (nodeA.nodeID!= nodeB.nodeID) and (i<j) and (nodeA in nodeFrom.connectedTo) and (nodeB in nodeFrom.connectedTo):
                        # print("{}-{}".format(i,j))
                        quest="With respect to {}, which one is more {}: {} or {} ? By how much?".format(nodeFrom.name, keyword, nodeA.name, nodeB.name)
                        if verb:
                            print(quest)
                        qset.append(quest)
                    j+=1
                questnr.append(qset)
                if verb:
                 print("---------------------------------------------------------------------------\n")
                
    return questnr

def genexport4QualtricsQuestFull(filepath,model,keyword,howMuch=True):
    count=1
    with open(filepath, 'w', encoding='UTF8',newline='') as f: 
        f.write("[[AdvancedFormat]]\n")
        for cluster in sorted( model.clusters, key=op.attrgetter('order')): 

            for nodeFrom in sorted(cluster.nodes, key=op.attrgetter('order')): 
                f.write("[[Block: With respect to: "+nodeFrom.name+"]]\n")
                connectedClusters=model.retAllClusterConnectionsFromNode(nodeFrom.name)
                for clusterPWC in sorted(connectedClusters, key=op.attrgetter('order')):
                    i=0

                    # print("Nodes:\n",clusterPWC.nodes)
                    for nodeA in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                        j=0
                        # print("NodeA: ",nodeA.nodeID)
                        for nodeB in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                            # print("NodeB: ",nodeB.nodeID)
                            if (nodeA.nodeID!= nodeB.nodeID) and (i<j) and (nodeA in nodeFrom.connectedTo) and (nodeB in nodeFrom.connectedTo):
                                # print("{}-{}".format(i,j))
                            
                                f.write("\n[[Question:MC:SingleAnswer]]\n")
                                quest1_csv=str(count)+'. With respect to '+nodeFrom.name+ ' which one is more '+keyword+':'+'\n'
                                f.write(quest1_csv) 
                                f.write("\n[[Choices]]\n")
                                
                                ans1=nodeA.name+'\n'
                                f.write(ans1)
                                ans2=nodeB.name+'\n'
                                f.write(ans2)
                                count+=1
                                
                                if(howMuch):
                                    f.write("\n[[Question:MC:Dropdown]]\n")
                                    quest2_csv=str(count)+". By how much?"+'\n'
                                    f.write(quest2_csv)
                                    f.write("\n[[Choices]]\n")
                                    f.write("1\n2\n3\n4\n5\n6\n7\n8\n9\n")
                                    count+=1
                                f.write('\n')
                                
                            j+=1
                        i+=1
def genexport4QualtricsFirstLineAboveDiagQuest(filepath,model,keyword,howMuch=True):
    count=1
    with open(filepath, 'w', encoding='UTF8',newline='') as f:
        f.write("[[AdvancedFormat]]\n")

        for cluster in sorted( model.clusters, key=op.attrgetter('order')): 

            for nodeFrom in sorted(cluster.nodes, key=op.attrgetter('order')): 
                f.write("[[Block: With respect to: "+nodeFrom.name+"]]\n")
                
                connectedClusters=model.retAllClusterConnectionsFromNode(nodeFrom.name)
                for clusterPWC in sorted(connectedClusters, key=op.attrgetter('order')):
                    i=0
                    # f.write("[[Block:"+clusterPWC.name+"]]\n")
                    # print("Nodes:\n",clusterPWC.nodes)
                    for nodeA in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                        j=0
                        # print("NodeA: ",nodeA.nodeID)
                        for nodeB in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                            # print("NodeB: ",nodeB.nodeID)
                            if (nodeA.nodeID!= nodeB.nodeID) and ((i==0)or (i+1==j)) and (nodeA in nodeFrom.connectedTo) and (nodeB in nodeFrom.connectedTo):
                                f.write("\n[[Question:MC:SingleAnswer]]\n")
                                quest1_csv=str(count)+'. With respect to '+nodeFrom.name+ ' which one is more '+keyword+':'+'\n'
                                f.write(quest1_csv) 
                                f.write("\n[[Choices]]\n")
                                
                                ans1=nodeA.name+'\n'
                                f.write(ans1)
                                ans2=nodeB.name+'\n'
                                f.write(ans2)
                                count+=1
                                
                                if(howMuch):
                                    f.write("\n[[Question:MC:Dropdown]]\n")
                                    quest2_csv=str(count)+". By how much?"+'\n'
                                    f.write(quest2_csv)
                                    f.write("\n[[Choices]]\n")
                                    f.write("1\n2\n3\n4\n5\n6\n7\n8\n9\n")
                                    count+=1
                                f.write('\n')
                            j+=1
                        i+=1       
def genexport4QualtricsFirstLineQuest(filepath,model,keyword,howMuch=True):
    count=1
    with open(filepath, 'w', encoding='UTF8',newline='') as f:
        f.write("[[AdvancedFormat]]\n")
        for cluster in sorted( model.clusters, key=op.attrgetter('order')): 
            
            for nodeFrom in sorted(cluster.nodes, key=op.attrgetter('order')): 
                f.write("[[Block: With respect to: "+nodeFrom.name+"]]\n")
                connectedClusters=model.retAllClusterConnectionsFromNode(nodeFrom.name)
                for clusterPWC in sorted(connectedClusters, key=op.attrgetter('order')):
                    i=0
                    qset=[]
                    # print("Nodes:\n",clusterPWC.nodes)
                    nodeA=clusterPWC.nodes[0]
                    j=0
                    # print("NodeA: ",nodeA.nodeID)
                    for nodeB in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                        # print("NodeB: ",nodeB.nodeID)
                        if (nodeA.nodeID!= nodeB.nodeID) and (i<j) and (nodeA in nodeFrom.connectedTo) and (nodeB in nodeFrom.connectedTo):
                                f.write("\n[[Question:MC:SingleAnswer]]\n")
                                quest1_csv=str(count)+'. With respect to '+nodeFrom.name+ ' which one is more '+keyword+':'+'\n'
                                f.write(quest1_csv) 
                                f.write("\n[[Choices]]\n")
                                
                                ans1=nodeA.name+'\n'
                                f.write(ans1)
                                ans2=nodeB.name+'\n'
                                f.write(ans2)
                                count+=1
                                
                                if(howMuch):
                                    f.write("\n[[Question:MC:Dropdown]]\n")
                                    quest2_csv=str(count)+". By how much?"+'\n'
                                    f.write(quest2_csv)
                                    f.write("\n[[Choices]]\n")
                                    f.write("1\n2\n3\n4\n5\n6\n7\n8\n9\n")
                                    count+=1
                                f.write('\n')
                        j+=1

def genexport4GoogleQuestFull(filepath,model,keyword,howMuch=True):
    count=1
    with open(filepath, 'w', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)  
        for cluster in sorted( model.clusters, key=op.attrgetter('order')): 

            for nodeFrom in sorted(cluster.nodes, key=op.attrgetter('order')): 
                
                connectedClusters=model.retAllClusterConnectionsFromNode(nodeFrom.name)
                for clusterPWC in sorted(connectedClusters, key=op.attrgetter('order')):
                    i=0

                    # print("Nodes:\n",clusterPWC.nodes)
                    for nodeA in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                        j=0
                        # print("NodeA: ",nodeA.nodeID)
                        for nodeB in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                            # print("NodeB: ",nodeB.nodeID)
                            if (nodeA.nodeID!= nodeB.nodeID) and (i<j) and (nodeA in nodeFrom.connectedTo) and (nodeB in nodeFrom.connectedTo):
                                # print("{}-{}".format(i,j))
                                quest1_csv=["With respect to "+nodeFrom.name+' which one is more '+keyword, nodeA.name, nodeB.name]
                                writer.writerow(quest1_csv)  
                                quest2_csv=["By how much?","1","2","3","4","5","6","7","8","9"]
                                writer.writerow(quest2_csv)                            
                            j+=1
                        i+=1
def genexport4GoogleFirstLineAboveDiagQuest(filepath,model,keyword,howMuch=True):
    count=1
    with open(filepath, 'w', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)  

        for cluster in sorted( model.clusters, key=op.attrgetter('order')): 

            for nodeFrom in sorted(cluster.nodes, key=op.attrgetter('order')): 
                
                
                connectedClusters=model.retAllClusterConnectionsFromNode(nodeFrom.name)
                for clusterPWC in sorted(connectedClusters, key=op.attrgetter('order')):
                    i=0
                    # f.write("[[Block:"+clusterPWC.name+"]]\n")
                    # print("Nodes:\n",clusterPWC.nodes)
                    for nodeA in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                        j=0
                        # print("NodeA: ",nodeA.nodeID)
                        for nodeB in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                            # print("NodeB: ",nodeB.nodeID)
                            if (nodeA.nodeID!= nodeB.nodeID) and ((i==0)or (i+1==j)) and (nodeA in nodeFrom.connectedTo) and (nodeB in nodeFrom.connectedTo):
                                quest1_csv=["With respect to "+nodeFrom.name+' which one is more '+keyword, nodeA.name, nodeB.name]
                                writer.writerow(quest1_csv)  
                                quest2_csv=["By how much?","1","2","3","4","5","6","7","8","9"]
                                writer.writerow(quest2_csv)  
                            j+=1
                        i+=1       
def genexport4GoogleFirstLineQuest(filepath,model,keyword,howMuch=True):
    count=1
    with open(filepath, 'w', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)  
        for cluster in sorted( model.clusters, key=op.attrgetter('order')): 
            
            for nodeFrom in sorted(cluster.nodes, key=op.attrgetter('order')): 
               
                connectedClusters=model.retAllClusterConnectionsFromNode(nodeFrom.name)
                for clusterPWC in sorted(connectedClusters, key=op.attrgetter('order')):
                    i=0
                    qset=[]
                    # print("Nodes:\n",clusterPWC.nodes)
                    nodeA=clusterPWC.nodes[0]
                    j=0
                    # print("NodeA: ",nodeA.nodeID)
                    for nodeB in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                        # print("NodeB: ",nodeB.nodeID)
                        if (nodeA.nodeID!= nodeB.nodeID) and (i<j) and (nodeA in nodeFrom.connectedTo) and (nodeB in nodeFrom.connectedTo):
                                quest1_csv=["With respect to "+nodeFrom.name+' which one is more '+keyword, nodeA.name, nodeB.name]
                                writer.writerow(quest1_csv)  
                                quest2_csv=["By how much?","1","2","3","4","5","6","7","8","9"]
                                writer.writerow(quest2_csv)  
                        j+=1


def export4ExcelQuestFull(model,filepath,verb=False):
    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0,20,15)

    cell_format_hd  = workbook.add_format({'bold': True,'font_color': 'red'})
    cell_format_hd.set_pattern(1)
    cell_format_hd.set_bg_color('C3D5FF')
    cell_format_hd2  = workbook.add_format({'bold': True,'font_color': 'red'})
    cell_format_hd2.set_pattern(1)
    cell_format_hd2.set_bg_color('#d5ffc3')
    cell_format_ln  = workbook.add_format({'bold': True,'font_color': 'blue'})
    cell_format_ln.set_border(1)
    cell_format_diag=workbook.add_format()
    cell_format_diag.set_pattern(1)
    cell_format_diag.set_border(1)
    cell_format_diag.set_bg_color('FFFF6B')
    cell_format_block=workbook.add_format()
    cell_format_block.set_pattern(1)
    cell_format_block.set_border(1)
    cell_format_block.set_bg_color('#808080')
    cell_format_empty  = workbook.add_format()
    cell_format_empty.set_border(1)
    
    row=0
    col=0
    for cluster in sorted( model.clusters, key=op.attrgetter('order')):
        for nodeFrom in sorted(cluster.nodes, key=op.attrgetter('order')): 

            connectedClusters=model.retAllClusterConnectionsFromNode(nodeFrom.name)
            if(len(connectedClusters)>0):
                worksheet.write(row, 0, nodeFrom.name,cell_format_hd)
                row=row+1
            for clusterPWC in sorted(connectedClusters, key=op.attrgetter('order')):
                # print("Nodes:\n",clusterPWC.nodes)

                worksheet.write(row, 2, clusterPWC.name,cell_format_hd2)
                row=row+1
                col=0
                size=0
                for nodeA in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                    # print("NodeA: ",nodeA.nodeID)         
                    
                    if(nodeA in nodeFrom.connectedTo):
                        worksheet.write(row, col+1, nodeA.name,cell_format_ln)
                        worksheet.write(row+col+1, 0, nodeA.name,cell_format_ln)
                        worksheet.write_number(row+col+1, col+1,1.000 ,cell_format_diag)
                        col+=1
                        size+=1
                for a in range(size):
                    for b in range (size):
                        if(a!=b and a>b):
                            worksheet.write(row+a+1,b+1,"",cell_format_block)
                        if(a!=b and a<b):
                            worksheet.write(row+a+1,b+1,"",cell_format_empty)
                # if verb:
                #     print(nodeA.name,size)        
                
                row=row+col+1
                if verb:
                    print("---------------------------------------------------------------------------\n")
            row+=1
    workbook.close()
       
def importFromExcel(model,filepath,sheet_name):

    all_excel = pd.read_excel (filepath, sheet_name=0) 
    array_excel=all_excel.fillna(0)
    file_len=len(array_excel)
    print("File Len=", file_len)
    # print("excel",array_excel)
    
    
    row=0
    if(row<file_len-2):
        print("row:",row)
        for cluster in sorted( model.clusters, key=op.attrgetter('order')):
            for nodeFrom in sorted(cluster.nodes, key=op.attrgetter('order')): 
                if(row>0 and row <file_len):
                    print(row,"with respect to:",array_excel.iat[row,0])
                    model.wrtlabels.append(array_excel.iat[row,0])
                    row+=1
                connectedClusters=model.retAllClusterConnectionsFromNode(nodeFrom.name)

                for clusterPWC in sorted(connectedClusters, key=op.attrgetter('order')):
                    # print("Nodes:\n",clusterPWC.nodes)
                    print(row,"In cluster:",array_excel.iat[row,2])
                    model.clabels.append(array_excel.iat[row,2])
                    row=row+1

                    size=0
                    for nodeA in sorted(clusterPWC.nodes, key=op.attrgetter('order')):
                        if(nodeA in nodeFrom.connectedTo):
                            model.nlabels.append(array_excel.iat[row,0])
                            size+=1
                    row=row+1
                    pc_matrix =  np.empty([size, size], dtype = float)
                    for a in range(size):
                        for b in range (size):
                            item=array_excel.iat[a+row,b+1]
                            if a==b:
                                pc_matrix[a,b]=1.0
                            elif a<b:
                                pc_matrix[a,b]=item
                                if(item!=0):
                                    pc_matrix[b,a]=1./item
                                else:
                                    pc_matrix[b,a]=0
                    print(pc_matrix)
                    # if verb:
                    #     print(nodeA.name,size)        
                    model.all_pc_matrices.append(pc_matrix)
                    row=row+size
                    
                row+=1


       