import sys
import json
import re

from graph.GraphClasses import GitNodeUser, TwitterNodeUser, TwitterEdgeFollowing, GitTwitterEdge
from credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from tweepy import OAuthHandler, API, TweepError

re_twitter = re.compile(r'twitter\.com[\/\#\!]*\/(\w*).*')
class BFSCrawler():
    def __init__(self):
        self.auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        self.api = API(self.auth, wait_on_rate_limit=True)
        self.git_nodes = {}
        self.git_edges = []
        self.twitter_nodes = {}
        self.twitter_edges = []

    def get_twitter_screen_name(self, link):
        twitter = re_twitter.findall(link)
        if twitter:
            twitter = twitter[0]
            return twitter.lower()
        return None

    def crawl(self, input, output):
        with open(input) as f:
            data = json.load(f)
            if 'nodes' in data and 'edges' in data:
                self.git_nodes = data['nodes']
                self.git_edges = data['edges']

        # get all accounts
        for gitKey, node in self.git_nodes.items():
            if node['label'] in GitNodeUser.__LABEL__:
                twitter_screen_name = self.get_twitter_screen_name(node['properties']['blog'])
                if twitter_screen_name:
                    tUser = self.api.get_user(twitter_screen_name)
                    tUser = { 'screen_name': tUser.screen_name, 'id': str(tUser.id), 'picture': tUser.profile_image_url  }
                    self.twitter_nodes[tUser['id']] = TwitterNodeUser(tUser)
                    self.twitter_edges.append(GitTwitterEdge(source=gitKey, target=tUser['id']))

        # get all friendships
        # twitter_ids = [k for k in self.twitter_nodes.items()]
        # following_common = {}
        # for follower_id in twitter_ids:
        #     following = self.api.friends_ids(follower_id)
        #     print(follower_id in self.twitter_nodes)
        #     self.twitter_nodes[follower_id].properties['following'] = following
        #     for followed_id in following:
        #         following_common[str(followed_id)] = (following_common[str(followed_id)] or 0) + 1
        #
        # # get all common friends
        # following_common = [id for id, cnt in following_common.items() if cnt > 1]
        # for follower_id in twitter_ids:
        #     for followed_id in self.twitter_nodes[follower_id].properties['following']:
        #         if followed_id in following_common:
        #             self.twitter_edges.append(TwitterEdgeFollowing(source=follower_id, target=followed_id))

        # write results
        with open(output, 'w') as file:
            writeNodes = { k: dict(i) for k, i in self.twitter_nodes.items() }
            writeNodes = { **writeNodes, **self.git_nodes }

            writeEdges = [dict(i) for i in self.twitter_edges]

            writeEdges += self.git_edges
            file.write(json.dumps({
                'nodes': writeNodes,
                'edges': writeEdges
            }))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Correct use:")
        print("GIT_USER=<git_user> GIT_TOKEN=<git_token> python bfs_crawler.py <input_file> <output_file>")
        sys.exit(0)

    crawler = BFSCrawler()
    crawler.crawl(sys.argv[1], sys.argv[2])
