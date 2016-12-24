import praw
import configloader


if __name__ == "__main__":
	cfg = configloader.ConfigLoader("credentials.ini")

	r = praw.Reddit(client_id = cfg.client_id,
					client_secret = cfg.client_secret,
					user_agent = cfg.user_agent)

	for submission in r.subreddit("askreddit").hot(limit=5):
		print(submission.title)