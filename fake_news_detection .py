# -*- coding: utf-8 -*-
"""Fake News Detection

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eNg_8kmVaQ9q_koKttp455Vn4gPdzPa3

# 1. Data Collection
"""

import pandas as pd
import numpy as np

true = pd.read_csv("/content/True.csv")

fake = pd.read_csv("/content/Fake.csv")

true

fake

true.head()

fake.head()

true['label'] = 1

fake['label'] = 0

news = pd.concat([fake,true],axis=0)

news = news.sample(frac=1).reset_index(drop=True)

news.head()

news.tail()

news.isnull().sum()

"""# 2. Data Preprocessing"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = text.split()
    text = [lemmatizer.lemmatize(word) for word in text if word not in stop_words]
    return ' '.join(text)

news['cleaned_text'] = news['text'].apply(preprocess_text)

print(news[['text', 'cleaned_text']].head())

"""# 3. Exploratory Data Analysis (EDA)"""

import matplotlib.pyplot as plt
import seaborn as sns

sns.countplot(x='label', data=news)
plt.title('Class Distribution (True vs Fake)')
plt.show()

from wordcloud import WordCloud

"""Word cloud for fake news"""

fake_words = ' '.join(news[news['label'] == 0]['cleaned_text'])
wordcloud_fake = WordCloud(width=800, height=400, background_color='black').generate(fake_words)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_fake)
plt.title('Fake News Word Cloud')
plt.axis('off')
plt.show()

""" Word cloud for true news"""

true_words = ' '.join(news[news['label'] == 1]['cleaned_text'])
wordcloud_true = WordCloud(width=800, height=400, background_color='black').generate(true_words)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_true)
plt.title('True News Word Cloud')
plt.axis('off')
plt.show()

"""# 4. Model Building"""

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

X_train, X_test, y_train, y_test = train_test_split(news['cleaned_text'], news['label'], test_size=0.2, random_state=42)

tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

"""Logistic Regression Model"""

model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy*100:.2f}%")

print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

def output_label(n):
  if  n==0:
    return "It is a Fake News"
  elif n==1:
    return "It is a True News"

"""# 5. Model Evaluation"""

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Fake', 'True'], yticklabels=['Fake', 'True'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

"""# 6.Deployement"""

import pickle
filename = 'fake_news_model.pkl'
pickle.dump(model, open(filename, 'wb'))


pickle.dump(tfidf_vectorizer.vocabulary_, open('tfidf_vocab.pkl', 'wb'))

import streamlit as st
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from nltk.stem.porter import PorterStemmer
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

model = pickle.load(open('fake_news_model.pkl', 'rb'))
vocab = pickle.load(open('tfidf_vocab.pkl', 'rb'))

tfidf = TfidfVectorizer(vocabulary=vocab)
ps = PorterStemmer()
stop_words = stopwords.words('english')

def preprocess_text(text):
    # Preprocess the input text
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = text.split()
    text = [ps.stem(word) for word in text if not word in stop_words]
    text = ' '.join(text)
    return text

st.title('Fake News Detection')

user_input = st.text_area('Enter the news article text here')

if st.button('Predict'):
    if user_input.strip() == "":
        st.write('Please enter some news text to predict.')
    else:

        processed_text = preprocess_text(user_input)
        vect_text = tfidf.transform([processed_text]).toarray()


        prediction = model.predict(vect_text)


        if prediction[0] == 0:
            st.write('The news article is **Fake**.')
        else:
            st.write('The news article is **Real**.')

