import json
import os
import sys
import re

with open('scraped_articles.json') as data_file:
    dataFile = json.load(data_file)
    articles = dataFile['washingtonpost']['articles']
    for article in articles:
        #docID = article['DocID']
        title = article['title']
        title = title + "\n"
        writeString = article['text']
        #text = re.sub(r'Media playback.*?Media caption','',writeString)
        #data = re.sub(r'Image copyright.*?Image caption','',text)
        data = re.sub(r'Media playback.*?\n','',writeString)
        data1 = re.sub(r'Media caption.*?\n','',data)
        data2 = re.sub(r'Image copyright.*?\n','',data1)
        data3 = re.sub(r'Image caption.*?\n','',data2)
        #data2 = data1.replace('Media playback is unsupported on your device','').replace('Image caption','')
        fileobj = open(r"TextFile.txt","a",encoding="utf-8")
        fileobj.write("\n\n\nNEW ARTICLE\n\n\n")
        fileobj.write(title)
        fileobj.writelines(data3)
        fileobj.close()


    