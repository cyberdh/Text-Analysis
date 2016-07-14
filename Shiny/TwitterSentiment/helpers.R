setwd("~/Documents/IU/CyberDH/Text_Analysis/Shiny/TwitterSentiment")

# Include necessary packages
library(twitteR)
library(plyr)
library(stringr)
library(ggplot2)
library(reshape2)
library(tm)

# Load data 
load("~/Documents/IU/CyberDH/Text_Analysis/data/twitter/trump/realdonaldtrump2016-07-07.RData")
trump.text = sapply(tweets, function(x) x$text)
load("~/Documents/IU/CyberDH/Text_Analysis/data/twitter/hillary/hillaryclinton2016-07-07.RData")
hillary.text = sapply(tweets, function(x) x$text)

# Loading the Opinion Lexicons to Determine Sentiment
#This is an essential step for sentiment analysis. These text documents from Hu and Liu, 2004* are filled with positive and negative words, respectively. The algorithm we will write next will check these documents to score each word in the tweet. If the algorithm runs across the word "love" in a tweet, it will check the positive-words.txt file, find "love" is included, and score the word with a +1. More on that in a second...

lex.pos = scan('~/Documents/IU/CyberDH/Text_Analysis/data/opinionLexicon/positive-words.txt', what='character', comment.char = ';')
lex.neg = scan('~/Documents/IU/CyberDH/Text_Analysis/data/opinionLexicon/negative-words.txt', what='character', comment.char = ';')

# Add words relevant to our corpus using the combine c() function:

pos.words = c(lex.pos)
neg.words = c(lex.neg)

# Implement the sentiment scoring algorithm
score.sentiment = function(tweets, pos.words, neg.words, .progress='none')
{
  
  #figure out the score for each tweet specifically
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

trump.result = score.sentiment(trump.text, pos.words, neg.words)
clinton.result = score.sentiment(hillary.text, pos.words, neg.words)

both.result <- data.frame(x = trump.result, y = clinton.result)