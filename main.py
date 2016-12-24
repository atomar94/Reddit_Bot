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

	askreddit_model = subredditmodel.SubredditModel(praw_object=r, 
													subreddit="askreddit")
	
	df = askreddit_model.get_df()
	sns.jointplot(df.score, df.length, kind="reg", color="#4CB391", xlim=(0, 500), ylim=(0, 1000))

	plt.show()