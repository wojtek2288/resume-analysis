import pickle
import tensorflow as tf
from transformers import pipeline
from tensorflow.keras.layers import Embedding, LSTM, Dense, Concatenate, Dropout, Lambda, Input
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2
from tensorflow.keras.backend import l2_normalize, sum
from tensorflow.keras.models import load_model

max_len = 100
vectorizer_file_path = 'ai/vectorizer.keras'
tfidf_vectorizer_file_path = 'ai/tfidf_vectorizer.pkl'
model_weights_file_path = 'ai/test.weights.h5'
classifier_model_file_path = 'ai/gradient_boosting_model.pkl'
tf.keras.config.enable_unsafe_deserialization()

def get_vectorizer():
    vectorizer_model = load_model(vectorizer_file_path)
    return vectorizer_model.layers[1]

def get_tfidf_vectorizer():
    with open(tfidf_vectorizer_file_path, 'rb') as file:
        return pickle.load(file)

def get_classifier():
    with open(classifier_model_file_path, 'rb') as file:
        return pickle.load(file)

def get_ranking_model():
    input_resume = Input(shape=(max_len,))
    input_job_desc = Input(shape=(max_len,))

    embedding_dim = 128
    embedding = Embedding(input_dim=10000, output_dim=embedding_dim, input_length=max_len)

    encoded_resume = embedding(input_resume)
    encoded_job_desc = embedding(input_job_desc)

    shared_lstm = LSTM(64, return_sequences=True)

    lstm_resume = shared_lstm(encoded_resume)
    lstm_job_desc = shared_lstm(encoded_job_desc)

    resume_pooling = Lambda(lambda x: sum(x, axis=1), output_shape=(64,))(lstm_resume)
    job_desc_pooling = Lambda(lambda x: sum(x, axis=1), output_shape=(64,))(lstm_job_desc)

    normalized_resume = Lambda(lambda x: l2_normalize(x, axis=1), output_shape=(64,))(resume_pooling)
    normalized_job_desc = Lambda(lambda x: l2_normalize(x, axis=1), output_shape=(64,))(job_desc_pooling)

    cosine_similarity = Lambda(lambda x: sum(x[0] * x[1], axis=1, keepdims=True), output_shape=(1,))([normalized_resume, normalized_job_desc])

    merged = Concatenate()([normalized_resume, normalized_job_desc, cosine_similarity])
    dense = Dense(64, activation='relu', kernel_regularizer=l2(0.001))(merged)
    dropout = Dropout(0.2)(dense)
    output = Dense(3, activation='softmax', kernel_regularizer=l2(0.001))(dropout)

    model = Model(inputs=[input_resume, input_job_desc], outputs=output)

    model.load_weights(model_weights_file_path)

    return model

vectorizer = get_vectorizer()
tfidf_vectorizer = get_tfidf_vectorizer()
ranking_model = get_ranking_model()
classifier = get_classifier()
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")