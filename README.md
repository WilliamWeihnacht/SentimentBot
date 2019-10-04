# SentimentBot
Set up:

1) install praw with 'pip3 install praw'
2) install nltk with 'pip3 install nltk'
3) repalce client secret and cliend id by registering a bot at https://www.reddit.com/prefs/apps/.
More information can be found at https://praw.readthedocs.io/en/latest/getting_started/quick_start.html.

Output:

Running this script will prompt you for a subreddit and post limit. Upon entering these you will get a pie chart of how many hot posts on the desired subreddit are positive, negative, or neutral. Afterwards two wordclouds will be displayed, one positive, one negative, showing the most popular words in their respective categories.
