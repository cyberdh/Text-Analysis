
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
import re
import pandas as pd
import glob
import matplotlib.pyplot as plt
import plotly as py
import plotly.graph_objs as go
from gensim import corpora, models
import pickle
from wordcloud import WordCloud

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
dataCleaned = os.path.join(homePath, "Text-Analysis-master", "TopicModeling", "LDA", "cleanedData", "malletModel")
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
                sentTopicsDf = sentTopicsDf.append(pd.Series([int(topicNum+1), round(propTopic,4), topicKeywords]), ignore_index=True)
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
    sortOrder = ['Topic 1','Filenames']
    
    docTopics = []
    for m in optimalModel[corpus]:
        docTopics.append(m)

    topicSeriesDf = pd.DataFrame([[y[1] for y in  x] for x in docTopics])

    txtPaths = pd.Series(os.path.basename(pathName) for pathName in paths)

    textPath = pd.Series(txtPaths)
    contents = pd.Series(texts)
    docTopicDis = pd.concat([textPath, topicSeriesDf], axis=1)

    docTopicsDf = docTopicDis.reset_index(drop = True)
    # get length of df's columns
    numCols = len(list(docTopicsDf))

    rng = range(0, (numCols) + 1)

    newCols = ['Filenames'] + ['Topic ' + str(i+1) for i in rng]

    # ensure the length of the new columns list is equal to the length of df's columns
    docTopicsDf.columns = newCols[:numCols]

    sortedDf = docTopicsDf.sort_values(sortOrder, ascending = False)
    sortedDF = sortedDf.set_index("Filenames")
    sortedDF = sortedDF.mul(100)
    sortedDF.to_csv(os.path.join(dataResults, docTopicsCSV))
    sortedDF.head(len(sortedDF))
else:
    None
    
if docLevel is True:
    x = optimalModel.show_topics(num_topics = -1)
    topicWords = {}
    for topic,word in x:
        topicWords[topic]=re.sub('[^A-Za-z ]+', '', word)
    tWords = topicWords.values()
    print(tWords)
else:
    None

# Plot a stacked bar graph
if docLevel is True:
    import plotly.express as px
    #Variables
    graphName = 'stackedBarGraphLDA.html'
    wide = 900
    tall = 700
    mainTitle = "Weight of Each Topic in Each Document"
    palette = px.colors.qualitative.Alphabet
    
    #Add row to dataframe
    pd.options.mode.chained_assignment = None
    topicKWlist = []
    for k in tWords:
        topicKWlist.append(k)
    sortedDfSh = sortedDF
    sortedDfSh = sortedDfSh.iloc[::-1]
    dfLength = len(sortedDfSh)
    sortedDfSh.loc["Keywords", :] = topicKWlist
    
    # Plot
    fig = go.Figure(go.Bar(name = "Topic 1", x = sortedDfSh["Topic 1"], y = sortedDfSh.index[:dfLength], orientation = "h",
                           hovertemplate = "<b>Document</b>: %{y}<br>"+"<b>Pct</b>: %{x}%<br>"+"<b>Keywords</b>: " + sortedDfSh.loc["Keywords","Topic 1"], 
                           hoverlabel={"namelength":-1}))
    for i in sortedDfSh.iloc[:, 1:]:
        fig.add_trace(go.Bar(name = str(i), x = sortedDfSh[i], y = sortedDfSh.index[:dfLength], orientation = "h", hovertemplate = "<b>Document</b>: %{y}<br>"+"<b>Pct</b>: %{x}%<br>"+"<b>Keywords</b>: " + sortedDfSh.loc["Keywords",i], hoverlabel={"namelength":-1}))
        fig.update_layout(title = {"text":mainTitle, 'y':0.95, 'x':0.55, 'xanchor': 'center', 'yanchor':'top'},barmode = "stack", width = wide, height = tall, hoverlabel_font_color = "black", colorway = palette)
    py.offline.plot(fig, filename=os.path.join(dataResults, graphName), auto_open = False)
    fig.show()
else:
    None

# Plot wordcloud
wcOutputFile = "wordcloudLDA"
fmt = "png"
width = 800
height = 400
bgc = "black"
cm = "Dark2"
dpi = 600
maxWordCnt = 500
minFont = 10
figSz = (10, 5)

wc = WordCloud(width = width, height = height, background_color = bgc, max_words = maxWordCnt, colormap = cm, min_font_size=minFont)
for t in range(optimalModel.num_topics):
    plt.figure(figsize = figSz)
    wc.fit_words(dict(optimalModel.show_topic(t, 75)))
    plt.imshow(wc, interpolation = 'bilinear')
    plt.axis("off")
    plt.tight_layout()
    
    # save graph as a png image to file
    plt.savefig(os.path.join(dataResults, wcOutputFile + "Topic" + str(t+1) + "." + fmt), format = fmt, dpi = dpi, bbox_inches = 'tight')
    plt.title("Topic #" + str(t+1))
    plt.show()

# Ackowledgements: This algorithm was adapted from the blog "Machine Learning Plus". Reference: Machine Learning Plus. Topic Modeling with Gensim (Python). Retrieved from https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/ on November 5, 2018.
