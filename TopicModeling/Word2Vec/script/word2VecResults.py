
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


# File paths
homePath = os.environ["HOME"]
cleanModel = os.path.join(homePath, "Text-Analysis-master", "TopicModeling", "Word2Vec", "cleanedData", "wordvecModel")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")


# Load the word2vec model
model = Word2Vec.load(cleanModel)


# Let's find some word relationships
w2vCSVfile = 'word2vec.csv'
w1 = "hamlet"
topn = 30

wtv = model.wv.most_similar(positive=[w1], topn = topn)
df = pd.DataFrame(wtv)
df.to_csv(os.path.join(dataResults, w2vCSVfile))
print(df.head(10))


# Compare two words to each other.
ws1="hamlet"
ws2="madness"
wordSim = model.wv.similarity(ws1, ws2)
print("Similarity score between {} and {} is {}".format(ws1, ws2, wordSim))

# This code was adapted from Kavita Ganesan at [http://kavita-ganesan.com/gensim-word2vec-tutorial-starter-code/#.XFnQmc9KjUI](http://kavita-ganesan.com/gensim-word2vec-tutorial-starter-code/#.XFnQmc9KjUI). Accessed 02/05/2019.
