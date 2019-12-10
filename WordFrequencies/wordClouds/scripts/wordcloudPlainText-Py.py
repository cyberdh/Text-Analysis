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
import matplotlib.pyplot as plt
import re

# File paths saved as variables for use later in code
homePath = os.environ['HOME']
dataHome = os.path.join(homePath, "Text-Analysis-master", "data")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")
corpusRoot = os.path.join(dataHome, "shakespeareFolger")

# Variables for use later in the code.
singleDoc = False
nltkStop = True
customStop = True
stopLang = 'english'
stopWords = []

# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))

    stopWords.extend(['would', 'said', 'says', 'say', 'also', 'lord', 'good', 'come', 'let', 'speak', 'ay', 'hast'])

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

# Function for plotting wordcloud
def plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt):

    freq = defaultdict(int)

    for t in tokens:
        freq[t] += 1
    
    wc = wordcloud.WordCloud(background_color = bgc, max_words = maxWordCnt, colormap = cm, min_font_size=minFont)
    
    # generate word cloud
    wc.fit_words(freq)

    # show
    plt.figure(figsize = figSz)
    plt.imshow(wc, interpolation = 'bilinear')
    plt.axis("off")

    plt.tight_layout()
    
    # save graph as a png image to file
    plt.savefig(wcImgFilepath, format = fmt, dpi = dpi, bbox_inches = 'tight')
    
    plt.show()

# Function for creating a wordcloud from a single text
def drawWordCloudSingleText(textFilepath, wcImgFilepath, dpi, 
                                maxWordCnt):
    
    with open(textFilepath, "r", encoding="UTF-8") as f:
        text = f.read()

    tokens = textClean(text)
    
    plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt)

# Function for creating a wordcloud from multiple texts
def drawWordCloudCorpus(corpusRoot, wcImgFilepath, dpi, 
                          maxWordCnt):
   
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
    
    plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt)

#Variables
document = "Hamlet.txt"
wcOutputFile = "wordcloud.png"
fmt = "png"
bgc = "white"
cm = "Dark2"
dpi = 300
maxWordCnt = 500
minFont = 10
figSz = (40, 20)

if singleDoc is True:
    # Use case one, draw word cloud from a single text

    textFilepath = os.path.join(corpusRoot, document)

    # filepath to save word cloud image
    wcImgFilepath = os.path.join(dataResults, wcOutputFile)

    # Plot wordcloud from single text
    drawWordCloudSingleText(textFilepath, wcImgFilepath, dpi, maxWordCnt)
else:
    # Use case two, draw word cloud from a corpus root

    # filepath to save word cloud image
    wcImgFilepath = os.path.join(dataResults, wcOutputFile)

    # Plot wordcloud from Corpus
    drawWordCloudCorpus(corpusRoot, wcImgFilepath, dpi, maxWordCnt)

