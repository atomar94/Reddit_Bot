import praw
import configloader
import subredditmodel

THRESHHOLD = 2000

#Given a submission object return a list of comments longer than threshhold.
def load_comments(submission):
	retlist = []
	submission.comments.replace_more(limit=10)
	for comment in submission.comments.list():
		if len(comment.body) > THRESHHOLD:
			retlist.append(comment)
	print()


if __name__ == "__main__":
	cfg = configloader.ConfigLoader("credentials.ini")

	r = praw.Reddit(client_id = cfg.client_id,
					client_secret = cfg.client_secret,
					user_agent = cfg.user_agent)

	askreddit_model = subredditmodel.SubredditModel(praw_object=r, 
													subreddit="askreddit")
	print(askreddit_model.get_score_distribution())