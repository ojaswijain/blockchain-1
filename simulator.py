# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 12:03:13 2023

@author: ojaswi

Building a discrete event simulator for a P2P cryptocurrency network
Event queue class
"""

import heapq

class Event:
    def __init__(self, time, src, event_type, data):
        self.time = time
        self.src = src
        self.type = event_type
        self.data = data

    def __lt__(self, other):
        return self.time < other.time

class EventQueue:
    def __init__(self):
        self.queue = []

    def push(self, event):
        heapq.heappush(self.queue, event)

    def pop(self):
        return heapq.heappop(self.queue)

    def empty(self):
        return len(self.queue) == 0

    def __len__(self):
        return len(self.queue)

    def __repr__(self):
        return str(self.queue)

