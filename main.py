# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023
@author: ojaswi
Building a discrete event simulator for a P2P cryptocurrency network
Main file to run the simulator
"""

import numpy as np
from simulator import EventQueue
from init import gen_nodes
from graph import create_graph, isConnected
from visualise import visualise_chain, visualise_tree
from init import gen_transaction, create_block
from time import time 
from msg import broadcast_transaction, broadcast_block
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number_of_nodes", type=int, default=100)
    parser.add_argument("-z0", "--z0", type=float, default=0.2)
    parser.add_argument("-z1", "--z1", type=float, default=0.5)
    parser.add_argument("-t", "--time", type=int, default=60)
    parser.add_argument("-p", "--power", type=float, default=1.5)
    parser.add_argument("-z", "--zeta", type=float, default=0.25)

    args = parser.parse_args()
    n = args.number_of_nodes
    z0 = args.z0
    z1 = args.z1
    t = args.time
    p = args.power
    zeta = args.zeta

    nodelist = gen_nodes(n, z0, z1, selfish=True, power=p)
    create_graph(nodelist, zeta)
    print(len(nodelist[0].neighbours), zeta*n)

    while not isConnected(nodelist, zeta):
        nodelist = gen_nodes(n, z0, z1, selfish=True, power=p)
        create_graph(nodelist, zeta)
        print(len(nodelist[0].neighbours), zeta*n)

    # visualise_tree(nodelist)
    # exit(0)
    # print(len(nodelist[0].neighbours), zeta*n)

    start = time()
    que = EventQueue()
    while time() - start < t:
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
        
        events = []
        new_event = []

        while len(que) > 0 and que.queue[0].time < time():
            events.append(que.pop())
            
        for event in events:
            if event.type == "txn":
                new_event = broadcast_transaction(event.data, event.src, event.time)
            else:
                new_event = broadcast_block(event.data, event.src, event.time)
            for e in new_event:
                que.push(e)

    print(len(nodelist[0].LocalChain.chain))
    print(len(nodelist[1].LocalChain.chain))

    for node in nodelist:
        visualise_chain(node)

    for node in nodelist:
        with open("ledgers/ledger_" + str(node.ID) + ".txt", "w") as f:
            for i in range(n):
                f.write(str(node.ledger[i]) + "\n")