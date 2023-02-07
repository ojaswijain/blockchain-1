# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
Main file to run the simulator
"""

import simpy
from simulator import Simulator
from init import gen_nodes
from graph import create_graph, isConnected

n = 10
z0 = 20
z1 = 50

nodelist = gen_nodes(n, z0*0.01, z1*0.01)
create_graph(nodelist)

while not isConnected(nodelist):
    nodelist = gen_nodes(n, z0, z1)
    create_graph(nodelist)

env = simpy.Environment()
sim_list = []

for node in nodelist:
    node.env = env
    sim_list.append(Simulator(node))

for sim in sim_list:
    sim.simulate()

env.run(until=1e8)