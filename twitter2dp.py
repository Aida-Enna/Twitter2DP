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

# Initialize twikit client
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
		print(Fore.RED + "ERROR: Something went wrong with loading the users.json file. Please check that it is a valid JSON and try again.")
		exit()

	for twitter_user in twitter_users:
		print("Loading " + str(len(twitter_users)) + " twitter user(s) to monitor...")
		
		if 'account_to_check' not in twitter_user:
			print(Fore.RED + "ERROR: One of the JSON entries is missing an " + Fore.YELLOW + "account_to_check" + Fore.RED + " entry! Please check the users.json file and relaunch.")
			exit()
			
		if 'posting_text' not in twitter_user:
			print(Fore.RED + "ERROR: The JSON entry for " + Fore.WHITE + twitter_user['account_to_check'] + Fore.RED + " is missing a " + Fore.YELLOW + "posting_text" + Fore.RED + " entry! Please check the users.json file and relaunch.")
			exit()
			
		if 'webhook_url' not in twitter_user:
			print(Fore.RED + "ERROR: The JSON entry for " + Fore.WHITE + twitter_user['account_to_check'] + Fore.RED + " is missing a " + Fore.YELLOW + "webhook_url" + Fore.RED + " entry! Please check the users.json file and relaunch.")
			exit()
			
		if not twitter_user['account_to_check']:
			print(Fore.RED + "ERROR: One of the JSON entries has a blank " + Fore.YELLOW + "account_to_check" + Fore.RED + " entry! Please check the users.json file and relaunch.")
			exit()
			
		if not twitter_user['posting_text']:
			print(Fore.RED + "ERROR: The JSON entry for " + Fore.WHITE + twitter_user['account_to_check'] + Fore.RED + " has a blank " + Fore.YELLOW + "posting_text" + Fore.RED + " entry! Please check the users.json file and relaunch.")
			exit()
			
		if not twitter_user['webhook_url']:
			print(Fore.RED + "ERROR: The JSON entry for " + Fore.WHITE + twitter_user['account_to_check'] + Fore.RED + " has a blank " + Fore.YELLOW + "webhook_url" + Fore.RED + " entry! Please check the users.json file and relaunch.")
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
		
		lasttweet = "Nothing?"
		
		#print("Checking " + str(len(user_tweets)) + " tweet(s) for non-retweets...")
		for tweet in user_tweets:
			if not tweet.text.startswith("RT @"): #to be replaced with if tweet.retweeted == False when the API person fixes it
				#print("Found an original tweet! " + tweet.text)
				lasttweet = tweet
			#else:
				#print("Retweet...")
				
		#print(lasttweet)
		if lasttweet == "Nothing?":
			#print('No new non-retweet in the past 20? tweets, moving on...')
			continue
		
		if twitter_user['previous_tweet_id'] == lasttweet.id:
			#No new tweet, moving on...
			continue
		
		#omg a hit tweet, let's post it
		#https://twitter.com/Username/status/TweetID
		tweetlink = f'https://twitter.com/{twitter_user["account_to_check"]}/status/{lasttweet.id}'
		
		print(f"New tweet found from {twitter_user['account_to_check']} (ID: {lasttweet.id}), sending it to the webhook!")
		
		#replace the keyword <tweetlink> with the actual twitter link.
		payload = {
			'avatar_url': twitter_user['webhook_avatar_url'],
			'content': twitter_user['posting_text'].replace("<tweetlink>", tweetlink),
			'username': twitter_user['webhook_name']
		}
		response = requests.post(twitter_user['webhook_url'], json=payload)
		
		#save the previous ID so we don't keep posting
		twitter_user['previous_tweet_id'] = lasttweet.id
	
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
	print('Source available at https://github.com/Aida-Enna/Twitter2DP')
	check_users_json()
	print(Fore.GREEN + 'Configuration loaded successfully, now watching for new tweets every ' + CHECK_TIMER_IN_SECONDS + " seconds.")
	while True:
		get_latest_tweets()
		time.sleep(int(CHECK_TIMER_IN_SECONDS))
	