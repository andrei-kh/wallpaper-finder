from image_viewer.image_viewer_base import ImageViewerBase

from PyQt5.QtWidgets import QApplication

import sys
import os

from typing import Optional


def suppress_qt_warnings():
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"


class ImageViewer:

    def __init__(self, pathsToImages: list = list(),
                 imagePickerToggle: bool = False) -> None:
        """
        Wrapper for ImageViwerBase.
        """
        suppress_qt_warnings()

        self.imagePickerToggle = imagePickerToggle
        self.pathsToImages = pathsToImages

        self.app = QApplication(sys.argv)

    def run(self) -> Optional[list]:
        """
        Runs image viwer.
        """
        while True:

            self.imageViewerBase = ImageViewerBase(
                pathsToImages=self.pathsToImages,
                imagePickerToggle=self.imagePickerToggle)
            self.imageViewerBase.show()

            if self.app.exec() != ImageViewerBase.EXIT_CODE_REBOOT:
                break

        if self.imagePickerToggle:
            return sorted(list(self.imageViewerBase.pickedImages))

        return None
