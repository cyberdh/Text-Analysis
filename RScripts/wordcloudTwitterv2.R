#Create a wordcloud of the top 75 words used in tweets about Winter Storm Jonas

setwd("~/Desktop/R/Text_Analysis/data/twitter/")

library(wordcloud)
library(twitteR)
library(tm)
library(RColorBrewer)



load(file = "snowzilla.RData")
tweets.df <- twListToDF(tweets)

corpus <- Corpus(VectorSource(tweets.df$text))
corpus <- tm_map(corpus, (tolower))


wordcloud(words,freqs,scale=c(4,.5),min.freq=1,max.words=75, rot.per=0, 
          colors=pal)

