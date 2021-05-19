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
import gensim
from gensim.models.phrases import Phrases, Phraser
from gensim.utils import simple_preprocess
import spacy
from scipy.stats import rankdata
import plotly as py
import plotly.express as px


# File paths

homePath = os.environ['HOME']
dataHome = os.path.join(homePath, 'Text-Analysis-master', 'data')
corpusRoot = os.path.join(dataHome, 'shakespeareFolger')
directRoot = os.path.join(dataHome, 'starTrek')
dataResults = os.path.join(homePath, 'Text-Analysis-master', 'Output')


# Set needed variables

corpusLevel = "lines"
nltkStop = True
customStop = True
spacyLem = True
stopLang = 'english'
lemLang = "en"
encoding = "utf-8"
errors = "ignore"
textFile = 'Hamlet.txt'
chunkSize = 300
stopWords = []
interestedWords = ["king", "hamlet", "mad", "death"]
freqDict = {}


# Stopwords

# NLTK Stop words
# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))

    stopWords.extend(['would', 'said', 'says', 'also'])


# Add own stopword list

if customStop is True:
    stopWordsFilepath = os.path.join(homePath, "Text-Analysis-master", "data", "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = encoding) as stopfile:
        stopWordsCustom = [x.strip() for x in stopfile.readlines()]

    stopWords.extend(stopWordsCustom)


# Functions

# Text Cleaning

def sentToWords(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations
    
# Variables
minCount = 5
tHold = 100

def get2gramPhrases(tokens):
    # Build the bigram and trigram models
    bigram = Phrases(tokens, min_count=minCount, threshold=tHold) # higher threshold fewer phrases.  

    # Removes model state from Phrases thereby reducing memory use.
    bigramMod = Phraser(bigram)
    
    return bigramMod

def get3gramPhrases(tokens):
    bigram = Phrases(tokens, min_count=minCount, threshold=tHold) # higher threshold fewer phrases.
    trigram = Phrases(bigram[tokens], threshold=tHold)
    
    trigramMod = Phraser(trigram)
    return trigramMod

# Define functions for stopwords, bigrams, trigrams and lemmatization
def removeStopwords(text):
    text = [w for w in text if w not in stopWords]
    return text
def makeBigrams(tokens):
    bigrams = get2gramPhrases(tokens)
    return [bigrams[doc] for doc in tokens]

def makeTrigrams(tokens):
    bigrams = get2gramPhrases(tokens)
    trigrams = get3gramPhrases(tokens)
    return [trigrams[bigrams[doc]] for doc in tokens]

# Form ngrams
def makeLemma(tokens):
    dataWordsNgrams = makeTrigrams(tokens)

    if spacyLem is True:
        def lemmatization(tokens):
            """https://spacy.io/api/annotation"""
            textsOut = []
            for sent in tokens:
                doc = nlp(" ".join(sent)) 
                textsOut.append([token.lemma_ for token in doc if token.lemma_ != '-PRON-'])
            return textsOut
        
        # Initialize spacy language model, eliminating the parser and ner components
        nlp = spacy.load(lemLang, disable=['parser', 'ner'])
    
        # Do lemmatization
       
        dataLemmatized = lemmatization(dataWordsNgrams)
       
        return dataLemmatized
    
    else:
        
        return dataWordsNgrams


# Read in the corpus
if corpusLevel == "lines":

    doc = PlaintextCorpusReader(corpusRoot, textFile, encoding = encoding)

    # get tokens
    docs = doc.words()

    tokens = list(sentToWords(docs))
    stop = removeStopwords(tokens)
    lemma = makeLemma(stop)
    text = [item for sublist in lemma for item in sublist]
    # chunking

    numberChunks = int(math.ceil(len(text) / chunkSize))

    words = []

    for i in range(numberChunks - 1):

        words.append(text[i * chunkSize : (i + 1) * chunkSize])

    words.append(text[(i + 1) * chunkSize : ])
    
elif corpusLevel == "files":
    # loop over text files
    filenames = [f for f in os.listdir(corpusRoot) if isfile(os.path.join(corpusRoot, f))]

    filenames = sorted(filenames, key = lambda x: str(splitext(x)[0]))

    words = []

    for filename in filenames:

        doc = PlaintextCorpusReader(corpusRoot, filename, encoding = encoding)

        # get tokens
        docs = doc.words()

        tokens = list(sentToWords(docs))
        stop = removeStopwords(tokens)
        lemma = makeLemma(stop)
        text = [item for sublist in lemma for item in sublist]

        words.append(text)
elif corpusLevel == "direct":
    paths = []
    txt = []
    text = []
    foldernames = []
    for folder in sorted(os.listdir(directRoot)):
        if not os.path.isdir(os.path.join(directRoot, folder)):
            continue
        for file in sorted(os.listdir(os.path.join(directRoot, folder))):
            paths.append(((directRoot, folder, file)))
    df = pd.DataFrame(paths, columns = ["Root", "Folder", "File"])
    df["Paths"] = df["Root"].astype(str) +"/" + df["Folder"].astype(str) + "/" + df["File"].astype(str)
    for path in df["Paths"]:
        if not path.endswith(".txt"):
            continue
        with open(path, "r", encoding = encoding, errors = errors) as f:
            doc = f.read().strip().split()
            txt.append(doc)
    
    df["Text"] = pd.Series(txt)
    df["Text"] = ["".join(map(str, l)) for l in df["Text"].astype(str)]
    d = {'Text':'merge'}
    dfText = df.groupby(['Folder'])["Text"].apply(lambda x: ' '.join(x)).reset_index()
    foldernames.extend(dfText['Folder'].tolist())
    
    text.extend(dfText["Text"].tolist())
    words = makeLemma(removeStopwords(list(sentToWords(text))))
else:
    print("No corpus has been read in because 'lines', 'files', or 'direct' was not assigned to the corpusLevel variable in the variables cell above. Please read the instructions to decide which setting is best for your corpus.")
    quit()
    


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

if corpusLevel == "lines":
    df = composeDataframe(freqDict)
elif corpusLevel == "files":
    df = composeDataframe(freqDict)

    seqLabel = []
    seqNum = df["SeqNum"]

    for i in seqNum:
        seqLabel.append(filenames[i-1])

    df["SeqLabel"] = seqLabel
    
    dfU = df["SeqLabel"].unique()
    dfU = pd.DataFrame(dfU)
    dfU.index += 1
    print(df)
elif corpusLevel == "direct":
    df = composeDataframe(freqDict)

    seqLabel = []
    seqNum = df["SeqNum"]

    for i in seqNum:
        seqLabel.append(foldernames[i-1])

    df["SeqLabel"] = seqLabel
    
    dfU = df["SeqLabel"].unique()
    dfU = pd.DataFrame(dfU)
    dfU.index += 1
    print(df)
else:
    None


# Plot the Stacked Area Graph
#Variables
outputFile = "areaStackHamlet.html"
colorScheme = px.colors.qualitative.Set1
if corpusLevel == "lines":
    xlabel = "Number of Chunks"
else:
    xlabel = "Sources"
ylabel = "Frequency"
mainTitle = "Comparison of selected words in Shakespeare's Hamlet"
yRange = [0, max(df["Freq"])*2]
angle = 45

# Plot
if corpusLevel == "lines":
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
