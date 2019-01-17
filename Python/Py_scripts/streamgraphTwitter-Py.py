from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk import word_tokenize
import string
import re
import os
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import rankdata
from ggplot import *


"""
Check if a token has all ASCII characters
"""
def isAsciiToken(token):
    
    return all(ord(c) < 128 for c in token)


"""
Remove non-ascii tokens
"""
def removeNonAsciiToken(tokens):
    
    # remove non-ascii tokens
    tokens = [x for x in tokens if isAsciiToken(x)]
    
    return tokens


def readCSV(filepath, textColIndex, encoding = 'utf-8'):
    
    with open(filepath, encoding = encoding) as f:
        
        reader = csv.reader(f, delimiter = ',', quotechar = '"')
        
        content = []
        for row in reader: 
            content.append(row[textColIndex])
         
        # skip header
        return content[1 : ]
    
    
"""
Remove URLs
"""
def removeURL(tokens):
    
    p = re.compile(r'^https?://.*$')
    
    tokens = [t for t in tokens if re.match(p, t) is None]
    
    return tokens 


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
    
    # remove urls
    words = removeURL(words)
    
    # remove non ascii tokens
    words = removeNonAsciiToken(words)
        
    return words


root = '/N/u/klosteda/Carbonate/Text-Analysis/data/twitter/parkland'

tweetFile = 'neverAgain.csv'

filepath = os.path.join(root, tweetFile)

textColIndex = 2
encoding = 'ISO-8859-1'

tweets = readCSV(filepath, textColIndex, encoding)

print('Read {} tweets'.format(len(tweets)))

numTweetsPerBlock = 1000

numberBlocks = int(math.ceil(len(tweets) / numTweetsPerBlock))

print('Tweets per block: {}, # blocks is {}'.format(numTweetsPerBlock, numberBlocks))

blocks = []

for i in range(numberBlocks - 1):
    
    blocks.append(tweets[i * numTweetsPerBlock : (i + 1) * numTweetsPerBlock])
    
blocks.append(tweets[(i + 1) * numTweetsPerBlock : ])



# load custom stop words list
filepath = "/N/u/klosteda/Carbonate/Text-Analysis/data/earlyModernStopword.txt"

with open(filepath) as f:
    lines = f.read().splitlines()

lines = [l.strip() for l in lines]
lines.extend(['amp','rt', 'dont'])

customStopWordsList = set(lines) # convert from list to set for fast lookup

tokenBlocks = []

for b in blocks:
    
    text = ' '.join(b)
    
    tokens = word_tokenize(text)
    
    tokenBlocks.append(clean(tokens, customStopWordsList))
    


# calculate frequency

interestedWords = ['nra', 'gop', 'msdstrong']

freqDict = {}

for w in interestedWords:
    
    freqDict[w] = np.zeros(len(tokenBlocks)).tolist()
    
for idx, block in enumerate(tokenBlocks):
    
    for token in block:
        
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



p = ggplot(df, aes(x = 'SeqNum', ymin = 'ymin', ymax = 'ymax', y = 'Freq', group = 'Term', fill = 'Term')) +\
    geom_ribbon() + \
    theme(axis_text_x = element_text(angle = 45, hjust = 1)) + \
    scale_fill_brewer(type = 'qual', palette = 'Dark2') + \
    xlab(element_text(text = "Segments of 1000 Tweets", size = 16, vjust = -0.02)) + \
    ylab(element_text(text = "Frequency", size = 16)) + \
    scale_x_continuous(breaks = list(range(1, len(tokenBlocks) + 1))) + \
    ggtitle(element_text(text = "Streamgraph of 3 words in tweets containing #neveragain", size = 16))
p.make()
plt.savefig("/N/u/klosteda/Carbonate/Text-Analysis/Output/streamgraphNeverAgainPy.png", width = 14, height = 8, dpi = 800)

plt.show()

