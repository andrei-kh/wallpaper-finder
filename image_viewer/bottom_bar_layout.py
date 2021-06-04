from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel

from settings import (BOTTOM_BAR_HEIGHT,
                      BOTTOM_BAR_MARGINS,
                      BOTTOM_BAR_SPACING,
                      PICKER_BAR_STYLE_SHEET,
                      STATUS_BAR_STYLE_SHEET,
                      PICKER_SYMBOL)


class BottomBarLayout(QHBoxLayout):
    def __init__(self):
        QHBoxLayout.__init__(self)

        self.setContentsMargins(*BOTTOM_BAR_MARGINS)
        self.setSpacing(BOTTOM_BAR_SPACING)

        self.statusBarLabel = QLabel()
        self.statusBarLabel.setFixedHeight(BOTTOM_BAR_HEIGHT)
        self.statusBarLabel.setStyleSheet(STATUS_BAR_STYLE_SHEET)
        self.statusBarLabel.setAlignment(Qt.AlignBottom)

        self.pickerBarLabel = QLabel()
        self.pickerBarLabel.setFixedHeight(BOTTOM_BAR_HEIGHT)
        self.pickerBarLabel.setStyleSheet(PICKER_BAR_STYLE_SHEET)
        self.pickerBarLabel.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        self.pickedSymbol = PICKER_SYMBOL

        self.addWidget(self.statusBarLabel)
        self.addWidget(self.pickerBarLabel)

    def changeStatus(self, text):
        self.statusBarLabel.setText(text)

    def setPickerAsPicked(self):
        self.pickerBarLabel.setText(self.pickedSymbol)

    def setPickerAsUnPicked(self):
        self.pickerBarLabel.setText("")
