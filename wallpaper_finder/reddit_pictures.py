from .reddit_pictures_base import RedditPicturesBase

import requests
import argparse

USER_AGENT = "Wallpaper finder"


class RedditPictures(RedditPicturesBase):
    def __init__(self, save_folder, temp_folder,
                 subreddits=["wallpaper"], sort_type="top", limit=10,
                 time_filter="month") -> None:
        """
        Used to parse and save images from reddit using 'praw' api.
        """
        super().__init__(save_folder, temp_folder, subreddits,
                         sort_type, limit, time_filter)

    def get_subreddit(self, subbreddit_name) -> dict:
        """
        Gets subreddit from 'subreddit_name' without using praw.
        """
        base_url = f"https://www.reddit.com/r/{subbreddit_name}/{self.sort_type}.json?limit={self.limit}"

        if self.sort_type == "top":
            base_url += f"&t={self.time_filter}"

        request = requests.get(base_url, headers={'User-agent': USER_AGENT})

        return request.json()

    def get_submissions(self, subbreddit_name) -> list:
        """
        Gets submissions from 'subreddit_name' without using praw.
        """
        subreddit = self.get_subreddit(subbreddit_name)

        submissions = []
        for post in subreddit['data']['children']:
            submission = argparse.Namespace()
            submission.url = post['data']['url']
            submission.is_gallery = post['data'].get('is_gallery', False)

            if submission.is_gallery:
                submission.gallery_data = post['data']['gallery_data']
                submission.media_metadata = post['data']['media_metadata']

            submissions.append(submission)

        return submissions
