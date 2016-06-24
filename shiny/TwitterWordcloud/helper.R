

setwd("~/Documents/IU/CyberDH/Text_Analysis/Shiny/Twitter")

words <- read.csv("words.csv", sep= ",")
freqs <- read.csv("freqs.csv", sep= ",")
cols <- colorRampPalette(brewer.pal(12,"Paired"))(500)
