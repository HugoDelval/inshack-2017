#!/usr/bin/python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    activated_widget.py
# date:    2017-01-12
# author:  paul dautry
# purpose:
#       
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSizePolicy

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
        buf_sz = len(self.cne)
        bsize = 16
        # iterate over blocks to decrypt
        for i in range(0,int(buf_sz/bsize)):
            for j in range(0,bsize):
                # decode character
                c = (self.cne[i*bsize+j] ^ self.yek[j]) ^ self.vei[j]
                # prepare next iv
                self.vei[j] = self.cne[i*bsize+j]
                # write decoded char on buf
                self.cne[i*bsize+j] = c
        # unpad PKCS#7
        i=self.cne[buf_sz-1]
        for j in range(0,i):
            self.cne[buf_sz-1-j]=0
        # print flag
        for i in range(0,buf_sz):
            if self.cne[i] == 0:
                break;
            clear += chr(self.cne[i])
        return clear
