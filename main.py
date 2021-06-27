from predict import predict
from tweets import pull_tweets


if __name__ == "__main__":
    csv_path = '.\\output_files\\tweets.csv'

    # pull_tweets(csv_path)
    predict(csv_path)
