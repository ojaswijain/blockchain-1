# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
"""

from datetime import datetime
from hashlib import sha256
import json
import numpy as np

class Node:
    def __init__(self, ID, speed, CPU, IP, port):
        self.ID = ID
        self.speed = speed
        self.CPU = CPU
        self.IP = IP
        self.port = port
        self.balance = 0
        self.blockchain = []

class Block:
    def __init__(self, BlkID, timestamp, data, previous_hash):
        self.BlkID = BlkID
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash

class Transaction:
    def __init__(self, TxID, sender, receiver, amount):
        self.TxID = TxID
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

def create_genesis_block():
    return Block(0, datetime.now(), "Genesis Block", "0")

def hash_block(block):
    content = str(block.BlkID) + str(block.timestamp) + str(block.data) + str(block.previous_hash)
    hash = sha256(content.encode('utf-8')).hexdigest()
    return hash

def next_block(last_block, data):
    index = last_block.index + 1
    timestamp = datetime.now()
    data = data
    hash = hash_block(last_block)
    return Block(index, timestamp, data, hash)










