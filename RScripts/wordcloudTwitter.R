library(wordcloud)
library(qdap)
library(RColorBrewer)

setwd("~/Desktop/R/Text_Analysis/data/twitter/")

load(file = "blizzard2016v2.RData")
tweetlist <- sapply(tweets, function(x) x$text)

#Strip URLS
tweetlist=gsub("(f|ht)(tp)(s?)(://)(.*)[.|/](.*)", "", tweetlist)

#Strip punctuation
tweetlist=gsub( "[^[:alnum:] ]", "", tweetlist )

#Split into words
words <-strsplit(tweetlist, "\\W+", perl=TRUE)

# #Remove common words
words=rm_stopwords(words,c(Top100Words,"rt", "amp", "blizzard2016"))

#Get rid of empty elements
words=words[lapply(words,length)>0]

#Flatten the list of lists
words=unlist(words,recursive = FALSE)

#Convert to a sorted frequency table
words=sort(table(words),decreasing=T)
freqs=as.vector(words)
words=names(words)

wordcloud(words,freqs,scale=c(2.5,.7),min.freq=3,max.words=100, rot.per=0, 
          colors=brewer.pal(8, "Dark2"))

