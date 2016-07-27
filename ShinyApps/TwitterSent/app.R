library(shiny)
library(wordcloud)
library(qdap)
library(RColorBrewer)

setwd("~/Documents/IU/CyberDH/Text_Analysis/")


ui <- fluidPage(
  titlePanel("Political Sentiment on Twitter"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("This interactive plot shows the sentiment of Tweets concerning the four presidential election front-runners"),
      textInput("posWords", "Positive words", "happy"),
      
      textInput("negWords", "Negative words", "sad"),
      actionButton('addPos', 'add'),
      actionButton('addNeg', 'add')
      
    ),
    
    mainPanel(
      plotOutput("plot")
    )
  )
  
)

server <- function(input, output) {
  
  posValues <- reactiveValues()
  negValues <- reactiveValues()
  
  library(twitteR)
  library(plyr)
  require(stringr)
  
  # Global Parameters

  
  #Source Multiplot Function
  source("RScripts/multiplot.R")
  
  # Load Data
  clinton.tweets <- readRDS("data/twitter/tweetsclinton.RData")
  cruz.tweets <- readRDS("data/twitter/tweetscruz.RData")
  sanders.tweets <- readRDS("data/twitter/tweetssanders.RData")
  trump.tweets <- readRDS("data/twitter/tweetstrump.RData")
  
  
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
  
  lex.pos = scan('data/opinionLexicon/positive-words.txt', what='character', comment.char = ';')
  lex.neg = scan('data/opinionLexicon/negative-words.txt', what='character', comment.char = ';')
  
  # add words using the c() [combine] function
  pos.words = c(lex.pos, input$posWords)
  neg.words = c(lex.neg, input$negWords)
  
  # Implement Sentiment Scoring Algorithm
  score.sentiment = function(tweets, pos.words, neg.words, .progress='none')
  {
    
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
                       main = "Sentiment of @HillaryClinton on Twitter", 
                       xlab= "Valence of Sentiment (Tweet Score)", ylab="Count (Tweets)")
  cruz.plot = qplot(cruz.result$score, xlim=(c(-7,7)),
                    main = "Sentiment of @tedcruz on Twitter",
                    xlab= "Valence of Sentiment (Tweet Score)", ylab="Count (Tweets)")
  sanders.plot = qplot(sanders.result$score, xlim=(c(-7,7)),
                       main = "Sentiment of @BernieSanders on Twitter", xlab= "Valence of Sentiment (Tweet Score)", ylab="Count (Tweets)")
  trump.plot = qplot(trump.result$score, xlim=(c(-7,7)),
                     main = "Sentiment of @realDonaldTrump on Twitter", xlab= "Valence of Sentiment (Tweet Score)", ylab="Count (Tweets)")
  
  
  output$plot <- renderPlot({
    multiplot(clinton.plot, sanders.plot, trump.plot, cruz.plot, cols=2)
  })
  
  
}

shinyApp(ui = ui, server = server)
