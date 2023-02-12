# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
File to visualise the tree and the chain using networkx and matplotlib
"""
import networkx as nx
import matplotlib.pyplot as plt

center = 0

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
    x = {}
    for i in range(len(chain)):
        if i==0:
            G.add_node(chain[i].BlkID[:7], pos = (center,chain[-1].chain_length-chain[i].chain_length))
            x[chain[i].BlkID] = 0
        else:
            x_coord = x[chain[i].parent.BlkID]
            G.add_node(chain[i].BlkID[:7], pos = (chain[i].parent.x+0.2*x_coord/len(chain), chain[-1].chain_length-chain[i].chain_length))
            chain[i].x = chain[i].parent.x+0.2*x_coord/len(chain)
            x[chain[i].parent.BlkID] += 1
            x[chain[i].BlkID] = 0
    for i in range(len(chain)):
        if chain[i].parent is not None:
            G.add_edge(chain[i].parent.BlkID[:7], chain[i].BlkID[:7])
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_shape =  's', node_size = 250, node_color = 'c', font_size = 8)
    plt.savefig(f'results/chain_{node.ID}.png')
    plt.clf()


