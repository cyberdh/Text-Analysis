library(shiny)
library(wordcloud)
library(qdap)
library(RColorBrewer)

<<<<<<< Updated upstream
source("helpers.R")
=======


setwd("~/Desktop/R/Text_Analysis/Shiny/Twitter")
#source("helpers.R")
>>>>>>> Stashed changes

ui <- fluidPage(
  titlePanel("Twitter Conversation on the Brussels Attack"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("This interactive plot shows the most frequently tweeted words in reference to the Brussels attack on March 22, 2016"),
      sliderInput("freq", 
                  label = "Minimum frequency of words:",
                  min = 1, max = 1020, value = 3),

      sliderInput("range", 
                  label = "Number of Words:",
                  min = 100, max = 500, value = 50)
      
    ),
    
    mainPanel(
      plotOutput("plot")
    )
  )
  
)

server <- function(input, output) {
  
<<<<<<< Updated upstream
=======
  
  words <- read.csv("words.csv", sep= ",")
  freqs <- read.csv("freqs.csv", sep= ",")
  
  cols <- colorRampPalette(brewer.pal(12,"Paired"))(500)
>>>>>>> Stashed changes
  wordcloud_rep <- repeatable(wordcloud)
  
  output$plot <- renderPlot({
    wordcloud_rep(words,freqs,scale=c(4,1),min.freq=input$freq,max.words=input$range, rot.per=0, 
                  colors=cols)
  })
  
  
}

shinyApp(ui = ui, server = server)
