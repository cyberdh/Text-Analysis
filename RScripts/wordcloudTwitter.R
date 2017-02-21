#Call libraries used in the script 
library(wordcloud)
library(tm)
library(RColorBrewer)
library(twitteR)

#Set the working directory
setwd("~/Text-Analysis/")

#load file with saved tweets
load("data/twitter/HillaryOct4.RData")

tweets_text <- sapply(tweets, function(x) x$text)

corpus <- Corpus(VectorSource(tweets_text))

corpus <- tm_map(corpus,
                 content_transformer(function(x) iconv(x, to='UTF-8', sub='byte')),
                 mc.cores=1)
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, content_transformer(removePunctuation))
corpus <- tm_map(corpus, content_transformer(removeNumbers))
corpus <- tm_map(corpus, content_transformer(removeWords), c(stopwords("english"),'amp','rt','http', 'https','httpstc','httpst','httpstco', 'marketing', 'hillary', 'dont'))



wordcloud(corpus, min.freq=10, max.words=100, scale=c(4,1), colors=brewer.pal(8, "Dark2"))

# Ackowledgements: Much of the algorithm was acquired from a blog by Hanxue Lee called "Flummoxed by IT." The title of this blog entry is "Twitter Word Cloud Using R." The blog can be found at http://flummox-engineering.blogspot.com/2016/03/twitter-word-cloud-using-r.html. This blog was posted March 11, 2016.
# Reference: Hanxue Lee. (2016, March 11). Twitter Word Cloud Using R. Retrieved from http://flummox-engineering.blogspot.com/2016/03/twitter-word-cloud-using-r.html                           
