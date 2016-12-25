import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import subredditmodel

#Helper class for plotting
#Is static class so dont need to instantiate anything.
class Charts:

	def kdeplot(data1, data2, xmin=-50, xmax=100, ymin=0, ymax=700):
		kde = sns.kdeplot(data1, data2, shade=True)
		axes = kde.axes
		axes.set_xlim(xmin, xmax) #set the x range
		axes.set_ylim(ymin, ymax)
		return kde


	def jointplot(data1, data2):
		jp = sns.jointplot(data1, data2, kind="hex", 
										 color="#4CB391", 
										 xlim=(0, 500), 
										 ylim=(0, 1000)
										 )
		return jp


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
		models = []
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
			hsf = df['Score'].size #Histogram Scaling Factor (because it is set to unity)
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
		models = []
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