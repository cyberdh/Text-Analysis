# Text Analysis Toolkit
For all kinds of textual analysis: literary, social media, surveys...


----
Our group has been developing an open instructional workflow for text analysis that aims to build understanding and basic coding skills before scaling up analyses. We have chosen to bootstrap in R because of its statistical and graphical capabilities and because of its wealth of domain-specific packages. Moreover, the open source and scripting nature of R allows for methods that are repeatable, extensible, scalable, and sustainable. The aim is to provide code templates that can be adapted, remixed, and scaled to fit a wide range of text analysis tasks.

----
### What is in this repo?

1. RNotebooks: heavily annotated to explain each line of code.
2. RScripts: lightly annotated to allow the user to experiment.
3. Data: need to replicate our results.*

----
### Getting Started

The suggested workflow is to fork the repository for your own use. Read the [RNotebook](https://github.com/cyberdh/Text-Analysis/tree/master/RNotebooks) as it explains how a given script works, line by line. Then load the lightly annotated script that goes along with the notebook and try it out for yourself in RStudio. Suggestions on alterations and basic parameter tweaking are provided in the script.


*So that you can replicate our work, we have provided all the data we have used in our examples. For plain text notebooks and scripts, we use the Shakespearean corpus from the [Visualizing English Print Project](http://graphics.cs.wisc.edu/WP/vep/) where speaker names and stage directions are removed; for Twitter notebooks and scripts, we provide Twitter data that has been harvested by the team.

[Text Preparation](https://github.com/cyberdh/Text-Analysis/blob/master/RNotebooks/textPrep.pdf)
* While the methods below offer new insights to corpora, cleaning and prepping your text is key to reliable results. This tutorial goes through the basics of getting your corpus ready for analysis.

Word Clouds

* [Plain Text](https://github.com/cyberdh/Text-Analysis/blob/master/RNotebooks/wordcloudPlainText.Rmd)

* [Twitter](https://github.com/cyberdh/Text-Analysis/blob/master/RNotebooks/wordcloudTwitter.Rmd)

* Word clouds may seem simplistic, they offer a wealth of information that is easily parseable at a glance.

[Word Co-ocurrence](https://github.com/cyberdh/Text-Analysis/blob/master/RNotebooks/cooccurrencePlainText.Rmd)

* The co-occurrence script aims to discover the semantic proximity of two words throughout the Shakespeare Drama Corpus. At the end, it will take in a word of the user’s choice and find the top ten closest terms by proximity.

[Sentiment Analysis](https://github.com/cyberdh/Text-Analysis/blob/master/RNotebooks/sentPolitical.Rmd)

* Sentiment determines whether a tweeter feels negatively or positively about a topic by comparing the words in a tweet to a lexicon of words that have positive valences or negative ones. By analyzing sentiment scores, we can determine how English-language twitter users feel about a topic.

---
