import json
import sys
import re

TERM_FREQUENCY_DICT = {}
TERM_TOTAL = 0


def load_tweets(tweets, callback):
    with open(tweets) as f:
        for line in f:
            tweet = json.loads(line)
            if 'text' in tweet:
                callback(tweet['text'])


def clean_tweet(text):
    # ignore non-ascii characters; for example, unicode
    text = text.encode('ascii', 'ignore')
    text = re.sub('RT ', '', text)  # remove meaningless characters
    text = re.sub('\n', '', text)  # remove \n
    text = text.lower()  # lower case
    text = text.strip()  # remove unnecessary whitespace
    text = re.sub(r'http\S+', '', text)  # remove url
    text = re.sub('\.|,|:|!|-|"|;', '', text)  # remove special characters
    return text


def calculate_term_frequency(text):
    global TERM_FREQUENCY_DICT
    global TERM_TOTAL

    text = clean_tweet(text)
    text_split = text.split(' ')
    TERM_TOTAL += len(text_split)
    for t in text_split:
        if t in TERM_FREQUENCY_DICT:
            TERM_FREQUENCY_DICT[t] += 1
        else:
            TERM_FREQUENCY_DICT[t] = 1
            TERM_TOTAL += 1


def print_term_frequency(term_frequency_dict, term_total):
    for key, value in term_frequency_dict.items():
        print key + ' ' + str(value/term_total * 1.0)


def main():
    if len(sys.argv) != 2:
        raise Exception(
            'usage: python frequency.py <tweet_file>'
        )
    load_tweets(sys.argv[1], calculate_term_frequency)
    print_term_frequency(TERM_FREQUENCY_DICT, TERM_TOTAL)


if __name__ == '__main__':
    main()
