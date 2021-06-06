import tensorflow
import sys
import keras
from os import listdir
from pickle import dump, load
from numpy import argmax
from keras.preprocessing.image import load_img, img_to_array
from keras.models import Model
from numpy import array
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical, plot_model
from keras.models import Model
from keras.layers import Input, Dense, LSTM, Embedding, Dropout
from keras.layers.merge import add
from keras.callbacks import ModelCheckpoint
from keras.models import Model, load_model


def extract_features(filename, model_name):
    if model_name == "Vgg16":
        from keras.applications.vgg16 import VGG16, preprocess_input
        model = VGG16()
        ts = (224, 224)
    elif model_name == "Inceptionv3":
        from keras.applications.inception_v3 import preprocess_input, InceptionV3
        model = InceptionV3()
        ts = (299, 299)
    elif model_name == "Xception":
        from keras.applications.xception import preprocess_input, Xception
        model = Xception()
        ts = (299, 299)
    model = model
    model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
    image = load_img(filename, target_size=ts)
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    feature = model.predict(image, verbose=0)
    return feature


def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'startseq'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo, sequence], verbose=0)
        yhat = argmax(yhat)
        word = word_for_id(yhat, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'endseq':
            break
    return in_text


if __name__ == "__main__":
    model_name = sys.argv[1]
    load_tokanizer = '/home/astron/Desktop/Thesis/Thesis_final/Dataset/Model/' + \
        model_name+'/tokanizer.pkl'
    tokenizer = load(open(load_tokanizer, 'rb'))
    max_length = 57
    model = load_model(
        '/home/astron/Desktop/Thesis/IMC/Dataset/Model/'+model_name+'/model_16.h5')
    photo = extract_features(sys.argv[2], model_name)
    description = generate_desc(model, tokenizer, photo, max_length)
    print(description)
    description = description.replace('startseq', '')
    description = description.replace('endseq', '')
    print(description)
