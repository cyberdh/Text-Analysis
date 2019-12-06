# NOTE: This csection is only for use with Research Desktop. You will get an error if you try to run this code on your personal device!!

import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages for notebook 

from nltk.corpus import stopwords
import string
from collections import defaultdict
import operator
import math
import matplotlib.pyplot as plt
import numpy as np
import re
import csv
import json
import pandas as pd
import glob
import zipfile


# Set needed variables

fileType = ".csv"
singleDoc = False
nltkStop = True
customStop = False
stopLang = "english"
stopWords = []

#print(" ".join(stopwords.fileids()))


# File paths

homePath = os.environ['HOME']
dataHome = os.path.join(homePath, "Text-Analysis-master", "data")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")
if fileType == ".csv":
    dataRoot = os.path.join(dataHome, "twitter", "CSV", "parkland")
else:
    dataRoot = os.path.join(dataHome, "twitter", "JSON")


# Stopwords

# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))
    
    stopWords.extend(['amp','rt', 'xo_karmin_ox', 'neveragain', 'ð', 'â', 'ï', 'emma4change', 'nra', 'parkland'])


# Add own stopword list

if customStop is True:
    stopWordsFilepath = os.path.join(dataHome, "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = 'utf-8') as stopfile:
        stopWordsCustom = [x.strip() for x in stopfile.readlines()]

    stopWords.extend(stopWordsCustom)


# Functions

def textClean(text):
    
    text = text.strip().lower()
    
    tweets = re.sub(r"http\S+", "", text)
    
    tokens = re.split(r'\W+', tweets )
    
    # remove empty string
    tokens = [t for t in tokens if t]
    
    # remove digits
    tokens = [t for t in tokens if not t.isdigit()]
    
    # built-in stop words list
    tokens = [t for t in tokens if t not in stopWords]
        
    # remove punctuation
    puncts = list(string.punctuation)
    puncts.append('--')

    tokens = [t for t in tokens if t not in puncts]

    return tokens


# Unzip files

direct = dataRoot
allZipFiles = glob.glob(os.path.join(dataRoot, "*.zip"))
for item in allZipFiles:
    fileName = os.path.splitext(direct)[0]
    zipRef = zipfile.ZipFile(item, "r")
    zipRef.extractall(fileName)
    zipRef.close()
    os.remove(item)


# Read a .csv file

if fileType == ".csv":
    def readTweets(filepath, textColIndex, encoding = 'utf-8', errors = 'ignore'):

        with open(filepath, encoding = encoding, errors = errors) as f:

            reader = csv.reader(f, delimiter = ',', quotechar = '"')

            content = []
            for row in reader: 
                content.append(row[textColIndex])

            # skip header
            return content[1 : ]


# Read a .json file

if fileType == ".json":
    def readTweets(filepath, textColIndex, encoding = 'utf-8', errors = 'ignore'):
        
        with open(filepath, encoding = encoding, errors = errors) as jsonData:
            tweets = []
            for line in jsonData:
                tweets.append(json.loads(line))
        tweet = pd.DataFrame(tweets)
        content = tweet[textColIndex].tolist()

        return content[1 : ]


# Frequency count

def getFreq(tokens):
    
    freq = defaultdict(int)

    for t in tokens:
        freq[t] += 1
    
    # sorted frequency in descending order
    return sorted(freq.items(), key = operator.itemgetter(1), reverse = True)


# Plot Graph Function

def plotTopTen(sortedFreq, title, imgFilepath, dpi):
    
    topn = n

    for t in sortedFreq[0 : topn]:
        
        print('{} : {}'.format(t[0], t[1]))
    
    topNWords = [w for w in sortedFreq[0 : topn]]

    x_pos = np.arange(len(topNWords))
    cnts = [w[1] for w in topNWords]

    plt.rcdefaults()

    plt.bar(x_pos, cnts, align = 'center', alpha = 0.5, color = color)
    

        
    plt.xticks(x_pos, [w[0] for w in topNWords])
    plt.xticks(rotation = angle)
        
    xlabel = plt.xlabel('Words')
    xlabel.set_color(labCol)
    ylabel = plt.ylabel('Frequency')
    ylabel.set_color(labCol)
    
    high = max(cnts)
    low = 0
    
    plt.ylim(low, math.ceil(high + 0.1 * (high - low)))
    
    for xpos, count in zip(x_pos, cnts):
    
        plt.text(x = xpos, y = count + 1, s = str(count), ha = 'center', va = 'bottom')

    plt.title(title)
 
    plt.savefig(imgFilepath, format = fmt, dpi = dpi, bbox_inches = 'tight')
    
    plt.show()


# Pull from a single file

def getTokensFromSingleText(dataFilepath, textColIndex, encoding):
    
    content = readTweets(dataFilepath, textColIndex, encoding)
    
    text = '\n'.join(content)

    return textClean(text)


# Pull from a directory

def getTokensFromScan(dataRoot, textColIndex, encoding):
   
    tokens = []
    
    for root, subdirs, files in os.walk(dataRoot):
        
        for filename in files:
            
            # skip hidden file
            if filename.startswith('.'):
                continue
            
            dataFilepath = os.path.join(root, filename)
            
            content = readTweets(dataFilepath, textColIndex, encoding)
            text = '\n'.join(content)
            tokens.extend(textClean(text))
                
            print('Finished tokenizing text {}\n'.format(dataFilepath))
            
    return tokens


# Plot Top Ten
# Variables
n = 10
textColIndex = 2
encoding = 'utf-8'
singleDocName = 'neverAgain' + fileType
outputFile = "topTenTwitter.svg"
fmt = 'svg'
dpi = 300
angle = 60
title = 'Top 10 Words, #neveragain, #parkland, #nra'
color = ['crimson','orange', 'yellow', 'green', 'blue','darkorchid', 'darkred', 'darkorange','gold', 'darkgreen']
labCol = 'crimson'

if singleDoc is True:
    # Use case one, analyze top 10 most frequent words from a single text

    dataFilepath = os.path.join(dataRoot, singleDocName)

    # get tokens
    tokens = getTokensFromSingleText(dataFilepath, textColIndex, encoding)

    # get frequency
    freq = getFreq(tokens)

    imgFilepath = os.path.join(dataResults, outputFile)

    plotTopTen(freq, title, imgFilepath, dpi)
else:
    # Use case two, analyze top 10 most frequent words from a corpus root

    tokens = getTokensFromScan(dataRoot, textColIndex, encoding)

    # get frequency
    freq = getFreq(tokens)

    imgFilepath = os.path.join(dataResults, outputFile)

    plotTopTen(freq, title, imgFilepath, dpi)
