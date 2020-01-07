import sys
import json
import re

HASHTAG_FREQUENCY_DICT = {}


def load_tweets(tweets, callback):
    with open(tweets) as f:
        for line in f:
            tweet = json.loads(line)
            if len(tweet['entities']['hashtags']) > 0:
                callback(tweet['entities']['hashtags'])


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


def calculate_hashtags_frequency(hashtags):
    global HASHTAG_FREQUENCY_DICT

    for hashtag in hashtags:
        if hashtag['text'] in HASHTAG_FREQUENCY_DICT:
            HASHTAG_FREQUENCY_DICT[hashtag['text']] += 1
        else:
            HASHTAG_FREQUENCY_DICT[hashtag['text']] = 1


def create_sorted_hashtags_frequency_list():
    global HASHTAG_FREQUENCY_DICT

    hashtags_frequency_list = [tuple(x)
                               for x in HASHTAG_FREQUENCY_DICT.items()]
    return sorted(
        hashtags_frequency_list, key=lambda x: x[1], reverse=True)


def print_top_ten_hashtags(sorted_hashtags_frequency_list):
    if len(sorted_hashtags_frequency_list) >= 10:
        for i in range(10):
            print sorted_hashtags_frequency_list[i][0].encode(
                'utf-8') + ' ' + str(sorted_hashtags_frequency_list[i][1])
    else:
        for hashtag, frequency in sorted_hashtags_frequency_list:
            print hashtag.encode('utf-8') + ' ' + str(frequency)


def main():
    if len(sys.argv) != 2:
        raise Exception(
            'usage: python top_ten.py <tweet_file>'
        )
    load_tweets(sys.argv[1], calculate_hashtags_frequency)
    sorted_hashtags_frequency_list = create_sorted_hashtags_frequency_list()
    print_top_ten_hashtags(sorted_hashtags_frequency_list)


if __name__ == '__main__':
    main()
