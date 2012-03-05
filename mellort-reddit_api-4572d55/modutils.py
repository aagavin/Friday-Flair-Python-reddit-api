#!/usr/bin/env python2
import sys
from optparse import OptionGroup, OptionParser
from reddit import Reddit


class ModUtils(object):
    VERSION = '0.1.dev'

    def __init__(self, subreddit, site=None, verbose=None):
        self.reddit = Reddit(str(self), site)
        self.sub = self.reddit.get_subreddit(subreddit)
        self.verbose = verbose
        self._current_flair = None

    def __str__(self):
        return 'BBoe\'s ModUtils %s' % self.VERSION

    def current_flair(self):
        if self._current_flair is None:
            self._current_flair = []
            if self.verbose:
                print 'Fetching flair list for %s' % self.sub
            for flair in self.sub.flair_list():
                self._current_flair.append(flair)
                yield flair
        else:
            for item in self._current_flair:
                yield item

    def flair_template_sync(self, editable, limit,  # pylint: disable-msg=R0912
                            static, sort, use_css, use_text):
        # Parameter verification
        if not use_text and not use_css:
            raise Exception('At least one of use_text or use_css must be True')
        sorts = ('alpha', 'size')
        if sort not in sorts:
            raise Exception('Sort must be one of: %s' % ', '.join(sorts))

        # Build current flair list along with static values
        if static:
            counter = dict((x, limit) for x in static)
        else:
            counter = {}
        if self.verbose:
            sys.stdout.write('Retrieving current flair')
            sys.stdout.flush()
        for flair in self.current_flair():
            if self.verbose:
                sys.stdout.write('.')
                sys.stdout.flush()
            if use_text and use_css:
                key = (flair['flair_text'], flair['flair_css_class'])
            elif use_text:
                key = flair['flair_text']
            else:
                key = flair['flair_css_class']
            if key in counter:
                counter[key] += 1
            else:
                counter[key] = 1
        if self.verbose:
            print

        # Sort flair list items according to the specified sort
        if sort == 'alpha':
            items = sorted(counter.items())
        else:
            items = sorted(counter.items(), key=lambda x: x[1], reverse=True)

        # Clear current templates and store flair according to the sort
        if self.verbose:
            print 'Clearing current flair templates'
        self.sub.clear_flair_templates()
        for key, count in items:
            if not key or count < limit:
                continue
            if use_text and use_css:
                text, css = key
            elif use_text:
                text, css = key, ''
            else:
                text, css = '', key
            if self.verbose:
                print 'Adding template: text: "%s" css: "%s"' % (text, css)
            self.sub.add_flair_template(text, css, editable)

    def login(self, user, pswd):
        if self.verbose:
            print 'Logging in'
        self.reddit.login(user, pswd)
        if self.verbose:
            print 'Fetching moderator list for %s' % self.sub
        if str(self.sub).lower() not in [str(x).lower() for x in
                                         self.reddit.user.my_moderation()]:
            raise Exception('You do not moderate %s' % self.sub)

    def message(self, category, subject, msg_file):
        users = getattr(self.sub, 'get_%s' % category)()
        if not users:
            print 'There are no %s on %s.' % (category, str(self.sub))
            return

        if msg_file:
            try:
                msg = open(msg_file).read()
            except IOError, error:
                print str(error)
                return
        else:
            print 'Enter message:'
            msg = sys.stdin.read()

        print ('You are about to send the following '
               'message to the users %s:') % ', '.join([str(x) for x in users])
        print '---BEGIN MESSAGE---\n%s\n---END MESSAGE---' % msg
        if raw_input('Are you sure? yes/[no]: ').lower() not in ['y', 'yes']:
            print 'Message sending aborted.'
            return
        for user in users:
            user.compose_message(subject, msg)
            print 'Sent to: %s' % str(user)

    def output_current_flair(self):
        for flair in self.current_flair():
            print flair['user']
            print '  Text: %s\n   CSS: %s' % (flair['flair_text'],
                                              flair['flair_css_class'])

    def output_list(self, category):
        print '%s users:' % category
        for user in getattr(self.sub, 'get_%s' % category)():
            print '  %s' % user


def main():
    mod_choices = ('banned', 'contributors', 'moderators')
    mod_choices_dsp = ', '.join(['`%s`' % x for x in mod_choices])
    msg = {
        'css': 'Ignore the CSS field when synchronizing flair.',
        'edit': 'When adding flair templates, mark them as editable.',
        'file': 'The file containing contents for --message',
        'flair': 'List flair for the subreddit.',
        'limit': ('The minimum number of users that must have the specified '
                  'flair in order to add as a template. default: %default'),
        'list': ('List the users in one of the following categories: '
                 '%s. May be specified more than once.') % mod_choices_dsp,
        'msg': ('Send message to users of one of the following categories: '
                '%s. Message subject provided via --subject, content provided '
                'via --file or STDIN.') % mod_choices_dsp,
        'pswd': ('The password to use for login. Can only be used in '
                 'combination with "--user". See help for "--user".'),
        'site': 'The site to connect to defined in ~/.reddit_api.cfg.',
        'sort': ('The order to add flair templates. Available options are '
                 '`alpha` to add alphabetically, and `size` to first add '
                 'flair that is shared by the most number of users. '
                 'default: %default'),
        'subject': 'The subject of the message to send for --message.',
        'sync': 'Synchronize flair templates with current user flair.',
        'text': 'Ignore the text field when synchronizing flair.',
        'user': ('The user to login as. If not specified the user (if any) '
                 'from the site config will be used, otherwise you will be '
                 'prompted for a username.'),
        'v': 'Display output for each web request.',
        }

    usage = 'Usage: %prog [options] SUBREDDIT'
    parser = OptionParser(usage=usage, version='%%prog %s' % ModUtils.VERSION)
    parser.add_option('-l', '--list', action='append', help=msg['list'],
                      choices=mod_choices, metavar='CATEGORY', default=[])
    parser.add_option('-F', '--file', help=msg['file'])
    parser.add_option('-f', '--flair', action='store_true', help=msg['flair'])
    parser.add_option('-v', '--verbose', action='store_true', help=msg['v'])
    parser.add_option('-m', '--message', choices=mod_choices, help=msg['msg'])
    parser.add_option('', '--subject', help=msg['subject'])

    group = OptionGroup(parser, 'Site/Authentication options')
    group.add_option('-s', '--site', help=msg['site'])
    group.add_option('-u', '--user', help=msg['user'])
    group.add_option('-p', '--pswd', help=msg['pswd'])
    parser.add_option_group(group)

    group = OptionGroup(parser, 'Sync options')
    group.add_option('', '--sync', action='store_true', help=msg['sync'])
    group.add_option('', '--editable', action='store_true', help=msg['edit'])
    group.add_option('', '--ignore-css', action='store_false',
                     default=True, help=msg['css'])
    group.add_option('', '--ignore-text', action='store_false',
                     default=True, help=msg['text'])
    group.add_option('', '--limit', type='int', help=msg['limit'], default=2)
    group.add_option('', '--sort', action='store', choices=('alpha', 'size'),
                     default='alpha', help=msg['sort'])
    parser.add_option_group(group)

    options, args = parser.parse_args()
    if options.pswd and not options.user:
        parser.error('Must provide --user when providing --pswd.')
    if len(args) == 0:
        parser.error('Must provide subreddit name.')
    if options.message and not options.subject:
        parser.error('Must provide --subject when providing --message.')
    subreddit = args[0]

    modutils = ModUtils(subreddit, options.site, options.verbose)
    modutils.login(options.user, options.pswd)

    for category in options.list:
        modutils.output_list(category)
    if options.flair:
        modutils.output_current_flair()
    if options.sync:
        modutils.flair_template_sync(editable=options.editable,
                                     limit=options.limit,
                                     static=None, sort=options.sort,
                                     use_css=options.ignore_css,
                                     use_text=options.ignore_text)
    if options.message:
        modutils.message(options.message, options.subject, options.file)

if __name__ == '__main__':
    sys.exit(main())
