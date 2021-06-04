from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap

from settings import IMAGE_GRAPHICS_STYLE_SHEET


class ImageGraphicsView(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)

        # Setting style sheet
        self.setStyleSheet(IMAGE_GRAPHICS_STYLE_SHEET)

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

    def hasImage(self):
        """
        Chescks if image is shown.
        """
        return self._pixmapHandle is not None

    def clearImage(self):
        if self.hasImage():
            self.scene.removeItem(self._pixmapHandle)
            self._pixmapHandle = None

    def updateView(self):
        if not self.hasImage():
            return

        self.fitInView(self.sceneRect(), self.aspectRatioMode)

    def setImage(self, image):
        pixmap = QPixmap.fromImage(image)

        if self.hasImage():
            self._pixmapHandle.setPixmap(pixmap)
        else:
            self._pixmapHandle = self.scene.addPixmap(pixmap)

        self.updateView()
