from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords
import string
import math
import numpy as np
import matplotlib.pyplot as plt
import os
from os.path import join, isfile, splitext
import pandas as pd
from scipy.stats import rankdata
from ggplot import *

def allPuncChar(token):
    
    for c in token:
        
        if c not in string.punctuation:
            return False
        
    return True

def clean(words, customStopWordsList = None):
    ################
    # cleanup
    ################

    # to lower case
    words = [w.lower() for w in words]


    # remove stop words

    # step 1: custom list
  
    if customStopWordsList is not None:
        words = [w for w in words if w not in customStopWordsList]


    # step 2: built in list
    builtinList = set(stopwords.words('english')) # convert from list to set for fast lookup
    words = [w for w in words if w not in builtinList]

    # remove punctuations
    words = [w for w in words if not allPuncChar(w)]


    # remove numbers
    words = [w for w in words if not w.isnumeric()]
    
    return words

root = '/N/u/klosteda/Carbonate/Text-Analysis/data/StarTrekNextGenClean'

dataHome = 'season1'

# load custom stop words list
filepath = "/N/u/klosteda/Carbonate/Text-Analysis/data/earlyModernStopword.txt"

with open(filepath) as f:
     lines = f.read().splitlines()

customStopWordsList = set([l.strip() for l in lines]) # convert from list to set for fast lookup

# loop over text files
filenames = [f for f in os.listdir(os.path.join(root, dataHome)) if isfile(os.path.join(root, dataHome, f))]

filenames = sorted(filenames, key = lambda x: str(splitext(x)[0]))

docs = []

for filename in filenames:

    doc = PlaintextCorpusReader(join(root, dataHome), filename, encoding = 'ISO-8859-1')

    # get tokens
    words = doc.words()

    words = clean(words, customStopWordsList)
    
    docs.append(words)
    
# calculate frequency

interestedWords = ['yar', 'troi', 'crusher']

freqDict = {}

for w in interestedWords:
    
    freqDict[w] = np.zeros(len(docs)).tolist()
    
for idx, doc in enumerate(docs):
    
    for token in doc:
        
        if token in freqDict:
            freqDict[token][idx] += 1
                    


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


df = composeDataframe(freqDict)

seqLabel = []
seqNum = df["SeqNum"]

for i in seqNum:
    seqLabel.append(filenames[i - 1])
    
df["SeqLabel"] = seqLabel
  
  
p = ggplot(df, aes(x = 'SeqNum', ymin = 'ymin', ymax = 'ymax', y = 'Freq', group = 'Term', fill = 'Term')) +\
    geom_ribbon() + \
    theme(axis_text_x = element_text(angle = 45, hjust = 1)) + \
    scale_fill_brewer(type = 'qual', palette = 'Dark2') + \
    xlab(element_text(text = "Episodes", size = 16, vjust = -0.02)) + \
    ylab(element_text(text = "Frequency", size = 16)) + \
    scale_x_discrete(breaks = list(range(1, len(docs) + 1))) + \
    ggtitle(element_text(text = "Streamgraph of 3 words across Star Trek: Next Generation, Season 1", size = 16))
p.make()
plt.savefig("/N/u/klosteda/Carbonate/Text-Analysis/Output/streamgraphStarTrek277Py.png", width = 14, height = 8, dpi = 800)

plt.show()

