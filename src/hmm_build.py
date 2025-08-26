import sys
import os
import subprocess
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, 
                               QLabel, QFileDialog, QProgressBar, QMessageBox, 
                               QLineEdit, QHBoxLayout, QGroupBox, QRadioButton)
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QFont, QIcon, QDoubleValidator

class HMMBuildWorker(QThread):
    progress_signal = Signal(str)
    finished_signal = Signal(bool, str)  # True for success, False for error

    def __init__(self, alignment_file, output_hmm, output_dir, weighting_option, wid_value):
        super().__init__()
        self.alignment_file = alignment_file
        self.output_hmm = output_hmm
        self.output_dir = output_dir
        self.weighting_option = weighting_option
        self.wid_value = wid_value
        self.error_log_path = os.path.join(output_dir, 'hmmbuild_error.log')
        self.process = None  # To store the running process

    def run(self):
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            output_path = os.path.join(self.output_dir, self.output_hmm)
            
            if hasattr(sys, '_MEIPASS'):
                hmmbuild_path = os.path.join(sys._MEIPASS, 'tools', 'phylogenetic', 'hmmbuild.exe')
            else:
                base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                hmmbuild_path = os.path.join(base_dir, 'tools', 'phylogenetic', 'hmmbuild.exe')

            cmd = [f'"{hmmbuild_path}"', self.weighting_option]

            if self.weighting_option == '--wblosum' and self.wid_value.strip():
                cmd += ['--wid', self.wid_value]

            cmd += [f'"{output_path}"', f'"{self.alignment_file}"']
            
            self.progress_signal.emit(f"Running HMMbuild: {' '.join(cmd)}")
            self.process = subprocess.Popen(' '.join(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            stdout, stderr = self.process.communicate()

            if self.process.returncode != 0:
                raise RuntimeError(f"HMMbuild failed: {stderr}")

            self.progress_signal.emit(f"HMM profile built successfully: {output_path}")
            self.finished_signal.emit(True, output_path)  # Notify success
            
        except Exception as e:
            self.log_error(str(e))
            self.progress_signal.emit("HMMbuild encountered an error. Check the log.")
            self.finished_signal.emit(False, "HMMBuild failed! Check the log file for details.")  # Notify error

    def log_error(self, message):
        with open(self.error_log_path, 'w') as error_log:
            error_log.write(message + '\n')

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.progress_signal.emit("Process stopped by user.")
            self.finished_signal.emit(False, "Process terminated by user.")

class HMMBuildApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.alignment_file = None
        self.output_dir = None
        self.worker = None  # To store running thread

    def init_ui(self):
        self.setWindowTitle("Genome Wide WorkBench")
        self.setWindowIcon(QIcon('src/image.png'))
        self.setGeometry(100, 100, 1000, 800)

        # Header
        self.header_label = QLabel("HMMerBuild")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        self.header_label.setStyleSheet("""
            QLabel {
                background-color: #2C3E50;
                color: white;
                padding: 10px;
                border-radius: 10px;
            }
        """)
        self.header_label.setFixedHeight(100)

        # Layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Input Fields
        self.alignment_input = self.create_file_input("Alignment Protein File:", "Browse...", self.browse_alignment_file)
        self.output_dir_input = self.create_file_input("Output Directory:", "Choose...", self.choose_output_dir)
        
        # Output File Name
        self.output_file_layout = QHBoxLayout()
        self.output_file_label = QLabel("Output HMM Name:")
        self.output_file_input = QLineEdit()
        self.output_file_input.setPlaceholderText("Enter output HMM file name")
        self.output_file_input.textChanged.connect(self.check_ready)
        self.output_file_layout.addWidget(self.output_file_label)
        self.output_file_layout.addWidget(self.output_file_input)
        
        # Weighting Options
        weight_group = QGroupBox("Sequence Weighting Options")
        weight_layout = QVBoxLayout()

        self.wpb_radio = QRadioButton("Henikoff position-based (default)")
        self.wgsc_radio = QRadioButton("Gerstein/Sonnhammer/Chothia")
        self.wblosum_radio = QRadioButton("BLOSUM-based clustering")
        self.wnone_radio = QRadioButton("Uniform weights")
        self.wpb_radio.setChecked(True)

        wid_layout = QHBoxLayout()
        self.wid_label = QLabel("Identity threshold (--wid):")
        self.wid_input = QLineEdit()
        self.wid_input.setPlaceholderText("e.g., 0.62")
        self.wid_input.setEnabled(False)
        self.wid_input.setValidator(QDoubleValidator(0.0, 1.0, 2, self))
        wid_layout.addWidget(self.wid_label)
        wid_layout.addWidget(self.wid_input)

        weight_layout.addWidget(self.wpb_radio)
        weight_layout.addWidget(self.wgsc_radio)
        weight_layout.addWidget(self.wblosum_radio)
        weight_layout.addWidget(self.wnone_radio)
        weight_layout.addLayout(wid_layout)
        weight_group.setLayout(weight_layout)

        # Connect radio buttons to update wid input state
        for radio in [self.wpb_radio, self.wgsc_radio, self.wblosum_radio, self.wnone_radio]:
            radio.toggled.connect(self.update_wid_enabled)

        # Add components to main layout
        layout.addWidget(self.header_label)
        layout.addLayout(self.alignment_input)
        layout.addLayout(self.output_dir_input)
        layout.addLayout(self.output_file_layout)
        layout.addWidget(weight_group)

        # Start Button
        self.start_btn = QPushButton("Start HMM Build")
        self.start_btn.setFixedSize(250, 50)
        self.start_btn.setStyleSheet(self.get_button_style())
        self.start_btn.clicked.connect(self.start_build)
        layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Stop Button
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setFixedSize(250, 50)
        self.stop_btn.setStyleSheet(self.get_button_style())
        self.stop_btn.setVisible(False)
        self.stop_btn.clicked.connect(self.stop_build)
        layout.addWidget(self.stop_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Status
        self.status_label = QLabel()
        self.status_label.setStyleSheet("font-size: 14px; color: #2C3E50;")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def create_file_input(self, label, button_text, callback):
        layout = QHBoxLayout()

        line_edit = QLineEdit()
        line_edit.setReadOnly(True)
        line_edit.setPlaceholderText(f"No {label.lower()} selected")
        line_edit.setFixedHeight(40)

        btn = QPushButton(button_text)
        btn.setFixedSize(120, 40)
        btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                color: white;
                background-color: #2C3E50;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn.clicked.connect(callback)

        layout.addWidget(QLabel(label))
        layout.addWidget(line_edit)
        layout.addWidget(btn)
    
        line_edit.textChanged.connect(self.check_ready)
        return layout

    def update_wid_enabled(self):
        self.wid_input.setEnabled(self.wblosum_radio.isChecked())

    def browse_alignment_file(self):
        # file, _ = QFileDialog.getOpenFileName(self, "Select Alignment File", "", "Stockholm Files (*.sto);;All Files (*)")
        file, _ = QFileDialog.getOpenFileName(self,"Select Alignment or HMM File","",
                                              "Supported Files (*.sto *.hmm);;Stockholm Files (*.sto);;HMM Files (*.hmm);;All Files (*)"
                                              )

        if file:
            self.alignment_file = file
            self.alignment_input.itemAt(1).widget().setText(os.path.basename(file))
            self.check_ready()

    def choose_output_dir(self):
        dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir:
            self.output_dir = dir
            self.output_dir_input.itemAt(1).widget().setText(dir)
            self.check_ready()

    def check_ready(self):
        ready = all([
            os.path.exists(self.alignment_file) if self.alignment_file else False,
            os.path.exists(self.output_dir) if self.output_dir else False,
            bool(self.output_file_input.text().strip())
        ])
        self.start_btn.setEnabled(ready)

    def start_build(self):
        output_hmm = self.output_file_input.text().strip()

        if not self.alignment_file:
            QMessageBox.critical(self, "Error", "Please select an alignment file before starting.")
            return
        if not self.output_dir:
            QMessageBox.critical(self, "Error", "Please choose an output directory before starting.")
            return
        if not output_hmm:
            QMessageBox.critical(self, "Error", "Please enter an output HMM file name before starting.")
            return

        # Determine weighting options
        weighting_option = '--wpb'
        if self.wgsc_radio.isChecked():
            weighting_option = '--wgsc'
        elif self.wblosum_radio.isChecked():
            weighting_option = '--wblosum'
        elif self.wnone_radio.isChecked():
            weighting_option = '--wnone'

        wid_value = self.wid_input.text().strip() if self.wblosum_radio.isChecked() else ''

        self.worker = HMMBuildWorker(
            self.alignment_file,
            output_hmm,
            self.output_dir,
            weighting_option,
            wid_value
        )
        self.worker.progress_signal.connect(self.status_label.setText)
        self.worker.finished_signal.connect(self.show_popup)
        self.worker.start()

        self.progress_bar.setVisible(True)
        self.stop_btn.setVisible(True)

    def stop_build(self):
        if self.worker:
            self.worker.stop()

    def show_popup(self, success, message):
        self.progress_bar.setVisible(False)
        self.stop_btn.setVisible(False)
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)

    def get_button_style(self):
        return """
            QPushButton {
                font-size: 16px;
                color: white;
                background-color: #2C3E50;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #34495E; }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HMMBuildApp()
    window.show()
    sys.exit(app.exec())