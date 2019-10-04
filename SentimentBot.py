#!/usr/bin/env python3

import praw
import prawcore
import re
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

#access reddit
def log_in():
	reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='')
	return reddit

#get subreddit info
def get_sub_top(reddit,sub,num):
	subreddit = reddit.subreddit(str(sub))
	p = subreddit.hot(limit=int(num))
	return p

#make tokenize into lowercase and stopworded dictionary
def pre_processing(titles):

	sw = stopwords.words('english')
	sw.append('til') #shows up a lot
	sw.append('like') #too boring/common

	tokenizer = RegexpTokenizer(r'\w+')

	tokens = []
	for title in titles:
		title = re.sub(r'\d+','',title) #remove numbers
		toks = tokenizer.tokenize(title)
		toks = [t.lower() for t in toks if t.lower() not in sw]
		tokens.extend(toks)

	return tokens

#create a dataframe of each title and it's polarity score
def make_df(titles):
	sia = SIA()
	results = []
	for title in titles:
		polarity = sia.polarity_scores(title)
		polarity['headline'] = title
		results.append(polarity)

	df = pd.DataFrame(results)

	#threshold the polarity values into overall positive or negative
	df['label'] = 0
	df.loc[df['compound'] > 0.2, 'label'] = 1
	df.loc[df['compound'] < -0.2, 'label'] = -1
	
	return df

#create pie chart of mood by post
def mood_pie(df):
	counts = df.label.value_counts(normalize=True) * 100
	labels = 'Neutral','Positive','Negative'
	colors = 'Gray','Green','Red'
	plt.pie(counts,labels=labels,colors=colors,autopct='%1.1f%%')
	plt.show()

#make a frequency dictionary for either postive or negative words
def get_freq(df,polarity):
	titles = list(df[df.label == polarity].headline)
	tokens = pre_processing(titles)
	freq = nltk.FreqDist(tokens)
	return freq

#generate a wordcloud from a freqeuncy dictionary
def make_wordcloud(freq_dict,color):
	settings = WordCloud(scale=3,background_color=color,color_func=lambda *args, **kwargs: "White")
	wordcloud = settings.generate_from_frequencies(freq_dict)
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.show()
	return settings

####Where the magic happens####
def main():
	
	try:
		sub = input("Enter Subreddit name. For example: all, funny, news, politics: ")
		num = input("Enter maximum amount of posts (note that more posts mean a longer run time): ")
		posts = get_sub_top(log_in(),sub,num)

		titles = set()
		for post in posts:
			titles.add(post.title)
			
	except (prawcore.exceptions.NotFound, prawcore.exceptions.Redirect) as e:
		print("Subreddit could not be found, please enter a valid one.")
		main()
	except ValueError:
		print("Please enter an integer number of posts.")
		main()

	df = make_df(titles)

	mood_pie(df)

	pos_freq = get_freq(df,1)
	neg_freq = get_freq(df,-1)

	make_wordcloud(pos_freq,'Green').to_file('p.png')
	make_wordcloud(neg_freq,'Red').to_file('n.png')

main()