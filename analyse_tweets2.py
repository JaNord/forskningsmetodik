import json
import pandas as pd
import matplotlib.pyplot as plt
import re
from matplotlib.backends.backend_pdf import PdfPages


def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False


def extract_link(text):
    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''


def load_tweets(file):
    with open(file, 'r') as f:
        tweets = (json.loads(line) for line in f.readlines())
    return tweets


def main():
    # Reading Tweets
    print('Reading Tweets\n')
    tweets_data_path = 'our_data.json'

    # tweets_data = []
    tweet = load_tweets(tweets_data_path)
    #	for t in tweet:
    #		   print json.dumps(t, indent=4)
    #		   break
    # tweets_file = open(tweets_data_path, 'r')

    #	for line in tweets_file:
    #            try:
    #                tweet = (json.loads(line))
    #                #tweets_data.append(tweet)
    #            except:
    #                continue
    # print (len(tweets_data))

    # Structuring Tweets
    print('Structuring Tweets\n')
    data = {'text': [], 'lang': [], 'country': [], 'source': []}

    for item in tweet:
        data['text'].append(item['text'])
        data['lang'].append(item['lang'])
        data['country'].append(item['user']['location'])
        data['source'].append(item['source'])
    tweets = pd.DataFrame(data)
    tweets.describe()


    pp = PdfPages('test.pdf')
    # Analyzing Tweets by Language
    print('Analyzing tweets by language\n')
    tweets_by_lang = tweets['lang'].value_counts()
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Languages', fontsize=15)
    ax.set_ylabel('Number of tweets', fontsize=15)
    ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
    tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')
    plt.savefig('tweet_by_lang', format='png')
    pp.savefig()

    # Analyzing Tweets by Device
    print('Analyzing tweets by device\n')
    tweets_by_device = tweets['source'].value_counts()
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Devices', fontsize=15)
    ax.set_ylabel('Number of tweets', fontsize=15)
    ax.set_title('Top 5 devices', fontsize=15, fontweight='bold')
    tweets_by_device[:5].plot(ax=ax, kind='bar', color='red')
    plt.savefig('tweet_by_device', format='png')
    pp.savefig()

    # Analyzing Tweets by Country
    print('Analyzing tweets by country\n')
    tweets_by_country = tweets['country'].value_counts()
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Countries', fontsize=15)
    ax.set_ylabel('Number of tweets', fontsize=15)
    ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
    tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')
    plt.savefig('tweet_by_country', format='png')
    pp.savefig()
    pp.close()


if __name__ == '__main__':
    main()
