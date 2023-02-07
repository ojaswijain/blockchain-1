# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
File for simulator class using simpy
"""

from time import time
import numpy as np
from init import gen_transaction, create_block


class Simulator:

    def __init__(self, node):
        self.node = node
        self.env = node.env
        self.env.process(self.run())
    
    def simulate(self):
        if (self.node.sim_time - self.node.last_txn_time) > np.random.exponential(self.node.tx_time)/1000:
            gen_transaction(self.node)

        if (self.node.sim_time - self.node.last_block_time) > np.random.exponential(self.node.tx_time)/1000: #TODO: Hashing power
            create_block(self.node)

        return

    def run(self):
        while True:
            yield self.env.timeout(1)
            self.node.sim_time = time()
            self.simulate()
