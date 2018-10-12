from github_api_requests import *
from collections import deque

class GithubRepoCrawled():
    def __init__(self,user,repoName,level):
        self.user = user
        self.repoName =repoName
        self.level = level
    def __str__(self):
        return "Name: "+self.name+" level: "+str(level)

class ApiBFSCrawler():
    def __init__(self,userSeeds):
        self.repoSeeds = repoSeeds
        self.queue = deque([])

    def perform_crawl(maxLevel,output):
        '''
            Crawl using breath first search add all the following users of
            each user crawled respecting the depth level of the crawling
        '''
        #add the seed to the queue
        [self.queue.append(GithubRepoCrawled(user,0)) for repo in self.repoSeeds]

        with open(output,"w") as file:
            while len(self.queue)>0:
                #dequeue de first repo in the queue
                repo = self.queue.popleft()
                print("Crawling repo: "+repo+" Queue size: "+str(len(self.queue)))

                #add an edge to the graph for each contributors of this repo
                arrContributors = get_contributors_from_repo(repo.user,repo.repoName)
                for cont1 in arrContributors:
                    for cont2 in arrContributors:
                        if cont1 != cont2:
                            file.write(cont1["login"]+","+cont2["login"])

                    #add the users repo to the queue
                    if(repo.level < maxLevel):
                        for usrRepo in get_repo_from_user(cont1['login']):
                            self.queue.append(GithubUserCrawled(usrRepo['owner']['login'],usrRepo['name'],user.level+1)



if __name__ == "__main__":

    print(get_user_following("fegemo")[0])
