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

import matplotlib.pyplot as plt



stop_words = stopwords.words('english')
stop_words.extend(['would', 'said', 'says', 'good'])

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

# load custom stop words list

#stopWordsFilepath = '/Users/klosteda/Text-Analysis/data/earlyModernStopword.txt'

dataHome = '/N/u/klosteda/Carbonate/Text-Analysis/data/StarTrekNextGenClean/season1'

#with open(stopWordsFilepath, "r") as f:
    #stopWordsList = f.readlines()
            
#stopWordsList = [w.strip().lower() for w in stopWordsList]

cleanText = []

for path in glob.glob(os.path.join(dataHome, "102.txt")):
    with open(path, "r") as f:
         # skip hidden file
        if path.startswith('.'):
            continue
        text = f.read()
        cleanText.extend(textClean(text))
        

    print('Finished tokenizing text {}\n'.format(path))
    

cleanTokens = ' '.join(cleanText)

blob = TextBlob(cleanTokens)

unigrams = blob.ngrams(n=1)
bigrams = blob.ngrams(n=2)
trigrams = blob.ngrams(n=3)

ngramList = []
for wlist in bigrams:
   ngramList.append(' '.join(wlist))

df = pd.DataFrame(ngramList)
df = df.replace(' ', '_', regex=True)
dfCounts = df[0].value_counts()
countsDF = pd.DataFrame(dfCounts)
df_C = countsDF.rename(columns={'index':'ngrams', 0:'freq'})
df_C = df_C.sort_values('freq', ascending = False)

df_C.head(10)

maskPath = '/N/u/klosteda/Carbonate/Text-Analysis/data/wordcloudMasks'
mask = np.array(Image.open(os.path.join(maskPath, "Enterprise.png")))

text = df_C

stopwords = set(STOPWORDS)
stopwords.update(["columns", "rows"])
    
wc = wordcloud.WordCloud(background_color = "white", colormap = 'Dark2', mask = mask, stopwords = stopwords).generate_from_frequencies(text['freq'])

# show
plt.figure(figsize = (20, 10))
plt.imshow(wc, interpolation = 'bilinear')
plt.axis("off")

plt.tight_layout()
    
# save graph as a png image to file
plt.savefig('/N/u/klosteda/Carbonate/Text-Analysis/Output/ngramWordCloudStarTrek.png', format = 'png', dpi = 300, bbox_inches = 'tight')
    
    


plt.show()



