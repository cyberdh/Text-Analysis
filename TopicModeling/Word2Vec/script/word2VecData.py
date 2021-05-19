
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
import itertools as it

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
chunkLevel = "lines"
n = 100
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
    if chunkLevel == "files":
        paths = glob.glob(os.path.join(dataHome, "shakespeareFolger", source + fileType))
        for path in paths:
            with open(path, "r", encoding = encoding, errors = errors) as file:
                 # skip hidden file
                if path.startswith('.'):
                    continue
                docs.append(file.read().strip('\n').splitlines())
                
    elif chunkLevel == "lines":
        paths = glob.glob(os.path.join(dataHome, "shakespeareFolger", source + fileType))
        for path in paths:
            with open(path, "r", encoding = encoding, errors = errors) as file:
                 # skip hidden file
                if path.startswith('.'):
                    continue
                for line in file:
                    stripLine = line.strip()
                    if len(stripLine) == 0:
                        continue
                    docs.append(stripLine.split())
    elif chunkLevel == "direct":
    
        paths = []
        txt = []
        dataPath = os.path.join(dataHome, "starTrek")
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
                t = f.read().strip().split()
                txt.append(t)
        df["Text"] = pd.Series(txt)
        df["Text"] = ["".join(map(str, l)) for l in df["Text"].astype(str)]
        d = {'Text':'merge'}
        dfText = df.groupby(['Folder'])["Text"].apply(lambda x: ' '.join(x)).reset_index()
        
        docs.extend(dfText["Text"].tolist())
        
    else:
        None
else:
    None


# Reading in .csv and .json files
if fileType == ".csv":
    allZipFiles = glob.glob(os.path.join(csvPath,"*.zip"))
    for item in allZipFiles:
        fileName = os.path.splitext(csvPath)[0]
        zipRef = zipfile.ZipFile(item, "r")
        zipRef.extractall(fileName)
        zipRef.close()
        os.remove(item)
elif fileType == ".json":
    allZipFiles = glob.glob(os.path.join(jsonPath,"*.zip"))
    for item in allZipFiles:
        fileName = os.path.splitext(jsonPath)[0]
        zipRef = zipfile.ZipFile(item, "r")
        zipRef.extractall(fileName)
        zipRef.close()
        os.remove(item)

elif not glob.glob(os.path.join(dataHome,"*.tar.gz")):
    None
else:
    None

if fileType == ".csv":
    allFiles = glob.glob(os.path.join(dataHome, "twitter", "CSV", source + fileType))     
    df = (pd.read_csv(f, engine = "python") for f in allFiles)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf, dtype = 'str')
    tweets = cdf[textColIndex].values.tolist()
if fileType == ".json":
    allFiles = glob.glob(os.path.join(dataHome, "twitter", "JSON", source + fileType))     
    df = (pd.read_json(f, encoding = encoding, lines = True) for f in allFiles)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf, dtype = 'str')
    tweets = cdf[textColIndex].values.tolist()

# Data variable
if len(docs) > 0:
    if chunkLevel == "files" or "direct":
        data = docs
    elif chunkLevel == "lines":
        data = []
        for i in list(it.zip_longest(*(iter(docs),)*n)):
            data.append(i)
    else:
        None
elif len(tweets) > 0:
    data = tweets
    # Remove Urls
    data = [re.sub(r'http\S+', '', sent) for sent in data]
    # Remove new line characters
    data = [re.sub('\s+', ' ', sent) for sent in data]
else:
    None
print(len(data))


# Tokenizing
def sentToWords(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

dataWords = list(sentToWords(data))

print(len(dataWords))


# Find Bigrams and Trigrams
#Variables
minCount = 5
tHold = 100
# Build the bigram and trigram models
bigram = Phrases(dataWords, min_count=minCount, threshold=tHold) # higher threshold fewer phrases.
trigram = Phrases(bigram[dataWords], threshold=tHold)  

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
minWrdCnt = 5

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
wordCount = sum(count.values())
uniqueWords = len(count)
minWrdCntLst = [i for i,j in enumerate(sortList) if j[1] == minWrdCnt]
minWrdCntMaxIdx = max(minWrdCntLst)
numTotalWordsKeep = sum(n for _,n in sortList[:minWrdCntMaxIdx])
keepUniqueWordsPct = "{:.0%}".format((minWrdCntMaxIdx+1)/uniqueWords)
keepTotalWordsPct = "{:.0%}".format(numTotalWordsKeep/wordCount)
print("Total number of words = {}".format(wordCount))
print("Total number of unique words = {}".format(uniqueWords+1))
print("If minimum word count is {} then {} total words will be kept.".format(minWrdCnt,numTotalWordsKeep))
print("If minimum word count is {} then {} unique words will be kept.".format(minWrdCnt,minWrdCntMaxIdx+1))
print("First word to be kept and the number of times it appears: {}".format(sortList[minWrdCntMaxIdx]))
print("If minimum word count is {} you will keep {} of unique words and {} of total words.".format(minWrdCnt,keepUniqueWordsPct,keepTotalWordsPct))


# Build vocabulary and train the model

# build vocabulary and train and save model
model = gensim.models.Word2Vec(
    texts,
    size=200,
    window=5,
    min_count=minWrdCnt,
    sg = 1,
    seed = 42,
    iter=150)
model.train(texts, total_examples=len(texts), epochs=model.iter)
model.save(os.path.join(homePath, cleanModel))


# This code was adapted from Kavita Ganesan at [http://kavita-ganesan.com/gensim-word2vec-tutorial-starter-code/#.XFnQmc9KjUI](http://kavita-ganesan.com/gensim-word2vec-tutorial-starter-code/#.XFnQmc9KjUI). Accessed 02/05/2019.
