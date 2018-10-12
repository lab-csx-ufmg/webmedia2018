from github_api_requests import *
from collections import deque

class GithubRepoToCrawl():
    def __init__(self,userName,repoName,depth=0):
        self.userName = userName
        self.repoName = repoName
        self.depth = depth
    def __str__(self):
        return "Name: "+self.userName+"/"+self.repoName+" depth: "+str(self.depth)

class ApiBFSCrawler():
    def __init__(self,repoSeeds):
        self.queue = deque(repoSeeds)
        self.usersCrawled = set()

    def write_edges(self,file,arrContributors):
        if(len(arrContributors)<=1):
            return
        for u,contu in enumerate(arrContributors):
            for contv in arrContributors[u+1:]:
                file.write(contu["login"]+','+contv["login"]+'\n')

    def perform_crawl(self,output,maxDepth):
        '''
            Crawl using breath first search adding all the following users of
            each crawled repository.
        '''

        with open(output,"w") as file:
            while len(self.queue)>0:
                #dequeue de first repo in the queue
                repo = self.queue.popleft()
                print("Crawling repo: "+str(repo)+" Queue size: "+str(len(self.queue)))
                self.usersCrawled.add(repo.userName)

                #add an edge to the graph for each contributors of this repo
                arrContributors = get_contributors_from_repo(repo.userName,repo.repoName)
                print("Number of contributors of "+repo.userName+"/"+repo.repoName+":"+str(len(arrContributors)))
                self.write_edges(file,arrContributors)

                #add all users repositories to the queue
                if(repo.depth < maxDepth):
                    for contributor in arrContributors:
                        if contributor['login'] not in self.usersCrawled:
                            for usrRepo in get_repo_from_user(contributor['login']):
                                print("Added to the queue: "+str(GithubRepoToCrawl(usrRepo['owner']['login'],usrRepo['name'],repo.depth+1)))
                                self.queue.append(GithubRepoToCrawl(usrRepo['owner']['login'],usrRepo['name'],repo.depth+1))



if __name__ == "__main__":
    repoSeeds = [GithubRepoToCrawl('daniel-hasan','cefet-web')]
    api = ApiBFSCrawler(repoSeeds)
    api.perform_crawl("teste-coleta.txt",2)
