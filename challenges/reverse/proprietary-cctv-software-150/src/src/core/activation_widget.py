#!/usr/bin/python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    activation_widget.py
# date:    2017-01-12
# author:  paul dautry
# purpose:
#       
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from core.activation import Activator
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSizePolicy

class Communicator(QObject):
    ok = pyqtSignal()
    ko = pyqtSignal()

class ActivationWidget(QWidget):
    """docstring for ActivationWidget"""
    def __init__(self):
        super(ActivationWidget, self).__init__()
        self.activator = Activator()
        self.c = Communicator()
        self.le_parts = []
        self.init_ui()

    def init_ui(self):
        # create widgets
        btn_validate = QPushButton('Ok', self)
        btn_cancel = QPushButton('Cancel', self)
        le_code_part_1 = QLineEdit(self)
        le_code_part_2 = QLineEdit(self)
        le_code_part_3 = QLineEdit(self)
        le_code_part_4 = QLineEdit(self)
        le_code_part_5 = QLineEdit(self)
        le_code_part_6 = QLineEdit(self)
        lab_instructions = QLabel('Enter a valid activation key:')
        # initialize widgets
        self.le_parts.append(le_code_part_1)
        self.le_parts.append(le_code_part_2)
        self.le_parts.append(le_code_part_3)
        self.le_parts.append(le_code_part_4)
        self.le_parts.append(le_code_part_5)
        self.le_parts.append(le_code_part_6)
        for le in self.le_parts:
            le.setMaxLength(6)
            le.setPlaceholderText('XXXXXX')
        # create layout
        input_field_layout = QHBoxLayout()
        btns_layout = QHBoxLayout()
        main_layout = QVBoxLayout()
        input_field_layout.addWidget(le_code_part_1)
        input_field_layout.addWidget(QLabel('-'))
        input_field_layout.addWidget(le_code_part_2)
        input_field_layout.addWidget(QLabel('-'))
        input_field_layout.addWidget(le_code_part_3)
        input_field_layout.addWidget(QLabel('-'))
        input_field_layout.addWidget(le_code_part_4)
        input_field_layout.addWidget(QLabel('-'))
        input_field_layout.addWidget(le_code_part_5)
        input_field_layout.addWidget(QLabel('-'))
        input_field_layout.addWidget(le_code_part_6)
        btns_layout.addWidget(btn_validate)
        btns_layout.addWidget(btn_cancel)
        main_layout.addWidget(lab_instructions)
        main_layout.addLayout(input_field_layout)
        main_layout.addLayout(btns_layout)
        # set self properties
        self.setWindowTitle('CCTV Manager Activation')
        #self.setWindowIcon()
        self.setLayout(main_layout)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        # initialize connections
        btn_validate.clicked.connect(self.btn_ok_clicked)
        btn_cancel.clicked.connect(self.btn_ko_clicked)

    def btn_ok_clicked(self):
        s = ''
        for le in self.le_parts:
            s += le.text()
            s += '-'
        s = s[:-1]
        if self.activator.activate(s.upper()):
            self.c.ok.emit()
        else:
            self.c.ko.emit()
        self.close()

    def btn_ko_clicked(self):
        self.c.ko.emit()
        self.close()