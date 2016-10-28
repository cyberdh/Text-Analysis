
# Simple Sentiment Analysis for Twitter

# Global parameters 
  
setwd("~/Desktop/Text-Analysis/")

# Include necessary packages
library(twitteR)
library(plyr)
library(stringr)
library(ggplot2)
library(reshape2)
library(tm)

# Load data 
load("~/Desktop/Text-Analysis/data/twitter/TrumpOct4.RData")
trump.text = sapply(tweets, function(x) x$text)
load("~/Desktop/Text-Analysis/data/twitter/HillaryOct4.RData")
hillary.text = sapply(tweets, function(x) x$text)
 
# Loading the Opinion Lexicons to Determine Sentiment
#This is an essential step for sentiment analysis. These text documents from Hu and Liu, 2004* are filled with positive and negative words, respectively. The algorithm we will write next will check these documents to score each word in the tweet. If the algorithm runs across the word "love" in a tweet, it will check the positive-words.txt file, find "love" is included, and score the word with a +1. More on that in a second...

lex.pos = scan('~/Desktop/Text-Analysis/data/opinionLexicon/positive-words.txt', what='character', comment.char = ';')
lex.neg = scan('~/Desktop/Text-Analysis/data/opinionLexicon/negative-words.txt', what='character', comment.char = ';')

# Add words relevant to our corpus using the combine c() function:
  
pos.words = c(lex.pos, 'imwithher', 'maga', 'america', 'makeamericagreatagain', 'first', 'hillaryforamerica', 'hillary4america', 'imwithyou', 'strongertogether')
neg.words = c(lex.neg, 'crooked', 'crookedhillary', 'drumpf', 'dumptrump', 'demagogue', 'prejudice', 'racist', 'thedonald', 'mock', 'xenophobic', 'trump', 'bitch', 'fuck', 'taxes', 'tax', 'deny', 'denying', 'cunt', 'pussy', 'russia', 'russian', 'wikileaks')

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
hillary.result = score.sentiment(hillary.text, pos.words, neg.words)

df.result <- data.frame(x = trump.result, y = hillary.result)

#Ignore--these are files to make the Shiny app run faster
write.csv(trump.result, file = "~/Desktop/TrumpResultDF.csv")
write.csv(hillary.result, file = "~/Desktop/ClintonResultDF.csv")
write.csv(df.result, file = "~/Desktop/BothResultDF.csv")

legend_title <- "Candidate"
p <- ggplot(melt(df.result), aes(value, fill=variable)) + 
  geom_histogram(position = "dodge", binwidth = .5 ) + xlab("Sentiment Score") + 
  ylab("Number of Tweets") + ggtitle("Sentiment Scoring of Tweets Mentioning @RealDonaldTrump and @HillaryClinton") + 
  scale_x_continuous(breaks=pretty(df.result$x.score, n=14)) + xlim(c(-7,7)) +
  scale_fill_manual(legend_title, values=c("red","blue"), labels = c("Trump", "Clinton"))
print(p)

#Acknowledgements: This algorithm was adapted from Jeffrey Breen's Mining Twitter for Airline Consumer Sentiment article. You can find it here: http://www.inside-r.org/howto/mining-twitter-airline-consumer-sentiment. 

#Reference: Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing and Comparing Opinions on the Web." Proceedings of the 14th International World Wide Web conference (WWW-2005), May 10-14, 2005, Chiba, Japan.

