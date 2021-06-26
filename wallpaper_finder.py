import argparse
import json
import os

from wallpaper_finder import RedditPicturesLoader, RedditPicturesLoaderApi, FileUtils
from image_viewer import ImageViewer

SETTINGS_PATH = "./settings.json"


def arguments() -> dict:
    """
    Console arguments.
    """
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
        help="How many submissions would be parsed."
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
        help="If present script would not save duplicates of images in save-folder."
    )

    parser.add_argument(
        "-nt",
        "--number-of-threads",
        type=int,
        dest="number_of_threads",
        default=None,
        nargs='?',
        help="Number of threads to use for loading images."
    )

    parser.add_argument(
        "-ua",
        "--use-api",
        action="store_true",
        default=None,
        dest="use_api",
        help="If present script would connect to reddit api. Needs 'credentials.json' to be present."
    )

    parser.add_argument(
        "-ae",
        "--allowed-extensions",
        type=str,
        default=None,
        nargs="+",
        help="Images with only this extensions are allowed."
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
        help="Folder where images would be saved."
    )

    parser.add_argument(
        "--temp-folder",
        dest="temp_folder_path",
        metavar="PATH",
        type=str,
        default=None,
        nargs='?',
        help="Temporary folder to save images. "
        "WARNING: After finishing loaded pictures in this folder would be removed"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=None,
        dest="verbose",
        help="Makes everything more verbose."
    )

    args = parser.parse_args()

    return vars(args)


def main(r_parser: RedditPicturesLoader, remove_duplicates: bool, verbose: bool) -> None:
    image_paths = []
    try:
        image_paths = r_parser.load_pictures(r_parser.subreddits, verbose)

        imageViewer = ImageViewer(image_paths, True)

        images_to_save = imageViewer.run()

        images_to_remove = [im for im in image_paths if im not in images_to_save]

        if remove_duplicates and images_to_save:
            images_to_save, images_to_remove_ = FileUtils.find_duplicates(images_to_save,
                                                                          FileUtils.save_folder_path,
                                                                          os.path.basename(FileUtils.temp_folder_path),
                                                                          verbose)

            images_to_remove += images_to_remove_

        images_to_remove += FileUtils.move_images(images_to_save,
                                                  FileUtils.save_folder_path,
                                                  verbose)

        FileUtils.remove_files(images_to_remove)
    except (BaseException, KeyboardInterrupt) as e:
        FileUtils.remove_files(image_paths)
        raise e


if __name__ == "__main__":
    args = arguments()

    print("Starting...")

    with open(SETTINGS_PATH) as f:
        settings = json.load(f)

    for key in settings:
        if args.get(key) is not None:
            settings[key] = args[key]

    FileUtils.set_save_folder_path(settings["save_folder_path"])
    FileUtils.set_temp_folder_path(settings["temp_folder_path"])
    FileUtils.set_extensions(settings["allowed_extensions"])
    FileUtils.set_number_of_threads(settings["number_of_threads"])

    reddit_parser = None
    if settings["use_api"]:
        print("Getting api credentials...")
        with open(settings["credentials_path"]) as f:
            credentials = json.load(f)

        reddit_parser = RedditPicturesLoaderApi(
            credentials=credentials,
            subreddits=settings["subreddits"],
            sort_type=settings["sort_type"],
            limit=settings["limit"],
            time_filter=settings["time_filter"])

    else:
        reddit_parser = RedditPicturesLoader(
            subreddits=settings["subreddits"],
            sort_type=settings["sort_type"],
            limit=settings["limit"],
            time_filter=settings["time_filter"])

    main(reddit_parser, settings["remove_duplicates"], settings["verbose"])

    print("Done...")
