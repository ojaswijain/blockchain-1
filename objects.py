# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
Objects to be used in the simulator
"""

import numpy as np
import simpy
from hashlib import sha256
from datetime import datetime

class Transaction:
    """
    Transaction class
    TxID = unique ID of the transaction (string)
    sender = sender of the transaction (int)
    Put sender as -1 if mining fee is the transaction
    receiver = receiver of the transaction (int)
    amount = amount of the transaction (int)
    size = size of the transaction (int (bits))
    """
    def __init__(self, sender, receiver, amount):
        self.timestamp = datetime.now()
        self.TxID = sha256(str(self.timestamp).encode('utf-8')).hexdigest()
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.size = 8e3
        self.string = None
        self.inChain = False

        def __str__(self):
            if self.sender is not -1:
                self.string = str(self.TxID) + ": " + str(self.sender) + " pays " + str(self.receiver) + str(self.amount) + " coins"
            else:
                self.string = str(self.TxID) + ": " + str(self.sender) + " mines " + str(self.amount) + " coins"
            return self.string

class Block:
    """
    Block class
    BlkID = unique ID of the block (string)
    timestamp = timestamp of the block (datetime)
    data = data of the block (string)
    size = size of the block (int (bits))
    """
    def __init__(self, data, miner):
        self.timestamp = datetime.now()
        self.BlkID = sha256(str(datetime.now()).encode('utf-8')).hexdigest()
        self.data = data
        self.size = 8e3
        self.parent = None
        self.miner = miner

class BlockChain:
    """
    BlockChain class
    chain = list of blocks (list)
    """
    chain = []
    def __init__(self, blk):
        self.chain.append(blk)

    def add_block(self, blk):
        for block in self.chain:
            if blk.BlkID == block.BlkID:
                return False
        last_block = self.chain[-1]
        blk.parent = last_block.BlkID
        self.chain.append(blk)
        return True
    
    def get_block(self):
        return self.chain[-1]
    
    def show_chain(self):
        for block in self.chain:
            print(block.BlkID)

class Node:
    """
    Node class
    ID = unique ID of the node (int)
    speed = speed of the node (slow, fast) (enum)
    CPU = CPU of the node(low, high) (enum)
    Balance = balance of the node (string)
    blockchain = blockchain of the node (list)
    neighbours = list of connected nodes (list)
    unused_transactions = list of unused transactions (list)
    env = environment (simpy)
    """
    genesisBlock = Block([],None)
    genesisBlock.blkid = sha256(str(0).encode('utf-8')).hexdigest()
    chain = BlockChain(genesisBlock)
    init_time = datetime.now()

    def __init__(self, ID, speed, CPU, env):
        self.ID = ID
        self.speed = speed
        self.CPU = CPU
        self.balance = 1000
        self.neighbours = []
        self.unused_transactions = []
        self.blocklist = [self.genesisBlock]
        self.env = env
        self.LocalChain = self.chain
        self.last_block = self.genesisBlock
        self.last_block_time = self.init_time
        self.last_txn_time = self.init_time
        self.tx_time = None #TODO
        self.tx_queue = {}
        self.blk_queue = {}

class Graph:
    """
    Graph class
    nodes = list of nodes (list)
    latency = list of latencies (list)
    """
    def __init__(self, nodes, latency):
        self.nodes = nodes
        self.latency = latency



