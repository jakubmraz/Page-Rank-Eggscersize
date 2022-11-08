import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
import matplotlib as mpl

file = open("PageRankExampleData\medium.txt", "rb")
G: nx.Graph = nx.read_adjlist(file, create_using=nx.DiGraph())
file.close()

def PageSurfer():
    pass

def CalculateGraphSize(graph):
    return [len(G), len(G)]

print(CalculateGraphSize(G))