from instagrapi import Client
import time
import requests.exceptions
from urllib3.exceptions import MaxRetryError

username = "username"
password = "password"

friend_username = "friend_username"

client = Client()

client.login(username, password)

while True:
    friend = client.user_info_by_username(friend_username)
    friend_id = friend.pk

    max_retries = 3
    retry_delay = 2

    for retry in range(max_retries):
        try:
            stories = client.user_stories(friend_id)
            latest_story = stories[0] if stories else None

            if latest_story:
                client.direct_messages(friend_id, "Wonderful")

            break

        except MaxRetryError as e:
            if retry < max_retries - 1:
                print(f"Retry {retry + 1}/{max_retries} after {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise e

        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            break

    time.sleep(3600)
