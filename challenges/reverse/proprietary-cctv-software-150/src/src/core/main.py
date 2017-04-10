#!/usr/bin/python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    main.py
# date:    2017-01-12
# author:  paul dautry
# purpose:
#       
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys
from core.activated_widget import ActivatedWidget
from core.activation_widget import ActivationWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

class Main(object):
    """docstring for Main"""
    def __init__(self):
        super(Main, self).__init__()
        self.app = QApplication(sys.argv)
        self.icon = QIcon('resources/cctv_logo.png')
        self.activation = ActivationWidget()
        self.activated = ActivatedWidget()
        self.activation.setWindowIcon(self.icon)
        self.activation.setWindowIcon(self.icon)
        self.activation.c.ok.connect(self.activated.activation_passed)
        self.activation.c.ko.connect(self.activated.activation_failed)

    def exec(self):
        self.activation.show()
        return self.app.exec_()