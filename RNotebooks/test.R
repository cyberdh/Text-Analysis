library(twitteR)
library(tm)
library(wordcloud)
library(RColorBrewer)

load(file = "Trump03042016.RData")
tweet_text = sapply(tweets, function(x) x$getText())
corpus = Corpus(VectorSource(tweet_text))


#if you get the below error
#In mclapply(content(x), FUN, ...) :
#  all scheduled cores encountered errors in user code
#add mc.cores=1 into each function

#run this step if you get the error:
#(please break it!)' in 'utf8towcs'
corpus <- tm_map(corpus,
                              content_transformer(function(x) iconv(x, to='UTF-8-MAC', sub='byte')),
                              mc.cores=1
)
corpus <- tm_map(corpus, content_transformer(tolower), mc.cores=1)
corpus <- tm_map(corpus, removePunctuation, mc.cores=1)
corpus <- tm_map(corpus, function(x)removeWords(x,stopwords()), mc.cores=1)
wordcloud(corpus, scale=c(2.5,.7),min.freq=3,max.words=75, rot.per=0, 
          colors=brewer.pal(8, "Dark2"))