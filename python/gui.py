import sys
"""PySide6>=6.6
numpy"""

from PySide6.QtCore import QIODevice, Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtWidgets import (
  QApplication,
  QCheckBox,
  QComboBox,
  QGridLayout,
  QGroupBox,
  QHBoxLayout,
  QLabel,
  QMainWindow,
  QPlainTextEdit,
  QPushButton,
  QSlider,
  QSpinBox,
  QVBoxLayout,
  QWidget,
)

BAUDRATE = 115200
SEND_DELAY_MS = 50
CAM_WIDTH = 
CAM_HEIGHT = 

AXES = [
  ("Silnik krokowy)" , 0 , 360, 0),
  ("Ramie)" , 0 , 180, 90),
  ("Łokiec)" , 0 , 180, 90),
  ("Nadgarstek)" , 0 , 180, 90),
  ("Chwytak 1)" , 0 , 180, 90),
  ("Chwytak 2)" , 0 , 180, 90),
]
class AxisRow:
  def __init__(self,grid: QGridLayout, row: int, name: str, lo: int, hi: int, start: int):
    self.label = QLabel(name)
    self.slider = QSlider(Qt.Horizontal)
    self.spin = QSpinBox()

    self.slider.setRange(lo,hi)
    self.spin.setRange(lo,hi)
    self.spin.setSuffix("°")
    self.slider.setValue(start)
    self.spin.setValue(start)
    self.slider.valueChanged.connect(self.spin.setValue)
    self.spin.valueChanged.connect(self.slider.setValue)

    grid.addWidget(self.labe., row, 0)
    grid.addWidget(self.slider, row, 1)
    grid.addWidget(self.spin, row, 2)

    def value(self) -> int:
      return self.slider.value()
    def set_value(self, v: int):
      self.slider.setValue(v)

class MainWindow(QMainWindow):
  
  
