# Run CyberDH environment

# NOTE: This chunk of code is only for use with Research Desktop. You will get an error if you try to run this code on your personal device!!

import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# ### Include necessary packages for notebook 

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
#import numpy as np
import os
#import csv
#import json
import glob
import zipfile
import matplotlib.pyplot as plt
from collections import Counter
import math


# Variables

source = "iranTweets"
fileType = ".json"
textColIndex = "text"
encoding = "utf-8"
scores = []
total = 0
numberOfTweets = 0
totalSquared = 0


# File paths

homePath = os.environ['HOME']
dataHome = os.path.join(homePath, "Text-Analysis-master","data","twitter")
dataResults = os.path.join(homePath,"Text-Analysis-master","Output")


# Shorten SentimentIntensityAnalyzer Function

vader = SentimentIntensityAnalyzer()


# Unzip files

if fileType == ".csv":
    direct = os.path.join(dataHome, "CSV", "Iran")
    allZipFiles = glob.glob(os.path.join(dataHome, "CSV", "Iran","*.zip"))
    for item in allZipFiles:
            fileName = os.path.splitext(direct)[0]
            zipRef = zipfile.ZipFile(item, "r")
            zipRef.extractall(fileName)
            zipRef.close()
            os.remove(item)
else:
    direct = os.path.join(dataHome, "JSON")
    allZipFiles = glob.glob(os.path.join(dataHome, "JSON","*.zip"))
    for item in allZipFiles:
            fileName = os.path.splitext(direct)[0]
            zipRef = zipfile.ZipFile(item, "r")
            zipRef.extractall(fileName)
            zipRef.close()
            os.remove(item)


# Reading in .csv and JSON files

if fileType == ".csv":
    allFiles = glob.glob(os.path.join(dataHome, "CSV", "Iran", source + fileType))     
    df = (pd.read_csv(f, engine = "python") for f in allFiles)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf)
    tweets = cdf[textColIndex].values.tolist()
if fileType == ".json":
    allFiles = glob.glob(os.path.join(dataHome, "JSON", source + fileType))     
    df = (pd.read_json(f, encoding = encoding) for f in allFiles)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf)
    tweets = cdf[textColIndex].values.tolist()


# Now we check to see if we have pulled our tweets from our dataset. We are just checking the first 10 tweets.

rtDF = pd.DataFrame(tweets)
rtDF.head(10)


# Create labels for different sentiment values and start the count for each value at zero

res = {"-1":0, "-.9":0, "-.8":0, "-.7":0, "-.6":0, "-.5":0, "-.4":0, "-.3":0, "-.2":0, "-.1":0, "0":0, ".1":0, ".2":0,".3":0, ".4":0, ".5":0, ".6":0, ".7":0, ".8":0, ".9":0, "1":0}


# Go through and apply the Vader sentiment analyzer to all tweets and count them

for index, row in rtDF.iterrows():
    vs = vader.polarity_scores(str(rtDF.iloc[:,0][index]))
    scores.append(vs['compound'])
    total += vs["compound"]
    numberOfTweets += 1
    totalSquared += vs["compound"]**2
    if vs["compound"]==0.0:
        res["0"] +=1
    elif 0 < vs["compound"] <= 0.1:
        res[".1"] +=1
    elif 0.1 <= vs["compound"] <= 0.2:
        res[".2"] +=1
    elif 0.2 < vs["compound"] <= 0.3:
        res[".3"] +=1
    elif 0.3 < vs["compound"] <= 0.4:
        res[".4"] +=1
    elif 0.4 < vs["compound"] <= 0.5:
        res[".5"] +=1
    elif 0.5 < vs["compound"] <= 0.6:
        res[".6"] +=1
    elif 0.6 < vs["compound"] <= 0.7:
        res[".7"] +=1
    elif 0.7 < vs["compound"] <= 0.8:
        res[".8"] +=1
    elif 0.8 < vs["compound"] <= 0.9:
        res[".9"] +=1
    elif 0.9 < vs["compound"] <= 1:
        res["1"] +=1
    elif 0 > vs["compound"] >= -0.1:
        res["-.1"] +=1
    elif -0.1 > vs["compound"] >= -0.2:
        res["-.2"] +=1
    elif -0.2 > vs["compound"] >= -0.3:
        res["-.3"] +=1
    elif -0.3 > vs["compound"] >= -0.4:
        res["-.4"] +=1
    elif -0.4 > vs["compound"] >= -0.5:
        res["-.5"] +=1
    elif -0.5 > vs["compound"] >= -0.6:
        res["-.6"] +=1
    elif -0.6 > vs["compound"] >= -0.7:
        res["-.7"] +=1
    elif -0.7 > vs["compound"] >= -0.8:
        res["-.8"] +=1
    elif -0.8 > vs["compound"] >= -0.9:
        res["-.9"] +=1
    elif -0.9 > vs["compound"] >= -1:
        res["-1"] +=1

print(res)



# Now we use the math package to calcualte the `mean` and the standard deviation (`std`) of our sentiment scores.

mean = total / numberOfTweets
std = math.sqrt(totalSquared / numberOfTweets) - mean**2


# Here we save the results of the `mean`, `std`, and `numberOfTweets` as a text file.

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
labelTitle = 'Iran VADER Overall Analysis: January 01, 2020 - January 04, 2020\n'
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
meanLine = plt.axvline(x = mean+10, color = 'purple', linestyle = 'dashed', linewidth = 2)

plt.legend((zeroLine, meanLine), ['zero line', 'mean line'], prop={'size' : fontLabel}, loc = 'upper right')

# Now make some labels

plt.tick_params(axis = 'both', which = 'major', labelsize = fontTick)

labels =round((resdf['count']/total) * 100, 2).astype(str)+'%'

for rect, label in zip(rects, labels):
    height = rect.get_height()
    fig.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='left', fontsize = fontPct, va='bottom', rotation = rotate)
    
plt.savefig(os.path.join(dataResults,vaderBarOutput), format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()


# Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
