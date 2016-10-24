#Call libraries used in the script
library(wordcloud)
library(qdap)
library(RColorBrewer)

#Set the working directory
setwd("~/Desktop/Text-Analysis/data/twitter/")

load("~/Desktop/Text-Analysis/data/twitter/hillary2016-07-28.RData")
tweetlist <- sapply(tweets, function(x) x$text)

#Strip URLS
tweetlist=rm_url(tweetlist, extract = FALSE)

#Strip punctuation
tweetlist=gsub( "[^[:alnum:] ]", "", tweetlist )

#Split into words
words <-strsplit(tweetlist, "\\W+", perl=TRUE)

# #Remove common words
words=rm_stopwords(words,c(Top100Words,"rt", "amp", "hillary", "https"))

#Get rid of empty elements
words=words[lapply(words,length)>0]

#Flatten the list of lists
words=unlist(words,recursive = FALSE)

#Convert to a sorted frequency table
words=sort(table(words),decreasing=T)
freqs=as.vector(words)
words=names(words)
cols <- colorRampPalette(brewer.pal(12,"Paired"))(500)


wordcloud(words,freqs,scale=c(3,1),min.freq=3,max.words=50, rot.per=0, 
          colors=cols)

