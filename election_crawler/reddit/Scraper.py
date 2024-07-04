from .Client import Client
from .ParsedPost import ParsedPost, Comment

class Scraper:
    def __init__(self, subreddit: str):
        '''
        - Initializes a Scraper object, which is used to scrape a subreddit for many posts at once.
        '''
        self.client = Client()
        self.sub = subreddit
        self.posts = None
        self.parsed_posts: list[ParsedPost] = []
        self.comments = None
        self.parsed_comments: list[Comment] = []

    def getPosts(self):
        '''
        - Returns a list of posts from the subreddit, only necessary so our main.py is easier to understand
        '''
        self.posts = self.client.get_posts(self.sub)
        return self

    def getComments(self):
        '''
        - Returns a list of comments from the subreddit, only necessary so our main.py is easier to understand
        '''
        self.comments = self.client.get_comments(self.sub)
        return self
    
    def parsePosts(self):
        '''
        - Parses the posts from the subreddit into ParsedPost objects
        '''
        for post in self.posts["data"]["children"]:
            if self.checkPostValid(post) == False:
                continue

            self.parsed_posts.append(ParsedPost(post, self.sub))

        return self