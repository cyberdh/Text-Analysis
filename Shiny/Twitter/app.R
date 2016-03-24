library(shiny)
library(wordcloud)
library(qdap)
library(RColorBrewer)

setwd("~/Documents/IU/CyberDH/Text_Analysis/Shiny/Twitter")
source("helpers.R")

ui <- fluidPage(
  titlePanel("Twitter Conversation on the Brussels Attack"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("This interactive plot shows the most frequently tweeted words in reference to the Brussels attack on March 22, 2016"),
      sliderInput("freq", 
                  label = "Minimum frequency of words:",
                  min = 1, max = 100, value = 3),

      sliderInput("range", 
                  label = "Number of Words:",
                  min = 1, max = 100, value = 50)
      
    ),
    
    mainPanel(
      plotOutput("plot")
    )
  )
  
)

server <- function(input, output) {
  wordcloud_rep <- repeatable(wordcloud)
  
  output$plot <- renderPlot({
    wordcloud_rep(words,freqs,scale=c(5,1.25),min.freq=input$freq,max.words=input$range, rot.per=0, 
                  colors=cols)
  })
  
  
}

shinyApp(ui = ui, server = server)
