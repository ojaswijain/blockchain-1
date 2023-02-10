# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
File for simulator class using simpy
"""

# from time import time
# import numpy as np
# from init import gen_transaction, create_block
# from multiprocessing import Process

#TODO: Why is this cyclic and not parallel


# class Simulator:

#     def __init__(self, node):
#         self.node = node
#         self.env = node.env
#         self.env.process(self.run())
    
#     def simulate(self):
#         if (self.node.sim_time - self.node.last_txn_time) > np.random.exponential(self.node.tx_time):
#             gen_transaction(self.node)

#         if (self.node.sim_time - self.node.last_block_time) > self.node.Tk:
#             create_block(self.node)


#     def run(self):
#         while True:
#             yield self.env.timeout(1)
#             self.node.sim_time = time()
#             # print("At node: ", self.node.ID, "at time: ", self.node.sim_time)
#             self.simulate()

import heapq

class Event:
    def __init__(self, time, src, event_type, data):
        self.time = time
        self.src = src
        self.type = event_type
        self.data = data

    def __lt__(self, other):
        return self.time < other.time

class EventQueue:
    def __init__(self):
        self.queue = []

    def push(self, event):
        heapq.heappush(self.queue, event)

    def pop(self):
        return heapq.heappop(self.queue)

    def empty(self):
        return len(self.queue) == 0

    def __len__(self):
        return len(self.queue)

    def __repr__(self):
        return str(self.queue)

