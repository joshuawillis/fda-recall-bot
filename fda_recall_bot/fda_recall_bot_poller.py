#!/usr/bin/env python

import requests
import tweepy
import datetime
from math import ceil


class FDA_Recall:
    def __init__(self):
        self.today_YYYYMMDD = (datetime.datetime.today()-datetime.timedelta(1)).strftime('%Y%m%d')
        self.today = (datetime.datetime.today()-datetime.timedelta(1)).strftime('%m/%d/%Y')


    def get_recall(self):

        """Polls the API using the company id and API token key for all of the employee names and ids.
          Returns a dictionary of names and ids of employees.
          """
        url = "https://api.fda.gov/food/enforcement.json?search=recall_initiation_date:{today}&limit=100".format(today=self.today_YYYYMMDD)
        r = requests.get(url)
        json_data = r.json()
        print(json_data["error"]['code'])
        if json_data['error']:
            self.tweet("No recalls for {today}".format(today=self.today))
        else:
            for element in json_data["results"]:
                print("##############################################")
                tweet_string = "RECALL of {product} on {date} from {company} for {reason}".format(
                    product=element["product_description"],
                    date=element["recall_initiation_date"],
                    company=element["recalling_firm"],
                    reason=element["reason_for_recall"],
                )
                print(tweet_string)
                self.tweet(tweet_string)
                print("##############################################")

    def tweet(self, tweet):
        """if tweet is more than 240 characters get status of first tweet and reply to it"""
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        length_of_tweet = len(tweet)
        if length_of_tweet > 240:
            number_of_tweets = ceil(length_of_tweet / 240)
            number_of_tweets_array = range(1, number_of_tweets)
            tweet_object = api.update_status(tweet[0:239])
            for number in number_of_tweets_array:
                print(240 * number)
                print(tweet[240 * number : 240 * (number + 1)])
                tweet_object = api.update_status(
                    tweet[240 * number : 240 * (number + 1)], tweet_object.id
                )
        else:
            api.update_status(tweet)

def main():
    recaller = FDA_Recall()
    recaller.get_recall()


if __name__ == "__main__":
    main()
