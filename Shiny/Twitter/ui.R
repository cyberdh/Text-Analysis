library (shiny)

# Define UI for application that draws a histogram
shinyUI(fluidPage(
  titlePanel("Twitter Conversation on the Brussels Attack"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("This interactive plot shows the most frequently tweeted words in reference to the Brussels attack on March 22, 2016"),

      #FIX THIS PART
      sliderInput("freq", 
                  label = "Frequency of Words:",
                  min = 1, max = 20, value = 20),
      sliderInput("range", 
                  label = "Number of Words:",
                  min = 1, max = 100, value = 50),
      
      helpText("CYBERDH LOGO??")
    
  ),
    
    mainPanel(
      plotOutput("plot")
    )
  )

))