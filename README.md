# Twitter2DP - Twitter to Discord (Python)

A simple script that will check on a list of user's last tweets and send them to the specified webhook if there's a new one, on a configurable timer.

Big thanks to the [Twikit API wrapper](https://github.com/d60/twikit) for making this possible!

## Installation
``pip install -r requirements.txt``

1. Rename the ".env_example" and "users.json_example" files to remove the "_example" from both. Fill them out, there is no limit on the amount of users you can add.
2. Run the script with ``python twitter2dp.py``

Optional arguments for users.sjon

webhook_avatar_url - a URL pointing to the image the webhook should use as it's profile picture
webhook_name - a name the webhook should use when posting

Possible improvements:

* An accounts.json with some twitter accounts in it which the program will swap between every so often to avoid rate limiting/account closure?
