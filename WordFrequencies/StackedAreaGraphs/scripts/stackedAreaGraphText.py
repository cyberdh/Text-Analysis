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
from os.path import isfile, splitext
import pandas as pd
from scipy.stats import rankdata
import plotly as py
import plotly.express as px


# File paths

homePath = os.environ['HOME']
dataHome = os.path.join(homePath, 'Text-Analysis-master', 'data', 'shakespeareFolger')
dataResults = os.path.join(homePath, 'Text-Analysis-master', 'Output')


# Set needed variables

singleDoc = True
nltkStop = True
customStop = True
stopLang = 'english'
encoding = "utf-8"
textFile = 'Hamlet.txt'
chunkSize = 300
stopWords = []
interestedWords = ["love", "father", "mother"]
freqDict = {}


# Stopwords

# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))

    stopWords.extend(['would', 'said', 'says', 'also', 'good', 'lord', 'come'])


# Add own stopword list

if customStop is True:
    stopWordsFilepath = os.path.join(homePath, "Text-Analysis-master", "data", "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = encoding) as stopfile:
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
if singleDoc is True:

    doc = PlaintextCorpusReader(dataHome, textFile, encoding = encoding)

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

        doc = PlaintextCorpusReader(dataHome, filename, encoding = encoding)

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


# Plot the Stacked Area Graph
high = max(df["Freq"])*2
#Variables
outputFile = "areaStackHamlet.html"
colorScheme = px.colors.qualitative.Set1
if singleDoc == True:
    xlabel = "Chunk"
else:
    xlabel = "Document"
ylabel = "Frequency"
mainTitle = "Comparison of selected words in Shakespeare's Hamlet"
yRange = [0, high]
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
    fig = px.area(df, x="SeqLabel", y="Freq", color = "Term", color_discrete_sequence=colorScheme, line_group = "Term", 
                  labels = {"SeqLabel":xlabel,"Freq":ylabel, "Term":""}, title=mainTitle, category_orders={"Term":interestedWords})
    fig.update_layout(title={'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor':'top'})
    fig.update_yaxes(range=yRange)
    fig.update_xaxes(tickangle=angle)
    
py.offline.plot(fig, filename=os.path.join(dataResults, outputFile))
fig.show()
