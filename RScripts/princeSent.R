library(devtools)
library(twitteR)
library(plyr)
library(ggplot2)

setwd("~/Documents/IU/CyberDH/Text_Analysis")

# api_key <- "akbmHVWwpoxSUIWprIrEx0Cqo"
# api_secret <- "pzkXmLBhV7jUKJKHXKN5Zz43evzn12tbUTL95muq6tYBZ08MAn"
# access_token <- "285932503-yymLCmhZmFAY2N1YcgBHGULyMMWviWauQIxD6LvS"
# access_token_secret <- "CRQirUWnRX1dRE75lELlUA7JryGao3F31VEYX5qm3pIg0"
# setup_twitter_oauth(api_key,api_secret,access_token,access_token_secret)
# 
# prince.tweets = searchTwitter('Prince', n=5000)

prince.tweets <- readRDS("data/princeTweets.RData")

prince.text = laply(prince.tweets, function(t) t$getText())

prince.text <- readRDS("data/princeTweets.RData")

# loading opinion lexicon - used Hu and Liu, 2004 http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
# citation - ing Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing and Comparing Opinions on the Web." Proceedings of the 14th International World Wide Web conference (WWW-2005), May 10-14, 2005, Chiba, Japan.
# downloads as a .rar compressed file
# if using Windows machine, should be able to unzip file
# if using Mac, download RAR Extractor Free (by qing qing yu) from the App Store
# open RAR Extractor Free and choose your settings, then drag downloaded .rar file to the Extractor
#   icon and it will unzip to the location you specified in settings

lex.pos = scan('data/opinionLexicon/positive-words.txt', what='character', comment.char = ';')
lex.neg = scan('data/opinionLexicon/negative-words.txt', what='character', comment.char = ';')

# add words using the c() [combine] function
pos.words = c(lex.pos)
neg.words = c(lex.neg)

# implement sentiment scoring algorithm

score.sentiment = function(tweets, pos.words, neg.words, .progress='none')
{
  require(plyr)
  require(stringr)
  
  scores = laply(tweets, function(tweet, pos.words, neg.words) {
    tweet = gsub('[[:punct:]]', '', tweet)
    tweet = gsub('[[:cntrl:]]', '', tweet)
    tweet = gsub('\\d+', '', tweet)
    
    #REMOVE EMOJIS!
    tweet = iconv(tweet, "ASCII", "UTF-8", sub="")
    
    tweet.lower = tolower(tweet)
    
    
    word.list = str_split(tweet.lower, '\\s+')
    words = unlist(word.list)
    
    #compare our words to the dictionaries of positive and negative terms
    pos.matches = match(words, pos.words)
    neg.matches = match(words, neg.words)
    
    #match returns a position of the matched term or NA, but we just want the TRUE/FALSE, not NA
    pos.matches = !is.na(pos.matches)
    neg.matches = !is.na(neg.matches)
    
    #the score of each tweet is the sum of the positive matches minus the sum of the negative matches
    score = sum(pos.matches) - sum(neg.matches)
    
    return(score)
  }, pos.words, neg.words, .progress = .progress)
  
  scores.df = data.frame(score=scores, text = tweets)
  return(scores.df)
}

sample = c("You're awesome and I love you", "I hate and hate and hate. So angry. Die!", "Impressed and amazed: you are peerless in your achievement of unparalleled mediocrity.")
sample[1]
sampleResult = score.sentiment(sample, pos.words, neg.words)
sampleResult

result = score.sentiment(prince.text, pos.words, neg.words)
head(result)


colnames(result)
rownames(result)
result[,'score']


hist(result$score)

head(result)

q = qplot(result$score, main = "Sentiment of Prince on Twitter", xlab= "Valence of Sentiment (Tweet Score)", ylab="Count (Tweets)")
q = q + theme_bw()
q

