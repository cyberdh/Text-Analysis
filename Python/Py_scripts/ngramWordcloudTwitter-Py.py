from textblob import TextBlob
from nltk.corpus import stopwords
import nltk
import os
import re

import string
import pandas as pd
from collections import Counter, defaultdict
import wordcloud
from wordcloud import STOPWORDS
from PIL import Image
import numpy as np
import operator
import glob
import csv

import matplotlib.pyplot as plt

stop_words = stopwords.words('english')
stop_words.extend(['amp','rt', 'xo_karmin_ox', 'neveragain', 'ð', 'â', 'ï','ã', 'emma4change'])

def textClean(text, stopWordsList = None):
    
    #text = [text.lower() for text in text]
    
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

def readCSV(filepath, textColIndex, encoding = 'utf-8', errors = 'ignore'):
    
    with open(filepath, encoding = encoding, errors = errors) as f:
        
        reader = csv.reader(f, delimiter = ',', quotechar = '"')
        
        content = []
        for row in reader: 
            content.append(row[textColIndex])
         
        # skip header
        return content[1 : ]
    
# load custom stop words list

#stopWordsFilepath = '/N/u/klosteda/Carbonate/Text-Analysis/data/nltkStopword.txt'

csvRoot = '/N/u/klosteda/Carbonate/Text-Analysis/data/twitter/parkland'

#with open(stopWordsFilepath, "r") as f:
    #stopWordsList = f.readlines()
            
#stopWordsList = [w.strip().lower() for w in stopWordsList]

all_files = glob.glob(os.path.join(csvRoot, "neverAgain.csv"))

df_all = pd.concat((pd.read_csv(f, index_col = None, header = 0, encoding = 'ISO-8859-1') for f in all_files))

tweets = df_all['text'].tolist()
content = '\n'.join(tweets)
cleanTokens = textClean(content)

print('Finished tokenizing text {}\n'.format(all_files))

cleanText = ' '.join(cleanTokens)

blob = TextBlob(cleanText)

unigrams = blob.ngrams(n=1)
bigrams = blob.ngrams(n=2)
trigrams = blob.ngrams(n=3)

ngramList = []
for wlist in bigrams:
   ngramList.append(' '.join(wlist))
   
df = pd.DataFrame(ngramList)
df = df.replace(' ', '_', regex = True)
dfCounts = df[0].value_counts()
countsDF = pd.DataFrame(dfCounts)
df_C = countsDF.rename(columns={'index':'ngrams', 0:'freq'})
df_C = df_C.sort_values('freq', ascending = False)

df_C.head(10)

maskPath = '/N/u/klosteda/Carbonate/Text-Analysis/data/wordcloudMasks'
mask = np.array(Image.open(os.path.join(maskPath, "USA.png")))

text = df_C

stopwords = set(STOPWORDS)
stopwords.update(["columns", "rows", "kidding_forgetting"])

wc = wordcloud.WordCloud(background_color = "white", colormap = 'Dark2', mask = mask, stopwords=stopwords).generate_from_frequencies(text['freq'])
    
# show
plt.figure(figsize = (20, 10))
plt.imshow(wc, interpolation = 'bilinear')
plt.axis("off")

plt.tight_layout()
    
# save graph as a png image to file
plt.savefig('/N/u/klosteda/Carbonate/Text-Analysis/Output/ngramWordcloudNeverAgain.png', format = 'png', dpi = 300, bbox_inches = 'tight')
    
    


plt.show()

