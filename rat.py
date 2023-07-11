import re
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
import tensorflow as tf
from tensorflow import keras 
from keras import preprocessing
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from googleapiclient.discovery import build

# import ctypes
# hllDll = ctypes.WinDLL("C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin")
train = pd.read_csv('Train.csv')
valid= pd.read_csv('Valid.csv')
test = pd.read_csv('Test.csv')
train_x = train['text']
valid_x = valid['text']
test_x = test['text']
train_y = train['label']
valid_y = valid['label']
test_y = test['label']
tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_x)
train_x = tokenizer.texts_to_sequences(train_x)
valid_x = tokenizer.texts_to_sequences(valid_x)
test_x = tokenizer.texts_to_sequences(test_x)
train_x=pad_sequences(train_x,maxlen=120)
valid_x=pad_sequences(valid_x,maxlen=120)
test_x=pad_sequences(test_x,maxlen=120)
def Preprocessing(text):
    text = re.sub(r'[^\w\s]','',text)
    text = text.lower()
    text = [w for w in text.split(' ') if w not in stopwords.words('english')]
    text = [WordNetLemmatizer().lemmatize(token) for token in text]
    text = [WordNetLemmatizer().lemmatize(token,pos='v') for token in text]
    text = " ".join(text)
    return text
model = keras.models.load_model("YT_model_v1.h5")


api_key = "AIzaSyBl3qSU3fCAo-sZS3iwGFaFEABQZ64ms2I"

youtube = build('youtube', 'v3', developerKey=api_key)
video_id = "uOeFasnuW6c"
max_results = 1000
response = youtube.commentThreads().list(
    part='snippet',
    videoId=video_id,
    order='relevance',
    maxResults=max_results
).execute()

comments = [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in response['items']]

for comment in comments:
    xx = tokenizer.texts_to_sequences([comment])
    xx=pad_sequences(xx,maxlen=120)
    model.predict(xx)
# sample = model.tokenizer.texts_to_sequences(['Imagine... trying to overclock a CPU the company has locked down and told people not to overclock might actually not be a good idea'])
# print(sample)