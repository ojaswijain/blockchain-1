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

    if node.selfish == True or node.stubborn == True:
        if block.BlkID not in node.block_queue.keys():
            node.block_queue[block.BlkID]=time
            node.update(block, time)
            if block.malice == False:
                events = take_action(node, time)
        return events
    if block.BlkID not in node.block_queue.keys():
            # print("Block: ", block.BlkID, " broadcasted by node: ", node.ID, " at time: ", time)
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

def take_action(node, time):
    """
    Actions taken by selfish miners
    Action depends on the type of selfish miner, and the current lead
    """
    events = []
    delta_time = 1e-1
    if node.lead > 0:
        node.lead -= 1
        print("New lead: ", node.lead)
    if node.selfish == True:
        #If lead = 0
        if node.lead == 0:
            #If the node has a private chain, broadcast the block
            if node.pvtChain != []:
                block = node.pvtChain.pop(0)
                for neighbour in node.neighbours:
                    delay = prop_delay(node, neighbour, block)
                    time_new = time + delay
                    events.append(Event(time_new, neighbour, "block", block))
                node.last_block = block
                return events
            #If the node does not have a private chain, return nothing
            else:
                return events
        
        #If lead = 1
        elif node.lead == 1:
            #Broadcast all blocks in the private chain
            while node.pvtChain != []:
                block = node.pvtChain.pop(0)
                for neighbour in node.neighbours:
                    delay = prop_delay(node, neighbour, block)
                    time_new = time + delay
                    events.append(Event(time_new, neighbour, "block", block))
                    #Broadcast blocks with a slight delay to maintain the order in the chains
                    time += delta_time
            node.lead = 0
            return events

        #If lead > 1
        else:
            #Broadcast one block from the private chain
            block = node.pvtChain.pop(0)
            for neighbour in node.neighbours:
                delay = prop_delay(node, neighbour, block)
                time_new = time + delay
                events.append(Event(time_new, neighbour, "block", block))
            return events

    elif node.stubborn == True:
        if node.pvtChain != []:
                block = node.pvtChain.pop()
                for neighbour in node.neighbours:
                    delay = prop_delay(node, neighbour, block)
                    time_new = time + delay
                    events.append(Event(time_new, neighbour, "block", block))
                node.last_block = block
                return events   