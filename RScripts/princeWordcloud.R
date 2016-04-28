library(wordcloud)
library(qdap)
library(RColorBrewer)
library(twitteR)
library(plyr)

setwd("~/Documents/IU/CyberDH/Text_Analysis")


api_key <- "akbmHVWwpoxSUIWprIrEx0Cqo"
api_secret <- "pzkXmLBhV7jUKJKHXKN5Zz43evzn12tbUTL95muq6tYBZ08MAn"
access_token <- "285932503-yymLCmhZmFAY2N1YcgBHGULyMMWviWauQIxD6LvS"
access_token_secret <- "CRQirUWnRX1dRE75lELlUA7JryGao3F31VEYX5qm3pIg0"
setup_twitter_oauth(api_key,api_secret,access_token,access_token_secret)

prince.tweets = searchTwitter('Prince', n=5000)

saveRDS(prince.tweets, "data/princeTweets.RData")



prince.text = laply(prince.tweets, function(t) t$getText())


#Strip URLS
prince.text=gsub("(f|ht)(tp)(s?)(://)(.*)[.|/](.*)", "", prince.text)

#Strip punctuation
prince.text=gsub( "[^[:alnum:] ]", "", prince.text )

#Split into words
words <-strsplit(prince.text, "\\W+", perl=TRUE)

# #Remove common words
words=rm_stopwords(words,c(Top100Words,"rt", "amp", "easter", "https", "futuredilf", "la", "s", "el", "en", "m", "de", "2"))

#Get rid of empty elements
words=words[lapply(words,length)>0]

#Flatten the list of lists
words=unlist(words,recursive = FALSE)

#Convert to a sorted frequency table
words=sort(table(words),decreasing=T)
freqs=as.vector(words)
words=names(words)
cols <- colorRampPalette(brewer.pal(12,"Paired"))(500)


wordcloud(words,freqs,scale=c(3,1),min.freq=3,max.words=75, rot.per=0, 
          colors=cols)

