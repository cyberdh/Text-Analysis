# Point to Cyber DH Python Environment
import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"

# Import additional packages
from nltk.corpus import stopwords
import string
from collections import defaultdict
import wordcloud
import matplotlib.pyplot as plt
import re
import pandas as pd
import glob
import zipfile


# Set needed variables. 
fileType = ".json"
singleDoc = True
nltkStop = True
customStop = True
stopLang = stopwords.fileids()
encoding = "utf-8"
errors = "ignore"
stopWords = []

# File paths saved as variables for later use.
homePath = os.environ['HOME']
dataHome = os.path.join(homePath, "Text-Analysis-master", "data")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")
if fileType == ".csv":
    dataRoot = os.path.join(dataHome, "twitter", "CSV")
else:
    dataRoot = os.path.join(dataHome, "twitter", "JSON")


# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))
    
    stopWords.extend(['pic', 'com', 'coronavirus', 'twitter'])


# Add own stopword list
if customStop is True:
    stopWordsFilepath = os.path.join(dataHome, "twitterStopword.txt")

    with open(stopWordsFilepath, "r",encoding = 'utf-8') as stopfile:
        stopWordsCustom = [x.strip() for x in stopfile.readlines()]

    stopWords.extend(stopWordsCustom)

# Function for cleaning tweets
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

# unzip files
direct = dataRoot
allZipFiles = glob.glob(os.path.join(dataRoot, "*.zip"))
for item in allZipFiles:
    fileName = os.path.splitext(direct)[0]
    zipRef = zipfile.ZipFile(item, "r")
    zipRef.extractall(fileName)
    zipRef.close()
    os.remove(item)

# Function for plotting wordcloud
def plotWordCloud(tokens, wcImgFilepath, dpi,  maxWordCnt):

    freq = defaultdict(int)

    for t in tokens:
        freq[t] += 1

    wc = wordcloud.WordCloud(font_path = "/usr/share/fonts/thai-scalable/Waree.ttf",background_color = bgc, width = width, height = height, max_words = maxWordCnt, colormap = cm, min_font_size=minFont)
    

    # generate word cloud
    wc.fit_words(freq)

    # store to file
    wc.to_file(wcImgFilepath)

    # show
    plt.figure(figsize = figSz)
    plt.imshow(wc, interpolation = 'bilinear')
    
    plt.axis("off")

    plt.tight_layout()
    
    # save graph as a png image to file
    plt.savefig(wcImgFilepath, format = fmt, dpi = dpi, bbox_inches = 'tight')
    plt.show()

# Function to read in a file
def readTweets(filepath, textColIndex, encoding = encoding, errors = errors):
    if fileType == ".csv":
        tweet = pd.read_csv(filepath, encoding = encoding)
    else:
        tweet = pd.read_json(filepath, encoding = encoding, lines = True)
    
    content = tweet[textColIndex].tolist()
    
    return content[1 : ]


# Function to create wordcloud from a single file
def drawWordCloudFile(dataFilepath, textColIndex, encoding, errors, 
                               wcImgFilepath, dpi,  maxWordCnt):
    
    content = readTweets(dataFilepath, textColIndex, encoding, errors)
    
    text = '\n'.join(content)
    
    tokens = textClean(text)
    
    plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt)
    

# Function to create wordcloud from multiple files
def drawWordCloudDirectory(dataRoot, textColIndex, encoding, errors, 
                             wcImgFilepath, dpi,  maxWordCnt):
   
    tokens = []
    
    for root, subdirs, files in os.walk(dataRoot):
        
        for filename in files:
            
            # skip hidden file
            if filename.startswith('.'):
                continue
            
            dataFilepath = os.path.join(root, filename)
            
            content = readTweets(dataFilepath, textColIndex, encoding, errors)
            text = '\n'.join(content)
            tokens.extend(textClean(text))
                
            print('Finished tokenizing text {}\n'.format(dataFilepath))
    
    plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt)


# Plot Wordcloud
#Variables

document = "coronaVirus01-21Jan2020" + fileType
wcOutputFile = "wordcloud.png"
fmt = "png"
width = 800
height = 400
textColIndex = "text"
bgc = "white"
cm = "Dark2"
dpi = 1200
maxWordCnt = 500
minFont = 12
figSz = (10,5)

if singleDoc is True:
    # Use case one, draw word cloud from a single text

    dataFilepath = os.path.join(dataRoot, document)

    # filepath to save word cloud image
    wcImgFilepath = os.path.join(dataResults, wcOutputFile)

    # Plot wordcloud from single file  
    drawWordCloudFile(dataFilepath, textColIndex, encoding, errors, 
                               wcImgFilepath, dpi,  maxWordCnt)
else:
    # Use case two, draw word cloud from a corpus root

    # filepath to save word cloud image
    wcImgFilepath = os.path.join(dataResults, wcOutputFile)

    # Plot wordlcoud from directory
    drawWordCloudDirectory(dataRoot, textColIndex, encoding, errors, 
                             wcImgFilepath, dpi,  maxWordCnt)

