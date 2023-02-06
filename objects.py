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
from time import time

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
        self.timestamp = time()
        self.TxID = sha256(str(np.random.randint(1,1000))+(str(self.timestamp).encode('utf-8'))).hexdigest()
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.size = 8e3
        self.string = None

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
    data = data of the block (list of transactions)
    size = size of the block (int (bits))
    """
    reward = 50
    def __init__(self, data):
        self.timestamp = time()
        self.BlkID = sha256(self.timestamp).encode('utf-8').hexdigest()
        self.data = data
        self.size = 8e3
        self.parent = None
        self.chain_length = 1

class BlockChain:
    """
    BlockChain class
    chain = list of blocks (list)
    """
    chain = []
    def __init__(self, blk):
        self.chain.append(blk)

    def add_block(self, blk):

        # Check if block already exists
        for block in self.chain:
            if blk.BlkID == block.BlkID:
                return False

        # Check if parent exists
        check = False
        for block in self.chain:
            if blk.parent.BlkID == block.BlkID:
                check = True
        if check == False:
            return False
        
        # Check if parent is the last block    
        blk.chain_length = blk.parent.chain_length + 1
        self.chain.append(blk)
        return True
    
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
    unused_txns = list of unused transactions (list)
    env = environment (simpy)
    """
    genesisBlock = Block([],None)
    genesisBlock.blkid = sha256(str(0).encode('utf-8')).hexdigest()
    chain = BlockChain(genesisBlock)
    init_time = time()

    def __init__(self, ID, speed, CPU, env):
        self.ID = ID
        self.speed = speed
        self.CPU = CPU
        self.balance = 1000
        self.neighbours = []
        self.env = env
        self.tx_time = None #TODO: Same for all?
        self.graph = None

        self.tk = self.init_time
        self.Tk = np.random.exponential(600/self.CPU)
        self.unused_txns = []
        self.LocalChain = self.chain
        self.last_block = self.genesisBlock
        self.last_block_time = self.init_time
        self.last_txn_time = self.init_time
        self.blk_queue = {}
        self.txn_queue = {}
        self.ledger = {}
    
    # def trycreateblock(self, time):
    #     Tk = xxx
    #     if(self.last_block_time )

    def isFork(self, block):
        if block.parent.BlkID == self.last_block.BlkID:
            return False
        if block.chain_length > self.last_block.chain_length:
            return True
        return False

    def update(self, block, time):
        if self.LocalChain.add_block(block):
            if not self.isFork(block) and block.chain_length > self.last_block.chain_length:
                self.last_block = block
                self.last_block_time = time
                for txn in block.data:
                    #TODO: Update ledger
                    self.unused_txns.remove(txn)
                return True
            elif self.isFork(block):
                parent = block.parent
                old_last = self.last_block
                common = None
                
                while parent.BlkID != old_last.BlkID:
                    old_last = old_last.parent
                    parent = parent.parent
                common = parent
                parent = block.parent
                old_last = self.last_block
                
                while old_last.BlkID != common.BlkID:
                    for txn in old_last.data:
                        self.unused_txns.append(txn)
                    old_last = old_last.parent
                
                while parent.BlkID != common.BlkID:
                    for txn in parent.data:
                        self.unused_txns.remove(txn)
                    parent = parent.parent

                self.last_block = block
                self.last_block_time = time
                for txn in block.data:
                    self.unused_txns.remove(txn)
                return True           

class Graph:
    """
    Graph class
    nodes = list of nodes (list)
    latency = list of latencies (dictionary)
    """
    def __init__(self, nodes, latency):
        self.nodes = nodes
        self.latency = latency



