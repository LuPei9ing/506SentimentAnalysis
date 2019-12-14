# 506SentimentAnalysis

The objective of this project is to understand the media coverage (news and social media) and the public response to the to the legislative agenda of Martin J. Walsh, the 54th Mayor of Boston. This implies understanding which of the agenda’s priorities were covered by mainstream media, in what quantity, the time of response of mainstream media when covering them with respect to the press release, and the public’s general sentiment regarding such topics.

## A couple of disclaimers...

1. This file simply provides the steps required to run the mainstream media model and it's not the documentation of our project. If you want to find out more about our approach, our experiments and our results please check our _\_Poster.pdf_ (created by @FaizGanz) or our _\_Report.pdf_ file. 

2. No datasets are have been uploaded to this repo, but if you would like to test our model, without having to run our Scraper first, feel free to contact me. 

3. You may need to modify some file path in the code to make it run correctly.

4. This repo just includes part of model and code used in this project, other part is at https://github.com/GiorgosKarantonis/CS-506-Mainstream-Media-Sentiment-Analysis 

## Requirements:
nltk==3.4.5
Scrapy==1.8.0
scrapy_splash==0.7.2
mxnet==1.6.0b20191207
Keras==2.3.1
pandas==0.25.3
gluonnlp==0.8.1
numpy==1.17.4
gensim==3.8.1
scikit_learn==0.22
textblob==0.15.3

## Code Structure:

* src folder includes all of the data about our project.

* Models includes some pre-train model files.

* Statistic is the code for statistic analysis.

* lstm folder includes lstm for twitter data, gluon LNP for mainstream media.


## Running the code

### Preparation

1. Clone or download the repo and _cd_ to its local directory. 

2. Run _pip3 install -r requirements.txt_ to download all the dependancies. 

3. Download pre-trained model file here: https://drive.google.com/file/d/1oT3FfvOI8feDJQS7jr5jgCLylyqEOQ3J/view?usp=sharing

4. Unpack the zip file above in the src, into a folder named Models

5. To run code on LSTM:
  >1. Download data from <br>
     https://www.kaggle.com/kazanova/sentiment140#training.1600000.processed.noemoticon.csv <br>
     and add it under folder /lstm_model/data
  >2. If you want to use the model we have already trained, download them from <br>
      https://drive.google.com/file/d/1leABsjuNDAttt5MFwFGSK9vAVQe59bBv/view?usp=sharing <br>
      and add files under folder /lstm_model/model, then run 'python twitter_model.py'

### Running the model

To run the preprocessing and sentiment analysis model just _cd_ to the _src_ folder and run the following commands: 

1. python3 data\_process.py to clean, tokenize, stemming on the data.

2. python3 lda.py using LDA and NMF algorithm to extract topics from text.

3. python3 sentiment\_textblob.py sentiment analysis based on Textblob and Vader.

4. python3 twitter_model.py under folder /lstm to run LSTM model for sentiment analysis.

5. python3 get_mayor_related_data.py a simple data filter.

6. python3 lemmatization.py to apply lemmatization on data.
