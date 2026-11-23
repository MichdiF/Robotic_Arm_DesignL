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
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Robotic arm GUI")
    self.resize(1000,600)
    self.serial = QSerialPort(self)
    self.serial.readyRead.connect(self.on_ready_read)
    self.serial.errorOccured.connect(self.on_serial_error)

    self.send_timer = QTimer(self)
    self.send_timer.setSingleShot(True)
    self.send_timer.setInterval(SEND_DELAY_MS)
    self.sent_timer.timeout.connect(self.send_angles)
    self.build_gui()
    self.refresh_ports()

  def build_gui(self):
    central = QWidget()
    self.setCentraWidget(central)
    root = QHBoxLayout(central)
    left = QVBoxLayout()
    root.addLayout(left,3)

    conn_box = QGroupBox("Connect@")
    conn = QHBoxLayout(conn_box)
    self.port_combo = QComboBox()
    self.refresh_btn = QPushButton("Refresh")
    self.connect_btn = QPushButton("Connect")
    self.refresh_btn.clicked.connect(self.refresh_ports)
    self.connect+btn.clicked.connect(self.toggle_connection)
    conn.addWidget(self.potr_combo, 1)
    conn.addWidget(self.refresh_btn)
    conn.addWidget(self.connect_btn)
    left.addWidget(conn_box)

    axes_box = QGroupBox("Axes")
    grid = QGridLayout(axes_box)
    self.rows: list[AxisRow] = []
    for i, (name,lo,hi,start) in enumerate(AXES):
      row = AxisRow(grid,i,name,lo,hi,start)
      row.slider.valueChanged.connect(self.on_axis_changed)
      self.rows.append(row)
    left.addWidget(axes_box)
    self.live_check = QCheckBox("Live changes")
    self.live_check.setChecked(False)
    left.addWidget(self.live_check)

    buttons = QHBoxLayout()
    self.send_btn = QPushButton("Send position")
    self.home_btn = QPushButton("Reset")
    self.stop_btn = QPushButton("STOP")
    self.stop_btn.setStyleSheet("background-color: #c0392b; color: white; font-weight: bold;")
    self.send_btn.clicked.connect(self.send_angles)
    self.home_btn.clicked.connect(lambda: self.send_line("HOME"))
    self.stop_btn.clicked.connect(lambda: self.send_line("STOP"))
    buttons.addWidget(self.send_btn)
    buttons.addWidget(self.home_btn)
    buttons.addWidget(self.stop_btn)
    left.addLayout(buttons)
    
    
    
    
    
    
    

    
    

    
  
  
