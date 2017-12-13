#Call libraries used in the script 
library(wordcloud)
library(tm)
library(RColorBrewer)
library(twitteR)

#Set the working directory
setwd("~/Text-Analysis/")

#load file with saved tweets
tweets <- read.csv("data/twitter/tweetsclinton.csv")

#convert to utf-8
corpus <- iconv(tweets$text, to = "utf-8")
corpus <- Corpus(VectorSource(corpus))

#read any non-utf-8 characters as ASCII
corpus <- tm_map(corpus,
                 content_transformer(function(x) iconv(x, 'ASCII', 'UTF-8', sub='')))
                                     
#convert all characters to lower case
corpus <- tm_map(corpus, content_transformer(tolower))
                                     
#clean tweets
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, stripWhitespace)
removeURL <- function(x) gsub("http[[:alnum:]]*", "", x)
corpus <- tm_map(corpus, content_transformer(removeURL))
                                     
#remove stopwords
corpus <- tm_map(corpus, removeWords, c(stopwords("english"),'amp', 'rt', 'marketing', 'hillary', 'dont', 'hillaryclinton'))

#plot wordcloud
wordcloud(corpus, min.freq=10, max.words=100, scale=c(4,1), colors=brewer.pal(8, "Dark2"))

# Ackowledgements: Much of the algorithm was acquired from a blog by Hanxue Lee called "Flummoxed by IT." The title of this blog entry is "Twitter Word Cloud Using R." The blog can be found at http://flummox-engineering.blogspot.com/2016/03/twitter-word-cloud-using-r.html. This blog was posted March 11, 2016.
# Reference: Hanxue Lee. (2016, March 11). Twitter Word Cloud Using R. Retrieved from http://flummox-engineering.blogspot.com/2016/03/twitter-word-cloud-using-r.html                           
