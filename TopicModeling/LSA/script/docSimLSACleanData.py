
# coding: utf-8

# Document Similarity with Latent Semantic Analysis (LSA)

# Run CyberDH environment

# NOTE: This cell is only for use with Research Desktop. You will get an error if you try to run this cell on your personal device!!
import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"

# Include necessary packages for notebook 
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
#from scipy.sparse.linalg import svds
import pandas as pd
import warnings
import numpy as np
import string
import nltk
from nltk.corpus import stopwords
import spacy

# This will ignore deprecation and future warnings. 
# Suppress warnings from pandas library
warnings.filterwarnings("ignore", category=DeprecationWarning,
                        module="pandas", lineno=570)
warnings.filterwarnings("ignore", category=FutureWarning,
                        module = "sklearn", lineno = 1059)
warnings.filterwarnings("ignore", category=UserWarning,
                        module = "sklearn", lineno = 300)

# Getting your data
# File paths
homePath = os.environ["HOME"]
dataHome = os.path.join(homePath, "Text-Analysis-master", "data", "shakespeareDated")
cleanedData = os.path.join(homePath, "Text-Analysis-master", "TopicModeling", "LSA", "cleanedData")

# Set needed variables
nltkStop = True
customStop = True
lem = True
lowerCase = True
removeDigits = True
language = 'english'
lemLang = "en"
encoding = 'utf-8'
errors = 'ignore'
singleDocs = False
nComp = True
stopWords = []
tokenDict = {}

# Stopwords
if nltkStop is True:
    # NLTK Stop words
    stopWords = stopwords.words(language)

    stopWords.extend(['would', 'said', 'says', 'also'])

# Add own stopword list
if customStop is True:
    stopWordsFilepath = os.path.join(homePath, "Text-Analysis-master", "data", "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = encoding, errors = errors) as f:
        stopWordsList = [x.strip() for x in f.readlines()]

    stopWords.extend(stopWordsList)



# Functions
if lem is True:
    nlp = spacy.load(lemLang, diasble=["parser","ner"])
    nlp.max_length=2500000
    def tokenFilter(token):
        return not (token.is_space)
    
    def tokenize(text):
        for doc in nlp.pipe([text]):
            tokens = [token.lemma_ for token in doc if tokenFilter(token)]
        return tokens

else:
    def tokenize(text):
        tokens = nltk.word_tokenize(text)
        return tokens


# Read in documents
if singleDocs is True:
    for subdir, dirs, files in os.walk(dataHome):
        for file in files:
            if file.startswith('.'):
                    continue
            filePath = subdir + os.path.sep + file
            with open(filePath, 'r', encoding = encoding, errors = errors) as textFile:
                text = textFile.read()
                if lowerCase and removeDigits is True:
                    lowers = text.lower()
                    noPunctuation = lowers.translate(str.maketrans('','', string.punctuation))
                    noDigits = noPunctuation.translate(str.maketrans('','', string.digits))
                    tokenDict[file] = noDigits
                elif lowerCase == True and removeDigits == False:
                    lowers = text.lower()
                    noPunctuation = lowers.translate(str.maketrans('','', string.punctuation))
                    tokenDict[file] = noPunctuation
                elif lowerCase == False and removeDigits == True:
                    noPunctuation = text.translate(str.maketrans('','', string.punctuation))
                    noDigits = noPunctuation.translate(str.maketrans('','', string.digits))
                    tokenDict[file] = noDigits
                else:
                    noPunctuation = text.translate(str.maketrans('','', string.punctuation))
                    tokenDict[file] = noPunctuation
else:
    data = []
    text = []
    for folder in sorted(os.listdir(dataHome)):
        if not os.path.isdir(os.path.join(dataHome, folder)):
            continue
        for file in sorted(os.listdir(os.path.join(dataHome, folder))):
            data.append(((dataHome,folder,file)))
    df = pd.DataFrame(data, columns = ["Root", "Folder", "File"])
    df["Paths"] = df["Root"].astype(str) + "/" + df["Folder"].astype(str) + "/" + df["File"].astype(str)
    for path in df["Paths"]:
        if not path.endswith(".txt"):
            continue
        with open(path, "r", encoding=encoding, errors = errors) as f:
            t = f.read().strip().split()
            if lowerCase and removeDigits is True:
                lowers = ' '.join(t).lower()
                noPunctuation = lowers.translate(str.maketrans('','', string.punctuation))
                noDigits = noPunctuation.translate(str.maketrans('','', string.digits))
                text.append(noDigits)
            elif lowerCase == True and removeDigits == False:
                lowers = ' '.join(t).lower()
                noPunctuation = lowers.translate(str.maketrans('','', string.punctuation))
                text.append(noPunctuation)
            elif lowerCase == False and removeDigits == True:
                noPunctuation = ' '.join(t).translate(str.maketrans('','', string.punctuation))
                noDigits = noPunctuation.translate(str.maketrans('','', string.digits))
                text.append(noDigits)
            else:
                noPunctuation = text.translate(str.maketrans('','', string.punctuation))
                text.append(noPunctuation)
    df["Text"] = pd.Series(text)
    df["Text"] = ["".join(map(str, l)) for l in df["Text"].astype(str)]
    d = {'Text':'merge'}
    dfText = df.groupby(["Folder"])["Text"].apply(lambda x: ' '.join(x)).reset_index()
    
    tokenDict = dict(zip(dfText["Folder"], dfText["Text"]))


# Let's check and see if our dictionary now has our data. 
print(list(tokenDict.keys())[0:10])


# Tfidf Vectorizer
vectorizer = TfidfVectorizer(tokenizer = tokenize, stop_words = stopWords)
dtm = vectorizer.fit_transform(tokenDict.values())

# Get words that correspond to each column
vectGFN = vectorizer.get_feature_names()
print(vectGFN[:20])


# Run SVD and Cosine Similarity
if nComp is True:
    tsvd = TruncatedSVD(n_components=dtm.shape[1]-1)
    tsvd.fit(dtm)
    tsvdVarRatios = tsvd.explained_variance_ratio_

    def selectNcomponents(var_ratio, goal_var: float) -> int:
        total_variance = 0.0
        n_components = 0
        for explained_variance in var_ratio:
            total_variance += explained_variance
            n_components += 1
            if total_variance >= goal_var:
                break
        return n_components
else:
    None

if nComp is True:
    nc = selectNcomponents(tsvdVarRatios, 0.95)
    print(nc)
else:
    None

if nComp is True:
    lsa = TruncatedSVD(n_components = nc, n_iter = 1000, random_state = 42)
    dtmLsa = lsa.fit_transform(dtm)
    cosineSim = cosine_similarity(dtmLsa)
else:
    lsa = TruncatedSVD(n_components = dtm.shape[0], n_iter = 1000, random_state = 42)
    dtmLsa = lsa.fit_transform(dtm)
    cosineSim = cosine_similarity(dtmLsa)
# Save as .csv file
csvFileName = "docSimilarityMatrix.csv"

df = pd.DataFrame(cosineSim, index = tokenDict.keys(), columns=tokenDict.keys())
dfS = df[sorted(df)]
sortedDf = dfS.sort_index(axis = 0)
np.fill_diagonal(sortedDf.values, np.nan)
sortedDf.to_csv(os.path.join(cleanedData, csvFileName))


# This notebook was adapted from https://www.datascienceassn.org/sites/default/files/users/user1/lsa_presentation_final.pdf at Colorado University, Boulder. Accessed on 02/01/2019.
