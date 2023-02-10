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
    # node.txn_queue[txn.TxID] = time
    Q = []
    Q.push([node, time])
    visited = []
    visited.push(node)

    while(Q):
        popnode, popnodetime = Q.pop(0)
        for neighbour in popnode.neighbours:
            if(neighbour not in visited):
                newtime = popnodetime + prop_delay(popnode, neighbour, txn)
                Q.push([neighbour, newtime])
                visited.push(neighbour)
                neighbour.unused_txns.append(txn)
    return

def broadcast_block(block, node, time):
    """
    Broadcasts a block from a node
    """
    # print("Block: ", block.BlkID, " broadcasted by node: ", node.ID, " at time: ", time)
    Q = []
    Q.push([node, time])
    visited = []
    visited.push(node)

    while(Q):
        popnode, popnodetime = Q.pop(0)
        for neighbor in popnode.neighbours:
            if(neighbor not in visited):
                delay = prop_delay(popnode, neighbor, block)
                time_new = popnodetime + delay
                Q.push([neighbor, time_new])
                visited.push(neighbor)
                newledger = neighbor.ledger.copy()
                for txn in block.data:
                    if txn.sender is not None:
                        newledger[txn.sender]-=txn.amount
                        if(newledger[txn.sender]<0):
                            return
                    newledger[txn.receiver]+=txn.amount
                neighbor.ledger = newledger
                neighbor.update(block, time_new)

    return