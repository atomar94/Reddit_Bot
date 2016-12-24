import praw
import configparser


def load_cfg():
	cfg = configparser.ConfigParser()
	cfg.read("credentials.ini")
	print(cfg["AUTH"])

if __name__ == "__main__":
	load_cfg()