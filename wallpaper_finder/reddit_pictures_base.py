from __future__ import with_statement
from PIL import Image, UnidentifiedImageError

from urllib.parse import urlparse

import warnings

from alive_progress.core.progress import alive_bar

from .utils import FileUtils


class RedditPicturesLoaderBase:
    def __init__(self, subreddits, sort_type, limit, time_filter) -> None:
        """
        Base class to parse images from reddit.
        """
        self.subreddits = subreddits
        self.sort_type = sort_type
        self.limit = limit
        self.time_filter = time_filter

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

        try:
            FileUtils.save_image_from_url(image_url, image_name)
            return True
        except ValueError:
            return False

    def get_submissions(self, subreddit_name) -> None:
        return None

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

    def load_pictures(self, subreddits, verbose=False) -> None:
        """
        Loads images from subreddits.
        """
        warnings.simplefilter("error", Image.DecompressionBombWarning)

        errors = []
        for subreddit in subreddits:
            submissions = self.get_submissions(subreddit)

            with alive_bar(self.limit, title=f"Loaded images from r/{subreddit}:", bar="classic2") as bar:
                for submission in submissions:
                    try:
                        if not self.process_image_url(submission.url):
                            if submission.is_gallery:
                                self.process_gallery(submission)
                    except (AttributeError, OSError, Image.DecompressionBombWarning):
                        errors.append(submission.url)
                    except UnidentifiedImageError as e:
                        print("oh no ( ͡• ͜ʖ ͡• )")
                        raise e

                    bar()

        if verbose:
            if errors:
                print("Can't load this files:")
                for error in errors:
                    print(error)
