from nltk.corpus import stopwords
import nltk

def get_tweet_histo():
    # Tweet data
    path_to_file = 'data' + '/user_tweets.txt'
    text = open(path_to_file, 'rb').read().decode(encoding='utf-8')
    #tokeznize the text
    tokens = [t for t in text.split()]
    print(tokens)

    #using nltk find freq of tokens
    freq = nltk.FreqDist(tokens)
    for key, val in freq.items():
        print(str(key) + ':' + str(val))

    #remove stopwords from the tokens
    clean_tokens = tokens[:]
    sr = stopwords.words('english')
    for token in tokens:
        if token in stopwords.words('english'):
            clean_tokens.remove(token)

    freq_clean = nltk.FreqDist(clean_tokens)
    freq_clean.plot(20, cumulative=False)

get_tweet_histo()