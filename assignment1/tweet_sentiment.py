import sys
import json
import re


def create_sentiment_dict(sent_file):
    sent_scores_dict = {}
    with open(sent_file) as f:
        for line in f:
            # The file is tab-delimited. "\t" means "tab character"
            term, score = line.split('\t')
            # Convert the score to an integer.
            sent_scores_dict[term] = int(score)
    return sent_scores_dict


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


def generate_tweet_score(text, sent_scores_dict):
    text = clean_tweet(text)
    text_split = text.split(' ')
    tweet_sent_score = reduce(lambda prev, current: prev +
                              sent_scores_dict[current] if current in sent_scores_dict else prev, text_split, 0)
    return tweet_sent_score


def print_twitter_sent_scores(output_file, sent_scores_dict):
    with open(output_file) as f:
        for line in f:
            tweet = json.loads(line)
            if 'text' in tweet:
                print generate_tweet_score(tweet['text'], sent_scores_dict)
            else:
                print 0


def main():
    if len(sys.argv) != 3:
        raise Exception(
            'usage: python tweet_sentiment.py sentiment_file output_file'
        )
    sent_scores_dict = create_sentiment_dict(sys.argv[1])
    print_twitter_sent_scores(sys.argv[2], sent_scores_dict)


if __name__ == '__main__':
    main()
