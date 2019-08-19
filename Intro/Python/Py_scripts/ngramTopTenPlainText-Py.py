# NOTE: This chunk of code is only for use with Research Desktop. You will get an error if you try to run this code on your personal device!!

import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages for notebook 

from textblob import TextBlob
from nltk.corpus import stopwords
import nltk
import re
import string
import pandas as pd
from collections import Counter, defaultdict
import numpy as np
import operator
import glob
import math
import matplotlib.pyplot as plt

get_ipython().magic('matplotlib inline')


# File paths

homePath = os.environ["HOME"]
dataHome = os.path.join(homePath, "Text-Analysis-master", "data", "shakespeareDated")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")


# Set needed variables

data = "*"
fileType = ".txt"
nltkStop = True
customStop = True
ng = 2
stopLang = 'english'
stopWords = []
cleanText = []
ngramList = []

#print(" ".join(stopwords.fileids()))


# Stopwords

# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))

    stopWords.extend(['would', 'said', 'says', 'also', 'good', 'lord', 'come', 'let'])


# Add own stopword list

if customStop is True:
    stopWordsFilepath = os.path.join(homePath, "Text-Analysis-DavidBranchV2", "data", "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = 'utf-8') as stopfile:
        stopWordsCustom = [x.strip() for x in stopfile.readlines()]

    stopWords.extend(stopWordsCustom)


# Functions

# Text Cleaning

def textClean(text):
    
    text = text.strip().lower()
    
    tokens = re.split(r'\W+', text )
    
    # remove empty string
    tokens = [t for t in tokens if t]
    
    # remove digits
    tokens = [t for t in tokens if not t.isdigit()]
    
    # built-in stop words list
    tokens = [t for t in tokens if t not in stopWords]
        
    # remove punctuation
    puncts = list(string.punctuation)
    puncts.append('--')

    tokens = [t for t in tokens if t not in puncts]

    return tokens


# Reading in the Text

for path in glob.glob(os.path.join(dataHome, data + fileType)):
    with open(path, "r") as file:
         # skip hidden file
        if path.startswith('.'):
            continue
        text = file.read()
        cleanText.extend(textClean(text))


# Convert text to a str object so we can find ngrams later.

cleanTokens = ' '.join(cleanText)


# Find Ngrams

blob = TextBlob(cleanTokens)

if ng == 1: 
    nGrams = blob.ngrams(n=1)
if ng == 2:
    nGrams = blob.ngrams(n=2)
if ng == 3:
    nGrams = blob.ngrams(n=3)


# Converting ngrams to a list.

for wlist in nGrams:
   ngramList.append(' '.join(wlist))


# Now we make our dataframe.

df = pd.DataFrame(ngramList)
dfCounts = df[0].value_counts()
countsDF = pd.DataFrame(dfCounts)
countsDF.reset_index(inplace = True)
df_C = countsDF.rename(columns={'index':'ngrams',0:'freq'})
df_C['ngrams'] = df_C['ngrams'].astype(str)
dfNG = df_C.sort_values('freq', ascending = False)


# Now lets see what our dataframe looks like.
df_C.head(10)


# Plot our bargraph

# Variables
n = 10
outputFile = "ngramTopTenPlainText.svg"
fmt = 'svg'
dpi = 300
angle = 60
title = 'Top 10 Ngrams, Shakespeare'
color = ['red','orange', 'yellow', 'green', 'blue','darkorchid', 'darkred', 'darkorange','gold', 'darkgreen']
labCol = 'red'
ngramStop = ["love love", "know know", "fie fie", "ha ha"]

# Ngram Stopwords
text = dfNG[~dfNG['ngrams'].isin(ngramStop)]
dfTN = text[0:n]

# Plot
plt.rcdefaults()

plt.bar(dfTN['ngrams'], dfTN['freq'], align = 'center', alpha = 0.5, color = color)
    

        
plt.xticks(dfTN['ngrams'])
plt.xticks(rotation = angle)
        
xlabel = plt.xlabel('Ngrams')
xlabel.set_color(labCol)
ylabel = plt.ylabel('Frequency')
ylabel.set_color(labCol)
    
high = max(dfTN['freq'])
low = 0
    
plt.ylim(low, math.ceil(high + 0.1 * (high - low)))
    
for xpos, count in zip(dfTN['ngrams'], dfTN['freq']):
    
    plt.text(x = xpos, y = count + 1, s = str(count), ha = 'center', va = 'bottom')

plt.title(title)
 
plt.savefig(os.path.join(dataResults, outputFile), format = fmt, dpi = dpi, bbox_inches = 'tight')
    
plt.show()
