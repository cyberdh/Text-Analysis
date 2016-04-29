library(shiny)
library(wordcloud)
library(qdap)
library(RColorBrewer)


source("helpers.R")



# setwd("~/Documents/IU/CyberDH/Text_Analysis/Shiny/Twitter")

#source("helpers.R")


ui <- fluidPage(
  titlePanel("Twitter Conversation After the Death of Prince"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("This interactive plot shows the most frequently tweeted words in reference to the death of the musician Price on April 22, 2016"),
      sliderInput("freq", 
                  label = "Minimum frequency of words:",
                  min = 1, max = 400, value = 3),

      sliderInput("range", 
                  label = "Number of Words:",
                  min = 5, max = 200, value = 50)
      
    ),
    
    mainPanel(
      plotOutput("plot")
    )
  )
  
)

server <- function(input, output) {
  
  #words <- read.csv("words.csv", sep= ",")
  #freqs <- read.csv("freqs.csv", sep= ",")
  
  cols <- colorRampPalette(brewer.pal(12,"Paired"))(500)

  wordcloud_rep <- repeatable(wordcloud)
  
  output$plot <- renderPlot({
    wordcloud_rep(words,freqs, scale=c(4,1),min.freq=input$freq,max.words=input$range, rot.per=0, 
                  colors=cols)
  })
  
  
}

shinyApp(ui = ui, server = server)
