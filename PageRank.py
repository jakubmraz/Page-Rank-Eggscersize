import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
import matplotlib as mpl

file = open("PageRankExampleData\\tiny.txt", "rb")
G: nx.Graph = nx.read_adjlist(file, create_using=nx.DiGraph())
file.close()

def CalculateGraphSize(graph):
    return [len(G), len(G)]

graphSize = CalculateGraphSize(G)

def PageSurfer():
    pass

def CreateAdjecencyMatrix(graph: nx.Graph):
    adj_matrix = np.zeros((CalculateGraphSize(graph)), dtype='int')

    for node_i, node_j in graph.edges:    
        adj_matrix[int(node_i), int(node_j)] = 1 # Unweighted network

    return adj_matrix

def CreateBacklinkMatrix(adjecencyMatrix):
    #The backlink matrix is the transpose of the adjecency matrix upside down
    backlinkMatrix = np.transpose(adjecencyMatrix)
    np.flip(backlinkMatrix, 1)
    print(backlinkMatrix)

def GetBacklinkCount(adjecencyMatrix):
    transposedAdj = np.transpose(adjecencyMatrix)
    backlinkDict = {}

    for pageBacklinkRow in range(0, graphSize[0]):
        for backlink in transposedAdj[pageBacklinkRow]:
            if(backlink > 0):
                if(pageBacklinkRow in backlinkDict):
                    backlinkDict[pageBacklinkRow] += 1
                else:
                    backlinkDict[pageBacklinkRow] = 1

    return backlinkDict

def RankPages(adjecencyMatrix):
    


    print(backlinkDict)
    CreateBacklinkMatrix(adjecencyMatrix)
    #Weigh by importance of voting pages
    #One page, one vote

adj = CreateAdjecencyMatrix(G)
RankPages(adj)