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
    parser.add_argument("-n", "--number_of_nodes", type=int, default=20)
    parser.add_argument("-z0", "--z0", type=float, default=0.2)
    parser.add_argument("-z1", "--z1", type=float, default=0.5)
    parser.add_argument("-t", "--time", type=int, default=90)
    parser.add_argument("-p", "--power", type=int, default=1.5)

    args = parser.parse_args()
    n = args.number_of_nodes
    z0 = args.z0
    z1 = args.z1
    t = args.time
    p = args.power

    nodelist = gen_nodes(n, z0, z1, selfish=True, power=p)
    create_graph(nodelist)

    while not isConnected(nodelist):
        nodelist = gen_nodes(n, z0, z1, selfish=True, power=p)
        create_graph(nodelist)

    # visualise_tree(nodelist)
    # exit(0)

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

    # print(len(nodelist[0].LocalChain.chain))
    # print(len(nodelist[1].LocalChain.chain))

    chainhonest = nodelist[1].LocalChain.chain
    chainad = nodelist[9].LocalChain.chain

    maxlen = chainhonest[0].chain_length

    for i in range(len(chainhonest)):
        # if(chainhonest[i].BlkID == "Genesis"):
        #     continue
        # if(chainhonest[i].creator in blocksby.keys()):
        #     blocksby[chain[i].creator]+=1
        # else:
        #     blocksby[chain[i].creator]=1
        if(chainhonest[i].chain_length > maxlen):
            maxlenat = i
            maxlen = chainhonest[i].chain_length
        elif(chainhonest[i].chain_length == maxlen and chainhonest[i].malice):
            maxlenat = i

    maliceinmain = 0
    totalinmain = 1
    block = chainhonest[maxlenat]
    while(block.BlkID!="Genesis"):
        totalinmain += 1
        if(block.malice):
            maliceinmain+=1
        block = block.parent
    
    # for node in nodelist:
    #     if(node.ID in blocksby.keys()):
    #         print(node.ID, blocksby[node.ID])
    #     else:
    #         print(node.ID, 0)
    # print(nodelist[0].forkcount)
    # print(len(chain))
    count = 0

    for block in nodelist[0].LocalChain.chain:
        if block.malice:
            count+=1
    
    # print("malice count = ", count)
    # print("total length = ", totalinmain)

    # print("lead = ", len(nodelist[0].pvtChain))
    # # print(len(nodelist[1].pvtChain))

    print("MPUavg = ",maliceinmain/count)
    print("MPUoverall = ", totalinmain/len(nodelist[0].LocalChain.chain))

    for node in nodelist:
        visualise_chain(node)

    for node in nodelist:
        with open("ledgers/ledger_" + str(node.ID) + ".txt", "w") as f:
            for i in range(n):
                f.write(str(node.ledger[i]) + "\n")