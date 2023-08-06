#!/usr/bin/python3
import json
import os
import random
import sys
import time
from PyQt5 import QtGui, QtWidgets, QtCore, uic
from PyQt5.QtCore import Qt

try:
    import qtpad.gui_preferences
    from qtpad.common import *
except ImportError:
    from common import *

# Init common settings
LOCAL_DIR, ICONS_DIR, PREFERENCES_FILE, PROFILES_FILE = getStaticPaths()
logger = getLogger()

PREFERENCES_DEFAULT = \
{
    'general':
    {
        'notesDb': os.path.expanduser("~/.config/qtpad/notes/"),
        'nameText': 'Untitled',
        'nameImage': 'Image',
        'nameFormatText': '%fullname%',
        'nameFormatImage': '%fullname% (%size%)',
        'borderColor': '#444444',
        'minimize': True,
        'autoIndent': True,
        'safeDelete': True,
        'hotkeys': True,
        'deleteEmptyNotes': True,
        'frameless': False,
        'fetchUrl': False,
        'fetchResize': False,
        'fetchClear': True,
        'fetchFile': True,
        'fetchTxt': True,
    },
    'actions':
    {
        'events':
        {
            'startup': 'None',
            'close button': 'Hide',
        },
        'tray icon':
        {
            'left click': 'Toggle actives',
            'middle click': 'Fetch clipboard or new note',
        },
        'top border':
        {
            'left click': 'None',
            'middle click': 'None',
            'right click': 'None',
            'wheel up': 'None',
            'wheel down': 'None',
        },
        'bottom border':
        {
            'left click': 'None',
            'middle click': 'None',
            'right click': 'None',
            'wheel up': 'None',
            'wheel down': 'None',
        },
    },
    'exec':
    {
        'events':
        {
            'startup': '',
        },
        'tray icon':
        {
            'left click': '',
            'middle click': '',
        },
    },
    'styleDefault':
    {
        'pin': False,
        'sizeGrip': True,
        'x': 0,
        'y': 0,
        'width': 300,
        'height': 220,
        'background': '#FFFF7F',
        'foreground': '#000000',
        'fontSize': 9,
        'fontFamily': 'Sans Serif',
        'opacity': 1.0,
    },
    'stylePresets':
    {
        'Black on yellow': {'background': '#FFFF7F', 'foreground': '#000000'},
        'Black on white': {'background': '#FFFFFF', 'foreground': '#000000'},
        'White on black': {'background': '#2A2A2A', 'foreground': '#FFFFFF'},
        'Low priority': {'background': '#C6EFCE', 'foreground': '#004000'},
        'Mid priority': {'background': '#FFEB9C', 'foreground': '#553400'},
        'High priority': {'background': '#FFC7CE', 'foreground': '#9C0006'},
    },
    'hotkeys':
    {
        'ctrl':
        {
            'D': 'duplicate line',
            'F': 'search',
            'P': 'pin',
            'R': 'rename',
            'Y': 'redo',
            'Wheel Up': 'zoom increase',
            'Wheel Down': 'zoom decrease',
            "<": "indent decrease",
        },
        'ctrl + shift':
        {
            'L': 'selection to lowercase',
            'R': 'toggle sizegrip',
            'S': 'sort selection',
            'U': 'selection to uppercase',
            'V': 'special paste',
            'Up': 'shift line up',
            'Down': 'shift line down',
            '+': 'zoom increase',
            '_': 'zoom decrease',
            ">": "indent increase",
        },
        'shift':
        {
            'Backspace': 'delete line',
            'Wheel Up': 'opacity increase',
            'Wheel Down': 'opacity decrease',
        }
    },
    'menus':
    {
        "mother": [
            "New note",
            "Toggle actives",
            "Fetch clipboard",
            "Show all",
            "Reset positions",
            "(Separator)",
            "Unload all folders",
            "Folders list",
            "(Separator)",
            "Notes list",
            "(Separator)",
            "Preferences",
            "Quit"
        ],
        "child": [
            "New note",
            "Rename",
            "Style",
            "Pin",
            "Save as",
            "Copy to clipboard",
            "Move to folder",
            "(Separator)",
            "Delete"
        ]
    },
    'actives': [],
    'unloaded': [],
}

CSS_FRAME_DEFAULT = \
{
    'QLabel#iconLabel':
    {
        'background-color': '#444444',
    },
    'QLabel#titleLabel':
    {
        'color': '#888888',
        'background-color': '#444444',
        'font-weight': 'bold',
    },
    'QLabel#titleLabel:active':
    {
        'color': '#ffffff',
    },
    'QPushButton#closeButton':
    {
        'color': '#888888',
        'background-color': '#444444',
        'font-weight': 'bold',
        'border': 'none',
        'padding': '5px',
    },
    'QPushButton#closeButton:active':
    {
        'color': '#ffffff',
    },
    'QPushButton#closeButton:hover':
    {
        'color': '#1d90cd',
    }
}

CSS_MENU_DEFAULT = \
{
    'QMenu::item':
    {
        'color': '#000000',
        'background-color': '#fefefe',
    },
    'QMenu::item:selected':
    {
        'color': '#ffffff',
        'background-color': '#2f8bc5',
    }
}

actionsChildBase = ['Copy', 'Cut', 'Copy line', 'Cut line', 'Paste', 'Undo', 'Redo', 'Hide', 'Pin', 'Rename',
                    'Selection to lowercase', 'Selection to uppercase', 'Sort selection', 'Toggle wordwrap',
                    'Special paste', 'Toggle sizegrip', 'New note', 'Delete',  'Save as']

actionsChildMenu = ['(Separator)', 'Move to folder', 'Style', 'Copy to clipboard']

actionsChildHotkeys = ['Delete line', 'Duplicate line', 'Shift line down', 'Shift line up', 'Indent increase',
                        'Search', 'Copy to clipboard', 'Indent decrease', 'Zoom increase', 'Zoom decrease',
                        'Opacity increase', 'Opacity decrease']

actionsMotherBase = ['Toggle actives', 'New note', 'Show all', 'Hide all', 'Reverse all', 'Reset positions',
                        'Fetch clipboard', 'Load all folders', 'Unload all folders']

actionsMotherMenu = ['(Separator)', 'Folders list', 'Notes list', 'Preferences', 'Quit']

class PreferencesDatabase(object):
    def __init__(self):
        CONFIG_DIR = os.path.expanduser("~/.config/qtpad")
        if not os.path.isdir(CONFIG_DIR):
            os.mkdir(CONFIG_DIR)

        if os.path.isfile(PREFERENCES_FILE) and os.stat(PREFERENCES_FILE).st_size > 0:
            self.load()
            # Look for missing keys
            if not set(PREFERENCES_DEFAULT) == set(self.db):
                missing = str(list(filter(lambda x: x not in self.db, PREFERENCES_DEFAULT)))
                logger.error(f"Preferences KeyError: {missing}")
                logger.warning("Restored preferences to default")
                self.db = copyDict(PREFERENCES_DEFAULT)
                self.save()
        else:
            self.db = copyDict(PREFERENCES_DEFAULT)
            with open(PREFERENCES_FILE, "w") as f:
                f.write(json.dumps(self.db, indent=2, sort_keys=False))
            logger.info("Created preferences file")
        self.initStyleSheet()

    def initStyleSheet(self):
        CSS_FRAME_FILE = os.path.expanduser("~/.config/qtpad/frame.css")
        if not os.path.isfile(CSS_FRAME_FILE) or os.stat(CSS_FRAME_FILE).st_size == 0:
            with open(CSS_FRAME_FILE, 'w') as f:
                f.write(dictToCss(CSS_FRAME_DEFAULT))
            logger.warning("New frame stylesheet created from default")

        CSS_MENU_FILE = os.path.expanduser("~/.config/qtpad/menu.css")
        if not os.path.isfile(CSS_MENU_FILE) or os.stat(CSS_MENU_FILE).st_size == 0:
            with open(CSS_MENU_FILE, 'w') as f:
                f.write(dictToCss(CSS_MENU_DEFAULT))
            logger.warning("New menu stylesheet created from default")

    def load(self):
        with open(PREFERENCES_FILE, "r") as f:
            self.db = json.load(f)
        logger.info("Loaded preferences database")

    def query(self, *keys, db=None, fault=False):
        if not db: db = self.db
        for key in keys:
            try:
                db = db[key]
            except KeyError:
                if fault:
                    logger.critical(f"Preferences KeyError: '{key}' not found in default database")
                    return None

                logger.error(f"Preferences KeyError: '{key}' not found")
                backup = PREFERENCES_FILE + ".broken"
                with open(backup, "w") as f:
                    f.write(json.dumps(self.db, indent=2, sort_keys=False))
                msg = "Preferences have been reset to default. This is\n" \
                    + "most likely caused by a backward incompatibility.\n" \
                    + f"A backup of the old configuration is saved at:\n\n{backup}"
                error = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Broken preferences error", msg)
                error.exec_()

                logger.warning("Restored preferences to default")
                self.db = copyDict(PREFERENCES_DEFAULT)
                self.save()
                return self.query(*keys, fault=True)
        return db

    def save(self):
        with open(PREFERENCES_FILE, "w") as f:
            f.write(json.dumps(self.db, indent=2, sort_keys=False))
        logger.info("Saved preferences database")

    def set(self, name, entry, value=None):
        if value is None:
            self.db[name] = entry
            self.save()
        else:
            self.db[name][entry] = value


class PreferencesForm(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__()

        # Load the ui file in case the gui modules are not loaded
        if "qtpad.gui_preferences" in sys.modules:
            self.ui = qtpad.gui_preferences.Ui_Dialog()
            self.ui.setupUi(self)
        else:
            self.ui = uic.loadUi(LOCAL_DIR + 'gui_preferences.ui', self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.parent = parent
        self.origin = type(parent).__name__

        # Load preferences from Mother instance
        if self.origin == "Mother":
            self.preferences = parent.preferences
        elif self.origin == "Child":
            self.preferences = parent.parent.preferences
        self.preferences.load()
        self.db = copyDict(self.preferences.db)

        # Init preferences or style dialog
        if self.origin == "Mother":
            self.settingsInitMother()
        elif self.origin == "Child":
            self.settingsInitChild()
        try:
            self.settingsLoad()
        except KeyError:
            logger.error("KeyError in preferences database, loaded default settings instead")
            self.settingsReset()

        # Hotkeys
        self.modifier = {"ctrl": False, "shift": False, "ctrl + shift": False}
        self.ui.hotkeyTree.sortByColumn(0, QtCore.Qt.AscendingOrder)

        # Style default
        self.ui.styleBackgroundButton.clicked.connect(lambda: self.stylePickLayerColor("background"))
        self.ui.styleForegroundButton.clicked.connect(lambda: self.stylePickLayerColor("foreground"))
        self.ui.styleFontFamilyCombo.currentFontChanged.connect(self.styleUpdateFontFamily)
        self.ui.styleFontSizeBox.valueChanged.connect(self.styleUpdateFontSize)
        self.ui.styleWidthBox.valueChanged.connect(self.styleUpdateWidth)
        self.ui.styleHeightBox.valueChanged.connect(self.styleUpdateHeight)
        self.ui.styleOpacityBox.valueChanged.connect(self.styleUpdateOpacity)

        # Init preferences dialog
        self.done = self.exec_()
        self.close()

    def closeEvent(self, event):
        if self.done:
            self.settingsApply()
        elif self.origin == "Child":
            self.parent.styleProfileLoad()
        event.accept()

    def eventFilter(self, obj, event):
        if obj is self.ui.hotkeyKeyLine:
            self.hotkeyParseEvent(event)
        return QtCore.QObject.event(obj, event)

    def showEvent(self, event):
        if self.origin == "Mother":
            foreground = self.preferences.query("styleDefault", "foreground")
            background = self.preferences.query("styleDefault", "background")
            self.presetViewUpdate(foreground, background)
            self.styleUpdateView()

    def actionComboSelect(self):
        self.ui.actionSaveButton.setEnabled(bool(self.ui.actionListCombo.currentText()))
        self.ui.actionListCombo.setEnabled(bool(self.ui.actionListCombo.currentText()))
        if self.ui.actionListCombo.currentText() == "Exec":
            self.ui.actionCommandLine.setEnabled(True)
        else:
            self.ui.actionCommandLine.setEnabled(False)
            self.ui.actionCommandLine.clear()

    def actionSave(self):
        item = self.ui.actionTree.currentItem()
        widget = item.parent().text(0).lower()
        trigger = item.text(0).lower()
        action = self.ui.actionListCombo.currentText()
        command = self.ui.actionCommandLine.text()

        item.setText(1, action)
        item.setText(2, command)
        if action == "Exec":
            self.db["exec"][widget][trigger] = command
        self.db["actions"][widget][trigger] = action

    def actionTreeSelect(self):
        item = self.ui.actionTree.currentItem()
        trigger = item.text(0)
        action = item.text(1)
        command = item.text(2)

        self.ui.actionListCombo.clear()
        if item.parent():
            widget = item.parent().text(0)
            if trigger == "Startup" or widget == "Tray icon":
                actions = ['None', 'Exec', 'Fetch clipboard or new note'] + actionsMotherBase
            elif trigger == "Close button":
                actions = ['Hide', 'Unload', 'Delete']
            else:
                actions = ['None'] + actionsChildBase + actionsChildHotkeys
            actions.sort()
            self.ui.actionListCombo.addItems(actions)
        self.ui.actionListCombo.setCurrentText(action)
        self.ui.actionCommandLine.setText(command)

    def cssFileChanged(self):
        current = self.ui.cssCombo.currentText()
        if current in self.css:
            self.ui.cssTextEdit.setPlainText(self.css[current])
            self.parent.preferencesIndexes["css"] = current

    def cssRefresh(self):
        configPath = os.path.expanduser("~/.config/qtpad/")
        css = configPath + self.ui.cssCombo.currentText()
        if os.path.isfile(css):
            with open(css) as stylesheet:
                stylesheet = stylesheet.read()
            self.ui.cssTextEdit.setPlainText(stylesheet)
            self.css[self.ui.cssCombo.currentText()] = stylesheet

    def cssTextChanged(self):
        self.css[self.ui.cssCombo.currentText()] = self.ui.cssTextEdit.toPlainText()

    def generalSetPath(self, path):
        # Validation of a new notes database path
        path = os.path.expanduser(path)
        path = sanitizeString(path, illegal=':*?"<>|')
        if not path.endswith("/"):
            path += "/"
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except PermissionError:
                logger.critical(f"PermissionError: could not create directory '{path}'")
                return False
        self.db["general"]["notesDb"] = path
        self.preferences.set("general", "notesDb", path)

        # Close old notes and load content from new folder
        for child in self.parent.children:
            self.parent.children[child].noteClose()
        self.parent.children = {}
        self.parent.lastActive = ""
        self.parent.folderLoad(path)
        logger.info("Unloaded all notes")
        logger.info(f"Loading notes from folder '{path}'")

    def hotkeyAdd(self):
        hotkey = self.ui.hotkeyKeyLine.text()
        action = self.ui.hotkeyActionCombo.currentText()
        if hotkey and action:
            self.ui.hotkeyKeyLine.clear()
            self.ui.hotkeyActionCombo.setCurrentText('')

            # Parse modifier from string
            for modifier in ("Ctrl + Shift", "Ctrl", "Shift"):
                if hotkey.startswith(modifier):
                    key = hotkey.replace(modifier + " + ", "")
                    self.db["hotkeys"][modifier.lower()][key] = action
                    break

            # Remove duplicates and insert the new hotkey
            for topItem in range(self.ui.hotkeyTree.topLevelItemCount()):
                topItem = self.ui.hotkeyTree.topLevelItem(topItem)
                if modifier == topItem.text(0):
                    self.hotkeyRemoveChild(topItem, key)
                    self.hotkeyAddChild(topItem, key, action)
                    break
            else:
                topItem = QtWidgets.QTreeWidgetItem()
                topItem.setText(0, modifier)
                self.hotkeyAddChild(topItem, key, action)
                self.hotkeyEnumerate()

    def hotkeyAddChild(self, topItem, key, action):
        subItem = QtWidgets.QTreeWidgetItem()
        topItem.addChild(subItem)
        subItem.setText(0, key)
        subItem.setText(1, action)
        self.ui.hotkeyTree.setCurrentItem(subItem)
        self.hotkeySelect()

    def hotkeyParseEvent(self, event):
        eventType = event.type()
        if eventType == QtCore.QEvent.KeyPress or eventType == QtCore.QEvent.KeyRelease:
            self.modifier["ctrl"] = (event.modifiers() == Qt.ControlModifier)
            self.modifier["shift"] = (event.modifiers() == Qt.ShiftModifier)
            self.modifier["ctrl + shift"] = int(event.modifiers()) == (Qt.ControlModifier + Qt.ShiftModifier)

        if eventType in (QtCore.QEvent.KeyPress, QtCore.QEvent.Wheel, QtCore.QEvent.MouseButtonPress):
            for m in self.modifier:
                if self.modifier[m]:
                    modifier = f"{m.title()} + "
                    break
            else:
                modifier = "Ctrl + "

        if eventType == QtCore.QEvent.KeyPress:
            key = QtGui.QKeySequence(event.key()).toString()
            try:
                key.encode('utf-8')
                self.ui.hotkeyKeyLine.setText(modifier + key)
            except UnicodeEncodeError:
                pass  # Filter unwanted unicode characters from modifiers

        elif eventType == QtCore.QEvent.Wheel:
            if int(event.angleDelta().y()) > 0:
                self.ui.hotkeyKeyLine.setText(modifier + "Wheel Up")
            else:
                self.ui.hotkeyKeyLine.setText(modifier + "Wheel Down")

        elif eventType == QtCore.QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.ui.hotkeyKeyLine.setText(modifier + "Left click")
            elif event.button() == Qt.MiddleButton:
                self.ui.hotkeyKeyLine.setText(modifier + "Middle click")

    def hotkeyRemoveChild(self, modifier, key):
        children = QtWidgets.QTreeWidgetItemIterator(modifier)
        while children.value():
            child = children.value()
            children += 1
            if child.text(0) == key:
                modifier.removeChild(child)
                break

    def hotkeyClear(self):
        self.db["hotkeys"]["ctrl"] = {}
        self.db["hotkeys"]["shift"] = {}
        self.db["hotkeys"]["ctrl + shift"] = {}
        self.ui.hotkeyTree.clear()
        self.ui.hotkeyDeleteButton.setEnabled(False)

    def hotkeyDelete(self):
        item = self.ui.hotkeyTree.currentItem()
        if item:
            del self.db["hotkeys"][item.parent().text(0).lower()][item.text(0)]

            # Select next available item
            if item.parent().indexOfChild(item) == 0:
                self.ui.hotkeyTree.setCurrentItem(self.ui.hotkeyTree.itemBelow(item))
            else:
                self.ui.hotkeyTree.setCurrentItem(self.ui.hotkeyTree.itemAbove(item))

            # Remove modifier top item if empty
            if item.parent().childCount() == 1:
                index = self.ui.hotkeyTree.indexOfTopLevelItem(item.parent())
                self.ui.hotkeyTree.takeTopLevelItem(index)
            else:
                item.parent().removeChild(item)

    def hotkeyEnumerate(self):
        self.ui.hotkeyTree.clear()
        self.hotkeyInsert(modifier="ctrl")
        self.hotkeyInsert(modifier="shift")
        self.hotkeyInsert(modifier="ctrl + shift")
        self.ui.hotkeyTree.expandAll()

    def hotkeyInsert(self, modifier):
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, modifier.title())
        for hotkey in self.db["hotkeys"][modifier]:
            subItem = QtWidgets.QTreeWidgetItem()
            subItem.setText(0, hotkey)
            subItem.setText(1, self.db["hotkeys"][modifier][hotkey].capitalize())
            item.addChild(subItem)
        if self.db["hotkeys"][modifier]:
            self.ui.hotkeyTree.addTopLevelItem(item)

    def hotkeySelect(self):
        item = self.ui.hotkeyTree.currentItem()
        if item:
            modifier = item.parent()
            if modifier:
                key = item.text(0)
                action = item.text(1)
                modifier = modifier.text(0)
                self.ui.hotkeyKeyLine.setText(f"{item.parent().text(0)} + {key}")
                self.ui.hotkeyActionCombo.setCurrentText(action)
            else:
                self.ui.hotkeyKeyLine.clear()
                self.ui.hotkeyActionCombo.setCurrentText('')
            self.ui.hotkeyDeleteButton.setEnabled(bool(modifier))

    def menuAddActions(self, actions, db, widgets):
        availableActions = {}
        for action in sorted(actions):
            icon = action.lower().replace(" ", "_")
            availableActions[action] = self.parent.icon[icon]

        for action in db:
            item = QtWidgets.QListWidgetItem(action)
            item.setIcon(availableActions[action])
            widgets[1].addItem(item)

        for action in availableActions:
            if action not in db:
                item = QtWidgets.QListWidgetItem(action)
                item.setIcon(availableActions[action])
                widgets[0].addItem(item)

    def menuAdd(self, widgets):
        item = widgets[0].currentItem()
        rowSelected = widgets[1].currentRow()
        if item:
            if item.text() == "(Separator)":
                separator = QtWidgets.QListWidgetItem("(Separator)")
                separator.setIcon(self.parent.icon["(separator)"])
                widgets[1].insertItem(rowSelected, separator)
            else:
                rowAvailable = widgets[0].currentRow()
                item = widgets[0].takeItem(rowAvailable)
                widgets[1].insertItem(rowSelected, item)
            widgets[1].setCurrentItem(item)

    def menuRemove(self, widgets):
        row = widgets[1].currentRow()
        item = widgets[1].takeItem(row)
        if item:
            if not item.text() == "(Separator)":
                widgets[0].addItem(item)
                widgets[0].setCurrentItem(item)

    def menuChildAdd(self):
        self.menuAdd((self.ui.menuChildAvailableList, self.ui.menuChildSelectedList))

    def menuChildRemove(self):
        self.menuRemove((self.ui.menuChildAvailableList, self.ui.menuChildSelectedList))

    def menuMotherAdd(self):
        self.menuAdd((self.ui.menuMotherAvailableList, self.ui.menuMotherSelectedList))

    def menuMotherRemove(self):
        self.menuRemove((self.ui.menuMotherAvailableList, self.ui.menuMotherSelectedList))

    def presetAdd(self):
        name = self.ui.presetNameLine.text()
        if not name:
            name = "Untitled style"

        if name in self.presetBuffer:
            foreground = self.presetBuffer[name][1]
            background = self.presetBuffer[name][2]
        else:
            foreground = self.preferences.query("styleDefault", "foreground")
            background = self.preferences.query("styleDefault", "background")

        if name in self.db["stylePresets"]:
            name = getNameIndex(name, self.db["stylePresets"])

        self.db["stylePresets"][name] = {}
        self.db["stylePresets"][name]["foreground"] = foreground
        self.db["stylePresets"][name]["background"] = background
        self.presetEnumerate(select=name)
        self.ui.presetNameLine.clear()

    def presetColorChanged(self, column):
        item = self.ui.presetTree.currentItem()
        color = self.colorWidget.currentColor()
        self.presetBuffer[item.text(0)][column] = color
        foreground = self.presetBuffer[item.text(0)][1]
        background = self.presetBuffer[item.text(0)][2]
        self.presetViewUpdate(foreground, background)

    def presetDelete(self):
        item = self.ui.presetTree.currentItem()
        if item:
            del self.db["stylePresets"][item.text(0)]
            index = self.ui.presetTree.indexOfTopLevelItem(item)
            self.ui.presetTree.takeTopLevelItem(index)

    def presetEnumerate(self, select=None):
        self.presetBuffer = {}
        self.ui.presetTree.clear()
        for style in self.db["stylePresets"]:
            background = self.db["stylePresets"][style]["background"]
            foreground = self.db["stylePresets"][style]["foreground"]
            item = QtWidgets.QTreeWidgetItem()
            item.setSizeHint(0, QtCore.QSize(0, 24))
            item.setText(0, style)
            item.setText(1, foreground)
            item.setText(2, background)
            item.setTextAlignment(1, QtCore.Qt.AlignCenter)
            item.setTextAlignment(2, QtCore.Qt.AlignCenter)
            self.presetBuffer[style] = {1: foreground, 2: background}
            self.ui.presetTree.addTopLevelItem(item)
            for i in range(3):
                item.setBackground(i, QtGui.QColor(background))
                item.setForeground(i, QtGui.QColor(foreground))
            if select == style:
                self.ui.presetTree.setCurrentItem(item)

    def presetPickColor(self, column, color):
        self.colorWidget = QtWidgets.QColorDialog(QtGui.QColor(color))
        self.colorWidget.setWindowFlags(self.colorWidget.windowFlags() | Qt.WindowStaysOnTopHint)
        self.colorWidget.currentColorChanged.connect(lambda: self.presetColorChanged(column))
        self.colorWidget.exec_()
        return self.colorWidget.selectedColor()

    def presetPickLayerColor(self, layer):
        item = self.ui.presetTree.currentItem()
        if item:
            lastColor = item.text(layer)
            color = self.presetPickColor(layer, item.text(layer))
            if color.isValid():
                self.presetBuffer[item.text(0)][layer] = color.name()
            else:
                self.presetBuffer[item.text(0)][layer] = lastColor
                self.presetSelect()

    def presetSave(self):
        item = self.ui.presetTree.currentItem()
        if item:
            name = item.text(0)
            foreground = self.presetBuffer[name][1].upper()
            background = self.presetBuffer[name][2].upper()
            for i in range(3):
                item.setBackground(i, QtGui.QColor(background))
                item.setForeground(i, QtGui.QColor(foreground))

            newName = self.ui.presetNameLine.text()
            if not newName:
                newName = name
            if not name == newName:
                if newName in self.db["stylePresets"]:
                    newName = getNameIndex(newName, self.db["stylePresets"])
                self.db["stylePresets"][newName] = self.db["stylePresets"].pop(name)
                self.presetBuffer[newName] = self.presetBuffer.pop(name)
            self.db["stylePresets"][newName]["foreground"] = foreground
            self.db["stylePresets"][newName]["background"] = background
            item.setText(0, newName)
            item.setText(1, foreground)
            item.setText(2, background)

    def presetSelect(self):
        item = self.ui.presetTree.currentItem()
        if item:
            self.presetViewUpdate(foreground=item.text(1), background=item.text(2))
            self.ui.presetNameLine.setText(item.text(0))
            self.ui.presetSaveButton.setEnabled(True)
            self.ui.presetDeleteButton.setEnabled(True)
            self.ui.presetForegroundButton.setEnabled(True)
            self.ui.presetBackgroundButton.setEnabled(True)
        else:
            self.ui.presetSaveButton.setEnabled(False)
            self.ui.presetDeleteButton.setEnabled(False)
            self.ui.presetForegroundButton.setEnabled(False)
            self.ui.presetBackgroundButton.setEnabled(False)

    def presetViewUpdate(self, foreground, background):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(background))
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor(foreground))
        self.ui.presetPreviewTextEdit.viewport().setPalette(palette)

    def settingsApply(self):
        # Set style of all children
        if self.ui.styleAllBox.isChecked():
            if self.origin == "Child":
                children = self.parent.parent.children
            elif self.origin == "Mother":
                children = self.parent.children

            for f in list(children):
                self.styleSave(children[f].profile)
                children[f].styleProfileLoad()

        # Update preferences database
        if self.origin == "Mother":
            frameChanged = not self.ui.framelessBox.isChecked() == self.preferences.query("general", "frameless")
            self.db["styleDefault"] = self.styleDefault
            self.settingsSave()
            self.parent.cssLoad()
        self.preferences.db = self.db
        self.preferences.save()

        # Update child attributes
        if self.origin == "Mother":
            if frameChanged:
                self.styleUpdateFrames()
            else:
                children = self.parent.children
                for f in list(children):
                    children[f].styleProfileLoad()

        elif self.origin == "Child":
            # Set style for current child
            self.styleSave(self.parent.profile)
            self.parent.resize(self.parent.profile.query("width"), self.parent.profile.query("height"))

    def settingsInitChild(self):
        self.styleDefault = copyDict(self.parent.profile.db[self.parent.fullname])
        self.setWindowTitle(f"Style for '{self.parent.fullname}'")
        self.setFixedSize(480, 200)
        self.ui.stackedWidget.setCurrentIndex(5)
        self.ui.sideMenuList.hide()
        self.ui.attributesGroupBox.hide()
        self.ui.framelessGroupBox.hide()
        self.ui.stylePreviewTextEdit.hide()

    def settingsInitMother(self):
        # General settings
        self.setFixedSize(640, 440)
        self.ui.resetButton.clicked.connect(self.settingsReset)

        # Default actions
        self.ui.actionTree.selectionModel().selectionChanged.connect(self.actionTreeSelect)
        self.ui.actionListCombo.currentTextChanged.connect(self.actionComboSelect)
        self.ui.actionSaveButton.clicked.connect(self.actionSave)

        # Hotkeys
        hotkeyActions = [''] + actionsChildBase + actionsChildHotkeys
        hotkeyActions.sort()
        self.ui.hotkeyActionCombo.addItems(hotkeyActions)
        self.ui.hotkeyKeyLine.installEventFilter(self)
        self.ui.hotkeyKeyLine.selectionChanged.connect(self.ui.hotkeyKeyLine.deselect)
        self.ui.hotkeyTree.selectionModel().selectionChanged.connect(self.hotkeySelect)
        self.ui.hotkeyDeleteButton.clicked.connect(self.hotkeyDelete)
        self.ui.hotkeyAddButton.clicked.connect(self.hotkeyAdd)
        self.ui.hotkeyClearButton.clicked.connect(self.hotkeyClear)

        # Style presets
        self.ui.presetTree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ui.presetTree.header().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.ui.presetTree.selectionModel().selectionChanged.connect(self.presetSelect)
        self.ui.presetBackgroundButton.clicked.connect(lambda: self.presetPickLayerColor(2))
        self.ui.presetForegroundButton.clicked.connect(lambda: self.presetPickLayerColor(1))
        self.ui.presetAddButton.clicked.connect(self.presetAdd)
        self.ui.presetSaveButton.clicked.connect(self.presetSave)
        self.ui.presetDeleteButton.clicked.connect(self.presetDelete)
        self.ui.presetSaveButton.setEnabled(False)
        self.ui.presetDeleteButton.setEnabled(False)
        self.ui.presetForegroundButton.setEnabled(False)
        self.ui.presetBackgroundButton.setEnabled(False)

        # Style default
        self.styleDefault = copyDict(self.preferences.db["styleDefault"])
        self.ui.framelessBorderButton.clicked.connect(self.stylePickBorderColor)

        # Style sheets
        configPath = os.path.expanduser("~/.config/qtpad/")
        self.css = {}
        self.ui.cssCombo.clear()
        for f in sorted(os.listdir(configPath)):
            if os.path.splitext(f)[1] == ".css":
                self.ui.cssCombo.addItem(f)
                with open(configPath + f) as stylesheet:
                    self.css[f] = stylesheet.read()
        self.ui.cssCombo.currentTextChanged.connect(self.cssFileChanged)
        self.ui.cssTextEdit.textChanged.connect(self.cssTextChanged)
        self.ui.cssRefreshButton.clicked.connect(self.cssRefresh)
        self.ui.cssRefreshButton.setIcon(self.parent.icon["reset_positions"])

        # Context menus
        self.ui.menuChildAvailableList.setIconSize(QtCore.QSize(16, 16))
        self.ui.menuChildSelectedList.setIconSize(QtCore.QSize(16, 16))
        self.ui.menuMotherAvailableList.setIconSize(QtCore.QSize(16, 16))
        self.ui.menuMotherSelectedList.setIconSize(QtCore.QSize(16, 16))
        self.ui.menuChildAddButton.clicked.connect(self.menuChildAdd)
        self.ui.menuMotherAddButton.clicked.connect(self.menuMotherAdd)
        self.ui.menuChildRemoveButton.clicked.connect(self.menuChildRemove)
        self.ui.menuMotherRemoveButton.clicked.connect(self.menuMotherRemove)

        # Setup side menu
        self.ui.stackedWidget.setCurrentIndex(self.parent.preferencesIndexes["menu"])
        self.ui.sideMenuList.item(self.parent.preferencesIndexes["menu"]).setSelected(True)
        self.ui.sideMenuList.selectionModel().selectionChanged.connect(self.settingsMenuSelect)

    def settingsLoad(self):
        # General settings
        self.ui.minimizeBox.setChecked(self.db["general"]["minimize"])
        self.ui.autoIndentBox.setChecked(self.db["general"]["autoIndent"])
        self.ui.deleteEmptyNotesBox.setChecked(self.db["general"]["deleteEmptyNotes"])
        self.ui.safeDeleteBox.setChecked(self.db["general"]["safeDelete"])
        self.ui.notesDbLine.setText(self.db["general"]["notesDb"])

        # Fetch clipboard
        self.ui.fetchClearBox.setChecked(self.db["general"]["fetchClear"])
        self.ui.fetchResizeBox.setChecked(self.db["general"]["fetchResize"])
        self.ui.fetchUrlBox.setChecked(self.db["general"]["fetchUrl"])
        self.ui.fetchFileBox.setChecked(self.db["general"]["fetchFile"])
        self.ui.fetchTxtBox.setChecked(self.db["general"]["fetchTxt"])

        # Hotkeys
        self.ui.hotkeyBox.setChecked(self.db["general"]["hotkeys"])
        self.hotkeyEnumerate()

        # Default actions
        self.ui.actionTree.clear()
        for widget in self.db["actions"]:
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, widget.capitalize())
            for trigger in self.db["actions"][widget]:
                action = self.db["actions"][widget][trigger]
                subItem = QtWidgets.QTreeWidgetItem()
                subItem.setText(0, trigger.capitalize())
                subItem.setText(1, action)
                if action == "Exec":
                    subItem.setText(2, self.db["exec"][widget][trigger])
                item.addChild(subItem)
            self.ui.actionTree.addTopLevelItem(item)
        self.ui.actionTree.expandAll()

        # Style presets
        self.presetEnumerate()

        # Style default
        font = QtGui.QFont()
        font.setFamily(self.styleDefault["fontFamily"])
        self.ui.styleFontFamilyCombo.setCurrentFont(font)
        self.ui.styleWidthBox.setValue(self.styleDefault["width"])
        self.ui.styleHeightBox.setValue(self.styleDefault["height"])
        self.ui.styleFontSizeBox.setValue(self.styleDefault["fontSize"])
        self.ui.styleOpacityBox.setValue(float(self.styleDefault["opacity"]))
        self.ui.stylePinBox.setChecked(self.db["styleDefault"]["pin"])
        self.ui.styleSizegripBox.setChecked(self.db["styleDefault"]["sizeGrip"])
        self.ui.nameTextLine.setText(self.db["general"]["nameText"])
        self.ui.nameImageLine.setText(self.db["general"]["nameImage"])
        self.ui.nameFormatTextLine.setText(self.db["general"]["nameFormatText"])
        self.ui.nameFormatImageLine.setText(self.db["general"]["nameFormatImage"])
        self.ui.framelessBox.setChecked(self.db["general"]["frameless"])
        self.ui.framelessBorderLabel.setStyleSheet("QLabel { background-color : " + self.db["general"]["borderColor"] + "; }")

        # Style sheets
        if self.origin == "Mother":
            currentCssFile = self.parent.preferencesIndexes["css"]
            if currentCssFile in self.css:
                self.ui.cssCombo.setCurrentText(currentCssFile)
                self.ui.cssTextEdit.setPlainText(self.css[currentCssFile])
            else:
                self.cssFileChanged()

        # Context menus
        self.ui.menuMotherSelectedList.clear()
        self.ui.menuMotherAvailableList.clear()
        self.ui.menuMotherAvailableList.addItem("(Separator)")
        self.ui.menuMotherAvailableList.item(0).setIcon(self.parent.icon["(separator)"])
        self.ui.menuChildSelectedList.clear()
        self.ui.menuChildAvailableList.clear()
        self.ui.menuChildAvailableList.addItem("(Separator)")
        self.ui.menuChildAvailableList.item(0).setIcon(self.parent.icon["(separator)"])

        menuWidgets = (self.ui.menuMotherAvailableList, self.ui.menuMotherSelectedList)
        menuActions = actionsMotherBase + actionsMotherMenu
        self.menuAddActions(actions=menuActions, db=self.db["menus"]["mother"], widgets=menuWidgets)

        menuWidgets = (self.ui.menuChildAvailableList, self.ui.menuChildSelectedList)
        menuActions = actionsChildBase + actionsChildMenu
        self.menuAddActions(actions=menuActions, db=self.db["menus"]["child"], widgets=menuWidgets)

    def settingsMenuSelect(self):
        index = self.ui.sideMenuList.currentRow()
        self.ui.stackedWidget.setCurrentIndex(index)
        self.parent.preferencesIndexes["menu"] = index

    def settingsReset(self):
        self.db["general"] = copyDict(PREFERENCES_DEFAULT["general"])
        self.db["actions"] = copyDict(PREFERENCES_DEFAULT["actions"])
        self.db["hotkeys"] = copyDict(PREFERENCES_DEFAULT["hotkeys"])
        self.db["menus"] = copyDict(PREFERENCES_DEFAULT["menus"])
        self.db["stylePresets"] = copyDict(PREFERENCES_DEFAULT["stylePresets"])
        self.db["styleDefault"] = copyDict(PREFERENCES_DEFAULT["styleDefault"])
        self.styleDefault = copyDict(PREFERENCES_DEFAULT["styleDefault"])
        self.css["frame.css"] = dictToCss(CSS_FRAME_DEFAULT)
        self.css["menu.css"] = dictToCss(CSS_MENU_DEFAULT)
        self.settingsLoad()

    def settingsSave(self):
        # General settings
        self.db["general"]["nameText"] = self.ui.nameTextLine.text()
        self.db["general"]["nameImage"] = self.ui.nameImageLine.text()
        self.db["general"]["nameFormatText"] = self.ui.nameFormatTextLine.text()
        self.db["general"]["nameFormatImage"] = self.ui.nameFormatImageLine.text()
        self.db["general"]["minimize"] = self.ui.minimizeBox.isChecked()
        self.db["general"]["autoIndent"] = self.ui.autoIndentBox.isChecked()
        self.db["general"]["safeDelete"] = self.ui.safeDeleteBox.isChecked()
        self.db["general"]["deleteEmptyNotes"] = self.ui.deleteEmptyNotesBox.isChecked()
        self.db["general"]["frameless"] = self.ui.framelessBox.isChecked()
        if not self.db["general"]["notesDb"] == self.ui.notesDbLine.text():
            self.generalSetPath(self.ui.notesDbLine.text())

        # Fetch clipboard
        self.db["general"]["fetchResize"] = self.ui.fetchResizeBox.isChecked()
        self.db["general"]["fetchClear"] = self.ui.fetchClearBox.isChecked()
        self.db["general"]["fetchUrl"] = self.ui.fetchUrlBox.isChecked()
        self.db["general"]["fetchFile"] = self.ui.fetchFileBox.isChecked()
        self.db["general"]["fetchTxt"] = self.ui.fetchTxtBox.isChecked()

        # Style default
        self.db["styleDefault"]["pin"] = self.ui.stylePinBox.isChecked()
        self.db["styleDefault"]["sizeGrip"] = self.ui.styleSizegripBox.isChecked()

        # Style sheets
        configPath = os.path.expanduser("~/.config/qtpad/")
        for f in self.css:
            with open(configPath + f, 'w') as stylesheet:
                stylesheet.write(self.css[f])

        # Hotkeys
        self.db["general"]["hotkeys"] = self.ui.hotkeyBox.isChecked()

        # Mother context menu
        menuMotherItems = []
        for item in range(self.ui.menuMotherSelectedList.count()):
            menuMotherItems.append(self.ui.menuMotherSelectedList.item(item).text())
        self.db["menus"]["mother"] = menuMotherItems

        # Child context menu
        menuChildItems = []
        for item in range(self.ui.menuChildSelectedList.count()):
            menuChildItems.append(self.ui.menuChildSelectedList.item(item).text())
        self.db["menus"]["child"] = menuChildItems

    def styleColorChanged(self, layer):
        color = self.colorWidget.currentColor()
        self.styleDefault[layer] = color.name()
        self.styleUpdateView()

    def stylePickBorderColor(self):
        currentColor = QtGui.QColor(self.db["general"]["borderColor"])
        color = self.stylePickColor(currentColor)
        if not color.isValid():
            color = QtGui.QColor(currentColor)
        self.ui.framelessBorderLabel.setStyleSheet("QLabel { background-color : " + color.name() + "; }")
        self.db["general"]["borderColor"] = color.name()

    def stylePickColor(self, color, layer=None):
        self.colorWidget = QtWidgets.QColorDialog(QtGui.QColor(color))
        self.colorWidget.setWindowFlags(self.colorWidget.windowFlags() | Qt.WindowStaysOnTopHint)
        if layer:
            self.colorWidget.currentColorChanged.connect(lambda: self.styleColorChanged(layer))
        self.colorWidget.exec_()
        return self.colorWidget.selectedColor()

    def stylePickLayerColor(self, layer):
        currentColor = self.styleDefault[layer]
        color = self.stylePickColor(currentColor, layer)
        if not color.isValid():
            color = QtGui.QColor(currentColor)
        self.styleDefault[layer] = color.name()
        self.styleUpdateView()

    def styleSave(self, profile):
        profile.load()
        profile.set("width", self.styleDefault["width"])
        profile.set("height", self.styleDefault["height"])
        profile.set("background", self.styleDefault["background"])
        profile.set("foreground", self.styleDefault["foreground"])
        profile.set("fontSize", self.styleDefault["fontSize"])
        profile.set("fontFamily", self.styleDefault["fontFamily"])
        profile.set("opacity", self.styleDefault["opacity"])
        profile.save()

    def styleUpdateFontFamily(self):
        self.styleDefault["fontFamily"] = self.ui.styleFontFamilyCombo.currentText()
        self.styleUpdateView()

    def styleUpdateFontSize(self):
        self.styleDefault["fontSize"] = self.ui.styleFontSizeBox.value()
        self.styleUpdateView()

    def styleUpdateFrames(self):
        # Override of window manager frame
        for name in self.parent.children:
            isVisible = self.parent.children[name].isVisible()
            self.parent.children[name].noteStateUpdate(updateFrame=True)
            time.sleep(0.1)
            if isVisible:
                self.parent.children[name].noteDisplay()

    def styleUpdateHeight(self):
        self.styleDefault["height"] = self.ui.styleHeightBox.value()
        self.styleUpdateView()

    def styleUpdateOpacity(self):
        self.styleDefault["opacity"] = self.ui.styleOpacityBox.value()
        self.styleUpdateView()

    def styleUpdateView(self):
        font = QtGui.QFont()
        font.setPointSize(self.styleDefault["fontSize"])
        font.setFamily(self.styleDefault["fontFamily"])

        if self.origin == "Mother":
            background = QtGui.QColor(self.styleDefault["background"])
            foreground = QtGui.QColor(self.styleDefault["foreground"])
            palette = self.ui.stylePreviewTextEdit.viewport().palette()
            palette.setColor(QtGui.QPalette.Base, background)
            palette.setColor(QtGui.QPalette.Text, foreground)
            self.ui.stylePreviewTextEdit.setFont(font)
            self.ui.stylePreviewTextEdit.viewport().setPalette(palette)

        elif self.origin == "Child":
            self.parent.ui.textEdit.setFont(font)
            self.parent.resize(self.styleDefault["width"], self.styleDefault["height"])
            self.parent.styleSetColors(self.styleDefault["background"], self.styleDefault["foreground"], updateProfile=False)
            self.parent.setWindowOpacity(float(self.styleDefault["opacity"]))

    def styleUpdateWidth(self):
        self.styleDefault["width"] = self.ui.styleWidthBox.value()
        self.styleUpdateView()


class ProfileDatabase(object):
    def __init__(self, parent):
        self.name = parent.fullname
        self.preferences = parent.parent.preferences
        PROFILES_FILE = os.path.expanduser("~/.config/qtpad/profiles.json")

        if os.path.isfile(PROFILES_FILE) and os.stat(PROFILES_FILE).st_size > 0:
            self.load()
        else:
            self.db = {}

        if self.name not in self.db:
            # Create a new profile and position the widget
            self.db[self.name] = copyDict(self.preferences.db["styleDefault"])

            if parent.extension == ".png":
                image = QtGui.QPixmap(parent.path)
                self.db[self.name]["width"] = image.width()
                self.db[self.name]["height"] = image.height()

            available = QtWidgets.QDesktopWidget().availableGeometry()
            position = parent.frameGeometry()
            position.moveCenter(available.center())
            x = position.x() + random.randint(-256,256)
            y = position.y() + random.randint(-128,128)
            self.db[self.name]["x"] = x
            self.db[self.name]["y"] = y

            with open(PROFILES_FILE, 'w') as f:
                f.write(json.dumps(self.db, indent=2, sort_keys=False))
            logger.info(f"Created profile for '{self.name}'")

    def load(self):
        with open(PROFILES_FILE) as f:
            self.db = json.load(f)
        logger.info(f"Loaded profiles database ({self.name})")

    def query(self, *keys, db=None):
        if not db: db = self.db[self.name]
        for key in keys:
            try:
                db = db[key]
            except KeyError:
                logger.error(f"Profile KeyError: '{key}' not found ({self.name})")
                logger.warning(f"Restored broken profile to default ({self.name})")
                self.db[self.name] = copyDict(PREFERENCES_DEFAULT["styleDefault"])
                self.save()
                return self.db[self.name][key]
        return db

    def save(self, entry=None, value=None):
        if entry and value is not None:
            self.load()
            self.set(entry, value)

        with open(PROFILES_FILE, "w") as f:
            f.write(json.dumps(self.db, indent=2, sort_keys=False))
        logger.info(f"Saved profile database ({self.name})")

    def set(self, entry, value):
        if self.name in self.db:
            self.db[self.name][entry] = value
        else:
            self.db[self.name] = {}
