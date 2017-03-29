# nltk notes and functions
# 03/03/17


''' - - - - GENERAL - - - - '''
# import 9 texts for analysis
from nltk.book import *

# turn gutenberg text into nltk text object (to be able to call methods like text.concordance())
emma = nltk.Text(nltk.corpus.gutenberg.words('austen-emma.txt'))
emma.concordance('surprise')


# lexical diversity (# of distinct words as percentage of total words)
def lex_diversity(text):
    return len(set(text)) / len(text)


# single word percentage of total
def single_percent(text, word):
    return text.count(word) / len(text)


# find words more than 15 characters long
vocab = set(text5)
long_words = [word for word in vocab if len(word) > 15]
sorted(long_words)

# frequently occuring long words
fdist5 = FreqDist(text5)
freq_long_words = sorted(word for word in set(text5) if len(word) > 7 and fdist[word] > 7)


# find two or more vowels in a text and determine their relative frequencies
wsj = sorted(set(nltk.corpus.treebank.words()))
fd = nltk.FreqDist(vs for word in wsj for vs in re.findall(r'[aeiou]{2,}', word))
fd.most_comon(12)


# find anything surrounded by two words, but only print out found word
from nltk.corpus import gutenberg
moby = nltk.Text(gutenberg.words('melville-moby_dick.txt'))
moby.findall(r"<a> (<.*>) <man>")


# find 3-word phrases ending in 'bro'
from nltk.corpus import nps_chat
chat = nltk.Text(nps_chat.words())
chat.findall(r"<.*> <.*> <bro>")

# find sequences of 3+ words starting with 'l'
chat.findall(r"<l.*>{3,}")
''' - - - - - - - - - - - - - - - '''


''' - - - - FREQUENCY DISTRIBUTIONS - - - - '''
# frequency ditribution
fdist4 = FreqDist(text4)
fdist4.most_common(50)
fdist4.plot(50, cumulative=True)

# words that occur only once
fdist4.hapaxes()

# frequency distribution of word lengths
fdist = FreqDist(len(word) for word in text1)

# which word is most frequent
fdist.max()

# word's percentage of whole
fdist.freq('trump')

# CONDITIONAL FREQUENCY DISTRIBUTION
# Chapter 2 section 2.3 explains how to use this to make comparison plots
# also lists common methods for cfd'
from nltk.corpus import brown
genre_word = [(genre, word) for genre in ['news', 'romance'] for word in brown.words(categories=genre)]
cfd = nltk.ConditionalFreqDist(genre_word)
# or
cfd = nltk.ConditionalFreqDist((genre, word) for genre in brown.categories() for word in brown.words(categories=genre))
''' - - - - - - - - - - - - - - - '''


''' - - - - STEMMING/LEMMATIZATION - - - - '''
# stemming - very basic
def stem(word):
    for suffix in ['ing', 'ly', 'ed', 'ious', 'ies', 'ive', 'es', 's', 'ment']:
        if word.endswith(suffix):
            return word[:-len(suffix)]
        return word


# stemming with regex
def stemm(word):
    regexp = r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)?$'
    stem, suffix = re.findall(regexp, word)[0]
    return stem


# NOTE:
# basic normalization: removing capitalization
# more complex normalization involves identifying non-standard words (like #s, abbrevs, dates) and mapping them to a special vocabulary; e.g., all decimals mapped to 0.0
# different stemmers have different outcomes, none are perfect
raw = 'DENNIS: Listen, strange women lying in ponds distributing swords is no basis for a system of government.  Supreme executive power derives from a mandate from the masses, not from some farcical aquatic ceremony.'
tokens = word_tokenize(raw)

# stem
porter = nltk.PorterStemmer()
[porter.stem() for t in tokens]

# stem
lancaster = nltk.LancasterStemmer()
[lancaster.stem(t) for t in tokens]

# lemmatize (only return stems that are in WordNet dictionary)
wnl = nltk.WordNetLemmatizer()
[wnl.lemmatize(t) for t in tokens]
''' - - - - - - - - - - - - - - - '''


''' - - - - REGEX - - - - '''
money = ['$', 'test', 'me', '$0.13', '$000.134', '$13.21', '$1.20', '$.15', '$25']
[word for word in money if re.search('^\$[0-9]*\.?[0-9]*$', word)]

dates = ['03/04/05', 'date', '3/4/2005', '4/05']
[word for word in dates if re.search('^[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{2,4}$', word)]

# count vowels in string
word = 'supercalifragilisticexpialidocious'
len(re.findall(r'[aeiou]', word))
''' - - - - - - - - - - - - - - - '''


''' - - - - STOPWORDS - - - - '''
# nltk provided list of stopwords to help filter out common, high frequency, inconsequential words
nltk.corpus.stopwords.words('english')


# fraction of words that are not in stopwords list
def content_fraction(text):
    stopwords = nltk.corpus.stopwords.words('english')
    content = [w for w in text if w.lower() not in stopwords]
    return len(content) / len(text)
''' - - - - - - - - - - - - - - - '''


''' - - - - FIRST NAMES - - - - '''
# list of 8,000 first names separated by gender
names = nltk.corpus.names
male_names = names.words('male.txt')
overlap = [name for name in male_names if name in female_names]

# plot frequency distribution of names by their last letter
cfd = nltk.ConditionalFreqDist((fileid, name[-1]) for fileid in names.fileids() for name in names.words(fileid))
cfd.plot()
''' - - - - - - - - - - - - - - - '''


''' - - - - PRONUNCIATION - - - - '''
# pronouncing dictionary designed for use by speech synths
entries = nltk.corpus.cmudict.entries()

# find words rhyming with 'nicks'
syllable = ['N', 'IH0', 'K', 'S']
rhymes = [word for word, pron in entries if pron[-4:] == syllable]


# find words with similar stress patterns
def stress(pron):
    return [char for phone in pron for char in phone if char.isdigit()]

sims = [w for w, pron in entries if stress(pron) == ['0', '1', '0', '2', '0']]
''' - - - - - - - - - - - - - - - '''


''' - - - - WORDNET/SYNONYMS - - - - '''
# Chapter 2 section 5; wordnet goes deep
from nltk.corpus import wordnet as wn
synset01 = wn.synsets('motorcar')
synonyms = wn.synset(synset01).lemma_names()
''' - - - - - - - - - - - - - - - '''


pattern = r'''(?x) ([A-Z]\.)+ | \w+(-\w+)* | \$?\d+(\.\d+)?%? | \.\.\. | [][.,;"'?():-_`]'''
