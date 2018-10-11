import github_api_requests

class GithubUserCrawled():
    def __init__(self,name,level):
        self.name = name
        self.level = level

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
                #save its repositories urls
                for repo in get_repo_from_user(user):
                    

                #add the following users
                get_user_following(user.name)



if __name__ == "__main__":

    print(get_user_followers("daniel-hasan"))
