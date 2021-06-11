# WALLPAPER FINDER
![Example](https://imgur.com/qMSnoyR.png)

A simple app that lets you download wallpapers from reddit.- 

- [WALLPAPER FINDER](#wallpaper-finder)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Image viewer controls:](#image-viewer-controls)
  - [Image Viewer settings](#image-viewer-settings)

## Installation
Make sure you have python 3.x installed.

1. Clone and install requirements
```sh
> git clone https://github.com/andreywastaken/wallpaper-finder.git
> cd wallpaper-finder

> pip install -r requirements.txt
```

2. Get reddit api access
     1. Go to [reddit app preferences](https://www.reddit.com/prefs/apps) and click __create another app...__
   
     2. Fill out the required details, select __script__ and click __create an application__
    ![Reddit application](https://imgur.com/OIvQUQs.png)

     3. __script for personal use__ and __secret__ tokens are used to connect to reddit api.
    ![Personal and Secret](https://imgur.com/sw6W1Qx.png)

     4. Create in __.secret__ create __credentials.json__ file
        ```json like that:
        {
        "client_id": "aB1cdeFghI23JK",               // short key one goes here
        "api_key": "LMNopQrst4Uv5Wx67yZOHNOItseNds", // long key one goes here
        "username": "<your reddit username>",        // reddit username goes her
        "password": "<your reddit password>"         // reddit password goes here
        }
        ```
     5. You finished with installation. For test you can execute:
        ```python
        python wallpaper_finder.py
        ```

## Usage
1. Before running
   
    You can run ```python wallpaper_finder.py -h``` or ```python wallpaper_finder.py -help``` to see help:

    ```
    > python .\wallpaper_finder.py -h
    usage: wallpaper_finder.py [-h] [-s SUBREDDITS [SUBREDDITS ...]] [-st   [TYPE]  ] [-l [LIMIT]]
                               [-tf [TIME_FILTER]] [-rd] [--credentials [PATH]  ]   [--save-folder [PATH]]
                               [--temp-folder [PATH]]

    optional arguments:
      -h, --help            show this help message and exit
      -s SUBREDDITS [SUBREDDITS ...], --subreddits SUBREDDITS [SUBREDDITS ...]
                            Images would be parsed from these.
      -st [TYPE], --sort-type [TYPE]
                            Sort type. Can be hot, new, top, rising.
      -l [LIMIT], --limit [LIMIT]
                            How many images would be parsed.
      -tf [TIME_FILTER], --time-filter [TIME_FILTER]
                            Only with sort-type top. Top from day, week,  month,   year or all.
      -rd, --remove-duplicates
                            Script would not save duplicates of images in     save-folder. If you have a lot of
                            images you will die before it finishes.
      --credentials [PATH]  Folder with credentials.json.
      --save-folder [PATH]  Folder where immages would be saved.
      --temp-folder [PATH]  Temporary folder to save images. WARNING:   TEMPORARY   FOLDER WOULD BE CLEARED!!!
    ```

    Also, you can edit __settings.json__, but values passed as a parameter     __override__ values from __settings.json__
    ```json
    {
        "credentials_path": ".secret/credentials.json", // folder with    credentialas.json
        "save_folder_path": "<better change this>",     // folder where   images  are  saved
        "temp_folder_path": "./temp",                   // folder where   images  are saved during runtime
        "subreddits": [                                 // subreddits to parse
            "wallpaper"
        ],
        "sort_type": "top",                             // how to sort    submissions
        "limit": 10,                                    // how many   submissions   will be loaded
        "time_filter": "month",                         // top from   'time_filter'
        "remove_duplicates": false                      // checks for   duplicates
    }
    ```
2. After executing script will load the images:
   ![Image loading](https://imgur.com/SWpOmzt.png)

3. Image viewer will open after all images are open:
   ![Image Viewer](https://imgur.com/KBwex7c.png)

   You can pick images you want to save with __ALT+X__ shortcut.

   All shortcuts:
   ### Image viewer controls:
   | Button            | Action          |
   | ----------------- | --------------- |
   | __Right arrow__   | next image      |
   | __Left arrow__    | previous image  |
   | __ESC or CTRL+Q__ | close viewer    |
   | __ALT+X__         | pick image      |
   | __CTRL+O__        | open files      |
   | __CTRL+F__        | maximize window |
   | __CTRL+R__        | reload window   |

4. After that chosen images would be saved to ```"save_folder"```. If ```-rt``` is present or ```"remove_duplicates"``` is set to ```true``` images that already exist in ```"save_folder"``` would not be saved.

## Image Viewer settings
Image viewer has it's own ```settings.json``` at ```wallpaper-finder/image_viewer```:
```json
{
    "main_window": {
        "main_layout_margins": [0, 4, 0, 0], // Borders of the main layout (left, top, right, bottom)
        "main_layout_spacing": 0,            // Spacing between app widgets

        "background": "black",               // Main window background color 
        "border_size": 6,                    // Main window border size in px
        "border_color": "white"              // Main window border color
    },

    "bottom_bar": {
        "bottom_bar_margins": [0, 0, 0, 0],  // Borders of the bottom bar layout
        "bottom_bar_spacing": 0,             // Spacing between bottom bar widgets
        "bottom_bar_height": 28,             // Bottom bar height in px


        "picker_symbol": "🗹",               // Symbol that shows when image is picked
        "picker_color": "black",             // Color of the symbol 

        "background": "gray",                // Bottom bar background
        "top_border_size": 2,                // Bottom bar top border size in px
        "top_border_color": "white",         // Bottom bar top border color

        "font_size": "11",                   // Bottom bar font
        "font_weight": "bold",               // Bottom bar font weight
        "font_family": "Consolas"            // Bottom bar font family
    }
}
```