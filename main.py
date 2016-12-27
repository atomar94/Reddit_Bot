import praw
import configloader
import subredditmodel


import seaborn as sns
from charts import Charts as ch



if __name__ == "__main__":
	cfg = configloader.ConfigLoader("credentials.ini")

	r = praw.Reddit(client_id = cfg.client_id,
					client_secret = cfg.client_secret,
					user_agent = cfg.user_agent)



	ch.single_kdeplot(r)