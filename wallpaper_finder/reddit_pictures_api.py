import requests

from .reddit_pictures import RedditPicturesLoader


class RedditPicturesLoaderApi(RedditPicturesLoader):
    def __init__(self, credentials: dict,
                 subreddits: list = ["wallpaper"], sort_type: str = "top",
                 limit: int = 10, time_filter: str = "month") -> None:
        """
        Used to parse and save images with authorization to reddit api.

        credentials: reddit api credentials.
        subreddits: subreddits from which images are parsed.
        sort_type: "hot", "new", "top", "rising".
        limit: how much submissions to parse.
        time_filter: "day", "week", "month", "year", "all".
        """
        super().__init__(subreddits, sort_type, limit, time_filter)

        self.client_id = credentials["client_id"]
        self.client_secret = credentials["client_secret"]

        self.authorization = self.get_authorization()

    def get_authorization_url(self) -> str:
        return "https://www.reddit.com/api/v1/access_token"

    def get_authorization(self) -> str:
        """
        Authorizes in reddit api and returns authorization header.
        """
        post_data = {"grant_type": "client_credentials"}

        client_auth = requests.auth.HTTPBasicAuth(self.client_id,
                                                  self.client_secret)

        response = requests.post(self.get_authorization_url(),
                                 auth=client_auth,
                                 data=post_data,
                                 headers={"User-Agent": "Wallpaper finder"})

        r_json = response.json()

        return r_json["token_type"] + " " + r_json["access_token"]

    def get_headers(self) -> dict:
        headers = super().get_headers()

        headers["authorization"] = self.authorization

        return headers

    def make_request_url(self, subreddit_name: str) -> str:
        return f"https://oauth.reddit.com/r/{subreddit_name}/{self.sort_type}.json"
