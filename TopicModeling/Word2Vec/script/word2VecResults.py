
# coding: utf-8

# Word 2 Vec Results

# ### Run CyberDH environment

# #### NOTE: This chunk of code is only for use with Research Desktop. You will get an error if you try to run this on your personal device!!
import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages 
import pandas as pd
from gensim.models import Word2Vec
import wordcloud
import matplotlib.pyplot as plt


# File paths
homePath = os.environ["HOME"]
cleanModel = os.path.join(homePath, "Text-Analysis-master", "TopicModeling", "Word2Vec", "cleanedData", "wordvecModel")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")


# Load the word2vec model
model = Word2Vec.load(cleanModel)

# Compare two words to each other.
ws1="man"
ws2="woman"
wordSim = model.wv.similarity(ws1, ws2)
print("Similarity score between {} and {} is {}".format(ws1, ws2, wordSim))

# Let's find some word relationships
w2vCSVfile = 'word2vec.csv'
w1 = "woman"
w2 = "king"
w3 = "man"
topn = 200

wtv = model.wv.most_similar(positive=[w1], topn = topn)
df = pd.DataFrame(wtv)
df.to_csv(os.path.join(dataResults, w2vCSVfile))
print(df.head(10))

# Variables
maxWrdCnt = 500
bgColor = "black"
color = "Dark2"
minFont = 10
width = 800
height = 400
figureSz = (20,10)
wcOutputFile = "word2vecWordCloud.png"
imgFmt = "png"
dpi = 600

df.set_index(df["Words"],inplace = True)
df['Words'] = df['Words'].astype(str)

# Additional Stopwords
stopwords = []
text = df[~df['Words'].isin(stopwords)]

# Wordcloud aesthetics

wc = wordcloud.WordCloud(background_color = bgColor, width = width, height = height, max_words = maxWrdCnt, colormap = color, min_font_size = minFont).generate_from_frequencies(text['Cosine Scores'])

# show
plt.figure(figsize = figureSz)
plt.imshow(wc, interpolation = 'bilinear')
plt.axis("off")
plt.tight_layout()
    
# save graph as an image to file
plt.savefig(os.path.join(dataResults, wcOutputFile), format = imgFmt, dpi = dpi, bbox_inches = 'tight')
    
plt.show()




# This code was adapted from Kavita Ganesan at [http://kavita-ganesan.com/gensim-word2vec-tutorial-starter-code/#.XFnQmc9KjUI](http://kavita-ganesan.com/gensim-word2vec-tutorial-starter-code/#.XFnQmc9KjUI). Accessed 02/05/2019.
