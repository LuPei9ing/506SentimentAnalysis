# 506SentimentAnalysis

The objective of this project is to understand the media coverage (news and social media) and the public response to the to the legislative agenda of Martin J. Walsh, the 54th Mayor of Boston. This implies understanding which of the agenda’s priorities were covered by mainstream media, in what quantity, the time of response of mainstream media when covering them with respect to the press release, and the public’s general sentiment regarding such topics.

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
* Scraper is the scraper we used to scrape data.
* Statistic is the code for statistic analysis.
* data processing includes the code for filtering and cleaning the data.
* sentiment includes 3 methods of sentiment analysis, including textblob and vader, lstm for twitter data, gluon LNP for mainstream media.
* topic extraction includes the code to identify the priority from press release of City of Boston.

* To run code on LSTM:
  >1. Download data from <br>
     https://www.kaggle.com/kazanova/sentiment140#training.1600000.processed.noemoticon.csv <br>
     and add it under folder /lstm_model/data
  >2. If you want to train the model by you own, run 'python twitter_model.py' under folder /lstm_model.
  >3. If you want to use the model we have already trained, download them from <br>
      https://drive.google.com/file/d/1leABsjuNDAttt5MFwFGSK9vAVQe59bBv/view?usp=sharing <br>
      and add files under folder /lstm_model/model, then run 'python twitter_model.py'



