# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
Handling transmission and reception of tranasctions
"""

from graph import prop_delay

#TODO: Change DFS to BFS

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
    # print("Block: ", block.BlkID, " broadcasted by node: ", node.ID, " at time: ", time)
    node.block_queue[block.BlkID] = time

    timenew = {}

    for neighbour in node.neighbours:
        if block.BlkID not in neighbour.block_queue.keys():
            delay = prop_delay(node, neighbour, block)
            # print("Delay: ", delay, " from node: ", node.ID, " to node: ", neighbour.ID)
            timenew[neighbour] = time + delay
            neighbour.block_queue[block.BlkID] = time
            newledger = neighbour.ledger.copy()
            for txn in block.data:
                if txn.sender is not None:
                    newledger[txn.sender]-=txn.amount
                    if(newledger[txn.sender]<0):
                        return
                newledger[txn.receiver]+=txn.amount
            neighbour.ledger = newledger
            neighbour.update(block, timenew)
    
    for neighbour in node.neighbours:
        if(neighbour in timenew):
            broadcast_block(block, neighbour, timenew[neighbour])
    return