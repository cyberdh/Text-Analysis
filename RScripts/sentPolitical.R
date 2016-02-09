# Simple Sentiment Analysis
# Using 16,000 tweets directed at or written by the top four 2016 presidential candidates post-Iowa Caucus: Hillary Clinton, Ted Cruz, Bernie Sanders, and Donald Trump, we will create plots to analyze the sentiment of Twitter users related to the four candidates.
# To be used in conjunction with the CyberDH RNotebook tutorial found on Github > CyberDH > Text_Analysis.

library(devtools)
library(twitteR)
library(plyr)
library(ggplot2)

# Global Parameters
setwd("~/Desktop/R/Text_Analysis/data/twitter/")


# Load Data
clinton.tweets <- readRDS("tweetsclinton.RData")
cruz.tweets <- readRDS("tweetscruz.RData")
sanders.tweets <- readRDS("tweetssanders.RData")
trump.tweets <- readRDS("tweetstrump.RData")


# Inspect Data
class(clinton.tweets)
length(clinton.tweets)
clinton.tweets[1]
head(clinton.tweets)


# Extract Text
clinton.text = laply(clinton.tweets, function(t) t$getText())
cruz.text = laply(cruz.tweets, function(t) t$getText())
sanders.text = laply(sanders.tweets, function(t) t$getText())
trump.text = laply(trump.tweets, function(t) t$getText())


# Loading Opinion Lexicon

# used Hu and Liu, 2004 http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
# downloads as a .rar compressed file
# if using Windows machine, should be able to unzip file
# if using Mac, download RAR Extractor Free (by qing qing yu) from the App Store
# open RAR Extractor Free and choose your settings, then drag downloaded .rar file to the Extractor
#   icon and it will unzip to the location you specified in settings

lex.pos = scan('../opinionLexicon/positive-words.txt', what='character', comment.char = ';')
lex.neg = scan('../opinionLexicon/negative-words.txt', what='character', comment.char = ';')

# add words using the c() [combine] function
pos.words = c(lex.pos, "congrats', 'congratulations', 'win', 'prove', 'beat', 'endorse', 'endorses', 'exciting', 'vote', 'wins', 'support', 'supports', 'help', 'winner')
neg.words = c(lex.neg, 'lose', 'losing', 'defeat', 'halt')

# Implement Sentiment Scoring Algorithm
score.sentiment = function(tweets, pos.words, neg.words, .progress='none')
{
  require(plyr)
  require(stringr)
  
  scores = laply(tweets, function(tweet, pos.words, neg.words) {
    #normalize tweet text
    tweet = gsub('[[:punct:]]', '', tweet)
    tweet = gsub('[[:cntrl:]]', '', tweet)
    tweet = gsub('\\d+', '', tweet)
    
    #REMOVE EMOJIS!
    tweet = iconv(tweet, "ASCII", "UTF-8", sub="")
    
    tweet.lower = tolower(tweet)
    
    #split list into separate words
    word.list = str_split(tweet.lower, '\\s+')
    words = unlist(word.list)
    
    #compare our words to the dictionaries of positive and negative terms using match function
    pos.matches = match(words, pos.words)
    neg.matches = match(words, neg.words)
    
    #match returns a position of the matched term or NA, but we just want the TRUE/FALSE, not NA
    pos.matches = !is.na(pos.matches)
    neg.matches = !is.na(neg.matches)
    
    #the score of each tweet is the sum of the positive matches minus the sum of the negative matches
    score = sum(pos.matches) - sum(neg.matches)
    
    return(score)
  }, pos.words, neg.words, .progress = .progress)
  
  #compile the scores and text of tweets into a data frame for plotting
  scores.df = data.frame(score=scores, text = tweets)
  return(scores.df)
}


# Algorithm Testing
sample = c("This ice cream is the best! I love this flavor!", "I am so angry at the terrible weather today. Frustrated.", "Wow, spectacular, I wish I could be as perfect as you.")
sampleResult = score.sentiment(sample, pos.words, neg.words)
sampleResult


# Scoring Twitter Data
clinton.result = score.sentiment(clinton.text, pos.words, neg.words)
cruz.result = score.sentiment(cruz.text, pos.words, neg.words)
sanders.result = score.sentiment(sanders.text, pos.words, neg.words)
trump.result = score.sentiment(trump.text, pos.words, neg.words)

# Peeking at results (run each of the following four lines one at a time)
head(clinton.result)

head(cruz.result)

head(sanders.result)

head(trump.result)


# Plotting Twitter Data
clinton.plot = qplot(clinton.result$score, xlim=(c(-7,7)),
                     main = "Sentiment of @HillaryClinton on Twitter", xlab= "Valence of Sentiment (Tweet Score)", ylab="Count (Tweets)")
cruz.plot = qplot(cruz.result$score, xlim=(c(-7,7)),
                  main = "Sentiment of @tedcruz on Twitter", xlab= "Valence of Sentiment (Tweet Score)", ylab="Count (Tweets)")
sanders.plot = qplot(sanders.result$score, xlim=(c(-7,7)),
                     main = "Sentiment of @BernieSanders on Twitter", xlab= "Valence of Sentiment (Tweet Score)", ylab="Count (Tweets)")
trump.plot = qplot(trump.result$score, xlim=(c(-7,7)),
                   main = "Sentiment of @realDonaldTrump on Twitter", xlab= "Valence of Sentiment (Tweet Score)", ylab="Count (Tweets)")

clinton.plot = clinton.plot + theme_bw()
cruz.plot = cruz.plot + theme_bw()
sanders.plot = sanders.plot + theme_bw()
trump.plot = trump.plot + theme_bw()


# Run each of the following four lines one at a time to view all plots. Can also export the plot to the right
clinton.plot

cruz.plot

sanders.plot

trump.plot


#########

# Acknowledgements: This algorithm was adapted from Jeffrey Breen's Mining Twitter for Airline Consumer Sentiment article. You can find it here: http://www.inside-r.org/howto/mining-twitter-airline-consumer-sentiment. 
# Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing and Comparing Opinions on the Web." Proceedings of the 14th International World Wide Web conference (WWW-2005), May 10-14, 2005, Chiba, Japan.
