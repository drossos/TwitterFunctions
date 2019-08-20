import nltk
import numpy
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import tensorflow as tf
import os
import sys

def preprocess():
    path_to_file = '../data' + '/user_tweets.txt'
    text = open(path_to_file, 'rb').read().decode(encoding='utf-8')

    tokens = tokenize_words(text)

    chars = sorted(list(set(tokens)))
    char_to_num = dict((c, i) for i, c in enumerate(chars))

    input_len = len(tokens)
    vocab_len = len(chars)

    seq_length = 100
    x_data = []
    y_data = []

    # loop through inputs, start at the beginning and go until we hit
    # the final character we can create a sequence out of
    for i in range(0, input_len - seq_length, 1):
        # Define input and output sequences
        # Input is the current character plus desired sequence length
        in_seq = tokens[i:i + seq_length]

        # Out sequence is the initial character plus total sequence length
        out_seq = tokens[i + seq_length]

        # We now convert list of characters to integers based on
        # previously and add the values to our lists
        x_data.append([char_to_num[char] for char in in_seq])
        y_data.append(char_to_num[out_seq])

    n_patterns = len(x_data)

    X = numpy.reshape(x_data, (n_patterns, seq_length, 1))
    X = X / float(vocab_len)

    y = tf.keras.utils.to_categorical(y_data)


    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.LSTM(256, return_sequences=True))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.LSTM(128))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(y.shape[1], activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')

    # Directory where the checkpoints will be saved
    checkpoint_dir = './training_checkpoints'
    # Name of the checkpoint files
    filepath = os.path.join(checkpoint_dir, "model_weights_saved.hdf5")

    checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
    desired_callbacks = [checkpoint]

    model.fit(X, y, epochs=15, batch_size=256, callbacks=desired_callbacks)

    model.load_weights(filepath)
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    num_to_char = dict((i, c) for i, c in enumerate(chars))

    start = numpy.random.randint(0, len(x_data) - 1)
    pattern = x_data[start]
    print("Random Seed:")
    print("\"", ''.join([num_to_char[value] for value in pattern]), "\"")

    for i in range(250):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / float(vocab_len)
        prediction = model.predict(x, verbose=0)
        index = numpy.argmax(prediction)
        result = num_to_char[index]
        seq_in = [num_to_char[value] for value in pattern]

        sys.stdout.write(result)

        pattern.append(index)
        pattern = pattern[1:len(pattern)]


def tokenize_words(input):
    # lowercase everything to standardize it
    input = input.lower()

    # instantiate the tokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(input)

    # if the created token isn't in the stop words, make it part of "filtered"
    filtered = filter(lambda token: token not in stopwords.words('english'), tokens)
    return " ".join(filtered)

preprocess()