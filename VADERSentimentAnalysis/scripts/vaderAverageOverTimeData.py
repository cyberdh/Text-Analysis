
# coding: utf-8

# Vader Sentiment Analysis Average Over Time Data Prep
 
# Run CyberDH environment

# NOTE: The below code is only for use with Research Desktop. 
# You will get an error if you try to run this code on your personal device!!

import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"

# Include necessary packages for notebook 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import glob
import zipfile

# Variables
source = "coronaVirus01-21Jan2020"
fileType = ".json"
textColIndex = "text"
timeLength = "D"
remove = True
remWords = ["novel", "ha", "l", "gt", "positive"]
add = True
newWords = {"virus": -1.7, "outbreak": -0.6, "epidemic": -2.3, "pandemic": -3.1, "quarantine": -2.6, "positive": -2.6}
encoding = "utf-8"

# File paths
homePath = os.environ['HOME']
dataHome = os.path.join(homePath,'Text-Analysis-master', 'data', 'twitter')
dataClean = os.path.join(homePath,"Text-Analysis-master","VADERSentimentAnalysis", "cleanedData")

# Shorten SentimentIntensityAnalyzer Function
vader = SentimentIntensityAnalyzer()

# Remove words
if remove == True:
    [vader.lexicon.pop(x) for x in remWords]
else:
    None

# Add words
if add == True:
    vader.lexicon.update(newWords)
else:
    None

# Unzip files
if fileType == ".json":
    direct = os.path.join(dataHome, "JSON")
    allZipFiles = glob.glob(os.path.join(dataHome, "JSON","*.zip"))
    for item in allZipFiles:
            fileName = os.path.splitext(direct)[0]
            zipRef = zipfile.ZipFile(item, "r")
            zipRef.extractall(fileName)
            zipRef.close()
            os.remove(item)    
else:
    direct = os.path.join(dataHome, "CSV")
    allZipFiles = glob.glob(os.path.join(dataHome, "CSV","*.zip"))
    for item in allZipFiles:
            fileName = os.path.splitext(direct)[0]
            zipRef = zipfile.ZipFile(item, "r")
            zipRef.extractall(fileName)
            zipRef.close()
            os.remove(item)

# Reading in .csv and .json files
if fileType == ".json":
    allFiles = glob.glob(os.path.join(dataHome,"JSON",source + fileType))     
    df = (pd.read_json(f, encoding = encoding, lines = True) for f in allFiles)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf)
if fileType == ".csv":
    allFiles = glob.glob(os.path.join(dataHome, "CSV", source + fileType))     
    df = (pd.read_csv(f, engine = "python") for f in allFiles)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf)
cdf["text"] = cdf["text"].astype(str)
print(len(cdf["text"]))

# Run VADER
sentiment = cdf['text'].apply(lambda x: vader.polarity_scores(x))
cdf = pd.concat([cdf,sentiment.apply(pd.Series)],1)
cdf.head(5)

# Get dates
cdf.sort_values(by="created_at", inplace=True)

if fileType == ".csv":
    cdf["created_at"] = cdf["created_at"].astype(str).str[:-6]
else:
    None

cdf["created_at"] = pd.to_datetime(cdf["created_at"])
cdf = cdf.dropna(subset=["created_at"])
cdf.index = cdf["created_at"]
cdf.index.names = ["dateTime"]
cdf.head(5)

# Create data frames and export data
meanDF = cdf.groupby(pd.Grouper(freq = timeLength))["compound"].mean().fillna(0).sort_index().reset_index()
meanDF.columns = ["date", "mean"]
meanDF.to_csv(os.path.join(dataClean, "vaderAvg.csv"))
meanDF.head(5)


countDF = cdf.groupby(pd.Grouper(freq = timeLength))["compound"].count().sort_index().reset_index()
countDF.columns = ["date", "count"]
countDF.to_csv(os.path.join(dataClean, "tweetCount.csv"))
countDF.head(5)


# ## VOILA!!

# Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
