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



stop_words = stopwords.words('english')
stop_words.extend(['good','come', 'would'])



def textClean(text, stopWordsList = None):
    
    text = text.strip().lower()
    
    tokens = re.split(r'\W+', text)
    
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
    plt.figure(figsize = (20, 10))
    plt.imshow(wc, interpolation = 'bilinear')
    plt.axis("off")

    plt.tight_layout()
    
    # save graph as a png image to file
    plt.savefig(wcImgFilepath, format = 'png', dpi = dpi, bbox_inches = 'tight')
    
    plt.show()
    
    


def drawWordCloudFromSingleText(textFilepath, stopWordsList, wcImgFilepath, dpi, 
                                maxWordCnt, maskFilepath = None):
    
    with open(textFilepath, "r") as f:
        text = f.read()

    tokens = textClean(text, stopWordsList)
    
    plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt, maskFilepath)




def drawWordCloudFromScan(corpusRoot, stopWordsList, wcImgFilepath, dpi, 
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
                tokens.extend(textClean(text, stopWordsList))
                
                print('Finished tokenizing text {}\n'.format(textFilepath))
    
    plotWordCloud(tokens, wcImgFilepath, dpi, maxWordCnt, maskFilepath)



# load custom stop words list

dataHome = '/N/u/klosteda/Carbonate/Text-Analysis/data'

corpusRoot = os.path.join(dataHome, 'StarTrekNextGenClean','season1')

stopWordsFilepath = os.path.join(dataHome,'earlyModernStopword.txt' )

with open(stopWordsFilepath, "r") as f:
    stopWordsList = f.readlines()
            
stopWordsList = [w.strip().lower() for w in stopWordsList]




# Use case one, draw word cloud from a single text

textFilepath = os.path.join(corpusRoot, '102.txt')

# filepath to save word cloud image
wcImgFilepath = '/N/u/klosteda/Carbonate/Text-Analysis/Output/starTrek102TopTenPy.png'

dpi = 300

# As an option, user can provision a mask related to the text theme
maskFilepath = '/N/u/klosteda/Carbonate/Text-Analysis/data/wordcloudMasks/StarTrek.png'

maxWordCnt = 500

drawWordCloudFromSingleText(textFilepath, stopWordsList, wcImgFilepath, dpi, maxWordCnt, maskFilepath)



"""
# Use case two, draw word cloud from a corpus root

# filepath to save word cloud image
wcImgFilepath = '/N/u/klosteda/Carbonate/Text-Analysis/Output/starTrekTopTenPy.png'

dpi = 300

# As an option, user can provision a mask related to the text theme
maskFilepath = '/N/u/klosteda/Carbonate/Text-Analysis/data/wordcloudMasks/StarTrek.png'

maxWordCnt = 500

drawWordCloudFromScan(corpusRoot, stopWordsList, wcImgFilepath, dpi, maxWordCnt, maskFilepath)
"""
