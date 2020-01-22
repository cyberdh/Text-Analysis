# NOTE: This chunk of code is only for use with Research Desktop. You will get an error if you try to run this code on your personal device!!

import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages for notebook 

#from nltk.corpus import PlaintextCorpusReader
#from nltk.corpus import stopwords
from nltk import word_tokenize
import string
import re
import glob
import math
import numpy as np
import pandas as pd
from scipy.stats import rankdata
import plotly as py
import plotly.express as px
import zipfile


# Set needed variables

fileType = ".json"
singleDoc = True
textColIndex = "text"
encoding = "utf-8"
tweetFile = "iranTweets" + fileType
numTweetsPerChunk = 1000
interestedWords = ["war", "trump", "america"]
freqDict = {}


# File paths
homePath = os.environ['HOME']
dataHome = os.path.join(homePath, "Text-Analysis-master", "data")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")
if fileType == ".csv":
    dataRoot = os.path.join(dataHome, "twitter", "CSV", "Iran")
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

# Read in data
def readTweets(filepath, textColIndex, encoding = encoding):
    if fileType == ".csv":
        tweet = pd.read_csv(filepath, index_col=None, header =0, encoding = encoding, lineterminator='\n')
    else:
        tweet = pd.read_json(filepath, encoding = encoding)
    
    content = tweet[textColIndex].tolist()
    
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
    
    blocks = ''.join(map(str, c))
    
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

#Variables
outputFile = "areaStackTwitter.html"
colorScheme = px.colors.qualitative.Set1
xlabel = "Chunk"
ylabel = "Frequency"
mainTitle = "Comparison of selected words in Tweets containing #Iran from 01/02/2020-01/04/2020"
yRange = [0, max(df["Freq"]*len(interestedWords))]
angle = 45

# Plot
if singleDoc is True:
    fig = px.area(df, x="SeqNum", y="Freq", color = "Term", color_discrete_sequence=colorScheme, line_group = "Term", 
                  labels = {"SeqNum":xlabel,"Freq":ylabel, "Term":""}, title=mainTitle, category_orders={"Term":interestedWords})
    fig.update_layout(title={'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor':'top'},
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 0,
        dtick = 1))
    fig.update_yaxes(range=yRange)
    fig.update_xaxes(tickangle=angle)
else:
    fig = px.area(df, x="SeqNum", y="Freq", color = "Term", color_discrete_sequence=colorScheme, line_group = "Term", 
                  labels = {"SeqNum":xlabel,"Freq":ylabel, "Term":""}, title=mainTitle, category_orders={"Term":interestedWords})
    fig.update_layout(title={'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor':'top'})
    fig.update_yaxes(range=yRange)
    fig.update_xaxes(tickangle=angle)
    
py.offline.plot(fig, filename=os.path.join(dataResults, outputFile))
fig.show()
