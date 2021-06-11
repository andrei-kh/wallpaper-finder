from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel

from .initializer import Config


class BottomBarLayout(QHBoxLayout):
    def __init__(self) -> None:
        """
        Class for layout of the bottom bar.
        """
        QHBoxLayout.__init__(self)

        # Layout margins and spacing between elements.
        self.setContentsMargins(*Config.BOTTOM_BAR_MARGINS)
        self.setSpacing(Config.BOTTOM_BAR_SPACING)

        # Label for image name.
        self.nameLabel = QLabel()
        self.nameLabel.setFixedHeight(Config.BOTTOM_BAR_HEIGHT)
        self.nameLabel.setStyleSheet(Config.NAME_LABEL_STYLE_SHEET)

        # Label for image counter.
        self.counterLabel = QLabel()
        self.counterLabel.setFixedHeight(Config.BOTTOM_BAR_HEIGHT)
        self.counterLabel.setStyleSheet(Config.COUNTER_LABEL_STYLE_SHEET)
        self.counterLabel.setAlignment(Qt.AlignRight)

        # Label for image resolution.
        self.resolutionLabel = QLabel()
        self.resolutionLabel.setFixedHeight(Config.BOTTOM_BAR_HEIGHT)
        self.resolutionLabel.setStyleSheet(Config.RESOLUTION_LABEL_STYLE_SHEET)

        # Label for picker symbol.
        self.pickerBarLabel = QLabel()
        self.pickerBarLabel.setFixedHeight(Config.BOTTOM_BAR_HEIGHT)
        self.pickerBarLabel.setStyleSheet(Config.PICKER_BAR_STYLE_SHEET)
        self.pickerBarLabel.setAlignment(Qt.AlignRight)

        # Symbol that would be shown if image is picked.
        self.pickedSymbol = Config.PICKER_SYMBOL

        # Adding widgets to layout
        self.addWidget(self.nameLabel)
        self.addWidget(self.resolutionLabel, stretch=1)  # Spacing between first 2 and others
        self.addWidget(self.pickerBarLabel)
        self.addWidget(self.counterLabel)

    def changeNametext(self, text) -> None:
        """
        Changes text of the label with picture name.
        """
        self.nameLabel.setText(text)

    def changeCounterText(self, text) -> None:
        """
        Changes text of label with the counter.
        """
        self.counterLabel.setText(text)

    def changeResolutionText(self, text) -> None:
        """
        Changes name of label with resolution.
        """
        self.resolutionLabel.setText(text)

    def setPickerAsPicked(self) -> None:
        """
        Sets picker label text to pickerSymbol.
        """
        self.pickerBarLabel.setText(self.pickedSymbol)

    def setPickerAsUnPicked(self) -> None:
        """
        Sets picker label text to "".
        """
        self.pickerBarLabel.setText("")
