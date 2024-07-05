from Client import Client
from ParsedPost import ParsedPost, Comment
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import os

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
        PROJECT_ROOT = "/home/brian/projects/election-crawler/election_crawler/reddit"
        if not os.path.exists(f"{PROJECT_ROOT}/logs"):
            os.makedirs(f"{PROJECT_ROOT}/logs")
        if not os.path.exists(f"{PROJECT_ROOT}/logs/{self.sub}"):
            os.makedirs(f"{PROJECT_ROOT}/logs/{self.sub}")

        file_name = f"{PROJECT_ROOT}/logs/{self.sub}/{dt}.yml"
        log_file = open(file_name, 'w', encoding="utf-8")

        for post in self.parsed_posts:
            post.print(log_file)
            print("\n", file=log_file)

if __name__ == "__main__":
    subreddit = "destiny"
    scraper = Scraper(subreddit)
    scraper \
        .getPosts().parsePosts() \
        .getComments().parseComments() \
        .logParsedPosts()
    print(f"Scraped {len(scraper.parsed_posts)} posts and {len(scraper.parsed_comments)} comments.")


# class ScraperGUI:
#     def __init__(self, root, scraper):
#         self.root = root
#         self.scraper = scraper
#         self.root.title("Scraper GUI")

#         self.create_posts_tab()
    
#     def create_posts_tab(self):
#         self.posts_frame = ttk.Frame(self.root)
#         self.posts_frame.pack(expand=1, fill="both")

#         self.posts_listbox = tk.Listbox(self.posts_frame)
#         self.posts_listbox.pack(fill=tk.BOTH, expand=1)
#         self.posts_listbox.bind('<<ListboxSelect>>', self.on_post_select)

#         self.posts_search_entry = tk.Entry(self.posts_frame)
#         self.posts_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=1)
        
#         self.posts_search_button = tk.Button(self.posts_frame, text="Search", command=self.search_posts)
#         self.posts_search_button.pack(side=tk.RIGHT)

#         self.load_posts()
    
#     def load_posts(self):
#         for post in self.scraper.parsed_posts:
#             self.posts_listbox.insert(tk.END, f"{len(post.comments)} {post.title}")
    
#     def search_posts(self):
#         search_term = self.posts_search_entry.get().lower()
#         self.posts_listbox.delete(0, tk.END)
#         for post in self.scraper.parsed_posts:
#             if search_term in post.title.lower():
#                 self.posts_listbox.insert(tk.END, post.title)
    
#     def on_post_select(self, event):
#         selected_index = self.posts_listbox.curselection()
#         if selected_index:
#             selected_post = self.scraper.parsed_posts[selected_index[0]]
#             self.show_comments(selected_post)
    
#     def show_comments(self, post):
#         comments_window = tk.Toplevel(self.root)
#         comments_window.title(f"Comments for: {post.title}")

#         comments_listbox = tk.Listbox(comments_window)
#         comments_listbox.pack(fill=tk.BOTH, expand=1)
        
#         for comment in post.comments:
#             comments_listbox.insert(tk.END, comment.body)

# if __name__ == "__main__":
#     subreddit = "destiny"
#     scraper = Scraper(subreddit)
#     scraper.getPosts().parsePosts()
#     scraper.getComments().parseComments()
#     print(f"Scraped {len(scraper.parsed_posts)} posts and {len(scraper.parsed_comments)} comments.")

#     root = tk.Tk()
#     app = ScraperGUI(root, scraper)
#     root.mainloop()