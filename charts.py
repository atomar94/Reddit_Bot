import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import subredditmodel

#Helper class for plotting
#Is static class so dont need to instantiate anything.
class Charts:

	#takes praw obj
	def single_kdeplot(r):
		sns.set(style="white", palette="muted", color_codes=True)
		sns.despine(left=True)

		subfile = open("subreddits.txt", 'r')
		x_i = 0
		y_i = 0

		color_function = sns.color_palette("Set2", 24)

		dfs = []

		for index, line in enumerate(subfile.read().split("\n")):
			print("Loading  /r/%s (%d of 24)" % (line, index))
			sub = subredditmodel.SubredditModel(praw_object=r,
												subreddit=line)
			dfs.append(sub.get_df())

		subfile.close()
		df = pd.concat(dfs)


		#really messy :/
		#TODO: Move this code to the subredditmodel filtering code
#		filtered_length = []
#		for index, row in df.iterrows():
#			if np.isnan(row['Filtered_Score']):
#				filtered_length.append(np.nan)
#			else:
#				filtered_length.append(row['Length'])
#		df['Filtered_Length'] = filtered_length
#
		xmax = df['Filtered_Length'].dropna().quantile(0.85)
		ymax = df['Filtered_Score'].dropna().quantile(0.90)
		xmin = -5 #give some space in the graph
		ymin = min(-10, int(-1*ymax*0.3)) #show upvotes to at least -10


		bi_colors = ["#ff0080", "#a349a4", "#0000ff"]
		bi_palette = sns.color_palette(palette=bi_colors)


		print("Plotting...")
		ax = sns.kdeplot(df['Filtered_Length'].dropna(), 
						 df['Filtered_Score'].dropna(),  
							kind="hex",
							shade=True,
							color="#a349a4",
							gridsize=1000
							#xlim=(0, xmax), 
							#ylim=(0, ymax)
							) 

		ax.set_title("All Comments")
		#ax.set_xticks( Charts.generate_axes(0, xmax) )
		ax.set_xlim(xmin, xmax)
		ax.set_ylim(ymin, ymax)
		#ax.set_yticklabels(['{:1.2f}%'.format(x*100) for x in ax.get_yticks()])

		plt.tight_layout(pad=0.7)
		#plt.margins(0.5)
		#plt.subplots_adjust(wspace=0.2, hspace=0.8)
		plt.show()



	#takes praw obj
	def kdeplot(r):
		sns.set(style="white", palette="muted", color_codes=True)
		f, axes = plt.subplots(8, 3, figsize=(10, 20))
		sns.despine(left=True)

		subfile = open("subreddits.txt", 'r')
		x_i = 0
		y_i = 0

		index = 1
		color_function = sns.color_palette("Set2", 24)

		for color, line in zip(color_function, subfile.read().split("\n")):
			print("Loading  /r/%s (%d of 24)" % (line, index))
			sub = subredditmodel.SubredditModel(praw_object=r,
												subreddit=line)
			df = sub.get_df()

			xmax = df['Length'].quantile(0.85)
			ymax = df['Score'].quantile(0.90)
			xmin = -5 #give some space in the graph
			ymin = min(-10, int(-1*ymax*0.3)) #show upvotes to at least -10

			print("Plotting...")
			ax = sns.kdeplot(df['Length'], df['Score'], 
											ax=axes[y_i, x_i], 
											kind="hex",
											shade=True,
											color=color,
											gridsize=400
											#xlim=(0, xmax), 
											#ylim=(0, ymax)
											) 

			ax.set_title(sub.subreddit)
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

		plt.tight_layout(pad=0.7)
		#plt.margins(0.5)
		plt.subplots_adjust(wspace=0.2, hspace=0.8)
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