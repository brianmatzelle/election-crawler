import requests
from config import CLIENT_ID, CLIENT_SECRET

class Client:

    BASE_API_URL = "https://reddit.com"
    ACCESS_TOKEN = ''
    USER_AGENT = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'

    def __init__(self) -> None:
        self.client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
        self.post_data = {"grant_type": "client_credentials"}
        self.headers = {'User-Agent': self.USER_AGENT}
        self.token_req = requests.post('https://www.reddit.com/api/v1/access_token',
                           auth=self.client_auth,
                           data=self.post_data,
                           headers=self.headers).json()
         
        self.ACCESS_TOKEN = self.token_req['access_token']

    def get_posts(self, sub):
        endpoint_url = self.build_request(['r', sub, 'new.json?sort=new'])
        return self.execute(endpoint_url)
    
    def get_hot_posts(self, sub):
        endpoint_url = self.build_request(['r', sub, 'hot.json'])
        return self.execute(endpoint_url)

    def get_comments(self, sub):
        endpoint_url = self.build_request(['r', sub, 'comments.json'])
        return self.execute(endpoint_url)
    
    def get_one_post(self, sub, tag, title):
        endpoint_url = self.build_request(['r', sub, 'comments', tag, title, '.json'])
        return self.execute(endpoint_url)
    
    def get_one_post_by_url(self, url):
        return self.execute(self.BASE_API_URL + url + '.json')

    def execute(self, endpoint_url):
        return requests.get(endpoint_url,
                            headers={'Authorization': 'Bearer {}'.format(self.ACCESS_TOKEN),
                                     'User-Agent': self.USER_AGENT},).json()
                            #params={'limit': '1'}).json()
    
    def build_request(self, endpoint_pieces):
        endpoint_url = '/'.join([self.BASE_API_URL] + endpoint_pieces)
        return endpoint_url
    
# test to ensure client still works
if __name__ == "__main__":
    client = Client()
    print(client.get_posts('destiny'))
    print(client.get_comments('destiny'))

# if __name__ == "__main__":
#     client = Client()
