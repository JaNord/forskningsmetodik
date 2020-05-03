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
    tweets_data_path = 'bigdata.json'

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

    # Analyzing tweets by quarantine vs isolation vs crisis (relevant)
    print('Analyzing tweets by amount (relevance)\n')
    tweets['quarantine'] = tweets['text'].apply(lambda tweet: word_in_text('quarantine', tweet))
    tweets['isolation'] = tweets['text'].apply(lambda tweet: word_in_text('isolation', tweet))
    tweets['crisis'] = tweets['text'].apply(lambda tweet: word_in_text('crisis', tweet))

    tweets['covid-19'] = tweets['text'].apply(lambda tweet: word_in_text('covid-19', tweet))
    tweets['corona'] = tweets['text'].apply(lambda tweet: word_in_text('corona', tweet))
    tweets['relevant'] = tweets['text'].apply(
        lambda tweet: word_in_text('covid-19', tweet) or word_in_text('corona', tweet))

    tweets_by_relevance = [tweets[tweets['relevant'] == True]['quarantine'].value_counts()[True],
                          tweets[tweets['relevant'] == True]['isolation'].value_counts()[True],
                          tweets[tweets['relevant'] == True]['crisis'].value_counts()[True]]

    pre_tweets = ['quarantine','isolation', 'crisis']
    x_pos = list(range(len(pre_tweets)))
    width = 0.8
    fig, ax = plt.subplots()
    plt.bar(x_pos, tweets_by_relevance, width, alpha=1, color='g')
    ax.set_ylabel('Number of tweets', fontsize=10)
    ax.set_title('Amount, quarantine vs isolation vs crisis (relevance with corona and covid-19)', fontsize=8, fontweight='bold')
    ax.set_xticks([p + 0.4 * width for p in x_pos])
    ax.set_xticklabels(pre_tweets)
    plt.savefig('tweet_by_amount', format='png')
    pp.savefig()

    # Analyzing tweets by quarantine vs isolation vs crisis (relevant)
    print('Analyzing tweets by amount trump vs biden (relevance)\n')
    tweets['trump'] = tweets['text'].apply(lambda tweet: word_in_text('trump', tweet))
    tweets['biden'] = tweets['text'].apply(lambda tweet: word_in_text('biden', tweet))

    tweets['quarantine'] = tweets['text'].apply(lambda tweet: word_in_text('quarantine', tweet))
    tweets['isolation'] = tweets['text'].apply(lambda tweet: word_in_text('isolation', tweet))
    tweets['crisis'] = tweets['text'].apply(lambda tweet: word_in_text('crisis', tweet))
    tweets['relevant'] = tweets['text'].apply(
        lambda tweet: word_in_text('quarantine', tweet) or word_in_text('isolation', tweet) or word_in_text('crisis', tweet))

    tweets_by_relevance = [tweets[tweets['relevant'] == True]['trump'].value_counts()[True],
                           tweets[tweets['relevant'] == True]['biden'].value_counts()[True]]

    pre_tweets = ['trump', 'biden']
    x_pos = list(range(len(pre_tweets)))
    width = 0.8
    fig, ax = plt.subplots()
    plt.bar(x_pos, tweets_by_relevance, width, alpha=1, color='g')
    ax.set_ylabel('Number of tweets', fontsize=10)
    ax.set_title('Amount, trump vs biden (relevance with quarantine isolation and crisis)', fontsize=8,
                 fontweight='bold')
    ax.set_xticks([p + 0.2 * width for p in x_pos])
    ax.set_xticklabels(pre_tweets)
    plt.savefig('tweet_by_amount', format='png')
    pp.savefig()

    # Analyzing tweets by quarantine vs isolation
    print('Analyzing tweets by amount\n')
    tweets['quarantine'] = tweets['text'].apply(lambda tweet: word_in_text('quarantine', tweet))
    tweets['isolation'] = tweets['text'].apply(lambda tweet: word_in_text('isolation', tweet))
    pre_tweets = ['quarantine','isolation']
    tweets_by_amount = [tweets['quarantine'].value_counts()[True], tweets['isolation'].value_counts()[True]]
    x_pos = list(range(len(pre_tweets)))
    width = 0.8
    fig, ax = plt.subplots()
    plt.bar(x_pos, tweets_by_amount, width, alpha=1, color='g')
    ax.set_ylabel('Number of tweets', fontsize=15)
    ax.set_title('Amount, quarantine vs isolation', fontsize=15, fontweight='bold')
    ax.set_xticks([p + 0.2 * width for p in x_pos])
    ax.set_xticklabels(pre_tweets)
    plt.savefig('tweet_by_amount', format='png')
    pp.savefig()
    pp.close()



if __name__ == '__main__':
    main()
