import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import json
import random
from .models import ChatBot
# nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

def load_dataset():
    cb=ChatBot.objects.all()
    for path_file in cb:
        pass

    model = load_model(path_file.chatbot_model.path)

    intents = json.loads(open(path_file.intents.path).read())
    words = pickle.load(open(path_file.words.path,'rb'))
    classes = pickle.load(open(path_file.classes.path,'rb'))
    return model, intents, words, classes

# tách từ, chuyển sang chữ thường
def preprocess(sentence):
    list_words = nltk.word_tokenize(sentence)
    list_words = [lemmatizer.lemmatize(word.lower()) for word in list_words]
    return list_words

# chuyển list words sang 0 1 
def bow(sentence, words):
    list_words = preprocess(sentence)
    bag = [0]*len(words) 
    for s in list_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
    return(np.array(bag))

def predict_class(sentence, model):
    dataset=load_dataset()
    classes=dataset[3]
    words=dataset[2]
    # bag
    p = bow(sentence, words)
    # predict
    res = model.predict(np.array([p]))[0]
    if res.max()<0.5:
        return 0
    index=np.argmax(res)
    return classes[index]

def getResponse(pred, intents_json):
    tag = pred
    if tag==0:
        return 'Không hiểu'
    # danh sách toàn bộ intent trong json
    list_of_intents = intents_json['intents']

    # duyệt qua từng intent so sánh tag nếu = thì chọn ngẫu nhiên 1 response 
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(text):
    dataset=load_dataset()
    pred = predict_class(text,dataset[0])
    res = getResponse(pred, dataset[1])
    return res