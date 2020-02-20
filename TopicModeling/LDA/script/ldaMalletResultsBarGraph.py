
# coding: utf-8

# Latent Dirichlet Allocation (LDA) with MALLET Results
# Run cyberdh Python evironment
# NOTE: This cell is only for use with Research Desktop. 
# You will get an error if you try to run this chunk of code on your personal device!!
import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"

#Import packages
import pandas as pd
import glob
import seaborn as sns
import matplotlib.pyplot as plt
from gensim import corpora, models
import pickle

# Import warning
import logging
import warnings

# Gives more details regarding error messages and will also ignore deprecation and user warnings.
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
warnings.filterwarnings("ignore",category=DeprecationWarning)
warnings.filterwarnings("ignore",category=UserWarning)
warnings.filterwarnings("ignore",category=FutureWarning)
warnings.filterwarnings("ignore",category=RuntimeWarning)

# Getting your data
# File paths
homePath = os.environ["HOME"]
dataHome = os.path.join(homePath, "Text-Analysis-master", "data")
dataCleaned = os.path.join(homePath, "Text-Analysis-master", "TopicModeling", "LDA", "cleanedData")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")
cleanDict = os.path.join(dataCleaned, "ldaDict")
cleanData = os.path.join(dataCleaned, "ldaDataClean")
cleanModel = os.path.join(dataCleaned, "ldaModel")
origData = os.path.join(dataCleaned, "ldaDataOrig")

# Set Variables
docLevel = True
paths = glob.glob(os.path.join(dataHome, "shakespeareFolger", "*.txt"))

# Load cleaned data
id2word = corpora.dictionary.Dictionary.load(cleanDict)
optimalModel = models.LdaModel.load(cleanModel)
with open(origData, "rb") as sd:
    data = pickle.load(sd)
with open(cleanData, "rb") as file:
    texts = pickle.load(file)

# Create sparse representation of word counts
corpus = [id2word.doc2bow(text) for text in texts]

# Finding the dominant topic in each chunk
def formatTopicsSentences(ldamodel=optimalModel, corpus=corpus, texts=data):
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


# Apply formatTopicsSentences function 
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
dfDominantTopic.head(10)


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
    graphName = 'stackedBarGraphLDA.png'
    boxSize = (1.01,.5,.35,.5)
    colorScheme = "tab20"
    topN = min(10, len(sortedDf))
    colors = plt.cm.get_cmap(colorScheme)
    sortedDfSh = sortedDf[:topN]
    sortedDfSh = sortedDfSh.iloc[::-1]
    ax = sortedDfSh.plot(kind='barh', figsize = (10,2*topN), stacked = True, colormap = colors)
    ax.set_yticklabels(sortedDfSh['Filenames'], rotation=0)
    ax.tick_params(axis = 'y', which = 'major',labelsize = 24)
    lgd = ax.legend(bbox_to_anchor = boxSize, fontsize = 24)
    ax.figure.savefig(os.path.join(dataResults, graphName), dpi = 300, bbox_inches='tight')
    plt.show()
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
figSz=(100,70)
nrows = k/num
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

# Ackowledgements: This algorithm was adapted from the blog "Machine Learning Plus". Reference: Machine Learning Plus. Topic Modeling with Gensim (Python). Retrieved from https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/ on November 5, 2018.
