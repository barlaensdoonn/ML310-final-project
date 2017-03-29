
# deletweet notepad

# R text mining methods:
# https://rstudio-pubs-static.s3.amazonaws.com/31867_8236987cf0a8444e962ccd2aec46d9c3.html

# R tweet sentiment analysis:
# https://www.r-bloggers.com/in-depth-analysis-of-twitter-activity-and-sentiment-with-r/

# R tweet preprocessing and text mining:
# http://www.rdatamining.com/examples/text-mining

# should specify dtypes: http://stackoverflow.com/questions/24251219/pandas-read-csv-low-memory-and-dtype-options#27232309
deletweet = pandas.read_csv('/Users/kestrel/Desktop/UW/machine_learning/310/final_project/me/data/deleted_tweets.csv', error_bad_lines=False)

# load tweet field into json dicty
tweet = json.loads(deletweet['tweet'][7962])


''' - - - TWEET - - - '''
# hashtags
tweet['entities']['hashtags']
# list of hashtags for tweet
[tweet['entities']['hashtags'][i]['text'] for i in range(len(tweet['entities']['hashtags']))]

# users mentioned in the tweet
tweet['entities']['user_mentions']


''' - - - LOCATION - - - '''
# geo coordinates
tweet['coordinates']

# more location info (might be empty)
tweet['place']


'''- - - USER - - -'''
# date user profile created
tweet['user']['created_at']

# how many tweets user has made
tweet['user']['statuses_count']

# user profile description
tweet['user']['description']

# user location (free form text; not guaranteed to geocode; could be multiple entries for same place)
# might return None
tweet['user']['location']



# convert all dates into datetime objects to do max, min, difference, etc
# not sure if this line is working properly
dates_created = [datetime.datetime.strptime(deletweet['created'][i], '%m/%d/%Y %H:%M:%S') for i in range(len(deletweet))]


# create NLTK corpus from individual tweet files
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
tweet_corpus = PlaintextCorpusReader('../../deletweet/data/tweets_txts', '.*', word_tokenizer=TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True))

# make cumulative frequency distribution from corpus
cfd_tweet = nltk.ConditionalFreqDist((this, fileid[:-4]) for fileid in tweet_corpus.fileids() for word in tweet_corpus.words(fileid) if word.lower().startswith('trump'))
cfd_tweet.plot(cumulative=True)


''' WRITE TO FILES '''
# write tweets to json
with open('/Users/kestrel/Desktop/UW/machine_learning/310/final_project/me/data/deletweet.json', 'w') as outfile:
    for i in range(len(deletweet)):
        tweet = json.loads(deletweet['tweet'][i])
        json.dump(tweet, outfile)
        outfile.write('\n')

# write 100 most frequent words
with open('/Users/kestrel/Desktop/UW/machine_learning/310/final_project/me/output/files/100_most_common_filtered.csv', 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['WORD', 'COUNT'])
    for row in most_common_filtered:
        csv_out.writerow(row)

# write text of each tweet to individual file
for i in range(len(tweet_text_raw)):
    with open('../../deletweet/data/tweets_txts/tweet_{:05d}.txt'.format(i+1), 'w') as out:
        out.write(tweet_text_raw[i])


'''CLEAN BAD ROWS FROM DATAFRAME'''
bad_rows = []

for i in range(len(deletweet)):
    if type(deletweet['tweet'][i]) != str:
        bad_rows.append(i)
    else:
        tweet = json.loads(deletweet['tweet'][i])
        if type(tweet) != dict:
            bad_rows.append(i)

deletweet.drop(deletweet.index[bad_rows], inplace=True)
deletweet.reset_index(inplace=True, drop=True)

# export cleaned dataframe to csv without adding index to csv
deletweet.to_csv('/Users/kestrel/gitBucket/deletweet/data/deleted_tweets_cleaned.csv', index=False)
