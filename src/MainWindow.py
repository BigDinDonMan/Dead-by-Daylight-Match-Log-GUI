from PyQt5.QtCore import *
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QSpinBox, \
    QDateEdit, QCalendarWidget
import sys
from guicontrols import ItemSelect, KillerSelect, AddonPopupSelect
import struct
from util import setQWidgetLayout, nonNegativeIntValidator, addWidgets

from constants import *

#todo: wrap everything in tab widget
class MainWindow(QMainWindow):
    def __init__(self, parent=None, title='PyQt5 Application', windowSize=(800,600)):
        super(MainWindow, self).__init__(parent=parent)
        self.setWindowTitle(title)
        self.resize(windowSize[0], windowSize[1])
        centralWidget, centralLayout = setQWidgetLayout(QWidget(), QVBoxLayout())
        self.setCentralWidget(centralWidget)
        self.killerSelection = KillerSelect([], iconSize=CHARACTER_ICON_SIZE)
        upperLayout = QHBoxLayout()
        centralLayout.addLayout(upperLayout)
        upperLayout.addWidget(self.killerSelection)

        eliminationsInfoWidget, eliminationsInfoLayout = setQWidgetLayout(QWidget(), QGridLayout())
        self.killsTextBox, self.sacrificesTextBox, self.disconnectsTextBox = QLineEdit(), QLineEdit(), QLineEdit()
        for label, textbox in zip(['Sacrifices', 'Kills (moris)', 'Disconnects'], [self.sacrificesTextBox, self.killsTextBox, self.disconnectsTextBox]):
            textbox.setValidator(nonNegativeIntValidator())
            cellWidget, cellLayout = setQWidgetLayout(QWidget(), QVBoxLayout())
            addWidgets(cellLayout, QLabel(label), textbox)
            eliminationsInfoLayout.addWidget(cellWidget)
        upperLayout.addWidget(eliminationsInfoWidget)

        self.pointsTextBox = QLineEdit()
        self.pointsTextBox.setValidator(nonNegativeIntValidator())
        self.killerMatchDatePicker = QDateEdit(calendarPopup=True)
        self.killerMatchDatePicker.setDate(QDate.currentDate())
        self.killerRankSpinner = QSpinBox()
        self.killerRankSpinner.setRange(HIGHEST_RANK, LOWEST_RANK)#lowest rank is 20, DBD ranks are going down the better they are, so rank 1 is the best
        otherInfoWidget, otherInfoLayout = setQWidgetLayout(QWidget(),QGridLayout())
        for label, obj in zip(['Match date','Points','Killer rank'], [self.killerMatchDatePicker, self.pointsTextBox, self.killerRankSpinner]):
            cellWidget, cellLayout = setQWidgetLayout(QWidget(),QVBoxLayout())
            addWidgets(cellLayout, QLabel(label), obj)
            otherInfoLayout.addWidget(cellWidget)
        upperLayout.addWidget(otherInfoWidget)

        middleLayoutWidget, middleLayout = setQWidgetLayout(QWidget(), QHBoxLayout())
        centralLayout.addWidget(middleLayoutWidget)
        killerAddonsWidget, killerAddonsSelectLayout = setQWidgetLayout(QWidget(),QHBoxLayout())
        middleLayout.addWidget(killerAddonsWidget)

        lowerLayoutWidget, lowerLayout = setQWidgetLayout(QWidget(), QHBoxLayout())
        centralLayout.addWidget(lowerLayoutWidget)

        self.killerAddonSelection = None
        self.itemAddonSelection = None
        self.addonItemsSelectPopup = AddonPopupSelect([])
