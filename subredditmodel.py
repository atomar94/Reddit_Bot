import pandas as pd

class SubredditModel:

	#so we dont pull as much data while just looking at graphical stuff
	testing = True

	def load(self, subreddit=""):
		if subreddit == "":
			subreddit = self.subreddit
		else:
			self.subreddit = subreddit

		comment_list = []
		for submission in self.praw.subreddit(self.subreddit).hot(limit=self.sub_limit):
			comment_list = self.get_submission_comments(submission) + comment_list

		self.comment_df = pd.DataFrame({"Length": [len(x.body) for x in comment_list],
										"Score": [x.score for x in comment_list]
										})


	def get_df(self):
		return self.comment_df


	#Given a submission object append to the class list the comments.
	def get_submission_comments(self, submission):
		submission.comments.replace_more(limit=self.comment_limit)
		comment_list = submission.comments.list()
		self.comments_read = self.comments_read + len(comment_list)
		return comment_list


	def __init__(self, praw_object, subreddit):

		if self.testing == True:
			self.sub_limit = 1
			self.comment_limit = 1
		else:
			self.sub_limit = 25
			self.comment_limit = 32


		self.praw = praw_object
		self.subreddit = subreddit
		self.comments = []
		self.scores = []
		self.comments_read = 0

		self.load(subreddit)