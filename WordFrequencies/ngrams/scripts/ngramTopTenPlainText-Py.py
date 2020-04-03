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
import math
import plotly as py
import plotly.express as px


# File paths

homePath = os.environ["HOME"]
dataHome = os.path.join(homePath, "Text-Analysis-master", "data", "shakespeareFolger")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")


# Set needed variables

data = "Hamlet"
fileType = ".txt"
nltkStop = True
customStop = True
ng = 2
stopLang = 'english'
encoding = "UTF-8"
errors = "ignore"
stopWords = []
cleanText = []
ngramList = []


# Stopwords

# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))

    stopWords.extend(['would', 'said', 'says', 'also', 'good', 'lord', 'come', 'let', 'hamlet'])


# Add own stopword list

if customStop is True:
    stopWordsFilepath = os.path.join(homePath, "Text-Analysis-master", "data", "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = encoding) as stopfile:
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
    with open(path, "r", encoding = encoding, errors = errors) as file:
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
dfNG["Pct"] = ((dfNG["freq"]/dfNG["freq"].sum())*100).round(3)
dfNG["Pct"] = dfNG["Pct"].astype(str) + "%"

# Now lets see what our dataframe looks like.
print(dfNG[:10])

# Plot our bargraph

# Variables
n = 10
outputFile = "ngramTopTenPlainText"
fmt = '.html'
Xlabel = "Ngram"
Ylabel = "Count"
Zlabel = "Percent"
wide = 750
tall = 550
angle = -45
title = 'Top 10 Words, Hamlet'
colors = px.colors.qualitative.Dark24
labCol = "crimson"
ngramStop = ["love love", "know know", "fie fie", "ha ha"]

# Ngram Stopwords
text = dfNG[~dfNG['ngrams'].isin(ngramStop)]
dfTN = text[0:n]

high = max(dfTN["freq"])
low = 0
# Plot
fig = px.bar(dfTN, x = "ngrams", y = "freq", hover_data=[dfTN["Pct"]],text = "freq", color = "ngrams",
             title = title, color_discrete_sequence=colors,
             labels = {"ngrams":Xlabel,"freq":Ylabel,"Pct":Zlabel})
fig.update_layout(title={'y':0.90, 'x':0.5, 'xanchor': 'center', 'yanchor':'top'},
                  font={"color": labCol}, width = wide, height = tall, 
                  showlegend=False)
fig.update_xaxes(tickangle = angle)
fig.update_yaxes(range = [low,math.ceil(high + 0.1 * (high - low))])
    
py.offline.plot(fig, filename=os.path.join(dataResults, outputFile + fmt), auto_open = False)
fig.show()
