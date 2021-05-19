# Points to Cyber DH Python Environment
import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"

# Import remaining packages
from nltk.corpus import stopwords
import string
from collections import defaultdict
import matplotlib.pyplot as plt
import re
import pandas as pd
import gensim
from gensim.models.phrases import Phrases, Phraser
from gensim.utils import simple_preprocess
import spacy
import wordcloud

# File paths saved as variables for use later in code
homePath = os.environ['HOME']
dataHome = os.path.join(homePath, "Text-Analysis-master", "data")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")
corpusRoot = os.path.join(dataHome, "shakespeareFolger")
directRoot = os.path.join(dataHome, "starTrek")

# Variables for use later in the code.
corpusLevel = "lines"
nltkStop = True
customStop = True
stopLang = 'english'
spacyLem = True
lemLang = "en"
encoding = "UTF-8"
errors = "ignore"
stopWords = []

# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))

    stopWords.extend(['would', 'said', 'says', 'say', 'also', 'ay', 'hast'])

# Custom stop words
if customStop is True:
    stopWordsFilepath = os.path.join(dataHome, "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = encoding) as stopfile:
        stopWordsCustom = [x.strip() for x in stopfile.readlines()]

    stopWords.extend(stopWordsCustom)

# Text cleaning function
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

def removeStopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stopWords] for doc in texts]

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
        nlp = spacy.load(lemLang+"_core_web_sm", disable=['parser', 'ner'])
    
        # Do lemmatization
       
        dataLemmatized = lemmatization(dataWordsNgrams)
       
        return dataLemmatized
    
    else:
        
        return dataWordsNgrams

# Function for plotting wordcloud
def plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt):

    freq = defaultdict(int)

    for t in tokens:
        freq[t] += 1
    
    wc = wordcloud.WordCloud(width = width, height = height, background_color = bgc, max_words = maxWordCnt, colormap = cm, min_font_size=minFont)
    

    # generate word cloud
    wc.fit_words(freq)

    # show
    plt.figure(figsize = figSz)
    plt.imshow(wc, interpolation = 'bilinear')
    plt.axis("off")

    plt.tight_layout()
    
    # save graph as a png image to file
    plt.savefig(wcImgFilepath, format = fmt, dpi = dpi, bbox_inches = 'tight')
    
    plt.show()

# Function for creating a wordcloud from a single text
def drawWordCloudLines(textFilepath, wcImgFilepath, dpi, 
                                maxWordCnt):
    docs = []
    with open(textFilepath, "r", encoding=encoding, errors = errors) as f:
        for line in f:
            stripLine = line.strip()
            if len(stripLine) == 0:
                continue
            docs.append(stripLine.split())

    words = list(sentToWords(docs))
    stop = removeStopwords(words)
    lemma = makeLemma(stop)
    tokens = [item for sublist in lemma for item in sublist]
    
    
    plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt)

# Function for creating a wordcloud from multiple texts
def drawWordCloudFiles(corpusRoot, wcImgFilepath, dpi, 
                          maxWordCnt):
   
    docs = []
    
    for root, subdirs, files in os.walk(corpusRoot):
        
        for filename in files:
            
            # skip hidden file
            if filename.startswith('.'):
                continue
            
            textFilepath = os.path.join(root, filename)
            
            with open(textFilepath, "r", encoding=encoding, errors = errors) as f:
                docs.append(f.read().strip('\n').splitlines())
                
        
        words = list(sentToWords(docs))
        stop = removeStopwords(words)
        lemma = makeLemma(stop)
        tokens = [item for sublist in lemma for item in sublist]
                
    
    plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt)

def drawWordCloudDirect(directRoot, wcImgFilepath, dpi, maxWordCnt):
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
            
    
    plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt)

#Variables
document = "Hamlet.txt"
wcOutputFile = "wordcloud.png"
fmt = "png"
width = 800
height = 400
bgc = "white"
cm = "Dark2"
dpi = 300
maxWordCnt = 500
minFont = 10
figSz = (20, 10)


if corpusLevel == "lines":
    # Use case one, draw word cloud from a single text

    textFilepath = os.path.join(corpusRoot, document)

    # filepath to save word cloud image
    wcImgFilepath = os.path.join(dataResults, wcOutputFile)

    # Plot wordcloud from single text
    drawWordCloudLines(textFilepath, wcImgFilepath, dpi, maxWordCnt)
elif corpusLevel == "files":
    # Use case two, draw word cloud from a corpus root

    # filepath to save word cloud image
    wcImgFilepath = os.path.join(dataResults, wcOutputFile)

    # Plot wordcloud from corpus
    drawWordCloudFiles(corpusRoot, wcImgFilepath, dpi, maxWordCnt)
elif corpusLevel == "direct":
    # Use case three, draw word cloud from multiple directories

    # filepath to save word cloud image
    wcImgFilepath = os.path.join(dataResults, wcOutputFile)

    # Plot wordcloud from corpus
    drawWordCloudDirect(directRoot, wcImgFilepath, dpi, maxWordCnt)
else:
    print('The corpusLevel variable in the variables cell of code (4th cell) was not assigned "lines", "files", or "direct" and so no corpus has been read in nor a wordcloud created. Please read the instructions preceding the variables cell and decide which option best fits your corpus.')
    exit()