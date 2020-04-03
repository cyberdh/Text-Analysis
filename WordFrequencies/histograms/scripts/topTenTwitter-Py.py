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
import plotly as py
import plotly.express as px
import math
import re
import pandas as pd
import glob
import zipfile


# Set needed variables

fileType = ".json"
singleDoc = True
nltkStop = True
customStop = True
stopLang = stopwords.fileids()
encoding = "utf-8"
stopWords = []


# File paths

homePath = os.environ['HOME']
dataHome = os.path.join(homePath, "Text-Analysis-master", "data")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")
if fileType == ".csv":
    dataRoot = os.path.join(dataHome, "twitter", "CSV")
else:
    dataRoot = os.path.join(dataHome, "twitter", "JSON")


# Stopwords

# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))
    
    stopWords.extend(["coronavirus", "com", "pic", "twitter"])


# Add own stopword list

if customStop is True:
    stopWordsFilepath = os.path.join(dataHome, "twitterStopword.txt")

    with open(stopWordsFilepath, "r",encoding = encoding) as stopfile:
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


# Read in data

def readTweets(filepath, textColIndex, encoding = encoding):
    if fileType == ".csv":
        tweet = pd.read_csv(filepath, index_col=None, header =0, encoding = encoding, lineterminator='\n')
    else:
        tweet = pd.read_json(filepath, encoding = encoding, lines = True)
    
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

def plotTopTen(sortedFreq, title, imgFilepath):
    
    topn = n
    
    df = pd.DataFrame(sortedFreq, columns = ["Words", "Count"])
    df["Pct"] = ((df["Count"]/df["Count"].sum())*100).round(3)
    df["Pct"] = df["Pct"].astype(str) + "%"
    dfPct = df[0 : topn]
    
    high = max(df["Count"])
    low = 0
    
    fig = px.bar(dfPct, x = "Words", y = "Count", hover_data=[dfPct["Pct"]],text = "Count", color = "Words", 
                 title = title, color_discrete_sequence=colors,
                labels = {"Words":Xlabel,"Count":Ylabel,"Pct":Zlabel})
    fig.update_layout(title={'y':0.90, 'x':0.5, 'xanchor': 'center', 'yanchor':'top'}, 
                      font={"color": labCol}, width = wide, height = tall, showlegend=False)
    fig.update_xaxes(tickangle = angle)
    fig.update_yaxes(range = [low,math.ceil(high + 0.1 * (high - low))])
    
    py.offline.plot(fig, filename=imgFilepath, auto_open = False)
    fig.show()


# Pull from a single file

def getTokensFromSingleText(dataFilepath, textColIndex, encoding):
    
    content = readTweets(dataFilepath, textColIndex, encoding)
    
    text = '\n'.join(map(str, content))

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
            text = '\n'.join(map(str, content))
            tokens.extend(textClean(text))
                
            print('Finished tokenizing text {}\n'.format(dataFilepath))
            
    return tokens


# Plot Top Ten
# Variables
n = 10
textColIndex = "text"
singleDocName = 'coronaVirus01-21Jan2020' + fileType
outputFile = "topTenTwitter"
fmt = '.html'
Xlabel = "Word"
Ylabel = "Count"
Zlabel = "Percent"
wide = 750
tall = 550
angle = -45
title = 'Top 10 Words, #Coronavirus<br>January 1-22, 2020'
colors = px.colors.qualitative.Dark24
labCol = 'crimson'

if singleDoc is True:
    # Use case one, analyze top 10 most frequent words from a single text

    dataFilepath = os.path.join(dataRoot, singleDocName)

    # get tokens
    tokens = getTokensFromSingleText(dataFilepath, textColIndex, encoding)

    # get frequency
    freq = getFreq(tokens)

    imgFilepath = os.path.join(dataResults, outputFile + fmt)

    plotTopTen(freq, title, imgFilepath)
else:
    # Use case two, analyze top 10 most frequent words from a corpus root

    tokens = getTokensFromScan(dataRoot, textColIndex, encoding)

    # get frequency
    freq = getFreq(tokens)

    imgFilepath = os.path.join(dataResults, outputFile + fmt)

    plotTopTen(freq, title, imgFilepath)

