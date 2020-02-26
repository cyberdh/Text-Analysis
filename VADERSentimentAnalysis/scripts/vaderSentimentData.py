
# coding: utf-8

# Vader Sentiment Analysis
# ### Run CyberDH environment
# NOTE: This chunk of code is only for use with Research Desktop. You will get an error if you try to run this on your personal device!!
import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pickle
import pandas as pd
import os
import glob
import zipfile

# Variables
source = "coronaVirus01-21Jan2020"
fileType = ".json"
textColIndex = "text"
encoding = "utf-8"
errors = "ignore"
scores = []
total = 0
numberOfTweets = 0
totalSquared = 0

# File paths
homePath = os.environ['HOME']
dataHome = os.path.join(homePath, "Text-Analysis-master","data","twitter")
dataClean = os.path.join(homePath,"Text-Analysis-master","VADERSentimentAnalysis", "cleanedData")

# Shorten SentimentIntensityAnalyzer Function
vader = SentimentIntensityAnalyzer()

# Unzip files
if fileType == ".csv":
    direct = os.path.join(dataHome, "CSV")
    allZipFiles = glob.glob(os.path.join(dataHome, "CSV","*.zip"))
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
    allFiles = glob.glob(os.path.join(dataHome, "CSV", source + fileType))     
    df = (pd.read_csv(f, engine = "python") for f in allFiles)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf)
    tweets = cdf[textColIndex].values.tolist()
if fileType == ".json":
    allFiles = glob.glob(os.path.join(dataHome, "JSON", source + fileType))     
    df = (pd.read_json(f, encoding = encoding, lines = True) for f in allFiles)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf)
    tweets = cdf[textColIndex].values.tolist()

# Check tweets
rtDF = pd.DataFrame(tweets)
print(rtDF.head(10))

# Create labels
res = {"-1":0, "-.9":0, "-.8":0, "-.7":0, "-.6":0, "-.5":0, "-.4":0, "-.3":0, "-.2":0, "-.1":0, "0":0, ".1":0, ".2":0,".3":0, ".4":0, ".5":0, ".6":0, ".7":0, ".8":0, ".9":0, "1":0}

# Apply the Vader sentiment analyzer
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

# Export data
with open(os.path.join(dataClean, "vaderScores"), "wb") as vaderScore:
    pickle.dump(res, vaderScore)
with open(os.path.join(dataClean, "total"), "wb") as vaderTotal:
    pickle.dump(total, vaderTotal)
with open(os.path.join(dataClean, "scores"), "wb") as s:
    pickle.dump(scores, s)
with open(os.path.join(dataClean, "numberOfText"), "wb") as nt:
    pickle.dump(numberOfTweets, nt)
with open(os.path.join(dataClean, "squared"), "wb") as squared:
    pickle.dump(totalSquared, squared)


# Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
