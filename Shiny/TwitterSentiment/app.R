#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

setwd("~/Documents/IU/CyberDH/Text_Analysis/Shiny/TwitterSentiment")

library(shiny)
source("helpers.R")

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
   
   output$plot <- renderPlot({
      if (input$data_set == "Donald Trump") {
        plot(ggplot(melt(trump.result), aes(value, fill=variable) + geom_histogram(position = "dodge") + xlab("Sentiment Score") + ylab("Number of Tweets") + ggtitle("Sentiment Scoring of Tweets Mentioning @RealDonaldTrump")) )
      }
     else if (input$data_set == "Hillary Clinton") {
       plot(ggplot(melt(clinton.result), aes(value, fill=variable) + geom_histogram(position = "dodge") + xlab("Sentiment Score") + ylab("Number of Tweets") + ggtitle("Sentiment Scoring of Tweets Mentioning @HillaryClinton")) )
     }
     else if (input$data_set == "Compare both candidates") {
       plot(ggplot(melt(both.result), aes(value, fill=variable) + geom_histogram(position = "dodge") + xlab("Sentiment Score") + ylab("Number of Tweets") + ggtitle("Sentiment Scoring of Tweets Mentioning @HillaryClinton")) )
     }

     
 
     

   })
})

# Run the application 
shinyApp(ui = ui, server = server)

