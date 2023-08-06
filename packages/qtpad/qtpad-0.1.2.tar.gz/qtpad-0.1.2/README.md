# qtPad
- Modern and highly customizable sticky note application
- Written in Python 3 and Qt 5

# Features
- Customizable actions for widgets events; startup, tray icon, bottom note border, titlebar
- Customizable default style for all new notes, style for specific notes and style presets
- Customizable hotkeys and context menus
- Notes saved in plain text and organized by folder structure
- Detection of image content/path from clipboard
- Handy text actions boundable to hotkeys; indent, sort, set case, line shift and more
- Auto save and load on focus events
- Search and replace GUI

# Screenshots
**Customizable style presets**

![alt tag](https://gitlab.com/william.belanger/qtpad/raw/master/screenshots/quickstyle.png)
![alt tag](https://gitlab.com/william.belanger/qtpad/raw/master/screenshots/stylepreset.gif)

**Preferences GUI**

![alt tag](https://gitlab.com/william.belanger/qtpad/raw/master/screenshots/preferences_general.png)

![alt tag](https://gitlab.com/william.belanger/qtpad/raw/master/screenshots/preferences_hotkeys.png)

![alt tag](https://gitlab.com/william.belanger/qtpad/raw/master/screenshots/preferences_actions.png)

![alt tag](https://gitlab.com/william.belanger/qtpad/raw/master/screenshots/preferences_menus.png)

![alt tag](https://gitlab.com/william.belanger/qtpad/raw/master/screenshots/preferences_presets.png)


**Profile GUI**

![alt tag](https://gitlab.com/william.belanger/qtpad/raw/master/screenshots/style.png)




**Folder organization**

![alt tag](https://gitlab.com/william.belanger/qtpad/raw/master/screenshots/folders.png)


**Search GUI**

![alt tag](https://gitlab.com/william.belanger/qtpad/raw/master/screenshots/search.png)

# Command line interface
- All the actions listed in the preferences dialog can be called from command, by using flags -a or --action
    - ie. qtpad -a "new note"

# Installation
- Arch Linux: install 'qtpad-git' from the AUR
- Debian/Ubuntu:
    - sudo apt-get install python3-setuptools python3-pip
    - sudo pip3 install qtpad

- Windows:
    - Install the lastest version of Python, along with the PyPi utility (pip)
    - Open the command prompt (cmd.exe) with administrator privileges
    - Type 'python -m pip install pyqt5 requests'
    - Clone the repository and extract the qtpad folder
    - Create a shortcut to run the script manually with 'python your_installation_path/qtpad/\_\_init\_\_.py'

# Compatibility
qtPad is developed on Openbox. Altough not tested as often, it should also work on other platforms:
- Linux: Openbox, MATE, Cinnamon, XFCE, Deepin, KDE Plasma 5
- Microsoft: Windows 7

Known bugs:
- Current font family is not loaded in style dialog font combo box
- Wrong position of the tray icon context menu in KDE

 Please report all issues on Gitlab :)
