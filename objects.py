# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
Objects to be used in the simulator
"""

import numpy as np

class Node:
    """
    Node class
    ID = unique ID of the node (int)
    speed = speed of the node (slow, fast) (enum)
    CPU = CPU of the node(low, high) (enum)
    Balance = balance of the node (string)
    blockchain = blockchain of the node (list)
    connected_nodes = list of connected nodes (list)
    """
    def __init__(self, ID, speed, CPU):
        self.ID = ID
        self.speed = speed
        self.CPU = CPU
        self.balance = 0
        self.blockchain = []
        self.neighbours = []

class Graph:
    """
    Graph class
    nodes = list of nodes (list)
    edges = list of edges (list)
    latencies = list of latencies (list)
    """
    def __init__(self, nodes, edges, latencies):
        self.nodes = nodes
        self.edges = edges
        self.latencies = latencies

class Block:
    """
    Block class
    BlkID = unique ID of the block (int)
    timestamp = timestamp of the block (datetime)
    data = data of the block (string)
    previous_hash = hash of the previous block (string)
    """
    def __init__(self, BlkID, timestamp, data, previous_hash):
        self.BlkID = BlkID
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash

class Transaction:
    """
    Transaction class
    TxID = unique ID of the transaction (int)
    sender = sender of the transaction (int)
    receiver = receiver of the transaction (int)
    amount = amount of the transaction (int)
    size = size of the transaction (int (KB))
    """
    def __init__(self, TxID, sender, receiver, amount):
        self.TxID = TxID
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.size = 1



