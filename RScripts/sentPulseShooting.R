
# Simple Sentiment Analysis for Twitter

# Global parameters 
  
setwd("~/Desktop/R/Text_Analysis/")

#Source Multiplot Function
source("RScripts/multiplot.R")

# Include necessary packages
library(twitteR)
library(plyr)
library(stringr)
library(ggplot2)
library(reshape)



  
# Load data 
load("~/Desktop/R/Text_Analysis/data/twitter/orlando2016-06-16.RData")
orlando.text = sapply(tweets, function(x) x$text)
load("~/Desktop/R/Text_Analysis/data/twitter/pulse2016-06-16.RData")
pulse.text = sapply(tweets, function(x) x$text)
 
# Loading the Opinion Lexicons to Determine Sentiment
#This is an essential step for sentiment analysis. These text documents from Hu and Liu, 2004* are filled with positive and negative words, respectively. The algorithm we will write next will check these documents to score each word in the tweet. If the algorithm runs across the word "love" in a tweet, it will check the positive-words.txt file, find "love" is included, and score the word with a +1. More on that in a second...

lex.pos = scan('~/Desktop/R/Text_Analysis/data/opinionLexicon/positive-words.txt', what='character', comment.char = ';')
lex.neg = scan('~/Desktop/R/Text_Analysis/data/opinionLexicon/negative-words.txt', what='character', comment.char = ';')

# Add words relevant to our corpus using the combine c() function:
  
pos.words = c(lex.pos, "prayers", "thoughts", "family", "LGBT", "gay", "pride")
neg.words = c(lex.neg, "ISIS", "gun", "abuser", "omar", "matteen")

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

orlando.result = score.sentiment(orlando.text, pos.words, neg.words)
pulse.result = score.sentiment(pulse.text, pos.words, neg.words)

# Plotting Twitter Data
p1 <- hist(orlando.result$score, xlab="Sentiment Score", ylab="Number of Tweets") 
p2 <- hist(pulse.result$score, xlab="Sentiment Score", ylab="Number of Tweets")  
plot( p1, col=rgb(0,0,1,1/4), ylim=c(0,2500))  # first histogram
plot( p2, col=rgb(1,0,0,1/4), ylim=c(0,2500), xlab="Sentiment Score", ylab="Number of Tweets", main = "Shooting at Pulse LGBT Nightclub in Orlando", add=T)
col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4))
legend(2, 1500, legend=c("orlando", "pulse"),
fill=col, cex=0.8)







#Acknowledgements: This algorithm was adapted from Jeffrey Breen's Mining Twitter for Airline Consumer Sentiment article. You can find it here: http://www.inside-r.org/howto/mining-twitter-airline-consumer-sentiment. 

#Reference: Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing and Comparing Opinions on the Web." Proceedings of the 14th International World Wide Web conference (WWW-2005), May 10-14, 2005, Chiba, Japan.



