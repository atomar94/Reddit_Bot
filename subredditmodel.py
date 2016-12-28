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

		newdf = self.filter_comments(self.comment_df)
		self.comment_df['Filtered_Score'] = newdf['Filtered_Score']
		self.comment_df['Filtered_Length'] = newdf['Filtered_Length']

	#TODO: Making this general is adding complexity. Scale it back
	def filter_comments(self, df):

		dflist = df['Score'].tolist()
		score_count = {}
		#count the occurances of each Score.
		for score in dflist:
			count = score_count.get(score, 0) + 1
			score_count[score] = count

		#get the 85th percentile and of score occurnces and trim everything above that
		score_count_df = pd.DataFrame(list(score_count.items()), columns=["Score", "Count"])
		limit = score_count_df['Count'].quantile(q=0.85)
		for key in score_count.keys():
			if score_count[key] > limit:
				score_count[key] = limit

		filtered_scores = []
		filtered_length = []
		for index, row in df.iterrows():
			score = row['Score']
			length = row['Length']

			if score_count.get(score, 1) <= 0: #we've put <limit> amount of this score into the filtered_scores list.
				filtered_scores.append( np.nan )
				filtered_length.append( np.nan )
			else: #if the score_count hasn't been reached yet. 
				filtered_scores.append(score)
				filtered_length.append(length)
				score_count[score] -= 1

		filtered_df = pd.DataFrame({
									"Filtered_Score": filtered_scores,
									"Filtered_Length": filtered_length
								   })

		return filtered_df
		

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