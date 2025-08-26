import sys
import os
import subprocess
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, 
    QProgressBar, QMessageBox, QLineEdit, QHBoxLayout
)
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QFont, QIcon, QDoubleValidator

class HMMSearchWorker(QThread):
    progress_signal = Signal(int)  # Progress bar updates
    status_signal = Signal(str)    # Status text updates
    finished_signal = Signal(bool)  # Search completion (success/failure)
    error_signal = Signal(str)      # Error messages for pop-ups

    def __init__(self, hmm_profile, seq_db, output_dir, output_file, evalue):
        super().__init__()
        self.hmm_profile = hmm_profile
        self.seq_db = seq_db
        self.output_dir = output_dir
        self.output_file = output_file
        self.evalue = evalue
        self.process = None
        self.stop_requested = False
        self.error_log_path = os.path.join(output_dir, 'hmmsearch_error.log')

    def run(self):
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            output_path = os.path.join(self.output_dir, self.output_file)
            
            if hasattr(sys, '_MEIPASS'):
                hmmsearch_path = os.path.join(sys._MEIPASS, 'tools', 'phylogenetic', 'hmmsearch.exe')
            else:
                base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                hmmsearch_path = os.path.join(base_dir, 'tools', 'phylogenetic', 'hmmsearch.exe')

            cmd = [
                hmmsearch_path,
                '--noali',
                '--notextw',
                '-E', str(self.evalue),
                '--tblout', output_path,
                self.hmm_profile,
                self.seq_db
            ]
            
            self.status_signal.emit(f"Running HMMsearch...")
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Simulated progress
            for i in range(1, 101, 10):
                if self.stop_requested:
                    self.process.terminate()
                    self.status_signal.emit("Process stopped by user.")
                    self.finished_signal.emit(False)
                    return
                self.progress_signal.emit(i)
                self.msleep(500)

            stdout, stderr = self.process.communicate()
            
            if self.process.returncode != 0:
                raise RuntimeError(f"HMMsearch failed: {stderr}")

            self.status_signal.emit(f"Search completed: {output_path}")
            self.progress_signal.emit(100)
            self.finished_signal.emit(True)
        except Exception as e:
            error_message = str(e)
            self.log_error(error_message)
            self.status_signal.emit("HMMsearch encountered an error. Check the log.")
            self.error_signal.emit(error_message)
            self.finished_signal.emit(False)

    def stop(self):
        """Request to stop the process."""
        self.stop_requested = True
        if self.process:
            self.process.terminate()

    def log_error(self, message):
        with open(self.error_log_path, 'w') as error_log:
            error_log.write(message + '\n')


class HMMSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.hmm_profile = None
        self.seq_db = None
        self.output_dir = None
        self.worker = None

    def init_ui(self):
        self.setWindowTitle("Genome Wide WorkBench")
        self.setWindowIcon(QIcon('src/image.png'))
        self.setGeometry(100, 100, 1000, 1000)

        layout = QVBoxLayout()

        # Header
        self.header_label = QLabel("HMMerSearch", alignment=Qt.AlignCenter)
        self.header_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        self.header_label.setStyleSheet("""
            QLabel {
                background-color: #2C3E50;
                color: white;
                padding: 10px;
                border-radius: 10px;
            }
        """)
        layout.addWidget(self.header_label)

        # File Inputs
        self.hmm_profile_input = self.create_file_input("HMM Profile:", self.browse_hmm_profile)
        self.seq_db_input = self.create_file_input("Sequence DB /Sequnce File:", self.browse_seq_db)
        self.output_dir_input = self.create_file_input("Output Directory:", self.choose_output_dir)

        layout.addLayout(self.hmm_profile_input)
        layout.addLayout(self.seq_db_input)
        layout.addLayout(self.output_dir_input)

        # Output File Name
        self.output_file_layout = QHBoxLayout()
        self.output_file_label = QLabel("Output File Name:")
        self.output_file_label.setFont(QFont("Arial", 12))  # Increased font size
        self.output_file_input = QLineEdit()
        self.output_file_input.setPlaceholderText("Enter output file name")
        self.output_file_input.setFont(QFont("Arial", 12))  # Increased font size
        self.output_file_input.textChanged.connect(self.check_ready)
        self.output_file_layout.addWidget(self.output_file_label)
        self.output_file_layout.addWidget(self.output_file_input)
        layout.addLayout(self.output_file_layout)

        # E-value Threshold
        self.evalue_layout = QHBoxLayout()
        self.evalue_label = QLabel("E-value Threshold:")
        self.evalue_label.setFont(QFont("Arial", 12))  # Increased font size
        # self.evalue_input = QLineEdit("10")
        self.evalue_input = QLineEdit("0.001")
        self.evalue_input.setFont(QFont("Arial", 12))  # Increased font size
        # self.evalue_input.setValidator(QDoubleValidator(0.0, 1000.0, 2))
        self.evalue_input.setValidator(QDoubleValidator(0.0, 1.0, 6))  # from 0 to 1, 6 decimal places

        self.evalue_layout.addWidget(self.evalue_label)
        self.evalue_layout.addWidget(self.evalue_input)
        layout.addLayout(self.evalue_layout)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start HMM Search")
        self.start_btn.setFixedSize(200, 50)
        self.start_btn.clicked.connect(self.start_search)
        self.start_btn.setEnabled(False)
        self.start_btn.setStyleSheet("""
        QPushButton {
        background-color: #2C3E50; 
        color: white; 
        border-radius: 10px;
        font-size: 14px;
          }
        QPushButton:disabled {
        background-color: #A0A0A0;
         }
         """)



        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setFixedSize(200, 50)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_search)
        self.stop_btn.setStyleSheet("""
       QPushButton {
        background-color: #2C3E50; 
        color: white; 
        border-radius: 10px;
        font-size: 14px;
        }
        QPushButton:disabled {
        background-color: #A0A0A0;
        }
     """)


        self.button_layout.addWidget(self.start_btn)
        self.button_layout.addWidget(self.stop_btn)
        layout.addLayout(self.button_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Status Label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    # def create_file_input(self, label, callback):
    #     layout = QHBoxLayout()
    #     line_edit = QLineEdit()
    #     line_edit.setReadOnly(True)
    #     btn = QPushButton("Browse...")
    #     btn.clicked.connect(callback)
    #     layout.addWidget(QLabel(label))
    #     layout.addWidget(line_edit)
    #     layout.addWidget(btn)
    #     line_edit.textChanged.connect(self.check_ready)
    #     return layout
    def create_file_input(self, label, callback):
        layout = QHBoxLayout()
    
        # Create label with bigger font
        lbl = QLabel(label)
        lbl.setFont(QFont("Arial", 12))  # Increased font size
    
       # Create read-only text box
        line_edit = QLineEdit()
        line_edit.setReadOnly(True)
        line_edit.setFont(QFont("Arial", 12))  # Increased font size
    
        # Browse Button with Blue Color
        btn = QPushButton("Browse...")
        btn.setStyleSheet("background-color: #2C3E50; color: white; font-weight: bold;")
        btn.clicked.connect(callback)
    
        layout.addWidget(lbl)
        layout.addWidget(line_edit)
        layout.addWidget(btn)
    
        line_edit.textChanged.connect(self.check_ready)
    
        return layout


    def browse_hmm_profile(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select HMM Profile ", "", "HMM Files (*.hmm);;All Files (*)")
        if file:
            self.hmm_profile = file
            self.hmm_profile_input.itemAt(1).widget().setText(file)
            self.check_ready()

    def browse_seq_db(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Sequence Database or Sequence File", "", "FASTA Files (*.fasta);;All Files (*)")
        if file:
            self.seq_db = file
            self.seq_db_input.itemAt(1).widget().setText(file)
            self.check_ready()

    def choose_output_dir(self):
        dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir:
            self.output_dir = dir
            self.output_dir_input.itemAt(1).widget().setText(dir)
            self.check_ready()

    def check_ready(self):
        self.start_btn.setEnabled(all([self.hmm_profile, self.seq_db, self.output_dir, self.output_file_input.text().strip()]))

    def start_search(self):
        self.progress_bar.setVisible(True)
        self.worker = HMMSearchWorker(self.hmm_profile, self.seq_db, self.output_dir, self.output_file_input.text(), self.evalue_input.text())
        self.worker.progress_signal.connect(self.progress_bar.setValue)
        self.worker.status_signal.connect(self.status_label.setText)
        self.worker.finished_signal.connect(self.handle_search_completion)
        self.worker.start()
        self.stop_btn.setEnabled(True)

    def stop_search(self):
        if self.worker:
            self.worker.stop()
        self.stop_btn.setEnabled(False)

    def handle_search_completion(self, success):
        if success:
            QMessageBox.information(self, "Success", "HMMsearch completed successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HMMSearchApp()
    window.show()
    sys.exit(app.exec())
