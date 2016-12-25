import praw
import configloader
import subredditmodel
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from charts import Charts as ch


#given a min and max return a reasonable number of ticks for an axis
#as a list
def generate_axes(mmin, mmax):
	span = mmax - mmin
	#max 5 ticks
	i = 100
	while True:
		if span  / i > 5:
			i = i * 2
		else:
			break

	return np.arange(0, mmax, i)
	#range(0, mmax, i)

if __name__ == "__main__":
	cfg = configloader.ConfigLoader("credentials.ini")

	r = praw.Reddit(client_id = cfg.client_id,
					client_secret = cfg.client_secret,
					user_agent = cfg.user_agent)



	models = []
	sns.set(style="white", palette="muted", color_codes=True)
	f, axes = plt.subplots(8, 3, figsize=(10, 90), sharey=True)
	sns.despine(left=True)

	subfile = open("subreddits.txt", 'r')
	x_i = 0
	y_i = 0

	index = 1
	for color, line in zip(sns.cubehelix_palette(24), subfile.read().split("\n")):
		print("Fetching subreddit %s (%d of 24)" % (line, index))
		sub = subredditmodel.SubredditModel(praw_object=r,
													subreddit=line)
		df = sub.get_df()
		ax = sns.distplot(df["Length"], ax=axes[y_i, x_i], 
											 hist=False,
											 label=line,
											 kde_kws={"shade": True},
											 color=color
											 )

		#ax.set_xticks( generate_axes(df["Length"].min(), df["Length"].max()) )
		ax.set_xlim(0, 1200)
		ax.set_xticks( [0, 200, 400, 600, 800, 1000, 1200] )
		ax.set_yticklabels(['{:1.2f}%'.format(x*100) for x in ax.get_yticks()])
		
		x_i = x_i + 1
		if x_i == 3:
			x_i = 0
			y_i = y_i + 1

		index = index + 1

	plt.tight_layout()
	plt.show()