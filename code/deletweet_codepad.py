
# deletweet code pad

import json
import pandas
import nltk
from nltk.tokenize import TweetTokenizer


deletweet = pandas.read_csv('/Users/kestrel/Desktop/UW/machine_learning/310/final_project/me/data/deleted_tweets.csv', error_bad_lines=False)


# tweet_text_raw will be a list that holds the text of each tweet as an individual item
tweet_text_raw = []

for i in range(len(deletweet)):
    if type(deletweet['tweet'][i]) == str:
        tweet = json.loads(deletweet['tweet'][i])
        if type(tweet) == dict:
            tweet_text_raw.append(tweet['text'])

len(tweet_text_raw)  # output: 67756

# convert list into single string
tweet_string = ' '.join(tweet_text_raw)


# tokenize
tknzr = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
tweet_tokenized = tknzr.tokenize(tweet_string)

len(tweet_tokenized)  # output: 1227667


# convert to nltk text object
text = nltk.Text(tweet_tokenized)

# make set of words for vocab
words = [w.lower() for w in text]
vocab = sorted(set(words))
len(vocab)  # output: 128203

# lexical diversity
len(vocab) / len(words)  # output: 0.09927273966217084

# remove stopwords
stopwords = nltk.corpus.stopwords.words('english')
punctuation = ['.', ':', ',', '!', '"', '-', '…', '...', "’", '?', '/', "'", '(', ')']
filtered = [w for w in tweet_tokenized if w.lower() not in stopwords]
filtered_again = [w for w in filtered if w.lower() not in punctuation]
text_filtered = nltk.Text(filtered_again)

# len(content) / len(text)  # output: 0.7165876414369695 (this was with just stopwords removed)
len(text_filtered) / len(text)  # output: 0.5811331574441604

words_filtered = [w.lower() for w in text_filtered]
vocab_filtered = sorted(set(words_filtered))
len(vocab_filtered) / len(words_filtered)  # output: 0.1435135218477289


fdist = nltk.FreqDist(text)
fdist_filtered = nltk.FreqDist(text_filtered)
most_common = fdist.most_common(100)
most_common_filtered = fdist_filtered.most_common(100)

# words longer than 3 characters occurring more than 1000 times (wrote to file)
freq_long_words = sorted(word for word in set(text_filtered) if len(word) > 3 and fdist_filtered[word] > 1000)

text.collocations()
'''
looking forward; last night; town hall; health care; #tg4lg #jobsnow;
make sure; high school; president obama; house floor; watch live;
happy birthday; years ago; it's time; white house; good luck; supreme
court; common sense; script class; middle class; great time
'''

# frequency distribition of the frequencies of word lengths
dist_of_dist = nltk.FreqDist(len(w) for w in text)
dist_of_dist_filtered = nltk.FreqDist(len(w) for w in text_filtered)
dist_of_dist.max()  # output: 1 [in fact is sequential with 1 highest, 2 next highest, etc]
dist_of_dist_filtered.max()  # output: 5
dist_of_dist.freq(1)  # output: 0.18264969246546497
dist_of_dist_filtered.freq(5)  # output: 0.15079095870979678
