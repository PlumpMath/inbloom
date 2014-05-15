# -*- coding: utf-8 -*-
"""
Created on Wed May 14 19:34:53 2014

@author: a
"""
import hashlib
import string
from random import choice 
import pickle

k = 3
array_size = 100
test_string_length = 5

bloom = [0 for i in range(array_size)]

x='x'
y='y'
z='z'
w='w'

inset = (x, y, z)
outset = (w)

def get_hash(e):
    hashes = []
    for algorithm in hashlib.algorithms[:k]:
        m = hashlib.new(algorithm)
        m.update(e)
        mg = m.digest()
        hashes.append(sum([int(ord(j)) for j in mg]) % array_size)
    return hashes

def add_to_set(e):
    for i in get_hash(e):
        bloom[i]=1

def query(e):    
    for i in get_hash(e):
        if bloom[i]==0:
            return False
    return True

for i in inset:
    add_to_set(i)
    assert query(i) == True, "Element %r expected in set, not found"%i

assert query(w) == False, "Elemet w should not have been in the set"

"""
Find false positives with x,y,z characters as members and a million 5 character strings as tests
Initial tests found 17 false positives in a 100 length array using all 6 hashlib hash algorithms
"""

sample_space = string.lowercase+string.uppercase+string.digits

t = 0
false_positives = 0
false_positive_list = []
while t < 1000000:
    print "Progress: %r"% t
    test_string_length = 5
    test_string = ""
    for l in range(test_string_length):
        test_string += choice(sample_space)
    if query(test_string):
        false_positives += 1
        false_positive_list.append(test_string)
    t+=1
        
print false_positives
print false_positive_list
# 17/100,000
# ['0chc3', '7UFb0', 'rJbF6', 'aLeU7', 'aS7qP', 'tT2Op', 'sgNA0', 'BakAi', 'ni3b1', 'QMgQf', 'AtPP7', '4h9Rk', '1r1gm', 'kmC8N', '4qT6e', '2TE7r', '87jys']

raw_input("Press Enter to Continue")

"""
Load the Daily Mail words list and add them to the set.
Need to experiment with different values for k, array_size, number of words and
what type of test measurement.
"""
f=open('femail_words.list')
femail_words = pickle.load(f)
for i in femail_words[:1000]:
    add_to_set(i)
print query("asdghasgdhja") # Should be False
