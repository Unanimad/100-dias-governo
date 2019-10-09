import csv

from utils import get_statuses_between_dates

screen_name = 'jairbolsonaro'
start_at = '01012019'
end_at = '08102019'

csv_file = open('../data/' + screen_name + '.csv',
                'w',  newline='', encoding='utf-8', )
writer = csv.writer(csv_file, delimiter=';')
writer.writerow(["id", "created_at", "text",
                 "retweet_count", "favorite_count"])


get_statuses_between_dates(screen_name, start_at, end_at, writer)
