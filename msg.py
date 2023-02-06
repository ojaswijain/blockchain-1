# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
Handling transmission and reception of tranasctions
"""

from objects import Transaction, Block, Node
from graph import prop_delay

def broadcast_transaction(txn, node, time):
    """
    Broadcasts a transaction from a node
    """
    for neighbour in node.neighbours:
        if txn not in neighbour.txn_queue.keys() and not (node == neighbour):
            neighbour.unused_txns.append(txn)
            time = time + prop_delay(node, neighbour, txn)
            neighbour.txn_queue[txn] = time
            broadcast_transaction(txn, neighbour, time)
    return

def broadcast_block(block, node, time):
    """
    Broadcasts a block from a node
    """
    for neighbour in node.neighbours:
        if block not in neighbour.block_queue.keys() and not (node == neighbour):
            time = time + prop_delay(node, neighbour, block)
            neighbour.block_queue[block.BlkID] = time
            if not(neighbour.isFork()):
                neighbour.update(block, time)
                broadcast_block(block, neighbour, time)
    return


    


