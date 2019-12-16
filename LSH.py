import numpy as np
from operator import itemgetter
import random as rnd

len_buckets = 11 # any prime number

def normalize(array):
    denominator = 0
    for row in range(0,array.shape[0]):
        denominator = denominator + array[row]**2
    denominator = denominator**0.5
    print(denominator)
    for row in range(0,array.shape[0]):
        array[row] = array[row] / denominator
    return array

def euclidean_distance(x,y,r=2.0):
    try:
        return sum(((x[i] - y[i]) ** r) for i in range(0,len(x))) ** (1.0/r)
    
    except (ValueError,ZeroDivisionError):
        print('Please, enter only even values for "r > 0".')
    except IndexError:
        print('Please, the sets must have the same size.')

def cosine_distance(x,y):
    #x = normalize(x)
    #y = normalize(y)
    prodAB = sum([x[i]*y[i] for i in range(0,len(x))])
    # zeros = [0 for i in range(0,len(x))]
    # A = euclidean_distance(x,zeros)
    # B = euclidean_distance(y,zeros)
    normX = sum([x[i]*x[i] for i in range(0,len(x))]) ** 0.5
    normY = sum([y[i]*y[i] for i in range(0,len(y))]) ** 0.5
    return prodAB / (normX * normY)
    #return prodAB

def jaccard_similarity(x,y):
    intersection = 0
    union = 0
    for i in range(0,len(x)):
        if(x[i] == 1 and y[i] == 1):
            intersection = intersection + 1
            union = union + 1
        elif(x[i] == 1 or y[i] == 1):
            union = union + 1
    return intersection/union

def isPrime(num):
    i = 2
    while(i < int(num**0.5)+1):
        if (num % i == 0):
            return False
        i += 1
    return True

def initialize_array_bucket(bands):
    global len_buckets
    array_buckets = []
    for band in range(0,bands):
        array_buckets.append([[] for i in range(0,len_buckets)])
    return array_buckets

def get_hash_functions(size,max):
    hash_pair = []
    i = 0
    while(i<size):
        # a = rnd.randint(1,1000)
        # b = rnd.randint(1,1000)
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
    matrix = np.zeros((len(shingles),numColumns))
    for shingle in shingles:
        postinglist = shingles[shingle]
        for docid in postinglist:
            #id = postinglist[docid]
            #print(docid)
            matrix[index_matrix[shingle]][docid-1] = 1
    return matrix,index_matrix

def make_signature_matrix(matrix,size,shingles,numOfDocs,index_matrix):
    hashFuncs = get_hash_functions(size,len(shingles))
    signature_matrix = np.ones((size,numOfDocs)) * np.inf
    c = len(shingles) # hash function = (ax + b) % c where c is a prime number slightly larger than number of shingles
    permutation = np.zeros((len(shingles),1))
    while not isPrime(c):
        c += 1
    # c = 53
    i = 0
    for hash in hashFuncs:
        a = hash[0]
        b = hash[1]
        for shingle in index_matrix:
            x = index_matrix[shingle]
            hashed_value = (a*x + b) % c
            permutation[x][0] = hashed_value
        for shingle in shingles:
            row = index_matrix[shingle]
            docids = shingles[shingle]
            for id in docids:
                if(matrix[row][id-1] == 1):
                    signature_matrix[i][id-1] = min(signature_matrix[i][id-1],permutation[row][0])
        i += 1
    return signature_matrix
        
def LSH(bands,rows,threshold,signature_matrix,shingle_document_matrix):
    bucket_array = initialize_array_bucket(bands)
    candidates = {}
    cosine_candidates = {}
    jaccard_candidates = {}
    euclidean_candidates = {}
    i = 0
    for b in range(0,bands):
        buckets = bucket_array[b]
        band = signature_matrix[i:i+rows,:]
        for column in range(0,band.shape[1]):
            hashed_value = int(sum(band[:,column]) % len_buckets)
            buckets[hashed_value].append(column)
        i += rows

        for item in buckets:
            if len(item) > 1:
                print(item)
            for i in range(0,len(item)):
                for j in range(i+1,len(item)):
                    pair = (item[i],item[j])
                    #pair = (item[0], item[1])
                    if pair not in candidates:
                        # A = signature_matrix[:,item[i]]
                        # B = signature_matrix[:,item[j]]
                        A = shingle_document_matrix[:,item[i]]
                        B = shingle_document_matrix[:,item[j]]
                        cosine_similarity = cosine_distance(A,B)
                        jaccard_coeff = jaccard_similarity(A,B)
                        if cosine_similarity > threshold:
                            cosine_candidates[pair] = cosine_similarity
                            candidates[pair] = cosine_similarity
                        if jaccard_coeff >= threshold:
                            jaccard_candidates[pair] = jaccard_coeff
                        #euclidean_sim = euclidean_distance(A,B,2)
                        # if similarity >= threshold:
                        #     candidates[pair] = similarity

        similar_documents_cosine = sorted(cosine_candidates.items(), key = itemgetter(1), reverse = True)
        similar_documents_jaccard = sorted(jaccard_candidates.items(), key = itemgetter(1), reverse = True) 
        # similar_documents = sorted(candidates.items(), key = itemgetter(1), reverse = True) 
        return candidates, similar_documents_cosine,similar_documents_jaccard               
    
docid = 0
documents = {}
document_content = ""

with open("testfile.txt","r",encoding="utf-8") as dataSet:
    for i, line in enumerate(dataSet):
        if(line.strip() == "NEW ARTICLE"):
            if(not (docid == 0)):
                documents[docid] = document_content
                document_content = ""
            docid += 1
        else:
            document_content = document_content + line.strip()
    documents[docid] = document_content

shingles = {}

for docid in documents:
    shingles = make_shingles(documents[docid],shingles,6,docid) #k value generally taken between 8-10


#print(shingles)

numberOfDocuments = len(documents)
shingle_index = {}
shingle_document_matrix = np.zeros((len(shingles),numberOfDocuments))

shingle_document_matrix,shingle_index = make_matrix(shingles,numberOfDocuments)

documentSignature_matrix = np.zeros((200,numberOfDocuments))
documentSignature_matrix = make_signature_matrix(shingle_document_matrix,200,shingles,numberOfDocuments,shingle_index)

candidatePairs = {}
similar_docs = {}

candidatePairs,similar_docs_cosine,similar_docs_jaccard = LSH(50,4,0.5,documentSignature_matrix,shingle_document_matrix)

#print(candidatePairs)

#print(similar_docs)

print("cosine similar docs ::")
for pair in similar_docs_cosine:
   print(pair)

print("jaccard similar docs ::")
for pair in similar_docs_jaccard:
   print(pair)