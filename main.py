# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
Main file to run the simulator
"""

from simulator import EventQueue
from init import gen_nodes
from graph import create_graph, isConnected
from visualise import visualise_tree
from init import gen_transaction, create_block
from time import time 
import numpy as np
from msg import broadcast_transaction, broadcast_block

n = 100
z0 = 20
z1 = 50

if __name__ == '__main__':

    nodelist = gen_nodes(n, z0*0.01, z1*0.01)
    create_graph(nodelist)

    while not isConnected(nodelist):
        nodelist = gen_nodes(n, z0, z1)
        create_graph(nodelist)

    que = EventQueue()
    while True:
        for node in nodelist:
            if (time() - node.last_txn_time) > np.random.exponential(node.tx_time):
                events = gen_transaction(node)
                for event in events:
                    que.push(event)
            if (time() - node.last_block_time) > node.Tk:
                events = create_block(node)
                for event in events:
                    que.push(event)
        if len(que) == 0:
            continue
        event = que.pop()
        if event.type == "txn":
            new_event = broadcast_transaction(event.data, event.src, event.time)
        else:
            new_event = broadcast_block(event.data, event.src, event.time)
        for e in new_event:
            que.push(e)

    # p_list = []
    # for node in nodelist:
    #     p = Process(target= run, args = [node])
    #     p_list.append(p)
    # for p in p_list:
    #     p.start()
    # p.join()


    # for node in nodelist:
    #     print(node.ID, len(node.neighbours))
    # visualise_tree(nodelist)

# if __name__ == '__main__':

#     nodelist = gen_nodes(n, z0*0.01, z1*0.01)
#     create_graph(nodelist)

#     while not isConnected(nodelist):
#         nodelist = gen_nodes(n, z0, z1)
#         create_graph(nodelist)
    
#     sim_list = []
#     env = simpy.Environment()

#     for node in nodelist:
#         node.env = env
#         sim_list.append(Simulator(node))
    
#     for sim in sim_list:
#         sim.simulate()

#     env.run(until=10000)
    # p_list = []
    # for node in nodelist:
    #     p = Process(target= run, args = [node])
    #     p_list.append(p)
    # for p in p_list:
    #     p.start()
    # p.join()


    # for node in nodelist:
    #     print(node.ID, len(node.neighbours))
    # visualise_tree(nodelist)