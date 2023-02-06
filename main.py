# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
Main file to run the simulator
"""

import simpy
import numpy as np
from simulator import Simulator
from init import gen_nodes
from objects import Node, Transaction, Block
from graph import create_graph, isConnected

n = 100
z0 = 0.1
z1 = 0.1


nodelist = gen_nodes(n, z0, z1)
create_graph(nodelist)

while not isConnected(nodelist):
    nodelist = gen_nodes(n, z0, z1)
    create_graph(nodelist)

env = simpy.Environment()
sim_list = []

for node in nodelist:
    print(1)
    sim_list.append(Simulator(node))

for sim in sim_list:
    sim.run()














