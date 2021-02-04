# About this repo:
Welcome to the Text-Analysis repository for Cyberinfrastructure for Digital Humanities and Creative Activities. To get started you'll need to click the green clone or download button and choose Download ZIP. This should download the repository as a .zip file to the folder of your choice. Whether you're on Research Desktop (ReD) here at Indiana University (IU) or on your own system, you will want to download and open the respository in your home directory. On ReD this is your Carbonate folder. It is marked on the Desktop as "username's home" and the folder is embossed with a little house. On Mac the home directory is usually in Users/yourUserName and on a PC it is usually the C: drive.

Already familiar with Python and don't really need any help? Then go ahead and dive right in with our introductory Python [word frequency](https://github.com/cyberdh/Text-Analysis/tree/master/WordFrequencies) scripts. Once in the WordFrequencies folder choose the algorithm/output you want (ngrams, StackedAreaGraphs, wordClouds, histograms) then choose the scripts folder. They have minimal directions and are ready to go.

For those who are new to Python and need a little assistance, please see our introductory Jupyter Notebooks in the [WordFrequencies](https://github.com/cyberdh/Text-Analysis/tree/master/WordFrequencies) folder. As with the scripts, first choose the algorithm/output you want then choose the notebooks folder. These notebooks go into more detail about the code and what it does with sample output.

We have notebooks and scripts for: 
* text preparation
* wordclouds (plain text and twitter)
* ngram wordclouds (plain text and twitter)
* top ten words (plain text and twitter)
* stacked area graphs (plain text and twitter)

## More Advanced Topics

#### Please note: These topics utilize two separate notebooks for each tool/algorithm within the topics. One notebook is for cleaning/acquiring the data and another notebook is for visual representation using the data provided by the other notebook. This has been done to help you save time by not having to re-run the data through the algorithm(s) everytime you simply want to make a change to the visualizations. In addition, this improves reproducibility of the results, especially for the topic modeling.

### Sentiment Analysis
Jupyter Notebooks for [sentiment analysis](https://github.com/cyberdh/Text-Analysis/tree/master/VADERSentimentAnalysis) using Twitter, adapted from VADER (1). 

(1). Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

### Topic Modeling 
Jupyter Notebooks using
* [LDA](https://github.com/cyberdh/Text-Analysis/tree/master/TopicModeling/LDA)
* [LSA](https://github.com/cyberdh/Text-Analysis/tree/master/TopicModeling/LSA)
* [word vectors](https://github.com/cyberdh/Text-Analysis/tree/master/TopicModeling/Word2Vec) 


#### Please note: The code in this repo is set up for use on Carbonate, the supercomputer at Indiana University, via Research Desktop (ReD). Carbonate is a Linux system and uses Python 2.7 or 3.6 and so some of this code may need to be altered if you are using a different version of Python on another computer. The Python code in this repo is all Python 3.
