from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QImage, QPixmap

from .initializer import Config

from typing import Optional


class ImageGraphicsView(QGraphicsView):
    """
    Class that displays the pictures.
    """

    def __init__(self) -> None:
        """
        GraphicsView that diplays pictures.
        """
        QGraphicsView.__init__(self)

        # Setting style sheet
        self.setStyleSheet(Config.IMAGE_GRAPHICS_STYLE_SHEET)

        # Image is displayed here.
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Image aspect ratio mode.
        self.aspectRatioMode = Qt.KeepAspectRatio

        # Scroll bar policy: no scroll bar.
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Current image pixelmap.
        self._pixmapHandle = None

# Image Displaying

    def hasImage(self) -> bool:
        """
        Checks if image is shown.
        """
        return self._pixmapHandle is not None

    def clearImage(self) -> None:
        """
        Clears displayed image.
        """
        if self.hasImage():
            self.scene.removeItem(self._pixmapHandle)
            self._pixmapHandle = None

    def updateView(self) -> None:
        """
        Updates image size to fit the scene.
        """
        if not self.hasImage():
            return

        self.fitInView(self.sceneRect(), self.aspectRatioMode)

    def setImage(self, image: QImage) -> None:
        """
        Sets scene image.
        """
        pixmap = QPixmap.fromImage(image)
        self.setSceneRect(0, 0, pixmap.width(), pixmap.height())

        if self.hasImage():
            self._pixmapHandle.setPixmap(pixmap)
        else:
            self._pixmapHandle = self.scene.addPixmap(pixmap)

        self.updateView()

    def getPixmapSize(self) -> Optional[tuple]:
        """
        Returns current image size.
        """
        if self.hasImage():
            w = self._pixmapHandle.pixmap().size().width()
            h = self._pixmapHandle.pixmap().size().height()
            return w, h

        return None
