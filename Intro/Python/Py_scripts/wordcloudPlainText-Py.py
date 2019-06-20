# Points to Cyber DH Python Environment
import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"

# Import remaining packages
from nltk.corpus import stopwords
import string
from collections import defaultdict
import wordcloud
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import re



# File paths saved as variables for use later in code
homePath = os.environ['HOME']
dataHome = os.path.join(homePath, "Text-Analysis-master", "data")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")
corpusRoot = os.path.join(dataHome, "shakespeareFolger")

# Variables for use later in the code. If you wish to see nltk stopword languages, remove '#' from in front of print.
singleDoc = False
nltkStop = True
customStop = True
stopLang = 'english'
stopWords = []

#print(" ".join(stopwords.fileids()))


# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))

    stopWords.extend(['would', 'said', 'says', 'also', 'lord', 'good', 'come'])


# Custom stop words
if customStop is True:
    stopWordsFilepath = os.path.join(dataHome, "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = 'utf-8') as stopfile:
        stopWordsCustom = [x.strip() for x in stopfile.readlines()]

    stopWords.extend(stopWordsCustom)


# Text cleaning function
def textClean(text):
    
    text = text.strip().lower()
    
    tokens = re.split(r'\W+', text)
    
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

# Function for ploting wordcloud
def plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt, maskFilepath = None):

    freq = defaultdict(int)

    for t in tokens:
        freq[t] += 1
        
    if maskFilepath is not None:
        mask = np.array(Image.open(maskFilepath))
    else:
        mask = None
    

    wc = wordcloud.WordCloud(background_color = "white", max_words = maxWordCnt, mask = mask, colormap = 'Dark2')
    

    # generate word cloud
    wc.fit_words(freq)

    # show
    plt.figure(figsize = (60, 20))
    plt.imshow(wc, interpolation = 'bilinear')
    plt.axis("off")

    plt.tight_layout()
    
    # save graph as a png image to file
    plt.savefig(wcImgFilepath, format = 'png', dpi = dpi, bbox_inches = 'tight')
    
    plt.show()


# Function for creating a wordcloud from a single text
def drawWordCloudFromSingleText(textFilepath, wcImgFilepath, dpi, 
                                maxWordCnt, maskFilepath = None):
    
    with open(textFilepath, "r", encoding="UTF-8") as f:
        text = f.read()

    tokens = textClean(text)
    
    plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt, maskFilepath)


# Function for creating a wordcloud from multiple texts
def drawWordCloudFromScan(corpusRoot, wcImgFilepath, dpi, 
                          maxWordCnt, maskFilepath = None):
   
    tokens = []
    
    for root, subdirs, files in os.walk(corpusRoot):
        
        for filename in files:
            
            # skip hidden file
            if filename.startswith('.'):
                continue
            
            textFilepath = os.path.join(root, filename)
            
            with open(textFilepath, "r") as f:
                text = f.read()
                tokens.extend(textClean(text))
    
    plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt, maskFilepath)


#Variables
document = "Hamlet.txt"
wcOutputFile = "wordcloud.png"
dpi = 300
maxWordCnt = 500
useMask = True
maskPath = os.path.join(dataHome,'wordcloudMasks','Shakespeare.png')


if singleDoc is True:
    # Use case one, draw word cloud from a single text

    textFilepath = os.path.join(corpusRoot, document)

    # filepath to save word cloud image
    wcImgFilepath = os.path.join(dataResults, wcOutputFile)

    # As an option, user can provision a mask related to the text theme
    if useMask is True:
        
        drawWordCloudFromSingleText(textFilepath, wcImgFilepath, dpi, maxWordCnt, maskFilepath = maskPath)
    else:
        maskFilepath = None
        
        drawWordCloudFromSingleText(textFilepath, wcImgFilepath, dpi, maxWordCnt, maskFilepath = maskFilepath)
else:
    # Use case two, draw word cloud from a corpus root

    # filepath to save word cloud image
    wcImgFilepath = os.path.join(dataResults, wcOutputFile)

    # As an option, user can provision a mask related to the text theme
    if useMask is True:
        
        drawWordCloudFromScan(corpusRoot, wcImgFilepath, dpi, maxWordCnt, maskFilepath = maskPath)
    else:
        maskFilepath = None
        
        drawWordCloudFromScan(corpusRoot, wcImgFilepath, dpi, maxWordCnt, maskFilepath = maskFilepath)

