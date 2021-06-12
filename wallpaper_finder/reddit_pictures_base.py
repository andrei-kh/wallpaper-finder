from PIL import Image, ImageChops, UnidentifiedImageError

import requests
from urllib.parse import urlparse

from progress.bar import PixelBar, Bar

import os


class RedditPicturesBase:
    def __init__(self, save_folder, temp_folder, subreddits,
                 sort_type, limit, time_filter) -> None:
        """
        Base class to parse images from reddit.
        """
        self.temp_folder_path = temp_folder
        if not os.path.isdir(self.temp_folder_path):
            os.mkdir(self.temp_folder_path)

        self.save_folder = save_folder

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

        file_path = os.path.join(self.temp_folder_path, name)
        while os.path.isfile(file_path):
            file_path = os.path.join(self.temp_folder_path, "new_" + name)

        image.save(file_path, icc_profile='', quality=95, subsampling=0)

    def process_image_url(self, image_url) -> bool:
        """
        Checks if images has valid extension and saves it.
        """
        parsed_url = urlparse(image_url)

        if "imgur.com" == parsed_url.netloc:
            if "/a/" in image_url:
                return False

            image_url = image_url.replace("imgur", "i.imgur") + ".png"

        image_name = parsed_url.path.split('/')[-1]

        if image_name.split('.')[-1] in self.allowed_extensions:
            self.save_image_from_url(image_url, image_name)
            return True

        return False

    def get_submissions(self, subreddit_name) -> None:
        return None

    def load_pictures(self, subreddits) -> None:
        """
        Loads images from subreddits.
        """
        errors = []
        for subreddit in subreddits:
            submissions = self.get_submissions(subreddit)

            progress_bar = Bar(f"Loaded images from r/{subreddit}:", max=self.limit)

            for submission in submissions:
                try:
                    if not self.process_image_url(submission.url):
                        if submission.is_gallery:
                            self.process_gallery(submission)
                except (AttributeError, OSError):
                    errors.append(submission.url)
                except UnidentifiedImageError as e:
                    print("oh no ( ͡• ͜ʖ ͡• )")
                    raise e

                progress_bar.next()

            progress_bar.finish()

        if errors:
            print("Can't load this one's:")
            for error in errors:
                print(error)

    def process_gallery(self, submission) -> None:
        """
        Procceses the pictures in gallery.
        """
        gallery_items = list(submission.gallery_data['items'])
        media_metadata = submission.media_metadata

        for item in gallery_items:
            image_url = media_metadata[item['media_id']]['s']['u']

            # i don't know why
            image_url = image_url.replace('amp;', '')

            self.process_image_url(image_url)

    def remove_files(self, to_remove) -> None:
        """
        Removes files in 'to_remove'.
        """
        for file_path in to_remove:
            os.unlink(file_path)

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

    def move_images(self, paths, folder) -> list:
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

        return files_existed

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
