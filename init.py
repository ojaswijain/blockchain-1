# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
File to initialize and modify the blockchain and the objects
"""

from time import time
from hashlib import sha256
import numpy as np
from objects import Node, Block, Transaction
from graph import Graph
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
        node_list.append(Node(i+1, speed_enum[speed[i]], type_enum[type[i]]))
    return node_list
    
def gen_transaction(sender):
    """
    Generates a transaction
    """
    receiver = np.random.choice(sender.neighbours)
    amount = np.random.randint(1, sender.balance)
    txn = Transaction(sender, receiver, amount)
    sender.unused_txns.append(txn)
    sender.last_txn_time = txn.timestamp
    broadcast_transaction(txn, sender, txn.timestamp)

def create_block(node):
    """
    Creates a block
    """
    if len(node.unused_txns) == 0:
        return
    #Creating a block
    block = Block(node)
    block.timestamp = time()
    block.parent = node.last_block
    #Adding transactions
    for txn in node.unused_txns[:10]:
        block.data.append(txn)
    #Adding block to blockchain
    node.update(block, block.timestamp)
    #Removing transactions from unused_txns
    node.unused_txns = node.unused_txns[10:]
    #Broadcasting block
    broadcast_block(block, node, block.timestamp)
    node.balance += block.reward