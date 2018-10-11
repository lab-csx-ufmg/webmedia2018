from github_api_requests import *

class GithubUserCrawled():
    def __init__(self,name,level):
        self.name = name
        self.level = level
    def __str__(self):
        return "Name: "+self.name+" level: "+str(level)
class ApiBFSCrawler():
    def __init__(self,userSeeds):
        self.userSeeds = userSeeds
        self.queue = []

    def perform_crawl(maxLevel,output):
        '''
            Crawl using breath first search add all the following users of
            each user crawled respecting the depth level of the crawling
        '''
        #add the seed to the queue
        [self.queue.append(GithubUserCrawled(user,0)) for user in self.userSeeds]

        with open(output,"w") as file:
            while len(self.queue)>0:
                #dequeue de first element
                user = self.queue.pop(0)
                print("Crawling user: "+user+" Queue size: "+str(len(self.queue)))
                #save its repositories clone url
                for repo in get_repo_from_user(user):
                    file.write(repo["name"],repo["clone_url"])

                #add the following users in the queue
                for userFollowing in get_user_following(user.name):
                    if(user.level < maxLevel):
                        self.queue.append(GithubUserCrawled(userFollowing['login'],user.level+1)



if __name__ == "__main__":

    print(get_user_following("fegemo")[0])
