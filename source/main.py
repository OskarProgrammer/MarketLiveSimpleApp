import sys
import os

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QGridLayout
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon

from gettingData import getData

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, "..")

class MonitorGieldowy(QWidget):
    
    symbolsList = []
    
    def __init__(self):
        super().__init__()

        appIcon_path = os.path.join(project_root, "Icons", "appIcon.ico")
        appIcon = QIcon(appIcon_path)

        self.setWindowIcon(appIcon)
        self.setWindowTitle("Market monitor")
        self.setGeometry(100, 100, 600, 400)
        self.setFixedSize(600, 400)

        self.createInterface()
        self._getSymbolsFromFile()
        
        self.timer = QTimer(self)
        self.timer.setInterval(15000)
        self.timer.timeout.connect(self._updatePrices)
        self.timer.start()

        self.countdown_timer = QTimer(self)
        self.countdown_timer.setInterval(1000)
        self.countdown_timer.timeout.connect(self._updateCountdown)
        self.countdown_timer.start()
        
        self.countdown_counter = self.timer.interval() // 1000
        self._updateCountdown()

        self._updatePrices()

    def _getSymbolsFromFile(self):
        try:
            symbols_file_path = os.path.join(project_root, "symbols.txt")
            with open(symbols_file_path, "r") as file:
                self.symbolsList = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            symbols_file_path = os.path.join(project_root, "symbols.txt")
            with open(symbols_file_path, "w") as file:
                pass
            print("File symbols.txt does not exist. Creating.")

    def _getSymbolFromInput(self):
        symbol = self.symbolInput.text().upper()
        if symbol and symbol not in self.symbolsList:
            self.symbolsList.append(symbol)
            try:
                symbols_file_path = os.path.join(project_root, "symbols.txt")
                with open(symbols_file_path, "a") as file:
                    file.write(f"{symbol}\n")
            except Exception as e:
                print(f"Error during writing to file: {e}")
            
            self.symbolInput.clear()
            self._updatePrices()
        else:
            print("Empty or already exist")
    
    def _updateCountdown(self):
        self.countdown_counter -= 1
        if self.countdown_counter < 0:
            self.countdown_counter = 0
            
        self.setWindowTitle(f"Market monitor | Refresh in {self.countdown_counter}s")

    def _updatePrices(self):
        
        self.countdown_counter = self.timer.interval() // 1000
        
        for i in reversed(range(self.symbolsLayout.count())):
            widget = self.symbolsLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        if not self.symbolsList:
            self.symbolsLayout.addWidget(QLabel("No symbols to display."), 0, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
            return
            
        row = 0
        for symbol in self.symbolsList:
            data = getData(symbol)
            if data and data.get('currentPrice') is not None:
                diff = data['currentPrice'] - data['lastClose']
                percent = ((data['currentPrice'] / data["lastClose"]) * 100 - 100)
                
                label_text = f"<b>{symbol}</b>: {data['currentPrice']} {data.get('currency', 'no data')} | {diff:.2f} | {percent:.2f} %"
                label = QLabel(label_text)
                
                if data['lastClose'] is not None:
                    if data['lastClose'] < data['currentPrice']:
                        label.setStyleSheet("font-size: 16pt; font-weight: bold; color: green;")
                    elif data['lastClose'] == data['currentPrice']:
                        label.setStyleSheet("font-size: 16pt; font-weight: bold; color: gray;")
                    else:
                        label.setStyleSheet("font-size: 16pt; font-weight: bold; color: red;")
                else:
                    label.setStyleSheet("font-size: 16pt; font-weight: bold; color: gray;")

                self.symbolsLayout.addWidget(label, row, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                row += 1
            else:
                label = QLabel(f"<b>{symbol}</b>: No data")
                label.setStyleSheet("font-size: 16pt; font-weight: bold; color: gray;")
                self.symbolsLayout.addWidget(label, row, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
                row += 1

    def createInterface(self):
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.symbolInput = QLineEdit()
        mainLayout.addWidget(self.symbolInput)

        self.button = QPushButton("Add symbol")
        self.button.clicked.connect(self._getSymbolFromInput)
        mainLayout.addWidget(self.button)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        
        self.symbolsLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.symbolsLayout.setSpacing(20)
        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        mainLayout.addWidget(self.scrollArea)
        self.setLayout(mainLayout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = MonitorGieldowy()
    okno.show()
    sys.exit(app.exec())