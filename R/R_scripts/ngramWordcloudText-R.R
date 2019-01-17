# set the working directory
setwd("~/Text-Analysis")

library(tm)
library(wordcloud)
library(ngram)
library(stringr)
library(readtext)


mycorpus <- readtext('data/StarTrekNextGenClean/season1/*.txt')


# Clean the corpus
mycorpus <- tolower(mycorpus)
#myStopWords <- scan("data/earlyModernStopword.txt", what="character", sep="\n")
mycorpus <- removeWords(mycorpus, stopwords("SMART"))
mycorpus <- removePunctuation(mycorpus)
mycorpus <- removeNumbers(mycorpus)
mycorpus <- stripWhitespace(mycorpus)


# collect most frequent bigrams
mycorpus <- toString(mycorpus)
ntoken <- ngram_asweka(mycorpus, min = 2, max = 2, sep = " ")
ngrm_word <- data.frame(table(ntoken))
sort_ngrm <- ngrm_word[order(ngrm_word$Freq,decreasing=TRUE),]

head(sort_ngrm, 10)


stop_words <- c('aye sir', 'sir sir')
sort_ngrm$ntoken <- gsub(paste0(stop_words, collapse = "|"), "", sort_ngrm$ntoken)

# Plot bigram wordcloud
wordcloud(sort_ngrm$ntoken,sort_ngrm$Freq,random.order=FALSE,scale = c(3,1),min.freq = 2,colors = brewer.pal(8,"Dark2"),max.words=30)

