import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"

          
from nltk.corpus import stopwords
import string
from collections import defaultdict
import pandas as pd
import operator
import plotly as py
import plotly.express as px
import re
import math


homePath = os.environ['HOME']
dataHome = os.path.join(homePath, 'Text-Analysis-master', 'data', 'shakespeareFolger')
dataResults = os.path.join(homePath, 'Text-Analysis-master', 'Output')

singleDoc = True
nltkStop = True
customStop = True
stopLang = 'english'
encoding = "utf-8"
errors = "ignore"
stopWords = []

# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))

    stopWords.extend(['would', 'said', 'says', 'also', 'good', 'lord', 'come', 'let', 'say', 'speak', 'know', 'hamlet'])


if customStop is True:
    stopWordsFilepath = os.path.join(homePath, "Text-Analysis-master", "data", "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = encoding) as stopfile:
        stopWordsCustom = [x.strip() for x in stopfile.readlines()]

    stopWords.extend(stopWordsCustom)
    
def textClean(text):
    
    text = text.strip().lower()
    
    tokens = re.split(r'\W+', text)
    
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


    
"""
Get sorted frequency in descending order
"""
def getFreq(tokens):
    
    freq = defaultdict(int)

    for t in tokens:
        freq[t] += 1
    
    # sorted frequency in descending order
    return sorted(freq.items(), key = operator.itemgetter(1), reverse = True)

def plotTopTen(sortedFreq, title, imgFilepath):
    
    topn = n
    
    df = pd.DataFrame(sortedFreq[0 : topn], columns = ["Words", "Count"])
    
    high = max(df["Count"])
    low = 0
    
    fig = px.bar(df, x = "Words", y = "Count", text = "Count", color = "Words", 
                 title = title, color_discrete_sequence=colors,
                labels = {"Words":Xlabel,"Count":Ylabel})
    fig.update_layout(title={'y':0.90, 'x':0.5, 'xanchor': 'center', 'yanchor':'top'}, 
                      font={"color": labCol}, width = wide, height = tall, showlegend=False)
    fig.update_xaxes(tickangle = angle)
    fig.update_yaxes(range = [low,math.ceil(high + 0.1 * (high - low))])
    
    py.offline.plot(fig, filename=imgFilepath, auto_open = False)
    fig.show()
    
    
def getTokensFromSingleText(textFilepath):
    
    with open(textFilepath, "r", encoding = encoding, errors = errors) as f:
        text = f.read()

    return textClean(text)


def getTokensFromScan(corpusRoot):
    
    tokens = []
    
    for root, subdirs, files in os.walk(corpusRoot):
        
        for filename in files:
            
            # skip hidden file
            if filename.startswith('.'):
                continue
            
            textFilepath = os.path.join(root, filename)
            
            with open(textFilepath, "r", encoding = encoding, errors = errors) as f:
                text = f.read()
                tokens.extend(textClean(text))
                
                print('Finished tokenizing text {}\n'.format(textFilepath))
    
    return tokens

# Variables
n = 10
singleDocName = 'Hamlet.txt'
outputFile = "topTenPlainText"
fmt = '.html'
Xlabel = "Word"
Ylabel = "Count"
wide = 750
tall = 550
angle = -45
title = 'Top 10 Words, Hamlet'
colors = px.colors.qualitative.Dark24
labCol = "crimson"

if singleDoc is True:
    # Use case one, analyze top 10 most frequent words from a single text

    textFilepath = os.path.join(dataHome, singleDocName)

    # get tokens
    tokens = getTokensFromSingleText(textFilepath)

    # get frequency
    freq = getFreq(tokens)

    imgFilepath = os.path.join(dataResults, outputFile + fmt)

    plotTopTen(freq, title, imgFilepath)
else:
    # Use case two, analyze top 10 most frequent words from a corpus root

    tokens = getTokensFromScan(dataHome)

    # get frequency
    freq = getFreq(tokens)

    imgFilepath = os.path.join(dataResults, outputFile +fmt)

    plotTopTen(freq, title, imgFilepath)


