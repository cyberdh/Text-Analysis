
# coding: utf-8

# Complex Sentiment Analysis Results

# Run CyberDH environment

# NOTE: This chunk of code is only for use with Research Desktop. You will get an error if you try to run this on your personal device!!
import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages 
import pandas as pd
import matplotlib.pyplot as plt


# File paths
homePath = os.environ['HOME']
dataClean = os.path.join(homePath, 'Text-Analysis-master', 'VADERSentimentAnalysis', 'cleanedData')
dataResults = os.path.join(homePath, 'Text-Analysis-master', 'Output')


# Read in positive words
pdf = pd.read_csv(os.path.join(dataClean, "posWords.csv"))
positdf = pd.DataFrame(pdf)
del positdf["Unnamed: 0"]
stopwords = []
poWordDF = positdf[~positdf["word"].isin(stopwords)]
posdf = poWordDF[:25]
posdf.head(10)


# Read in negative words
ndf = pd.read_csv(os.path.join(dataClean, "negWords.csv"))
negadf = pd.DataFrame(ndf)
del negadf["Unnamed: 0"]
stopwords = []
neWordDF = negadf[~negadf["word"].isin(stopwords)]
negdf = neWordDF[:25]
negdf.head(10)


# Combine the positive and negative dataframes.
freqDF = pd.concat([posdf, negdf], ignore_index=True)


# Plot positive words 
# Variables
posWordFile = "posWordsVader.svg"
posFmt = "svg"
posdpi = 600
posclr = ['darkgreen']
postitle = 'Top 25 Positive Words, #Coronavirus: VADER'
pFigSz = (8,4)
pFntSz = 8

fig = posdf.plot(x= 'word',kind='barh', align='center', color = posclr, figsize = pFigSz, fontsize = pFntSz)
fig.set_ylabel('Words', fontsize = pFntSz)
fig.set_xlabel('Frequency', fontsize = pFntSz)
fig.set_title(postitle, fontweight='bold',fontsize = pFntSz)
fig.set_ylim(fig.get_ylim()[::-1])
fig.set_xlim(0,1500 + max(freqDF['freq']))

for i, v in enumerate(posdf['freq']):
    fig.text(v + 3, i + .25, str(v), color='black', fontweight='bold', fontsize = pFntSz )
    
plt.savefig(os.path.join(dataResults, posWordFile), format= posFmt, dpi=posdpi, bbox_inches='tight',)
plt.show()


# Plot negative words
# Variables
negWordFile = "negWordsVader.svg"
negFmt = "svg"
negdpi = 600
negclr = ['darkred']
negtitle = 'Top 25 Negative Words, #Coronavirus: VADER'
nFigSz = (8,4)
nFntSz = 8

# plot

fig = negdf.plot(x= 'word',kind='barh', align='center', color = negclr, figsize = nFigSz, fontsize = nFntSz)
fig.set_ylabel('Words', fontsize = nFntSz)
fig.set_xlabel('Frequency', fontsize = nFntSz)
fig.set_title(negtitle, fontweight = 'bold', fontsize = nFntSz)
fig.set_ylim(fig.get_ylim()[::-1])
fig.set_xlim(0,1500 + max(freqDF['freq']))

for i, v in enumerate(negdf['freq']):
    fig.text(v + 3, i + .25, str(v), color='black', fontweight='bold', fontsize = nFntSz)

    

plt.savefig(os.path.join(dataResults, negWordFile), format=negFmt, dpi=negdpi, bbox_inches='tight',)

plt.show()


# ## VOILA!!

# This code was adapted from Stefan Sinclair's GitHub page called Art of Literary Text Analysis and can be found here: https://github.com/sgsinclair/alta/blob/e908bae2c224578485e10482e812924d7c6b7b05/ipynb/utilities/ComplexSentimentAnalysis.ipynb . Accessed 01/25/2019
