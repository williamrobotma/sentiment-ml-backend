# -*- coding: utf-8 -*-
from terms import *

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
from math import log, sqrt
"""NLP_solution

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pAmvY3BJwsf0Cb92DUPIDLRrLCcGdg-t
"""
sem_classifier = None
tech_classifier = None
bank_classifier = None
online_classifier = None
sc_tf_idf = None
import re, string, random

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

def process_nlp():
    from nltk.corpus import twitter_samples, stopwords
    from nltk.tokenize import word_tokenize
    global sem_classifier 
    global tech_classifier 
    global bank_classifier 
    global online_classifier 
    global sc_tf_idf 
    
    load_file = "banktweetsDataList.txt"
    #load_file = "RBC_googleplaydata.txt.txt"
    train_test_split = 3000

    import nltk
    nltk.download('twitter_samples')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    nltk.download('punkt')

    """##SENTIMENT ANALYSIS"""




    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    text = twitter_samples.strings('tweets.20150430-223406.json')
    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    freq_dist_pos = FreqDist(all_pos_words)
    print(freq_dist_pos.most_common(10))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                         for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    sem_classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(sem_classifier, test_data))

    print(sem_classifier.show_most_informative_features(10))

    custom_tweet = "I ordered just once from TerribleCo, they screwed up, never used the app again."

    custom_tokens = remove_noise(word_tokenize(custom_tweet))

    print(custom_tweet, sem_classifier.classify(dict([token, True] for token in custom_tokens)))

    custom_tweet = "My daughter has been at MEM airport for almost 7 hours trying to fly #unitedAIRLINES to houston. #unitedair what are you going to do???"

    custom_tokens = remove_noise(word_tokenize(custom_tweet))

    print(custom_tweet, sem_classifier.classify(dict([token, True] for token in custom_tokens)))

    """##Technical and Non techincal extraction"""

    from nltk.tokenize import sent_tokenize, word_tokenize

    #with open("rbcDataList.txt") as f:
    with open(load_file) as f:
      lines = f.readlines()
    print(lines[1])

    technical_tweets = []
    non_technical_tweets = []

    banking_tweets = []
    insurance_tweets = []
    bi_unkown = []

    online_tweets = []
    offline_tweets = []
    oo_unkown = []

    tokens_technical_tweets = []
    tokens_non_technical_tweets = []

    all_terms = techincal_terms + onsite_terms + online_terms + banking_terms + insurance_terms

    for line in lines:
      lowercase = line.lower()
      tech = False
      for term in all_terms:
        if term in line:
          technical_tweets.append(line)
          tokens_technical_tweets.append(word_tokenize(line))
          tech = True
      if tech == False:
          non_technical_tweets.append(line)
          tokens_non_technical_tweets.append(word_tokenize(line))

    clean_technical_tweets = []
    clean_non_technical_tweets = []

    for tokens in tokens_technical_tweets:
      clean_technical_tweets.append(remove_noise(tokens, stop_words))

    for tokens in tokens_non_technical_tweets:
      clean_non_technical_tweets.append(remove_noise(tokens, stop_words))

    technical_tokens_for_model = get_tweets_for_model(clean_technical_tweets)
    non_technical_tokens_for_model = get_tweets_for_model(clean_non_technical_tweets)

    technical_dataset = [(tweet_dict, "Technical") for tweet_dict in technical_tokens_for_model]
    non_technical_dataset = [(tweet_dict, "Not Technical") for tweet_dict in non_technical_tokens_for_model]

    dataset = technical_dataset + non_technical_dataset

    random.shuffle(dataset)

    train_data = dataset[:train_test_split]
    test_data = dataset[train_test_split:]

    tech_classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(tech_classifier, test_data))

    print(tech_classifier.show_most_informative_features(10))

    custom_tweet = "Hey @RBC. You may need to update your website for this credit card lol. 2017 is a long time ago. https://t.co/r80qf9FuWr"

    custom_tokens = remove_noise(word_tokenize(custom_tweet))

    print(custom_tweet, tech_classifier.classify(dict([token, True] for token in custom_tokens)))

    """##BANKING VS INSURANCE TWEETS"""

    banking_tweets = []
    insurance_tweets = []
    bi_unkown = []

    token_banking_tweets = []
    token_insurance_tweets = []
    token_bi_unkown = []

    for tweet in technical_tweets:
      line = tweet.lower()
      match = False
      for term in banking_terms:
        if term in line:
          banking_tweets.append(line)
          token_banking_tweets.append(word_tokenize(line))
          match = True
      for term in insurance_terms:
        if term in line:
          insurance_tweets.append(line)
          token_insurance_tweets.append(word_tokenize(line))
          match = True
      if match == False:
        bi_unkown.append(line)
        token_bi_unkown.append(word_tokenize(line))

    clean_banking_tweets = []
    clean_insurance_tweets = []
    clean_bi_unkown = []

    for tokens in token_banking_tweets:
      clean_banking_tweets.append(remove_noise(tokens, stop_words))

    for tokens in token_insurance_tweets:
      clean_insurance_tweets.append(remove_noise(tokens, stop_words))

    for tokens in token_bi_unkown:
      clean_bi_unkown.append(remove_noise(tokens, stop_words))

    token_banking_tweets_model = get_tweets_for_model(clean_banking_tweets)
    token_insurance_tweets_model = get_tweets_for_model(clean_insurance_tweets)
    token_bi_unkown_model = get_tweets_for_model(clean_bi_unkown)

    banking_dataset = [(tweet_dict, "Banking") for tweet_dict in token_banking_tweets_model]
    insurance_dataset = [(tweet_dict, "Insurance") for tweet_dict in token_insurance_tweets_model]
    bi_unkown_dataset = [(tweet_dict, "Unkown") for tweet_dict in token_bi_unkown_model]

    dataset = banking_dataset + insurance_dataset + bi_unkown_dataset

    random.shuffle(dataset)

    train_data = dataset[:train_test_split]
    test_data = dataset[train_test_split:]

    bank_classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(bank_classifier, test_data))

    print(bank_classifier.show_most_informative_features(10))

    """##ONLINE VS ONSITE"""

    online_tweets = []
    onsite_tweets = []
    oo_unkown = []

    token_online_tweets = []
    token_onsite_tweets = []
    token_oo_unkown = []

    for tweet in technical_tweets:
      line = tweet.lower()
      match = False
      for term in online_terms:
        if term in line:
          online_tweets.append(line)
          token_online_tweets.append(word_tokenize(line))
          match = True
      for term in onsite_terms:
        if term in line:
          onsite_tweets.append(line)
          token_onsite_tweets.append(word_tokenize(line))
          match = True
      if match == False:
        oo_unkown.append(line)
        token_oo_unkown.append(word_tokenize(line))

    clean_online_tweets = []
    clean_onsite_tweets = []
    clean_oo_unkown = []

    for tokens in token_online_tweets:
      clean_online_tweets.append(remove_noise(tokens, stop_words))

    for tokens in token_onsite_tweets:
      clean_onsite_tweets.append(remove_noise(tokens, stop_words))

    for tokens in token_oo_unkown:
      clean_oo_unkown.append(remove_noise(tokens, stop_words))

    token_online_tweets_model = get_tweets_for_model(clean_online_tweets)
    token_onsite_tweets_model = get_tweets_for_model(clean_onsite_tweets)
    token_oo_unkown_model = get_tweets_for_model(clean_oo_unkown)

    online_dataset = [(tweet_dict, "Online") for tweet_dict in token_online_tweets_model]
    onsite_dataset = [(tweet_dict, "Onsite") for tweet_dict in token_onsite_tweets_model]
    oo_unkown_dataset = [(tweet_dict, "Unkown") for tweet_dict in token_oo_unkown_model]

    dataset = online_dataset + onsite_dataset + oo_unkown_dataset

    random.shuffle(dataset)

    train_data = dataset[:train_test_split]
    test_data = dataset[train_test_split:]

    online_classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(online_classifier, test_data))

    print(online_classifier.show_most_informative_features(10))

    """##SPAM VS NO SPAM"""

    # Commented out IPython magic to ensure Python compatibility.
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    from math import log, sqrt
    import pandas as pd
    import numpy as np
    import re
    # %matplotlib inline

    mails = pd.read_csv('spam.csv', encoding = 'latin-1')
    mails.head()

    mails.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis = 1, inplace = True)
    mails.head()

    mails.rename(columns = {'v1': 'labels', 'v2': 'message'}, inplace = True)
    mails.head()

    mails['labels'].value_counts()

    mails['label'] = mails['labels'].map({'ham': 0, 'spam': 1})
    mails.head()

    mails.drop(['labels'], axis = 1, inplace = True)
    mails.head()

    totalMails = 4825 + 747
    trainIndex, testIndex = list(), list()
    for i in range(mails.shape[0]):
        if np.random.uniform(0, 1) < 0.75:
            trainIndex += [i]
        else:
            testIndex += [i]
    trainData = mails.loc[trainIndex]
    testData = mails.loc[testIndex]

    trainData.reset_index(inplace = True)
    trainData.drop(['index'], axis = 1, inplace = True)
    trainData.head()

    testData.reset_index(inplace = True)
    testData.drop(['index'], axis = 1, inplace = True)
    testData.head()

    trainData['label'].value_counts()
    sc_tf_idf = SpamClassifier(trainData, 'tf-idf')
    sc_tf_idf.train()
    preds_tf_idf = sc_tf_idf.predict(testData['message'])
    metrics(testData['label'], preds_tf_idf)

    pm = process_message('@RBC @WPGHomeShows @Bryan_Baeumler I\xe2\x80\x99m here in branch trying to pay or US dollar RBC credit card and they won\xe2\x80\x99t eve\xe2\x80\xa6 https://t.co/vE8I15uYQ8')
    sc_tf_idf.classify(pm)
    """##Data for Tweets"""

    analyze_file("banktweetsDataList.txt")

    """##Data for RBC Banking"""

    analyze_file("RBC_banking_googleplaydata.txt")

    """##Data for RBC Insurance"""

    analyze_file("RBC_insurance_googleplaydata.txt")

    """##Data for RBC Investment"""

    analyze_file("investment_googleplaydata_master.txt")

def process_message(message, lower_case = True, stem = True, stop_words = True, gram = 2):
    if lower_case:
        message = message.lower()
    words = word_tokenize(message)
    words = [w for w in words if len(w) > 2]
    if gram > 1:
        w = []
        for i in range(len(words) - gram + 1):
            w += [' '.join(words[i:i + gram])]
        return w
    if stop_words:
        sw = stopwords.words('english')
        words = [word for word in words if word not in sw]
    if stem:
        stemmer = PorterStemmer()
        words = [stemmer.stem(word) for word in words]   
    return words

from math import log, sqrt
class SpamClassifier(object):
    def __init__(self, trainData, method = 'tf-idf'):
        self.mails, self.labels = trainData['message'], trainData['label']
        self.method = method

    def train(self):
        self.calc_TF_and_IDF()
        if self.method == 'tf-idf':
            self.calc_TF_IDF()
        else:
            self.calc_prob()

    def calc_prob(self):
        self.prob_spam = dict()
        self.prob_ham = dict()
        for word in self.tf_spam:
            self.prob_spam[word] = (self.tf_spam[word] + 1) / (self.spam_words + \
                                                                len(list(self.tf_spam.keys())))
        for word in self.tf_ham:
            self.prob_ham[word] = (self.tf_ham[word] + 1) / (self.ham_words + \
                                                                len(list(self.tf_ham.keys())))
        self.prob_spam_mail, self.prob_ham_mail = self.spam_mails / self.total_mails, self.ham_mails / self.total_mails 


    def calc_TF_and_IDF(self):
        noOfMessages = self.mails.shape[0]
        self.spam_mails, self.ham_mails = self.labels.value_counts()[1], self.labels.value_counts()[0]
        self.total_mails = self.spam_mails + self.ham_mails
        self.spam_words = 0
        self.ham_words = 0
        self.tf_spam = dict()
        self.tf_ham = dict()
        self.idf_spam = dict()
        self.idf_ham = dict()
        for i in range(noOfMessages):
            message_processed = process_message(self.mails[i])
            count = list() #To keep track of whether the word has ocured in the message or not.
                           #For IDF
            for word in message_processed:
                if self.labels[i]:
                    self.tf_spam[word] = self.tf_spam.get(word, 0) + 1
                    self.spam_words += 1
                else:
                    self.tf_ham[word] = self.tf_ham.get(word, 0) + 1
                    self.ham_words += 1
                if word not in count:
                    count += [word]
            for word in count:
                if self.labels[i]:
                    self.idf_spam[word] = self.idf_spam.get(word, 0) + 1
                else:
                    self.idf_ham[word] = self.idf_ham.get(word, 0) + 1

    def calc_TF_IDF(self):
        self.prob_spam = dict()
        self.prob_ham = dict()
        self.sum_tf_idf_spam = 0
        self.sum_tf_idf_ham = 0
        for word in self.tf_spam:
            self.prob_spam[word] = (self.tf_spam[word]) * log((self.spam_mails + self.ham_mails) \
                                                          / (self.idf_spam[word] + self.idf_ham.get(word, 0)))
            self.sum_tf_idf_spam += self.prob_spam[word]
        for word in self.tf_spam:
            self.prob_spam[word] = (self.prob_spam[word] + 1) / (self.sum_tf_idf_spam + len(list(self.prob_spam.keys())))
            
        for word in self.tf_ham:
            self.prob_ham[word] = (self.tf_ham[word]) * log((self.spam_mails + self.ham_mails) \
                                                          / (self.idf_spam.get(word, 0) + self.idf_ham[word]))
            self.sum_tf_idf_ham += self.prob_ham[word]
        for word in self.tf_ham:
            self.prob_ham[word] = (self.prob_ham[word] + 1) / (self.sum_tf_idf_ham + len(list(self.prob_ham.keys())))
            
    
        self.prob_spam_mail, self.prob_ham_mail = self.spam_mails / self.total_mails, self.ham_mails / self.total_mails 
                    
    def classify(self, processed_message):
        pSpam, pHam = 0, 0
        for word in processed_message:                
            if word in self.prob_spam:
                pSpam += log(self.prob_spam[word])
            else:
                if self.method == 'tf-idf':
                    pSpam -= log(self.sum_tf_idf_spam + len(list(self.prob_spam.keys())))
                else:
                    pSpam -= log(self.spam_words + len(list(self.prob_spam.keys())))
            if word in self.prob_ham:
                pHam += log(self.prob_ham[word])
            else:
                if self.method == 'tf-idf':
                    pHam -= log(self.sum_tf_idf_ham + len(list(self.prob_ham.keys()))) 
                else:
                    pHam -= log(self.ham_words + len(list(self.prob_ham.keys())))
            pSpam += log(self.prob_spam_mail)
            pHam += log(self.prob_ham_mail)
        return pSpam >= pHam
    
    def predict(self, testData):
        result = dict()
        for (i, message) in enumerate(testData):
            processed_message = process_message(message)
            result[i] = int(self.classify(processed_message))
        return result

def metrics(labels, predictions):
    true_pos, true_neg, false_pos, false_neg = 0, 0, 0, 0
    for i in range(len(labels)):
        true_pos += int(labels[i] == 1 and predictions[i] == 1)
        true_neg += int(labels[i] == 0 and predictions[i] == 0)
        false_pos += int(labels[i] == 0 and predictions[i] == 1)
        false_neg += int(labels[i] == 1 and predictions[i] == 0)
    precision = true_pos / (true_pos + false_pos)
    recall = true_pos / (true_pos + false_neg)
    Fscore = 2 * precision * recall / (precision + recall)
    accuracy = (true_pos + true_neg) / (true_pos + true_neg + false_pos + false_neg)

    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F-score: ", Fscore)
    print("Accuracy: ", accuracy)



"""#Generate Data

##Data Gen
"""

#sem_classifier
#tech_classifier
#bank_classifier
#online_classifier
#sc_tf_idf

def get_lines(load_file):
  with open(load_file) as f:
    lines = f.readlines()
  return lines

def analyze_text(clf, text):
  custom_tokens = remove_noise(word_tokenize(text))
  return clf.classify(dict([token, True] for token in custom_tokens))

def analyze_file(file):
  tweets_lines = get_lines(file)

  tweets_pos = 0
  tweets_neg = 0
  tweets_tech = 0
  tweets_not_tech = 0
  tweets_banking = 0
  tweets_insurance = 0
  tweets_bi_un = 0
  tweets_online = 0
  tweets_onsite = 0
  tweets_oo_un = 0
  tweets_spam = 0
  tweets_not_spam = 0

  tech_pos = 0
  tech_neg = 0
  not_tech_pos = 0
  not_tech_neg = 0

  for line in tweets_lines:
    sem = analyze_text(sem_classifier, line)
    if sem == "Positive":
      tweets_pos+=1
    else:
      tweets_neg+=1
    
    tech = analyze_text(tech_classifier, line)
    if tech == "Technical":
      tweets_tech+=1
      if sem == "Positive":
        tech_pos+=1
      else:
        tech_neg+=1
    else:
      tweets_not_tech+=1
      if sem == "Positive":
        not_tech_pos+=1
      else:
        not_tech_neg+=1
    
    banking = analyze_text(bank_classifier, line)
    if banking == "Banking":
      tweets_banking+=1
    elif banking == "Insurance":
      tweets_insurance+=1
    else:
      tweets_bi_un+=1
    
    online = analyze_text(online_classifier, line)
    if online == "Online":
      tweets_online+=1
    elif online == "Onsite":
      tweets_onsite+=1
    else:
      tweets_oo_un+=1
    
    spam = sc_tf_idf.classify(process_message(line))
    if spam:
      tweets_spam+=1
    else:
      tweets_not_spam+=1

  print("Pos", tweets_pos)
  print("Neg", tweets_neg)
  print("Tech", tweets_tech)
  print("Not tech", tweets_not_tech)
  print("Banking", tweets_banking)
  print("Insurance", tweets_insurance)
  print("BI Unkown", tweets_bi_un)
  print("Online", tweets_online)
  print("Onsite", tweets_onsite)
  print("OO Unkown", tweets_oo_un)
  print("Spam", tweets_spam)
  print("Not Spam", tweets_not_spam)
  print("Tech pos", tech_pos)
  print("Tech neg", tech_neg)
  print("Not tech pos", not_tech_pos)
  print("Not tech neg", not_tech_neg)


from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps 
from flask import jsonify
from flask import abort
 
import random

app = Flask(__name__)
api = Api(app) 

@app.route('/start', methods=['GET'])
def just_start():
    process_nlp()
    return jsonify({})

@app.route('/get_random_message', methods=['GET'])
def get_random_tweet():
  with open("banktweetsDataList.txt") as f:
    lines = f.readlines()
  random_tweet = lines[random.randrange(0, len(lines))]

  result = {'random_tweet': random_tweet, 
            'sem': analyze_text(sem_classifier, random_tweet),
            'tech': analyze_text(tech_classifier, random_tweet),
            'banking_type': analyze_text(bank_classifier, random_tweet),
            'online_type': analyze_text(online_classifier, random_tweet),
            'spam': sc_tf_idf.classify(process_message(random_tweet))}
  return jsonify(result)

@app.route('/send_text', methods=['POST'])
def send_text():
  if not request.json or not 'text' in request.json:
    abort(400)
  text = request.json['text']
  result = { 
          'sem': analyze_text(sem_classifier, text),
          'tech': analyze_text(tech_classifier, text),
          'banking_type': analyze_text(bank_classifier, text),
          'online_type': analyze_text(online_classifier, text),
          'spam': sc_tf_idf.classify(process_message(text))}
  return jsonify(result)


#api.add_resource(GetRandomMessage, '/get_random_message') # Route_3
if __name__ == '__main__':
  app.run(debug=True)

