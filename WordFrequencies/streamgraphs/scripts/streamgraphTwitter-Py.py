# NOTE: This chunk of code is only for use with Research Desktop. You will get an error if you try to run this code on your personal device!!

import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages for notebook 

from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk import word_tokenize
import string
import re
import os
import csv
import json
import glob
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import rankdata
from ggplot import *
import zipfile


# Set needed variables

fileType = ".json"
singleDoc = False
interestedWords = ['gop', 'blame', 'trump']
freqDict = {}

#print(" ".join(stopwords.fileids()))


# File paths

homePath = os.environ['HOME']
dataHome = os.path.join(homePath, "Text-Analysis-master", "data")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")
if fileType == ".csv":
    dataRoot = os.path.join(dataHome, "twitter", "CSV", "parkland")
else:
    dataRoot = os.path.join(dataHome, "twitter", "JSON")


# Unzip files

direct = dataRoot
allZipFiles = glob.glob(os.path.join(dataRoot,"*.zip"))
for item in allZipFiles:
    fileName = os.path.splitext(direct)[0]
    zipRef = zipfile.ZipFile(item, "r")
    zipRef.extractall(fileName)
    zipRef.close()
    os.remove(item)


# Functions

# Read a .csv file

if fileType == ".csv":
    def readTweets(filepath, textColIndex, encoding = 'utf-8'):

        with open(filepath, encoding = encoding) as f:

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
            data = []
            for line in jsonData:
                data.append(json.loads(line))
        jData = pd.DataFrame(data)
        jData['created_at']=pd.to_datetime(jData.created_at)
        jData = jData.sort_values(by='created_at')
        content = jData[textColIndex].tolist()

        return content[1 : ]


# Text Cleaning

def clean(text):
    
    text = text.strip().lower()
    
    tweets = re.sub(r"http\S+", "", text)
    
    tokens = re.split(r'\W+', tweets )
    
    # remove empty string
    tokens = [t for t in tokens if t]
        
    # remove punctuation
    puncts = list(string.punctuation)
    puncts.append('--')

    tokens = [t for t in tokens if t not in puncts]

    return tokens


# Read in the tweets
# Variables
tweetFile = 'parkland' + fileType
textColIndex = 'text'
encoding = 'ISO-8859-1'
numTweetsPerChunk = 1000

# If...else statement

if singleDoc is True:
    
    filepath = os.path.join(dataRoot, tweetFile)

    tweets = readTweets(filepath, textColIndex, encoding)

    print('Read {} tweets'.format(len(tweets)))

    numberChunks = int(math.ceil(len(tweets) / numTweetsPerChunk))

    print('Tweets per chunk: {}, # chunks is {}'.format(numTweetsPerChunk, numberChunks))

    chunks = []

    for i in range(numberChunks - 1):

        chunks.append(tweets[i * numTweetsPerChunk : (i + 1) * numTweetsPerChunk])

    chunks.append(tweets[(i + 1) * numTweetsPerChunk : ])
else:
    tweets = []
    for root, subdirs, files in os.walk(dataRoot):
        
        for filename in files:
            
            # skip hidden file
            if filename.startswith('.'):
                continue
            
            dataFilepath = os.path.join(dataRoot, filename)
            
            content = readTweets(dataFilepath, textColIndex, encoding)
            tweets.extend(content)
            
            
            print('Read {} tweets'.format(len(tweets)))

            numberChunks = int(math.ceil(len(tweets) / numTweetsPerChunk))

            print('Tweets per chunk: {}, # chunks is {}'.format(numTweetsPerChunk, numberChunks))

            chunks = []

            for i in range(numberChunks - 1):

                chunks.append(tweets[i * numTweetsPerChunk : (i + 1) * numTweetsPerChunk])

            chunks.append(tweets[(i + 1) * numTweetsPerChunk : ])


# Clean chunks

tokenBlocks = []

for c in chunks:
    
    blocks = ''.join(c)
    
    words = word_tokenize(blocks)
    
    words = clean(str(words))
    tokenBlocks.append(words)


# Count words in each chunk

# calculate frequency
for w in interestedWords:
    
    freqDict[w] = np.zeros(len(tokenBlocks)).tolist()
    
for idx, block in enumerate(tokenBlocks):
    
    for token in block:
        
        if token in freqDict:
            freqDict[token][idx] += 1


# Emulate R's stat_steamgraph in 'ggTimeSeries' package

def composeDataframe(freqDict, debug = False):

    if debug:
        df = pd.DataFrame(data = freqDict)
        print(df)
        print('\n' * 3)


    wordCol = []
    freqCol = []
    seqNum = []
    
    for word in freqDict:
        wordCol.extend([word] * len(freqDict[word]))
        freqCol.extend(freqDict[word])
        seqNum.extend(list(range(1, len(freqDict[word]) + 1)))

    dataDict = {"Term" : wordCol, "Freq" : freqCol, 'SeqNum' : seqNum}

    df = pd.DataFrame(data = dataDict)

    if debug:
        print(df)
        print('\n' * 3)

    rankdf = df.groupby(["Term"], as_index = False).agg({"Freq" : "std"}).rename(columns = {"Freq" : "Std"})

    if debug:
        print(df)
        print('\n' * 3)

    rankdf["StdRank"] = rankdata(rankdf["Std"], method = 'ordinal')

    if debug:
        print(rankdf)
        print('\n' * 3)

    for idx, row in rankdf.iterrows():

        if row["StdRank"] % 2 == 0:
            rankdf.at[idx, "StdRank"] = -row["StdRank"]


    if debug:
        print(rankdf)
        print('\n' * 3)

    df = df.merge(rankdf, on = 'Term')

    if debug:
        print(df)
        print('\n' * 3)

    df = df.sort_values(by = ['SeqNum', 'StdRank'])

    if debug:
        print(df)
        print('\n' * 3)

    def f(x):

        x["cumsum"] = x["Freq"].cumsum()
        x["ymax"] = x["Freq"].cumsum() - x["Freq"].sum() / 2
        x["ymin"] = x["ymax"] - x["Freq"]

        return x


    df = df.groupby(["SeqNum"], as_index = False).apply(f)

    if debug:
        print(df)
        print('\n' * 3)
        
    return df


# Now we apply the `composeDataframe` function from above

df = composeDataframe(freqDict)


# Plot the Streamgraph

# Variables
streamTwitterOutput = "streamgraphTwitter.svg"
width = 14
height = 8
dpi = 300
color = 'Dark2'
fontSz = 16
angle = 45
hjust = 1
vjust = -0.02
xlabel = "Tweets in chunks of 1000"
title = "Streamgraph of 3 words in tweets containing #governmentshutdown"

# Plot
p = ggplot(df, aes(x = 'SeqNum', ymin = 'ymin', ymax = 'ymax', y = 'Freq', group = 'Term', fill = 'Term')) +    geom_ribbon() +     theme(axis_text_x = element_text(angle = angle, hjust = hjust)) +     scale_fill_brewer(type = 'qual', palette = color) +     xlab(element_text(text = xlabel, size = fontSz, vjust = vjust)) +     ylab(element_text(text = "Frequency", size = fontSz)) +     scale_x_continuous(breaks = list(range(1, len(tokenBlocks) + 1))) +     ggtitle(element_text(text = title, size = fontSz))
p.make()
plt.savefig(os.path.join(dataResults,streamTwitterOutput), width = width, height = height, dpi = dpi)

plt.show()
