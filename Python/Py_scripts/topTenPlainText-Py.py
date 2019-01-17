from nltk.corpus import stopwords
import os
import string
from collections import defaultdict
import operator
import matplotlib.pyplot as plt
import numpy as np
import re
import math


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


"""
Get sorted frequency in descending order
"""
def getFreq(tokens):
    
    freq = defaultdict(int)

    for t in tokens:
        freq[t] += 1
    
    # sorted frequency in descending order
    return sorted(freq.items(), key = operator.itemgetter(1), reverse = True)


def plotTopTen(sortedFreq, title, fontParas, imgFilepath, dpi):
    
    topn = 15

    for t in sortedFreq[0 : topn]:
        
        print('{} : {}'.format(t[0], t[1]))
    
    topNWords = [w for w in sortedFreq[0 : topn]]

    x_pos = np.arange(len(topNWords))
    cnts = [w[1] for w in topNWords]

    plt.rcdefaults()

    plt.bar(x_pos, cnts, align = 'center', alpha = 0.5, color = ['red', 
                                                             'orange', 'yellow', 'green', 'blue',
                                                             'darkorchid', 'darkred', 'darkorange', 
                                                             'gold', 'darkgreen'])
    
    for k in fontParas:
        plt.rcParams[k] = fontParas[k]
        
    plt.xticks(x_pos, [w[0] for w in topNWords])
    plt.xticks(rotation = 45)
        
    xlabel = plt.xlabel('Words')
    xlabel.set_color('red')
    ylabel = plt.ylabel('Frequency')
    ylabel.set_color('red')
    
    high = max(cnts)
    low = 0
    
    plt.ylim(low, math.ceil(high + 0.1 * (high - low)))
    
    for xpos, count in zip(x_pos, cnts):
    
        plt.text(x = xpos, y = count + 1, s = str(count), ha = 'center', va = 'bottom')

    plt.title(title)
 
    plt.savefig(imgFilepath, format = 'png', dpi = dpi, bbox_inches = 'tight')
    
    plt.show()



def getTokensFromSingleText(textFilepath, stopWordsList):
    
    with open(textFilepath, "r") as f:
        text = f.read()

    return textClean(text, stopWordsList)



def getTokensFromScan(corpusRoot, stopWordsList):
    
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
    
    return tokens



# load custom stop words list

dataHome = '/N/u/klosteda/Carbonate/Text-Analysis/data'

corpusRoot = os.path.join(dataHome, 'StarTrekNextGenClean/season1')

stopWordsFilepath = os.path.join(dataHome, 'nltkStopword.txt')

with open(stopWordsFilepath, "r") as f:
    stopWordsList = f.readlines()
            
stopWordsList = [w.strip().lower() for w in stopWordsList]




# Use case one, analyze top 10 most frequent words from a single text

textFilepath = os.path.join(corpusRoot, '102.txt')

# get tokens
tokens = getTokensFromSingleText(textFilepath, stopWordsList)

# get frequency
freq = getFreq(tokens)

title = 'Top 10 Words, Star Trek'

# a dictionary that specifies font related parameters as key-value pairs

fontParas = {'font.sans-serif' : 'Arial', 'font.family' : 'sans-serif'}

imgFilepath = '/N/u/klosteda/Carbonate/Text-Analysis/Output/starTrek102TopTenPlainText.png'

dpi = 300

plotTopTen(freq, title, fontParas, imgFilepath, dpi)




"""
# Use case two, analyze top 10 most frequent words from a corpus root

tokens = getTokensFromScan(corpusRoot, stopWordsList)

# get frequency
freq = getFreq(tokens)

title = 'Top 10 Words, Star Trek: Next Generation'

# a dictionary that specifies font related parameters as key-value pairs

fontParas = {'font.sans-serif' : 'Arial', 'font.family' : 'sans-serif'}

imgFilepath = '/N/u/klosteda/Carbonate/Text-Analysis/Output/starTrekTopTenPlainText.png'

dpi = 300

plotTopTen(freq, title, fontParas, imgFilepath, dpi)
"""
