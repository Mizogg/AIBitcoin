import sys
import random
import multiprocessing
import secp256k1 as ice
from bloomfilter import BloomFilter
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QProgressBar, QPlainTextEdit, QMessageBox, QRadioButton, QButtonGroup
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QTime, Qt
from PyQt5.QtGui import QPainter, QFont, QColor
import time
try:
    with open('btc.bf', "rb") as fp:
        addfind = BloomFilter.load(fp)
except FileNotFoundError:

    filename = 'btc.txt'
    with open(filename) as file:
        addfind = file.read().split()

class CustomProgressBar(QProgressBar):
    def paintEvent(self, event):
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        
        progress_str = f"Progress: {self.value()/self.maximum()*100:.2f}%"
        painter.setPen(QColor(Qt.black))
        painter.setFont(QFont("Courier", 10, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, progress_str)
        
class KeyGenerationThread(QThread):
    update_keys_per_sec = pyqtSignal(int)
    value_edit_hex = pyqtSignal(str)
    btc_address_edit = pyqtSignal(str)
    found_keys_scanned_edit = pyqtSignal(int)
    recoveryFinished = pyqtSignal(str)

    def __init__(self, priv_start, priv_end, order, num_cpus):
        super().__init__()
        self.priv_start = priv_start
        self.priv_end = priv_end
        self.order = order
        self.found_count__slot = 0
        self.num_cpus = num_cpus

    def run(self):
        def process_address(address, private_key):
            if address in addfind:
                found_data = f'\nFOUND!! Private Key: {hex(private_key)}\tAddress: {address}\n'
                with open('found.txt', 'a') as result:
                    result.write(found_data)
                self.found_count__slot += 1
                self.found_keys_scanned_edit.emit(self.found_count__slot)
                self.recoveryFinished.emit(found_data)

        def generate_keys(priv_start, priv_end):
            keys_generated = 0
            total_keys_scanned = 0
            start_time = time.time()
            try:
                if self.order == 'sequence':
                    group_size = 100000
                    private_key = priv_start
                    P = ice.scalar_multiplication(private_key)
                    current_pvk = private_key + 1
                    for i in range(priv_start, priv_end, group_size):
                        Pv = ice.point_sequential_increment(group_size, P)
                        for t in range(group_size):
                            this_btc = ice.pubkey_to_address(0, True, Pv[t * 65:t * 65 + 65])
                            process_address(this_btc, current_pvk + t)
                            if keys_generated % group_size == 0 and multiprocessing.current_process().name == 'MainProcess':
                                self.update_keys_per_sec.emit(keys_generated)
                                self.value_edit_hex.emit(str(hex(current_pvk + t)))
                                self.btc_address_edit.emit(this_btc)
                                start_time = time.time()

                            keys_generated += 1*self.num_cpus

                        P = Pv[-65:]
                        current_pvk += group_size
                    self.recoveryFinished.emit('Recovery Finished')
                elif self.order =='random':
                    group_size = 1000
                    while True:
                        private_key = random.randrange(priv_start, priv_end)
                        P = ice.scalar_multiplication(private_key)
                        current_pvk = private_key + 1
                        for i in range(group_size):
                            Pv = ice.point_sequential_increment(group_size, P)
                            for t in range(group_size):
                                this_btc = ice.pubkey_to_address(0, True, Pv[t * 65:t * 65 + 65])
                                process_address(this_btc, current_pvk + t)
                                if keys_generated % group_size == 0 and multiprocessing.current_process().name == 'MainProcess':
                                    self.update_keys_per_sec.emit(keys_generated)
                                    self.value_edit_hex.emit(str(hex(current_pvk + t)))
                                    self.btc_address_edit.emit(this_btc)
                                    start_time = time.time()
                                keys_generated += 1*self.num_cpus
                            P = Pv[-65:]
                            current_pvk += group_size
            except KeyboardInterrupt:
                print("Program interrupted. Cleaning up...")
                return False
            return True

        generate_keys(self.priv_start, self.priv_end)


class CryptoHunterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mizogg QTMizICE.py")
        self.setGeometry(100, 100, 780, 560)
        self.initUI()
        self.start_time = time.time()
        self.threads = []

    def initUI(self):
        cpu_count = multiprocessing.cpu_count()
        radio_button_layout = QHBoxLayout()
        Order_label = QLabel('<html><b><left><font color="blue"size="3">Order of Scan: </font></left></b></html>')
        radio_button_layout.addWidget(Order_label)
        self.random_button = QRadioButton('Random')
        self.random_button.setChecked(True)
        self.sequence_button = QRadioButton('Sequence')
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.random_button)
        self.button_group.addButton(self.sequence_button)
        radio_button_layout.addWidget(self.random_button)
        radio_button_layout.addWidget(self.sequence_button)
        cpu_label = QLabel('<html><b><left><font color="blue" size="2">Number of CPUS : </font></left></b></html>')
        radio_button_layout.addWidget(cpu_label)
        self.cpu_box = QComboBox()
        for i in range(1, cpu_count + 1):
            self.cpu_box.addItem(str(i))
        radio_button_layout.addWidget(self.cpu_box)
        start_button = QPushButton('Start')
        start_button.setStyleSheet("color: green")
        start_button.clicked.connect(self.start)
        stop_button = QPushButton('Stop')
        stop_button.setStyleSheet("color: red")
        stop_button.clicked.connect(self.stop)
        radio_button_layout.addWidget(start_button)
        radio_button_layout.addWidget(stop_button)
        start_label = QLabel('Start Hexadecimal Value set to puzzle 66:')
        start_label.setStyleSheet("color: green")
        self.start_edit = QLineEdit('20000000000000000')
        self.start_edit.setStyleSheet("color: green")
        end_label = QLabel('End Hexadecimal Value set to puzzle 66:')
        end_label.setStyleSheet("color: red")
        self.end_edit = QLineEdit('3ffffffffffffffff')
        self.end_edit.setStyleSheet("color: red")
        hex_label = QLabel('Current HEX value :')
        self.value_edit_hex = QLineEdit()
        self.value_edit_hex.setReadOnly(True)
        Bitcoin_address_label = QLabel('Current Bitcoin address:')
        self.btc_address_edit = QLineEdit()
        self.btc_address_edit.setReadOnly(True)
        layout = QVBoxLayout()
        layout.addLayout(radio_button_layout)
        layout.addWidget(start_label)
        layout.addWidget(self.start_edit)
        layout.addWidget(end_label)
        layout.addWidget(self.end_edit)
        layout.addWidget(hex_label)
        layout.addWidget(self.value_edit_hex)
        address_layout_BTC = QHBoxLayout()
        address_layout_BTC.addWidget(Bitcoin_address_label)
        address_layout_BTC.addWidget(self.btc_address_edit)
        layout.addLayout(address_layout_BTC)
        keys_layout = QHBoxLayout()

        found_keys_scanned_label = QLabel('Found')
        self.found_keys_scanned_edit = QLineEdit()
        self.found_keys_scanned_edit.setReadOnly(True)
        self.found_keys_scanned_edit.setText('0')

        total_keys_scanned_label = QLabel('Total keys scanned:')
        self.total_keys_scanned_edit = QLineEdit()
        self.total_keys_scanned_edit.setReadOnly(True)
        self.total_keys_scanned_edit.setText('0')

        keys_per_sec_label = QLabel('Keys per second:')
        self.keys_per_sec_edit = QLineEdit()
        self.keys_per_sec_edit.setReadOnly(True)

        total_time_label = QLabel('Total time scanning:')
        self.total_time_edit = QLineEdit()
        self.total_time_edit.setReadOnly(True)

        keys_layout.addWidget(found_keys_scanned_label)
        keys_layout.addWidget(self.found_keys_scanned_edit)
        keys_layout.addWidget(total_keys_scanned_label)
        keys_layout.addWidget(self.total_keys_scanned_edit)
        keys_layout.addWidget(keys_per_sec_label)
        keys_layout.addWidget(self.keys_per_sec_edit)
        keys_layout.addWidget(total_time_label)
        keys_layout.addWidget(self.total_time_edit)

        layout.addLayout(keys_layout)
        self.setLayout(layout)

        self.counter = 0
        progress_layout_text = QHBoxLayout()
        progress_label = QLabel('progress %')
        self.progress_bar = CustomProgressBar()
        self.progress_bar.setRange(0, 100)
        progress_layout_text.addWidget(progress_label)
        progress_layout_text.addWidget(self.progress_bar)
        layout.addLayout(progress_layout_text)
        Information_label = QLabel('<html><b><center><font color="green" size="5">-- Information from Current Check --</font></center></b></html>')
        information_layout = QVBoxLayout()
        self.Information_label_edit = QPlainTextEdit()
        self.Information_label_edit.setStyleSheet("QPlainTextEdit { background-color: #333; color: #00FF00; font-weight: bold; font-family: Courier; text-align: center; }")
        self.Information_label_edit.setReadOnly(True)
        information_layout.addWidget(Information_label)
        information_layout.addWidget(self.Information_label_edit)
        layout.addLayout(information_layout)


    def handle_results(self, result):
        self.Information_label_edit.appendPlainText(result)
    
    def convert_int(self, num: int):
        dict_suffix = {0: 'key', 1: 'Kkey/s', 2: 'Mkey/s', 3: 'Gkey/s', 4: 'Tkey/s', 5: 'Pkey/s', 6: 'Ekeys/s'}
        num *= 1.0
        idx = 0
        for ii in range(len(dict_suffix) - 1):
            if int(num / 1000) > 0:
                idx += 1
                num /= 1000
            else:
                break
        return f"{num:.2f} {dict_suffix[idx]}"
    
    def update_keys_per_sec_slot(self, keys_generated_counter):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        total_keys_scanned = keys_generated_counter
        keys_per_sec = total_keys_scanned / elapsed_time if elapsed_time > 0 else 0
        formatted_speed = self.convert_int(keys_per_sec)
        self.total_keys_scanned_edit.setText(str(total_keys_scanned))
        self.keys_per_sec_edit.setText(formatted_speed)

    def update_total_time(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        time_obj = QTime(0, 0)
        time_obj = time_obj.addSecs(int(elapsed_time))
        total_time_str = time_obj.toString("d:hh:mm:ss")
        
        if total_time_str.startswith("d:"):
            total_time_str = total_time_str[2:]

        self.total_time_edit.setText(total_time_str)


    def start(self):
        self.start_time = time.time()
        self.total_time_timer = QTimer()
        self.total_time_timer.timeout.connect(self.update_total_time)
        self.total_time_timer.start(1000)  # Update every second
        start_value = self.start_edit.text()
        end_value = self.end_edit.text()
        num_cpus = int(self.cpu_box.currentText())
        self.start_hex = int(start_value, 16)
        self.end_hex = int(end_value, 16)
        chunk_size = (self.end_hex - self.start_hex) // num_cpus
        if self.end_hex < self.start_hex:
            error_range= (f'\n\n !!!!!  ERROR !!!!!! \n Your Start HEX {start_value} is MORE that your Stop HEX {end_value}')
            self.handle_results(error_range)
        else:
            if self.sequence_button.isChecked():
                order = 'sequence'
            elif self.random_button.isChecked(): 
                order = 'random'
            ranges = [(self.start_hex + i * chunk_size, self.start_hex + (i + 1) * chunk_size) for i in range(num_cpus)]
            start_index = self.start_hex
            self.start_time = time.time()
            self.scanning = True
            self.counter = 0
            for i in range(num_cpus - 1, -1, -1):
                priv_start = ranges[i][0]
                priv_end = ranges[i][1]
                if start_index >= priv_start and start_index < priv_end:
                    displayprint = f'{order} CPU {i + 1}:\t{hex(priv_start)} - {hex(priv_end)}\t<<-- Current CPU'
                    self.Information_label_edit.appendPlainText(displayprint)
                else:
                    displayprint = f'{order} CPU {i + 1}:\t{hex(priv_start)} - {hex(priv_end)}'
                    self.Information_label_edit.appendPlainText(displayprint)

            self.threads = []
            for i in range(num_cpus):
                priv_start = ranges[i][0]
                priv_end = ranges[i][1]
                thread = KeyGenerationThread(priv_start, priv_end, order, num_cpus)
                thread.update_keys_per_sec.connect(self.update_keys_per_sec_slot)
                thread.value_edit_hex.connect(self.value_edit_hex_slot)
                thread.btc_address_edit.connect(self.btc_address_edit_slot)
                thread.found_keys_scanned_edit.connect(self.found_count__slot)
                thread.recoveryFinished.connect(self.handle_results)
                self.threads.append(thread)
                thread.start()

    def stop(self):
        for thread in self.threads:
            thread.terminate()
            self.worker_finished('Recovery Finished')

    def worker_finished(self, result):
        if self.scanning:
            QMessageBox.information(self, 'Recovery Finished', result)
        self.scanning = False


    def closeEvent(self, event):
        self.stop()
        super().closeEvent(event)

    def value_edit_hex_slot(self, hex_value):
        start= int(self.start_hex)
        stop= int(self.end_hex)
        total_steps = stop - start
        max_value = 10000
        scaled_current_step = int((int(hex_value, 16) - start) * max_value / total_steps)
        self.progress_bar.setMaximum(max_value)
        self.progress_bar.setValue(scaled_current_step)
        self.value_edit_hex.setText(hex_value)

    def btc_address_edit_slot(self, btc_address):
        self.btc_address_edit.setText(btc_address)
    
    def found_count__slot(self, found_count):
        self.found_keys_scanned_edit.setText(str(found_count))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CryptoHunterApp()
    window.show()
    sys.exit(app.exec_())