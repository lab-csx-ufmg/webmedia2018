import sys
from GitHubAPI import GitHubUser
from collections import deque

class BFSUserRepoContributors():
    def __init__(self, seeds):
        self.queue = deque([(GitHubUser(username), 0) for username in seeds])
        self.discovered_users = set(seeds)

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
        pass

if __name__ == "__main__":
    if len(sys.argv) < 3 or not int(sys.argv[2]):
        print("Correct use:")
        print("GIT_USER=<git_user> GIT_TOKEN=<git_token> python crawler/bfs_user_repo_contributors.py <output_file> <depth>")
        sys.exit(0)

    seeds = ['daniel-hasan']
    crawler = BFSUserRepoContributors(seeds)
    crawler.perform_crawl(sys.argv[1], int(sys.argv[2]))
