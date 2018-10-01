import praw
import config 
import time
import os
import requests


def bot_login():

    r = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "pamplemouseplanet's comment responder bot v0.1")
    print('logging in')
    return r


def run_bot(r, comments_replied):
	# getting 25 comments with keyword in comments
    for comment in r.subreddit('test').comments(limit=25):
        if '!SeinfeldQuote' in comment.body and comment.id not in comments_replied and not comment.author == r.user.me():
            print('String with \"!SeinfeldQuote\" found in comment ' + comment.id)
            # comment.reply('pamplemousse is French for grapefruit')
            print("replied to comment " + comment.id)

            # Builds the reply with API quote
            comment_reply = "A little Seinfeld for ya:\n\n"
            data = requests.get('https://seinfeld-quotes.herokuapp.com/random').json()
            quote = data['quote']
            author = data['author']
            comment_reply += ">" + quote + "\n>\n" + ">" + "*" + author + "*"
            comment_reply += "\n\n^This ^joke ^brought ^to ^you ^by ^[seinfeld-quotes](https://seinfeld-quotes.herokuapp.com)"
            # writes comment and tracks id
            comment.reply(comment_reply)
            comments_replied.append(comment.id)


            with open("comments_replied", "a") as file:
            	file.write("comment id: " + comment.id + "\n")
            	# file.write("comment body: " + comment.body + "\n")

    print("sleep for 10 seconds")
    # sleep for 10 seconds
    time.sleep(10)

def get_saved_comments():
	if not os.path.isfile("comments_replied.txt"):
		comments_replied = []
	else: 
		with open("comments_replied.txt", "r") as file: 
			comments_replied = file.read()
			comments_replied = comments_replied.split("\n")
			comments_replied = filter(None, comments_replied)

	return comments_replied

r = bot_login()
comments_replied = []
print(comments_replied)

while True: 
	run_bot(r, comments_replied)