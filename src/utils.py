import csv
import twitter
import time
import datetime


def get_statuses_between_dates(api, screen_name, start_at, end_at, writer):
    """ Get User Tweets between two dates

    Args:
        screen_name (str): The screen name, handle, or alias that
                            this user identifies themselves with.
        start_at (datetime): When the mining started
        end_at (datetime): When the mining ended
        save (bool): If True save status into database

    Returns:
        Saved tweets
    """
    tweets = []

    start_at = datetime.datetime.strptime(start_at, '%d%m%Y')
    end_at = datetime.datetime.strptime(end_at, '%d%m%Y')

    start_time = time.time()

    print(
        f"Fetching tweets from @{screen_name} between {start_at} and {end_at}")

    tmp_statuses = api.GetUserTimeline(screen_name=screen_name)

    if len(tmp_statuses) > 0:
        for status in tmp_statuses:
            created_at = twitter_date(status.created_at)

            if start_at < created_at < end_at:
                if status.id not in tweets:
                    tweets.append(status.id)
                    add_status(status, screen_name, writer)

        while (twitter_date(tmp_statuses[-1].created_at) > start_at):
            tmp_statuses = api.GetUserTimeline(
                screen_name=screen_name, trim_user=True, max_id=tmp_statuses[-1].id)

            if status.id == tmp_statuses[-1].id:
                print(f'More than 3.2k tweets were post since {end_at}')
                break

            for status in tmp_statuses:
                created_at = twitter_date(status.created_at)

                if start_at < created_at < end_at:
                    if status.id not in tweets:
                        tweets.append(status.id)
                        add_status(status, screen_name, writer)
                        print(
                            f'Tweet {status.id_str} founded! Created at {created_at}')

        tweets = []

        print("Fetching done! Spend {seconds} seconds!".format(
            seconds=time.time() - start_time))

    else:
        print('No tweets posted!')


def twitter_date(value):
    """Convert Twitter date to Datetime object

    Args:
        value (str): Twitter date

    Returns:
        datetime: Converted datetime object
    """
    split_date = value.split()
    del split_date[0], split_date[-2]
    value = ' '.join(split_date)

    return datetime.datetime.strptime(value, '%b %d %H:%M:%S %Y')


def add_status(status, screen_name, writer):  # TODO: Return bool if saved
    output = [
        status.id, twitter_date(status.created_at),
        status.full_text.replace("\n", ""),
        status.retweet_count, status.favorite_count
    ]
    writer.writerow(output)


def conn_api(TWITTER_API_CONSUMER_KEY, TWITTER_API_CONSUMER_SECRET_KEY, TWITTER_API_ACCESS_TOKEN,
             TWITTER_API_ACCESS_TOKEN_SECRET):
    """ Connect to Twitter API

    Returns:
        object: Connection
    """
    api = twitter.Api(
        consumer_key=TWITTER_API_CONSUMER_KEY,
        consumer_secret=TWITTER_API_CONSUMER_SECRET_KEY,
        access_token_key=TWITTER_API_ACCESS_TOKEN,
        access_token_secret=TWITTER_API_ACCESS_TOKEN_SECRET,
        sleep_on_rate_limit=True,
        tweet_mode='extended'
    )

    return api


def get_file(f):
    data = []
    with open(f, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.reader(scraped, delimiter=';')
        next(reader, None)
        for i, row in enumerate(reader):
            if row:  # avoid blank lines
                columns = [str(i), row[0], row[1], row[2], row[3], row[4]]
                data.append(columns)
    return data
