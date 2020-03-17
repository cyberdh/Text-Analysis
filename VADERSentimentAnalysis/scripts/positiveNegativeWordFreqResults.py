
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
import plotly as py
import plotly.express as px


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
posWordFile = "posWordsVader"
posFmt = ".html"
pFntClr = "black"
pFntSz = 10
posclr = ["darkgreen"]
pXlabel = "Frequency"
pYlabel = "Word"
postitle = 'Top 25 Positive Words, #Coronavirus: January 01-21, 2020; VADER'
pWide = 800
pTall = 500
pXlimit = [0, 1000+max(freqDF['freq'])]

# Plot
figP = px.bar(posdf, x="freq", y="word", orientation="h", 
              title=postitle, color_discrete_sequence = posclr, 
              labels = {"freq":pXlabel,"word":pYlabel})
figP.update_layout(width = pWide, height = pTall, title={'y':0.90, 'x':0.5, 'xanchor': 'center', 'yanchor':'top'}, 
                  font={"color": pFntClr, "size":pFntSz})
figP.update_yaxes(autorange = "reversed")
figP.update_xaxes(range = pXlimit)

py.offline.plot(figP, filename = os.path.join(dataResults, posWordFile + posFmt), auto_open=False)
figP.show()


# Plot negative words
# Variables
negWordFile = "negWordsVader"
negFmt = ".html"
nFntClr = "black"
nFntSz = 10
negclr = ["crimson"]
nXlabel = "Frequency"
nYlabel = "Word"
negtitle = 'Top 25 Negative Words, #Coronavirus: January 01-21, 2020; VADER'
nWide = 800
nTall = 500
nXlimit = [0, 1000+max(freqDF['freq'])]

# Plot
figN = px.bar(negdf, x="freq", y="word", orientation="h", 
              title=negtitle, color_discrete_sequence = negclr, 
              labels = {"freq":nXlabel,"word":nYlabel})
figN.update_layout(width = nWide, height = nTall, title={'y':0.90, 'x':0.5, 'xanchor': 'center', 'yanchor':'top'}, 
                  font={"color": nFntClr, "size":nFntSz})
figN.update_yaxes(autorange = "reversed")
figN.update_xaxes(range = nXlimit)

py.offline.plot(figN, filename = os.path.join(dataResults, negWordFile + negFmt), auto_open=False)
figN.show()


# ## VOILA!!

# This code was adapted from Stefan Sinclair's GitHub page called Art of Literary Text Analysis and can be found here: https://github.com/sgsinclair/alta/blob/e908bae2c224578485e10482e812924d7c6b7b05/ipynb/utilities/ComplexSentimentAnalysis.ipynb . Accessed 01/25/2019
