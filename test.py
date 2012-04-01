
#import cPickle
import reddit
#import getpass

'''inFridge = ["ketchup", "mustard", "relish"]
print inFridge


FILE = open("flair.txt", 'w')

cPickle.dump(inFridge, FILE)

FILE.close()

FILE=open("fridge.txt",'r')
fridge=cPickle.load(FILE)
print fridge'''

print ".",

r = reddit.Reddit(user_agent='example')
r.login('aagavin', 'gavin123A')

print ".",
item = r.get_subreddit('shittyaskscience').flair_list()
print ".",
for i in item:
	print ".",
	r.get_subreddit('shittyaskscience').set_flair(i['user'])
	#flist.insert(0,[i['user'],i['flair_text'],i['flair_css_class']])
	print ".",


'''flist=list()

item = r.get_subreddit('shittyaskscience').flair_list()
for i in item:
	flist.insert(0,[i['user'],i['flair_text'],i['flair_css_class']])
	print ".",




FILE=open("flair.txt",'w')
cPickle.dump(flist,FILE)
FILE.close()
'''


'''FILE=open("flair.txt",'r')
dlist=cPickle.load(FILE)

for i in dlist:
	print "%s[%s],class=%s" % (i[0],i[1],i[2])'''
