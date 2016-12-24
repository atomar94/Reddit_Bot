import pandas as pd

class SubredditModel:

	#THRESHHOLD = 2000
	THRESHHOLD = 100

	def load(self, subreddit=""):
		if subreddit == "":
			subreddit = self.subreddit
		else:
			self.subreddit = subreddit

		comment_list = []
		#for submission in self.praw.subreddit(self.subreddit).hot(limit=25):
		for submission in self.praw.subreddit(self.subreddit).hot(limit=2):
			comment_list = self.get_submission_comments(submission) + comment_list

		self.comment_df = pd.DataFrame({"Length": [len(x.body) for x in comment_list],
										"Score": [x.score for x in comment_list]
										})
		print("All Comments for %s loaded" % self.subreddit)

	def get_df(self):
		return self.comment_df

	#Given a submission object append to the class list the comments longer than threshhold.
	def get_submission_comments(self, submission):
		retlist = []
		#submission.comments.replace_more(limit=32)
		submission.comments.replace_more(limit=1)
		comment_list = submission.comments.list()
		self.comments_read = self.comments_read + len(comment_list)

		for comment in comment_list:
			if len(comment.body) > self.THRESHHOLD:
				retlist.append(comment)

		return retlist

	def __init__(self, praw_object, subreddit):
		self.praw = praw_object
		self.subreddit = subreddit
		self.comments = []
		self.scores = []
		self.comments_read = 0

		self.load(subreddit)