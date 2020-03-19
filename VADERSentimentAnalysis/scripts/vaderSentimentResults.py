
# coding: utf-8

# Vader Sentiment Analysis Results

# Run CyberDH environment

# NOTE: This chunk of code is only for use with Research Desktop. You will get an error if you try to run this on your personal device!!
import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages 
import pickle
import pandas as pd
import plotly as py
import plotly.express as px
import plotly.graph_objs as go
from collections import Counter
import math


# File paths
homePath = os.environ['HOME']
dataResults = os.path.join(homePath, "Text-Analysis-master","Output")
dataClean = os.path.join(homePath,"Text-Analysis-master","VADERSentimentAnalysis", "cleanedData")


# Load data
with open(os.path.join(dataClean, "vaderScores"), "rb") as vaderScore:
    res = pickle.load(vaderScore)
with open(os.path.join(dataClean, "total"), "rb") as vaderTotal:
    total = pickle.load(vaderTotal)
with open(os.path.join(dataClean, "scores"), "rb") as s:
    scores = pickle.load(s)
with open(os.path.join(dataClean, "numberOfText"), "rb") as nt:
    numberOfTweets = pickle.load(nt)
with open(os.path.join(dataClean, "squared"), "rb") as squared:
    totalSquared = pickle.load(squared)


print(res)


# Calcualte the `mean` and the standard deviation (`std`) of sentiment scores.
mean = total / numberOfTweets
std = math.sqrt(totalSquared / numberOfTweets) - mean**2
rmean = round(mean,2)

# Save the results of the `mean`, `std`, and `numberOfTweets` as a text file. 
with open(os.path.join(dataResults, 'VADERCombinedRawData.txt'), 'w') as write_file:
    write_file.write(str(res))
    write_file.write("\nMean: " + str(mean))
    write_file.write("\nStandard Deviation: " + str(std))
    write_file.write("\nNumber of Tweets: " +str(numberOfTweets))

# Create data frame
cres = Counter(res)
resdf = pd.DataFrame.from_dict(cres, orient='index').reset_index()
resdf = resdf.rename(columns={'index':'score', 0:'count'})
total = resdf['count'].sum()
pct = []
for i in resdf["count"]:
    pct.append(round((i/total) * 100, 2).astype(str)+'%')
resdf["pct"] = pct
    
print(resdf.head(21))

# Plot the graph
# Variables
vaderBarOutput = 'vaderBarGraph'
fmt = '.html'
mainColor = ["crimson"]
fontColor = "black"
zeroColor = "black"
meanColor = "mediumpurple"
wide = 750
tall = 550
labelX = 'Sentiment Score'
labelY = 'Number of Tweets'
labelTitle = 'Coronavirus VADER Overall Analysis: January 01-21, 2020<br>'+ 'Mean = {0:.2f}'.format(mean) + ', ' + 'Std = {0:.2f}'.format(std) +', ' + "Number of Tweets = {:,}".format(numberOfTweets)
rotate = -45
yMax = 2000 + max(res.values())

# Plot
fig = px.bar(resdf, x="score", y="count", text = "pct", title=labelTitle, color_discrete_sequence = mainColor, labels = {"score":labelX,"count":labelY})
fig.update_traces(texttemplate='%{text}', textposition='outside', textangle=rotate)
fig.update_layout(title={'y':0.90, 'x':0.5, 'xanchor': 'center', 'yanchor':'top'}, font={"color": fontColor}, width = wide, height = tall)
fig.add_trace(go.Scatter(x = [0,0], y = [0,yMax], mode = "lines", name = "Zero", showlegend = True, marker_color = zeroColor))
fig.add_trace(go.Scatter(x = [rmean,rmean], y = [0,yMax], mode = "lines", name = "Mean", showlegend = True, marker_color = meanColor))
fig.update_xaxes(layer = "below traces", dtick=.1, tickangle = rotate)
fig.update_yaxes(range = [0,yMax])
py.offline.plot(fig, filename=os.path.join(dataResults, vaderBarOutput + fmt), auto_open = False)
fig.show()

# ## VOILA!!

# Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
