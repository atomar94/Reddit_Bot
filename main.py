import praw
import configloader
import subredditmodel
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":
	cfg = configloader.ConfigLoader("credentials.ini")

	r = praw.Reddit(client_id = cfg.client_id,
					client_secret = cfg.client_secret,
					user_agent = cfg.user_agent)

	askreddit_model = subredditmodel.SubredditModel(praw_object=r, 
													subreddit="askreddit")
	
	sns.kdeplot(askreddit_model.get_df().score)
	plt.show()