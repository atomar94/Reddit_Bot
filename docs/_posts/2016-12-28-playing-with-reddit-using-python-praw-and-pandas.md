---
layout: post
title: Playing with Reddit Using Python, PRAW, and Pandas
---

This is part 1 of a 3 part series about using Python to gather comments from Reddit and analyze them using Seaborn, Pandas, and Matplotlib.

In this part I am going to give an overview of using [PRAW](https://praw.readthedocs.io/en/latest/), a Python Reddit API Wrapper, to collect Reddit comments and load it into a Pandas Dataframe.

# Setup and Installation

## Python & Dependencies

For this project I am using Anaconda Python 3.5 interpreter, which you can download [here.](https://www.continuum.io/downloads) A few of the other libraries, such as Pandas and Numpy, come preinstalled with Anaconda and I highly recommend it.

To grab Reddit comments I am using PRAW, which I linked above. To download the PRAW package for Anaconda open the Anaconda Prompt and run

<pre>
  <code class="shell">
    pip install PRAW
  </code>
</pre>

## Registering Your Reddit Bot

In order to use PRAW, or any other Reddit API, we first need to register our bot through Reddit. You must have a Reddit account in order to create a bot.

1. Go to the Reddit Application Preferences page [here.](https://ssl.reddit.com/prefs/apps)

2. Create a new Application of type "Web App" and in the Description field put a small description of what your bot does.
..* The About URL field can be left blank. The Redirect URL field put "http://example.com/redirect".

![Reddit Bot Config]({{ site.baseurl }}/images/reddit-bot-fields.png)

# Connecting to Reddit With PRAW

To connect PRAW to Reddit we need to supply our client ID, client secret, and user agent.

<pre>
  <code class="python">
  r = praw.Reddit(client_id = cfg.client_id,
      client_secret = cfg.client_secret,
      user_agent = cfg.user_agent)
  </code>
</pre>

This returns a Reddit object *r* that we can use to collect all kinds of Reddit data. Let's start by getting the top 25 submissions in /r/AskReddit

<pre>
  <code class="python">
    comments = []
    for submission in r.subreddit("askreddit").hot(limit=25):
      submission.comments.replace_more(limit=32)
      comments.append(submission.comments.list())
  </code>
</pre>
