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
from visualise import visualise_chain

class Transaction:
    """
    Transaction class
    TxID = unique ID of the transaction (string)
    sender = sender of the transaction (int)
    Put sender as None if mining fee is the transaction
    receiver = receiver of the transaction (int)
    amount = amount of the transaction (int)
    size = size of the transaction (int (bits))
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
    """
    reward = 50
    def __init__(self, data):
        self.timestamp = time()
        self.BlkID = sha256((str(np.random.randint(1,1000))+str(self.timestamp)).encode('utf-8')).hexdigest()
        self.data = data
        self.size = 0
        self.parent = None
        self.chain_length = 1

class BlockChain:
    """
    BlockChain class
    chain = list of blocks (list)
    """
    # chain = []
    def __init__(self, blk, number_of_nodes):
        ledger = {}
        
        for i in range(number_of_nodes):
            for j in range(number_of_nodes):
                idx = j
                ledger[idx] = 1000
        
        self.chain=[(blk, ledger)]

    def add_block(self, blk):

        # Check if block already exists
        for (block, ledger) in self.chain:
            if blk.BlkID == block.BlkID:
                print("Block already in chain")
                return None

        # Check if parent exists
        newledger = {}
        check = False
        for (block, ledger) in self.chain:
            if blk.parent.BlkID == block.BlkID:
                newledger = ledger.copy()
                check = True
        if check == False:
            print("Parent not in chain")
            return None
        
        # Check if parent is the last block    
        blk.chain_length = blk.parent.chain_length + 1

        for txn in block.data:
                    #TODO: Update ledger
            if txn.sender is not None:
                newledger[txn.sender]-=txn.amount
            newledger[txn.receiver]+=txn.amount
        self.chain.append((blk, newledger))
        return newledger
    
    def show_chain(self):
        for (block, ledger) in self.chain:
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
    
    init_time = time()
    interArrival = 2
    genesisBlock = Block([])
    genesisBlock.blkid = sha256(str(0).encode('utf-8')).hexdigest()
    chain = BlockChain(genesisBlock, 100)

    def __init__(self, ID, speed, CPU, number_of_nodes):
        

        self.ID = ID
        self.sim_time = time()
        self.speed = speed
        self.CPU = CPU
        self.balance = 1000
        self.neighbours = []
        self.env = env
        self.tx_time = 1e-2
        self.Tk_mean = None
        self.Tk = None
        ledger = {}
        
        for i in range(number_of_nodes):
            for j in range(number_of_nodes):
                idx = j
                ledger[idx] = 1000
        
        # self.tk = self.init_time
        # self.Tk = np.random.exponential(600/self.CPU)
        self.unused_txns = []
        self.LocalChain = copy.deepcopy(self.chain)
        self.last_block = self.genesisBlock
        self.last_block_time = self.init_time
        self.last_txn_time = self.init_time
        self.block_queue = {}
        self.txn_queue = {}
        self.last_ledger = ledger
        self.latency = {}
    
    # def trycreateblock(self, time):
    #     Tk = xxx
    #     if(self.last_block_time )

    def isFork(self, block):
        if block.parent.BlkID == self.last_block.BlkID:
            return False
        print("Fork detected")
        if block.chain_length > self.last_block.chain_length:
            return True
        return False

    def update(self, block, time):
        newledger = self.LocalChain.add_block(block)
        if newledger:
            print("Block with ID: " + block.BlkID + " added to node " + str(self.ID))
            with open(f"log/log_node{self.ID}.txt", "a") as f:
                f.write("Block ID: " + block.BlkID[:5] + " at " + str(time)+"\n")
            if not self.isFork(block) and block.chain_length > self.last_block.chain_length:
                self.last_block = block
                self.last_ledger = newledger
                print(block.BlkID, " added to ", self.ID)
                self.last_block_time = time
                # for txn in block.data:
                #     #TODO: Update ledger
                #     if txn.sender is not None:
                #         self.ledger[txn.sender]-=txn.amount
                #     self.ledger[txn.receiver]+=txn.amount
                #     if txn in self.unused_txns: 
                #         self.unused_txns.remove(txn)
                visualise_chain(self)
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
                        # if txn.sender is not None:
                        #     self.ledger[txn.sender]+=txn.amount
                        # self.ledger[txn.receiver]-=txn.amount
                    old_last = old_last.parent
                
                while parent.BlkID != common.BlkID:
                    for txn in parent.data:
                        if txn in self.unused_txns:
                            self.unused_txns.remove(txn)
                        # if txn.sender is not None:
                        #     self.ledger[txn.sender]-=txn.amount
                        # self.ledger[txn.receiver]+=txn.amount
                    parent = parent.parent

                # for txn in block.data:
                #     if txn.sender is not None:
                #         self.ledger[txn.sender]-=txn.amount
                #     self.ledger[txn.receiver]+=txn.amount
                #     if txn in self.unused_txns: 
                #         self.unused_txns.remove(txn)

                self.last_block = block
                self.last_ledger = newledger
                self.last_block_time = time
                for txn in block.data:
                    if txn in self.unused_txns:
                        self.unused_txns.remove(txn)
                visualise_chain(self)
                return True   

    def validate_block(self, block):
        parent = block.parent
        check = False
        checkledger = {}
        for (blk, ledger) in self.LocalChain.chain:
            if blk.BlkID == parent.BlkID:
                check = True
                checkledger = ledger.copy()
        if check == False:
            print("Parent not in chain")
            return False  

        parent = block.parent

        for txn in block.data:
            if txn.sender is not None:
                checkledger[txn.sender]-=txn.amount
                if(checkledger[txn.sender]<0):
                    return False
            checkledger[txn.receiver]+=txn.amount
        print("Validated ", block.BlkID, self.ID)
        return True

env = None