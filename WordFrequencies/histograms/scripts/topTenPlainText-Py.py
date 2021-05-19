import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"

          
from nltk.corpus import stopwords
import string
from collections import defaultdict
import numpy.core.multiarray
import pandas as pd
import gensim
from gensim.models.phrases import Phrases, Phraser
from gensim.utils import simple_preprocess
import spacy
import operator
import plotly as py
import plotly.express as px
import re
import math


homePath = os.environ['HOME']
dataHome = os.path.join(homePath, 'Text-Analysis-master', 'data')
corpusRoot = os.path.join(dataHome, 'shakespeareFolger')
directRoot = os.path.join(dataHome, 'starTrek')
dataResults = os.path.join(homePath, 'Text-Analysis-master', 'Output')

corpusLevel = "lines"
nltkStop = True
customStop = True
spacyLem = True
stopLang = 'english'
lemLang = "en"
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
    
def sentToWords(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

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

def removeStopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stopWords] for doc in texts]

def makeBigrams(tokens):
    bigrams = get2gramPhrases(tokens)
    return [bigrams[doc] for doc in tokens]

def makeTrigrams(tokens):
    bigrams = get2gramPhrases(tokens)
    trigrams = get3gramPhrases(tokens)
    return [trigrams[bigrams[doc]] for doc in tokens]

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
    df = pd.DataFrame(sortedFreq, columns = ["Words", "Count"])
    df["Pct"] = ((df["Count"]/df["Count"].sum())*100).round(3)
    df["Pct"] = df["Pct"].astype(str) + "%"
    dfPct = df[0 : topn]
    
    high = max(df["Count"])
    low = 0
    
    fig = px.bar(dfPct, x = "Words", y = "Count",hover_data=[dfPct["Pct"]],text = "Count", color = "Words", 
                 title = title, color_discrete_sequence=colors,
                labels = {"Words":Xlabel,"Count":Ylabel,"Pct":Zlabel})
    fig.update_layout(title={'y':0.90, 'x':0.5, 'xanchor': 'center', 'yanchor':'top'}, 
                      font={"color": labCol}, width = wide, height = tall, showlegend=False)
    fig.update_xaxes(tickangle = angle)
    fig.update_yaxes(range = [low,math.ceil(high + 0.1 * (high - low))])
    
    py.offline.plot(fig, filename=imgFilepath, auto_open = False)
    fig.show()
    
    
def getTokensFrom1File(textFilepath):
    docs=[]
    with open(textFilepath, "r", encoding = encoding, errors = errors) as f:
        for line in f:
            stripLine = line.strip()
            if len(stripLine) == 0:
                continue
            docs.append(stripLine.split())

    words = list(sentToWords(docs))
    stop = removeStopwords(words)
    lemma = makeLemma(stop)
    tokens = [item for sublist in lemma for item in sublist]
    
    return tokens


def getTokensFromManyFiles(corpusRoot):
    
    docs = []
    
    for root, subdirs, files in os.walk(corpusRoot):
        
        for filename in files:
            
            # skip hidden file
            if filename.startswith('.'):
                continue
            
            textFilepath = os.path.join(root, filename)
            
            with open(textFilepath, "r", encoding = encoding, errors = errors) as f:
                docs.append(f.read().strip('\n').splitlines())
        
        words = list(sentToWords(docs))
        stop = removeStopwords(words)
        lemma = makeLemma(stop)
        tokens = [item for sublist in lemma for item in sublist]
    return tokens

def getTokensFromDirect(directRoot):
    paths = []
    docs = []
   
    dataPath = os.path.join(directRoot)
    for folder in sorted(os.listdir(dataPath)):
        if not os.path.isdir(os.path.join(dataPath, folder)):
            continue
        for file in sorted(os.listdir(os.path.join(dataPath, folder))):
            paths.append(((dataPath, folder, file)))
    df = pd.DataFrame(paths, columns = ["Root", "Folder", "File"])
    df["Paths"] = df["Root"].astype(str) +"/" + df["Folder"].astype(str) + "/" + df["File"].astype(str)
    for path in df["Paths"]:
        if not path.endswith(".txt"):
            continue
        with open(path, "r", encoding = encoding, errors = errors) as f:
            docs.extend(f.read().strip().split())
    
    words = list(sentToWords(docs))
    stop = removeStopwords(words)
    lemma = makeLemma(stop)
    tokens = [item for sublist in lemma for item in sublist]
    
    return tokens

# Variables
n = 10
singleDocName = 'Hamlet.txt'
outputFile = "topTenPlainText"
fmt = '.html'
Xlabel = "Word"
Ylabel = "Count"
Zlabel = "Percent"
wide = 750
tall = 550
angle = -45
title = 'Top 10 Words, Hamlet'
colors = px.colors.qualitative.Dark24
labCol = "crimson"

if corpusLevel == "lines":
    # Use case one, analyze top 10 most frequent words from a single text

    textFilepath = os.path.join(corpusRoot, singleDocName)

    # get tokens
    tokens = getTokensFrom1File(textFilepath)

    # get frequency
    freq = getFreq(tokens)

    imgFilepath = os.path.join(dataResults, outputFile + fmt)

    plotTopTen(freq, title, imgFilepath)
elif corpusLevel == "files":
    # Use case two, analyze top 10 most frequent words from a corpus root

    tokens = getTokensFromManyFiles(corpusRoot)

    # get frequency
    freq = getFreq(tokens)

    imgFilepath = os.path.join(dataResults, outputFile +fmt)

    plotTopTen(freq, title, imgFilepath)
elif corpusLevel == "direct":
    tokens = getTokensFromDirect(directRoot)

    # get frequency
    freq = getFreq(tokens)

    imgFilepath = os.path.join(dataResults, outputFile +fmt)

    plotTopTen(freq, title, imgFilepath)
else:
    None