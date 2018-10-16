import sys
import json
import time

from GitHubAPI import GitHubUser
from graph.GraphClasses import GitNodeRepo, GitNodeUser, GitEdgeOwn, GitEdgeContrib
from collections import deque

# foutoucour

class BFSUserRepoContributors():
    def __init__(self, seeds):
        self.users = [(GitHubUser(username), 0) for username in seeds]
        self.queue = deque(self.users)
        self.nodes = {}
        self.edges = []
        self.users = []

    def perform_crawl(self, output, maxDepth):
        '''
            Crawl the collaboration network usining breath first search (BFS) by walking through:
                users => his/her repos => repos contributors
            which represent one depth level of BFS
        '''

        while len(self.queue) > 0:
            # dequeue de first user
            user, curDepth = self.queue.popleft()
            if user.username in self.users:
                continue
            print("Crawling {user}, Repos: {nun_repos}, Queue size: {queue_size}".format(
                user=user,
                nun_repos=len(user.repos),
                queue_size=len(self.queue)
            ))

            # ensure that user will not be collected again
            self.nodes[user.info['node_id']] = GitNodeUser(user.info)
            self.users.append(user.username)

            # for each repo of the current user
            for repo in user.repos:
                print("Crawling {repo}, Contributors: {num_contributors}".format(
                    repo=repo,
                    num_contributors=len(repo.contributors)
                ))
                self.nodes[repo.info['node_id']] = GitNodeRepo(repo.info)
                self.edges.append(GitEdgeOwn(source=user.info['node_id'], target=repo.info['node_id']))

                # write edge between all collaborators
                for cont in repo.contributors:
                    self.nodes[cont.info['node_id']] = GitNodeUser(cont.info)
                    self.edges.append(GitEdgeContrib(source=repo.info['node_id'], target=cont.info['node_id']))

                # verify if will keep walking
                if curDepth + 1 < maxDepth:
                    for nextUser in repo.contributors:
                        if nextUser.username not in self.users:
                            self.queue.append((nextUser, curDepth+1))

            with open(output,"w") as file:
                file.write(json.dumps({
                    'nodes': { k: dict(i) for k, i in self.nodes.items() },
                    'edges': [ dict(i) for i in self.edges ]
                }))
            time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) < 3 or not int(sys.argv[2]):
        print("Correct use:")
        print("GIT_USER=<git_user> GIT_TOKEN=<git_token> python crawler/bfs_user_repo_contributors.py <output_file> <depth>")
        sys.exit(0)

    seeds = ['tweepy']
    crawler = BFSUserRepoContributors(seeds)
    crawler.perform_crawl(sys.argv[1], int(sys.argv[2]))
