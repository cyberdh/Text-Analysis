
# coding: utf-8

# 
# 
# 
# # Document Similarity with Latent Semantic Analysis (LSA)
# 
# The following code does LSA document similarity in Python. We then output the document similarity matrix as a .csv file which can be manipulated to highlight similarity between documents. We also output a heatmap which gives an initial impression of the similarity between documents. 

# ###  Before we begin
# Before we start, you will need to have set up a [Carbonate account](https://kb.iu.edu/d/aolp) in order to access [Research Desktop (ReD)](https://kb.iu.edu/d/apum). You will also need to have access to ReD through the [thinlinc client](https://kb.iu.edu/d/aput). If you have not done any of this, or have only done some of this, but not all, you should go to our [textPrep-Py.ipynb](https://github.com/cyberdh/Text-Analysis/blob/master/Intro/Python/Py_notebooks/textPrep-Py.ipynb) before you proceed further. The textPrep-Py notebook provides information and resources on how to get a Carbonate account, how to set up ReD, and how to get started using the Jupyter Notebook on ReD.   


# In[1]:

import sys
import os

# The code in the cell below points to a Python environment specificaly for use with the Python code created by Cyberinfrastructure for Digital Humanities. It allows for the use of the different pakcages in our code and their subsequent data sets.

# NOTE: The two lines of code below are only for use with Research Desktop. You will get an error if you try to run this code on your personal device!!

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
import seaborn as sns
import matplotlib.pyplot as plt


# This will ignore deprecation and future warnings. All the warnings in this code are not concerning and will not break the code or cause errors in the results.

# Suppress warnings from pandas library
warnings.filterwarnings("ignore", category=DeprecationWarning,
                        module="pandas", lineno=570)
warnings.filterwarnings("ignore", category=FutureWarning,
                        module = "sklearn", lineno = 1059)


# Getting your data

# File path variables

homePath = os.environ["HOME"]
dataHome = os.path.join(homePath, "Text-Analysis-master", "data", "shakespeareDated")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")


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


# NLTK Stopwords

if nltkStop is True:
    # NLTK Stop words
    stopWords = stopwords.words(language)

    stopWords.extend(['would', 'said', 'says', 'also'])
    #print (" ".join(stopwords.fileids()))


# Add own stopword list

if customStop is True:
    stopWordsFilepath = os.path.join(homePath, "Text-Analysis-master", "data", "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = encoding, errors = errors) as f:
        stopWordsList = [x.strip() for x in f.readlines()]

    stopWords.extend(stopWordsList)


# Dictionary and stemmer

if stem is True:
    stemmer = SnowballStemmer(language)
    #print(" ".join(SnowballStemmer.languages))


# Functions
# Stemming and tokenization functions

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


# Now let's take a look at our data frame.

print(testDF.iloc[:10, 7640:7650])

# Get words that correspond to each column
vectorizer.get_feature_names()


# Run SVD and Cosine Similarity

lsa = TruncatedSVD(n_components = 100, n_iter = 1000, random_state = 42)
dtmLsa = lsa.fit_transform(dtm)
cosineSim = cosine_similarity(dtmLsa)


# Save as a data frame

csvFileName = "docSimilarityMatrix.csv"

df = pd.DataFrame(cosineSim, index = tokenDict.keys(), columns=tokenDict.keys())
dfS = df[sorted(df)]
sortedDf = dfS.sort_index(axis = 0)
np.fill_diagonal(sortedDf.values, np.nan)
sortedDf.to_csv(os.path.join(dataResults, csvFileName))
sortedDf


# Plot Heatmap

#Variables
heatmapFileName = 'DocSimHeatmap.svg'
dpi = 600
colorScheme = 'RdYlGn'
fontScale = 1

# Plot
figureSize = len(sortedDf)
sns.set(rc={'figure.figsize':(figureSize + 10, figureSize)}, font_scale = fontScale)
ax = sns.heatmap(sortedDf, cmap = colorScheme)
ax.figure.savefig(os.path.join(dataResults, heatmapFileName), dpi = dpi, bbox_inches='tight')
plt.yticks(rotation=0)
plt.xticks(rotation=90)
plt.show()


# ## VOILA!!

# This notebook was adapted from https://www.datascienceassn.org/sites/default/files/users/user1/lsa_presentation_final.pdf at Colorado University, Boulder. Accessed on 02/01/2019.
