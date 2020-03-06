
# coding: utf-8

# Vader Sentiment Analysis Average Over Time Data Results

# Run CyberDH environment

# NOTE: The below code is only for use with Research Desktop. 
# You will get an error if you try to run this code on your personal device!!

import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"


# Include necessary packages
import pandas as pd
import plotly.express as px
import plotly as py
import warnings

warnings.filterwarnings("ignore",category=FutureWarning)
warnings.filterwarnings("ignore",category=UserWarning)


# File paths
homePath = os.environ['HOME']
cleanedData = os.path.join(homePath,"Text-Analysis-master","VADERSentimentAnalysis", "cleanedData")
dataResults = os.path.join(homePath, "Text-Analysis-master", "Output")

# Read in .csv files
# Mean file
csvAvgDF = pd.read_csv(os.path.join(cleanedData, "vaderAvg.csv"))
avgDF = pd.DataFrame(csvAvgDF)
meanDF = avgDF.set_index(avgDF["Unnamed: 0"])
del meanDF.index.name
del meanDF["Unnamed: 0"]
meanDF["date"] = pd.to_datetime(meanDF["date"], errors='coerce')
meanDF.head(5)

# Count file
csvCountDF = pd.read_csv(os.path.join(cleanedData, "tweetCount.csv"))
codf = pd.DataFrame(csvCountDF)
countDF = codf.set_index(codf["Unnamed: 0"])
del countDF.index.name
del countDF["Unnamed: 0"]
countDF["date"] = pd.to_datetime(countDF["date"], errors='coerce')
countDF.head(5)


# Plot the avg VADER score graph

#Variables
outputFile = "vaderSentMeanOverTime.html"
lineColor = ["crimson"]
fontColor = "black"
bgColor = "darkgray"
zeroColor = "white"
gridColor = "black"
xlabel = "Date"
ylabel = "Sentiment Mean"
mainTitle = "Sentiment Shift Regarding Coronavirus Over Time January 01, 2020 - January 21, 2020"
yRange = [-1, 1]
yIntervals = .2
xTickFormat = "%b-%d, %Y"
angle = 310
xFontSz = 12
yFontSz = 14

# Plot
fig = px.line(meanDF, x="date", y="mean", color_discrete_sequence = lineColor,
                labels = {"date":xlabel,"mean":ylabel}, title=mainTitle)
fig.update_layout(title={'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor':'top'}, 
                  xaxis_rangeslider_visible=True, xaxis = dict(tickmode = "auto", nticks = len(meanDF["date"])),
                  xaxis_tickformat = xTickFormat, plot_bgcolor = bgColor, font={"color": fontColor})
fig.update_yaxes(range=yRange, zeroline = True, zerolinecolor = zeroColor, 
                 dtick = yIntervals, gridcolor = gridColor, tickfont = {"size":yFontSz})
fig.update_xaxes(tickangle=angle, gridcolor = gridColor, tickfont = {"size":xFontSz})
    
py.offline.plot(fig, filename=os.path.join(dataResults, outputFile))

fig.show()


# Plot the tweet count graph
#Variables
coOutputFile = "vaderSentCountOverTime.html"
coLineColor = ["darkgreen"]
coFontColor = "black"
coBgColor = "darkgray"
coGridColor = "black"
coXlabel = "Date"
coYlabel = "Number of Tweets"
coMainTitle = "Count of Coronavirus Tweets Over Time January 01, 2020 - January 21, 2020"
coYrange = [0, max(countDF["count"]+1000)]
coYintervals = 500
coXtickFormat = "%b-%d, %Y"
coAngle = 310
coXfontSz = 10
coYfontSz = 10

# Plot
fig = px.line(countDF, x="date", y="count", color_discrete_sequence = coLineColor,
                labels = {"date":coXlabel,"count":coYlabel}, title=coMainTitle)
fig.update_layout(title={'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor':'top'}, xaxis_rangeslider_visible=True,
                  xaxis = dict(tickmode = 'auto', nticks = len(countDF["date"])), xaxis_tickformat = coXtickFormat, 
                  plot_bgcolor = coBgColor, font={"color": coFontColor})
fig.update_yaxes(range=coYrange, tick0 = 0, dtick = coYintervals, gridcolor = coGridColor, tickfont = {"size":coYfontSz})
fig.update_xaxes(tickangle=coAngle, gridcolor = coGridColor, tickfont = {"size":coXfontSz})
    
py.offline.plot(fig, filename=os.path.join(dataResults, coOutputFile))
fig.show()

# ## VOILA!!

# Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
