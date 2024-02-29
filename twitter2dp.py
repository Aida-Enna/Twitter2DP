# Humans must learn to apply their intelligence correctly and evolve beyond their current state.
# People must change. Otherwise, even if humanity expands into space, it will only create new
# conflicts, and that would be a very sad thing. - Aeolia Schenberg, 2091 A.D.


import ast
from colorama import Fore, Back, Style
import discord
import json
import os
import time
from dotenv import load_dotenv
from twikit import Client

load_dotenv()
bot = discord.Bot()

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
		
@bot.event
async def on_ready():
	print(f"{bot.user} is ready and online, checking every {CHECK_TIMER_IN_SECONDS} seconds!")
	while True:
		await get_latest_tweets()
		time.sleep(int(CHECK_TIMER_IN_SECONDS))

async def get_latest_tweets():
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
		channel = bot.get_channel(int(twitter_user['posting_channel']))
		#https://twitter.com/Username/status/TweetID
		tweetlink = f'https://twitter.com/{twitter_user["account_to_check"]}/status/{user_tweets[0].id}'
		print(f"New tweet found from {twitter_user['account_to_check']} (ID: {user_tweets[0].id}), sending it on it's way to channel {twitter_user['posting_channel']}!")
		#replace the keyword <tweetlink> with the actual twitter link.
		await channel.send(twitter_user['posting_text'].replace("<tweetlink>", tweetlink))
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
	print(Style.RESET_ALL)
	bot.run(os.getenv('DISCORD_BOT_TOKEN'))
	