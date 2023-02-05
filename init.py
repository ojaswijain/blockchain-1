# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
File to initialize and modify the blockchain and the objects
"""

from datetime import datetime
from hashlib import sha256
import numpy as np
from objects import Node, Block, Transaction

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
    

def create_genesis_block():
    """
    Creates the genesis block
    """
    return Block(0, datetime.now(), "Genesis Block", "0")

def hash_block(block):
    """
    Hashes a block
    """
    content = str(block.BlkID) + str(block.timestamp) + str(block.data) + str(block.previous_hash)
    hash = sha256(content.encode('utf-8')).hexdigest()
    return hash

def next_block(last_block, data):
    index = last_block.index + 1
    timestamp = datetime.now()
    data = data
    hash = hash_block(last_block)
    return Block(index, timestamp, data, hash)