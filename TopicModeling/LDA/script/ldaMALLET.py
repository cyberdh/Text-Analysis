# encoding: utf-8
# # Topic Modeling with Latent Dirichlet Allocation (LDA) and MALLET   


# Import Packages
import sys
import os

# The code in the lines below point to a Python environment specificaly for use with the code created by Cyberinfrastructure for Digital Humanities. It allows for the use of the different pakcages in our code and their subsequent data sets.
# NOTE: These two lines of code are only for use with Research Desktop. You will get an error if you try to run this code on your personal device!!
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"

# Import more packages
import re
from nltk.corpus import stopwords
import glob
import pandas as pd
from pprint import pprint
from collections import Counter
import seaborn as sns


# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models.phrases import Phrases, Phraser
from gensim.models.wrappers import LdaMallet

# spacy for lemmatization
import spacy

# Plotting tools
import matplotlib.pyplot as plt


# Import warning
import logging
import warnings


# This will give more details regarding error messages and will also ignore deprecation and user warnings. All the deprecation and user warnings in this code are not concerning and will not break the code or cause errors in the results.

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
warnings.filterwarnings("ignore",category=DeprecationWarning)
warnings.filterwarnings("ignore",category=UserWarning)
warnings.filterwarnings("ignore",category=FutureWarning)



# File path variables
homePath = os.environ["HOME"]
dataHome = os.path.join(homePath, "Text-Analysis-master", "data")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")
malletPath = os.path.join(homePath, "mallet-2.0.8", "bin", "mallet") # update this path



# Set needed variables 
source = "iranTweets"
fileType = ".json"
docLevel = False
nltkStop = True
customStop = True
spacyLem = True
coherence = False
stopLang = 'english'
lemLang = 'en'
encoding = "utf-8"
errors = "ignore"
textColIndex = "text"
stopWords = []
docs = []
tweets = []

# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words(stopLang))

    stopWords.extend(['would', 'said', 'says', 'also'])


# Add own stopword list

if customStop is True:
    stopWordsFilepath = os.path.join(homePath, "Text-Analysis-master", "data", "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = encoding) as stopfile:
        stopWordsCustom = [x.strip() for x in stopfile.readlines()]

    stopWords.extend(stopWordsCustom)


# Reading in .txt files

if fileType == ".txt":
    paths = glob.glob(os.path.join(dataHome, "shakespeareDated", source + fileType))
    for path in paths:
        with open(path, "r", encoding = encoding, errors = errors) as file:
             # skip hidden file
            if path.startswith('.'):
                continue
            if docLevel is True:
                docs.append(file.read().strip('\n').splitlines())
            else:
                for line in file:
                    stripLine = line.strip()
                    if len(stripLine) == 0:
                        continue
                    docs.append(stripLine.split())


# Reading in .csv and .json files
if fileType == ".csv":
    allFiles = glob.glob(os.path.join(dataHome, "twitter", "CSV", "Iran", source + fileType))     
    df = (pd.read_csv(f, engine = "python") for f in allFiles)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf, dtype = 'str')
    tweets = cdf[textColIndex].values.tolist()
if fileType == ".json":
    allFiles = glob.glob(os.path.join(dataHome, "twitter", "JSON", source + fileType))     
    df = (pd.read_json(f, encoding = encoding) for f in allFiles)
    cdf = pd.concat(df, ignore_index=True)
    cdf = pd.DataFrame(cdf, dtype = 'str')
    tweets = cdf[textColIndex].values.tolist()
    
    


# Data variable

if len(docs) > 0:
    data = docs
else:
    if len(tweets) > 0:
        data = tweets
        # Remove Urls
        data = [re.sub(r'http\S+', '', sent) for sent in data]
        # Remove new line characters
        data = [re.sub('\s+', ' ', sent) for sent in data]
#pprint(data[:1])


# Tokenizing

def sentToWords(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

dataWords = list(sentToWords(data))

if docLevel is True:
    for i in dataWords:
        print(i[:1])
else:
	None
    #print(dataWords[:1])


# Find Bigrams and Trigrams
# Build the bigram and trigram models
bigram = Phrases(dataWords, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = Phrases(bigram[dataWords], threshold=100)  

# Removes model state from Phrases thereby reducing memory use.
bigramMod = Phraser(bigram)
trigramMod = Phraser(trigram)

# See bigram/trigram example
testNgram = trigramMod[bigramMod[dataWords[0]]]
char = "_"
nGrams = [s for s in testNgram if char in s]
            
#pprint(Counter(nGrams))


# Functions

# Define functions for stopwords, bigrams, trigrams and lemmatization
def removeStopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stopWords] for doc in texts]

def makeBigrams(texts):
    return [bigramMod[doc] for doc in texts]

def makeTrigrams(texts):
    return [trigramMod[bigramMod[doc]] for doc in texts]


if spacyLem is True:
    def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        """https://spacy.io/api/annotation"""
        textsOut = []
        lemmaPOS = []
        for sent in texts:
            doc = nlp(" ".join(sent)) 
            textsOut.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
            lemmaPOS.append([token.text and token.lemma_ and token.pos_ for token in doc if token.pos_ in allowed_postags])
        return textsOut
        print(lemmaPOS[:10])


# Apply functions

# Remove Stop Words
dataWordsNostops = removeStopwords(dataWords)

# Form Bigrams
dataWordsNgrams = makeBigrams(dataWordsNostops)

if spacyLem is True:
    # Initialize spacy language model, eliminating the parser and ner components
    nlp = spacy.load(lemLang, disable=['parser', 'ner'])
    
    # Do lemmatization tagging only noun, adj, vb, adv
    allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']
    dataLemmatized = lemmatization(dataWordsNgrams, allowed_postags=allowed_postags)
    lemmaPOS = []
    for sent in dataLemmatized:
        lemmaNLP = nlp(" ".join(sent))
        for token in lemmaNLP:
            lemmaPOS.append([token.text, token.lemma_, token.pos_])
    print(lemmaPOS[:10])
    

    # Find ngrams and count number of times they occur
    dataNgrams = [s for s in dataLemmatized[0] if char in s]
    
else:
    dataNgrams = [s for s in dataWordsNgrams[0] if char in s]
#print(Counter(dataNgrams))


# Create the Dictionary and Corpus needed for Topic Modeling

if spacyLem is True:
    # Create Dictionary
    id2word = corpora.Dictionary(dataLemmatized)

    # Create Corpus
    texts = dataLemmatized
else:
    # Create Dictionary
    id2word = corpora.Dictionary(dataWordsNgrams)

    # Create Corpus
    texts = dataWordsNgrams
    
# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]


# If you want to see what word a given id corresponds to, pass the id as a key to the dictionary.

id2word[10]

# Human readable format of corpus (term-frequency)
hReadable = [[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]]
for i in hReadable:
    print(i[:10])

# USING MALLET

# Variables
nTopics = 20
workers = 1
nIter = 1000
seed = 42

ldamallet = LdaMallet(malletPath, corpus=corpus, num_topics=nTopics, id2word=id2word, workers = workers, iterations = nIter, random_seed = seed)


# Now we display the "Top Ten" topics and the coherence score of the MALLET topics. The results show the topic number, the ten highest weighted (or important) keywords, and the weight score of those words. Finally, you get the coherence score.

# Show Topics
pprint(ldamallet.show_topics(formatted=False)[:3])
if coherence is True:
    if spacyLem is True:
        # Compute Coherence Score
        coherenceModelLdamallet = CoherenceModel(model=ldamallet, texts=dataLemmatized, dictionary=id2word, coherence='c_v')
        coherenceLdamallet = coherenceModelLdamallet.get_coherence()
    else:
        # Compute Coherence Score
        coherenceModelLdamallet = CoherenceModel(model=ldamallet, texts=dataWordsNgrams, dictionary=id2word, coherence='c_v')
        coherenceLdamallet = coherenceModelLdamallet.get_coherence()
    
    print('\nCoherence Score: ', coherenceLdamallet)
else:
    None


# FIND OPTIMAL NUMBER OF TOPICS

if coherence is True:
    def computeCoherenceValues(dictionary, corpus, texts, limit, start=20, step=10):
        """
        Compute c_v coherence for various number of topics

        Parameters:
        ----------
        dictionary : Gensim dictionary
        corpus : Gensim corpus
        texts : List of input texts
        limit : Max num of topics

        Returns:
        -------
        modelList : List of LDA topic models
        coherenceValues : Coherence values corresponding to the LDA model with respective number of topics
        """
        coherenceValues = []
        modelList = []
        for numTopics in range(start, limit, step):
            model = gensim.models.wrappers.LdaMallet(malletPath, corpus=corpus, num_topics=numTopics, id2word=id2word)
            modelList.append(model)
            coherenceModel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
            coherenceValues.append(coherenceModel.get_coherence())

        return modelList, coherenceValues
else:
    None

# Compute coherence scores
# Can take a long time to run.
if coherence is True:
    nt = 20
    lmt = 81
    steps = 10
    if spacyLem is True:
        modelList, coherenceValues = computeCoherenceValues(dictionary=id2word, corpus=corpus, texts=dataLemmatized, start=nt, limit=lmt, step=steps)
    else:
        modelList, coherenceValues = computeCoherenceValues(dictionary=id2word, corpus=corpus, texts=dataWordsNgrams, start=nt, limit=lmt, step=steps)
else:
    None

# Show coherence line graph
if coherence is True:
    limit=lmt; start=nt; step=steps;
    x = range(start, limit, step)
    plt.plot(x, coherenceValues)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherenceValues"), loc='best')
    plt.show()
else:
    None

# Print the coherence scores
if coherence is True:
    for m, cv in zip(x, coherenceValues):
        print("Num Topics =", m, " has Coherence Value of", round(cv, 4))
else:
    None


# Select the model containing desired number of topics and print the topics
if coherence is True:
    modelNum = 0
    optimalModel = modelList[modelNum]
    modelTopics = optimalModel.show_topics(formatted=False)
    pprint(optimalModel.print_topics(num_words=10)[:3])
else:
    optimalModel = ldamallet
    modelTopics = optimalModel.show_topics(formatted=False)
    pprint(optimalModel.print_topics(num_words=10)[:3])


# Finding the dominant topic in each chunk
def formatTopicsSentences(ldamodel=ldamallet, corpus=corpus, texts=data):
    # Init output
    
    sentTopicsDf = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topicNum, propTopic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topicNum)
                topicKeywords = ", ".join([word for word, prop in wp])
                sentTopicsDf = sentTopicsDf.append(pd.Series([int(topicNum), round(propTopic,4), topicKeywords]), ignore_index=True)
            else:
                break
    sentTopicsDf.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    if docLevel is True:
        txtPaths = pd.Series(os.path.basename(pathName) for pathName in paths)

        textPath = pd.Series(txtPaths)
        contents = pd.Series(texts)
        sentTopicsDf = pd.concat([textPath, sentTopicsDf, contents], axis=1)
        return(sentTopicsDf)
    else:
        contents = pd.Series(texts)
        sentTopicsDf = pd.concat([sentTopicsDf, contents], axis=1)
        return(sentTopicsDf)

domTopicPerChunkCSV = 'domTopicPerChunk.csv'

dfTopicSentsKeywords = formatTopicsSentences(ldamodel=optimalModel, corpus=corpus, texts=data)

# Format
dfDominantTopic = dfTopicSentsKeywords.reset_index(drop=True)
if docLevel is True:
    dfDominantTopic.columns = ['Filename', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
else:
    dfDominantTopic.columns = ['Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']

    
dfDominantTopic.to_csv(os.path.join(dataResults, domTopicPerChunkCSV))
# Show
dfDominantTopic


# Find the most representative chunk for each topic

chunkRepCSV = 'chunkRepPerTopic.csv'

# Group top 5 sentences under each topic
sentTopicsSorteddfMallet = pd.DataFrame()

sentTopicsOutdfGrpd = dfTopicSentsKeywords.groupby('Dominant_Topic')

for i, grp in sentTopicsOutdfGrpd:
    sentTopicsSorteddfMallet = pd.concat([sentTopicsSorteddfMallet, 
                                             grp.sort_values(['Perc_Contribution'], ascending=[0]).head(1)], 
                                            axis=0)

# Reset Index    
sentTopicsSorteddfMallet.reset_index(drop=True, inplace=True)

# Format
if docLevel is True:
    sentTopicsSorteddfMallet.columns = ['Filename','Topic_Num', "Topic_Perc_Contrib", "Keywords", "Text"]
else:
    sentTopicsSorteddfMallet.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Text"]
    
sentTopicsSorteddfMallet.to_csv(os.path.join(dataResults, chunkRepCSV))

# Show
sentTopicsSorteddfMallet


# Topic distribution across chunks

topicDistCSV = 'domTopicCount.csv'

# Number of Documents for Each Topic
topicCounts = dfTopicSentsKeywords.groupby(['Dominant_Topic','Topic_Keywords']).size().to_frame('Num_Documents').reset_index()

# Percentage of Documents for Each Topic
topicContribution = round(topicCounts['Num_Documents']/topicCounts['Num_Documents'].sum(), 4)

# Concatenate Column wise
dfDominantTopics = pd.concat([topicCounts, topicContribution], axis=1)

# Change Column names
dfDominantTopics.columns = ['Dominant_Topic', 'Topic_Keywords', 'Num_Documents', 'Perc_Documents']
dfDominantTopics.to_csv(os.path.join(dataResults, topicDistCSV))
# Show
dfDominantTopics


# Distribution of each topic across each chunk

if docLevel is True:
    #Variables
    docTopicsCSV = 'docTopics.csv'
    sortOrder = ['topic_0','Filenames']
    
    docTopics = []
    for i in range(len(texts)):
        docTopics.append(optimalModel[corpus[i]])


    topicSeriesDf = pd.DataFrame([[y[1] for y in  x] for x in docTopics])


    txtPaths = pd.Series(os.path.basename(pathName) for pathName in paths)

    textPath = pd.Series(txtPaths)
    contents = pd.Series(texts)
    docTopicDis = pd.concat([textPath, topicSeriesDf], axis=1)

    docTopicsDf = docTopicDis.reset_index(drop = True)
    # get length of df's columns
    numCols = len(list(docTopicsDf))

    rng = range(0, (numCols) + 1)

    newCols = ['Filenames'] + ['topic_' + str(i) for i in rng]

    # ensure the length of the new columns list is equal to the length of df's columns
    docTopicsDf.columns = newCols[:numCols]

    sortedDf = docTopicsDf.sort_values(sortOrder, ascending = False)
    sortedDf.to_csv(os.path.join(dataResults, docTopicsCSV))

    sortedDf
else:
    None


# Plot a stacked bar graph

if docLevel is True:
    #Variables
    graphName = 'barGraphLDA.png'
    boxSize = (1.01,.5,.35,.5)
    colorScheme = "Vega20"
    topN = min(10, len(sortedDf))
    colors = plt.cm.get_cmap(colorScheme)
    sortedDfSh = sortedDf[:topN]
    sortedDfSh = sortedDfSh.iloc[::-1]
    ax = sortedDfSh.plot(kind='barh', figsize = (10,2*topN), stacked = True, colormap = colors)
    ax.set_yticklabels(sortedDfSh['Filenames'], rotation=0)
    ax.tick_params(axis = 'y', which = 'major',labelsize = 24)
    lgd = ax.legend(bbox_to_anchor = boxSize, fontsize = 24)
    ax.figure.savefig(os.path.join(dataResults, graphName), dpi = 300, bbox_inches='tight')
else:
    None

# Plot horizontal bargraph
k = len(sentTopicsSorteddfMallet['Topic_Num'])
if k % 2 == 0:
    num = 2
else:
    num = 5
# Variables
outputFile = "topicsBarGraphHamlet.png"
dpi=300
imgFmt="png"
labSz=.5
figSz=(10,40)
nrows = nTopics/num
ncols = num
colPal = "colorblind"
xlimit = 0,0.4

fiz = plt.figure(dpi = dpi, figsize=figSz)
for i in range(k):
    sns.set(font_scale=labSz)
    df=pd.DataFrame(optimalModel.show_topic(i), columns=['term','prob']).set_index('term')
    plt.subplot(nrows,ncols,i+1)
    plt.title('topic '+str(i+1))
    sns.barplot(x='prob', y=df.index, data=df, label='Hamlet', palette=colPal)
    plt.xlabel('weight')
    sns.plt.xlim(xlimit) 
plt.savefig(os.path.join(dataResults, outputFile), format = imgFmt, dpi = dpi, bbox_inches = 'tight')
plt.show()
