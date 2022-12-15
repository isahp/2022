# from curses.ascii import alt
import itertools
import pandas as pd
import numpy as np
from operator import inv
import operator as op

class Model:
    id_generator = itertools.count(0)
    def __init__(self):
        
        # choose appropriate comparative word that will be saved in the keyword variable. Usually we use: "important","preferred", "likely" can support different keywords
        self.modelID=next(self.id_generator)
        self.clusters=[]
       
        self.nodeConnections=[]
        self.clusterConnections=[]
        self.all_pc_matrices=[]
        self.all_pr_vectors=[]
        self.pc_with_respect_to=[]
        self.pc_node_order=[]
        self.supermatrix=[]
        self.weighted_supermatrix=[]
        self.limit=[]
        self.questionnaires=[]
        self.nlabels=[]
        self.clabels=[]
        self.wrtlabels=[]
        

        

    def __repr__(self):
        return "Nodes: "+str(self.getNodeListFromClusters())+"\n Clusters: "+str(self.clusters)+"\n Node Connections: "+str(self.nodeConnections)+"\n Cluster Connections: "+str(self.clusterConnections)
    
    def addCluster2Model(self,cluster):
    #add a cluster that DOES NOT belong to a model to this model
        if (cluster.parModel==""):
            if cluster not in self.clusters:
                self.clusters.append(cluster)
                cluster.parModel=self.modelID
                # print(cluster.parModel, "--",self.modelID)
        else:
            print("Cluster already assigned to model")
    
    def remClusterFromModel(self,clusterName):
        cluster=self.getClusterObjByName(clusterName)
    #add a cluster that DOES NOT belong to a model to this model
        # print(cluster.parModel, "--",self.modelID)
        if (cluster.parModel==self.modelID):
            if cluster in self.clusters:
                self.clusters.remove(cluster)
                cluster.parCluster=""

                #   update model connections
                self.defineAllNodeConnections()
                #update cluster connections
                self.defineAllClusterConnections()
        else:
            print("Cluster not assigned to this model")

    def remClusterFromModelAndDettach(self,clusterObj):
        # print(cluster.parModel, "--",self.modelID)
        if (clusterObj.parModel==self.modelID):
            if clusterObj in self.clusters:
                self.clusters.remove(clusterObj)
                clusterObj.parCluster=""

                #   update model connections
                self.defineAllNodeConnections()
                #update cluster connections
                self.defineAllClusterConnections()
        else:
            print("Cluster not assigned to this model")

    def getNodeListFromClusters(self):
        nodes=[]
        for cluster in self.clusters:
            for node in cluster.nodes:
                nodes.append(node)
        return nodes

    def defineAllNodeConnections(self):
        self.nodeConnections={}
        for cluster in self.clusters:
            for node in cluster.nodes:
                self.nodeConnections[node]=node.connectedTo
        return self.nodeConnections
    
    def getClusterIndexByName(self,name):
        for index, item in enumerate(self.clusters):
            if item.name == name:
                break
        else:
            index = -1
        return index
    
    def getClusterObjByName(self,name):
        for item in self.clusters:
            # print(item.name)
            if item.name == name:
                return item
        return -1
        
    def getClusterObjByID(self,ID):
        for item in self.clusters:
            # print(item.name)
            if item.clusterID == ID:
                return item
        return -1
    
    def getClusterIDByName(self,name):
        for item in self.clusters:
            # print(item.name)
            if item.name == name:
                return item.clusterID
        return -1

    def getNodeIndexInClusterModelByName(self,name):
        indexN = -1
        for index, item in enumerate(self.clusters):
            for indexN, itemN in enumerate(item.nodes):
                if itemN.name == name:
                    return indexN
        return indexN
    
    def getNodeInClusterModelByName(self,name):

        for item in self.clusters:
            for itemN in item.nodes:
                if itemN.name == name:
                    # print(itemN)
                    return itemN
        return -1
    
    def getNodeIDByName(self,name):

        for item in self.clusters:
            for itemN in item.nodes:
                if itemN.name == name:
                    # print(itemN)
                    return itemN.nodeID
        return -1

   
    
    def addNodeConnectionFromTo(self,nodeFromName,nodeToName, verb=False):
         #will add a connection from nodeFrom to the nodeTo node

        nodeFrom=self.getNodeInClusterModelByName(nodeFromName)
        # print("From {} ".format(nodeFrom))
        nodeTo=self.getNodeInClusterModelByName(nodeToName)
        # print("To {} ".format(nodeTo))

        if nodeTo not in nodeFrom.connectedTo:
            nodeFrom.connectedTo.append(nodeTo)
        else:
            print("Trying to add n{}. Node already in connections.".format(str(nodeTo.nodeID)))
        if verb==True: 
            print("node: "+nodeFrom.name+" connectedTo: "+str(nodeFrom.connectedTo))

        #   update model connections
        self.defineAllNodeConnections()
        #update cluster connections
        self.defineAllClusterConnections()


    def addNodeConnectionFromNodeToAllNodesOfCluster(self,nodeFromName,clusterToName):
         #will add a connection from nodeFrom to each nodeTo of clusterToName
         clusterTo=self.getClusterObjByName(clusterToName)
         for nodeTo in clusterTo.nodes:
            self.addNodeConnectionFromTo(nodeFromName,nodeTo.name)

    def addNodeConnectionFromAllNodesToAllNodesOfCluster(self,clusterFromName,clusterToName):
         #will add a connection from each nodeFrom of clusterFromName to each nodeTo of clusterToName
         clusterFrom=self.getClusterObjByName(clusterFromName)
         for nodeFrom in clusterFrom.nodes:
            self.addNodeConnectionFromNodeToAllNodesOfCluster(nodeFrom.name,clusterToName)   
   
    def remNodeConnectionFromTo(self,nodeFromName,nodeToName,verb=False):
        flag=0
        nodeFrom=self.getNodeInClusterModelByName(nodeFromName)
        # print("From {} ".format(nodeFrom))
        nodeTo=self.getNodeInClusterModelByName(nodeToName)
        # print("To {} ".format(nodeTo))

        if nodeTo in nodeFrom.connectedTo:
            nodeFrom.connectedTo.remove(nodeTo)
        else:
            print("Trying to delete n{}. Node not in connections.".format(str(nodeTo.nodeID)))
        if verb==True: 
            print("node: "+nodeFrom.name+" after the deletion is now connected to: "+str(nodeFrom.connectedTo))

        #   update model connections
        self.defineAllNodeConnections()
        #update cluster connections
        self.defineAllClusterConnections()
   

    def defineAllClusterConnections(self):
        self.clusterConnections={}
        for cluster in self.clusters:
            self.clusterConnections[cluster]=cluster.calcAllConnectionsFrom()
        return self.clusterConnections

    def remAllNodeConnectionsTo(self,nodeName):
        flag=0
        nodeTo_del_id=self.getNodeIDByName(nodeName)
        for nodeFrom in self.getNodeListFromClusters():
            for nodeTo in nodeFrom.connectedTo:
                if nodeTo.nodeID==nodeTo_del_id:
                    flag=1
                    nodeFrom.connectedTo.remove(nodeTo)
                    print("node connection from: "+nodeFrom.name+" to :"+nodeName+" removed.")
                    #update cluster connections
                    nodeTo.parCluster.calcAllConnectionsFrom()
        if flag==0:
            print("Trying to delete n{}. Node was not found.".format(nodeName))
      

    def remAllNodeConnectionsFrom(self,nodeFromName):
        flag=0 
        toDel=[]
        nodeFrom=self.getNodeInClusterModelByName(nodeFromName)
        for nodeTo in nodeFrom.connectedTo:
            toDel.append(nodeTo)
        # print(*toDel, sep='\n')
        for nodeTo in toDel:
            self.remNodeConnectionFromTo(nodeFrom.name,nodeTo.name)


    def showAllNodeConnectionsFrom(self, nodeFromName):
        flag=0
        nodeFrom_id=self.getNodeIDByName(nodeFromName)
        for nodeFrom in self.getNodeListFromClusters():
            if nodeFrom.nodeID==nodeFrom_id:
                
                for nodeTo in nodeFrom.connectedTo:
                    if flag==0:
                        print("Connections from node "+str(nodeFrom) +" to: ")
                    flag=1
                    print(str(nodeTo))
        if(flag==0):
            print("No connections from",nodeFromName)

    def showAllNodeConnectionsTo(self, nodeToName):
        #same with enumerating the connectedTo list of each node
        flag=0
        nodeTo_id=self.getNodeIDByName(nodeToName)
        for nodeFrom in self.getNodeListFromClusters():
            for nodeTo in nodeFrom.connectedTo:
                if nodeTo.nodeID==nodeTo_id:
                    flag=1
                    print("Connections from node "+str(nodeFrom) +" to: "+str(nodeTo))        

        if(flag==0):
            print("No connections to",nodeToName)

    def showAllNodeConnections(self):
        #same with enumerating the connectedTo list of each node
        for nodeFrom in self.getNodeListFromClusters():
            flag=0
            for nodeTo in nodeFrom.connectedTo:
                    if(flag==0):
                        print("Connections from node "+str(nodeFrom))
                    flag=1
                    print(" to: "+str(nodeTo))
            if(flag==0):
                print("No connections from",nodeFrom.name)

    def showAllClusterConnections(self):
        #same with enumerating the connectedTo list of each node
        for clusterFrom in self.clusters:
            flag=0
            for clusterTo in clusterFrom.connectedTo:
                    if(flag==0):
                        print("Connection(s) from cluster "+str(clusterFrom))
                    flag=1
                    print(" to: "+str(clusterTo))
            if(flag==0):
                print("No connections from",clusterFrom.name)  
    def retAllClusterConnectionsFrom(self,clusterName):
        #same with enumerating the connectedTo list of each node
        connected_to=[]
        clusterFrom_id=self.getClusterIDByName(clusterName)
        for clusterFrom in self.clusters:
            flag=0
            if clusterFrom.clusterID==clusterFrom_id:
                for clusterTo in clusterFrom.connectedTo:
                        if(flag==0):
                            connected_to.append(clusterTo)
                            #print("Connection(s) from cluster "+str(clusterFrom))
                        flag=1
                        #print(" to: "+str(clusterTo))
                if(flag==0):
                    return None
               # print("No connections from",clusterFrom.name) 
        return connected_to 
    def retAllClusterConnectionsFromNode(self,nodeName,verb=False):
        #to which clusters is this node connected to
        connected_to=[]
        flag=0
        node_id=self.getNodeIDByName(nodeName)

        # print("working with",node_id)
        for nodeFrom in self.getNodeListFromClusters():
            if nodeFrom.nodeID==node_id:
                for nodeTo in nodeFrom.connectedTo:
                    flag=1
                    clusterTo=nodeTo.parCluster
                    if(clusterTo not in connected_to):
                        if verb==True:
                            print("Connections from node "+str(nodeFrom) +" to cluster: "+str(clusterTo)) 
                        connected_to.append(clusterTo)      
        if(flag==0):
             if verb==True:
                print("No connections form",nodeName)
        return connected_to
    
    def showAllClusterConnectionsFrom(self,clusterName):
        #same with enumerating the connectedTo list of each node
        clusterFrom_id=self.getClusterIDByName(clusterName)
        for clusterFrom in self.clusters:
            flag=0
            if clusterFrom.clusterID==clusterFrom_id:
                for clusterTo in clusterFrom.connectedTo:
                        if(flag==0):
                            print("Connection(s) from cluster "+str(clusterFrom))
                            flag=1
                            print(" to: "+str(clusterTo))
                if(flag==0):
                    print("No connections from",clusterFrom.name) 
        
    def listAllClusterConnections(self,clusterFrom):
        connected_to=[]
        #same with enumerating the connectedTo list of each node
        
        for clusterTo in clusterFrom.connectedTo:
            connected_to.append(clusterTo)
        return connected_to       
    
    def moveNode2ClusterWithConnections(self,node,toCluster):    
        #moving node from Cluster A to Cluster B (toCluster)
        for movingNode in self.getNodeListFromClusters():
            if movingNode.nodeID==node.nodeID:
                ClusterA=movingNode.parCluster
                ClusterA.nodes.remove(movingNode)
                print("Origin cluster updated: "+str(ClusterA.nodes))
        if movingNode not in toCluster.nodes:
            toCluster.nodes.append(node)
        node.parCluster=toCluster
       
    def moveNode2ClusterWithoutConnections(self,node,toCluster):    
        #moving node from Cluster A to Cluster B (toCluster)
        for movingNode in self.getNodeListFromClusters():
         if movingNode.nodeID==node.nodeID:
            ClusterA=movingNode.parCluster
            ClusterA.nodes.remove(movingNode)
            print("Origin cluster updated: "+str(ClusterA.nodes))
        if movingNode not in toCluster.nodes:
            toCluster.nodes.append(node)
        node.parCluster=toCluster
        #remove all connections from this node
        self.remAllConnectionsFrom(node.nodeID)
        #remove all connections to this node
        self.remAllConnectionsTo(node.nodeID)
    
class Node:
    id_generator = itertools.count(0)

    def __init__(self, node_name,node_order):
        self.name = node_name
        self.order = node_order
        self.nodeID = next(self.id_generator)
        self.parCluster=""
        self.connectedTo=[]

    def __repr__(self):
        return self.name+" NID: "+str(self.nodeID)+" order: "+ str(self.order)
     
    def myParentCluster(self):
        return self.parCluster
    def updateN_DisplayOrder(self,newOrder):
        self.order=newOrder

class Cluster:
    id_generator = itertools.count(0)
    
    def __init__(self, cluster_name,cluster_order):
        self.name = cluster_name
        self.order = cluster_order
        self.clusterID = next(self.id_generator)
        self.nodes=[]
        self.connectedTo=[]
        self.parModel=""
       
    def __repr__(self):
        return self.name+" CID:  "+str(self.clusterID)+" order: "+ str(self.order)
    def printWithNodes(self):
        print("Cluster: {} with nodes: {}\n".format(self.name,self.nodes))
    def addNode2Cluster(self,node):
    #add a node that DOES NOT belong to a cluster to this cluster
        if (node.parCluster==""):
            if node not in self.nodes:
                self.nodes.append(node)
                node.parCluster=self
        else:
            print("Node already assigned to cluster")
    
    def remNodeFromCluster(self,node):
    #rem a node from the cluster -- not to be used if node has been assigned to model

        print(self.clusterID, "--",node.parCluster.clusterID,"--",node.parCluster.parModel)
        if (node.parCluster.parModel==""):
            if (node.parCluster.clusterID==self.clusterID):
                if node not in self.nodes:
                    self.nodes.remove(node)
                    node.parCluster=""
            else:
                print("Node not assigned to this cluster")
        else: 
                print("Node already assigned to model - use the model remNodeFromClusterOfModel function")
    def forceAddNode2Cluster(self,node):
    #add a node even if it already belongs to another cluster to a this cluster
        ClusterA=node.parCluster
        ClusterA.nodes.remove(node)
        if node not in self.nodes:
                self.nodes.append(node)
                node.parCluster=self

    def detachFromModel(self):
        self.parModel=""

    def calcAllConnectionsFrom(self,verb=False):
        # print("cluster connections for: "+self.name)
        # print('cluster nodes: {}'.format(self.nodes))
        for fromNode in self.nodes:
            # print("From node:",str(fromNode.nodeID))
            for toNode in fromNode.connectedTo:
                # print("To node:",str(toNode.nodeID))
                if toNode.parCluster not in self.connectedTo:
                    self.connectedTo.append(toNode.parCluster)
                    if verb==True:
                        print("connecting from cluster: {} to cluster {}".format(str(self.clusterID),str(toNode.parCluster.clusterID)))
                # else:
                    # print("Connection from cluster: {} to cluster {} already exists".format(str(self.clusterID),str(toNode.parCluster.clusterID)))
        return self.connectedTo
    def updateC_DisplayOrder(self,newOrder):
        self.order=newOrder

