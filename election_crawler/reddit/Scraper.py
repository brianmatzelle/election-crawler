from reddit.Client import Client
from reddit.ParsedPost import ParsedPost, Comment
# from Client import Client
# from ParsedPost import ParsedPost, Comment
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from reddit.utils.api_calls import getToxic
from config import uri
# from utils.api_calls import getToxic

class Scraper:
    def __init__(self, subreddit: str):
        '''
        - Initializes a Scraper object, which is used to scrape a subreddit for many posts at once.
        '''
        self.client = Client() # client makes requests to reddit API
        self.sub = subreddit
        self.posts = None
        self.parsed_posts: list[ParsedPost] = []
        self.comments = None
        self.parsed_comments: list[Comment] = []

        print("Spinning up reddit db for " + self.sub + "...")
        self.mongo_client = MongoClient(uri, server_api=ServerApi('1'))
        self.reddit_db = self.mongo_client.reddit
        self.reddit_db_posts = self.reddit_db.posts
        self.reddit_db_comments = self.reddit_db.comments
        self.reddit_db_params = self.reddit_db.params

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
        - Parses the posts from the subreddit, storing them as ParsedPost objects in Scraper.parsed_posts list.
        - ParsedPost objects contain the post data, as well as the comments for each post.
        '''

        #self.checkForErrors("parsePosts")

        latest_id = ''
        q_string = "latest_post_" + self.sub
        query = {"kind": q_string}
        
        try:
            query_post = self.reddit_db_params.find(query, limit=1)
            for q in query_post:
                # there should be only one, but u have to do this anyway
                # bc it's a collection
                latest_id = q["meat"]
        except:
            latest_id = "initial_run"
            self.reddit_db_params.insert_one({"kind": q_string, "meat": "initial_run"})

        i = 0
        new_id = latest_id
        for post in self.posts["data"]["children"]:
            if self.checkPostValid(post) == False:
                continue

            curr_id = post["data"]["id"]

            # if we found the last post we got last run, break
            if curr_id == latest_id:
                break

            # if we find any post, save it as the newest post found
            if i == 0:
                new_id = curr_id

            # toks = post["data"]["permalink"].split('/') 
            #later check toxicity here
            toxic = -1
            self.parsed_posts.append(ParsedPost(post, toxic, self.sub, i))
            i += 1

        newval = {"$set": {"meat": new_id}}
        self.reddit_db_params.update_one(query, newval)
        
        return self

    def parseComments(self):
        '''
        - Parses comments from comment json for new comments
        '''

        # this here just grabs the id of the last comment we grabbed.
        # if this is the first run of the program on the machine, it
        # just puts in a place holder to populate the field
        latest_id = ''
        query = {"kind": "latest_comment"}
        try:
            query_comment = self.reddit_db_params.find(query, limit=1)
            for q in query_comment:
                # there should be only one, but u have to do this anyway
                # bc it's a collection
                latest_id = q["meat"]
        except:
            latest_id = 'initial_run'
            self.reddit_db_params.insert_one({"kind": "latest_comment", "meat": "initial_run"})

        i = 0
        new_id = latest_id
        for comment in self.comments["data"]["children"]:
            if self.checkCommentValid(comment) == False:
                continue

            curr_id = comment["data"]["id"]

            # if we found the last comment we got last run, break
            if curr_id == latest_id:
                break

            # if we successfully find any comment, we save its id
            # to become the new latest comment id
            if i == 0:
                new_id = curr_id
                #print("new: " + new_id)
            
            toks = comment["data"]["permalink"].split('/')

            #check toxicity
            toxic = getToxic(comment["data"]["body"])

            self.parsed_comments.append(Comment(comment, toks[4], toxic))
            i += 1

        # setting the new latest comment id
        newval = {"$set": {"meat": new_id}}
        self.reddit_db_params.update_one(query, newval)

        return self

    def logParsedPosts(self, file_name: str):
        '''
        - Logs the parsed posts to a file, in YAML format.
        - I only chose YAML because it's easier to read than .txt, ignore the incorrect formatting. (I like the highlighting)
        '''

        #self.checkForErrors("logParsedPosts")

        out_file = open(file_name, 'w', encoding="utf-8")
        i = 0
        print(f"Number of posts: {len(self.parsed_posts)}", file=out_file)

        for post in self.parsed_posts:
            post.print(out_file)
            i += 1

            post_dict = post.getAsDict()
            post_id = post.id

            print("(" + self.sub + ") storing post " + post_id)
            x = self.reddit_db_posts.insert_one(post_dict)

        out_file.close()

        return self
    
    def insertParsedPosts(self):
        for post in self.parsed_posts:
            post_dict = post.getAsDict()
            post_id = post.id
            print("(" + self.sub + ") storing post " + post_id)
            self.reddit_db_posts.insert_one(post_dict)
        return self
    
    def getLinks(self) -> list[str]:
        links = []
        for post in self.parsed_posts:
            links.append(f'https://www.reddit.com{post.post_link}')
        return links

    def logParsedComments(self, file_name: str):
        '''
        - Logs the parsed comments to a file, in YAML format.
        - I only chose YAML because it's easier to read than .txt, ignore the incorrect formatting. (I like the highlighting)
        '''

        out_file = open(file_name, 'w', encoding="utf-8")
        i = 0
        print(f"Number of comments: {len(self.parsed_comments)}", file=out_file)

        for comment in self.parsed_comments:
            comment.print(out_file, i)
            i += 1

            # add comment to mongo. parseComments should have already
            # only collected new comments
            comment_dict = comment.getAsDict()
            comment_id = comment.id

            print("storing comment " + comment_id)
            x = self.reddit_db_comments.insert_one(comment_dict)

            # add comment id to list of comment ids of parent post
            # if we've seen the parent post
            post_id = comment_dict["post_id"]
            query = {"id" : post_id}
            query_post = self.reddit_db_posts.find(query)

            # this will either loop once, or not at all
            for q in query_post:
                try:
                    q_comment_ids = q["comment_ids"]
                except:
                    print("this is an old post without a comment_ids list")
                    continue
                q_comment_ids.append(comment_id)
                set_comment_ids = {"$set": {"comment_ids": q_comment_ids}}
                self.reddit_db_posts.update_one(query, set_comment_ids)
                print("gave post " + post_id + " comment " + comment_id)

        out_file.close()
        return self
    
    def insertParsedComments(self):
        for comment in self.parsed_comments:
            comment_dict = comment.getAsDict()
            comment_id = comment.id
            print("storing comment " + comment_id)
            x = self.reddit_db_comments.insert_one(comment_dict)

            # add comment id to list of comment ids of parent post
            # if we've seen the parent post
            post_id = comment_dict["post_id"]
            query = {"id" : post_id}
            query_post = self.reddit_db_posts.find(query)

            # this will either loop once, or not at all
            for q in query_post:
                try:
                    q_comment_ids = q["comment_ids"]
                except:
                    print("this is an old post without a comment_ids list")
                    continue
                q_comment_ids.append(comment_id)
                set_comment_ids = {"$set": {"comment_ids": q_comment_ids}}
                self.reddit_db_posts.update_one(query, set_comment_ids)
                print("gave post " + post_id + " comment " + comment_id)

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

        return valid