# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
Handling transmission and reception of tranasctions
"""

from graph import prop_delay
from simulator import EventQueue, Event

#TODO: Change DFS to BFS

def broadcast_transaction(txn, node, time):
    """
    Broadcasts a transaction from a node
    """
    events = []
    node.txn_queue[txn.TxID] = time
    for neighbour in node.neighbours:
        if txn.TxID not in neighbour.txn_queue.keys():
            neighbour.unused_txns.append(txn)
            time_new = time + prop_delay(node, neighbour, txn)
            neighbour.txn_queue[txn.TxID] = time_new
            # broadcast_transaction(txn, neighbour, time)
            events.append(Event(time_new, neighbour, "txn", txn))
    return events

def broadcast_block(block, node, time):
    """
    Broadcasts a block from a node
    """
    # print("Block: ", block.BlkID, " broadcasted by node: ", node.ID, " at time: ", time)
    events = []
    for neighbour in node.neighbours:
        if block.BlkID not in neighbour.block_queue.keys():
            delay = prop_delay(node, neighbour, block)
            time_new = time + delay
            neighbour.block_queue[block.BlkID] = time
            if(neighbour.validate_block(block)==False):
                return []
            neighbour.update(block, time_new)
            # broadcast_block(block, neighbour, time_new)
            events.append(Event(time_new, neighbour, "block", block))
    return events