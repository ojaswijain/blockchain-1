# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
File to visualise the tree
"""
import networkx as nx
import graphviz as gv
import matplotlib.pyplot as plt

# def visualise_tree(nodelist):
#     dot = gv.Digraph()
#     for node in nodelist:
#         dot.node(str(node.ID))
#         for child in node.neighbours:
#             dot.edge(str(node.ID), str(child.ID))
#     dot.render('results/tree.gv', view=True)

# def visualise_chain(node):
#     dot = gv.Digraph()
#     BlockChain = node.LocalChain
#     chain = BlockChain.chain
#     for i in range(len(chain)):
#         dot.node(str(chain[i].BlkID[:5]))
#     for i in range(len(chain)):
#         if chain[i].parent is not None:
#             dot.edge(str(chain[i].parent.BlkID[:5]), str(chain[i].BlkID[:5]))
#     dot.render('results/'+str(node.ID), view=True)

def visualise_tree(nodelist):
    G = nx.Graph()
    for node in nodelist:
        G.add_node(node.ID)
        for child in node.neighbours:
            G.add_edge(node.ID, child.ID)
    nx.draw(G, with_labels=True)
    plt.show()

def visualise_chain(node):
    G = nx.DiGraph()
    BlockChain = node.LocalChain
    chain = BlockChain.chain
    for i in range(len(chain)):
        G.add_node(chain[i].BlkID[:7])
    for i in range(len(chain)):
        if chain[i].parent is not None:
            G.add_edge(chain[i].parent.BlkID[:7], chain[i].BlkID[:7])
    nx.draw_spectral(G, with_labels=True)
    plt.savefig(f'results/chain_{node.ID}.png')
    plt.clf()