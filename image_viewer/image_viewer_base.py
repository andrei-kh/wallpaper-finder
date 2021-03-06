from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QImage
from PyQt5.QtWidgets import (QMainWindow,
                             QShortcut,
                             QFileDialog,
                             QVBoxLayout,
                             QWidget,
                             qApp)

from .image_graphics_view import ImageGraphicsView
from .bottom_bar_layout import BottomBarLayout
from .initializer import Config

import os


class ImageViewerBase(QMainWindow):
    EXIT_CODE_REBOOT = -80084

    def __init__(self, pathsToImages: list = list(), imagePickerToggle: bool = False) -> None:
        """
        Simple image viewer made with PyQt.

        """
        QMainWindow.__init__(self)

        # Loading settings from settings.json
        Config.apply_settings()

        # QGraphicsView to display images
        self.imageGraphicsView = ImageGraphicsView()

        # Bottom bar
        self.bottomBarLayout = BottomBarLayout()

        # Layout stuff
        self.mainWidget = QWidget(self)
        self.mainLayout = QVBoxLayout(self.mainWidget)
        self.mainLayout.setContentsMargins(*Config.MAIN_LAYOUT_MARGINS)
        self.mainLayout.setSpacing(Config.MAIN_LAYOUT_SPACING)

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
        self.setStyleSheet(Config.MAIN_WINDOW_STYLE_SHEET)

        # All button actions
        self.connectShortcuts()

        # Sets first image
        self.setImagePaths(pathsToImages)

# Initializes shortcuts

    def connectShortcuts(self) -> None:
        """
        Initializes all shotcuts.

        """
        # Close shortcuts
        self.shotcutClose1 = QShortcut(QKeySequence(Config.CLOSE_SHORTCUT1), self)
        self.shotcutClose1.activated.connect(self.close)

        self.shotcutClose2 = QShortcut(QKeySequence(Config.CLOSE_SHORTCUT2), self)
        self.shotcutClose2.activated.connect(self.close)

        # Image changing shortcuts
        self.shortcutPrevious = QShortcut(QKeySequence(Config.PREVIOUS_IMAGE_SHORTCUT), self)
        self.shortcutPrevious.activated.connect(self.previousImage)

        self.shortcutNext = QShortcut(QKeySequence(Config.NEXT_IMAGE_SHORTCUT), self)
        self.shortcutNext.activated.connect(self.nextImage)

        # Open files shortcut
        self.shortcutOpen = QShortcut(QKeySequence(Config.OPEN_FILES_SHORTCUT), self)
        self.shortcutOpen.activated.connect(self.setImagePaths)

        # Maximized screen shortcut
        self.shortcutMaximize = QShortcut(QKeySequence(Config.MAXIMIZE_SHORTCUT), self)
        self.shortcutMaximize.activated.connect(self.toggleMaximize)

        # Reload window shortcut
        self.shortcutReload = QShortcut(QKeySequence(Config.RELOAD_SHORTCUT), self)
        self.shortcutReload.activated.connect(self.reloadWindow)

        # Picker shortcuts
        self.shortcutPick = QShortcut(QKeySequence(Config.PICK_SHORTCUT), self)
        self.shortcutPickAll = QShortcut(QKeySequence(Config.PICK_ALL_SHORTCUT), self)

        if self.usingPicker():
            self.shortcutPick.activated.connect(self.tickCurrentImage)
            self.shortcutPickAll.activated.connect(self.tickAll)

# Utility

    def reloadWindow(self) -> None:
        """
        Exits app with the exit code = EXIT_CODE_REBOOT
        """
        qApp.exit(self.EXIT_CODE_REBOOT)

    def toggleMaximize(self) -> None:
        """
        Toggles window from size (from max size to normal).
        """
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

# Image loading and setting

    def getCurrentImagePath(self) -> str:
        """
        Return path to current image.
        """
        return self.pathsToImages[self.currentImageIndex]

    def loadImageFromFile(self, filePath: str = None) -> QImage:
        """
        Loads located at filePath.
        """
        if not os.path.isfile(filePath):
            raise FileNotFoundError

        return QImage(filePath)

    def setLoadedImage(self) -> None:
        """
        Loads and then displays current image.
        """
        self.imageGraphicsView.clearImage()

        filePath = self.getCurrentImagePath()

        if self.usingPicker():
            self.updatePickerBar()

        image = self.loadImageFromFile(filePath)
        self.imageGraphicsView.setImage(image)
        self.updateBottomBar(filePath)

    def setImagePaths(self, filePaths: list = None) -> None:
        """
        Sets paths to images. Then displays first image.
        """
        if not filePaths:
            filePaths, _ = QFileDialog.getOpenFileNames(self, "Open image files.")

        self.pathsToImages = filePaths
        self.totalImages = len(filePaths)
        self.currentImageIndex = 0

        self.setLoadedImage()

# Changing Image

    def nextImage(self) -> None:
        """
        Switches screen to the next image in the imagePaths.
        """
        if self.totalImages > 1:
            self.currentImageIndex = (self.currentImageIndex + 1) % self.totalImages
            self.setLoadedImage()

    def previousImage(self) -> None:
        """
        Switches screen to the previous image in the imagePaths.
        """
        if self.totalImages > 1:
            self.currentImageIndex = (self.currentImageIndex - 1) % self.totalImages
            self.setLoadedImage()

    def updateBottomBar(self, imagePath: str) -> None:
        """
        Updates bottom bar.
        """
        fileName = os.path.basename(imagePath)
        self.bottomBarLayout.changeNametext(fileName)

        w, h = self.imageGraphicsView.getPixmapSize()
        imageSize = f"{w}x{h}"
        self.bottomBarLayout.changeResolutionText(imageSize)

        text = f"{self.currentImageIndex + 1}/{self.totalImages}"
        self.bottomBarLayout.changeCounterText(text)

# Image Picking

    def usingPicker(self) -> bool:
        """
        Checks if image picker is needed.
        """
        return self.pickedImages is not None

    def imageIsPicked(self, imagePath: str) -> bool:
        """
        Checks if displayed image is picked.
        """
        return imagePath in self.pickedImages

    def updatePickerBar(self) -> None:
        """
        Updates picker bar.
        """
        if self.imageIsPicked(self.getCurrentImagePath()):
            self.bottomBarLayout.setPickerAsPicked()
        else:
            self.bottomBarLayout.setPickerAsUnPicked()

    def tickCurrentImage(self) -> None:
        """
        Updates current image in picked images and picker bar.
        """
        currentImagePath = self.getCurrentImagePath()

        if self.imageIsPicked(currentImagePath):
            self.pickedImages.remove(currentImagePath)
        else:
            self.pickedImages.add(currentImagePath)

        self.updatePickerBar()

    def tickAll(self) -> None:
        """
        Ticks all images, updates bar.
        """
        self.pickedImages = self.pathsToImages.copy()
        self.updatePickerBar()

# Events

    def resizeEvent(self, event) -> None:
        self.imageGraphicsView.updateView()
        return super().resizeEvent(event)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.old_pos = event.pos()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.old_pos = None
        return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if not self.old_pos:
            return
        delta = event.pos() - self.old_pos
        self.move(self.pos() + delta)
        return super().mouseMoveEvent(event)
