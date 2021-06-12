import praw

from typing import Optional

from .reddit_pictures_base import RedditPicturesBase

USER_AGENT = "Wallpaper finder"


class RedditPicturesApi(RedditPicturesBase):
    def __init__(self, credentials, save_folder, temp_folder,
                 subreddits=["wallpaper"], sort_type="top", limit=10,
                 time_filter="month") -> None:
        """
        Used to parse and save images from reddit using 'praw' api.
        """
        super().__init__(save_folder, temp_folder, subreddits,
                         sort_type, limit, time_filter)
        try:
            self.reddit = praw.Reddit(client_id=credentials['client_id'],
                                      client_secret=credentials['api_key'],
                                      password=credentials['password'],
                                      user_agent=USER_AGENT,
                                      username=credentials['username'])
        except ImportError:
            print("To use api you need to install praw")

    def get_submissions(self, subreddit_name) -> Optional["praw.models.listing.generator.ListingGenerator"]:
        """
        Get submissions from 'subreddit_name' with praw.
        """

        subreddit = self.reddit.subreddit(subreddit_name)

        if self.sort_type == "top":
            return subreddit.top(self.time_filter, limit=self.limit)
        elif self.sort_type == "hot":
            return subreddit.hot(limit=self.limit)
        elif self.sort_type == "new":
            return subreddit.new(limit=self.limit)
        elif self.sort_type == "rising":
            return subreddit.rising(limit=self.limit)

        return None
