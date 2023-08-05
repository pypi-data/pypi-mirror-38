class QueryIterator(object):

    def __init__(self, github_session, arguments, results):
        self.github_session = github_session
        self.arguments = arguments
        self.pos = arguments.get('p')
        self.results = results

    def next(self):
        self.github_session.proxy = self.github_session.obtain_new_proxy()
        self.pos += 1
        args = self.arguments
        args['p'] = self.pos

        if args.get('type').lower() == 'repositories':
            self.results = self.github_session.search_handler(args)
