import numpy as np
import networkx as nx
import random

file = open("PageRankExampleData\\p2p-Gnutella08-mod.txt", "rb")
G: nx.Graph = nx.read_adjlist(file, create_using=nx.DiGraph())
file.close()

def CalculateGraphSize(graph):
    #calculates graph size form loaded data
    return [len(graph), len(graph)]

graphSize = CalculateGraphSize(G)
dampingFactor = 0.15

def SurferAddToDict(dictionary: dict, pageNr: int):
    if (pageNr not in dictionary):
        dictionary[pageNr] = 1
    else:
        dictionary[pageNr] += 1

def SurferGetRandomPage(dictionary: dict):
    newPage = random.randint(0, graphSize[0] - 1)
    SurferAddToDict(dictionary, newPage)
    return newPage

def PageSurfer(noOfIterarions: int, G: nx.Graph) -> dict:
    visitedPages = {}
    #Start at random page
    pageNr = SurferGetRandomPage(visitedPages)
    for _ in range(noOfIterarions):
        #Random chance to go to a random page (chance same as damping factor)
        if(random.random() <= dampingFactor):
            pageNr = SurferGetRandomPage(visitedPages)
        #Else go to one of the pages linked by this page at random
        pagesLinked = list(G.neighbors(str(pageNr)))
        #If no neighbours, go to random page
        if(len(pagesLinked) == 0):
            pageNr = SurferGetRandomPage(visitedPages)
        else:
            pageNr = random.choice(pagesLinked)
            SurferAddToDict(visitedPages, int(pageNr))
    
    return dict(sorted(visitedPages.items(), key=lambda item: item[1], reverse=True))

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
        if(rowNr in linkDict):
            numberOfFrontLinks = linkDict[rowNr]
            adjecencyMatrix[rowNr] = adjecencyMatrix[rowNr] / numberOfFrontLinks 
        else:
            adjecencyMatrix[rowNr] = 0
        
def RankPages(adjecencyMatrix, k):
    frontlinkDict = GetFrontLinkCount(adjecencyMatrix)
    #Weigh by importance of voting pages
    #One page, one vote
    GivePageOneVote(adjecencyMatrix, frontlinkDict)

    #Matrix A
    backlinkMatrix = CreateBacklinkMatrix(adjecencyMatrix)

    #Matrix D for dangling nodes
    D = np.zeros(graphSize)
    arrayOfSums = np.sum(backlinkMatrix, axis=0)

    for j in range(0, graphSize[0]):
        if(arrayOfSums[j] == 0):
            D[:,j] = 1/graphSize[0]

    #Calculating the approximation xk
    #x0 gon give it to you
    x = np.full((graphSize[0], 1), 1/graphSize[0])
    oneMinusM = 1 - dampingFactor
    mSx = dampingFactor * 1/graphSize[0] * 1/graphSize[0]

    #xk+1 = (1 - m) * Axk + (1 - m) * Dxk + mSxk
    #Save first value for reference
    reference = 0
    for _ in range(0, k):
        reference = x[0][0]
        x = oneMinusM * np.matmul(backlinkMatrix, x) + oneMinusM * CalculateOptimalDx(D, x) + mSx
        #If the ranks didn't change, abort, no point in going
        if(x[0][0] == reference):
            break

    #Rank pages based on their xk score
    pageRankDict = {}
    for i in range(0, graphSize[0]):
        pageRankDict[i] = x[i][0]

    return dict(sorted(pageRankDict.items(), key=lambda item: item[1], reverse=True))

def CalculateOptimalDx(D, x):
    numberToFill = np.matmul(D[0,:], x)
    return np.full((graphSize[0], 1), numberToFill[0])

adj = CreateAdjecencyMatrix(G)
print(RankPages(adj, 100))
#print(PageSurfer(100000, G))