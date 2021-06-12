import argparse
import json
import os

from wallpaper_finder import RedditPictures, RedditPicturesApi
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


def main(r_parser, remove_duplicates) -> None:
    """
    Driver code.
    """
    r_parser.clear_folder(r_parser.temp_folder_path)

    r_parser.load_pictures(r_parser.subreddits)

    image_paths = r_parser.get_files_from_folder(r_parser.temp_folder_path)
    imageViewer = ImageViewer(image_paths, True)

    chosen_images = imageViewer.run()

    if remove_duplicates and chosen_images:
        images_to_save = r_parser.remove_duplicates(chosen_images,
                                                    r_parser.save_folder)

        r_parser.move_images(images_to_save, r_parser.save_folder)
    else:
        r_parser.move_images(chosen_images, r_parser.save_folder)

    r_parser.clear_folder(r_parser.temp_folder_path)


if __name__ == "__main__":
    """
    Setings, arguments stuff.
    """
    args = arguments()

    print("Starting...")

    with open(SETTINGS_PATH) as f:
        settings = json.load(f)

    for key, value in args.items():
        if value is not None:
            settings[key] = value

    if not os.path.isdir(settings["temp_folder_path"]):
        os.mkdir(settings["temp_folder_path"])

    reddit_parser = None
    if settings["use_api"]:
        print("Getting api credentials...")
        with open(settings["credentials_path"]) as f:
            credentials = json.load(f)

        reddit_parser = RedditPicturesApi(credentials=credentials,
                                          save_folder=settings["save_folder_path"],
                                          temp_folder=settings["temp_folder_path"],
                                          subreddits=settings["subreddits"],
                                          sort_type=settings["sort_type"],
                                          limit=settings["limit"],
                                          time_filter=settings["time_filter"])

    else:
        reddit_parser = RedditPictures(save_folder=settings["save_folder_path"],
                                       temp_folder=settings["temp_folder_path"],
                                       subreddits=settings["subreddits"],
                                       sort_type=settings["sort_type"],
                                       limit=settings["limit"],
                                       time_filter=settings["time_filter"])

    main(reddit_parser, settings["remove_duplicates"])

    print("Done...")
