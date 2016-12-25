import praw
import configloader
import subredditmodel
import numpy as np

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



	ch.plot_distribution(r)