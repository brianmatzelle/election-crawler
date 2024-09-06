from election_crawler.reddit.Client import Client
from election_crawler.reddit.ParsedPost import ParsedPost, Comment
from election_crawler.reddit.config import subreddits, uri
from datetime import datetime
import os
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from tqdm import tqdm
from tqdm.auto import trange
import time

"""
# PROGRAM CALLING ORDERs:
init -> 
    getPosts() -> 
        ** call reddit for a single subreddit's hot posts **, then
        savePosts(posts) -> 
            ↻ DAO ** if post isn't in DB, save in memory **
    uploadToMongo() ->
        ** upload all posts in memory to MongoDB **

init ->
    update_unfinalised_posts() ->
        ** get 20 unfinalised posts from MongoDB **, then
        ** update the posts with the most recent data from Reddit **, then
        ** save the updated posts back to MongoDB **

"""

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
        self.hot_ids = []

    def update_unfinalised_posts(self) -> str:
        # Find 20 unfinalised posts
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client["reddit"]
        unfinalised_posts = db.posts.find({"finalized": False}).limit(20)

        log_string = ""
        for post in unfinalised_posts:
            time.sleep(1)
            try:
                # Get the most recent version of the post from Reddit
                updated_post = self.client.get_one_post_by_url(post["data"]["permalink"])
                for element in updated_post:
                    for index in element["data"]["children"]:
                        if index["kind"] == "t3":  # Post
                            log_string += f"main post found, updating post {post['id']}...\n"
                            # Update the post data
                            db.posts.update_one(
                                {"id": post["id"]}, 
                                {
                                    "$set": {
                                        "data": index["data"],
                                        "finalized": True  # Mark the post as finalized
                                    }
                                }
                            )
                        elif index["kind"] == "t1":  # Comment
                            # Update or insert the comment in the post's comments field
                            log_string += f"comment found, updating post {post['id']}...\n"
                            post_id = index["data"]["link_id"].split('_')[1]
                            if post_id == post["id"]:  # Make sure the comment belongs to the correct post
                                db_post = db.posts.find_one({"id": post_id})
                                if db_post:
                                    if "comments" in db_post:
                                        db_post["comments"][index["data"]["id"]] = index["data"]
                                    else:
                                        db_post["comments"] = {index["data"]["id"]: index["data"]}

                                    # Update the comments field in the database
                                    db.posts.update_one(
                                        {"id": post_id}, 
                                        {"$set": {"comments": db_post["comments"]}}
                                    )
                        else:
                            # Skip any other kind of content (e.g., ads or other kinds of listings)
                            continue

                    updated_count += 1

            except Exception as e:
                log_string += f"Error updating post {post['id']}: {e}\n"
                continue

        return updated_count


    def getPosts(self):
        '''
        - Returns a list of posts from the subreddit, only necessary so our main.py is easier to understand
        '''
        posts = self.client.get_posts(self.sub) # if this fails, we're getting rate limited
        self.savePosts(posts, "new")
        return self
    
    def savePosts(self, posts, type=""):
        for post in tqdm(posts["data"]["children"], ascii=True, desc=f"Scraping {self.sub} [{type}]"):
            try:
                client = MongoClient(uri, server_api=ServerApi('1'))
                db = client["reddit"]
                existing_post = db.posts.find_one({"id": post["data"]["id"]})
                # if existing_post and (existing_post["hot"] == (post["data"]["id"] in self.hot_ids)): # if post already exists in db, and it's hot in both the db and the current scrape, skip
                #     continue
                if existing_post:
                    continue
                self.posts.append(self.client.get_one_post_by_url(post["data"]["permalink"]))
                time.sleep(1)

            except Exception as e:
                PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
                if not os.path.exists(f"{PROJECT_ROOT}/logs"):
                    os.makedirs(f"{PROJECT_ROOT}/logs")
                if not os.path.exists(f"{PROJECT_ROOT}/logs/{self.sub}"):
                    os.makedirs(f"{PROJECT_ROOT}/logs/{self.sub}")
                if not os.path.exists(f"{PROJECT_ROOT}/logs/{self.sub}/errors"):
                    os.makedirs(f"{PROJECT_ROOT}/logs/{self.sub}/errors")
                with open(f"{PROJECT_ROOT}/logs/{self.sub}/errors/error_ids.txt", "a") as f:
                    f.write(f"{post['data']['id']}\n")
                continue
        return self

    def getHotPosts(self):
        '''
        - Returns a list of hot posts from the subreddit, only necessary so our main.py is easier to understand
        '''
        posts = self.client.get_hot_posts(self.sub)
        for post in posts["data"]["children"]:
            self.hot_ids.append(post["data"]["id"])
            
        self.savePosts(posts, "hot")
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
        for response_arr in tqdm(self.posts, ascii=True, desc=f"Uploading {self.sub}"):
            for post in response_arr:
                try:
                    for index in post["data"]["children"]:
                        if index["kind"] == "t3": # t3 is a post
                            if db.posts.find_one({"id": index["data"]["id"]}):
                                continue
                            else:
                                hot = False
                                if index["data"]["id"] in self.hot_ids:
                                    hot = True
                                id = db.posts.insert_one({
                                    "id": index["data"]["id"],
                                    "data": index["data"],
                                    "comments": {},
                                    "hot": hot
                                })
                                # print(f"INSERTED post: {index['data']['id']}")
                        if index["kind"] == "t1": # t1 is a comment
                            post_id = index["data"]["link_id"].split('_')[1]
                            db_post = db.posts.find_one({"id": post_id})
                            if db_post:
                                if "comments" in db_post:
                                    if index["data"]["id"] in db_post["comments"]:
                                        # print(f"skipping comment: {index['data']['id']}")
                                        continue
                                    db_post["comments"][index["data"]["id"]] = index["data"]
                                    db.posts.update_one({"id": post_id}, {"$set": {"comments": db_post["comments"]}})
                                    # print(f"INSERTED comment: {index['data']['id']}")
                                else:
                                    db.posts.update_one({"id": post_id}, {"$set": {"comments": {index["data"]["id"]: index["data"]}}})
                                    # print(f"INSERTED comment: {index['data']['id']}")
                            else:
                                # print("skipping post, post not found in db")
                                continue
                except Exception as e:
                    print(f"Error: {e},\n skipping post {post['data']}")


# if __name__ == "__main__":
#     scraper = Scraper("destiny")
#     scraper.getPosts()
#     scraper.uploadToMongo()

# if __name__ == "__main__":
#     scraper = Scraper("destiny")
#     scraper.update_unfinalised_posts()
