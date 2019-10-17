import json
import sys
import re
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string

def makeTokens(text):
    # tokenize text
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]
    # remove punctuation from words
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    porter = PorterStemmer()
    stemmedwords = [porter.stem(w) for w in words]
    return stemmedwords

#datafile = open("TextFile.txt","r")
#text = datafile.read()
termfrequency = {}
inverted_index = {}
docid = 0
with open("TextFile.txt","r") as datafile:
    for i, line in enumerate(datafile):
        if(line.strip() == "NEW ARTICLE"):
            docid += 1
        else:
            keywords = makeTokens(line)
            for word in keywords:
                if word in termfrequency:
                    termfrequency[word] += 1
                else:
                    termfrequency[word] = 1
                if word in inverted_index:
                    posting_list = inverted_index[word]
                    if docid in posting_list:
                        posting_list[docid] += 1
                    else:
                        posting_list[docid] = 1
                else:
                    inverted_index[word] = {docid : 1}



# i = 0

# for word in inverted_index:
#     if(i>10):
#         break
#     i = i  + 1
#     postinglist = inverted_index[word]
#     print(word)
#     print(postinglist)
#     # for doc,val in postinglist:
#     #     print(str(doc) + ":" + str(val))
#     #break
    

#datafile.close()


# for word in keywords:
#     if word in termfrequency:
#         termfrequency[word] += 1
#     else:
#         termfrequency[word] = 1
#     if word in inverted_index:
#         something
#     else:
#         inverted_index[word] = {}




#writefile = open("termfrquency.txt","w")
#writefile.write(str(len(termfrequency)))

