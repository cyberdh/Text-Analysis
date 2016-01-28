library(wordcloud)
library(qdap)
library(RColorBrewer)

setwd("~/Desktop/R/Text_Analysis/data/twitter/")

load(file = "snowzilla.RData")
tweetlist <- sapply(tweets, function(x) x$text)

#Strip URLS
tweetlist=gsub("(f|ht)(tp)(s?)(://)(.*)[.|/](.*)", "", tweetlist)

#strip @mentions and @usernames
tweetlist=gsub("@(.*)", "", tweetlist)

#Strip punctuation
tweetlist=gsub( "[^[:alnum:] ]", "", tweetlist )

#Split into words
words <-strsplit(tweetlist, "\\W+", perl=TRUE)

# #Remove common words
words=rm_stopwords(words,c(Top100Words,"rt", "amp", "snowzilla"))

#Get rid of empty elements
words=words[lapply(words,length)>0]

#Flatten the list of lists
words=unlist(words,recursive = FALSE)

#Convert to a sorted frequency table
words=sort(table(words),decreasing=T)
freqs=as.vector(words)
words=names(words)

#add color to the word cloud
pal <- brewer.pal(10, "Spectral")


wordcloud(words,freqs,scale=c(4,.5),min.freq=1,max.words=75, rot.per=0, 
          colors=pal)

