# NOTE: This chunk of code is only for use with Research Desktop. You will get an error if you try to run this code on your personal device!!

import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages for notebook 

from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords
import string
import math
import numpy as np
import matplotlib.pyplot as plt
from os.path import join, isfile, splitext
import pandas as pd
from scipy.stats import rankdata
from ggplot import *


# File paths

homePath = os.environ['HOME']
dataHome = os.path.join(homePath, 'Text-Analysis-master', 'data', 'shakespeareFolger')
dataResults = os.path.join(homePath, 'Text-Analysis-master', 'Output')


# Set needed variables

singleDoc = False
nltkStop = True
customStop = True
stopLang = 'english'
stopWords = []
interestedWords = ['night', 'death', 'love']
freqDict = {}

#print(" ".join(stopwords.fileids()))


# Stopwords

# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))

    stopWords.extend(['would', 'said', 'says', 'also', 'good', 'lord', 'come'])


# Add own stopword list

if customStop is True:
    stopWordsFilepath = os.path.join(homePath, "Text-Analysis-master", "data", "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = 'utf-8') as stopfile:
        stopWordsCustom = [x.strip() for x in stopfile.readlines()]

    stopWords.extend(stopWordsCustom)


# Functions

# Text Cleaning

def allPuncChar(token):
    
    for c in token:
        
        if c not in string.punctuation:
            return False
        
    return True

def clean(words):
    ################
    # cleanup
    ################

    # to lower case
    words = [w.lower() for w in words]

    # step 2: built in list
    builtinList = set(stopWords) # convert from list to set for fast lookup
    words = [w for w in words if w not in builtinList]

    # remove punctuations
    words = [w for w in words if not allPuncChar(w)]


    # remove numbers
    words = [w for w in words if not w.isnumeric()]
    
    return words
    


# Read in the corpus

textFile = 'RomeoAndJuliet.txt'
chunkSize = 250

if singleDoc is True:

    doc = PlaintextCorpusReader(dataHome, textFile)

    # get tokens
    text = doc.words()

    text = clean(text)
    # chunking

    numberChunks = int(math.ceil(len(text) / chunkSize))

    words = []

    for i in range(numberChunks - 1):

        words.append(text[i * chunkSize : (i + 1) * chunkSize])

    words.append(text[(i + 1) * chunkSize : ])
else:
    # loop over text files
    filenames = [f for f in os.listdir(dataHome) if isfile(os.path.join(dataHome, f))]

    filenames = sorted(filenames, key = lambda x: str(splitext(x)[0]))

    words = []

    for filename in filenames:

        doc = PlaintextCorpusReader(dataHome, filename, encoding = 'ISO-8859-1')

        # get tokens
        text = doc.words()

        text = clean(text)

        words.append(text)


# Count words

# calculate frequency
for w in interestedWords:
    
    freqDict[w] = np.zeros(len(words)).tolist()
    
for idx, word in enumerate(words):
    
    for token in word:
        
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


# Now we apply the emulator data frame function from above

if singleDoc is True:
    df = composeDataframe(freqDict)
else:
    df = composeDataframe(freqDict)

    seqLabel = []
    seqNum = df["SeqNum"]

    for i in seqNum:
        seqLabel.append(filenames[i-1])

    df["SeqLabel"] = seqLabel
    
    dfU = df["SeqLabel"].unique()
    dfU = pd.DataFrame(dfU)
    dfU.index += 1
    print(dfU)


# Plot the Streamgraph

# Variables
streamOutput = "streamgraph.svg"
width = 14
height = 8
dpi = 300
color = 'Dark2'
fontSz = 16
angle = 45
hjust = 1
vjust = -0.02
xlabel = "Plays"
title = "Streamgraph of 3 words across Shakespeare"

# Plot
get_ipython().magic('matplotlib inline')
p = ggplot(df, aes(x = "SeqNum", ymin = 'ymin', ymax = 'ymax', y = 'Freq', group = 'Term', fill = 'Term')) +    geom_ribbon() +    theme(axis_text_x = element_text(angle=angle, hjust = hjust)) +    scale_fill_brewer(type = 'qual', palette = color) +    xlab(element_text(text = xlabel, size = fontSz, vjust = vjust)) +    ylab(element_text(text = "Frequency", size = fontSz)) +    scale_x_continuous(breaks = list(range(1, len(words) + 1))) +     ggtitle(element_text(text = title, size = fontSz))

    
p.make()
plt.savefig(os.path.join(dataResults, streamOutput), width = width, height = height, dpi = dpi)

plt.show()

if singleDoc is False:
    print(dfU)
