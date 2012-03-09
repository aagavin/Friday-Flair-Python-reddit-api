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
    topPost = self.r.get_subreddit(self.thesub).get_top(limit=1, url_data={'t': 'week'})
    for i in topPost:
      if i.author_flair_text==None:
        self.r.get_subreddit(self.thesub).set_flair(i.author, 'I have no flair', '1')
      else:
        self.r.get_subreddit(self.thesub).set_flair(i.author, i.author_flair_text, '1')
      self.post='Top post of the week(gold flair):\n\n---\n\n[%s][%s](%s){[%s comments](%s)} by [%s[%s]](http://www.reddit/u/%s)\n\n\n\n' % (i.ups-i.downs, i.title, i.url,i.num_comments,i.permalink, i.author,i.author_flair_text, i.author)
      self.post=self.post+'\n\n\n\nTop Comment of the week(silver flair):\n\n---\n\n[%s][%s](%s) by [%s](http://www.reddit.com/u/%s)\n' % (i.comments_flat[0].ups-i.comments_flat[0].downs,i.comments_flat[0],i.comments_flat[0].permalink,i.comments_flat[0].author,i.comments_flat[0].author)
      if i.comments_flat[0].author_flair_text==None:
        self.r.get_subreddit(self.thesub).set_flair(i.comments_flat[0].author, 'I have no flair', '2')
      else:
        self.r.get_subreddit(self.thesub).set_flair(i.comments_flat[0].author, i.author_flair_text, '2')


  # The name should explain it self
  def getTopComments(self):
    submissions = self.r.get_subreddit(self.thesub).get_top(limit=None, url_data={'t': 'week'})
    for i in submissions:
      for j in i.all_comments_flat:
        try:
          if (datetime.now() - datetime.fromtimestamp(j.created)).days < 7 and j.ups>15:
            #print '[%s]%s' %(j.ups-j.downs, j)
            self.topcomments.insert(0,[j,j.ups-j.downs])
          #dtime = datetime.fromtimestamp(j.created)
        except AttributeError:
          continue
    self.topcomments=sorted(self.topcomments, key=itemgetter(1), reverse=True)
    self.post=self.post+'\n\n\n\nTop Comments of the week:\n\n---\n\n'
    for j in self.topcomments[0:10]:
      self.post=self.post+'\n[%s][%s](%s) by [%s](http://www.reddit.com/u/%s)\n' % (j[0].ups-j[0].downs,j[0],j[0].permalink,j[0].author,j[0].author)


  #This will post it to the subreddit
  def postToSub(self):
    self.r.submit(self.thesub, '[Announcement] Friday Flair Awards', text=self.post)
    self.r.logout()

u=raw_input("Enter your username: ")
p=getpass.getpass("Enter your password: ")
s=raw_input("Enter your subreddit: ")
friday=FridayFlair(u,p,s)
friday.getTopPost()
friday.getTopComments()
friday.postToSub()
