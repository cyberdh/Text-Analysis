# NOTE: This chunk of code is only for use with Research Desktop. You will get an error if you try to run this code on your personal device!!

import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages for notebook 

from textblob import TextBlob
from nltk.corpus import stopwords
import re
import string
import pandas as pd
import glob
import zipfile
import math
import matplotlib.pyplot as plt

# Set needed variables
source = "coronaVirus01-21Jan2020"
fileType = ".json"
nltkStop = True
customStop = True
ng = 2
textColIndex = "text"
stopLang = stopwords.fileids()
encoding = "UTF-8"
errors = "ignore"
stopWords = []
cleanText = []
ngramList = []



# File paths

homePath = os.environ['HOME']
dataHome = os.path.join(homePath, "Text-Analysis-master", "data")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")
if fileType == ".csv":
    dataRoot = os.path.join(dataHome, "twitter", "CSV")
else:
    dataRoot = os.path.join(dataHome, "twitter", "JSON")


# Stopwords

# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))
    
    stopWords.extend(['pic', 'com', 'coronavirus', 'twitter'])


# Add own stopword list

if customStop is True:
    stopWordsFilepath = os.path.join(dataHome, "twitterStopword.txt")

    with open(stopWordsFilepath, "r",encoding = encoding, errors = errors) as stopfile:
        stopWordsCustom = [x.strip() for x in stopfile.readlines()]

    stopWords.extend(stopWordsCustom)


# Functions

def textClean(text):
    
    text = text.strip().lower()
    
    tweets = re.sub(r"http\S+", "", text)
    
    tokens = re.split(r'\W+', tweets )
    
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


# Unzip files

direct = dataRoot
allZipFiles = glob.glob(os.path.join(dataRoot, "*.zip"))
for item in allZipFiles:
    fileName = os.path.splitext(direct)[0]
    zipRef = zipfile.ZipFile(item, "r")
    zipRef.extractall(fileName)
    zipRef.close()
    os.remove(item)


# Reading in data

if fileType == ".csv":
    filenames = glob.glob(os.path.join(dataRoot, source + fileType))     
    df = (pd.read_csv(file, engine = "python") for file in filenames)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf, dtype = 'str')
    tweets = cdf[textColIndex].values.tolist()
if fileType == ".json":
    filenames = glob.glob(os.path.join(dataRoot, source+fileType))
    df = (pd.read_json(file, encoding = encoding, lines = True) for file in filenames)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf, dtype = 'str')
    tweets = cdf[textColIndex].values.tolist()
    
    
content = '\n'.join(tweets)
cleanTokens = textClean(content)

print('Finished tokenizing text {}\n'.format(filenames))


# Convert text to a str object so we can find ngrams later.

cleanText = ' '.join(cleanTokens)


# Find Ngrams

blob = TextBlob(cleanText)

if ng == 1: 
    nGrams = blob.ngrams(n=1)
if ng == 2:
    nGrams = blob.ngrams(n=2)
if ng == 3:
    nGrams = blob.ngrams(n=3)


# Convert ngrams to a list

for wlist in nGrams:
   ngramList.append(' '.join(wlist))


# Make dataframe. 
df = pd.DataFrame(ngramList)
dfCounts = df[0].value_counts()
countsDF = pd.DataFrame(dfCounts)
countsDF.reset_index(inplace = True)
df_C = countsDF.rename(columns={'index':'ngrams',0:'freq'})
df_C['ngrams'] = df_C['ngrams'].astype(str)
dfNG = df_C.sort_values('freq', ascending = False)


# Now lets see what our dataframe looks like.
dfNG.head(10)


# Plot our bargraph

# Variables
n = 10
outputFile = "ngramTopTenTwitter.svg"
fmt = 'svg'
dpi = 300
figSz = (8,4)
angle = 85
title = 'Top 10 Ngrams, Coronavirus'
color = ['red','orange', 'yellow', 'green', 'blue','darkorchid', 'darkred', 'darkorange','gold', 'darkgreen']
labCol = 'red'
ngramStop = ["via youtube"]

# Ngram Stopwords
text = dfNG[~dfNG['ngrams'].isin(ngramStop)]
dfTN = text[0:n]


# Plot
plt.rcdefaults()

plt.figure(dpi=dpi, figsize = figSz)

plt.bar(dfTN["ngrams"], dfTN["freq"], align = 'center', alpha = 0.5, color = color)
    

        
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
