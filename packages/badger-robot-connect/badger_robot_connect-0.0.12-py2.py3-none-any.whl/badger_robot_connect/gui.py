import numpy as np
import sys
from enum import Enum

from PyQt5.QtGui import QPixmap, QPainter, QImage, QColor, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtSvg import QSvgRenderer, QSvgWidget


class GUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._fields = dict()

        # WiFi Connection ########

        lbl_ip = QLabel('IP')
        self.txt_ip = QLineEdit('192.168.0.100')
        self._fields['ip'] = self.txt_ip
        self.btn_wifi_connect = QPushButton('Connect')

        lay_wifi_connect = QHBoxLayout()

        for w in [lbl_ip, self.txt_ip, self.btn_wifi_connect]:
            lay_wifi_connect.addWidget(w)

        # Gamepad Connection ########

        self.btn_gamepad = QPushButton('ATTACH\nGamepad')
        self.btn_gamepad.setFixedHeight(50)

        # Tab Box ########

        self.tab_box = QTabWidget()

        self.navigation = NavigationPanel()
        self.tab_box.addTab(self.navigation, 'Navigation')

        self.tab_settings = QWidget()
        self.tab_box.addTab(self.tab_settings, 'Settings')

        # self.tab_box.setMinimumWidth(700)

        # Controls Panel ########

        img_logo = QLabel()
        img_logo.setPixmap(QPixmap(r'./BADGER.png'))
        img_logo.setAlignment(Qt.AlignCenter)

        self.btn_stop = QPushButton('STOP')
        self.btn_stop.setFont(QFont('Sans Serif', 22, 2))
        self.btn_stop.setStyleSheet('background-color: #E57373')
        self.btn_stop.setFixedHeight(75)

        lay_controls = QVBoxLayout()

        lay_controls.addLayout(lay_wifi_connect)
        lay_controls.addSpacing(10)
        lay_controls.addWidget(self.btn_gamepad)
        lay_controls.addStretch(10)
        lay_controls.addWidget(img_logo)
        lay_controls.addStretch(10)
        lay_controls.addWidget(self.btn_stop)

        wid_controls = QWidget()
        wid_controls.setFixedWidth(250)
        wid_controls.setLayout(lay_controls)

        # Top Layout ########

        lay_top = QHBoxLayout()

        for w in [wid_controls, self.tab_box]:
            lay_top.addWidget(w)

        # Main Layout ########

        self.wid_indicators = IndicatorPanel()

        lay_main = QVBoxLayout()

        lay_main.addLayout(lay_top)
        # lay_main.addWidget(self.wid_indicators)

        self.setLayout(lay_main)

        self.setWindowTitle('BADGER Connect')

    def set_fields(self, **kwargs):

        # Fill all specified text fields
        for key, value in kwargs.items():
            try:
                self._fields[key].setText(str(value))
            except KeyError:
                print(f'ERROR: field "{key}" not found\n'
                      f'\tOptions: {", ".join(self._fields.keys())}')


class NavigationPanel(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        lbl_route = QLabel('Route')
        self.combo_route = QComboBox()

        self.rad_full_route = QRadioButton('Full Route')
        self.rad_full_route.setChecked(True)

        self.rad_partial_route = QRadioButton('Partial Route')
        lbl_partial_start = QLabel('Start')
        self.txt_partial_start = QLineEdit('0')
        self.txt_partial_start.setEnabled(False)
        lbl_partial_end = QLabel('End')
        self.txt_partial_end = QLineEdit('1')
        self.txt_partial_end.setEnabled(False)

        def on_toggled_rad_partial_route():
            """ Enable or disable items under the radio button, depending on if it's checked """
            isEnabled = self.rad_partial_route.isChecked()
            self.txt_partial_start.setEnabled(isEnabled)
            self.txt_partial_end.setEnabled(isEnabled)

        self.rad_partial_route.toggled.connect(on_toggled_rad_partial_route)

        self.rad_custom_route = QRadioButton('Custom Order')
        self.txt_custom_route = QLineEdit('1, 2, 3')
        self.txt_custom_route.setEnabled(False)

        def on_toggled_rad_custom_route():
            """ Enable or disable items under the radio button, depending on if it's checked """
            isEnabled = self.rad_custom_route.isChecked()
            self.txt_custom_route.setEnabled(isEnabled)

        self.rad_custom_route.toggled.connect(on_toggled_rad_custom_route)

        lbl_at_end = QLabel('At End')
        self.chk_repeat_route = QCheckBox('Repeat at End')

        nc = QGridLayout()

        nc.addWidget(lbl_route, 0, 0)
        nc.addWidget(self.combo_route, 0, 1, 1, 2)
        nc.addWidget(self.rad_full_route, 1, 0, 1, 3)
        nc.addWidget(self.rad_partial_route, 2, 0, 1, 3)
        nc.addWidget(lbl_partial_start, 3, 1)
        nc.addWidget(self.txt_partial_start, 3, 2)
        nc.addWidget(lbl_partial_end, 4, 1)
        nc.addWidget(self.txt_partial_end, 4, 2)
        nc.addWidget(self.rad_custom_route, 5, 0, 1, 3)
        nc.addWidget(self.txt_custom_route, 6, 1, 1, 2)
        nc.addWidget(self.chk_repeat_route, 7, 0, 1, 3)

        btn_start_navigation = QPushButton('Make it Happen!')
        btn_start_navigation.setFixedHeight(50)

        lay_navigation_controls = QVBoxLayout()
        lay_navigation_controls.addStretch(10)
        lay_navigation_controls.addLayout(nc)
        lay_navigation_controls.addSpacing(30)
        lay_navigation_controls.addWidget(btn_start_navigation)
        lay_navigation_controls.addStretch(10)

        wid_navigation_controls = QWidget()
        wid_navigation_controls.setLayout(lay_navigation_controls)
        wid_navigation_controls.setMaximumWidth(300)

        # self.img_route = QLabel()
        # self.img_route.setPixmap(QPixmap(r'./routes/route_soccer.png'))
        # self.img_route.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.img_route = ResizingImage()
        self.img_route.setPixmap(QPixmap(r'./routes/route_soccer.png'))
        self.img_route.setMinimumSize(300, 400)

        lay_navigation = QHBoxLayout()

        lay_navigation.addWidget(wid_navigation_controls)
        lay_navigation.addSpacing(10)
        lay_navigation.addWidget(self.img_route)
        lay_navigation.addSpacing(10)

        self.setLayout(lay_navigation)


class IndicatorPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.gage_pitch = RotatedSvg()
        self.gage_pitch.setFixedSize(75, 75)

        lay_main = QHBoxLayout()

        lay_main.addWidget(self.gage_pitch)
        lay_main.addStretch()

        self.setLayout(lay_main)


class RotatedSvg(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

    def paintEvent(self, event):
        angle = -20
        painter = QPainter(self)
        svg = QSvgRenderer(r'./Pitch_Indicator_Back.svg')
        svg.render(painter)
        rad = np.radians(angle)
        L = self.width() / 2
        painter.translate(L - np.sqrt(2) * L * np.cos(np.pi / 4 + rad),
                          L - np.sqrt(2) * L * np.sin(np.pi / 4 + rad))
        painter.rotate(angle)
        svg_top = QSvgRenderer(r'./Pitch_Indicator_Needle.svg')
        svg_top.render(painter)


class ResizingImage(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.pixmap: QPixmap = None

    def setPixmap(self, pixmap: QPixmap):
        self.pixmap = pixmap
        self.setMinimumSize(10, 10)
        # self.setMinimumSize(QSize(self.pixmap.width() // 2, self.pixmap.height() // 2))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, event):
        if self.pixmap:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            aspect_ratio = self.pixmap.width() / self.pixmap.height()
            aspect_height = self.width() / aspect_ratio
            aspect_width = self.height() * aspect_ratio
            height = min([self.height(), self.pixmap.height(), aspect_height])
            width = min([self.width(), self.pixmap.width(), aspect_width])
            img_rect = QRect(0, 0, width, height)
            img_rect.moveCenter(self.rect().center())
            # scaled_pixmap = self.pixmap.scaled(img_rect.size())
            painter.drawPixmap(img_rect, self.pixmap, self.pixmap.rect())
