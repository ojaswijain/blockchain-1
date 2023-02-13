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
from visualise import visualise_chain
from init import gen_transaction, create_block
from time import time 
from msg import broadcast_transaction, broadcast_block

n = 20
z0 = 0.2
z1 = 0.5

if __name__ == '__main__':

    nodelist = gen_nodes(n, z0, z1)
    create_graph(nodelist)

    while not isConnected(nodelist):
        nodelist = gen_nodes(n, z0, z1)
        create_graph(nodelist)

    start = time()
    que = EventQueue()
    while time() - start < 20:
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
        while len(que) > 0 and que.queue[0].time < time():
            events.append(que.pop())
            
        for event in events:
            if event.type == "txn":
                new_event = broadcast_transaction(event.data, event.src, event.time)
            else:
                new_event = broadcast_block(event.data, event.src, event.time)
            for e in new_event:
                que.push(e)

    for node in nodelist:
        visualise_chain(node)

    for node in nodelist:
        with open("ledgers/ledger_" + str(node.ID) + ".txt", "w") as f:
            for i in range(n):
                f.write(str(node.ledger[i]) + "\n")