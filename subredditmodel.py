import pandas as pd
import numpy as np

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

		self.comment_df['Filtered_Score'] = self.filter_comments(self.comment_df['Score'])


	#TODO: Making this general is adding complexity. Scale it back
	# given a pandas df and a series name, count the occurances of each item and
	# set any that appear too often (within the top +-1 sigma) to nan, along with
	# the items in the other columns for that row.
	#
	# Returns a list of that series but with any occurances too frequently
	# set to np.nan
	def filter_comments(self, pdseries):

		dflist = pdseries.tolist()
		score_count = {}
		for score in dflist:
			count = score_count.get(score, 0) + 1
			score_count[score] = count

		score_count_df = pd.DataFrame(list(score_count.items()), columns=["Score", "Count"])
		limit = score_count_df['Count'].quantile(q=0.9) # above this gets trimmed
		for key in score_count.keys():
			if score_count[key] > limit:
				score_count[key] = limit

		filtered_scores = []
		for score in dflist:
			if score_count.get(score, 1) <= 0:
				filtered_scores.append( (np.nan) )
			else:
				filtered_scores.append(score)
				score_count[score] -= 1

		return filtered_scores
		

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
			self.sub_limit = 3
			self.comment_limit = 4
		else:
			self.sub_limit = 15
			self.comment_limit = 20


		self.praw = praw_object
		self.subreddit = subreddit
		self.comments = []
		self.scores = []
		self.comments_read = 0

		self.load(subreddit)