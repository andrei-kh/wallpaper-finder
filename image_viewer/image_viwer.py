from image_viwer_base import ImageViewerBase

from PyQt5.QtWidgets import QApplication

from typing import Optional
import sys


def suppress_qt_warnings():
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"


class ImageViewer:

    def __init__(self, pathsToImages=list(), imagePickerToggle=False) -> None:
        """
        Wrapper for ImageViwerBase.
        """
        suppress_qt_warnings()

        self.app = QApplication(sys.argv)

        self.imageViewerBase = ImageViewerBase(pathsToImages=pathsToImages, imagePickerToggle=imagePickerToggle)

    def run(self) -> Optional[list]:
        """
        Runs image viwer.
        """
        self.imageViewerBase.show()
        self.app.exec()

        return sorted(list(self.imageViewerBase.pickedImages))


if __name__ == '__main__':
    try:
        import os
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test')
        images = [os.path.join(dir_path, p) for p in os.listdir(dir_path)]
        imageViewer = ImageViewer(images, True)

        print(imageViewer.run())
    except FileNotFoundError as e:
        print(f"! Probably you need to create '{dir_path}' folder and add some pictures there", end='\n\n')
        raise e
    except BaseException as e:
        print("( ͡• ͜ʖ ͡• )")
        raise e
