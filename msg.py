# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
Handling transmission and reception of tranasctions
"""

from graph import prop_delay
from init import create_block
import numpy

def broadcast_transaction(txn, node, time):
    """
    Broadcasts a transaction from a node
    """
    node.txn_queue[txn.TxID] = time
    for neighbour in node.neighbours:
        if txn.TxID not in neighbour.txn_queue.keys():
            neighbour.unused_txns.append(txn)
            time = time + prop_delay(node, neighbour, txn)
            neighbour.txn_queue[txn.TxID] = time
            broadcast_transaction(txn, neighbour, time)
    return

def broadcast_block(block, node, time):
    """
    Broadcasts a block from a node
    """
    node.block_queue[block.BlkID] = time

    if(node.tk + node.Tk < time):
        create_block(node)
    
    node.tk = time
    node.Tk = numpy.random.exponential(600/node.CPU)
    for neighbour in node.neighbours:
        if block.BlkID not in neighbour.block_queue.keys():
            time = time + prop_delay(node, neighbour, block)
            neighbour.block_queue[block.BlkID] = time
            neighbour.update(block, time)
            broadcast_block(block, neighbour, time)
    return


    


