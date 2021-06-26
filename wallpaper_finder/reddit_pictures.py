from .utils import FileUtils

from multiprocessing.pool import ThreadPool
from functools import partial

import requests
from urllib.parse import ParseResult, urlparse

from os.path import basename, splitext

from alive_progress import alive_bar

import warnings
from PIL.Image import DecompressionBombWarning
from PIL import UnidentifiedImageError

from typing import Callable


class RedditPicturesLoader():
    def __init__(self, subreddits: list = ["wallpaper"], sort_type: str = "top",
                 limit: int = 10, time_filter: str = "month") -> None:
        """
        Used to parse and save images from reddit.

        subreddits: subreddits from which images are parsed.
        sort_type: "hot", "new", "top", "rising".
        limit: how much submissions to parse.
        time_filter: "day", "week", "month", "year", "all".
        """
        self.subreddits = subreddits
        self.sort_type = sort_type
        self.limit = limit
        self.time_filter = time_filter

        self.errors = []

    def get_user_agent(self) -> str:
        return "Wallpaper finder"

    def get_headers(self) -> dict:
        return {'User-agent': self.get_user_agent()}

    def make_request_url(self, subreddit_name: str) -> str:
        return f"https://www.reddit.com/r/{subreddit_name}/{self.sort_type}.json"

    def get_json_submissions(self, subreddit_name: str, limit: int, after: str = "null") -> dict:
        """
        Gets submissions from 'subreddit_name' in a form of json.
        """
        url = self.make_request_url(subreddit_name)

        params = {"raw_json": "1",
                  "show": "all",
                  "t": self.time_filter,
                  "limit": limit,
                  "after": after}

        request = requests.get(url,
                               headers=self.get_headers(),
                               params=params)

        return request.json()

    def __proccess_metadata(self, media_metadata: dict) -> list:
        image_urls = []

        for media_id in media_metadata:
            _, image_ext = media_metadata[media_id]['m'].split('/')

            image_url = f"https://i.redd.it/{media_id}.{image_ext}"
            image_urls.append(image_url)

        return image_urls

    def process_imgur_url(self, url: ParseResult) -> str:
        if "/a/" in url.path or "/gallery/" in url.path:
            raise TypeError("Imgur gallery.")

        url = url._replace(netloc="i.imgur.com")

        _, file_ext = splitext(url.path)

        if file_ext not in FileUtils.allowed_extensions:
            url = url._replace(path=url.path + ".png")

        return url.geturl()

    def process_reddit_url(self, url: ParseResult, post: dict) -> list:
        if "/comments/" in url.path:
            if not post['data'].get('media_metadata'):
                raise TypeError("Plain Text.")

        if post['data'].get('crosspost_parent'):
            metadata = post['data']['crosspost_parent_list'][0]['media_metadata']
        else:
            metadata = post['data']['media_metadata']

        return self.__proccess_metadata(metadata)

    def extract_image_urls(self, json_submissions: dict) -> list:
        """
        Parses json for image download links.
        """
        image_urls = []

        for post in json_submissions['data']['children']:
            try:
                post_url = post['data']['url']

                parsed_url = urlparse(post_url)

                if post['data'].get('is_video') or "v." in parsed_url.netloc:
                    TypeError("It is a video.")

                # removes query from url
                parsed_url = parsed_url._replace(query="")

                if "i." in parsed_url.netloc and splitext(parsed_url.path)[1]:
                    image_urls.append(parsed_url.geturl())

                elif "imgur.com" in parsed_url.netloc:
                    image_urls.append(self.process_imgur_url(parsed_url))

                elif "reddit" in parsed_url.netloc:
                    image_urls += self.process_reddit_url(parsed_url, post)
                else:
                    raise TypeError("Unknown link.")

            except TypeError as e:
                self.errors.append(post_url + " -> " + str(e))

        return image_urls

    def __handle_submissions(self, subreddit_name: str, bar: Callable[[], None] = None) -> list:
        """
        Makes list of image urls adding them by a 100 because of request limitations.
        """
        image_urls = []

        after = "null"

        for limit in range(self.limit, 0, -100):
            request_limit = min(limit, 100)

            json_submissions = self.get_json_submissions(subreddit_name, request_limit, after)

            image_urls += self.extract_image_urls(json_submissions)

            after = json_submissions["data"]["after"]

            if after is None:
                break

            # verbose mode
            if bar:
                # done this percent of work
                bar(1 - limit / self.limit)
        # verbose mode
        if bar:
            bar(1)

        return image_urls

    def get_image_urls(self, subreddit_name: str, verbose: bool) -> list:
        try:
            if verbose:
                print(f"\nFetching urls from r/{subreddit_name}:")
                with alive_bar(bar="blocks", spinner="long_message", manual=True) as bar:
                    image_urls = self.__handle_submissions(subreddit_name, bar)

                print()
            else:
                image_urls = self.__handle_submissions(subreddit_name)
        except KeyError as e:
            print("Probably passed invalid parameter to 'sort_type' or 'time_filter'.")
            raise e

        if verbose:
            if self.limit != len(image_urls):
                print(f"Got {len(image_urls)} image urls\n")

        return image_urls

    def __process_submission(self, image_url: str, bar: Callable[[], None]) -> None:
        try:
            image_name = basename(image_url)

            file_path = FileUtils.save_image_from_url(image_url, image_name)

            self.loaded.append(file_path)
        except (DecompressionBombWarning, ValueError, UnidentifiedImageError) as e:
            self.errors.append(image_url + " -> " + str(e))

        bar()

    def load_pictures(self, subreddits: list, verbose: bool = False) -> list:
        # Treats Pictures with a lot of pixels as error.
        warnings.simplefilter("error", DecompressionBombWarning)

        self.loaded = []
        try:
            for subreddit in subreddits:
                image_urls = self.get_image_urls(subreddit, verbose)

                print(f"Loading images from r/{subreddit}:")
                with alive_bar(len(image_urls), bar="classic2") as bar:
                    part = partial(self.__process_submission, bar=bar)

                    with ThreadPool(FileUtils.number_of_threads) as pool:
                        pool.map(part, image_urls)

            print()
            if verbose:
                if self.errors:
                    print(f"Loaded only {len(self.loaded)} files...")
                    print("Can't load this files:")
                    for error in self.errors:
                        print(error)
                    print()

            return self.loaded

        except BaseException as e:
            print("oh no ( ͡• ͜ʖ ͡• )")
            FileUtils.remove_files(self.loaded)
            raise e
