# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
Handling transmission and reception of tranasctions
"""

from objects import Transaction, Block, Node

def transmit_transaction(txn, node, time):
    """
    Transmits a transaction to a node
    """
    for neighbour in node.neighbours:
        if txn not in neighbour.txn_queue.keys():
            neighbour.unused_txns.append(txn)


    pass

def transmit_block(block, node):
    """
    Transmits a block to a node
    """
    pass

def receive_transaction(transaction, node):
    """
    Receives a transaction from a node
    """
    pass

def receive_block(block, node):
    """
    Receives a block from a node
    """
    pass


    


