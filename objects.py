# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
Objects to be used in the simulator
"""

import numpy as np
from hashlib import sha256
from time import time
import copy

class Transaction:
    """
    Transaction class
    TxID = unique ID of the transaction (string)
    sender = sender of the transaction (int)
    Put sender as None if mining fee is the transaction
    receiver = receiver of the transaction (int)
    amount = amount of the transaction (int)
    size = size of the transaction (int (bits))
    Solution to part 3 of the assignment
    """
    def __init__(self, sender, receiver, amount):
        self.timestamp = time()
        self.TxID = sha256((str(np.random.randint(1,1000))+str(self.timestamp)).encode('utf-8')).hexdigest()
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.size = 8e3
        self.string = None

        def __str__(self):
            if self.sender is not None:
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
    parent = parent of the block (block)
    chain_length = length of the chain (int)
    """
    reward = 50
    def __init__(self, data):
        self.timestamp = time()
        self.BlkID = sha256((str(np.random.randint(1,1000))+str(self.timestamp)).encode('utf-8')).hexdigest()
        self.data = data
        self.size = 0
        self.parent = None
        self.chain_length = 1
        self.x = 0

class BlockChain:
    """
    BlockChain class
    chain = list of blocks (list)
    """
    
    def __init__(self, blk):
        self.chain=[blk]

    def add_block(self, blk):

        # Check if block already exists
        for block in self.chain:
            if blk.BlkID == block.BlkID:
                print("Block already in chain")
                return False

        # Check if parent exists
        check = False
        for block in self.chain:
            if blk.parent.BlkID == block.BlkID:
                check = True
        if check == False:
            print("Parent not in chain")
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
    blockchain = blockchain of the node (list)
    neighbours = list of connected nodes (list)
    unused_txns = list of unused transactions (list)
    LocalChain = local blockchain of the node (list)
    last_block = last block of the node (block)
    last_block_time = timestamp of the last block (datetime)
    last_txn_time = timestamp of the last transaction (datetime)
    block_queue = queue of blocks to be added to the blockchain (dict)
    txn_queue = queue of transactions to be added to the blockchain (dict)
    ledger = ledger of the node (dict)
    latency = latency of the node (dict)
    """
    genesisBlock = Block([])
    genesisBlock.BlkID = "Genesis"
    chain = BlockChain(genesisBlock)
    init_time = time()
    interArrival = 0.8

    def __init__(self, ID, speed, CPU):
        self.ID = ID
        self.sim_time = time()
        self.speed = speed
        self.CPU = CPU
        self.neighbours = []
        #Transaction generation parameters, solution to part 2 of the assignment
        self.tx_time = 1e-3
        self.Tk_mean = None
        self.Tk = None

        self.unused_txns = []
        self.LocalChain = copy.deepcopy(self.chain)
        self.last_block = self.genesisBlock
        self.last_block_time = self.init_time
        self.last_txn_time = self.init_time
        self.block_queue = {}
        self.txn_queue = {}
        self.ledger = {}
        self.latency = {}

    def isFork(self, block):
        """
        Checks if the block is a fork
        """
        if block.parent.BlkID == self.last_block.BlkID:
            return False
        print("Fork detected")
        if block.chain_length > self.last_block.chain_length:
            return True
        return False

    def update(self, block, time):
        """
        Updates the node with the new block
        """
        if self.LocalChain.add_block(block):
            print("Block with ID: " + block.BlkID + " added to node " + str(self.ID))
            with open(f"log/log_node{self.ID}.txt", "a") as f:
                """
                Write to log file
                Solution to part 8 of the assignment
                """
                f.write("Block ID: " + block.BlkID[:5] + " at " + str(time)+"\n")
            if not self.isFork(block) and block.chain_length > self.last_block.chain_length:
                """
                Update the node if the block is not a fork and the chain length is greater than the last block
                """
                self.last_block = block
                self.last_block_time = time
                for txn in block.data:
                    if txn.sender is not None:
                        self.ledger[txn.sender]-=txn.amount
                    self.ledger[txn.receiver]+=txn.amount
                    if txn in self.unused_txns: 
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
                        if txn.sender is not None:
                            self.ledger[txn.sender]+=txn.amount
                        self.ledger[txn.receiver]-=txn.amount
                    old_last = old_last.parent
                
                while parent.BlkID != common.BlkID:
                    for txn in parent.data:
                        if txn in self.unused_txns:
                            self.unused_txns.remove(txn)
                        if txn.sender is not None:
                            self.ledger[txn.sender]-=txn.amount
                        self.ledger[txn.receiver]+=txn.amount
                    parent = parent.parent

                self.last_block = block
                self.last_block_time = time
                for txn in block.data:
                    if txn in self.unused_txns:
                        if txn.sender is not None:
                            self.ledger[txn.sender]-=txn.amount
                        self.ledger[txn.receiver]+=txn.amount
                        self.unused_txns.remove(txn)
                return True           