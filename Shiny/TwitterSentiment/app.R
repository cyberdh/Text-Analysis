#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

setwd("~/Documents/IU/CyberDH/Text_Analysis/Shiny/TwitterSentiment")

library(twitteR)
library(plyr)
library(stringr)
library(ggplot2)
library(reshape2)
library(tm)
# source("helpers.R") - this script reads in final data frames instead of the raw data

# Define UI for application that draws a histogram
ui <- shinyUI(fluidPage(
   
   # Application title
   titlePanel("Simple Sentiment Analysis with Political Data from Twitter"),
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
      sidebarPanel(
        radioButtons(inputId="data_set", label = "Choose a candidate:", choices = c("Donald Trump", "Hillary Clinton", "Compare both candidates"), selected = "Compare both candidates")
      ),
      
      # Show a plot of the generated distribution
      mainPanel(
         plotOutput("plot")
      )
   )
))

# Define server logic required to draw a histogram
server <- shinyServer(function(input, output) {
   
  trump <- read.csv(file="TrumpResultDF.csv",head=TRUE,sep=",")
  clinton <- read.csv(file="ClintonResultDF.csv",head=TRUE,sep=",")
  both <- read.csv(file="BothResultDF.csv",head=TRUE,sep=",")
  
  output$plot <- renderPlot({
      if (input$data_set == "Donald Trump") {
        ggplot(melt(trump), aes(value, fill=variable)) + geom_histogram(position = "dodge", binwidth = .5, fill = "red") + xlab("Sentiment Score") + ylab("Number of Tweets") + ggtitle("Sentiment Scoring of Tweets Mentioning @RealDonaldTrump") + xlim(c(-7,7)) + scale_x_continuous(breaks=pretty(trump$x.score, n=14))
      }
     else if (input$data_set == "Hillary Clinton") {
       ggplot(melt(clinton), aes(value, fill=variable)) + geom_histogram(position = "dodge", binwidth = .5, fill = "blue") + xlab("Sentiment Score") + ylab("Number of Tweets") + ggtitle("Sentiment Scoring of Tweets Mentioning @HillaryClinton") + xlim(c(-7,7)) + scale_x_continuous(breaks=pretty(clinton$x.score, n=14))
     }
     else if (input$data_set == "Compare both candidates") {
       legend_title <- "Candidate"
       ggplot(melt(both), aes(value, fill=variable)) + 
         geom_histogram(position = "dodge", binwidth = .5 ) + xlab("Sentiment Score") + 
         ylab("Number of Tweets") + ggtitle("Sentiment Scoring of Tweets Mentioning @RealDonaldTrump and @HillaryClinton") + 
         xlim(c(-7,7)) + scale_x_continuous(breaks=pretty(both$x.score, n=14)) + 
         scale_fill_manual(legend_title, values=c("red","blue"), labels = c("Trump", "Clinton"))
     }
   })
})


# Run the application 
shinyApp(ui = ui, server = server)

