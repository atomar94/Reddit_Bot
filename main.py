import praw
import configloader


#Given a submission object return a list of comment text.
def load_comments(submission):
	submission.comments.replace_more(limit=0)
	return [x.body for x in submission.comments.list()]


if __name__ == "__main__":
	cfg = configloader.ConfigLoader("credentials.ini")

	r = praw.Reddit(client_id = cfg.client_id,
					client_secret = cfg.client_secret,
					user_agent = cfg.user_agent)

	for submission in r.subreddit("askreddit").hot(limit=2):
		comment_list = load_comments(submission)
		for comment in comment_list:
			if "reddit" in comment:
				try:
					print(comment)
				#because python doesnt like windows unicode translation
				except UnicodeEncodeError:
					print("a comment could not displayed.")
				input()

