# from AHPLib import *
import numpy as np
import pandas as pd
#for windows only 
import sys
sys.path.insert(0, './sourceLibs')


import inputs_AHPLib as cdf_inp
import structs_AHPLib as cdf_str
import calcs_AHPLib as cdf_calc
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
#set here the number of decimals that you want to be displayed

carModel=cdf_str.Model()

goal_node=cdf_str.Node("GoalNode",0)


prestige=cdf_str.Node("1Prestige",1)
price=cdf_str.Node("2Price",2)
mpg=cdf_str.Node("3MPG",3)
comf=cdf_str.Node("4Comfort",4)


alt1=cdf_str.Node("1Acura TL",5)
alt2=cdf_str.Node("2Toyota Camry",6)
alt3=cdf_str.Node("3Honda Civic",7)


cluster0=cdf_str.Cluster("1Goal",0)
cluster1=cdf_str.Cluster("2Criteria",1)
cluster2=cdf_str.Cluster("3Alternatives",2)


cluster1.addNode2Cluster(goal_node) #on purpose wrong assignment

cluster1.addNode2Cluster(prestige)
cluster1.remNodeFromCluster(prestige)
cluster1.addNode2Cluster(price)
cluster1.addNode2Cluster(mpg)
cluster1.addNode2Cluster(comf)

cluster2.addNode2Cluster(alt1)
cluster2.addNode2Cluster(alt2)
cluster2.addNode2Cluster(alt3)



cluster0.forceAddNode2Cluster(goal_node)


carModel.addCluster2Model(cluster0)
carModel.addCluster2Model(cluster1)
carModel.addCluster2Model(cluster2)

carModel.addNodeConnectionFromNodeToAllNodesOfCluster("GoalNode","2Criteria")



carModel.addNodeConnectionFromAllNodesToAllNodesOfCluster("2Criteria","3Alternatives")

print("___________________________________________________________")


carModel.showAllNodeConnections()
print("___________________________________________________________")
carModel.showAllClusterConnections()

#INPUTS 
print("___________________________________________________________")

q1=cdf_inp.genFullQuest(carModel,"important",False)
q2=cdf_inp.genFirstLineAboveDiagQuest(carModel,"important",False)
q3=cdf_inp.genFirstLineQuest(carModel,"important",False)


# #Qualtrics

# cdf_inp.genexport4QualtricsQuestFull(".\Examples\IO Files\QualtricsTestCarFull.txt",carModel,"important",True)
# cdf_inp.genexport4QualtricsFirstLineQuest(".\Examples\IO Files\QualtricsTestCarFirstLine.txt",carModel,"important",True)
# cdf_inp.genexport4QualtricsFirstLineAboveDiagQuest(".\Examples\IO Files\QualtricsTestCarFirstAndAbove.txt",carModel,"important",True)

# #Google

# cdf_inp.genexport4GoogleQuestFull(".\Examples\IO Files\GoogleTestCarFull.csv",carModel,"important",False)
# cdf_inp.genexport4GoogleFirstLineQuest(".\Examples\IO Files\GoogleTestCarFirstLine.csv",carModel,"important",False)
# cdf_inp.genexport4GoogleFirstLineAboveDiagQuest(".\Examples\IO Files\GoogleTestCarFirstAndAbove.csv",carModel,"important",False)

# Excel
# cdf_inp.export4ExcelQuestFull(carModel,"./Examples/IO Files/excelTestCarFull.xlsx",True)

cdf_inp.importFromExcel(carModel,"./Examples/IO Files/excelTestCarFull.xlsx",0)

 
for i in range(0,len(carModel.all_pc_matrices)):
    a=cdf_calc.priorityVector(carModel.all_pc_matrices[i])
    print(a)

listTitles=cdf_calc.nodeNameList(carModel)

super=cdf_calc.calcUnweightedSuperMatrix(carModel)

df = pd.DataFrame (super,index=listTitles,columns=listTitles)
filepath = "./Examples/IO Files/carExampleSupermatrix.xlsx"
df.to_excel(filepath)


limit = cdf_calc.calcLimitingPriorities(carModel.supermatrix)
df2 = pd.DataFrame (limit,index=listTitles)
filepath = "./Examples/IO Files/carExampleLimitPriorities.xlsx"
df2.to_excel(filepath)

bycluster = cdf_calc.calcPrioritiesNormalizedByCluster(limit, carModel)
df3 = pd.DataFrame (bycluster,index=listTitles)
filepath = "./Examples/IO Files/carExampleLimitByCluster.xlsx"
df3.to_excel(filepath)



# cdf_calc.sensitivityCellSupermatrix(super,1)
# cdf_calc.sensitivityCellSupermatrixShort(super,1,"3Alternatives",carModel)

cdf_calc.sensitivityCellSupermatrixPlot(super,1,"3Alternatives",carModel)
cdf_calc.sensitivityCellSupermatrixPlot(super,2,"3Alternatives",carModel)
cdf_calc.sensitivityCellSupermatrixPlot(super,3,"3Alternatives",carModel)
cdf_calc.sensitivityCellSupermatrixPlot(super,4,"3Alternatives",carModel)
