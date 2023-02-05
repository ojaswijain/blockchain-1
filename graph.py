# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
File to handle the initialization of the graph and latencies
"""

import numpy as np
from objects import Node, Graph, Block, Transaction

c_slow = 5e3
c_fast = 1e5

def create_graph(node_list):
    """
    Creates a connected graph
    4-8 neighbours for each node
    """
    number_of_neighbours = {}
    edges = []
    latency = {}
    nodes = node_list

    #Generating random number of neighbours for each node
    for node in node_list:
        number_of_neighbours[node.ID] = np.random.randint(4, 8)
    
    #Creating edges
    while len(nodes)>1:
        n1, n2 = np.random.choice(nodes, 2, replace=False)
        
        if(n2.ID, n1.ID) not in edges:
            #Adding edge
            edges.append((n1.ID, n2.ID))
            n1.neighbours.append(n2)
            n2.neighbours.append(n1)
            
            #Latency implementation
            p = np.random.uniform(10, 500)
            speed = 0
            if n1.speed == "slow" or n2.speed == "slow":
                speed = c_slow
            else:
                speed = c_fast
            d = np.random.exponential(96e3/speed)
            latency[(n1.ID, n2.ID)] = (p, speed, d)

            #Removing nodes with no more neighbours
            number_of_neighbours[n1.ID] -= 1
            number_of_neighbours[n2.ID] -= 1
            if number_of_neighbours[n1.ID] == 0:
                del nodes[n1.ID]
            if number_of_neighbours[n2.ID] == 0:
                del nodes[n2.ID]

    return Graph(node_list, latency)

def isConnected(graph):
    """
    Checks if the graph is connected
    """
    #Check if the number of neighbours is correct
    for i in graph.nodes:
        if len(i.neighbours) < 4 or len(i.neighbours) > 8:
            return False

    #Create a visited array and do BFS
    visited = [False] * (len(graph.nodes) + 1)
    queue = []
    queue.append(graph.nodes[0])
    visited[graph.nodes[0].ID] = True

    while queue:
        s = queue.pop(0)
        for i in s.neighbours:
            if visited[i.ID] == False:
                queue.append(i)
                visited[i.ID] = True

    #Check if all nodes are visited
    for i in visited:
        if i == False:
            return False
    return True

def prop_delay(graph, node1, node2, msg):
    """
    Returns the time to propagate a message from node1 to node2
    """
    if node1.ID in node2.neighbours:
        p, speed, d = graph.latency[(node1.ID, node2.ID)]
        return p + (msg.size)/speed + d
    else:
        return 0
    