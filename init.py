# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
File to initialize and modify the blockchain and the objects
"""

from time import time
import numpy as np
from objects import Node, Block, Transaction
from msg import broadcast_transaction, broadcast_block

def gen_nodes(number_of_nodes, z0, z1):
    """
    Generates a list of nodes
    """
    node_list = []
    speed = np.random.choice([0,1], number_of_nodes, p=[z0, 1-z0])
    type = np.random.choice([0,1], number_of_nodes, p=[z1, 1-z1])
    speed_enum = {0: "slow", 1: "fast"}
    type_enum = {0: "low", 1: "high"}
    for i in range(number_of_nodes):
        node_list.append(Node(i, speed_enum[speed[i]], type_enum[type[i]]))
    for i in range(number_of_nodes):
        for j in range(number_of_nodes):
            idx = j
            node_list[i].ledger[idx] = 1000
    h = 1/((10*(1-z1)+z1)*number_of_nodes)
    for i in range(number_of_nodes):
        if node_list[i].speed == "low":
            node_list[i].Tk_mean = node_list[i].interArrival/h
        else:
            node_list[i].Tk_mean = node_list[i].interArrival/(h*10)
        node_list[i].Tk = np.random.exponential(node_list[i].Tk_mean)
    return node_list
    
def gen_transaction(sender):
    """
    Generates a transaction
    """
    receiver = np.random.choice(sender.neighbours)
    amount = np.random.randint(1, sender.balance)
    txn = Transaction(sender.ID, receiver.ID, amount)
    sender.unused_txns.append(txn)
    sender.last_txn_time = txn.timestamp
    # print("Transaction with TxID: ", txn.TxID, " created by node: ", sender.ID, "to node: ", receiver.ID, "at time: ", txn.timestamp)
    broadcast_transaction(txn, sender, txn.timestamp)

def create_block(node):
    """
    Creates a block
    """
    if len(node.unused_txns) == 0:
        return
    #Creating a block
    newledger = node.ledger.copy()
    block = Block([])
    block.parent = node.last_block
    print("Block with ID: ", block.BlkID, " created by node: ", node.ID)
    block.timestamp = time()
    block.parent = node.last_block
    #Adding transactions
    for txn in node.unused_txns[:10]:
        newledger[txn.sender]-=txn.amount
        newledger[txn.receiver]+=txn.amount
        if(newledger[txn.sender]<0):
            return
        block.data.append(txn)
        block.size += txn.size
    #Adding miner reward
    txn_miner = Transaction(None, node.ID, block.reward)
    block.data.append(txn_miner)
    block.size += txn_miner.size
    newledger[node.ID]+=block.reward
    node.ledger = newledger
    #Adding block to blockchain
    node.update(block, block.timestamp)
    #Removing transactions from unused_txns
    node.unused_txns = node.unused_txns[10:]
    #Broadcasting block
    broadcast_block(block, node, block.timestamp)
    node.balance += block.reward
    node.Tk = np.random.exponential(node.Tk_mean)