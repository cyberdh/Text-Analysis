from nltk.corpus import stopwords
import os
import string
from collections import defaultdict
import wordcloud
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import re
import operator
import csv


stop_words = stopwords.words('english')
stop_words.extend(['amp','rt', 'xo_karmin_ox', 'neveragain', 'ð', 'â', 'ï', 'emma4change'])



def textClean(text, stopWordsList = None):
    
    text = text.strip().lower()
    
    tweets = re.sub(r"http\S+", "", text)
    
    tokens = re.split(r'\W+', tweets )
    
    # remove empty string
    tokens = [t for t in tokens if t]
    
    # remove digits
    tokens = [t for t in tokens if not t.isdigit()]
    
    # built-in stop words list
    tokens = [t for t in tokens if t not in stop_words]
    
    # custom stop words list
    if stopWordsList is not None:
        tokens = [t for t in tokens if t not in stopWordsList]
        
    # remove punctuation
    puncts = list(string.punctuation)
    puncts.append('--')

    tokens = [t for t in tokens if t not in puncts]

    return tokens




def plotWordCloud(tokens, wcImgFilepath, dpi,  maxWordCnt, maskFilepath = None):

    freq = defaultdict(int)

    for t in tokens:
        freq[t] += 1
        
    if maskFilepath is not None:
        mask = np.array(Image.open(maskFilepath))
    else:
        mask = None

    wc = wordcloud.WordCloud(background_color = "white", scale=4, colormap='Dark2_r', max_words = maxWordCnt, mask = mask)
    

    # generate word cloud
    wc.fit_words(freq)

    # store to file
    wc.to_file(wcImgFilepath)

    # show
    plt.figure(figsize = (20, 10))
    plt.imshow(wc, interpolation = 'bilinear')
    
    plt.axis("off")

    plt.tight_layout()
    
    # save graph as a png image to file
    plt.savefig(wcImgFilepath, format = 'png', dpi = dpi, bbox_inches = 'tight')
    plt.show()
    
    
    
def readCSV(filepath, textColIndex, encoding = 'utf-8', errors = 'ignore'):
    
    with open(filepath, encoding = encoding, errors = errors) as f:
        
        reader = csv.reader(f, delimiter = ',', quotechar = '"')
        
        content = []
        for row in reader: 
            content.append(row[textColIndex])
         
        # skip header
        return content[1 : ]
    
    
    
def drawWordCloudFromSingleCSV(csvFilepath, textColIndex, encoding, errors, 
                               stopWordsList, wcImgFilepath, dpi,  maxWordCnt, maskFilepath = None):
    
    content = readCSV(csvFilepath, textColIndex, encoding, errors)
    
    text = '\n'.join(content)
    
    tokens = textClean(text, stopWordsList)
    
    plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt, maskFilepath)
    
    
    
def drawWordCloudFromScanCSV(csvRoot, textColIndex, encoding, errors, stopWordsList, 
                             wcImgFilepath, dpi,  maxWordCnt, maskFilepath = None):
   
    tokens = []
    
    for root, subdirs, files in os.walk(csvRoot):
        
        for filename in files:
            
            # skip hidden file
            if filename.startswith('.'):
                continue
            
            textFilepath = os.path.join(root, filename)
            
            content = readCSV(textFilepath, textColIndex, encoding, errors)
            text = '\n'.join(content)
            tokens.extend(textClean(text, stopWordsList))
                
            print('Finished tokenizing text {}\n'.format(textFilepath))
    
    plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt, maskFilepath)
    
    
    
# load custom stop words list

stopWordsFilepath = '/N/u/klosteda/Carbonate/Text-Analysis/data/earlyModernStopword.txt'

csvRoot = '/N/u/klosteda/Carbonate/Text-AnalysisBox/data/twitter/parkland'

with open(stopWordsFilepath, "r") as f:
    stopWordsList = f.readlines()
            
stopWordsList = [w.strip().lower() for w in stopWordsList]



# Use case one, draw word cloud from a single tweet csv

csvFilepath = os.path.join(csvRoot,'neverAgain.csv')

textColIndex = 2

encoding = 'utf-8'

errors = 'ignore'

wcImgFilepath = '/N/u/klosteda/Carbonate/Text-Analysis/Output/wordcloudTwitterNeverAgain.png'

dpi = 300

# As an option, user can provision a mask related to the text theme
maskFilepath = '/N/u/klosteda/Carbonate/Text-Analysis/data/wordcloudMasks/Fist.png'

maxWordCnt = 500

drawWordCloudFromSingleCSV(csvFilepath, textColIndex, encoding, errors, 
                               stopWordsList, wcImgFilepath, dpi, maxWordCnt, maskFilepath)




"""
# Use case two, draw word cloud from a corpus root

textColIndex = 2

encoding = 'utf-8'

errors = 'ignore'

wcImgFilepath = '/N/u/klosteda/Carbonate/Text-Analysis/Output/wordcloudTwitterPolitical.png'

dpi = 300
# As an option, user can provision a mask related to the text theme
maskFilepath = '/N/u/klosteda/Carbonate/Text-Analysis/data/wordcloudMasks/USA.png'
maxWordCnt = 100

drawWordCloudFromScanCSV(csvRoot, textColIndex, encoding, errors, stopWordsList, wcImgFilepath, dpi, maxWordCnt, maskFilepath)
"""

