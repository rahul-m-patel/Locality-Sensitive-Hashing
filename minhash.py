import numpy as np
from operator import itemgetter
import random as rnd

def get_hash_functions(size,max):
    hash_pair = []
    i = 0
    while(i<size):
        a = rnd.randint(1,max-1) # hash function = (ax + b) % c where a,b are random integers
        b = rnd.randint(1,max-1) # hash function = (ax + b) % c where a,b are random integers
        hash_pair.append([a,b])
        i += 1
    return hash_pair


def make_shingles(doc,shingles,k,docid):
    doc = doc.lower()
    # removing spaces between words
    tokens = doc.split(' ')
    doc = ''.join(tokens)
    # making shingles
    for i in range(len(doc)):
        shingle = doc[i:i+k:1] # slicing 'k' characters
        if len(shingle) == k and shingle not in shingles:
            shingles[shingle] = [docid] # list of documents which contain the shingle
        elif len(shingle) == k and shingle in shingles:
            postinglist = shingles[shingle]
            if docid not in postinglist:
                postinglist.append(docid)
    return shingles

def make_matrix(shingles,numColumns):
    index_matrix = {}
    index = 0
    # indexing the shingles
    for shingle in shingles:
        index_matrix[shingle] = index
        index += 1
    # making shingle document matrix
    matrix = np.zeros(len(shingles),numColumns)
    for shingle in shingles:
        postinglist = shingles[shingle]
        for docid in postinglist:
            matrix[index_matrix[shingle]][docid] = 1
    return matrix

def make_signature_matrix(matrix,size,numOfShingles):
    hashFuncs = get_hash_functions(size,numOfShingles)
    c = numOfShingles # hash function = (ax + b) % c where c is a prime number slightly larger than number of shingles
    while not c.isPrime():
        c += 1
    
    
print("hello")