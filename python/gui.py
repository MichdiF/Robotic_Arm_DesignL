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

    self.log = QPlainTextEdit()
    self.log.setReadOnly(True)
    self.log.setMaximumBlockCount(256)
    left.addWidget(self.log, 1)

    right = QVBoxLayout()
    root.addLayout(right, 2)
    cam_box = QGroupBox("Camera")
    cam_layout = QVBoxLayout(cam_box)
    self.cam_label = QLabel("No image")
    self.cam_label.setAlignment(Qt.AlignCenter)
    self.cam_label.setMinimumSize(CAM_WIDTH, CAM_HEIGHT)
    self.cam_label.setStyleSheet("background-color: #222; color: #aaa;")
    cam_layout.addWidget(self.cam_label)
    right.addWidget(cam_box)
    right.addStretch(1)
    self.set_controls_enabled(False)

  def set_controls_enabled(self, enabled: bool):
    for w in (self.send_btn, self.home_btn, self.stop_btn):
      w.setEnabled(enabled)

  def refresh_ports(self):
    self.port_combo.clear()
    for info in QSerialPortInfo.availablePorts():
      self.port_combo.addItem(f"{info.portName()} – {info.description()}", info.portName())

  def toggle_connection(self):
    if self.serial.isOpen():
      self.serial.close()
      self.connect_btn.setText("Connect")
      self.set_controls_enabled(False)
      self.log_msg("Disconnected")
      return

    name = self.port_combo.currentData()
    if not name:
      self.log_msg("No port selecetd")
      return

    self.serial.setPortName(name)
    self.serial.setBaudRate(BAUDRATE)
    if self.serial.open(QIODevice.OpenModeFlag.ReadWrite):
      self.connect_btn.setText("Disconnect")
      self.set_controls_enabled(True)
      self.log_msg(f"Connected with {name}")
    else:
      self.log_msg(f"Failed to connect with port: {self.serial.errorString()}")

  def send_line(self, text: str):
    if nor self.serial.isOpen():
      return
    self.serial.write((text + "\n").encode("ascii"))
    self.log_msg(f">> {text}")

  def send_angles(self):
    angles = [row.value() for row in self.rows]
    self.send_line(",".join(str(a) for a in angles))

  def on_axis_changed(self):
    if self.live_check.isChecked() and self.serial.isOpen():
      self.send_timer.start()

  def on_ready_read(self):
    while self.serial.canReadLine():
      line = bytes(self.serial.readLine()).decode("utf-8", errors="replace").strip()
      if line:
        self.handle_line_from_pico(line)

  def handle_line_from_pico(self, line: str):
        self.log_msg(f"< {line}")

  def on_serial_error(self, error):
    if error != QSerialPort.SerialPortError.NoError:
      self.log_msg(f"Błąd portu: {self.serial.errorString()}")
      if error == QSerialPort.SerialPortError.ResourceError:
        self.serial.close()
        self.connect_btn.setText("Connect")
        self.set_controls_enabled(False)

  def show_frame(self, data: bytes, width: int = CAM_WIDTH, height = CAM_HEIGHT):
    if len(data) != width*height:
      self.log_msg(f"Bad frame size: {len(data)} B")
      return
    img = QImage(data, width, height, width, QImage.Format.Format_Grayscale8)
    self.cam_label.setPixmap(QPixmap.fromImage(img.copy()))

  def log_msg(self, text: str)
    self.log.appendPlainText(text)

  def closeEvent(self, event):
    if self.serial.isOpen():
      self.serial.close()
    super().closeEvent(event)

def main():
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.ecit(app.exec())

if __name__ == "__main__":
  main()

    
      
    	  
    
    
    
    
    
    

    
    

    
  
  
