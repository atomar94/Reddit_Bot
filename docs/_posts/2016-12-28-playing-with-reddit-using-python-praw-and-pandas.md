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

1) Go to the Reddit Application Preferences page [here.](https://ssl.reddit.com/prefs/apps)

2) Create a new Application of type "Web App" and in the Description field put a small description of what your bot does. For mine I simply put "Scraping Reddit comments to play with some data." The About URL field can be left blank, and in the Redirect URL field put "http://example.com/redirect".

![Reddit Bot Config]({{ site.baseurl }}/images/reddit-bot-fields.png)



Next you can update your site name, avatar and other options using the _config.yml file in the root of your repository (shown below).

![_config.yml]({{ site.baseurl }}/images/config.png)
