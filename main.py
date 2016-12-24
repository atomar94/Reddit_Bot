import praw
import configloader
import subredditmodel
import matplotlib.pyplot as plt
from scipy.stats import kendalltau
import seaborn as sns
from charts import Charts as ch

if __name__ == "__main__":
	cfg = configloader.ConfigLoader("credentials.ini")

	r = praw.Reddit(client_id = cfg.client_id,
					client_secret = cfg.client_secret,
					user_agent = cfg.user_agent)



	models = []
	sns.set(style="white", palette="muted", color_codes=True)
	f, axes = plt.subplots(5, 5, figsize=(12, 12))
	sns.despine(left=True)

	subfile = open("subreddits.txt", 'r')
	x_i = 0
	y_i = 0
	for line in subfile.read().split("\n"):
		print("Fetching subreddit %s" % line)
		sub = subredditmodel.SubredditModel(praw_object=r,
													subreddit=line)
		sns.distplot(sub.get_df()["Length"], ax=axes[x_i, y_i], bins=15, label=line)

		x_i = x_i + 1
		if x_i == 5:
			x_i = 0
			y_i = y_i + 1

	
	plt.setp(axes, yticks=[])
	plt.tight_layout()
	plt.show()