# -*- coding: utf-8 -*-
"""streamlit app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JR0tXUTSjvBJikK91OgQMjlJF_28hL4O
"""

import streamlit as st
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from nltk.stem.porter import PorterStemmer
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
with open('tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
    tfidf_vectorizer = pickle.load(vectorizer_file)

with open('logistic_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# User input from Streamlit app
user_input = st.text_input("Enter a news article text")

if user_input:
    # Transform the user input using the loaded vectorizer
    user_input_transformed = tfidf_vectorizer.transform([user_input])

    # Predict using the loaded model
    prediction = model.predict(user_input_transformed)

    # Display the result
    st.write(f"Prediction: {prediction[0]}")
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
