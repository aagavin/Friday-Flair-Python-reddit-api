#!/usr/bin/env python2.7
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


#class FridayFlair
class FridayFlair:
  '''yea let declair some variables '''
  def __init__(self,username, password, thesubreddityouwant):
  	self.r=reddit.Reddit(user_agent='aagavin_script')
  	self.thesub=self.r.get_subreddit(thesubreddityouwant)
  	#self.thesub=thesubreddityouwant
  	self.topcomments=list()
  	self.r.login(username,password)
  	self.topweekpost=''
  	self.topweekcomment=''
  	self.comments=''


  #This will get the top post of the week post it and give will gold flair
  #it will also get the top comment in the top post and give it silver flair!
  def getTopPost(self):
  	#removes current gold and silver flair
  	item =self.thesub.flair_list()
  	for i in item:
  		if i['flair_css_class']=="1" or i['flair_css_class']=="2":
  			(self.thesub).set_flair(i['user'], i['flair_text'], None)
  	
  	
  	#gets the top post of the week in the givin subreddit
  	topPost = self.thesub.get_top(limit=1, url_data={'t': 'week'})
  	topPost = topPost.next()
  	
  	
  	#Checks to see if the author of the post has flair
  	#if not it gives the author a flair of "I have no flair"
  	if topPost.author_flair_text==None:
  		try:
  			self.r.get_subreddit(self.thesub).set_flair(topPost.author, 'I have no flair', '1')
  			#self.r.compose_message(topPost.author, 'Your a winner', 'You won the [r/shittyaskscience](http://www.reddit.com/r/shittyaskscience) flair award!')
  		except:
  			print "There was an error(are you sure your mod?), continuing..."
  	else:
  		try:
  			self.r.get_subreddit(self.thesub).set_flair(topPost.author, topPost.author_flair_text, '1')
  			#self.r.compose_message(topPost.author, 'Your a winner', 'You won the [r/shittyaskscience](http://www.reddit.com/r/shittyaskscience) flair award!')
  		except:
  			print "There was an error(are you sure your mod?), continuing..."
  	
  	#Checks to see if the author of the top comment has flair
  	#if not it gives the author a flair of "I have no flair"
  	if topPost.comments_flat[0].author_flair_text==None:
  		try:
  			self.r.get_subreddit(self.thesub).set_flair(topPost.comments_flat[0].author, 'I have no flair', '2')
  			#self.r.compose_message(topPost.comments_flat[0].author, 'Your a winner', 'You won the [r/shittyaskscience](http://www.reddit.com/r/shittyaskscience) flair award!')
		except:
			print "again you don't have mod access to this subreddit, thats cool no problem I'll just not set flair"
	else:
		try:
			self.r.get_subreddit(self.thesub).set_flair(topPost.comments_flat[0].author, topPost.author_flair_text, '2')
			#self.r.compose_message(topPost.comments_flat[0].author, 'Your a winner', 'You won the [r/shittyaskscience](http://www.reddit.com/r/shittyaskscience) flair award!')
		except:
			print "again you don't have mod access to this subreddit, thats cool no problem I'll just not set flair"
    
	#adds the top post and top coment
	#to a var that is later posted out
	self.topweekpost='* [%s](%s) by %s, [%s points]' % (topPost.title,topPost.permalink,topPost.author,topPost.ups-topPost.downs)    
	self.topweekcomment='* [%s](%s) by %s, [%s points]' % (topPost.comments_flat[0],topPost.comments_flat[0].permalink,topPost.comments_flat[0].author,topPost.comments_flat[0].ups-topPost.comments_flat[0].downs)


  # The name should explain it self
  def getTopComments(self):
  	#gets all the comments form the top posts of the week
  	#and sorts them by votes(upvotes-downvotes)
  	submissions =self.thesub.get_top(limit=45, url_data={'t': 'week'})
  	print 'sorting comments(This could take some time) . . .',
  	for i in submissions:
  		print '.',
  		for j in i.all_comments_flat:
  			if (datetime.now() - datetime.fromtimestamp(j.created)).days < 7 and j.ups>15:
				self.topcomments.insert(0,[j,j.ups-j.downs])

	#The magic of python will now sort the comments
	self.topcomments=sorted(self.topcomments, key=itemgetter(1), reverse=True)
	top10=self.topcomments[0:10]
	for j in top10:
		self.comments+='1. [%s](%s) by %s, [%s points]\n\n' % (str(j[0]),j[0].permalink,j[0].author,j[0].ups-j[0].downs)


      
  #This will post it to the subreddit that was entered
  def postToSub(self):
  	print 'done'
  	ans=raw_input("OK. Done do you want to post to r/"+self.thesub+"?: ")
  	body='intro para stuff'
  	body+='\n\n---\n\n'
  	body+='**Top Post of the week(gold flair):**\n\n'
  	body+=self.topweekpost+'\n\n'
  	body+='**Top comment in the top post(silver flair):**\n\n'
  	body+=self.topweekcomment+'\n\n'
  	body+='**Most voted on comment in last weeks thread(gold flair):**\n\n'
  	body+='* Insert some stuff here\n\n'
  	body+='**Top ten comments**\n\n'
  	body+=self.comments
  	if ans=='yes' or ans=='y' or ans=='YES' or ans=='Y':
  		#self.r.submit(self.thesub, '[Announcement] Friday Flair Awards', text=body)
  		self.r.submit('SaSModRoom', '(testing)[Announcement] Friday Flair Awards', text=body)
	else:
		print "Ok cool I'll show it here than"
		print body
	self.r.logout()

u=raw_input("Enter your username: ")
p=getpass.getpass("Enter your password: ")
s=raw_input("Enter your subreddit: r/")
friday=FridayFlair(u,p,s)
friday.getTopPost()
friday.getTopComments()
friday.postToSub()
