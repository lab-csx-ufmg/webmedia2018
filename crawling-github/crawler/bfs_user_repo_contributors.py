import sys
from GitHubAPI import GitHubUser
from collections import deque

class BFSUserRepoContributors():
    def __init__(self, seeds):
        self.users = [(GitHubUser(username), 0) for username in seeds]
        self.queue = deque(self.users)
        self.users_crawled = set()

    def write_edges(self, file, repo):
        if(len(repo.contributors) <= 1):
            return
        for idx, c1 in enumerate(repo.contributors):
            for c2 in repo.contributors[idx+1:]:
                file.write("{c1}, {c2}, {repo}\n".format(
                    c1=c1.username,
                    c2=c2.username,
                    repo=repo.info['full_name']
                ))

    def perform_crawl(self, output, maxDepth):
        '''
            Crawl the collaboration network usining breath first search (BFS) by walking through:
                users => his/her repos => repos contributors
            which represent one depth level of BFS
        '''

        with open(output,"w") as file:
            while len(self.queue) > 0:
                # dequeue de first user
                user, curDepth = self.queue.popleft()
                print("Crawling {user}, Repos: {nun_repos}, Queue size: {queue_size}".format(
                    user=user,
                    nun_repos=len(user.repos),
                    queue_size=len(self.queue)
                ))

                # ensure that user will not be collected again
                self.users_crawled.add(user.username)

                # for each repo of the current user
                for repo in user.repos:
                    print("Crawling {repo}, Contributors: {num_contributors}".format(
                        repo=repo,
                        num_contributors=len(repo.contributors)
                    ))

                    # write edge between all collaborators
                    self.write_edges(file, repo)

                    # verify if will keep walking
                    if curDepth + 1 < maxDepth:
                        for nextUser in repo.contributors:
                            if nextUser not in self.users_crawled:
                                self.queue.append(nextUser)

if __name__ == "__main__":
    if len(sys.argv) < 3 or not int(sys.argv[2]):
        print("Correct use:")
        print("GIT_USER=<git_user> GIT_TOKEN=<git_token> python crawler/bfs_user_repo_contributors.py <output_file> <depth>")
        sys.exit(0)

    seeds = ['daniel-hasan']
    crawler = BFSUserRepoContributors(seeds)
    crawler.perform_crawl(sys.argv[1], int(sys.argv[2]))
