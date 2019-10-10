import twitter
import time
import datetime


TWITTER_API_CONSUMER_KEY = 'Nf135wAjYubMMaGZLAnmFcNcd'
TWITTER_API_CONSUMER_SECRET_KEY = 'IIdkmvmRBpONqV6PceciYWCyAoPMJmjQ0VKVB2CgEVknGPdPmp'
TWITTER_API_ACCESS_TOKEN = '1119658154655199238-jJ9oiBlYe9YVz1t5FKESOGa8t3I2CG'
TWITTER_API_ACCESS_TOKEN_SECRET = 'V3jczJqJJECjl1ik2kWGvPabWhnbulGugeDchnDjqbSdB'


def get_statuses_between_dates(screen_name, start_at, end_at, writer):
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
    instances = []
    size = 0

    start_at = datetime.datetime.strptime(start_at, '%d%m%Y')
    end_at = datetime.datetime.strptime(end_at, '%d%m%Y')

    api = conn_api()

    start_time = time.time()

    print(
        f"Fetching tweets from @{screen_name} between {start_at} and {end_at}")

    tmp_statuses = api.GetUserTimeline(screen_name=screen_name)

    if len(tmp_statuses) > 0:
        for status in tmp_statuses:
            created_at = twitter_date(status.created_at)

            if created_at < end_at and created_at > start_at:
                add_status(status, screen_name, writer)
                print(
                    f'Tweet {status.id_str} founded! Created at {created_at}')

        last_status = 0

        while twitter_date(tmp_statuses[-1].created_at) > start_at:
            tmp_statuses = api.GetUserTimeline(
                screen_name=screen_name, max_id=tmp_statuses[-1].id)

            if last_status == tmp_statuses[-1].id:
                print('No more tweets!')
                break

            last_status = tmp_statuses[-1].id

            for status in tmp_statuses:
                created_at = twitter_date(status.created_at)

                if created_at < end_at and created_at > start_at:
                    add_status(status, screen_name, writer)
                    print(
                        f'Tweet {status.id_str} founded! Created at {created_at}')

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


def conn_api():
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
