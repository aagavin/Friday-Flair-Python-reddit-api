

import reddit


r=reddit.Reddit(user_agent='aagavin_script')

class tst:
	def __init__(self,username, password, thesubreddityouwant):
		self.r=reddit.Reddit(user_agent='test_aagavin')
		self.sub=self.r.get_subreddit(thesubreddityouwant)
	
	def printnew(self):
		post=(self.sub).get_top(limit=1).next()
		print post.title


s=raw_input("Enter your subreddit: r/")
t=tst("","",s)
t.printnew()
