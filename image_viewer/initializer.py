import json
import os
from PyQt5.QtGui import QFontDatabase

SETTINGS_FILE = "settings.json"
MAIN_WINDOW_SETTINGS = "main_window"
BOTTOM_BAR_SETTINGS = "bottom_bar"
SHORTCUTS_SETTINGS = "shortcuts"
FONTS_FOLDER = "fonts"


class Config:
    def _load_settings() -> dict:
        """
        Loads settings.json.
        """
        working_direcory = os.path.dirname(os.path.abspath(__file__))
        settings_path = os.path.join(working_direcory, SETTINGS_FILE)

        with open(settings_path, encoding="utf-8") as settings_file:
            return json.load(settings_file)

    def _load_fonts() -> None:
        """
        Loads all files in fonts folder.
        """
        working_direcory = os.path.dirname(os.path.abspath(__file__))
        fonts_path = os.path.join(working_direcory, FONTS_FOLDER)

        for filename in os.listdir(fonts_path):
            a = QFontDatabase()
            a.addApplicationFont(os.path.join(fonts_path, filename))

    @classmethod
    def apply_settings(cls) -> None:
        """
        Sets all constants.
        """
        cls._load_fonts()

        user_settings = cls._load_settings()

        main_window_settings = user_settings[MAIN_WINDOW_SETTINGS]
        bottom_bar_settings = user_settings[BOTTOM_BAR_SETTINGS]
        shortcuts = user_settings[SHORTCUTS_SETTINGS]

        # Constants
        cls.MAIN_LAYOUT_MARGINS = main_window_settings["main_layout_margins"]
        cls.MAIN_LAYOUT_SPACING = main_window_settings["main_layout_spacing"]

        cls.BOTTOM_BAR_MARGINS = bottom_bar_settings["bottom_bar_margins"]
        cls.BOTTOM_BAR_SPACING = bottom_bar_settings["bottom_bar_spacing"]
        cls.BOTTOM_BAR_HEIGHT = bottom_bar_settings["bottom_bar_height"]
        cls.PICKER_SYMBOL = bottom_bar_settings["picker_symbol"]

        # Style sheets
        cls.MAIN_WINDOW_STYLE_SHEET = (
            "background-color: {background};"

            "border:       {size}px solid {color};"
            "border-top:   None;".format(
                background=main_window_settings["background"],
                size=main_window_settings["border_size"],
                color=main_window_settings["border_color"])
        )

        cls.IMAGE_GRAPHICS_STYLE_SHEET = (
            "border:       None;"
            "border-left:  {size}px solid {color};"
            "border-right: {size}px solid {color};".format(
                size=main_window_settings["border_size"],
                color=main_window_settings["border_color"]
            )
        )

        cls.NAME_LABEL_STYLE_SHEET = (
            "background-color: {background};"

            "border:       {size}px solid {color};"
            "border-top:   {tSize}px solid {tColor};"
            "border-right: None;"

            "font-size:    {fSize}pt;"
            "font-weight:  {weight};"
            "font-family:  {family};".format(
                background=bottom_bar_settings["background"],
                size=main_window_settings["border_size"],
                color=main_window_settings["border_color"],
                tSize=bottom_bar_settings["top_border_size"],
                tColor=bottom_bar_settings["top_border_color"],
                fSize=bottom_bar_settings["font_size"],
                weight=bottom_bar_settings["font_weight"],
                family=bottom_bar_settings["font_family"]
            )
        )

        cls.COUNTER_LABEL_STYLE_SHEET = (
            "background-color: {background};"

            "border:      {size}px solid {color};"
            "border-top:  {tSize}px solid {tColor};"
            "border-left: None;"

            "font-size:   {fSize}pt;"
            "font-weight: {weight};"
            "font-family: {family};".format(
                background=bottom_bar_settings["background"],
                size=main_window_settings["border_size"],
                color=main_window_settings["border_color"],
                tSize=bottom_bar_settings["top_border_size"],
                tColor=bottom_bar_settings["top_border_color"],
                fSize=bottom_bar_settings["font_size"],
                weight=bottom_bar_settings["font_weight"],
                family=bottom_bar_settings["font_family"]
            )
        )

        cls.RESOLUTION_LABEL_STYLE_SHEET = (
            "background-color: {background};"

            "border:       {size}px solid {color};"
            "border-top:   {tSize}px solid {tColor};"
            "border-left:  None;"
            "border-right: None;"

            "font-size:    {fSize}pt;"
            "font-weight:  {weight};"
            "font-family:  {family};".format(
                background=bottom_bar_settings["background"],
                size=main_window_settings["border_size"],
                color=main_window_settings["border_color"],
                tSize=bottom_bar_settings["top_border_size"],
                tColor=bottom_bar_settings["top_border_color"],
                fSize=bottom_bar_settings["font_size"],
                weight=bottom_bar_settings["font_weight"],
                family=bottom_bar_settings["font_family"]
            )
        )

        cls.PICKER_BAR_STYLE_SHEET = (
            "background-color: {background};"

            "border:       {size}px solid {color};"
            "border-top:   {tSize}px solid {tColor};"
            "border-left:  None;"
            "border-right: None;"

            "color:        {pColor};"
            "font-size:    10pt;".format(
                background=bottom_bar_settings["background"],
                size=main_window_settings["border_size"],
                color=main_window_settings["border_color"],
                tSize=bottom_bar_settings["top_border_size"],
                tColor=bottom_bar_settings["top_border_color"],
                pColor=bottom_bar_settings["picker_color"],
            )
        )

        # Shortcuts
        cls.CLOSE_SHORTCUT1 = shortcuts["close_shortcut1"]
        cls.CLOSE_SHORTCUT2 = shortcuts["close_shortcut2"]
        cls.PREVIOUS_IMAGE_SHORTCUT = shortcuts["previous_image_shortcut"]
        cls.NEXT_IMAGE_SHORTCUT = shortcuts["next_image_shortcut"]
        cls.OPEN_FILES_SHORTCUT = shortcuts["open_files_shortcut"]
        cls.MAXIMIZE_SHORTCUT = shortcuts["maximize_shortcut"]
        cls.RELOAD_SHORTCUT = shortcuts["reload_shortcut"]
        cls.PICK_SHORTCUT = shortcuts["pick_shortcut"]
        cls.PICK_ALL_SHORTCUT = shortcuts["pick_all_shortcut"]
