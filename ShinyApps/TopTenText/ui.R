fluidPage(
  # Application title
  titlePanel("Top Ten Words in a Text"),
  
  sidebarLayout(
    # Sidebar with a slider and selection inputs
    sidebarPanel(
      selectInput("selection", "Choose a play:",
                  choices = plays),
      selectInput("selection2", "Choose a play:",
                  choices = plays),
      actionButton("update", "Change"),
      hr()
    ),
    
    # Show Word Cloud
    mainPanel(
      plotOutput("plot1"),
      plotOutput("plot2")
    )
  )
)