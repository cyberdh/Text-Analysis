library(twitteR)
library(wordcloud)
library(qdap)
setwd("~/Desktop/R/RStyleometry/plainText/twitter")

#Read in the text 
text_raw<-scan("snowzilla.txt", what="character", sep="\n")

#Strip URLS
tweets_clean <- gsub("(f|ht)(tp)(s?)(://)(.*)[.|/](.*)", "", tweets_raw)

#strip @mentions and @usernames
tweets_clean <- gsub("@(.*)", "", tweets_raw)

#Split into words
words <-strsplit(tweets_clean, "\\W+", perl=TRUE)

#Flatten the list of lists
words=unlist(words,recursive = FALSE)

#Create a corpus 
corpus <- Corpus(VectorSource(text_raw))

#Clean the corpus
corpus <- tm_map(corpus, stripWhitespace)
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removeWords, stopwords("english"))
corpus <- tm_map(corpus, removePunctuation)

wordcloud(corpus,random.order=FALSE,scale=c(3,.1),rot.per=0,min.freq=1,
          max.words=75,colors=brewer.pal(8, "Dark2"))
wordcloud(words,random.order=FALSE,scale=c(3,.5),rot.per=0,min.freq=1,
          max.words=75,colors=brewer.pal(8, "Dark2"))
          