# FRANCESCO GERRATANA 2023 QT5 Gmaps embed Manipulation Exif GPS data
import os
import sys

from PyQt5 import QtCore
from PyQt5 import QtWebChannel
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QApplication

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class WebObj(QtCore.QObject):
    pLatLng = QtCore.pyqtSignal([float, float])
    pMuovi = QtCore.pyqtSignal(list)

    @QtCore.pyqtSlot(float, float)
    def mapclick(self, x, y):
        self.pLatLng.emit(x, y)

    @QtCore.pyqtSlot(list)
    def getPositionOfMarkers(self, latlng):
        self.pMuovi.emit(latlng)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.form_widget = FormWidget(self)
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.form_widget)
        self.setCentralWidget(_widget)
        self.setMinimumSize(QSize(1280, 800))
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("GPS TOOL PYTHON 2023")
        self.statusBar().showMessage("Copyright F.Gerratana 2023")


class FormWidget(QWidget):
    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.coordinate = None
        self.__controls()
        self.__layout()

    def __controls(self):
        self.browser = QWebEngineView()
        evento = WebObj(self)
        evento.pLatLng.connect(self.onpointchanged)
        evento.pMuovi.connect(self.getPos)
        channel = QtWebChannel.QWebChannel(self)
        channel.registerObject('evento', evento)
        self.browser.page().setWebChannel(channel)
        file = os.path.join(CURRENT_DIR, "google_map.html")
        url = QUrl.fromLocalFile(file)
        self.browser.load(url)

    @QtCore.pyqtSlot(float, float)
    def onpointchanged(self, x, y):
        print(x, y)
        self.outputlatlng.setText(str(x) + ',' + str(y))

    def __layout(self):
        self.grid = QGridLayout()
        self.writegps = QPushButton("WRITE GPS")
        self.writegps.setToolTip('WRITE GPS')
        self.sendgps = QPushButton("SEND GPS")
        self.sendgps.setToolTip('SEND GPS')
        self.outputlatlng = QLineEdit()
        self.inputlatlng = QLineEdit()
        self.grid.addWidget(self.browser, 0, 0, 1, 2)
        self.grid.addWidget(self.writegps, 1, 0)
        self.grid.addWidget(self.outputlatlng, 1, 1)
        self.grid.addWidget(self.sendgps, 2, 0)
        self.grid.addWidget(self.inputlatlng, 2, 1)
        self.setLayout(self.grid)
        self.writegps.clicked.connect(self.leggi_valore_mappa)

    def leggi_valore_mappa(self):
        valore_mappa = self.outputlatlng.text()
        print(valore_mappa)

    @QtCore.pyqtSlot(list)
    def getPos(self, latlng):
        if latlng is not None and len(latlng) > 0:
            latlng_str = ','.join(str(x) for x in latlng).replace('[', '').replace(']', '').replace('\'', '')
            self.inputlatlng.setText(f"{latlng_str}")
            print(latlng)
        else:
            self.inputlatlng.setText("No Gps Value")
            print("No Gps Value")


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()


if __name__ == '__main__':
    sys.exit(main())
