library(tidytext)
library(dplyr)
library(fuzzyjoin)
library(tm)


setwd <- "~/Text-Analysis"
corpus <- scan("data/shakespeareFolger/Hamlet.txt", what="character", sep="\n")
myStopWords <- scan("data/earlyModernStopword.txt", what="character", sep="\n")

#clean corpus
mycorpus <- tolower(corpus)
mycorpus <- removePunctuation(mycorpus)
mycorpus <- stripWhitespace(mycorpus)
mycorpus <- removeWords(mycorpus, myStopWords)

#tokenize the corpus into a data.frame where each row is one word
all_words <- data_frame(text = mycorpus) %>%
  unnest_tokens(word, text) %>%
#add a position column
  mutate(position = row_number()) %>%
#remove regular english stopwords from the tm package
  filter(!word %in% tm::stopwords("en"))

nearby_words <- all_words %>%
  filter(word == "love") %>%
  #filter(word %in% c("father", "good"))
  select(focus_term = word, focus_position = position) %>%
  difference_inner_join(all_words, by = c(focus_position = "position"), max_dist = 10) %>%
  mutate(distance = abs(focus_position - position))

words_summarized <- nearby_words %>%
  group_by(word) %>%
  #group_by(focus_term, word)
  summarize(number = n(),
            maximum_distance = max(distance),
            minimum_distance = min(distance),
            average_distance = mean(distance)) %>%
  arrange(desc(number))
write.csv(words_summarized, file = "ChooseAnyNameYouWant.csv")
print(words_summarized)
#NOTE: The term of interest counts itself, and so the numbers for your chosen word are inflated.
#Much of this code was derived from David Robinson on stackoverflow who helped create the tidytext and fuzzyjoin packages in R.
