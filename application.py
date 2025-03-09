# Import necessary libraries
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os

app = Flask(__name__)

# Load the trained model and tokenizer
MODEL_PATH = "next_word_lstm.keras"
TOKENIZER_PATH = "tokenizer.pickle"

# Load the model
model = tf.keras.models.load_model(MODEL_PATH)

# Load the tokenizer
with open(TOKENIZER_PATH, 'rb') as handle:
    tokenizer = pickle.load(handle)

# Get max sequence length from model input shape
max_sequence_len = model.input_shape[1] + 1

# Function to predict the next word
def predict_next_word(text):
    token_list = tokenizer.texts_to_sequences([text])[0]
    if len(token_list) >= max_sequence_len:
        token_list = token_list[-(max_sequence_len-1):]
    token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
    predicted = model.predict(token_list, verbose=0)
    
    # Get top 5 predictions
    top_indices = np.argsort(predicted[0])[-5:][::-1]
    top_words = []
    
    for idx in top_indices:
        for word, index in tokenizer.word_index.items():
            if index == idx:
                top_words.append(word)
                break
    
    return top_words

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        data = request.get_json()
        input_text = data['text']
        
        # Make prediction
        predictions = predict_next_word(input_text)
        
        return jsonify({
            'input_text': input_text,
            'predictions': predictions
        })

# Run the app
if __name__ == '__main__':
    app.run(debug=True)