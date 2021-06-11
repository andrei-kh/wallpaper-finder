import praw
import json
import os
import shutil

from PIL import Image

from urllib.parse import urlparse
import requests
from progress.bar import Bar
from typing import Optional

from image_viewer import ImageViewer

USER_AGENT = "Wallpaper finder"


# subreddit = reddit.subreddit('wallpaper')
# for i, submission in enumerate(subreddit.top('month', limit=4)):
#     url = submission.url
#     im = Image.open((requests.get(url, stream=True).raw))
#     im.save('pic' + str(i) + '.png')


class RedditPictures:
    def __init__(self) -> None:
        self.app_path = os.path.dirname(os.path.abspath(__file__))
        self.temp_folder_path = os.path.join(self.app_path, "temp")
        if not os.path.isdir(self.temp_folder_path):
            os.mkdir(self.temp_folder_path)

        self.save_folder = os.path.join(self.app_path, "test")

        params = self.load_json(".secret/credentials.json")
        self.reddit = praw.Reddit(client_id=params['client_id'],
                                  client_secret=params['api_key'],
                                  password=params['password'],
                                  user_agent=USER_AGENT,
                                  username=params['username'])

        self.subbreddits = ["wallpaper"]  # , "AMA"]
        self.allowed_extensions = ["png", "jpg", "jpeg"]
        self.sort_type = "top"  # hot new top rising
        self.limit = 10  # max maybe
        self.time_filter = "month"  # hour day week month year all

    def load_json(self, file_path) -> dict:
        with open(os.path.join(self.app_path, file_path)) as f:
            return json.load(f)

    def save_image(self, url, name) -> None:
        image = Image.open(requests.get(url, stream=True).raw)
        image.save(os.path.join(self.temp_folder_path, name), icc_profile='')

    def get_image_name(self, url) -> str:
        parsed = urlparse(url).path.split('/')
        return parsed[-1]

    def process_image_url(self, image_url) -> bool:
        image_name = self.get_image_name(image_url)

        if image_name.split('.')[-1] in self.allowed_extensions:
            self.save_image(image_url, image_name)
            return True

        return False

    def process_gallery(self, submission) -> None:
        gallery_items = list(submission.gallery_data['items'])
        media_metadata = submission.media_metadata

        for item in gallery_items:
            image_url = media_metadata[item['media_id']]['s']['u']
            self.process_image_url(image_url)

    def clear_folder(self, folder_path) -> None:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def get_submissions(self, subreddit_name) -> Optional[praw.models.listing.generator.ListingGenerator]:
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

    def load_pictures(self, subreddits) -> None:
        for subreddit in subreddits:
            submissions = self.get_submissions(subreddit)

            progress_bar = Bar(f"Loaded images from r/{subreddit}:", max=submissions.limit)

            for submission in submissions:
                if not self.process_image_url(submission.url):
                    try:
                        if submission.is_gallery:
                            self.process_gallery(submission)
                    except AttributeError:
                        print("submission:"
                              "\n{}\n"
                              "dosen't have images with allowed extentions\n".format(submission.url))

                progress_bar.next()

            progress_bar.finish()

    def get_files_from_folder(self, folder_path) -> list:
        files = []

        for name in os.listdir(folder_path):
            full_path = os.path.join(folder_path, name)

            if os.path.isfile(full_path):
                files.append(full_path)

        return files

    def move_images(self, paths, folder):
        for path in paths:
            file_name = os.path.basename(path)

            destination = os.path.join(folder, file_name)

            os.rename(path, destination)

    def run(self):
        self.load_pictures(self.subbreddits)

        image_paths = self.get_files_from_folder(self.temp_folder_path)
        imageViewer = ImageViewer(image_paths, True)

        images_to_save = imageViewer.run()
        self.move_images(images_to_save, "./saved")

        self.clear_folder(self.temp_folder_path)


if __name__ == "__main__":
    redditPictures = RedditPictures()
    redditPictures.run()
