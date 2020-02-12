
# coding: utf-8

# Create Word 2 Vec Model

# Run CyberDH environment
# NOTE: This chunk of code is only for use with Research Desktop. You will get an error if you try to run this on your personal device!!
import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages 
import re
from nltk.corpus import stopwords
import glob
import pandas as pd
import warnings
from pprint import pprint
import spacy
from collections import Counter

import gensim
from gensim.utils import simple_preprocess
from gensim.models.phrases import Phrases, Phraser


# This will ignore deprecation, user, and future warnings.
warnings.filterwarnings("ignore", category=UserWarning,
                        module = "gensim", lineno = 598)

warnings.filterwarnings("ignore", category=FutureWarning,
                        module = "gensim", lineno = 737)
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Getting your data
# File paths

homePath = os.environ["HOME"]
dataHome = os.path.join(homePath, "Text-Analysis-master", "data")
cleanModel = os.path.join(homePath, "Text-Analysis-master", "TopicModeling", "Word2Vec", "cleanedData", "wordvecModel")


# Set needed variables
source = "Hamlet"
fileType = ".txt"
docLevel = False
nltkStop = True
customStop = True
spacyLem = True
stopLang = 'english'
lemLang = 'en'
encoding = "utf-8"
errors = "ignore"
textColIndex = "text"
stopWords = []
docs = []


# Stopwords
# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))

    stopWords.extend(['would', 'said', 'says', 'also', 'let', 'not', 'know', 'come', 'good', 'twere'])


# Add own stopword list
if customStop is True:
    stopWordsFilepath = os.path.join(homePath, "Text-Analysis-master", "data", "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = encoding, errors = errors) as stopfile:
        stopWordsCustom = [x.strip() for x in stopfile.readlines()]

    stopWords.extend(stopWordsCustom)


# Reading in .txt files
if fileType == ".txt":
    paths = glob.glob(os.path.join(dataHome, "shakespeareFolger",source + fileType))
    for path in paths:
        with open(path, "r", encoding = encoding, errors = errors) as file:
             # skip hidden file
            if path.startswith('.'):
                continue
            if docLevel is True:
                docs.append(file.read().strip('\n').splitlines())
            else:
                for line in file:
                    stripLine = line.strip()
                    if len(stripLine) == 0:
                        continue
                    docs.append(stripLine.split())


# Reading in .csv and .json files
if fileType == ".csv":
    allFiles = glob.glob(os.path.join(dataHome, "twitter", "CSV", source + fileType))     
    df = (pd.read_csv(f, engine = "python") for f in allFiles)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf, dtype = 'str')
    tweets = cdf[textColIndex].values.tolist()
if fileType == ".json":
    allFiles = glob.glob(os.path.join(dataHome, "twitter", "JSON", source + fileType))     
    df = (pd.read_json(f, encoding = encoding) for f in allFiles)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf, dtype = 'str')
    tweets = cdf[textColIndex].values.tolist()


# Data variable
if len(docs) > 0:
    data = docs
else:
    if len(tweets) > 0:
        data = tweets
        # Remove Urls
        data = [re.sub(r'http\S+', '', sent) for sent in data]
        # Remove new line characters
        data = [re.sub('\s+', ' ', sent) for sent in data]
print(len(data))


# Tokenizing
def sentToWords(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

dataWords = list(sentToWords(data))

if docLevel is True:
    for i in dataWords:
        print(i[:1])
else:
    print(dataWords[:1])


# Find Bigrams and Trigrams
# Build the bigram and trigram models
bigram = Phrases(dataWords, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = Phrases(bigram[dataWords], threshold=100)  

# Removes model state from Phrases thereby reducing memory use.
bigramMod = Phraser(bigram)
trigramMod = Phraser(trigram)

# See bigram/trigram example
testNgram = trigramMod[bigramMod[dataWords[0]]]
char = "_"
nGrams = [s for s in testNgram if char in s]
            
pprint(Counter(nGrams))


# Functions
# Define functions for stopwords, bigrams, trigrams and lemmatization
def removeStopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stopWords] for doc in texts]

def makeBigrams(texts):
    return [bigramMod[doc] for doc in texts]

def makeTrigrams(texts):
    return [trigramMod[bigramMod[doc]] for doc in texts]


if spacyLem is True:
    def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        """https://spacy.io/api/annotation"""
        textsOut = []
        lemmaPOS = []
        for sent in texts:
            doc = nlp(" ".join(sent)) 
            textsOut.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
            lemmaPOS.append([token.text and token.lemma_ and token.pos_ for token in doc if token.pos_ in allowed_postags])
        return textsOut
        print(lemmaPOS[:10])


# Now we apply the functions. 
# Remove Stop Words
dataWordsNostops = removeStopwords(dataWords)

# Form Bigrams
dataWordsNgrams = makeBigrams(dataWordsNostops)

if spacyLem is True:
    # Initialize spacy language model, eliminating the parser and ner components
    nlp = spacy.load(lemLang, disable=['parser', 'ner'])
    
    # Do lemmatization tagging only noun, adj, vb, adv
    allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']
    dataLemmatized = lemmatization(dataWordsNgrams, allowed_postags=allowed_postags)
    lemmaPOS = []
    for sent in dataLemmatized:
        lemmaNLP = nlp(" ".join(sent))
        for token in lemmaNLP:
            lemmaPOS.append([token.text, token.lemma_, token.pos_])
    print(lemmaPOS[:10])
    

    # Find ngrams and count number of times they occur
    dataNgrams = [s for s in dataLemmatized[0] if char in s]
    
else:
    dataNgrams = [s for s in dataWordsNgrams[0] if char in s]
print(Counter(dataNgrams))


# Getting Information
if spacyLem is True:
    # Create Corpus
    texts = dataLemmatized
    tokens = sum(texts, [])
else:
    # Create Corpus
    texts = dataWordsNgrams
    tokens = sum(texts, [])

count = Counter(tokens)
sortList = sorted(count.items(), key=lambda x:x[1], reverse = True)
print(sum(count.values()))
print(len(count))
print(sortList[150])


# Build vocabulary and train the model

# build vocabulary and train and save model
model = gensim.models.Word2Vec(
    texts,
    size=100,
    window=5,
    min_count=12,
    sg = 1,
    seed = 42,
    iter=10)
model.train(texts, total_examples=len(texts), epochs=model.iter)
model.save(os.path.join(homePath, cleanModel))


# This code was adapted from Kavita Ganesan at [http://kavita-ganesan.com/gensim-word2vec-tutorial-starter-code/#.XFnQmc9KjUI](http://kavita-ganesan.com/gensim-word2vec-tutorial-starter-code/#.XFnQmc9KjUI). Accessed 02/05/2019.
