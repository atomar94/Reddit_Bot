

class SubredditModel:

	THRESHHOLD = 2000

	#returns the percent of comments above the threshhold
	def get_percent_long(self):
		return(len(self.comments) / self.comments_read)


	#return a list of scores of the long comments.
	def get_score_distribution(self):
		self.scores = [x.score for x in self.comments]
		return self.scores

	#Given a submission object append to the class list the comments longer than threshhold.
	def load_submission_comments(self, submission):
		submission.comments.replace_more(limit=32)
		comment_list = submission.comments.list()
		self.comments_read = self.comments_read + len(comment_list)

		for comment in comment_list:
			if len(comment.body) > self.THRESHHOLD:
				self.comments.append(comment)

	def __init__(self, praw_object, subreddit):
		self.praw = praw_object
		self.subreddit = subreddit
		self.comments = []
		self.scores = []
		self.comments_read = 0

		for submission in self.praw.subreddit(self.subreddit).hot(limit=25):
			self.load_submission_comments(submission)
