# Simple Sentiment Analysis
# Using comments from the 2017 UITS Survey.
# To be used in conjunction with the CyberDH RNotebook tutorial found on Github > CyberDH > Text_Analysis.

library(tm)
library(plyr)
library(stringr)
library(ggplot2)

# Global Parameters
setwd("~/Text-Analysis/")



# Load Data
faculty.uits <- read.csv("data/survey/IUBfaculty.csv")
staff.uits <- read.csv("data/survey/IUBstaff.csv")
grad.uits <- read.csv("data/survey/IUBgrad.csv")
undergrad.uits <- read.csv("data/survey/IUBundergrad.csv")


# Inspect Data
class(faculty.uits)
length(faculty.uits)
faculty.uits[1]
head(faculty.uits)


# Extract Text
faculty.text = faculty.uits$text
staff.text = staff.uits$text
grad.text = grad.uits$text
undergrad.text = undergrad.uits$text


# Loading Opinion Lexicon

# used Hu and Liu, 2004 http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
# downloads as a .rar compressed file
# if using Windows machine, should be able to unzip file
# if using Mac, download RAR Extractor Free (by qing qing yu) from the App Store
# open RAR Extractor Free and choose your settings, then drag downloaded .rar file to the Extractor
#   icon and it will unzip to the location you specified in settings

lex.pos = scan('data/opinionLexicon/positive-words.txt', what='character', comment.char = ';')
lex.neg = scan('data/opinionLexicon/negative-words.txt', what='character', comment.char = ';')

#add words using the c() [combine] function
pos.words = lex.pos
neg.words = lex.neg
pos.words <- removeWords(pos.words, c('work', 'secure', 'support'))
neg.words <- removeWords(neg.words, c('issue', 'issues', 'problem', 'problems', 'cloud'))

# Implement Sentiment Scoring Algorithm
score.sentiment = function(contents,pos.words, neg.words, .progress='none')
{
  
  #figure out the score for each tweet specifically
  scores = laply(contents, function(content, pos.words, neg.words) {
    #normalize tweet text
    content = gsub('[[:punct:]]', '', content)
    content = gsub('[[:cntrl:]]', '', content)
    content = gsub('\\d+', '', content)
    
    #REMOVE EMOJIS!
    content = iconv(content, "ASCII", "UTF-8", sub="")
    
    content.lower = tolower(content)
    
    #split list into separate words
    word.list = str_split(content.lower, '\\s+')
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
  scores.df = data.frame(score=scores, text = contents)
  return(scores.df)
}


# Algorithm Testing
sample = c("This ice cream is the best! I love this flavor!", "I am so angry at the terrible weather today. Frustrated.", "Wow, spectacular, I wish I could be as perfect as you.")
sample.result = score.sentiment(sample, pos.words, neg.words)
sample.result


# Scoring Twitter Data
faculty.result = score.sentiment(faculty.text, pos.words, neg.words)
staff.result = score.sentiment(staff.text, pos.words, neg.words)
grad.result = score.sentiment(grad.text, pos.words, neg.words)
undergrad.result = score.sentiment(undergrad.text, pos.words, neg.words)

faculty.result$group = 'Faculty'
staff.result$group = 'Staff'
grad.result$group = 'Grad'
undergrad.result$group = 'Undergrad'

# Peeking at results (run each of the following four lines one at a time)
head(faculty.result)

head(staff.result)

head(grad.result)

head(undergrad.result)

#Plotting Twitter Data
options(digits=3)
par(mfrow=c(2,2))
p1 = hist(faculty.result$score, col = "darkblue", ylim = c(0,80),xlim=c(-17,17), 
                     main = "Sentiment Scoring from the 2017 UITS Survey, IUB", 
                     xlab= "Sentiment Score", ylab="Number of Responses", breaks = seq(-17,17),labels=TRUE, axes = FALSE,xaxt = 'n')
axis(side=1, at = p1$mids, labels = seq(-16,17,1), las = 2)
abline(v = mean(faculty.result$score)-.5, col = "purple", lwd = 2, untf = TRUE)
abline(v = 0-.5, col = "black", lwd = 2)
facMean <- mean(faculty.result$score)
facSD <- sd(faculty.result$score)
fa= list( bquote(Mean== .(facMean)), bquote(SD== .(facSD) ) )
legend("topright", c("Faculty", "Mean", "Zero", sapply(fa, as.expression)) , col = c("darkblue", "purple", "black", "white","white"), lwd=c(8, 4, 4,1,1), cex=.5, pt.cex=.5)
#legend('topleft', legend=sapply(fa, as.expression))

p2 = hist(staff.result$score, col = "darkred", ylim = c(0,80),xlim=c(-17,17),
                  main = "Sentiment Scoring from the 2017 UITS Survey, IUB",
                  xlab= "Sentiment Score", ylab="Number of Responses", breaks = seq(-17,17),labels=TRUE, xaxt = 'n')
axis(side=1, at=p2$mids, labels = seq(-16,17,1), las = 2)
abline(v = mean(staff.result$score)-.5, col = "purple", lwd = 2)
abline(v = 0-.5, col = "black", lwd = 2)
stfMean <- mean(staff.result$score)
stfSD <- sd(staff.result$score)
st= list( bquote(Mean== .(stfMean)), bquote(SD== .(stfSD) ) )
legend("topright", c("Staff", "Mean", "Zero", sapply(st, as.expression)) , col = c("darkred", "purple", "black", "white", "white"), lwd=c(8, 4, 4), cex=.5, pt.cex=.5)
#legend('topleft', legend=sapply(st, as.expression))

p3 = hist(grad.result$score, col = "darkorange", ylim =c(0,80),xlim=c(-17,17),
                    main = "Sentiment Scoring from the 2017 UITS Survey, IUB", 
                    xlab= "Sentiment Score", ylab="Number of Responses", breaks = seq(-17,17),labels=TRUE, xaxt = 'n')
axis(side=1, at=p3$mids, labels = seq(-16,17,1), las = 2)
abline(v = mean(grad.result$score)-.5, col = "purple", lwd = 2)
abline(v = 0-.5, col = "black", lwd = 2)
grdMean <- mean(grad.result$score)
grdSD <- sd(grad.result$score)
g= list( bquote(Mean== .(grdMean)), bquote(SD== .(grdSD) ) )
legend("topright", c("Grad", "Mean", "Zero", sapply(g, as.expression)) , col = c("darkorange", "purple", "black", "white", "white"), lwd=c(8, 4, 4), cex=.5, pt.cex=.5)
#legend('topleft', legend=sapply(g, as.expression))

p4 = hist(undergrad.result$score, col = "darkgreen", ylim = c(0,80),xlim=c(-17,17),
                   main = "Sentiment Scoring from the 2017 UITS Survey, IUB", 
                   xlab= "Sentiment Score", ylab="Number of Responses", breaks = seq(-17,17),labels=TRUE, xaxt = 'n')
axis(side=1, at=p4$mids, labels = seq(-16,17,1), las = 2)
abline(v = mean(undergrad.result$score)-.5, col = "purple", lwd = 2)
abline(v = 0-.5, col = "black", lwd = 2)
ugrdMean <- mean(undergrad.result$score)
ugrdSD <- sd(undergrad.result$score)
ug= list( bquote(Mean== .(ugrdMean)), bquote(SD== .(ugrdSD) ) )
legend("topright", c("Undergrad", "Mean", "Zero", sapply(ug, as.expression)) , col = c("darkgreen", "purple", "black", "white", "white"), lwd=c(8, 4, 4), cex=.5, pt.cex=.5)
#legend('topleft', legend=sapply(ug, as.expression))



#########

# Acknowledgements: This algorithm was adapted from Jeffrey Breen's Mining Twitter for Airline Consumer Sentiment article. You can find it here: http://www.inside-r.org/howto/mining-twitter-airline-consumer-sentiment. 
# Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing and Comparing Opinions on the Web." Proceedings of the 14th International World Wide Web conference (WWW-2005), May 10-14, 2005, Chiba, Japan.
