
# coding: utf-8

# Complex Sentiment Analysis

# Run CyberDH environment
# 
# #### NOTE: This chunk of code is only for use with Research Desktop. You will get an error if you try to run this on your personal device!!
import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages 
import pandas as pd
import re
import glob
import nltk
from collections import Counter
import zipfile


# Variables
source = "iranTweets"
fileType = ".json"
negColHead = 'Neg'
posColHead = 'Pos'
tweetColHead = 'text'
encoding = "utf-8"
remNegWords = []
negAdds = []
remPosWords = ['3']
posAdds = []


# File paths
homePath = os.environ['HOME']
dataHome = os.path.join(homePath, 'Text-Analysis-master','data','twitter')
dataClean = os.path.join(homePath, 'Text-Analysis-master', 'VADERSentimentAnalysis', 'cleanedData')
negFile = glob.glob(os.path.join(dataHome, "dict", "negativeVADER.csv"))
posFile = glob.glob(os.path.join(dataHome, "dict", "positiveVADER.csv"))


# Load the negative words
for f in negFile:
    negText = pd.read_csv(f, index_col = False)

negDf = pd.DataFrame(negText)
negTokens = negDf[negColHead].tolist()
 
negTokens.extend(negAdds)
for word in list(negTokens):
    if word in remNegWords: 
        negTokens.remove(word)
print(negTokens[-10:])

# list to set for efficient lookup
negTokens = set(negTokens)


# Load the positive words
for f in posFile:
    posText = pd.read_csv(f, index_col = False)

posDf = pd.DataFrame(posText)
posTokens = posDf[posColHead].tolist()
posTokens.extend(posAdds)
for word in list(posTokens):
    if word in remPosWords: 
        posTokens.remove(word)
#if 'right' in posTokens: posTokens.remove('right')
print(posTokens[-10:])

# list to set for efficient lookup
posTokens = set(posTokens)


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


# Reading in .csv and .json files
if fileType == ".csv":
    allFiles = glob.glob(os.path.join(dataHome, "CSV", "Iran", source + fileType))     
    df = (pd.read_csv(f, engine = "python") for f in allFiles)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf, dtype = 'str')
    tweetsTokens = cdf[tweetColHead].values.tolist()
if fileType == ".json":
    allFiles = glob.glob(os.path.join(dataHome, "JSON", source + fileType))     
    df = (pd.read_json(f, encoding = encoding) for f in allFiles)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf, dtype = 'str')
    tweetsTokens = cdf[tweetColHead].values.tolist()    
print(len(tweetsTokens)) 


# Functions
# Tokenizing the tweets
def tokenizer(theText):
    theTokens = re.findall(r'\b\w[\w-]*\b', theText.lower())
    return theTokens

def calculator(theTweet, posTokenList, negTokenList):
    
    posWordsList = []
    negWordsList = []

    numPosWords = 0 
    numNegWords = 0
    
    theTweetTokens = tokenizer(theTweet)
    
    # Count positive and negative words
    for word in theTweetTokens:
        if word in posTokenList:
            numPosWords += 1
            posWordsList.append(word)
        
        if word in negTokenList:
            numNegWords += 1
            negWordsList.append(word)
        
        
    score = (numPosWords - numNegWords)
    return {'score': score, 'posWordsList' : posWordsList, 'negWordsList' : negWordsList}


# Analyzing tweets
# do all calculation once
results = []

for tweet in tweetsTokens:
    results.append(calculator(tweet, posTokens, negTokens))
    
scores = [x['score'] for x in results]

posWordsList = [x['posWordsList'] for x in results]
posWordsList = [item for sublist in posWordsList for item in sublist]

negWordsList = [x['negWordsList'] for x in results]
negWordsList = [item for sublist in negWordsList for item in sublist]

# Here we set up the thresholds
posi = 0 # This means there have to be at least 1 positive word
nega = 0 # This means there has to be at least 1 negative words

# Here we prime our variables
numTweets = len(results)
numPosTweets = 0
numNegTweets = 0
numNeutTweets = 0

# This loop goes through all the Tweets and calculates number of positive, negative, and neutral ones.
for score in scores:
    if score > posi:
        numPosTweets += 1
       
    elif score < nega:
        numNegTweets += 1
        
    else:
        numNeutTweets += 1
        

# This prints out the results 
print("Total: " + str(numTweets) + "\n" + "Positive: " + str(numPosTweets) + "\n" + "Neutral: " + str(numNeutTweets) + "\n" + "Negative: " +str(numNegTweets))


# Gathering positive tweets
# Here we set up the threshold.
posi = 1 # This means there have to be more than 1 positive word
numberWanted = 4 # Here you decide how many tweets you want

# Here we prime our variables
numTweets = len(results)
numPosTweets = 0
posiTweetList = []


for idx, score in enumerate(scores):
    if score > posi:
        posiTweetList.append(tweetsTokens[idx])
        numPosTweets += 1
        
        if numPosTweets >= numberWanted:
            break

#print(posiTweetList)


# Gathering negative tweets
# Here we set up the threshold.
nega = -1 # This means there have to be more than 1 negative word
numberWanted = 4 # Here you decide how many tweets you want

# Here we prime our variables
numTweets = len(results)
numNegTweets = 0
negaTweetList = []


for idx, score in enumerate(scores):
    if score < nega:
        negaTweetList.append(tweetsTokens[idx])
        numNegTweets += 1
        
        if numNegTweets >= numberWanted:
            break
        

#print(negaTweetList)


# Testing a tweet


tweetToCalc = input("What is the tweet to calculate? ")
res = calculator(tweetToCalc, posTokens, negTokens)
print(res['score'])



tweet2Process = input("What tweet do you want to process? ")
res = calculator(tweet2Process, posTokens, negTokens)
print("Positive words: " + str(res['posWordsList'][:10]))
print("Negative words: " + str(res['negWordsList'][:10]))


# Gathering all positive and negative words
# Gathering and counting positive and negative words
print("Positive words: " + str(len(posWordsList)))
print("Negative words: " + str(len(negWordsList)))


# Count number of times positive words occur
posDist = nltk.FreqDist(posWordsList)
posit = Counter(posDist)
positdf = pd.DataFrame.from_dict(posit, orient='index').reset_index()
positdf = positdf.rename(columns={'index':'word', 0:'freq'})
positdf = positdf.sort_values('freq', ascending = False)
positdf.to_csv(os.path.join(dataClean, "posWords.csv"))


# Count number of times negative words occur
negDist = nltk.FreqDist(negWordsList)
nega = Counter(negDist)
negadf = pd.DataFrame.from_dict(nega, orient='index').reset_index()
negadf = negadf.rename(columns={'index':'word', 0:'freq'})
negadf = negadf.sort_values('freq', ascending = False)
negadf.to_csv(os.path.join(dataClean, "negWords.csv"))


# This code was adapted from Stefan Sinclair's GitHub page called Art of Literary Text Analysis and can be found here: https://github.com/sgsinclair/alta/blob/e908bae2c224578485e10482e812924d7c6b7b05/ipynb/utilities/ComplexSentimentAnalysis.ipynb . Accessed 01/25/2019
