#!/usr/bin/python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    cctv_manager_standalone.py
# date:    2017-01-12
# author:  paul dautry
# purpose:
#       Contains full implementation of cctv_manager
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import signal
import sys

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSizePolicy

DEBUG = False

def print_dbg(msg):
    if DEBUG:
        print(msg)

class Activator(object):
    CHARSET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    """docstring for Activator"""
    def __init__(self):
        super(Activator, self).__init__()
        self.z = 36
        self.checksum = [ 30, 24, 18, 12, 6, 0 ]

    def block(self, b, mod):
        print_dbg('call: block(self, b=<%s>, mod=%d)' % (b, mod))
        if len(b) != 6:
            print_dbg('err: incorrect block length (%d)' % len(b))
            return None
        s = 0
        for k in range(0, len(b)):
            l = b[k]
            if l not in Activator.CHARSET:
                print_dbg('err: input not found in charset (%s)' % l)
                return None
            v = abs(Activator.CHARSET.index(l) - (k+1))
            s += v
            print_dbg('current l is: %s' % l)
            print_dbg('current k is: %d' % k)
            print_dbg('current value is: %d' % v)
            print_dbg('current sum is: %d' % s)
        return s % mod

    def activate(self, s):
        print_dbg('call: activate(self, s=<%s>)' % s)
        blocks = s.split('-')
        blocks_sz = len(blocks)
        if blocks_sz != 6:
            print_dbg('err: incorrect number of blocks (%d)' % blocks_sz)
            return False
        for k in range(0, blocks_sz):
            self.z = self.block(blocks[k], self.z)
            print_dbg('dbg: new z is: %d' % self.z)
            if self.z is None:
                print_dbg('err: block function returned error')
                return False
            if self.z != self.checksum[k]:
                print_dbg('err: incorrect checksum (z=%d tested against checksum[%d]=%d)' % (self.z, k, self.checksum[k]))
                return False
        return True


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

class ActivatedWidget(QWidget):
    """docstring for ActivatedWidget"""
    def __init__(self):
        super(ActivatedWidget, self).__init__()
        self.lab_result = None
        self.yek = [ 
            0x05, 0xca, 0xea, 0x5f,
            0x4c, 0xad, 0x60, 0x0a,
            0xe8, 0x07, 0x92, 0x4f,
            0x6f, 0x93, 0x91, 0x0d 
        ]
        self.vei = [
            0xaf, 0xa1, 0x3d, 0x46,
            0x90, 0xda, 0x00, 0x32,
            0x49, 0xad, 0xf0, 0xca,
            0xb8, 0x11, 0x94, 0x02
        ]
        self.cne = [
            0xfd, 0x0e, 0xbb, 0x75,
            0xfc, 0x13, 0x0f, 0x56,
            0xc4, 0x8a, 0x43, 0xa5,
            0x8e, 0xed, 0x70, 0x2f,
            0x9a, 0xbd, 0x21, 0x4b,
            0xc3, 0xcd, 0x0a, 0x38,
            0x03, 0xe6, 0xb4, 0x93,
            0x86, 0x1b, 0x8f, 0x0f,
            0xfa, 0x13, 0xeb, 0x60,
            0xe7, 0x05, 0x4a, 0x53,
            0x88, 0x95, 0x4f, 0xaa,
            0x88, 0xfc, 0x71, 0x70,
            0xdf, 0xf8, 0x21, 0x77,
            0xce, 0xda, 0x4f, 0x79,
            0x09, 0xe1, 0xfd, 0x9c,
            0x88, 0x1a, 0x92, 0x5d,
            0xbc, 0x5e, 0xaa, 0x4f,
            0xb8, 0x57, 0x66, 0x3d,
            0xb2, 0xa7, 0x14, 0xe7,
            0x84, 0xfd, 0x6a, 0x26,
            0x8d, 0xe0, 0x70, 0x62,
            0xab, 0x99, 0x32, 0x59,
            0x05, 0xc2, 0xb5, 0xf7,
            0x89, 0x17, 0x8b, 0x1f,
            0xfb, 0x59, 0xa9, 0x59,
            0xc6, 0x7f, 0x61, 0x0a,
            0xaa, 0xf6, 0x69, 0xc5,
            0xe2, 0x80, 0x1e, 0x16 
        ]
        self.init_ui()

    def init_ui(self):
        # create widgets
        btn_validate = QPushButton('Ok', self)
        self.lab_result = QLabel('')
        # create layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.lab_result)
        main_layout.addWidget(btn_validate)
        # set self properties
        self.setWindowTitle('CCTV Manager Activation Result')
        #self.setWindowIcon()
        self.setLayout(main_layout)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        # connects
        btn_validate.clicked.connect(self.terminate)

    def activation_passed(self):
        self.lab_result.setText('Activation is a success !\n%s' % self.finalize())
        self.show()

    def activation_failed(self):
        self.lab_result.setText('Activation failed, please try again...')
        self.show()

    def terminate(self):
        self.close()
        QApplication.quit()

    def finalize(self):
        clear = ''
        buf = self.cne
        key = self.yek
        iv = self.vei
        buf_sz = len(buf)
        bsize = 16
        # iterate over blocks to decrypt
        for i in range(0,int(buf_sz/bsize)):
            for j in range(0,bsize):
                # decode character
                c = (buf[i*bsize+j] ^ key[j]) ^ iv[j]
                # prepare next iv
                iv[j]=buf[i*bsize+j]
                # write decoded char on buf
                buf[i*bsize+j]=c
        # unpad PKCS#7
        i=buf[buf_sz-1]
        for j in range(0,i):
            buf[buf_sz-1-j]=0
        # print flag
        for i in range(0,buf_sz):
            if buf[i] == 0:
                break;
            clear += chr(buf[i])
        return clear

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

def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    if QMessageBox.question(None, '', "Are you sure you want to quit?",
                            QMessageBox.Yes | QMessageBox.No,
                            QMessageBox.No) == QMessageBox.Yes:
        QApplication.quit()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    m = Main()
    exit(m.exec())
