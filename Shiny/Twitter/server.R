library(shiny)

# Define server logic required to draw a histogram

library(wordcloud)
library(qdap)
library(RColorBrewer)
source("helpers.R")


shinyServer(function(input, output) {
  wordcloud_rep <- repeatable(wordcloud)
  
  #FIX MIN.FREQ PART - MAKE IT WORK
  output$plot <- renderPlot({
    wordcloud_rep(words,freqs,scale=c(5,1.25),min.freq=input$freq,max.words=input$range, rot.per=0, 
              colors=cols)
  })


  })



