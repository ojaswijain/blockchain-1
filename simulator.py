# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
File for simulator class using simpy
"""

from time import time
import numpy as np
from init import gen_transaction, gen_block


class Simulator:

    def __init__(self, node):
        self.node = node
        self.env.process(self.run())

    def env(self):
        return self.node.env
    
    def simulate(self):
        if (self.node.sim_time - self.node.last_txn_time) > np.random.exponential(self.node.tx_time)/1000:
            self.node.gen_transaction()

        if (self.node.sim_time - self.node.last_block_time) > np.random.exponential(self.node.tx_time)/1000: #TODO: Hashing power
            self.node.create_block()

        return

    def run(self):
        while True:
            yield self.env.timeout(1)
            self.node.sim_time = time()
            self.simulate()
