# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
Handling transmission and reception of tranasctions
"""

from graph import prop_delay
from simulator import Event

def broadcast_transaction(txn, node, time):
    """
    Broadcasts a transaction from a node
    Solution to part 6 of the assignment
    """
    events = []
    node.txn_queue[txn.TxID] = time
    for neighbour in node.neighbours:
        if txn.TxID not in neighbour.txn_queue.keys():
            neighbour.unused_txns.append(txn)
            time_new = time + prop_delay(node, neighbour, txn)
            neighbour.txn_queue[txn.TxID] = time_new
            events.append(Event(time_new, neighbour, "txn", txn))
    return events

def broadcast_block(block, node, time):
    """
    Broadcasts a block from a node
    """
    events = []
    if block.BlkID not in node.block_queue.keys():
            print("Block: ", block.BlkID, " broadcasted by node: ", node.ID, " at time: ", time)
            node.block_queue[block.BlkID]=time
            newledger = node.ledger.copy()
            for txn in block.data:
                if txn.sender is not None:
                    newledger[txn.sender]-=txn.amount
                    if(newledger[txn.sender]<0):
                        print("Error: Negative balance")
                        return []
                newledger[txn.receiver]+=txn.amount
            # node.ledger = newledger
            node.update(block, time)
            
            for neighbour in node.neighbours:
                delay = prop_delay(node, neighbour, block)
                time_new = time + delay
                events.append(Event(time_new, neighbour, "block", block))
    return events