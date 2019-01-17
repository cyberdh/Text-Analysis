#Set the working directory
setwd("~/Text-Analysis/")

library(tm)
library(wordcloud)
library(ngram)
library(stringr)
library(readtext)


tweets <- readtext('data/twitter/parkland/neverAgain.csv', text_field = "text")

#corpus <- iconv(tweets, to = "utf-8")


removeChars <- function(x) iconv(x, "ASCII", "UTF-8", sub="")
corpus <- removeChars(tweets)


corpus <- tolower(corpus)
corpus <- removeNumbers(corpus)
corpus <- gsub("[[:punct:]]", "", corpus)
removeURL <- function(x) gsub("http[[:alnum:]]*", "", x)
corpus <- removeURL(corpus)
corpus <- removeWords(corpus, c(stopwords("SMART"), 'amp','rt', 'emmachange', 'xokarminox', 'neveragain', ','))
corpus <- stripWhitespace(corpus)


corpus <- toString(corpus)
corpus <- preprocess(corpus, remove.punct = TRUE)
ntoken <- ngram_asweka(corpus, min = 2, max = 2, sep = " ")
ngrm_word <- data.frame(table(ntoken))
sort_ngrm <- ngrm_word[order(ngrm_word$Freq,decreasing=TRUE),]

head(sort_ngrm, 10)

wordcloud(sort_ngrm$ntoken,sort_ngrm$Freq,random.order=FALSE,scale = c(2,1),min.freq = 2,colors = brewer.pal(8,"Dark2"),max.words=50)


