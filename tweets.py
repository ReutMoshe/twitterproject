import pandas as pd
import tweepy
from authentication import authenticate_api


def get_time_category_in_day(hour):
    if 4 <= hour < 12:
        return 1
    elif 12 <= hour < 20:
        return 2
    else:
        return 3


def get_followers_group(followers_count):
    if 0 <= followers_count < 1000:
        return 1
    elif 1000 <= followers_count < 5000:
        return 2
    else:
        return 3


def get_tweet_data(tweet, hashtag_index):
    tweet_media = tweet.entities.get('media')
    if tweet_media:
        has_images = True
    else:
        has_images = False

    data = (tweet.id,
            hashtag_index,
            get_time_category_in_day(tweet.created_at.hour),
            len(tweet.text),
            int(tweet.user.verified),
            tweet.user.followers_count,
            get_followers_group(tweet.user.followers_count),
            tweet.favorite_count,
            int(has_images),
            int(tweet.retweet_count > 10),
            tweet.retweet_count)

    return data

def get_hashtag_tweets(api, hashtag, hashtag_index, since, count):
    print("searching for " + hashtag)
    tweets = []
    # Search only for original tweets
    for tweet in tweepy.Cursor(api.search, q=hashtag + " -filter:retweets", since=since).items(count):
        try:
            data = get_tweet_data(tweet, hashtag_index)
            tweets.append(data)

            if len(tweets) % 100 == 0:
                print("collected {} tweets for {}".format(len(tweets), hashtag))
        except tweepy.TweepError as e:
            continue
        except StopIteration:
            break
    return tweets

def pull_tweets(csv_path):
    auth = authenticate_api()
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    tweets = []
    pull_since = '2020-01-01'
    hashtags_to_search = ['#Israel', '#Palestine']
    tweets_to_pull_per_hashtag = 3000

    print("pulling tweets")
    for index, hashtag in enumerate(hashtags_to_search):
        hashtag_index = index+1
        hashtag_tweets = get_hashtag_tweets(api, hashtag, hashtag_index, since=pull_since, count=tweets_to_pull_per_hashtag)
        tweets.extend(hashtag_tweets)

    print("creating dataframe")
    df = pd.DataFrame(tweets, columns=['tweed_id', 'hashtag', 'time_in_day', 'tweet_length', 'is_user_verified', 'user_followers', 'user_followers_group', 'tweet_likes', 'tweet_has_media_attached', 'is_popular', 'retweet_count'])

    print ("exporting to csv")
    df.to_csv(path_or_buf=csv_path)
