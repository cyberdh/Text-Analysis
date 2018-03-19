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

# based on the observation that the distance of a focus word to itself is 0,
# we simply remove it by apply following filter
nearby_words = filter(nearby_words, distance != 0)

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
#NOTE: In this code, the counting starts with the word at the 0 position and counts out from there. So 0 position is word 1 up
# to your specified distance. The code does not start counting with the word immediately preceding and  the word immediately
# following the word at the 0 position.

#Much of this code was derived from David Robinson on stackoverflow who helped create the tidytext and fuzzyjoin packages in R.
