library(shiny)
library(rsconnect)
library(wordcloud)
library(qdap)
library(RColorBrewer)

#setwd("~/Desktop/R/Text_Analysis/Shiny/Twitter")

source("helpers.R")


ui <- fluidPage(
  titlePanel("Twitter Conversation After the Shooting at the Pulse Nightclub"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("This interactive plot shows the most frequently tweeted words in reference to the shooting at the Pulse Nightclub"),
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
  
  cols <- colorRampPalette(brewer.pal(12,"Paired"))(500)

  wordcloud_rep <- repeatable(wordcloud)
  
  output$plot <- renderPlot({

    wordcloud_rep(words,freqs,scale=c(5,1),max.words=75, rot.per=0, 
                     colors=brewer.pal(8, "Dark2"))
  })
  
  
}

shinyApp(ui = ui, server = server)
