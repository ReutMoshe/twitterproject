from tweepy import OAuthHandler

def authenticate_api():
    access_token = '1394606262172667908-LgtVAq4p9SsmV9ctzDrNRHIU9UpvD2'
    access_token_secret = '0NWC1L5nDV5nzCpWJByujlia5modjOmJeC6WSeX3L4Q6M'
    consumer_key = 'IpgTqtI4dLMR4taG3KB6U0RzH'
    consumer_secret = 'SsVVFX36XTHNiev0yozCINYgo0mgbFmpajDhKTExwDKyO0Jr2u'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return auth
