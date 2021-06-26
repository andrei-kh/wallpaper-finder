import os

from alive_progress import alive_bar

from PIL import Image, UnidentifiedImageError

import requests

from uuid import uuid4

from typing import Tuple


class FileUtils:
    allowed_extensions = [".png", ".jpg", ".jpeg", ".bmp"]
    temp_folder_path = "./temp"
    save_folder_path = "./saved"
    number_of_threads = 4

    @classmethod
    def set_extensions(cls, extensions: list) -> None:
        """
        Sets allowed image extensions.
        """
        for ext in extensions:
            ext_, _ = os.path.splitext(ext)

            if ext_ != ext:
                raise ValueError("Passed invalid extension")

        cls.allowed_extensions = extensions

    @classmethod
    def set_temp_folder_path(cls, path: str) -> None:
        """
        Sets temp folder path.
        """
        if not os.path.isdir(path):
            os.mkdir(path)

        cls.temp_folder_path = path

    @classmethod
    def set_save_folder_path(cls, path: str) -> None:
        """
        Sets save folder path.
        """
        if not os.path.isdir(path):
            os.mkdir(path)

        cls.save_folder_path = path

    @classmethod
    def set_number_of_threads(cls, num: int) -> None:
        """
        Sets number of threads for loading.
        """

        cls.number_of_threads = num

    @classmethod
    def get_images_from_folder(cls, folder_path: str) -> list:
        """
        Returns list of paths to images that have 'ALOWED_EXTENSION' in 'folder_path'.
        """
        folder_images = []
        for filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, filename)

            if os.path.splitext(image_path)[1] in cls.allowed_extensions:
                folder_images.append(image_path)

        return folder_images

    def ahash(image_path: str, hashSize: int = 10) -> str:
        """
        Calculates aproximate hash of image at 'image_path'.
        """
        image = Image.open(image_path).resize((hashSize, hashSize), Image.ANTIALIAS)
        image = image.convert("L")

        pixel_values = list(image.getdata())
        avg_px_val = sum(pixel_values) / len(pixel_values)

        bits = "".join(['1' if (px > avg_px_val) else "0" for px in pixel_values])

        return hex(int(bits, 2))[2:]

    @classmethod
    def calculate_hashes(cls, images: list) -> Tuple[dict, list]:
        """
        Calculates hashes and finds duplicates of files in 'images'.
        """
        duplicates = []
        hashes = {}

        if images:
            with alive_bar(len(images), bar="filling", spinner="dots_reverse") as bar:
                for image in images:
                    try:
                        image_hash = cls.ahash(image)

                        if hashes.get(image_hash):
                            duplicates.append((image, hashes[image_hash], ))
                        else:
                            hashes[image_hash] = image

                    except UnidentifiedImageError:
                        duplicates.append((image, None))

                    bar()

        return hashes, duplicates

    def print_duplicates(duplicates: list, string: str) -> None:
        """
        Prints 'string' then "dup is a duplicate of orig" for dup, orig from 'duplicates'.
        """
        if duplicates:
            print(string)

            for dup, orig in duplicates:
                print("{} is a duplicate of {}".format(dup, orig))

            print()

    @classmethod
    def find_duplicates(cls, image_paths: list, folder: str,
                        string: str = "Image Paths", verbose=False) -> Tuple[list, list]:
        """
        Returns list of paths from image_paths without images from 'folder2'.

        Image paths are displayed as 'string'. For example: Finding duplicates in 'string':.
        """
        folder_images = cls.get_images_from_folder(folder)

        folder_name = os.path.basename(folder)

        if image_paths:
            print("Finding duplicates in '{}':".format(string))
        f1_hashes, f1_duplicates = cls.calculate_hashes(image_paths)

        if folder_images:
            print("Finding duplicates in '{}':".format(folder_name))
        f2_hashes, f2_duplicates = cls.calculate_hashes(folder_images)

        result = []
        duplicates = []
        print("Finding duplicates of '{}/*' in '{}'".format(string, folder_name))
        with alive_bar(len(f1_hashes), bar="filling", spinner='dots_reverse') as bar:
            for im_hash in f1_hashes:
                if f2_hashes.get(im_hash):
                    duplicates.append((f1_hashes[im_hash], f2_hashes[im_hash]))
                else:
                    result.append(f1_hashes[im_hash])
                bar()

        print()
        if verbose:
            string_ = "Duplicates in '{}':".format(string)
            cls.print_duplicates(f1_duplicates, string_)

            string_ = "Duplicates in '{}':".format(folder_name)
            cls.print_duplicates(f2_duplicates, string_)

            string_ = "Duplicates of '{}/*' in '{}'".format(string_, folder_name)
            cls.print_duplicates(duplicates, string_)

        duplicates = [e[0] for e in duplicates + f1_duplicates]
        return result, duplicates

    @classmethod
    def save_image_from_url(cls, url: str, name: str) -> str:
        """
        Saves image located at 'url'.
        """
        if os.path.splitext(name)[1] not in cls.allowed_extensions:
            raise ValueError("Invalid extension to save")

        try:
            raw_responce = requests.get(url, stream=True).raw
        except requests.ConnectionError:
            raise ValueError("Failed to establish connection to url.")

        image = Image.open(raw_responce)

        file_path = os.path.join(cls.temp_folder_path, name)
        if os.path.isfile(file_path):
            new_name = str(uuid4()) + "-" + name
            file_path = os.path.join(cls.temp_folder_path, new_name)

        try:
            image.save(file_path, icc_profile='', quality=95, subsampling=0)

            return file_path
        except OSError:
            image.convert("RGB").save(file_path, icc_profile='', quality=95, subsampling=0)

            return file_path
        except BaseException as e:
            if os.path.isfile(file_path):
                os.unlink(file_path)

            raise e

    def remove_files(to_remove: list) -> None:
        """
        Removes files in 'to_remove'.
        """
        for file_path in to_remove:
            try:
                os.unlink(file_path)
            except FileNotFoundError:
                continue

    def move_images(paths: list, folder: str, verbose: bool = False) -> list:
        """
        Moves images with 'paths' to 'folder'.
        """
        # for already existing files
        files_existed = []

        if paths:
            print("Moving images: ")
            with alive_bar(len(paths), bar="classic", spinner="dots_recur") as bar:

                for path in paths:
                    try:
                        file_name = os.path.basename(path)

                        destination = os.path.join(folder, file_name)

                        os.rename(path, destination)

                    except FileExistsError:
                        files_existed.append(path)

                    bar()

            print()
            if verbose:
                # if we got already existing files -> print them
                if files_existed:
                    for path in files_existed:
                        print(f"File {path} already exists. Did not move.")
                    print()

        return files_existed
