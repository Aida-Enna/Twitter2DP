# Humans must learn to apply their intelligence correctly and evolve beyond their current state.
# People must change. Otherwise, even if humanity expands into space, it will only create new
# conflicts, and that would be a very sad thing. - Aeolia Schenberg, 2091 A.D.

import ast
from colorama import Fore, Back, Style, init
import json
import requests
import os
import time
from dotenv import load_dotenv
from twikit import Client

load_dotenv()
init(autoreset=True)

YOUR_TWITTER_USERNAME = os.getenv('YOUR_TWITTER_USERNAME')
YOUR_TWITTER_EMAIL = os.getenv('YOUR_TWITTER_EMAIL')
YOUR_TWITTER_PASSWORD = os.getenv('YOUR_TWITTER_PASSWORD')
CHECK_TIMER_IN_SECONDS = os.getenv('CHECK_TIMER_IN_SECONDS')

# Initialize twikit client (https://github.com/d60/twikit)
client = Client('en-US')
# Login to the service with provided user credentials
client.login(
    auth_info_1=YOUR_TWITTER_USERNAME ,
    auth_info_2=YOUR_TWITTER_EMAIL,
    password=YOUR_TWITTER_PASSWORD
)

def check_users_json():
	try:
		raw_json = open('users.json')
		twitter_users = json.load(raw_json)
	except:
		print(Fore.RED + f"ERROR: Something went wrong with loading the users.json file. Please check that it is a valid JSON and try again.")
		exit()

	for twitter_user in twitter_users:
		#print(twitter_user)
		if 'account_to_check' not in twitter_user:
			print(Fore.RED + 'ERROR: One of the JSON entries is missing an account_to_check entry! Please check the users.json file and relaunch.')
			exit()
		if 'posting_text' not in twitter_user:
			print(Fore.RED + f"ERROR: The JSON entry for {twitter_user['account_to_check']} is missing a posting_text entry! Please check the users.json file and relaunch.")
			exit()
		if 'webhook_url' not in twitter_user:
			print(Fore.RED + f"ERROR: The JSON entry for {twitter_user['account_to_check']} is missing a webhook_url entry! Please check the users.json file and relaunch.")
			exit()

def get_latest_tweets():
	raw_json = open('users.json')
	twitter_users = json.load(raw_json)

	for twitter_user in twitter_users:
		#If we don't have a previous tweet recorded, just put something there so it fails successfully.
		if 'previous_tweet_id' not in twitter_user:
			twitter_user['previous_tweet_id'] = 'null'

		user = client.get_user_by_screen_name(twitter_user['account_to_check'])
		user_tweets = user.get_tweets('Tweets')
		
		if twitter_user['previous_tweet_id'] == user_tweets[0].id:
			#No new tweet, moving on...
			continue
		
		#omg a hit tweet, let's post it
		#channel = bot.get_channel(int(twitter_user['posting_channel']))
		#https://twitter.com/Username/status/TweetID
		tweetlink = f'https://twitter.com/{twitter_user["account_to_check"]}/status/{user_tweets[0].id}'
		
		print(f"New tweet found from {twitter_user['account_to_check']} (ID: {user_tweets[0].id}), sending it to the webhook!")
		
		#replace the keyword <tweetlink> with the actual twitter link.
		payload = {'content': twitter_user['posting_text'].replace("<tweetlink>", tweetlink)}
		response = requests.post(twitter_user['webhook_url'], json=payload)
		
		#save the previous ID so we don't keep posting
		twitter_user['previous_tweet_id'] = user_tweets[0].id
	
	#write the JSON with the new previous tweet IDs
	with open('users.json', 'w') as f:
		json.dump(twitter_users, f, ensure_ascii=False, sort_keys=True, indent='\t')
	
if __name__ == '__main__':
	print(Fore.CYAN + '████████╗██╗    ██╗██╗████████╗████████╗███████╗██████╗ ██████╗ ██████╗ ██████╗ ')
	print(Fore.CYAN + '╚══██╔══╝██║    ██║██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗╚════██╗██╔══██╗██╔══██╗')
	print(Fore.CYAN + '   ██║   ██║ █╗ ██║██║   ██║      ██║   █████╗  ██████╔╝ █████╔╝██║  ██║██████╔╝')
	print(Fore.CYAN + '   ██║   ██║███╗██║██║   ██║      ██║   ██╔══╝  ██╔══██╗██╔═══╝ ██║  ██║██╔═══╝ ')
	print(Fore.CYAN + '   ██║   ╚███╔███╔╝██║   ██║      ██║   ███████╗██║  ██║███████╗██████╔╝██║     ')
	print(Fore.CYAN + '   ╚═╝    ╚══╝╚══╝ ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝     ')
	print('')
	check_users_json()
	get_latest_tweets()
	