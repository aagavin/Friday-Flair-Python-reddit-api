#!/usr/bin/env python
#
'''
The shitty ask science friday flair award script

This script will get the top post in a subreddit and give it
a gold flair(css class '1')

It will also get the top 10 comments in the week

Then it posts it to the subreddit... yea
'''

'''
Special thanks to bboe for the python wrapper and the whole team at r/redditdev
without there help this wouldn't be possible :)
'''
import reddit
import getpass
from datetime import datetime
from operator import itemgetter, attrgetter

'''
yea kinda messyish right now
'''
#class FridayFlair=boss
class FridayFlair:
  '''yea let declair some variables '''
  def __init__(self,username, password, thesubreddityouwant): 
    self.thesub       = thesubreddityouwant
    self.topcomments  =list()
    self.r            =reddit.Reddit(user_agent='aagavin_script')
    self.r.login(username,password)
    self.post=''


  #This will get the top post of the week post it and give will gold flair
  #it will also get the top comment in the top post and give it silver flair!
  def getTopPost(self):
		#gets the top post of the week in the givin subreddit
    topPost = self.r.get_subreddit(self.thesub).get_top(limit=1, url_data={'t': 'week'})
    topPost = topPost.next()
    
    
    #Checks to see if the author of the post has flair
    #if not it gives the author a flair of "I have no flair"
    if topPost.author_flair_text==None:
			try:
				self.r.get_subreddit(self.thesub).set_flair(topPost.author, 'I have no flair', '1')
			except:
				print "There was an error(are you sure your mod?), continuing..."
    else:
			try:
				self.r.get_subreddit(self.thesub).set_flair(topPost.author, topPost.author_flair_text, '1')
			except:
				print "There was an error(are you sure your mod?), continuing..."
    
    #Checks to see if the author of the top comment has flair
    #if not it gives the author a flair of "I have no flair"
    if topPost.comments_flat[0].author_flair_text==None:
			try:
				self.r.get_subreddit(self.thesub).set_flair(topPost.comments_flat[0].author, 'I have no flair', '2')
			except:
				print "again you don't have mod access to this subreddit, thats cool no problem I'll just not set flair"
    else:
			try:
				self.r.get_subreddit(self.thesub).set_flair(topPost.comments_flat[0].author, topPost.author_flair_text, '2')
			except:
				print "again you don't have mod access to this subreddit, thats cool no problem I'll just not set flair"
    
    #adds the top post and top coment
    #to var post that is later posted out
    self.post='Top post of the week(gold flair):\n\n---\n\n[%s][%s](%s){[%s comments](%s)} by [%s[%s]](http://www.reddit/u/%s)\n\n\n\n' % (topPost.ups-topPost.downs, topPost.title, topPost.url,topPost.num_comments,topPost.permalink, topPost.author,topPost.author_flair_text, topPost.author)
    self.post=self.post+'\n\n\n\nTop Comment of the week(silver flair):\n\n---\n\n[%s][%s](%s) by [%s](http://www.reddit.com/u/%s)\n' % (topPost.comments_flat[0].ups-topPost.comments_flat[0].downs,topPost.comments_flat[0],topPost.comments_flat[0].permalink,topPost.comments_flat[0].author,topPost.comments_flat[0].author)
    


  # The name should explain it self
  def getTopComments(self):
		#gets all the comments form the top posts of the week
		#and sorts them by votes(upvotes-downvotes)
    submissions = self.r.get_subreddit(self.thesub).get_top(limit=100, url_data={'t': 'week'})
    print 'sorting comments(This could take some time) ...',
    for i in submissions:
			print '.',
			for j in i.all_comments_flat:
				if (datetime.now() - datetime.fromtimestamp(j.created)).days < 7 and j.ups>15:
					self.topcomments.insert(0,[j,j.ups-j.downs])
    #The magic of python will now sort the comments
    self.topcomments=sorted(self.topcomments, key=itemgetter(1), reverse=True)
    self.post=self.post+'\n\n\n\nTop Comments of the week:\n\n---\n\n'
    top10=self.topcomments[0:10]
    for j in top10:
			#self.post=self.post+'[%d][%s](%s) by [%s](http://www.reddit.com/u/%s)\n' % (j[0].ups-j[0].downs,j[0],j[0].permalink,j[0].author,j[0].author)
			self.post=self.post+'['u'%s''](%s) by [%s](http://www.reddit.com/u/%s)\n' % (j[0],j[0].permalink,j[0].author,j[0].author)
			
			
			
  #This will post it to the subreddit
  def postToSub(self):
		print 'done'
		ans=raw_input("OK. Done do you want to post to r/%s?: ")
		if ans=='yes' or ans=='y' or ans=='YES':
			self.r.submit(self.thesub, '[Announcement] Friday Flair Awards', text=self.post)
		else:
			print "Ok cool I'll show it here than"
			print self.post
		self.r.logout()

u=raw_input("Enter your username: ")
p=getpass.getpass("Enter your password: ")
s=raw_input("Enter your subreddit: r/")
friday=FridayFlair(u,p,s)
#friday.getTopPost()
friday.getTopComments()
friday.postToSub()
