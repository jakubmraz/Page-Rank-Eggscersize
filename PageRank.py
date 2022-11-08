import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
import matplotlib as mpl

file = open("PageRankExampleData\\tiny.txt", "rb")
G: nx.Graph = nx.read_adjlist(file, create_using=nx.DiGraph())
file.close()

def CalculateGraphSize(graph):
    return [len(graph), len(graph)]

graphSize = CalculateGraphSize(G)

def PageSurfer(noOfIterarions: int):
    #TODO:
    #Start at random page
    #Random chance to go to a random page (chance same as damping factor)
    #Else go to one of the pages linked by this page at random
    #Page is reached, record this in a dictionary
    #Repeat for noOfIteration times
    pass

def CreateAdjecencyMatrix(graph: nx.Graph):
    adj_matrix = np.zeros((CalculateGraphSize(graph)), dtype='float')

    for node_i, node_j in graph.edges:    
        adj_matrix[int(node_i), int(node_j)] = 1 # Unweighted network

    return adj_matrix

def CreateBacklinkMatrix(adjecencyMatrix):
    #The backlink matrix is the transpose of the adjecency matrix upside down
    backlinkMatrix = np.transpose(adjecencyMatrix)
    np.flip(backlinkMatrix, 1)
    return backlinkMatrix

def GetFrontLinkCount(adjecencyMatrix):
    linkDict = {}

    #TODO: Read the sum of the rows using numpy instead
    for pageLinkRow in range(0, graphSize[0]):
        for link in adjecencyMatrix[pageLinkRow]:
            if(link > 0):
                if(pageLinkRow in linkDict):
                    linkDict[pageLinkRow] += 1
                else:
                    linkDict[pageLinkRow] = 1

    return linkDict

def GetBacklinkCount(adjecencyMatrix):
    transposedAdj = np.transpose(adjecencyMatrix)
    backlinkDict = {}

    #TODO: Read the sum of the rows using numpy instead
    for pageBacklinkRow in range(0, graphSize[0]):
        for backlink in transposedAdj[pageBacklinkRow]:
            if(backlink > 0):
                if(pageBacklinkRow in backlinkDict):
                    backlinkDict[pageBacklinkRow] += 1
                else:
                    backlinkDict[pageBacklinkRow] = 1

    return backlinkDict

def GivePageOneVote(adjecencyMatrix, linkDict):
    for rowNr in range(0, graphSize[0]):
        numberOfFrontLinks = linkDict[rowNr]
        adjecencyMatrix[rowNr] = adjecencyMatrix[rowNr] / numberOfFrontLinks 

def RankPages(adjecencyMatrix):
    frontlinkDict = GetFrontLinkCount(adjecencyMatrix)
    #Weigh by importance of voting pages
    #One page, one vote
    GivePageOneVote(adjecencyMatrix, frontlinkDict)

    #Matrix A
    backlinkMatrix = CreateBacklinkMatrix(adjecencyMatrix)

    #Fix dangling nodes
    #TODO: Modify adjecency matrix so that nodes that do not link to any pages instead link to every page (easier to code)
    #OR: Create new matrix D with the same dimensions as A where D[i,j] is 1/n (total pages, i.e. dimension of D) if j is dangling
    #A2 = A + D

    #Fix disconnected web
    #TODO: Introduce a damping factor m between 0 and 1 (0.15 in requirements I think)
    #A3 = (1 - m)(A2) + m*S where S is a new matrix of the same dimensions as A, all numbers in matrix are 1/n

    #TODO: Compute approximation instead of doing all these calculations
    #I don't understand it from the notes

    print(backlinkMatrix)

adj = CreateAdjecencyMatrix(G)
RankPages(adj)