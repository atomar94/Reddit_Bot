import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import subredditmodel

#Helper class for plotting
#Is static class so dont need to instantiate anything.
class Charts:

	#takes praw obj
	def kdeplot(r):
		sns.set(style="white", palette="muted", color_codes=True)
		f, axes = plt.subplots(8, 3, figsize=(10, 150))
		sns.despine(left=True)

		subfile = open("subreddits.txt", 'r')
		x_i = 0
		y_i = 0

		index = 1
		color_function = sns.color_palette("Set2", 12)

		for color, line in zip(color_function, subfile.read().split("\n")):
			print("Fetching subreddit %s (%d of 24)" % (line, index))
			sub = subredditmodel.SubredditModel(praw_object=r,
												subreddit=line)
			df = sub.get_df()

			xmax = df['Length'].quantile(0.95)
			ymax = df['Score'].quantile(0.80)
			xmin = 0
			ymin = min(-10, -1*ymax) #show upvotes to at least -10

			ax = sns.kdeplot(df['Length'], df['Score'], 
											ax=axes[y_i, x_i], 
											kind="hex",
											shade=True,
											color=color,
											gridsize=10
											#xlim=(0, xmax), 
											#ylim=(0, ymax)
											) 

			#ax.set_xticks( Charts.generate_axes(0, xmax) )
			ax.set_xlim(xmin, xmax)
			ax.set_ylim(ymin, ymax)
			#ax.set_yticklabels(['{:1.2f}%'.format(x*100) for x in ax.get_yticks()])
			x_i = x_i + 1
			if x_i == 3:
				x_i = 0
				y_i = y_i + 1

			index = index + 1

		subfile.close()

		plt.tight_layout()
		plt.subplots_adjust(wspace=0.2, hspace=0.4)
		plt.show()


	#takes a praw object
	#broken becuase jointplot is a different type of plot than the others.
	def jointplot(r):
		sns.set(style="white", palette="muted", color_codes=True)
		sns.despine(left=True)

		subfile = open("subreddits.txt", 'r')
		x_i = 0
		y_i = 0

		index = 1

		dfs = []
		for line in subfile.read().split("\n"):
			print("Fetching subreddit %s (%d of 24)" % (line, index))
			sub = subredditmodel.SubredditModel(praw_object=r,
												subreddit=line)
			dfs.append(sub.get_df())
			index = index + 1

		all_dfs = pd.concat(dfs)

		sns.jointplot(all_dfs['Length'], all_dfs['Score'], kind="hex", stat_func=kendalltau, color="#4CB391")

		subfile.close()

		plt.tight_layout()
		plt.subplots_adjust(wspace=0.2, hspace=0.2)
		plt.show()





















	#given a min and max return a reasonable number of ticks for an axis
	#as a list
	def generate_axes(mmin, mmax):
		span = mmax - mmin
		#max 5 ticks
		i = 25
		while True:
			if span  / i > 5:
				i = i * 2
			else:
				break

		return np.arange(0, mmax, i)

	#takes a praw object
	def plot_score_distribution(r):
		sns.set(style="white", palette="muted", color_codes=True)
		f, axes = plt.subplots(8, 3, figsize=(10, 90))
		sns.despine(left=True)

		subfile = open("subreddits.txt", 'r')
		x_i = 0
		y_i = 0

		index = 1
		color_function = sns.cubehelix_palette(24, start=.5, rot=-.75)

		for color, line in zip(color_function, subfile.read().split("\n")):
			print("Fetching subreddit %s (%d of 24)" % (line, index))
			sub = subredditmodel.SubredditModel(praw_object=r,
														subreddit=line)
			df = sub.get_df()
			ax = sns.distplot(df["Score"], ax=axes[y_i, x_i], 
												 hist=False,
												 label=line,
												 kde_kws={"shade": True},
												 color=color
												 )

			xmax = df["Score"].quantile(0.995)
			ax.set_xticks( Charts.generate_axes(0, xmax) )
			ax.set_xlim(0, xmax)
			ax.set_yticklabels(['{:1.2f}%'.format(x*100) for x in ax.get_yticks()])
			x_i = x_i + 1
			if x_i == 3:
				x_i = 0
				y_i = y_i + 1

			index = index + 1

		subfile.close()

		plt.tight_layout()
		plt.subplots_adjust(wspace=0.2, hspace=0.2)
		plt.show()


	#this one is for length graphs
	#takes a praw object
	def plot_distribution(r):
		sns.set(style="white", palette="muted", color_codes=True)
		f, axes = plt.subplots(8, 3, figsize=(10, 90), sharey=True)
		sns.despine(left=True)

		subfile = open("subreddits.txt", 'r')
		x_i = 0
		y_i = 0

		index = 1
		color_function = sns.cubehelix_palette(24)

		for color, line in zip(color_function, subfile.read().split("\n")):
			print("Fetching subreddit %s (%d of 24)" % (line, index))
			sub = subredditmodel.SubredditModel(praw_object=r,
														subreddit=line)
			df = sub.get_df()
			ax = sns.distplot(df["Length"], ax=axes[y_i, x_i], 
												 hist=True,
												 label=line,
												 kde_kws={"shade": True},
												 color=color
												 )

			xmax = df["Score"].quantile(0.95)
			ax.set_xticks( Charts.generate_axes(0, xmax) )
			ax.set_xlim(0, xmax)
			ax.set_yticklabels(['{:1.2f}%'.format(x*100) for x in ax.get_yticks()])
			
			x_i = x_i + 1
			if x_i == 3:
				x_i = 0
				y_i = y_i + 1

			index = index + 1

		plt.tight_layout()
		plt.subplots_adjust(wspace=0.2, hspace=0.2)
		plt.show()