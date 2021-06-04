from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QImage
from PyQt5.QtWidgets import (QMainWindow,
                             QShortcut,
                             QFileDialog,
                             QVBoxLayout,
                             QWidget)

from image_graphics_view import ImageGraphicsView
from bottom_bar_layout import BottomBarLayout
from settings import (MAIN_LAYOUT_MARGINS,
                      MAIN_LAYOUT_SPACING,
                      MAIN_WINDOW_STYLE_SHEET)

import os


class ImageViewerBase(QMainWindow):

    def __init__(self, pathsToImages=list(), imagePickerToggle=False) -> None:
        """
        Simple image viewer made with PyQt.

        """
        QMainWindow.__init__(self)

        # QGraphicsView to display images
        self.imageGraphicsView = ImageGraphicsView()

        # Bottom bar
        self.bottomBarLayout = BottomBarLayout()

        # Layout stuff
        self.mainWidget = QWidget(self)
        self.mainLayout = QVBoxLayout(self.mainWidget)
        self.mainLayout.setContentsMargins(*MAIN_LAYOUT_MARGINS)
        self.mainLayout.setSpacing(MAIN_LAYOUT_SPACING)
        self.mainLayout.addWidget(self.imageGraphicsView)
        self.mainLayout.addLayout(self.bottomBarLayout)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        # Image picker enabled/disabled
        self.pickedImages = set() if imagePickerToggle else None

        # Window border style
        self.centralWidget().setAttribute(Qt.WA_TransparentForMouseEvents)

        # For mouse draging
        self.setMouseTracking(True)
        self.old_pos = None

        # Removes window title bar.
        self.setWindowFlags(Qt.CustomizeWindowHint)

        # Styles(borders, background).
        self.setStyleSheet(MAIN_WINDOW_STYLE_SHEET)

        # All button actions
        self.createShortcuts()

        # Sets first image
        self.setImagePaths(pathsToImages)

    def createShortcuts(self) -> None:
        """
        Initializes all shotcuts.

        """
        # Close shortcuts
        self.escCloseShortcut = QShortcut(QKeySequence('Esc'), self)
        self.escCloseShortcut.activated.connect(self.close)

        self.ctrlQCloseShortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.ctrlQCloseShortcut.activated.connect(self.close)

        # Image changing shortcuts
        self.leftPreviousImage = QShortcut(QKeySequence('Left'), self)
        self.leftPreviousImage.activated.connect(self.previousImage)

        self.rightNextImage = QShortcut(QKeySequence('Right'), self)
        self.rightNextImage.activated.connect(self.nextImage)

        # Open files shortcut
        self.ctrlOLoadImage = QShortcut(QKeySequence('Ctrl+O'), self)
        self.ctrlOLoadImage.activated.connect(self.setImagePaths)

        # Maximized screen shortcut
        self.superUpMaximize = QShortcut(QKeySequence("Ctrl+F"), self)
        self.superUpMaximize.activated.connect(self.showMaximized)

        # Picker shortcuts
        self.altXPick = QShortcut(QKeySequence('Alt+X'), self)

        if self.usingPicker():
            self.altXPick.activated.connect(self.tickCurrentImage)

# Image loading and setting

    def getCurrentImagePath(self) -> None:
        return self.pathsToImages[self.currentImageIndex]

    def loadImageFromFile(self, filePath=None) -> None:
        if not os.path.isfile(filePath):
            raise FileNotFoundError

        image = QImage(filePath)
        self.imageGraphicsView.setImage(image)

    def setLoadedImage(self) -> None:
        self.imageGraphicsView.clearImage()

        filePath = self.getCurrentImagePath()
        self.updateStatusBarLabel(filePath)

        if self.usingPicker():
            self.updatePickerBar()

        self.loadImageFromFile(filePath)

    def setImagePaths(self, filePaths=None) -> None:
        if filePaths is None:
            filePaths, _ = QFileDialog.getOpenFileNames(self, "Open image files.")

        self.pathsToImages = filePaths
        self.totalImages = len(filePaths)
        self.currentImageIndex = 0

        self.setLoadedImage()

# Changing Image

    def nextImage(self) -> None:
        if self.totalImages > 1:
            self.currentImageIndex = (self.currentImageIndex + 1) % self.totalImages
            self.setLoadedImage()

    def previousImage(self) -> None:
        if self.totalImages > 1:
            self.currentImageIndex = (self.currentImageIndex - 1) % self.totalImages
            self.setLoadedImage()

    def updateStatusBarLabel(self, imagePath) -> None:
        filename = os.path.split(imagePath)[-1]
        text = f"{self.currentImageIndex + 1}/{self.totalImages} | {filename}"
        self.bottomBarLayout.changeStatus(text)

# Image Picking

    def usingPicker(self) -> bool:
        return self.pickedImages is not None

    def imageIsPicked(self, imagePath) -> bool:
        return imagePath in self.pickedImages

    def updatePickerBar(self) -> None:
        if self.imageIsPicked(self.getCurrentImagePath()):
            self.bottomBarLayout.setPickerAsPicked()
        else:
            self.bottomBarLayout.setPickerAsUnPicked()

    def tickCurrentImage(self) -> None:
        currentImagePath = self.getCurrentImagePath()

        if self.imageIsPicked(currentImagePath):
            self.pickedImages.remove(currentImagePath)
        else:
            self.pickedImages.add(currentImagePath)

        self.updatePickerBar()

# Events

    def resizeEvent(self, event) -> None:
        self.imageGraphicsView.updateView()
        return super().resizeEvent(event)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.old_pos = event.pos()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None
        return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if not self.old_pos:
            return
        delta = event.pos() - self.old_pos
        self.move(self.pos() + delta)
        return super().mouseMoveEvent(event)
