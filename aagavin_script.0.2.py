#!/usr/bin/env python2.7
#
import reddit
import getpass
from operator import itemgetter, attrgetter



class FridayFlair:
	def __init__(self,username, password, thesubreddityouwant): 
		self.user 				= username
		self.passwd 			= password
		self.thesub 			= thesubreddityouwant
		self.topcomments	=list()
		self.r 						= reddit.Reddit(user_agent='aagavin_script')
		self.r.login(self.user,self.passwd)

	def getTopPost(self):
		self.submissions = self.r.get_subreddit(self.thesub).get_top(limit=1, url_data={'t': 'week'})
		for i in self.submissions:
			return 'Top post of the week:\n[%s][%s](%s){%s comments} by [%s[%s]](http://www.reddit/u/%s)' % (i.ups-i.downs, i.title, i.url,i.num_comments, i.author,i.author_flair_text, i.author)

	def getTopComments(self):
		self.submissions = self.r.get_subreddit(self.thesub).get_top(limit=None, url_data={'t': 'week'})
		for i in self.submissions:
			for j in i.comments_flat:
				print j
				

u=raw_input("Enter your username: ")
p=getpass.getpass("Enter your password: ")
s=raw_input("Enter your subreddit: ")
friday=FridayFlair(u,p,s)
print friday.getTopPost()

	
	
		
