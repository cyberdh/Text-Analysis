library(wordcloud)
library(qdap)
library(RColorBrewer)
library(twitteR)

<<<<<<< Updated upstream
=======
setwd("~/Desktop/R/Text_Analysis/Shiny/Twitter")

>>>>>>> Stashed changes
load(file = "brussels.RData")
tweetlist <- sapply(tweets, function(x) x$text)

#Strip URLS
tweetlist=gsub("(f|ht)(tp)(s?)(://)(.*)[.|/](.*)", "", tweetlist)

#Strip punctuation
tweetlist=gsub( "[^[:alnum:] ]", "", tweetlist )

#Split into words
words <-strsplit(tweetlist, "\\W+", perl=TRUE)

# #Remove common words
words=rm_stopwords(words,c(Top100Words,"rt", "amp", "brussels"))

#Get rid of empty elements
words=words[lapply(words,length)>0]

#Flatten the list of lists
words=unlist(words,recursive = FALSE)

#Convert to a sorted frequency table
words=sort(table(words),decreasing=T)
freqs=as.vector(words)
words=names(words)







