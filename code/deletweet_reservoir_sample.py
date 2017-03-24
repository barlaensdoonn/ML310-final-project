#!/usr/local/bin/python3

# pull out random sample of tweets from politwoops dataset via reservoir sampling
# 3/23/17


import pandas
import json
from random import randint


def reservoir(stream, k):
    '''
    Populate sample space with first k items from stream. For remaining items in stream,
    choose a random number j from 0 to item's index. If j is less than k, replace
    jth element in sample with ith element from stream
    '''
    sample = stream[0:k]

    for i in range(k, len(stream)):
        j = randint(0, i + 1)
        if j < k:
            sample[j] = stream[i]

    return sample


def write_to_file(samples):
    '''write out sample subset to line separated json file'''

    nmbr = len(samples)
    file_name = 'deletweet_subset_{}.json'.format(nmbr)

    with open('../data/{}'.format(file_name), 'w') as outfile:
        for i in range(nmbr):
            tweet = json.loads(samples[i])
            json.dump(tweet, outfile)
            outfile.write('\n')

    return(file_name, nmbr)


if __name__ == '__main__':
    num = int(input('how many samples?\n'))

    deletweet = pandas.read_csv('../../deletweet/data/deleted_tweets_cleaned.csv')
    tweets = deletweet['tweet']

    samples = reservoir(tweets, 10000)
    stats = write_to_file(samples)

    print('created {} with {} samples'.format(*stats))
