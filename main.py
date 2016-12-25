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
	f, axes = plt.subplots(9, 3, figsize=(12, 42))
	sns.despine(left=True)

	subfile = open("subreddits.txt", 'r')
	x_i = 0
	y_i = 0

	for color, line in zip(sns.cubehelix_palette(25), subfile.read().split("\n")):
		print("Fetching subreddit %s" % line)
		sub = subredditmodel.SubredditModel(praw_object=r,
													subreddit=line)
		df = sub.get_df()
		ax = sns.distplot(df["Length"], ax=axes[y_i, x_i], 
											 label=line,
											 hist=False,
											 kde_kws={"shade": True},
											 color=color
											 )

		ax.set_xticks( generate_axes(df["Length"].min(), df["Length"].max()) )
		
		old_vals = ax.get_yticks()
		thinned_vals = []
		for i, tick in enumerate(old_vals):
			if i % 2 == 0:
				thinned_vals.append(tick)

		ax.set_yticks(thinned_vals)
		ax.set_yticklabels(['{:1.2f}%'.format(x*100) for x in thinned_vals])
		

		x_i = x_i + 1
		if x_i == 3:
			x_i = 0
			y_i = y_i + 1

	
	#plt.setp(axes, yticks=[0, 0.5, 1.0])
	plt.tight_layout()
	plt.show()