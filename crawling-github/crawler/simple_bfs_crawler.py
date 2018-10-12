import sys
from GitHubAPI import GitHubRepo
from collections import deque

class ApiBFSCrawler():
    def __init__(self, seeds):
        self.queue = deque([(s, 0) for s in seeds])
        self.reposCrawled = set()

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

    def perform_crawl(self,output,maxDepth):
        '''
            Crawl using breath first search adding all the following users of
            each crawled repository.
        '''

        with open(output,"w") as file:
            while len(self.queue)>0:
                # dequeue de first repo in the queue
                repo, curDepth = self.queue.popleft()
                print("Crawling repo: "+str(repo)+" Queue size: "+str(len(self.queue)))
                self.reposCrawled.add(repo.info['full_name'])

                # add an edge to the graph for each contributors of this repo
                print("Number of contributors of {repo_full_name}: {contributors}".format(
                    repo_full_name=repo.info['full_name'],
                    contributors=len(repo.contributors)
                ))
                self.write_edges(file, repo)

                # add all users repositories to the queue
                if(curDepth + 1 < maxDepth):
                    for user in repo.contributors:
                            for nextRepo in user.repos:
                                if nextRepo.info['full_name'] not in self.reposCrawled:
                                    print("Added to the queue: {repo_full_name} depth: {depth}".format(
                                        repo_full_name=nextRepo.info['full_name'],
                                        depth=curDepth+1
                                    ))
                                    self.queue.append((nextRepo, curDepth+1))



if __name__ == "__main__":
    if len(sys.argv) < 3 or not int(sys.argv[2]):
        print("Correct use:")
        print("GIT_USER=<git_user> GIT_TOKEN=<git_token> python crawler/simple_bfs_crawler.py <output_file> <depth>")
        sys.exit(0)

    seeds = [GitHubRepo('daniel-hasan','cefet-web')]
    api = ApiBFSCrawler(seeds)
    api.perform_crawl(sys.argv[1], int(sys.argv[2]))
