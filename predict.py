from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd


def print_score(model, x, y):
    score = model.score(x, y)
    print("Train score: {}%".format(score * 100))


def show_table_plot(data, feature, values):
    table = pd.pivot_table(data, index=feature, values=values)
    table.plot(kind='bar')
    print(table, '\n')

def show_tables(data):
    for feature in ['hashtag', 'time_in_day', 'is_user_verified', 'user_followers_group']:
        show_table_plot(data, feature, ['is_popular'])

def predict(csv_path):
    data = pd.read_csv(csv_path)
    show_tables(data)

    x = data[['hashtag', 'time_in_day', 'tweet_length', 'is_user_verified', 'user_followers', 'tweet_likes']]
    y = data['retweet_count']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    model = LinearRegression()
    model.fit(x_train, y_train)

    print_score(model, x_train, y_train)
    print_score(model, x_test, y_test)

    predictions = model.predict(x_test)

    # Save diffs to csv
    diff = pd.DataFrame({'Actual value': y_test, 'Predicted value': predictions})
    diff.to_csv(path_or_buf='.\\output_files\\tweets.csv')

    # Draw linear graph
    plt.clf()
    plt.scatter(y_test, predictions)
    plt.plot(range(250), range(250), color='red', linewidth=2)
    plt.show()
