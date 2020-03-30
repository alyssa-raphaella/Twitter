import base64
import requests
import json
import pandas as pd


client_key = 'CfqZfNRTvcHdDRCo23PZt3ETa'
client_secret = '9NVfiSz9tcp2GvLDchPxfh2sNLHKpmUVwfvuxeCPwdjKM14upU'

key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type': 'client_credentials'
}

auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

access_token = auth_resp.json()['access_token']

search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

search_params = {
    'q': 'scott%20morrison%20-filter:retweets', # RT not included
    'count': 100, #max
    'until': '2020-03-27', #7 days retainment
    'include_entities': 'false',
    'lang': 'en',
    'tweet_mode': 'extended'
}

search_url = '{}1.1/search/tweets.json'.format(base_url)

search_resp = requests.get(search_url, headers=search_headers, params=search_params)

tweet_data = search_resp.json()

tweet_list = []
for x in tweet_data['statuses']:
    tweet_list.append(x)

with open('tweet.txt', 'w') as file:
    file.write(json.dumps(tweet_list, indent = 4))

fetch_list = []
with open('tweet.txt', encoding = 'utf-8') as json_file:
    all_data = json.load(json_file)
    for d in all_data:
        created_at = d['created_at']
        tweet_id = d['id']
        text = d['full_text']

        fetch_list.append({'created_at': created_at,
                           'tweet_id': str(tweet_id),
                           'text': str(text)
                           })

tweet_json = pd.DataFrame(fetch_list, columns = ['created_at', 'tweet_id', 'text'])
tweet_json.to_csv('tweet.csv', index = False)

print(tweet_json)

print(len(tweet_data['statuses']))