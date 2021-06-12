import praw

from PIL import Image, ImageChops

import json

import os
import shutil

from urllib.parse import urlparse
import requests

from progress.bar import Bar, PixelBar

from typing import Optional

import argparse

from image_viewer import ImageViewer

USER_AGENT = "Wallpaper finder"
SETTINGS_PATH = "./settings.json"


class RedditPicturesTest:
    def __init__(self, credentials, save_folder, temp_folder="temp",
                 subreddits=["wallpaper"], sort_type="top", limit=10,
                 time_filter="month", remove_duplicates=False, use_api=False) -> None:
        """
        Used to parse and save images from reddit.
        """
        self.temp_folder_path = temp_folder
        if not os.path.isdir(self.temp_folder_path):
            os.mkdir(self.temp_folder_path)

        self.save_folder = save_folder

        self.check_for_duplicates = remove_duplicates
        self.use_api = use_api

        self.reddit = praw.Reddit(client_id=credentials['client_id'],
                                  client_secret=credentials['api_key'],
                                  password=credentials['password'],
                                  user_agent=USER_AGENT,
                                  username=credentials['username'])

        self.allowed_extensions = ["png", "jpg", "jpeg"]

        self.subreddits = subreddits
        self.sort_type = sort_type
        self.limit = limit
        self.time_filter = time_filter

    def save_image_from_url(self, url, name) -> None:
        """
        Saves image.
        """
        image = Image.open(requests.get(url, stream=True).raw)
        image.save(os.path.join(self.temp_folder_path, name), icc_profile='')

    def process_image_url(self, image_url) -> bool:
        """
        Checks if images has valid extension and saves it.
        """
        image_name = urlparse(image_url).path.split('/')[-1]

        if image_name.split('.')[-1] in self.allowed_extensions:
            self.save_image_from_url(image_url, image_name)
            return True

        return False

    def process_gallery(self, submission) -> None:
        """
        Procceses the pictures in gallery.
        """
        gallery_items = list(submission.gallery_data['items'])
        media_metadata = submission.media_metadata

        for item in gallery_items:
            image_url = media_metadata[item['media_id']]['s']['u']
            self.process_image_url(image_url)

    def get_submissions_api(self, subreddit_name) -> Optional["praw.models.listing.generator.ListingGenerator"]:
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

    def get_subreddit_no_api(self, subbreddit_name) -> dict:
        """
        Gets subreddit from 'subreddit_name' without using praw.
        """
        base_url = f"https://www.reddit.com/r/{subbreddit_name}/{self.sort_type}.json?limit={self.limit}"

        if self.sort_type == "top":
            base_url += f"&t={self.time_filter}"

        request = requests.get(base_url, headers={'User-agent': USER_AGENT})

        return request.json()

    def get_submissions_no_api(self, subbreddit_name) -> list:
        """
        Gets submissions from 'subreddit_name' without using praw.
        """
        subreddit = self.get_subreddit_no_api(subbreddit_name)

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

    def get_submissions(self, subbreddit_name) -> Optional[list]:
        """
        Gets 'self.limit' submissions from 'subreddit_name'.
        """
        if self.use_api:
            return self.get_submissions_api(subbreddit_name)
        else:
            return self.get_submissions_no_api(subbreddit_name)

    def load_pictures(self, subreddits) -> None:
        """
        Loads images from subreddits.
        """
        for subreddit in subreddits:
            submissions = self.get_submissions(subreddit)

            progress_bar = Bar(f"Loaded images from r/{subreddit}:", max=self.limit)

            for submission in submissions:
                if not self.process_image_url(submission.url):
                    try:
                        if submission.is_gallery:
                            self.process_gallery(submission)
                    except AttributeError:
                        print("\nsubmission:"
                              "\n{}\n"
                              "dosen't have images with allowed extentions\n".format(submission.url))

                progress_bar.next()

            progress_bar.finish()

    def clear_folder(self, folder_path) -> None:
        """
        Clears 'folder_path'.
        """
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def get_files_from_folder(self, folder_path) -> list:
        """
        Returns list of filepaths to files in 'folder_path'.
        """
        files = []

        for name in os.listdir(folder_path):
            full_path = os.path.join(folder_path, name)

            if os.path.isfile(full_path):
                files.append(full_path)

        return files

    def move_images(self, paths, folder) -> None:
        """
        Moves images with 'paths' to 'folder'.
        """
        # for already existing files
        files_existed = []

        if paths:
            progress_bar = Bar("Moving picked images: ", fill="=", max=len(paths), bar_prefix="[", bar_suffix="]")

            for path in paths:
                try:
                    file_name = os.path.basename(path)

                    destination = os.path.join(folder, file_name)

                    os.rename(path, destination)

                    progress_bar.next()
                except FileExistsError:
                    files_existed.append(path)
                    progress_bar.next()
                    continue

            progress_bar.finish()

            # if we got already existing files -> print them
            if files_existed:
                for path in files_existed:
                    print(f"File {path} already exists. Did not move.")

    def remove_duplicates(self, images, folder) -> list:
        """
        Returns list of paths without imagess from 'folder'.
        """
        bar_lenght = len(images)
        progress_bar = PixelBar("Checking if duplicated:", max=bar_lenght)

        duplicates = []
        for image_path in images:
            image = Image.open(image_path)

            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                s_image = Image.open(file_path)

                try:
                    diff = ImageChops.difference(image, s_image)
                except ValueError:
                    continue

                if not diff.getbbox():
                    duplicates.append((image_path, file_path))
                    break

            progress_bar.next()

        print()
        for duplicate, original in duplicates:
            print("{} is a duplicate of {}".format(os.path.basename(duplicate), original))

        duplicates = [dup for dup, _ in duplicates]
        return [im for im in images if im not in duplicates]

    def run(self) -> None:
        """
        Driver code.
        """

        self.clear_folder(self.temp_folder_path)

        self.load_pictures(self.subreddits)

        image_paths = self.get_files_from_folder(self.temp_folder_path)
        imageViewer = ImageViewer(image_paths, True)

        chosen_images = imageViewer.run()

        if self.check_for_duplicates and chosen_images:
            images_to_save = self.remove_duplicates(chosen_images, self.save_folder)

            self.move_images(images_to_save, self.save_folder)
        else:
            self.move_images(chosen_images, self.save_folder)

        self.clear_folder(self.temp_folder_path)


def arguments() -> dict:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--subreddits",
        type=str,
        default=None,
        nargs="+",
        help="Images would be parsed from these."
    )

    parser.add_argument(
        "-st",
        "--sort-type",
        metavar="TYPE",
        type=str,
        default=None,
        nargs='?',
        help="Sort type. Can be hot, new, top, rising."
    )

    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=None,
        nargs='?',
        help="How many images would be parsed."
    )

    parser.add_argument(
        "-tf",
        "--time-filter",
        type=str,
        default=None,
        nargs='?',
        help="Only with sort-type top. Top from day, week, month, year or all."
    )

    parser.add_argument(
        "-rd",
        "--remove-duplicates",
        action="store_true",
        default=None,
        dest="remove_duplicates",
        help="If present script would not save duplicates of images in save-folder. "
        "If you have a lot of images you will die before it finishes."
    )

    parser.add_argument(
        "-ua",
        "--use-api",
        action="store_true",
        default=None,
        dest="use_api",
        help="If present script would use 'praw' to parse reddit. Needs 'credentials.json' to be present."
    )

    parser.add_argument(
        "--credentials",
        metavar="PATH",
        dest="credentials_path",
        type=str,
        default=None,
        nargs='?',
        help="Folder with credentials.json."
    )

    parser.add_argument(
        "--save-folder",
        dest="save_folder_path",
        metavar="PATH",
        type=str,
        default=None,
        nargs='?',
        help="Folder where immages would be saved."
    )

    parser.add_argument(
        "--temp-folder",
        dest="temp_folder_path",
        metavar="PATH",
        type=str,
        default=None,
        nargs='?',
        help="Temporary folder to save images. WARNING: TEMPORARY FOLDER WOULD BE CLEARED!!!"
    )

    args = parser.parse_args()

    return vars(args)


if __name__ == "__main__":
    args = arguments()
    print("Starting...")

    with open(SETTINGS_PATH) as f:
        settings = json.load(f)

    for k, v in args.items():
        if v is not None:
            settings[k] = v

    with open(settings["credentials_path"]) as f:
        credentials = json.load(f)

    redditPictures = RedditPicturesTest(credentials=credentials,
                                        save_folder=settings["save_folder_path"],
                                        temp_folder=settings["temp_folder_path"],
                                        subreddits=settings["subreddits"],
                                        sort_type=settings["sort_type"],
                                        limit=settings["limit"],
                                        time_filter=settings["time_filter"],
                                        remove_duplicates=settings["remove_duplicates"],
                                        use_api=settings["use_api"])
    redditPictures.run()

    print("Done...")
