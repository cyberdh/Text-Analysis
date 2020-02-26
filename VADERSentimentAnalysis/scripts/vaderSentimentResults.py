
# coding: utf-8

# Vader Sentiment Analysis Results

# Run CyberDH environment

# NOTE: This chunk of code is only for use with Research Desktop. You will get an error if you try to run this on your personal device!!
import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages 
import pickle
import pandas as pd
import os
import matplotlib.pyplot as plt
from collections import Counter
import math


# File paths
homePath = os.environ['HOME']
dataResults = os.path.join(homePath, "Text-Analysis-master","Output")
dataClean = os.path.join(homePath,"Text-Analysis-master","VADERSentimentAnalysis", "cleanedData")


# Load data
with open(os.path.join(dataClean, "vaderScores"), "rb") as vaderScore:
    res = pickle.load(vaderScore)
with open(os.path.join(dataClean, "total"), "rb") as vaderTotal:
    total = pickle.load(vaderTotal)
with open(os.path.join(dataClean, "scores"), "rb") as s:
    scores = pickle.load(s)
with open(os.path.join(dataClean, "numberOfText"), "rb") as nt:
    numberOfTweets = pickle.load(nt)
with open(os.path.join(dataClean, "squared"), "rb") as squared:
    totalSquared = pickle.load(squared)


print(res)


# Calcualte the `mean` and the standard deviation (`std`) of sentiment scores.
mean = total / numberOfTweets
std = math.sqrt(totalSquared / numberOfTweets) - mean**2


# Save the results of the `mean`, `std`, and `numberOfTweets` as a text file. 
with open(os.path.join(dataResults, 'VADERCombinedRawData.txt'), 'w') as write_file:
    write_file.write(str(res))
    write_file.write("\nMean: " + str(mean))
    write_file.write("\nStandard Deviation: " + str(std))
    write_file.write("\nNumber of Tweets: " +str(numberOfTweets))


# Plot the graph
# Variables
vaderBarOutput = 'vaderBarGraph.png'
fmt = 'png'
dpi = 300
color = ['red']
figSz = (10,5)
fontLabel = 18
fontTick = 10
fontPct = 8
labelX = 'Sentiment Score'
labelY = 'Number of Tweets'
labelTitle = 'Coronavirus VADER Overall Analysis: February 01, 2020 - February 07, 2020\n'
rotate = 45

# Plot graph   
cres = Counter(res)
resdf = pd.DataFrame.from_dict(cres, orient='index').reset_index()
resdf = resdf.rename(columns={'index':'score', 0:'count'})
total = resdf['count'].sum()

print(resdf)

fig = resdf.plot(x='score',kind='bar', align = 'center', color = color, grid = True, legend = None, figsize=figSz)
fig.set_ylabel(labelY, fontsize = fontLabel)
fig.set_xlabel(labelX, fontsize = fontLabel)
fig.set_title(labelTitle + 'Mean = {0:.2f}'.format(mean) + ', ' + 'Std = {0:.2f}'.format(std) +', ' + "Number of Tweets = {:,}".format(numberOfTweets),fontsize = fontLabel)
fig.set_ylim(0,2000 + max(res.values()))

rects = fig.patches

# vertical line for 0
zeroLine = plt.axvline(x = 10, color = 'black', linewidth = 2)

# vertical line for mean
meanLine = plt.axvline(x = mean*10+10, color = 'purple', linestyle = 'dashed', linewidth = 2)

plt.legend((zeroLine, meanLine), ['zero line', 'mean line'], prop={'size' : fontLabel}, loc = 'upper right')

# Now make some labels

plt.tick_params(axis = 'both', which = 'major', labelsize = fontTick)

labels =round((resdf['count']/total) * 100, 2).astype(str)+'%'

for rect, label in zip(rects, labels):
    height = rect.get_height()
    fig.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='left', fontsize = fontPct, va='bottom', rotation = rotate)
    
plt.savefig(os.path.join(dataResults,vaderBarOutput), format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()


# ## VOILA!!

# Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
