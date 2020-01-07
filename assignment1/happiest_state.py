import sys
import json
import re

STATE_ABBRE_US_SET = {
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
}
STATE_SENT_DICT = {}


def create_sentiment_dict(sent_file):
    sent_scores_dict = {}
    with open(sent_file) as f:
        for line in f:
            # The file is tab-delimited. "\t" means "tab character"
            term, score = line.split('\t')
            # Convert the score to an integer.
            sent_scores_dict[term] = int(score)
    return sent_scores_dict


def load_tweets(tweets, callback, sent_scores_dict):
    with open(tweets) as f:
        for line in f:
            tweet = json.loads(line)
            if 'text' in tweet:
                callback(tweet, sent_scores_dict)


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


def calcuate_sentiment_for_tweet(text, sent_scores_dict):
    text = clean_tweet(text)
    text_split = text.split(' ')
    tweet_sent_score = reduce(lambda prev, current: prev +
                              sent_scores_dict[current] if current in sent_scores_dict else prev, text_split, 0)
    return tweet_sent_score


def update_state_sentiment_dict(tweet, sent_scores_dict):
    global STATE_ABBRE_US_SET
    global STATE_SENT_DICT

    if tweet['user']['location']:
        state = tweet['user']['location'].split(', ')[-1]
        if state and state in STATE_ABBRE_US_SET:
            sentiment = calcuate_sentiment_for_tweet(
                tweet['text'], sent_scores_dict)
            if state in STATE_SENT_DICT:
                STATE_SENT_DICT[state].append(sentiment)
            else:
                STATE_SENT_DICT[state] = [sentiment]


def calculate_average_sentiments():
    global STATE_SENT_DICT

    for key, value in STATE_SENT_DICT.items():
        STATE_SENT_DICT[key] = sum(value) / len(value)


def print_top_sentiment_state():
    global STATE_SENT_DICT

    state_sent_list = [tuple(x) for x in STATE_SENT_DICT.items()]
    sorted_state_sent = sorted(
        state_sent_list, key=lambda x: x[1], reverse=True)
    print(sorted_state_sent[0][0].encode('utf-8'))


def main():
    if len(sys.argv) != 3:
        raise Exception(
            'usage: python happiest_state.py <sentiment_file> <tweet_file>')

    sent_scores_dict = create_sentiment_dict(sys.argv[1])
    load_tweets(sys.argv[2], update_state_sentiment_dict, sent_scores_dict)
    calculate_average_sentiments()
    print_top_sentiment_state()


if __name__ == '__main__':
    main()
