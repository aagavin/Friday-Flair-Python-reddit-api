#!/usr/bin/env python2.7
#
#
#
#############################
import reddit
from operator import itemgetter, attrgetter
#############################
topcomments=list()
#############################
r = reddit.Reddit(user_agent='aagavin_script')
r.login('aagavin', 'aaaaaa')
#submissions = r.get_subreddit('shittyaskscience').get_top(limit=5, url_data={'t': 'week'})
submissions = r.get_subreddit('shittyaskscience').get_top(limit=None, url_data={'t': 'week'})
#############################

print 'Top post of the week:\n[%s][%s](%s){%s comments} by [%s](http://www.reddit/u/%s)' % (submissions[0].ups-submissions[0].downs, submissions[0].title, submissions[0].url,submissions[0].num_comments, submissions[0].author, submissions[0].author)

for i in submissions:
	try:
		#d=datetime.timedelta(seconds=x.created_utc)
		#d=datetime.fromtimestamp(x.created)
		#print '[%s][%s](%s){%s comments} by [%s](http://www.reddit/u/%s)' % (i.ups-i.downs, i.title, i.url,i.num_comments, i.author, i.author)
		#for j in i.comments_flat:

		for j in i.comments_flat:
			try:
				j.ups
			except AttributeError:
				continue
			except UnicodeDecodeError:
				continue
			topcomments.insert(0,[j,j.ups-j.downs])
	except UnicodeDecodeError:
		continue
	except AttributeError:
		continue

topcomments=sorted(topcomments, key=itemgetter(1), reverse=True)


for j in topcomments:
	try:
		print '----\n[%s][%s](%s) by [%s](http://www.reddit.com/u/%s)\n----\n' % (j[0].ups-j[0].downs,j[0],j[0].permalink,j[0].author,j[0].author)
		#print j
	except UnicodeDecodeError:
		continue
	except AttributeError:
		continue		

r.logout()
