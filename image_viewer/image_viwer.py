from image_viwer_base import ImageViewerBase

from PyQt5.QtWidgets import QApplication

from sys import argv
from typing import Optional


class ImageViewer:
    def __init__(self, pathsToImages=list(), imagePickerToggle=False) -> None:
        """
        Wrapper for ImageViwerBase.
        """

        self.app = QApplication(argv)

        self.imageViewerBase = ImageViewerBase(pathsToImages=pathsToImages, imagePickerToggle=imagePickerToggle)

    def run(self) -> Optional[list]:
        self.imageViewerBase.show()
        self.app.exec()

        return sorted(list(self.imageViewerBase.pickedImages))


if __name__ == '__main__':
    import os
    images = [os.path.join('./.tmp/', p) for p in os.listdir('./.tmp/')]
    imageViewer = ImageViewer(images, True)

    print(imageViewer.run())
