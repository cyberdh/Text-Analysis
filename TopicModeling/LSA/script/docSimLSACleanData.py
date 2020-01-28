
# coding: utf-8

# Document Similarity with Latent Semantic Analysis (LSA)

# Run CyberDH environment

# NOTE: This cell is only for use with Research Desktop. You will get an error if you try to run this cell on your personal device!!
import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"

# Include necessary packages for notebook 
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import warnings
import numpy as np
import string
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

# This will ignore deprecation and future warnings. 
# Suppress warnings from pandas library
warnings.filterwarnings("ignore", category=DeprecationWarning,
                        module="pandas", lineno=570)
warnings.filterwarnings("ignore", category=FutureWarning,
                        module = "sklearn", lineno = 1059)
warnings.filterwarnings("ignore", category=UserWarning,
                        module = "sklearn", lineno = 300)

# Getting your data
# File paths
homePath = os.environ["HOME"]
dataHome = os.path.join(homePath, "Text-Analysis-master", "data", "shakespeareDated")
cleanedData = os.path.join(homePath, "Text-Analysis-master", "TopicModeling", "LSA", "cleanedData")

# Set needed variables
nltkStop = True
customStop = True
stem = True
lowerCase = True
language = 'english'
encoding = 'utf-8'
errors = 'ignore'
stopWords = []
tokenDict = {}

# Stopwords
if nltkStop is True:
    # NLTK Stop words
    stopWords = stopwords.words(language)

    stopWords.extend(['would', 'said', 'says', 'also'])

# Add own stopword list
if customStop is True:
    stopWordsFilepath = os.path.join(homePath, "Text-Analysis-master", "data", "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = encoding, errors = errors) as f:
        stopWordsList = [x.strip() for x in f.readlines()]

    stopWords.extend(stopWordsList)

# Dictionary and stemmer
if stem is True:
    stemmer = SnowballStemmer(language)


# Functions
if stem is True:
    def stemTokens(tokens, stemmer):
        stemmed = []
        for item in tokens:
            stemmed.append(stemmer.stem(item))
        return stemmed

    def tokenize(text):
        tokens = nltk.word_tokenize(text)
        stems = stemTokens(tokens, stemmer)
        return stems

else:
    def tokenize(text):
        tokens = nltk.word_tokenize(text)
        return tokens


# Read in documents
for subdir, dirs, files in os.walk(dataHome):
    for file in files:
        if file.startswith('.'):
                continue
        filePath = subdir + os.path.sep + file
        with open(filePath, 'r', encoding = encoding, errors = errors) as textFile:
            text = textFile.read()
            if lowerCase is True:
                lowers = text.lower()
                noPunctuation = lowers.translate(str.maketrans('','', string.punctuation))
                tokenDict[file] = noPunctuation
            else:
                noPunctuation = text.translate(str.maketrans('','', string.punctuation))
                tokenDict[file] = noPunctuation


# Let's check and see if our dictionary now has our data. 
print(list(tokenDict.keys())[0:10])


# Tfidf Vectorizer
vectorizer = TfidfVectorizer(tokenizer = tokenize, stop_words=stopWords)
dtm = vectorizer.fit_transform(tokenDict.values())
testDF = pd.DataFrame(dtm.toarray(), index=tokenDict.keys(), columns = vectorizer.get_feature_names())
testDF = testDF.sort_index(axis = 0)


# Now let's take a look at our data frame where the rows are the documents and the columns are the terms. 
testDF.iloc[:10, 7640:7650]

# Get words that correspond to each column
vectGFN = vectorizer.get_feature_names()
print(vectGFN[:20])


# Run SVD and Cosine Similarity
lsa = TruncatedSVD(n_components = 100, n_iter = 1000, random_state = 42)
dtmLsa = lsa.fit_transform(dtm)
cosineSim = cosine_similarity(dtmLsa)


# Save as .csv file
csvFileName = "docSimilarityMatrix.csv"

df = pd.DataFrame(cosineSim, index = tokenDict.keys(), columns=tokenDict.keys())
dfS = df[sorted(df)]
sortedDf = dfS.sort_index(axis = 0)
np.fill_diagonal(sortedDf.values, np.nan)
sortedDf.to_csv(os.path.join(cleanedData, csvFileName))


# This notebook was adapted from https://www.datascienceassn.org/sites/default/files/users/user1/lsa_presentation_final.pdf at Colorado University, Boulder. Accessed on 02/01/2019.
