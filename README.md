# 🖼 WALLPAPER FINDER

![Example](https://imgur.com/nL2wYbY.png)

A simple app that lets you download wallpapers from reddit. 

- [🖼 WALLPAPER FINDER](#-wallpaper-finder)
  - [Installation](#installation)
    - [Firstly](#firstly)
    - [Reddit api](#reddit-api)
  - [Usage](#usage)
    - [Image viewer controls:](#image-viewer-controls)
  - [Image Viewer settings](#image-viewer-settings)

## Installation
Make sure you have __python 3.x__ installed.<br>
You can use it with or without api.<br>
Using api requires __api keys__.

### Firstly 

```sh
> git clone https://github.com/andreywastaken/wallpaper-finder.git --depth=1
> cd wallpaper-finder

> pip install -r requirements.txt
```

__After that script would work, but you can get capped by reddit.__

### Reddit api
<details>
    <summary markdown="span"> Click to view </summary>

Firstly you need to clone repository.

Now you need to get reddit api access (__you need to have reddit account__)
  1. Go to [reddit app preferences](https://www.reddit.com/prefs/apps) and click __create another app...__
    
  2. Fill out the required details, select __script__ option and click __create an  application__
        
        ![Reddit application](https://imgur.com/t0Ze6Xc.png)

  3. __script for personal use__ and __secret__ tokens are used to connect to reddit    api.

        ![Personal and Secret](https://imgur.com/sw6W1Qx.png)

  4. Create in __.secret__ create __credentials.json__ file like that:
        ```javascript 
        {
        "client_id": "aB1cdeFghI23JK",               // short key goes here
        "api_key": "LMNopQrst4Uv5Wx67yZOHNOItseNds", // long key goes here
        }
        ```
</details>

## Usage
1. Before running
   
    You can run ```python wallpaper_finder.py -h``` or ```python wallpaper_finder.py --help``` to see help:

    ```
    > python .\wallpaper_finder.py -h
    usage: wallpaper_finder.py [-h] [-s SUBREDDITS [SUBREDDITS ...]] [-st [TYPE]] [-l [LIMIT]]
                               [-tf [TIME_FILTER]] [-rd] [-nt [NUMBER_OF_THREADS]] [-ua]
                               [-ae ALLOWED_EXTENSIONS [ALLOWED_EXTENSIONS ...]]
                               [--credentials [PATH]] [--save-folder [PATH]] [--temp-folder [PATH]]
                               [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -s SUBREDDITS [SUBREDDITS ...], --subreddits SUBREDDITS [SUBREDDITS ...]
                            Images would be parsed from these.
      -st [TYPE], --sort-type [TYPE]
                            Sort type. Can be hot, new, top, rising.
      -l [LIMIT], --limit [LIMIT]
                            How many submissions would be parsed.
      -tf [TIME_FILTER], --time-filter [TIME_FILTER]
                            Only with sort-type top. Top from day, week, month, year or all.
      -rd, --remove-duplicates
                            If present script would not save duplicates of images in save-folder.
      -nt [NUMBER_OF_THREADS], --number-of-threads [NUMBER_OF_THREADS]
                            Number of threads to use for loading images.
      -ua, --use-api        If present script would connect to reddit api. Needs 'credentials.json' to be present.
      -ae ALLOWED_EXTENSIONS [ALLOWED_EXTENSIONS ...], --allowed-extensions ALLOWED_EXTENSIONS [ALLOWED_EXTENSIONS ...]
                            Images with only this extensions are allowed.
      --credentials [PATH]  Folder with credentials.json.
      --save-folder [PATH]  Folder where images would be saved.
      --temp-folder [PATH]  Temporary folder to save images. WARNING: After finishing loaded pictures
                            in this folder would be removed
      -v, --verbose         Makes everything more verbose.                      
    ```

    Also, you can edit __settings.json__, but values passed as a parameter __overrides__ values from __settings.json__
    ```javascript
    {
        "save_folder_path": "./saved",                  // folder where images are saved
        "temp_folder_path": "./temp",                   // folder where images are saved during runtime
        "subreddits": [                                 // subreddits to parse
            "wallpaper"
        ],
        "sort_type": "top",                             // how to sort submissions
        "limit": 10,                                    // how many submissions will be loaded
        "time_filter": "month",                         // top from 'time_filter'
        "remove_duplicates": false,                     // check for duplicates
        "use_api": false                                // connect to api
        "credentials_path": ".secret/credentials.json", // folder with credentials.json
        "allowed_extensions": [                         // load images with this extensions.
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp"
        ],
        "number_of_threads": 4,                         // threads to use when downloading
        "verbose": false                                // verbose mode
    }
    ```
2. After executing script will load the images to __"temp_folder"__:
 
   ![Image loading](https://imgur.com/cDqTWRE.png)

3. Image viewer will open after all images are open:
 
   ![Image Viewer](https://imgur.com/QLbH2GF.png)

   You can pick images you want to save with __ALT+X__ shortcut.

   All shortcuts:
   ### Image viewer controls:
   | Button            | Action              |
   | ----------------- | ------------------- |
   | __Right arrow__   | next image          |
   | __Left arrow__    | previous image      |
   | __ESC or CTRL+Q__ | close viewer        |
   | __ALT+X__         | pick image          |
   | __ALT+A__         | pick all images     |
   | __CTRL+O__        | open files          |
   | __CTRL+F__        | toggles window size |
   | __CTRL+R__        | reload window       |

4. After that chosen images would be saved to ```"save_folder"```. If ```-rt``` is present or ```"remove_duplicates"``` is set to ```true``` images that already exist in ```"save_folder"``` would not be saved. Speed of ```"remove_duplicates"``` is depends on number of pictures in you ```"save folder"```. On my machine it's ~500 pictures per minute.

## Image Viewer settings
You can also add fonts to the ```image_viewer/fonts```.

Image viewer has it's own ```settings.json``` at ```wallpaper-finder/image_viewer```:
```javascript
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

        "font_size": "12",                   // Bottom bar font
        "font_weight": "medium",             // Bottom bar font weight
        "font_family": "Lemon"               // Bottom bar font family
    },

    "shortcuts":{
        "close_shortcut1": "ESC",            // First shortcut to close window
        "close_shortcut2": "Ctrl+Q",         // Second shortcut to close window

        "previous_image_shortcut": "Left",   // Shortcut to go to previous image
        "next_image_shortcut": "Right",      // Shortcut to go to next image

        "open_files_shortcut": "Ctrl+O",     // Shortcut to open files

        "maximize_shortcut": "Ctrl+F",       // Shortcut to maximize window

        "reload_shortcut": "Ctrl+R",         // Shortcut to reload window
        
        "pick_shortcut": "Alt+X",            // Shortcut to pick image
        "pick_all_shortcut": "Alt+A"         // Shortcut to pick all images
    }
}
```
