#!/usr/bin/python3
import json
import os
import sys
from PyQt5 import QtGui, QtWidgets, QtCore, uic
from PyQt5.QtCore import Qt

try:
    import qtpad.gui_child
    from qtpad.preferences import PreferencesForm, ProfileDatabase
    from qtpad.common import *
except ImportError:
    from preferences import PreferencesForm, ProfileDatabase
    from common import *

# Init common settings
LOCAL_DIR, ICONS_DIR, PREFERENCES_FILE, PROFILES_FILE = getStaticPaths()
logger = getLogger()


class Child(QtWidgets.QWidget):
    def __init__(self, parent, path, popup=False, image=None, text=None):
        super().__init__()

        # Load ui file if pre-compile ui is unavailable
        if "qtpad.gui_child" in sys.modules:
            self.ui = qtpad.gui_child.Ui_Form()
            self.ui.setupUi(self)
        else:
            self.ui = uic.loadUi(LOCAL_DIR + 'gui_child.ui', self)

        # Set path and filetype
        notesDir = parent.preferences.query("general", "notesDb")
        self.path = path
        self.extension = os.path.splitext(path)[1]
        self.fullname = path[len(notesDir):-len(self.extension)]
        self.shortname = self.fullname.rsplit("/", 1)[-1]
        self.folder = path[len(notesDir):-len(self.shortname)-len(self.extension)]

        # Load common settings
        self.parent = parent
        self.preferences = parent.preferences
        self.icon = parent.icon
        self.profile = ProfileDatabase(self)
        self.ui.titleLabel.setText(self.fullname)
        self.modifier = {"ctrl": False, "shift": False, "ctrl + shift": False}

        # Format title
        self._noteTitleUpdate()

        # Hide window from system taskbar
        if os.environ.get('DESKTOP_SESSION') == "openbox":
            self.setAttribute(Qt.WA_X11NetWmWindowTypeToolBar)
        else:
            self.setAttribute(Qt.WA_X11NetWmWindowTypeUtility)

        # Save widget size only once the resize event is done
        self.saveTimer = QtCore.QTimer(singleShot=True)
        self.saveTimer.timeout.connect(self._styleSaveGeometry)

        # Init frame events
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.titleLabel.mousePressEvent = self._noteFrameMousePressEvent
        self.ui.titleLabel.mouseMoveEvent = self._noteFrameMouseMoveEvent
        self.sizeGrip = QtWidgets.QSizeGrip(self)
        self.ui.bottomLayout.addWidget(self.sizeGrip)
        self.ui.bottomLayout.setAlignment(self.sizeGrip, Qt.AlignRight)
        self.ui.bottomLabel.installEventFilter(self)
        self.ui.titleLabel.installEventFilter(self)
        self.ui.iconLabel.installEventFilter(self)

        # Init context menus
        self.menu = QtWidgets.QMenu()
        self.menu.aboutToShow.connect(self._menuRefresh)
        self.styleMenu = QtWidgets.QMenu("Style")
        self.styleMenu.setIcon(self.icon["style"])
        self.moveMenu = QtWidgets.QMenu("Move to folder...")
        self.moveMenu.setIcon(self.icon["folder_active"])

        # Apply settings and display children
        if image:
            self._noteImageInit(image)
        else:
            self._noteTextInit(text)
        self.noteStateUpdate(updateFrame=True)
        if popup or self.profile.query("pin") or not self.preferences.query("general", "minimize"):
            self.noteDisplay(updateState=False)

    def closeEvent(self, event):
        if self.fullname:
            logger.info(f"Closed '{self.fullname}'")
            action = self.preferences.query("actions", "events", "close button")
            self._noteAction(action)
            if action == "Hide":
                event.ignore()

            # Remove empty notes
            if self.extension == ".txt":
                if self.preferences.query("general", "deleteEmptyNotes") and self.ui.textEdit.toPlainText() == "":
                    logger.warning(f"Removed '{self.fullname}' (empty)")
                    self.noteDelete()

    def eventFilter(self, obj, event):
        eventType = event.type()

        # Text only events
        if obj == self.ui.textEdit.viewport():
            if eventType == QtCore.QEvent.Drop:
                QtWidgets.QPlainTextEdit.dropEvent(self.ui.textEdit, event)
                self.noteTextSave()
                return True

        elif obj == self.ui.textEdit:
            if eventType == QtCore.QEvent.KeyPress:
                if self._noteTextIndent(event):
                    return True

            elif eventType == QtCore.QEvent.KeyRelease:
                self._noteTextChangeIndicator()

            elif eventType == QtCore.QEvent.Show:
                self.parent.lastActive = self

            elif eventType == QtCore.QEvent.FocusIn:
                self.parent.lastActive = self
                self._noteTextLoad(self.fullname)

            elif eventType == QtCore.QEvent.FocusOut:
                if self.fullname:
                    self.noteTextSave()

        # Actions events
        if obj == self.ui.bottomLabel:
            self._noteBorderEvent("bottom border", event)

        elif obj == self.ui.iconLabel or obj == self.ui.titleLabel:
            self._noteBorderEvent("top border", event)

        # Hotkeys events
        if obj == self.ui.textEdit.viewport() or obj == self.ui.imageLabel:
            if eventType == QtCore.QEvent.Wheel or eventType == QtCore.QEvent.MouseButtonPress:
                if self._hotkeySpecial(event):
                    return True

        if obj == self.ui.textEdit or obj == self.ui.imageLabel:
            if eventType == QtCore.QEvent.KeyPress or eventType == QtCore.QEvent.KeyRelease:
                self.modifier["ctrl"] = (event.modifiers() == Qt.ControlModifier)
                self.modifier["shift"] = (event.modifiers() == Qt.ShiftModifier)
                self.modifier["ctrl + shift"] = int(event.modifiers()) == (Qt.ControlModifier + Qt.ShiftModifier)

            if eventType == QtCore.QEvent.KeyPress:
                if self._hotkeyParse(event):
                    return True

        if eventType == QtCore.QEvent.Resize:
            # Workaround to avoid saving geometry after each pixel update
            self._noteTitleUpdate()
            self.saveTimer.start(400)

        elif eventType == QtCore.QEvent.FocusOut:
            self._styleSaveGeometry()

        return QtCore.QObject.event(obj, event)

    def paintEvent(self, event):
        # Draw a border for FramelessWindowHint
        if self.preferences.query("general", "frameless"):
            borderColor = QtGui.QColor(self.preferences.query("general", "borderColor"))
            painter = QtGui.QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QtGui.QBrush(borderColor))
            painter.drawRect(0, 0, self.width(), self.height())

    def _folderPrompt(self):
        msg = QtWidgets.QInputDialog()
        msg.setInputMode(QtWidgets.QInputDialog.TextInput)
        msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
        msg.setWindowTitle(f"Move '{self.fullname}'")
        msg.setLabelText("Enter the folder name:")
        msg.setFixedSize(250, 100)
        accept = msg.exec_()
        folder = msg.textValue()
        folder = sanitizeString(folder)
        if accept and folder and not folder == self.folder[:-1]:
            self.noteMove(folder)

    def _hotkeyForceRelease(self):
        ctrlReleaseEvent = QtGui.QKeyEvent(QtCore.QEvent.KeyRelease, Qt.Key_Control, Qt.ControlModifier)
        QtCore.QCoreApplication.postEvent(self.ui.textEdit, ctrlReleaseEvent)

    def _hotkeyParse(self, event):
        if self.preferences.query("general", "hotkeys"):
            hotkeys = self.preferences.db["hotkeys"]
            key = QtGui.QKeySequence(event.key()).toString()
            for modifier in hotkeys:
                if self.modifier.get(modifier):
                    for hotkey in hotkeys[modifier]:
                        if key == hotkey:
                            self._hotkeyForceRelease()
                            return self._noteAction(hotkeys[modifier][hotkey])
        return False

    def _hotkeySpecial(self, event):
        if self.preferences.query("general", "hotkeys"):
            hotkeys = self.preferences.db["hotkeys"]
            if event.type() == QtCore.QEvent.Wheel:
                if int(event.angleDelta().y()) > 0:
                    trigger = "Wheel Up"
                else:
                    trigger = "Wheel Down"
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    trigger = "Left click"
                elif event.button() == Qt.RightButton:
                    trigger = "Right click"  # Unused
                elif event.button() == Qt.MiddleButton:
                    trigger = "Middle click"

            for modifier in hotkeys:
                if hotkeys[modifier].get(trigger) and self.modifier[modifier]:
                    if not event.type() == QtCore.QEvent.Wheel:
                        self._hotkeyForceRelease()
                    return self._noteAction(hotkeys[modifier][trigger])

    def _menuAddOption(self, option):
        option = option.lower()
        icon = self.icon.get(option.replace(" ", "_"))

        if option == "(separator)":
            self.menu.addSeparator()

        elif option == "cut line":
            self.menu.addAction(icon, 'Cut line', lambda: self._noteTextAction("cut line"))

        elif option == "cut":
            self.menu.addAction(icon, 'Cut', lambda: self._noteTextAction("cut"))

        elif option == "copy line":
            self.menu.addAction(icon, 'Copy line', lambda: self._noteTextAction("copy line"))

        elif option == "copy":
            self.menu.addAction(icon, 'Copy', lambda: self._noteTextAction("copy"))

        elif option == "paste":
            self.menu.addAction(icon, 'Paste', lambda: self._noteTextAction("paste"))

        elif option == "undo":
            self.menu.addAction(icon, 'Undo', self.ui.textEdit.undo)

        elif option == "redo":
            self.menu.addAction(icon, 'Redo', self.ui.textEdit.redo)

        elif option == "hide":
            self.menu.addAction(icon, 'Hide', self.hide)

        elif option == "pin":
            self.menu.addAction(icon, 'Pin', self._notePin)

        elif option == "rename":
            self.menu.addAction(icon, 'Rename', self._noteRenamePrompt)

        elif option == "selection to lowercase":
            self.menu.addAction(icon, 'Selection to lowercase', lambda: self._noteAction("selection to lowercase"))

        elif option == "selection to uppercase":
            self.menu.addAction(icon, 'Selection to uppercase', lambda: self._noteAction("selection to uppercase"))

        elif option == "sort selection":
            self.menu.addAction(icon, 'Sort selection', lambda: self._noteTextAction("sort selection"))

        elif option == "toggle wordwrap":
            self.menu.addAction(icon, 'Toggle word wrap', self._noteTextWrap)

        elif option == "special paste":
            self.menu.addAction(icon, 'Special paste', lambda: self._noteAction("special paste"))

        elif option == "toggle sizegrip":
            self.menu.addAction(icon, 'Toggle sizegrip', lambda: self._noteAction("toggle sizegrip"))

        elif option == "new note":
            self.menu.addAction(icon, 'New note', lambda: self.parent.noteAction("New note"))

        elif option == "delete":
            self.menu.addAction(icon, 'Delete', self.noteDelete)

        elif option == "search":
            self.menu.addAction(icon, 'Search', lambda: self._noteAction("search"))

        elif option == "copy to clipboard":
            if self.extension == ".png":
                self.menu.addAction(icon, 'Copy to clipboard', self._noteImageToClipboard)

        elif option == "save as":
            if self.extension == ".txt":
                self.menu.addAction(icon, 'Save text as', self._noteTextToFile)
            elif self.extension == ".png":
                self.menu.addAction(icon, 'Save image as', self._noteImageToFile)

        elif option == "style":
            self._menuStyle()
            self.menu.addMenu(self.styleMenu)

        elif option == "move to folder":
            self._menuFolders()

        else:
            logger.error(f"Invalid child menu option '{option}'")

    def _menuRefresh(self):
        self.menu.clear()
        for option in self.preferences.query("menus", "child"):
            self._menuAddOption(option)

    def _menuStyle(self):
        self.styleMenu.clear()
        # Load style presets and replace transparency with background color, foreground with 'foreground'
        for entry in self.preferences.db["stylePresets"]:
            bg = self.preferences.db["stylePresets"][entry]["background"]
            fg = self.preferences.db["stylePresets"][entry]["foreground"]
            pixmap = QtGui.QPixmap(ICONS_DIR + "rename.svg")
            painter = QtGui.QPainter(pixmap)
            painter.setCompositionMode(painter.CompositionMode_Xor)
            painter.fillRect(pixmap.rect(), QtGui.QColor(bg))
            painter.setCompositionMode(painter.CompositionMode_Overlay)
            painter.fillRect(pixmap.rect(), QtGui.QColor(fg))
            painter.end()
            icon = QtGui.QIcon(pixmap)
            self.styleMenu.addAction(icon, entry, lambda bg=bg, fg=fg: self.styleSetColors(bg, fg, updateProfile=True))
        self.styleMenu.addSeparator()
        self.styleMenu.addAction(self.icon["preferences"], "Customize", lambda: PreferencesForm(self))
        self.styleMenu.addAction(self.icon["preferences"], "Set as default", self._styleSetDefault)
        self.styleMenu.addAction(self.icon["preferences"], "Save current style", self._styleAddPreset)

    def _menuFolders(self):
        notesDir = self.preferences.query("general", "notesDb")
        self.moveMenu.clear()
        self.parent.folderLoadEnabled()  # Make sure each folders have a key in preferences database
        for folder in self.parent.folderList(notesDir):
            if not folder == self.folder[:-1]:
                self.moveMenu.addAction(self.icon["folder_active"], folder, lambda folder=folder: self.noteMove(folder))
        self.moveMenu.addSeparator()
        if self.folder:
            self.moveMenu.addAction(self.icon["hide"], "None", self.noteMove)
        self.moveMenu.addAction(self.icon["preferences"], "New folder", self._folderPrompt)
        self.menu.addMenu(self.moveMenu)

    def _noteAction(self, action):
        action = action.lower()

        if action == "none":
            pass

        elif action == "toggle sizegrip":
            if self.sizeGrip.isVisible():
                self.sizeGrip.hide()
                self.ui.bottomLabel.hide()
                self.profile.save("sizeGrip", False)
            else:
                self.sizeGrip.show()
                self.ui.bottomLabel.show()
                self.profile.save("sizeGrip", True)

        elif action == "special paste":
            txt = self.parent.clipboard.text()
            txt = txt.replace("\n", " ")
            txt = txt.replace("\t", " ")
            self.ui.textEdit.insertPlainText(txt)

        elif action == "selection to uppercase":
            cursor = self.ui.textEdit.textCursor()
            cursor.insertText(cursor.selectedText().upper())

        elif action == "selection to lowercase":
            cursor = self.ui.textEdit.textCursor()
            cursor.insertText(cursor.selectedText().lower())

        elif action == "delete line":
            self._noteTextAction("delete")

        elif action == "duplicate line":
            self._noteTextAction("duplicate")

        elif action == "shift line up":
            self._noteTextAction("shift up")

        elif action == "shift line down":
            self._noteTextAction("shift down")

        elif action == "indent increase":
            self._noteTextAction("indent increase")

        elif action == "indent decrease":
            self._noteTextAction("indent decrease")

        elif action == "sort selection":
            self._noteTextAction("sort selection")

        elif action == "toggle wordwrap":
            self._noteTextWrap()

        elif action == "zoom increase":
            self._noteResize(20)

        elif action == "zoom decrease":
            self._noteResize(-20)

        elif action == "rename":
            self._noteRenamePrompt()

        elif action == "save":
            self.noteTextSave()

        elif action == "pin":
            self._notePin()

        elif action == "hide":
            self.hide()

        elif action == "new note":
            self.parent.noteAction("New note")

        elif action == "unload":
            if self.folder:
                self.parent.noteUnload(self)
            else:
                self.hide()

        elif action == "delete":
            self.noteDelete()

        elif action == "cut line":
            self._noteTextAction("cut line")

        elif action == "cut":
            self._noteTextAction("cut")

        elif action == "copy line":
            self._noteTextAction("copy line")

        elif action == "copy":
            self._noteTextAction("copy")

        elif action == "paste":
            self._noteTextAction("paste")

        elif action == "undo":
            self.ui.textEdit.undo()

        elif action == "redo":
            self.ui.textEdit.redo()

        elif action == "opacity increase":
            self._noteOpacity(0.02)

        elif action == "opacity decrease":
            self._noteOpacity(-0.02)

        elif action == "save as":
            if self.extension == ".txt":
                self._noteTextToFile()
            elif self.extension == ".png":
                self._noteImageToFile()

        elif action == "search":
            if self.extension == ".txt":
                selection = self.ui.textEdit.textCursor().selectedText()
                self.parent.searchForm.ui.searchFindLine.setText(selection)
                self.parent.searchForm.show()
                self.parent.searchForm.activateWindow()
                self.parent.searchForm.ui.searchFindLine.setFocus()
                self.parent.searchForm.ui.searchFindLine.selectAll()

        else:
            logger.error(f"Invalid hotkey action '{action}'")
            return False
        return True

    def _noteBorderEvent(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self._noteAction(self.preferences.query("actions", obj, "left click"))
            elif event.button() == Qt.RightButton:
                self._noteAction(self.preferences.query("actions", obj, "right click"))
            elif event.button() == Qt.MiddleButton:
                self._noteAction(self.preferences.query("actions", obj, "middle click"))
        elif event.type() == QtCore.QEvent.Wheel:
            if int(event.angleDelta().y()) > 0:
                self._noteAction(self.preferences.query("actions", obj, "wheel up"))
            else:
                self._noteAction(self.preferences.query("actions", obj, "wheel down"))

    def _noteFrameMouseMoveEvent(self, event):
        # Mouse dragging for frameless windows
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def _noteFrameMousePressEvent(self, event):
        # Mouse dragging for frameless windows
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def _noteImageInit(self, image):
        self.ui.textEdit.hide()
        self.ui.imageLabel.installEventFilter(self)
        self.ui.imageLabel.setScaledContents(True)
        self.ui.imageLabel.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.imageLabel.customContextMenuRequested.connect(lambda: self.menu.popup(QtGui.QCursor.pos()))
        self.ui.imageLabel.setFocusPolicy(Qt.StrongFocus)
        if os.path.isfile(self.path):
            image = QtGui.QPixmap(self.path)
            width, height = image.width(), image.height()
        else:
            f = QtCore.QFile(self.path)
            f.open(QtCore.QIODevice.WriteOnly)
            image.save(f, "PNG")
            width, height = image.width(), image.height()

        # Load the image file and set the widget size
        if self.preferences.query("general", "fetchResize"):
            widthMax = round(QtWidgets.QDesktopWidget().screenGeometry().width() * 0.8)
            heightMax = round(QtWidgets.QDesktopWidget().screenGeometry().height() * 0.8)
            if width > widthMax:
                width = widthMax
            if height > heightMax:
                height = heightMax
        self.ui.imageLabel.setPixmap(image.scaled(width, height, Qt.KeepAspectRatio))

    def _noteImageToClipboard(self):
        self.parent.clipboard.setPixmap(self.ui.imageLabel.pixmap())

    def _noteOpacity(self, increment):
        opacity = float(self.profile.query("opacity")) + increment
        if opacity > 1.0:
            opacity = 1.0
        elif opacity < 0.1:
            opacity = 0.1

        if not opacity == self.profile.query("opacity"):
            self.setWindowOpacity(opacity)
            self.profile.save("opacity", opacity)

    def _noteImageToFile(self):
        saveWidget = QtWidgets.QFileDialog.getSaveFileName(self, "Save image as", self.fullname, ".png")
        path = saveWidget[0]
        if path:
            path += ".png"
            f = QtCore.QFile(path)
            f.open(QtCore.QIODevice.WriteOnly)
            self.ui.imageLabel.pixmap().save(f, "PNG")

    def _notePin(self):
        self.profile.save("pin", not self.profile.query("pin"))
        self.noteDisplay(updatePosition=False)

    def _noteRename(self, name, folder, soft=False):
        notesDir = self.preferences.query("general", "notesDb")

        # Append new folder to name (if any)
        if folder:
            name = folder + "/" + name

        # Handle name conflicts
        if not soft and os.path.isdir(notesDir + folder):
            noteList = os.listdir(notesDir + folder)
            if folder:
                noteList = list(map(lambda name: folder + "/" + name, noteList))
                noteList = list(map(lambda name: name.rstrip(self.extension), noteList))
            if name in noteList:
                name = getNameIndex(name, noteList)

        try:
            if not soft:
                os.renames(self.path, (notesDir + name + self.extension))
        except OSError:
            logger.error("Could not rename file (name too long?)")
        except FileNotFoundError:
            logger.error(f"File not found ({self.path})")
        else:
            oldName = self.fullname
            self.path = notesDir + name + self.extension
            self.fullname = self.path[len(notesDir):-len(self.extension)]
            self.shortname = self.fullname.rsplit("/", 1)[-1]
            self.folder = self.path[len(notesDir):-len(self.shortname)-len(self.extension)]

            # Replace name in profiles database
            with open(PROFILES_FILE, "r+") as db:
                profiles = json.load(db)
                profiles[name] = profiles.pop(oldName)
                db.seek(0)
                db.truncate()
                db.write(json.dumps(profiles, indent=2, sort_keys=False))

            # Replace name in children list
            self.parent.children[name] = self.parent.children.pop(oldName)

            # Update child proprieties
            logger.info(f"Renamed '{oldName}' to '{self.fullname}'")
            self.profile.path = self.path
            self.profile.name = self.fullname
            self._noteTitleUpdate()

            # Change name in active list
            if oldName in self.preferences.db["actives"]:
                self.preferences.db["actives"].remove(oldName)
                self.preferences.db["actives"].append(self.fullname)
                self.preferences.set("actives", self.preferences.db["actives"])

            # Update profile database
            self.profile.load()

    def _noteRenamePrompt(self):
        msg = QtWidgets.QInputDialog()
        msg.setInputMode(QtWidgets.QInputDialog.TextInput)
        msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
        msg.setWindowTitle(f"Rename '{self.fullname}'")
        msg.setLabelText("Enter the new name:")
        msg.setTextValue(self.shortname)
        msg.setFixedSize(250, 100)
        accept = msg.exec_()
        newName = msg.textValue()
        newName = sanitizeString(newName)
        if accept and newName and not newName == self.fullname:
            self._noteRename(newName, folder=self.folder.rstrip("/"))

    def _noteResize(self, sizeIncrement):
        if sizeIncrement > 0:
            fontIncrement = 1
        else:
            fontIncrement = -1

        if self.extension == ".txt":
            font = self.ui.textEdit.font()
            size = font.pointSize() + fontIncrement
            if size < 7:
                size = 7
            font.setPointSize(size)
            self.ui.textEdit.setFont(font)
            self.profile.save("fontSize", size)

        elif self.extension == ".png":
            width, height = self.width() + sizeIncrement, self.height() + sizeIncrement
            if 'width' in locals() and width > 50:
                self.resize(width, self.height())
            if 'height' in locals() and height > 50:
                self.resize(self.width(), height)

    def _noteTextAction(self, action):
        savedLineWrapMode = bool(self.ui.textEdit.lineWrapMode())
        self._noteTextWrap(False)
        cursor = self.ui.textEdit.textCursor()

        if action == "paste":
            cursor.insertText(self.parent.clipboard.text())

        elif action == "copy":
            self.parent.clipboard.setText(cursor.selectedText())

        elif action == "cut":
            self.parent.clipboard.setText(cursor.selectedText())
            cursor.removeSelectedText()

        else:
            # Save initial selection
            hasSelection = cursor.hasSelection()
            initialSelectedText = cursor.selectedText()
            initialSelectionStart = cursor.selectionStart()
            initialSelectionEnd = cursor.selectionEnd()

            # Extend selection, save content and selection borders
            linesCount = cursor.selectedText().count("\u2029") + 1  # \u2029 is unicode for \n
            if linesCount > 1:
                selectionEnd = cursor.selectionEnd()
                cursor.setPosition(cursor.selectionStart())
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                selectionStart = cursor.position()
                cursor.setPosition(selectionEnd, QtGui.QTextCursor.KeepAnchor)
                cursor.movePosition(QtGui.QTextCursor.EndOfLine, QtGui.QTextCursor.KeepAnchor)
                selectionEnd = cursor.position()
                selectedText = cursor.selectedText()
            else:
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                selectionStart = cursor.position()
                cursor.movePosition(QtGui.QTextCursor.EndOfLine, QtGui.QTextCursor.KeepAnchor)
                selectionEnd = cursor.position()
                selectedText = cursor.selectedText()

        if action == "paste line":
            cursor.insertText(self.parent.clipboard.text())

        elif action == "copy line":
            self.parent.clipboard.setText(cursor.selectedText())
            cursor.setPosition(initialSelectionStart)

        elif action == "cut line":
            self.parent.clipboard.setText(cursor.selectedText())
            self._noteTextAction("delete")

        elif action == "delete":
            if cursor.atEnd():
                cursor.movePosition(QtGui.QTextCursor.EndOfLine)
                cursor.movePosition(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.KeepAnchor)
                cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.KeepAnchor)
            else:
                cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor)
            cursor.removeSelectedText()

        elif action == "duplicate":
            cursor.insertText(selectedText + "\n" + selectedText)
            cursor.setPosition(initialSelectionStart)

        elif action == "shift up":
            # Remove selected text
            cursor.removeSelectedText()
            cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.KeepAnchor)

            # Save and remove newline character
            newline = cursor.selectedText()
            cursor.removeSelectedText()

            # Insert saved text
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            cursor.insertText(selectedText + newline)

            # Select inserted text
            cursor.movePosition(QtGui.QTextCursor.Up, n=linesCount)
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor, n=len(selectedText))

        elif action == "shift down":
            # Remove selected text
            cursor.removeSelectedText()
            cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor)

            # Save and remove newline character
            newline = cursor.selectedText()
            cursor.removeSelectedText()

            # Insert saved text
            cursor.movePosition(QtGui.QTextCursor.EndOfLine)
            cursor.insertText(newline + selectedText)

            # Select inserted text
            cursor.movePosition(QtGui.QTextCursor.EndOfLine)
            cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.KeepAnchor, n=len(selectedText))

        elif action == "indent increase":
            # Add one tab before every line
            newText = []
            for line in selectedText.splitlines(True):
                newText.append("\t" + line)
            newText = "".join(newText)
            cursor.insertText(newText)

            # Restore selection
            cursor.setPosition(selectionStart)
            cursor.setPosition(selectionEnd+linesCount, QtGui.QTextCursor.KeepAnchor)

        elif action == "indent decrease":
            # Remove one tab before every line (if any)
            newText = []
            tabsCount = 0
            for line in selectedText.splitlines(True):
                if line[:1] == "\t":
                    line = line[1:]
                    tabsCount += 1
                elif line[:4] == "    ":
                    line = line[4:]
                    tabsCount += 4
                newText.append(line)
            newText = "".join(newText)
            cursor.insertText(newText)

            # Restore selection
            cursor.setPosition(selectionStart)
            cursor.setPosition(selectionEnd-tabsCount, QtGui.QTextCursor.KeepAnchor)

        elif action == "sort selection":
            # Sort either the whole line or a partial selection
            if hasSelection:
                selectedText = initialSelectedText
                selectionStart = initialSelectionStart
                selectionEnd = initialSelectionEnd
                cursor.setPosition(selectionStart)
                cursor.setPosition(selectionEnd, QtGui.QTextCursor.KeepAnchor)

            # Determine how to split the text
            if linesCount > 1:
                separator = "\u2029"
            elif selectedText.count(" ") > 0:
                separator = " "
            else:
                separator = ""

            # Determine direction, split and sort
            newText = []
            if separator:
                sortedList = sorted(selectedText.split(separator))
                if sortedList == selectedText.split(separator):
                    sortedList = sorted(selectedText.split(separator), reverse=True)
                for item in sortedList:
                    newText.append(item + separator)
                newText = separator.join(sortedList)
            else:
                direction = (sorted(list(selectedText)) == list(selectedText))
                sortedList = sorted(list(selectedText), reverse=direction)
                newText = "".join(sortedList)

            # Insert the result and restore previous selection
            cursor.insertText(newText)
            cursor.setPosition(selectionStart)
            cursor.setPosition(selectionEnd, QtGui.QTextCursor.KeepAnchor)

        self.ui.textEdit.setTextCursor(cursor)
        self._noteTextWrap(savedLineWrapMode)

    def _noteTextChangeIndicator(self):
        # Indicate unsaved changes in title with an asterisk* suffix
        if self.ui.textEdit.isVisible() and os.path.isfile(self.path):
            with open(self.path) as f:
                content = f.read()
            isSame = (content == self.ui.textEdit.toPlainText())
            asterisk = (self.windowTitle()[-1] == "*" or self.ui.titleLabel.text()[-1] == "*")
            if asterisk and isSame:
                self.setWindowTitle(self.windowTitle()[:-1])
                self.ui.titleLabel.setText(self.ui.titleLabel.text()[:-1])
            elif not asterisk and not isSame:
                self.setWindowTitle(self.windowTitle() + "*")
                self.ui.titleLabel.setText(self.ui.titleLabel.text() + "*")

    def _noteTextIndent(self, event):
        if self.preferences.query("general", "autoIndent"):
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                cursor = self.ui.textEdit.textCursor()
                position = cursor.position()
                cursor.movePosition(QtGui.QTextCursor.EndOfLine, QtGui.QTextCursor.KeepAnchor)

                # If cursor is at the end of the line
                if not cursor.selectedText():
                    # Get indent of current line
                    savedLineWrapMode = bool(self.ui.textEdit.lineWrapMode())
                    ##scrollPosition = self.ui.textEdit.verticalScrollBar().value()
                    self._noteTextWrap(False)
                    cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                    self._noteTextWrap(savedLineWrapMode)
                    ##self.ui.textEdit.verticalScrollBar().setValue(scrollPosition)
                    cursor.movePosition(QtGui.QTextCursor.EndOfLine, QtGui.QTextCursor.KeepAnchor)

                    line = cursor.selectedText()
                    indent_tab = len(line) - len(line.lstrip("\t"))
                    indent_space = (len(line) - len(line.lstrip("    "))) / 4
                    indent = indent_tab + int(indent_space)

                    # Restore position and indent new line
                    cursor.setPosition(position)
                    cursor.insertText("\n")
                    for tab in range(0, indent):
                        cursor.insertText("\t")
                    return True
        return False

    def _noteTextInit(self, text):
        self.ui.imageLabel.hide()
        self.ui.textEdit.installEventFilter(self)
        self.ui.textEdit.viewport().installEventFilter(self)
        self.ui.textEdit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.textEdit.customContextMenuRequested.connect(lambda: self.menu.popup(QtGui.QCursor.pos()))
        self.ui.textEdit.setAttribute(Qt.WA_TranslucentBackground)
        if text:
            self.ui.textEdit.setPlainText(text)
        elif os.path.isfile(self.path):
            with open(self.path) as f:
                self.ui.textEdit.setPlainText(f.read())
        else:
            with open(self.path, 'w') as f:
                f.write('')

    def _noteTextLoad(self, name):
        if os.path.isfile(self.path):
            with open(self.path) as f:
                content = f.read()
            if not content == self.ui.textEdit.toPlainText():
                self.ui.textEdit.setPlainText(content)
                logger.info(f"Updated content of '{self.fullname}'")

    def _noteTextToFile(self):
        saveWidget = QtWidgets.QFileDialog.getSaveFileName(self, "Save text as", self.fullname, ".txt")
        path = saveWidget[0]
        if path:
            path += ".txt"
            with open(path, 'w') as f:
                f.write(self.ui.textEdit.toPlainText())

    def _noteTextWrap(self, state=None):
        if state is None:
            self._noteTextWrap(not self.ui.textEdit.lineWrapMode())
        elif state is True:
            self.ui.textEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        elif state is False:
            self.ui.textEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)

    def _noteTitleUpdate(self):
        if self.extension == ".txt":
            title = self.preferences.query("general", "nameFormatText")
        elif self.extension == ".png":
            title = self.preferences.query("general", "nameFormatImage")
        title = title.replace("%fullname%", self.fullname)
        title = title.replace("%shortname%", self.shortname)
        title = title.replace("%extension%", self.extension)
        title = title.replace("%folder%", self.folder)
        title = title.replace("%path%", self.path)
        title = title.replace("%size%", str(self.width()) + "*" + str(self.height()))
        self.setWindowTitle(title)
        self.ui.titleLabel.setText(title)

    def _styleAddPreset(self):
        msg = QtWidgets.QInputDialog()
        msg.setInputMode(QtWidgets.QInputDialog.TextInput)
        msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
        msg.setWindowTitle("Add style preset")
        msg.setLabelText("Enter preset name:")
        msg.setFixedSize(250, 100)
        accept = msg.exec_()
        name = msg.textValue()
        name = sanitizeString(name)
        if accept and name:
            if name in self.preferences.db["stylePresets"]:
                logger.info(f"Name '{name}' already exist, name index has been appended")
                name = getNameIndex(name, self.preferences.db["stylePresets"])
            self.preferences.db["stylePresets"][name] = {}
            self.preferences.db["stylePresets"][name]["foreground"] = self.profile.query("foreground")
            self.preferences.db["stylePresets"][name]["background"] = self.profile.query("background")
            self.preferences.save()

    def _styleSaveGeometry(self):
        self.profile.load()
        self.profile.set("x", self.pos().x())
        self.profile.set("y", self.pos().y())
        if self.extension == ".txt":
            self.profile.set("width", self.width())
            self.profile.set("height", self.height())
        elif self.extension == ".png":
            self.profile.set("width", self.ui.imageLabel.width())
            self.profile.set("height", self.ui.imageLabel.height())
        self.profile.save()

    def _styleSetBackground(self, textEditColor):
        textEditColor = QtGui.QColor(textEditColor )
        widgetColor = QtGui.QColor(self.preferences.query("general", "borderColor"))
        palette = self.ui.textEdit.viewport().palette()
        palette.setColor(QtGui.QPalette.Base, textEditColor)
        palette.setColor(QtGui.QPalette.Background, widgetColor)
        self.ui.textEdit.viewport().setPalette(palette)
        self.ui.textEdit.viewport().update()
        self.setPalette(palette)
        self.update()

    def _styleSetDefault(self):
        self.preferences.db["styleDefault"] = copyDict(self.profile.db[self.fullname])
        self.preferences.save()
        logger.info(f"Replaced default style with '{self.fullname}' profile")

    def _styleSetForeground(self, color):
        color = QtGui.QColor(color)
        palette = self.ui.textEdit.viewport().palette()
        palette.setColor(QtGui.QPalette.Text, color)  # textEdit
        palette.setColor(QtGui.QPalette.WindowText, color)  # label
        self.ui.textEdit.viewport().setPalette(palette)

    def noteClose(self):
        # Remove from active list
        if self.fullname in self.preferences.db["actives"]:
            self.preferences.db["actives"].remove(self.fullname)
            self.preferences.set("actives", self.preferences.db["actives"])

        # Remove from loaded list
        if self.fullname in self.parent.children:
            del self.parent.children[self.fullname]

        # Close widget
        self.fullname = ""
        self.close()

    def noteDelete(self):
        # Move the file to trash folder, or remove from drive
        if os.path.isfile(self.path):
            if self.preferences.query("general", "safeDelete") and os.stat(self.path).st_size > 0:
                trashDir = self.preferences.query("general", "notesDb") + ".trash/" + self.folder
                newName = self.shortname
                if os.path.isfile(trashDir + newName + self.extension):
                    files = []
                    for f in os.listdir(trashDir):
                        files.append(os.path.splitext(f)[0])
                    newName = getNameIndex(newName, files)
                os.renames(self.path, trashDir + newName + self.extension)
            else:
                os.remove(self.path)

        # Remove from profile list
        if self.fullname in self.profile.db:
            del self.profile.db[self.fullname]
            self.profile.save()
        self.noteClose()

    def noteDisplay(self, updateState=True, updatePosition=True):
        if updateState:
            self.noteStateUpdate()
        if updatePosition:
            self.resize(self.profile.query("width"), self.profile.query("height"))
            self.move(self.profile.query("x"), self.profile.query("y"))
        self.show()
        self.styleProfileLoad()
        self.activateWindow()
        self.ui.textEdit.setFocus(True)
        logger.info(f"Displayed '{self.fullname}'")

    def noteMove(self, folder="", soft=False):
        self._noteRename(self.shortname, folder, soft)

    def noteStateUpdate(self, updateFrame=False):
        # Handle window icon
        if self.profile.query("pin"):
            icon = self.icon["pin_title"]
        elif self.fullname in self.preferences.query("actives"):
            icon = self.icon["toggle_actives"]
        else:
            icon = self.icon["tray"]
        self.ui.iconLabel.setPixmap(icon.pixmap(14, 14))
        self.setWindowIcon(icon)

        # Choose between native and custom frame
        if updateFrame:
            if self.preferences.query("general", "frameless"):
                self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
                self.setContentsMargins(1, 0, 1, 1)
                self.ui.iconLabel.show()
                self.ui.titleLabel.show()
                self.ui.closeButton.show()
            else:
                self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
                self.setContentsMargins(0, 0, 0, 0)
                self.ui.iconLabel.hide()
                self.ui.titleLabel.hide()
                self.ui.closeButton.hide()

        # Handle resize corner
        if self.profile.query("sizeGrip") or self.preferences.query("general", "frameless"):
            self.sizeGrip.show()
            self.ui.bottomLabel.show()
        else:
            self.sizeGrip.hide()
            self.ui.bottomLabel.hide()

        logger.info(f"Updated window state for '{self.fullname}'")

    def noteTextSave(self):
        if self.extension == ".txt":
            try:
                with open(self.path, 'w') as f:
                    f.write(self.ui.textEdit.toPlainText())
            except PermissionError:
                logger.error(f"Could not save content to file '{self.path}' (insufficient permission)")
            else:
                if self.windowTitle()[-1] == "*" or self.ui.titleLabel.text()[-1] == "*":
                    self.setWindowTitle(self.windowTitle()[:-1])
                    self.ui.titleLabel.setText(self.ui.titleLabel.text()[:-1])

    def styleProfileLoad(self):
        font = self.ui.textEdit.font()
        font.setFamily(self.profile.query("fontFamily"))
        font.setPointSize(self.profile.query("fontSize"))
        self.ui.textEdit.setFont(font)
        self.styleSetColors(self.profile.query("background"), self.profile.query("foreground"), updateProfile=False)
        self.resize(self.profile.query("width"), self.profile.query("height"))
        self.setWindowOpacity(float(self.profile.query("opacity")))
        logger.info(f"Loaded style for '{self.fullname}'")

    def styleSetColors(self, background, foreground, updateProfile):
        self._styleSetForeground(foreground)
        self._styleSetBackground(background)
        if updateProfile:
            self.profile.set("background", background)
            self.profile.set("foreground", foreground)
            self.profile.save()
