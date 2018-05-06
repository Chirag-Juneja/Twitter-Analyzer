import tweepy
import time
import csv
from textblob import TextBlob 


consumer_key = ''
consumer_secret = ''

access_token = ''
access_token_secret = ''

def analyze_user(screen_name):

	auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	tweets = []
	user=api.get_user(screen_name)
	total_tweets=user.statuses_count
	
	if total_tweets<200:
		update = api.user_timeline(screen_name,count=total_tweets)
		tweets.extend(update)
	
	else:
		update = api.user_timeline(screen_name,count=200)
		tweets.extend(update)
		last_tweet_id =update[-1].id
		
		for i in range(0,int(total_tweets/200)):
			update = api.user_timeline(screen_name,count=200,max_id=last_tweet_id)
			tweets.extend(update)
			last_tweet_id =update[-1].id
			time.sleep(10)
		
		update = api.user_timeline(screen_name,count=int(total_tweets)%200)
		tweets.extend(update)

	with open('%s_tweets.csv'%screen_name,'w') as csvfile:
		csvWriter=csv.writer(csvfile,dialect='excel')
		csvWriter.writerow( ['id','tweet','polarity','subjectivity'])
		for i in range(0,len(tweets)):
			analysis = TextBlob(tweets[i].text)
			csvWriter.writerow( [tweets[i].id,tweets[i].text.encode('utf-8'),analysis.sentiment.polarity,analysis.sentiment.subjectivity])
	return

def get_followers(screen_name):

	auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	user=api.get_user(screen_name)
	follower_id = []
	followers = []
	
	for page in tweepy.Cursor(api.followers_ids,screen_name).pages():
		follower_id.extend(page)
		time.sleep(10)

	with open('%s_followers.csv'%screen_name,'w') as csvfile:
		csvWriter=csv.writer(csvfile,dialect='excel')
		csvWriter.writerow( ['id','name','description','followers_count','location'])
		for i in range(len(follower_id)) :
			followers.append(api.get_user(follower_id[i]))
			csvWriter.writerow( [follower_id[i],followers[i].name,followers[i].description,followers[i].followers_count,followers[i].location])
	return

def analyze_topic(topic,total_tweets):
	auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	tweet = []

	with open('%s_analysis.csv'%topic,'w') as csvfile:
		csvWriter=csv.writer(csvfile,dialect='excel')
		csvWriter.writerow( ['tweet','polarity','subjectivity'])
		for tweet in tweepy.Cursor(api.search,q=topic,count=100,lang="en",tweet_mode='extended').items(total_tweets):
			analysis = TextBlob(tweet.full_text)
			csvWriter.writerow([tweet.full_text.encode('utf-8'),analysis.polarity,analysis.subjectivity])
			time.sleep(10)
	return


if __name__ == '__main__':

	analyze_user('elonmusk')
	get_followers('elonmusk')
	analyze_topic('modi',100)
