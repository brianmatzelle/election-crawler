class Comment:
    '''
    - "Private" class for ParsedPost, contains the data for a comment. Better to have a class for type safety.
    '''
    def __init__(self, comment, post_id):
        self.author = comment["data"]["author"]
        self.body = comment["data"]["body"]
        self.id = comment["data"]["id"]
        self.comment_link = comment["data"]["permalink"]
        self.post_id = post_id
        self.created_utc = comment["data"]["created_utc"]
        self.toxic = -1
    
    def print(self, out_file, index):
        print("    Comment %2d:" % (index), file=out_file)
        print('      Author: ', self.author, file=out_file)
        print('      Body: ', self.body, file=out_file)
        print('      Id: ', self.id, file=out_file)
        print('      Created UTC: ', self.created_utc, file=out_file)
        print('      Toxic: ', self.toxic, file=out_file)

    def getAsDict(self):
        comment_dict = {
            "author": self.author,
            "body": self.body,
            "id": self.id,
            "comment_link": self.comment_link,
            "post_id": self.post_id,
            "created_utc": self.created_utc,
            "toxic": self.toxic
        }

        return comment_dict

class ParsedPost:
    def __init__(self, post, sub):
        '''
        - Initializes a ParsedPost object, which contains the data for a post, as well as the comments for that post.
        - The comments are stored as Comment objects in ParsedPost.comments list.
        '''
        self.author = post["data"]["author"]
        self.title = post["data"]["title"]
        self.id = post["data"]["id"]
        self.post_link = post["data"]["permalink"]
        self.clip_link = post["data"]["url"]
        self.clip_time = post["data"]["created_utc"]
        self.sub = sub
        self.toxic = -1
        self.comments = []

        #not super necessary to make this a field, but whatever
        self.comment_ids: list[str] = []
        self.twitch_ids: list[str] = []

        # loop through comments and create Comment objects for each one, store in self.comments list
        #self.comments: list[Comment] = (Comment(comment) for comment in post_page[1]["data"]["children"])
    
    def print(self, out_file):
        print('Author: ', self.author, file=out_file)
        print('Title: ', self.title, file=out_file)
        print('Id: ', self.id, file=out_file)
        print('Post Link: ', self.post_link, file=out_file)
        print('Clip Link: ', self.clip_link, file=out_file)
        print('Created UTC: ', self.clip_time, file=out_file)
        print('Sub: ', self.sub, file=out_file)
        print('Toxic: ', self.toxic, file=out_file)
        print('Comments: ', file=out_file)
        if len(self.comments) == 0:
            print("        none", file=out_file)
        for i, comment in enumerate(self.comments):
            comment.print(out_file, i)

    def getAsDict(self):
        post_dict = {
            "title": self.title,
            "author": self.author,
            "id": self.id,
            "post_link": self.post_link,
            "clip_link": self.clip_link,
            "created_utc": self.clip_time,
            "sub": self.sub,
            "toxic": self.toxic,
            "comments": [comment.getAsDict() for comment in self.comments],
        }

        return post_dict