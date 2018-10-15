class Node():
    __LABEL__ = 'NODE'

    def __init__(self, properties):
        self.label = self.__class__.__LABEL__
        self.properties = properties

    def __iter__(self):
        yield 'label', getattr(self, 'label')
        yield 'properties', getattr(self, 'properties')

class Edge():
    __TYPE__ = 'EDGE'

    def __init__(self, source, target):
        self.type = self.__class__.__TYPE__
        self.source = source
        self.target = target

    def __iter__(self):
        yield 'type', getattr(self, 'type')
        yield 'source', getattr(self, 'source')
        yield 'target', getattr(self, 'target')

# Git Graph
class GitNodeUser(Node):
    __LABEL__ = 'git.user'

class GitNodeRepo(Node):
    __LABEL__ = 'git.repo'

class GitEdgeOwn(Edge):
    __TYPE__ = 'git.user:own:git.repo'

class GitEdgeContrib(Edge):
    __TYPE__ = 'git.user:contributes:git.repo'

# Twitter
class TwitterNodeUser(Node):
    __LABEL__ = 'twitter.user'

class TwitterEdgeFollowing(Edge):
    __TYPE__ = 'twitter.user:following:twitter.user'

# from git to twitter
class GitTwitterEdge(Edge):
    __TYPE__ = 'git.user:same_as:twitter.user'
