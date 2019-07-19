
# coding: utf-8

# # Word 2 Vec
# 
# The following code walks you through using word2vec from the Python Gensim package. Word2Vec is a Word Embedding Model (WEM) and helps to find how specific words are used in a given text. 

# ###  Before we begin
# Before we start, you will need to have set up a [Carbonate account](https://kb.iu.edu/d/aolp) in order to access [Research Desktop (RED)](https://kb.iu.edu/d/apum). You will also need to have access to RED through the [thinlinc client](https://kb.iu.edu/d/aput). If you have not done any of this, or have only done some of this, but not all, you should go to our [textPrep-Py.ipynb](https://github.com/cyberdh/Text-Analysis/blob/master/Python/Py_notebooks/textPrep-Py.ipynb) before you proceed further. The textPrepPy notebook provides information and resources on how to get a Carbonate account, how to set up RED, and how to get started using the Jupyter Notebook on RED. 

import sys
import os

# The code in the below points to a Python environment specificaly for use with the Python code created by Cyberinfrastructure for Digital Humanities. It allows for the use of the different pakcages in our code and their subsequent data sets.
# NOTE: These two lines of code are only for use with Research Desktop. You will get an error if you try to run this code on your personal device!!
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages for notebook 

import re
from os.path import join, isfile, splitext
import string
import nltk
from nltk.corpus import stopwords
import glob
import numpy as np
import pandas as pd
import warnings
from pprint import pprint
import spacy
from sklearn.decomposition import PCA
get_ipython().magic('matplotlib notebook')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from collections import Counter

import gensim
import gensim.corpora as corpora
import gensim.downloader as api
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models import doc2vec
from gensim.models.phrases import Phrases, Phraser


# This will ignore deprecation, user, and future warnings. All the warnings in this code are not concerning and will not break the code or cause errors in the results.

warnings.filterwarnings("ignore", category=UserWarning,
                        module = "gensim", lineno = 598)

warnings.filterwarnings("ignore", category=FutureWarning,
                        module = "gensim", lineno = 737)
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Getting your data

# File path variables

homePath = os.environ["HOME"]
dataHome = os.path.join(homePath, "Text-Analysis-master", "data")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")


# Set needed variables

source = "*"
fileType = ".txt"
docLevel = True
nltkStop = True
customStop = False
spacyLem = True
stopLang = 'english'
lemLang = 'en'
stopWords = []
docs = []
tweets = []

#print(" ".join(stopwords.fileids()))


# Stopwords
# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))

    stopWords.extend(['would', 'said', 'says', 'also', 'let', 'not'])


# Add own stopword list

if customStop is True:
    stopWordsFilepath = os.path.join(homePath, "Text-Analysis-master", "data", "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = 'utf-8') as stopfile:
        stopWordsCustom = [x.strip() for x in stopfile.readlines()]

    stopWords.extend(stopWordsCustom)


# Reading in .txt files

if fileType == ".txt":
    paths = glob.glob(os.path.join(dataHome, "shakespeareDated",source + fileType))
    for path in paths:
        with open(path, "r", encoding = 'ISO-8859-1') as file:
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


# Reading in .csv files

if fileType == ".csv":
    all_files = glob.glob(os.path.join(dataHome, "twitter", source + fileType))     
    df_all = (pd.read_csv(f) for f in all_files)
    cc_df = pd.concat(df_all, ignore_index=True)
    cc_df = pd.DataFrame(cc_df, dtype = 'str')
    tweets = cc_df['text'].values.tolist()


# Reading in JSON files

if fileType == ".json":
    for filename in glob.glob(os.path.join(dataHome, "twitter", "JSON", source + fileType)):
        with open(filename, 'r', encoding = "utf-8") as jsonData:
            for line in jsonData:
                tweets.append(json.loads(line))
    df = pd.DataFrame(tweets)
    tweets = df['text'].tolist()


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

pprint(data[:1])


# Tokenizing

def sentToWords(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

dataWords = list(sentToWords(data))

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


# Now we apply the functions

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
# 
# Now we want to get some information about our corpus now that it is cleaned.

if spacyLem is True:
    # Create Corpus
    texts = dataLemmatized
    tokens = sum(texts, [])
else:
    # Create Corpus
    texts = dataWordsNgrams
    tokens = sum(texts, [])

from collections import Counter
count = Counter(tokens)
print(sum(count.values()))
print(len(count))
print(count.most_common(1000))


# Build vocabulary and train the model

# build vocabulary and train model

model = gensim.models.Word2Vec(
    texts,
    size=100,
    window=10,
    min_count=60,
    workers=1,
    sg = 1,
    seed = 42)
model.train(texts, total_examples=len(texts), epochs=10)


# Let's find some word relationships

w2vCSVfile = 'word2vec.csv'
w1 = "woman"
topn = 30

wtv = model.wv.most_similar(positive=[w1], topn = topn)
df = pd.DataFrame(wtv)
df.to_csv(os.path.join(dataResults, w2vCSVfile))
dfG = df[:10]
dfG


# Here we can compare two words to each other.

model.wv.similarity(w1 = 'king', w2 = 'queen')


# Now convert our results in the `df` variable from above to a list

dfLst = df[0].tolist()
dfLst.append(w1)


# Here we create a function that uses Principal Component Analysis (PCA) for dimensionality reduction.

# Variables
pcaScatterPlot = "pcaScatterPlot.svg"
color = 'crimson'

# Function
def display_pca_scatterplot(model, words=None, sample=0):
    if words == None:
        if sample > 0:
            words = np.random.choice(list(model.wv.vocab.keys()), sample)
        else:
            words = [ word for word in model.wv.vocab ]
        
    word_vectors = np.array([model[w] for w in words])

    twodim = PCA().fit_transform(word_vectors)[:,:2]
    
    plt.figure(figsize=(9,9))
    plt.scatter(twodim[:,0], twodim[:,1], edgecolors='k', c=color)
    for word, (x,y) in zip(words, twodim):
        plt.text(x+0.05, y+0.05, word)
        plt.savefig(os.path.join(dataResults, pcaScatterPlot))


# Now we apply the function to our `model` from above and the list we made from our `df` variable. 
# Note however that the graph is interactive. You can zoom in by clicking the button with the square on it and the dragging over the section of the graph you wish to zoom in on. You can then click the save button to save the zoomed in version of the graph.

display_pca_scatterplot(model, dfLst)


# ## VOILA!!

# This code was adapted from Kavita Ganesan at [http://kavita-ganesan.com/gensim-word2vec-tutorial-starter-code/#.XFnQmc9KjUI](http://kavita-ganesan.com/gensim-word2vec-tutorial-starter-code/#.XFnQmc9KjUI). Accessed 02/05/2019. The display_pca_scatterplot function was taken entirley from [https://web.stanford.edu/class/cs224n/materials/Gensim%20word%20vector%20visualization.html](https://web.stanford.edu/class/cs224n/materials/Gensim%20word%20vector%20visualization.html) and was accessed on 07/18/2019.
