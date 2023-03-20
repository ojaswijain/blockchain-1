# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
File to handle the initialization of the graph and latencies
"""

import numpy as np

c_slow = 5e6
c_fast = 1e8

def create_graph(node_list, zeta = 0):
    """
    Creates a connected graph
    4-8 neighbours for each node
    Solution to part 4 of the assignment
    """

    number_of_neighbours = {}
    edges = []
    latency = {}
    nodes = node_list.copy()

    #Generating random number of neighbours for each node
    for node in node_list:
        number_of_neighbours[node.ID] = np.random.randint(4, 7)

    #Addition for assignment 2, number of neighbours of malicious node
    if zeta != 0:
        selfish_neighbours = np.random.choice(node_list, int(zeta*len(node_list)), replace=False)
        for node in selfish_neighbours:
            nodes[0].neighbours.append(node)
            node.neighbours.append(nodes[0])
            number_of_neighbours[node.ID] -= 1
        nodes.remove(nodes[0])
    #Creating edges
    while len(nodes)>1:
        n1, n2 = np.random.choice(nodes, 2, replace=False)
        
        if(n2.ID, n1.ID) not in edges:
            #Adding edge
            edges.append((n1.ID, n2.ID))
            n1.neighbours.append(n2)
            n2.neighbours.append(n1)
            #Latency implementation
            p = np.random.uniform(10, 500)*1e-3
            speed = 0
            if n1.speed == "slow" or n2.speed == "slow":
                speed = c_slow
            else:
                speed = c_fast
            d = 96e3/speed
            latency[(n1.ID, n2.ID)] = (p, speed, d)

            #Removing nodes with no more neighbours
            number_of_neighbours[n1.ID] -= 1
            number_of_neighbours[n2.ID] -= 1
            if number_of_neighbours[n1.ID] == 0:
                nodes.remove(n1)
            if number_of_neighbours[n2.ID] == 0:
                nodes.remove(n2)

    # print("Graph created")
    for node in node_list:
        node.latency = latency
    return

def isConnected(nodelist, zeta):
    """
    Checks if the graph is connected
    Solution to part 4 of the assignment
    """
    #Check if the number of neighbours is correct
    for i in nodelist:
        #Adding the check for malicious node
        if i.selfish and len(i.neighbours) < 0.9*zeta*len(nodelist):
            return False
        elif (not i.selfish) and (len(i.neighbours) < 4 or len(i.neighbours) > 8):
            return False
        return True

    #Create a visited array and do BFS
    visited = [False] * len(nodelist)
    queue = []
    queue.append(nodelist[0])
    visited[nodelist[0].ID] = True

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

def prop_delay(node1, node2, msg):
    """
    Returns the time to propagate a message from node1 to node2
    Solution to part 5 of the assignment
    """
    if (node1.ID, node2.ID) in node1.latency.keys():
        (p, speed, d) = node1.latency[(node1.ID, node2.ID)]
        return p + (msg.size)/speed + np.random.exponential(d)
    elif (node2.ID, node1.ID) in node1.latency.keys():
        (p, speed, d) = node1.latency[(node2.ID, node1.ID)]
        return p + (msg.size)/speed + np.random.exponential(d)
    else:
        return 0    