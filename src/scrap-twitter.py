import csv
import datetime

from os import path

from utils import get_statuses_between_dates, conn_api, get_file

TWITTER_API_CONSUMER_KEY = ''
TWITTER_API_CONSUMER_SECRET_KEY = ''
TWITTER_API_ACCESS_TOKEN = ''
TWITTER_API_ACCESS_TOKEN_SECRET = ''

screen_name = 'jairbolsonaro'
start_at = '01012019'
end_at = datetime.datetime.now().strftime('%d%m%Y')

f = f'../data/{screen_name}.csv'

csv_file = open(f, 'w',  newline='', encoding='utf-8',)
writer = csv.writer(csv_file, delimiter=';')
writer.writerow(["id", "created_at", "text",
                 "retweet_count", "favorite_count"])

api = conn_api(TWITTER_API_CONSUMER_KEY, TWITTER_API_CONSUMER_SECRET_KEY,
               TWITTER_API_ACCESS_TOKEN, TWITTER_API_ACCESS_TOKEN_SECRET)
get_statuses_between_dates(api, screen_name, start_at, end_at, writer)
