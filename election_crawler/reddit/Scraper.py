from election_crawler.reddit.Client import Client
from election_crawler.reddit.ParsedPost import ParsedPost, Comment
from election_crawler.reddit.config import subreddits, uri
from datetime import datetime
import os
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi

class Scraper:
    def __init__(self, subreddit: str):
        '''
        - Initializes a Scraper object, which is used to scrape a subreddit for many posts at once.
        '''
        self.client = Client()
        self.sub = subreddit
        self.posts = []
        self.parsed_posts: list[ParsedPost] = []
        self.comments = []
        self.parsed_comments: list[Comment] = []

    def getPosts(self):
        '''
        - Returns a list of posts from the subreddit, only necessary so our main.py is easier to understand
        '''
        posts = self.client.get_posts(self.sub) # if this fails, we're getting rate limited
        for post in posts["data"]["children"]:
            try:
                self.posts.append(self.client.get_one_post_by_url(post["data"]["permalink"]))
            except Exception as e:
                print(f"Error: {e}, skipping post {post['data']}")
                PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
                if not os.path.exists(f"{PROJECT_ROOT}/logs"):
                    os.makedirs(f"{PROJECT_ROOT}/logs")
                if not os.path.exists(f"{PROJECT_ROOT}/logs/{self.sub}"):
                    os.makedirs(f"{PROJECT_ROOT}/logs/{self.sub}")
                if not os.path.exists(f"{PROJECT_ROOT}/logs/{self.sub}/errors"):
                    os.makedirs(f"{PROJECT_ROOT}/logs/{self.sub}/errors")
                now = datetime.now()
                dt = now.strftime("%Y%m%d_%H%M%S")
                file_name = f"{PROJECT_ROOT}/logs/{self.sub}/errors/{dt}.json"
                log_file = open(file_name, 'w', encoding="utf-8")
                json.dump(post, log_file)
                continue
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
    
    def parseComments(self):
        '''
        - Parses the comments from the subreddit into Comment objects
        '''
        for comment in self.comments["data"]["children"]:
            if self.checkCommentValid(comment) == False:
                continue
            toks = comment["data"]["permalink"].split('/')
            post_id = toks[4]
            self.parsed_comments.append(Comment(comment, post_id))

        self._assignCommentsToPost()

        return self
    
    def _assignCommentsToPost(self):
        '''
        - Assigns the comments to the correct posts
        '''
        for comment in self.parsed_comments:
            for post in self.parsed_posts:
                if comment.post_id == post.id:
                    post.comments.append(comment)
    
    def checkForErrors(self, method_name: str):
        '''
        - Function to check for errors the user might make when calling any of the public methods in Scraper. 
        - Should not be called by the user.
        '''
        match method_name:
            case "parsePosts":
                if not self.posts:
                    raise Exception("Error: Scraper.getPosts() must be called before Scraper.parsePosts()")
            case "logParsedPosts":
                if not self.parsed_posts:
                    raise Exception("Error: Scraper.parsePosts() must be called before Scraper.logParsedPosts()")
            case _:
                raise Exception("Error: Invalid method name passed to Scraper.checkForErrors(), check private calls to Scraper.checkForErrors()")
        
    
    def checkPostValid(self, post):
        link = post["data"]["permalink"]
        errors = ""
        valid = True

        try:
            var = post["data"]["author"]
        except:
            errors = errors + "\nPost has no author"
            valid = False

        try:
            var = post["data"]["title"]
        except:
            errors = errors + "\nPost has no title"
            valid = False

        try:
            var = post["data"]["id"]
        except:
            errors = errors + "\nPost has no id"
            valid = False

        try:
            var = post["data"]["url"]
        except:
            errors = errors + "\nPost has no clip"
            valid = False
        
        try:
            var = post["data"]["created_utc"]
        except:
            errors = errors + "\nPost has no UTC"
            valid = False
        
        if valid == False:
            now = datetime.now()
            dt = now.strftime("%Y%m%d_%H%M%S")
            file_name = "error-logs/" + dt + ".txt"
            err_file = open(file_name, 'w', encoding="utf-8")


            print("Post " + link + " has errors:" + errors, file=err_file)

        return valid

    def checkCommentValid(self, comment):
        link = comment["data"]["permalink"]
        errors = ""
        valid = True

        try:
            var = comment["data"]["author"]
        except:
            errors = errors + "\nComment has no author"
            valid = False

        try:
            var = comment["data"]["body"]
        except:
            errors = errors + "\nComment has no body"
            valid = False

        try:
            var = comment["data"]["id"]
        except:
            errors = errors + "\nComment has no id"
            valid = False
        
        try:
            var = comment["data"]["created_utc"]
        except:
            errors = errors + "\nComment has no UTC"
            valid = False
        
        try:
            var = comment["data"]["permalink"]
        except:
            errors = errors + "\nComment has no permalink"
            valid = False
        
        if valid == False:
            now = datetime.now()
            dt = now.strftime("%Y%m%d_%H%M%S")
            file_name = "error-logs/" + dt + ".txt"
            err_file = open(file_name, 'w', encoding="utf-8")


            print("Comment " + link + " has errors:" + errors, file=err_file)

    def logParsedPosts(self):
        '''
        - Logs the parsed posts to a file
        '''
        self.checkForErrors("logParsedPosts")

        now = datetime.now()
        dt = now.strftime("%Y%m%d_%H%M%S")
        # PROJECT_ROOT = "/home/brian/projects/election-crawler/election_crawler/reddit"
        PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(f"{PROJECT_ROOT}/logs"):
            os.makedirs(f"{PROJECT_ROOT}/logs")
        if not os.path.exists(f"{PROJECT_ROOT}/logs/{self.sub}"):
            os.makedirs(f"{PROJECT_ROOT}/logs/{self.sub}")

        file_name = f"{PROJECT_ROOT}/logs/{self.sub}/{dt}.yml"
        log_file = open(file_name, 'w', encoding="utf-8")

        for post in self.parsed_posts:
            post.print(log_file)
            print("\n", file=log_file)

    def logParsedPostsJson(self):
        self.checkForErrors("logParsedPosts")
        now = datetime.now()
        dt = now.strftime("%Y%m%d_%H%M%S")
        PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

        if not os.path.exists(f"{PROJECT_ROOT}/logs"):
            os.makedirs(f"{PROJECT_ROOT}/logs")
        if not os.path.exists(f"{PROJECT_ROOT}/logs/{self.sub}"):
            os.makedirs(f"{PROJECT_ROOT}/logs/{self.sub}")

        file_name = f"{PROJECT_ROOT}/logs/{self.sub}/{dt}.json"
        log_file = open(file_name, 'w', encoding="utf-8")

        posts = []
        for post in self.parsed_posts:
            posts.append(post.getAsDict())

        json.dump(posts, log_file)

    def uploadToMongo(self):
        '''
        - Uploads the parsed posts to a MongoDB database
        '''
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client["reddit"]
        for response_arr in self.posts:
            for post in response_arr:
                try:
                    for index in post["data"]["children"]:
                        if index["kind"] == "t3": # t3 is a post
                            if db.posts.find_one({"id": index["data"]["id"]}):
                                print("Post with id: ", index["data"]["id"], " already exists in database, skipping")
                            else:
                                id = db.posts.insert_one({
                                    "id": index["data"]["id"],
                                    "data": index["data"],
                                    "comments": {},
                                })
                                print("Inserted post with id: ", id.inserted_id)
                        if index["kind"] == "t1": # t1 is a comment
                            post_id = index["data"]["link_id"].split('_')[1]
                            db_post = db.posts.find_one({"id": post_id})
                            if db_post:
                                if "comments" in db_post:
                                    if index["data"]["id"] in db_post["comments"]:
                                        print("Comment with id: ", index["data"]["id"], " already exists in database, skipping")
                                        continue
                                    db_post["comments"][index["data"]["id"]] = index["data"]
                                    db.posts.update_one({"id": post_id}, {"$set": {"comments": db_post["comments"]}})
                                    print("Inserted comment with id: ", index["data"]["id"])
                                else:
                                    db.posts.update_one({"id": post_id}, {"$set": {"comments": {index["data"]["id"]: index["data"]}}})
                                    print("Inserted comment with id: ", index["data"]["id"])
                            else:
                                print("Post with id: ", post_id, " does not exist in database, skipping")
                except Exception as e:
                    print(f"Error: {e},\n skipping post {post['data']}")


# if __name__ == "__main__":
#     for subreddit in subreddits:
#         scraper = Scraper(subreddit)
#         scraper.getPosts()
#         PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
#         if not os.path.exists(f"{PROJECT_ROOT}/logs"):
#             os.makedirs(f"{PROJECT_ROOT}/logs")
#         if not os.path.exists(f"{PROJECT_ROOT}/logs/{subreddit}"):
#             os.makedirs(f"{PROJECT_ROOT}/logs/{subreddit}")
#         now = datetime.now()
#         dt = now.strftime("%Y%m%d_%H%M%S")
#         file_name = f"{PROJECT_ROOT}/logs/{subreddit}/{dt}.json"
#         log_file = open(file_name, 'w', encoding="utf-8")
#         json.dump(scraper.posts, log_file)

if __name__ == "__main__":
    scraper = Scraper("destiny")
    scraper.getPosts()
    scraper.uploadToMongo()
