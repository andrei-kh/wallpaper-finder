import os
from alive_progress import alive_bar
from PIL import Image
from typing import Tuple
import requests


class FileUtils:
    allowed_extensions = [".png", ".jpg", ".jpeg", ".bmp"]
    temp_folder_path = "./temp"
    save_folder_path = "./saved"

    @classmethod
    def set_extensions(cls, extensions) -> None:
        """
        Sets allowed image extensions.
        """
        for ext in extensions:
            ext_, _ = os.path.splitext(ext)

            if ext_ != ext:
                raise ValueError("Passed invalid extension")

        cls.allowed_extensions = extensions

    @classmethod
    def set_temp_folder_path(cls, path) -> None:
        """
        Sets temp folder path.
        """
        if not os.path.isdir(path):
            os.mkdir(path)

        cls.temp_folder_path = path

    @classmethod
    def set_save_folder_path(cls, path) -> None:
        """
        Sets save folder path.
        """
        if not os.path.isdir(path):
            os.mkdir(path)

        cls.save_folder_path = path

    @classmethod
    def get_images_from_folder(cls, folder_path) -> list:
        """
        Returns list of paths to images that have 'ALOWED_EXTENSION' in 'folder_path'.
        """
        folder_images = []
        for filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, filename)

            if os.path.splitext(image_path)[1] in cls.allowed_extensions:
                folder_images.append(image_path)

        return folder_images

    def ahash(image_path, hashSize=10) -> str:
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
    def calculate_hashes(cls, images) -> Tuple[dict, list]:
        """
        Calculates hashes and finds duplicates of files in 'images'.
        """
        duplicates = []
        hashes = {}

        with alive_bar(len(images), bar="filling", spinner="dots_reverse") as bar:
            for image in images:
                image_hash = cls.ahash(image)

                if hashes.get(image_hash):
                    duplicates.append((hashes[image_hash], image))
                else:
                    hashes[image_hash] = image

                bar()

        return hashes, duplicates

    def print_duplicates(duplicates, string) -> None:
        """
        Prints list of duplicates.
        """
        if duplicates:
            print(string)

            for dup, orig in duplicates:
                print("{} is a duplicate of {}".format(dup, orig))

            print()

    @classmethod
    def find_duplicates(cls, folder1, folder2, verbose=False) -> Tuple[list, list]:
        """
        Returns list of paths from 'folder1' without images from 'folder2'.
        """
        folder1_images = cls.get_images_from_folder(folder1)
        folder2_images = cls.get_images_from_folder(folder2)

        folder1_name = os.path.basename(folder1)
        folder2_name = os.path.basename(folder2)

        print("Finding duplicates in '{}':".format(folder1_name))
        f1_hashes, f1_duplicates = cls.calculate_hashes(folder1_images)

        print("Finding duplicates in '{}':".format(folder2_name))
        f2_hashes, f2_duplicates = cls.calculate_hashes(folder2_images)

        result = []
        duplicates = []
        print("Finding duplicates of '{}/*' in '{}'".format(folder1_name, folder2_name))
        with alive_bar(len(f1_hashes), bar="filling", spinner='dots_reverse') as bar:
            for im_hash in f1_hashes:
                if f2_hashes.get(im_hash):
                    duplicates.append((f1_hashes[im_hash], f2_hashes[im_hash]))
                else:
                    result.append(f1_hashes[im_hash])
                bar()

        if verbose:
            print()
            string = "Duplicates in '{}':".format(folder1_name)
            cls.print_duplicates(f1_duplicates, string)

            string = "Duplicates in '{}':".format(folder2_name)
            cls.print_duplicates(f2_duplicates, string)

            string = "Duplicates of '{}/*' in '{}'".format(folder1_name, folder2_name)
            cls.print_duplicates(duplicates, string)

        duplicates = [e[0] for e in duplicates + f1_duplicates]
        return result, duplicates

    @classmethod
    def save_image_from_url(cls, url, name) -> None:
        """
        Saves image.
        """
        if os.path.splitext(name)[1] not in cls.allowed_extensions:
            raise ValueError("Invalid extension to save")

        image = Image.open(requests.get(url, stream=True).raw)

        file_path = os.path.join(cls.temp_folder_path, name)
        while os.path.isfile(file_path):
            file_path = os.path.join(cls.temp_folder_path, "new_" + name)

        image.save(file_path, icc_profile='', quality=95, subsampling=0)

    def remove_files(to_remove) -> None:
        """
        Removes files in 'to_remove'.
        """
        for file_path in to_remove:
            os.unlink(file_path)

    def move_images(paths, folder, verbose=False) -> list:
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

            if verbose:
                print()
                # if we got already existing files -> print them
                if files_existed:
                    for path in files_existed:
                        print(f"File {path} already exists. Did not move.")

        return files_existed
