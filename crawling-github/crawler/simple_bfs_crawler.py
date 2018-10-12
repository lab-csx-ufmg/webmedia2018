from github_api_requests import GitHubAPI

api = GitHubAPI()

class GitHubUser():
    def __init__(self,name,level):
        self.name = name
        self.level = level
    def __str__(self):
        return "GitHubUser(name={name}, level={level})".format(name=self.name, level=str(self.level))


class GitHubBFSCrawler():
    def __init__(self,userSeeds):
        self.userSeeds = userSeeds
        self.queue = []

    def perform_crawl(self, maxLevel,output):
        '''
            Crawl using breath first search add all the following users of
            each user crawled respecting the depth level of the crawling
        '''
        #add the seed to the queue
        [self.queue.append(GitHubUser(user,0)) for user in self.userSeeds]

        with open(output,"w") as file:
            while len(self.queue)>0:
                #dequeue de first element
                user = self.queue.pop(0)
                print("Crawling user: {gitUser} Queue size: {queueSize}".format()+str(len(self.queue)))
                #save its repositories clone url
                for repo in api.get_repo_from_user(user):
                    file.write(repo["name"],repo["clone_url"])

                #add the following users in the queue
                for userFollowing in api.get_user_following(user.name):
                    if(user.level < maxLevel):
                        self.queue.append(GitHubUser(userFollowing['login'],user.level+1))


if __name__ == "__main__":

    # print(api.get_user_following("fegemo")[0])
    crawler = GitHubBFSCrawler(['fegemo'])
    crawler.perform_crawl(2, 'output')
