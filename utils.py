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

def write_to_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data)

def read_from_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def get_random_number():
    return np.random.randint(0, 100)

