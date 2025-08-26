# import os
# import subprocess
# import logging
# from PySide6.QtWidgets import (
#     QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog,
#     QProgressBar, QMessageBox, QLineEdit, QHBoxLayout, QSizePolicy, QSpacerItem, QComboBox
# )
# from PySide6.QtCore import QThread, Signal, Qt, QSize
# from PySide6.QtGui import QFont, QIcon
# import sys
# import shutil

# class AlignThread(QThread):
#     progress_signal = Signal(str, str)  # Message, output file path
#     stopped_signal = Signal()

#     def __init__(self, seq_file, output_dir):
#         super().__init__()
#         self.seq_file = seq_file
#         self.output_dir = output_dir
#         self.error_log_path = os.path.join(self.output_dir, "bioalignx_error.log")
#         self.log_file = os.path.join(self.output_dir, "bioalignx_log_file.log")
#         self.process = None
#         self.stop_requested = False

#         # Clear existing log files
#         for log_path in [self.log_file, self.error_log_path]:
#             if os.path.exists(log_path):
#                 open(log_path, "w").close()

#         logging.basicConfig(
#             level=logging.INFO,
#             format="%(asctime)s - %(levelname)s - %(message)s",
#             handlers=[
#                 logging.FileHandler(self.log_file),
#                 logging.FileHandler(self.error_log_path),
#             ]
#         )

#         # Create temp folder
#         self.temp_dir = os.path.join(self.output_dir, "temp_files")
#         os.makedirs(self.temp_dir, exist_ok=True)

#     def run(self):
#         try:
#             # Build MUSCLE path
#             if hasattr(sys, '_MEIPASS'):
#                 muscle_dir = os.path.join(sys._MEIPASS, 'tools', 'phylogenetic', 'muscle.exe')
#             else:
#                 base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#                 muscle_dir = os.path.join(base_dir, 'tools', 'phylogenetic', 'muscle.exe')

#             # Generate output file name
#             seq_file_name = os.path.splitext(os.path.basename(self.seq_file))[0]
#             aligned_output = os.path.join(self.output_dir, f"{seq_file_name}.fa.aln")

#             # Run MUSCLE alignment
#             if self.stop_requested:
#                 self.stopped_signal.emit()
#                 return
#             self.run_command(f'"{muscle_dir}" -super5 "{self.seq_file}" -output "{aligned_output}" -threads 56')

#             # Signal completion
#             self.progress_signal.emit("Alignment Complete", aligned_output)

#             # Cleanup
#             self.cleanup_temp_dir()

#         except Exception as e:
#             if not self.stop_requested:
#                 self.log_error(str(e))
#                 self.progress_signal.emit(f"Error during alignment: {str(e)}", "Check alignment_log_file.log and alignment_error.log for details.")

#     def stop(self):
#         self.stop_requested = True
#         if self.process:
#             self.process.terminate()
#             self.process.wait()
#         self.cleanup_temp_dir()
#         self.stopped_signal.emit()

#     def log_error(self, message):
#         with open(self.error_log_path, "w") as error_log:
#             error_log.write(message + "\n")

#     def run_command(self, command):
#         if self.stop_requested:
#             raise RuntimeError("Process stopped by user.")
#         try:
#             logging.info(f"Running command: {command}")
#             with open(self.log_file, "a") as log:
#                 self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#                 stdout, stderr = self.process.communicate()
#                 log.write(f"Command: {command}\n")
#                 log.write(f"STDOUT: {stdout}\n")
#                 if stderr:
#                     log.write(f"STDERR: {stderr}\n")
#                     logging.error(f"STDERR: {stderr}")
#                 if self.process.returncode != 0:
#                     raise RuntimeError(f"Command failed with return code {self.process.returncode}: {stderr}")
#         except Exception as e:
#             self.log_error(str(e))
#             self.progress_signal.emit("Command encountered an error", "Please check the log for details.")
#             logging.error(f"An error occurred while running the command: {e}")
#             raise e

#     def cleanup_temp_dir(self):
#         try:
#             shutil.rmtree(self.temp_dir)
#             logging.info(f"Successfully removed temporary directory: {self.temp_dir}")
#         except Exception as e:
#             logging.error(f"Failed to remove temporary directory: {e}")

# class AlignApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.thread = None
#         self.init_ui()

#     def init_ui(self):
#         self.setWindowTitle("Genome Wide WorkBench")
#         self.setWindowIcon(QIcon('src/image.png'))
#         self.setGeometry(100, 100, 800, 600)

#         # Header
#         self.header_label = QLabel("BioAlignX")
#         self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.header_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
#         self.header_label.setStyleSheet("""
#             QLabel {
#                 background-color: #2C3E50;
#                 color: white;
#                 padding: 20px;
#                 border-radius: 12px;
#             }
#         """)
#         self.header_label.setFixedHeight(80)

#         # Main layout
#         self.layout = QVBoxLayout()
#         self.layout.setContentsMargins(10, 10, 10, 10)
#         self.layout.setSpacing(10)
#         self.layout.addWidget(self.header_label)

#         # Spacer
#         spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
#         self.layout.addItem(spacer)

#         # File selection
#         self.input_width = 400
#         self.file_layout = QHBoxLayout()
#         self.seq_file_display = QLineEdit(self)
#         self.seq_file_display.setReadOnly(True)
#         self.seq_file_display.setPlaceholderText("No sequence file chosen")
#         self.seq_file_display.setFixedWidth(self.input_width)
#         self.seq_file_display.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 14px;
#                 border-radius: 4px;
#             }
#         """)
#         self.file_layout.addWidget(self.seq_file_display)

#         self.load_seq_file_button = QPushButton("Select FASTA File")
#         self.load_seq_file_button.setFixedSize(200, 50)
#         self.load_seq_file_button.setIcon(QIcon("upload_icon.png"))
#         self.load_seq_file_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 14px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 padding: 10px;
#             }
#             QPushButton:hover {
#                 background-color: #34495E;
#             }
#             QPushButton:pressed {
#                 background-color: #34495E;
#             }
#         """)
#         self.load_seq_file_button.clicked.connect(self.open_seq_file_dialog)
#         self.file_layout.addWidget(self.load_seq_file_button)
#         self.layout.addLayout(self.file_layout)

#         # Output directory
#         self.dir_layout = QHBoxLayout()
#         self.dir_display = QLineEdit(self)
#         self.dir_display.setReadOnly(True)
#         self.dir_display.setPlaceholderText("No output directory chosen")
#         self.dir_display.setFixedWidth(self.input_width)
#         self.dir_display.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 14px;
#                 border-radius: 4px;
#             }
#         """)
#         self.dir_layout.addWidget(self.dir_display)

#         self.load_output_button = QPushButton("Select Output Directory")
#         self.load_output_button.setFixedSize(200, 50)
#         self.load_output_button.setIcon(QIcon("folder_icon.png"))
#         self.load_output_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 14px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 padding: 10px;
#             }
#             QPushButton:hover {
#                 background-color: #34495E;
#             }
#             QPushButton:pressed {
#                 background-color: #34495E;
#             }
#         """)
#         self.load_output_button.clicked.connect(self.open_output_dir_dialog)
#         self.dir_layout.addWidget(self.load_output_button)
#         self.layout.addLayout(self.dir_layout)

#         # Button layout
#         self.button_layout = QHBoxLayout()
#         self.button_layout.addStretch()

#         # Submit button
#         self.align_button = QPushButton("Align")
#         self.align_button.setFixedSize(150, 40)
#         self.align_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 14px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 padding: 10px;
#             }
#             QPushButton:hover {
#                 background-color: #34495E;
#             }
#             QPushButton:pressed {
#                 background-color: #34495E;
#             }
#         """)
#         self.align_button.clicked.connect(self.start_alignment)
#         self.button_layout.addWidget(self.align_button)

#         # Stop button
#         self.stop_button = QPushButton("Stop")
#         self.stop_button.setFixedSize(150, 40)
#         self.stop_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 14px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 padding: 10px;
#             }
#             QPushButton:hover {
#                 background-color: #34495E;
#             }
#             QPushButton:pressed {
#                 background-color: #34495E;
#             }
#             QPushButton:disabled {
#                 background-color: #A0A0A0;
#             }
#         """)
#         self.stop_button.setEnabled(False)
#         self.stop_button.clicked.connect(self.stop_process)
#         self.button_layout.addWidget(self.stop_button)

#         self.button_layout.addStretch()
#         self.layout.addLayout(self.button_layout)

#         # Progress bar
#         self.progress_bar = QProgressBar(self)
#         self.progress_bar.setRange(0, 0)
#         self.progress_bar.setVisible(False)
#         self.layout.addWidget(self.progress_bar)

#         # Final spacer
#         self.layout.addItem(spacer)

#         self.setLayout(self.layout)

#     def open_seq_file_dialog(self):
#         file_name, _ = QFileDialog.getOpenFileName(self, "Open Sequence FASTA File", "", "FASTA Files (*.fa *.fasta);;All Files (*)")
#         if file_name:
#             self.seq_file_display.setText(file_name)

#     def open_output_dir_dialog(self):
#         output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
#         if output_dir:
#             self.dir_display.setText(output_dir)

#     def start_alignment(self):
#         seq_file = self.seq_file_display.text()
#         output_dir = self.dir_display.text()

#         if not seq_file or not output_dir:
#             QMessageBox.warning(self, "Input Error", "Please provide a sequence file and output directory.")
#             return

#         self.align_button.setEnabled(False)
#         self.stop_button.setEnabled(True)
#         self.progress_bar.setVisible(True)
#         self.thread = AlignThread(seq_file, output_dir)
#         self.thread.progress_signal.connect(self.on_progress)
#         self.thread.stopped_signal.connect(self.on_stopped)
#         self.thread.start()

#     def stop_process(self):
#         if self.thread:
#             self.thread.stop()

#     def on_stopped(self):
#         self.stop_button.setEnabled(False)
#         self.align_button.setEnabled(True)
#         self.progress_bar.setVisible(False)
#         QMessageBox.information(self, "Process Stopped", "The alignment process was stopped by the user.")

#     def on_progress(self, message, file_path):
#         self.stop_button.setEnabled(False)
#         self.align_button.setEnabled(True)
#         self.progress_bar.setVisible(False)
#         QMessageBox.information(self, "Process Completed", f"{message}\nOutput file: {file_path}")

#     def closeEvent(self, event):
#         msg_box = QMessageBox(self)
#         msg_box.setWindowTitle("Exit Application")
#         msg_box.setText("Are you sure you want to quit the application?")
#         msg_box.setIcon(QMessageBox.Question)
#         yes_button = msg_box.addButton("Yes", QMessageBox.YesRole)
#         minimize_button = msg_box.addButton("Minimize", QMessageBox.NoRole)
#         no_button = msg_box.addButton("No", QMessageBox.RejectRole)
#         msg_box.exec()
#         if msg_box.clickedButton() == yes_button:
#             if self.thread and self.thread.isRunning():
#                 self.thread.stop()
#                 # Wait for the thread to finish stopping
#                 self.thread.wait()
#             event.accept()
#         elif msg_box.clickedButton() == minimize_button:
#             event.ignore()
#             self.showMinimized()
#         else:
#             event.ignore()

# if __name__ == "__main__":
#     app = QApplication([])
#     window = AlignApp()
#     window.show()
#     app.exec()

import os
import subprocess
import logging
import webbrowser
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog,
    QProgressBar, QMessageBox, QLineEdit, QHBoxLayout, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import QThread, Signal, Qt, QSize
from PySide6.QtGui import QFont, QIcon
import sys
import shutil

class AlignThread(QThread):
    progress_signal = Signal(str, str)  # Message, output file path
    stopped_signal = Signal()

    def __init__(self, seq_file, output_dir):
        super().__init__()
        self.seq_file = seq_file
        self.output_dir = output_dir
        self.error_log_path = os.path.join(self.output_dir, "bioalignx_error.log")
        self.log_file = os.path.join(self.output_dir, "bioalignx_log_file.log")
        self.process = None
        self.stop_requested = False

        # Clear existing log files
        for log_path in [self.log_file, self.error_log_path]:
            if os.path.exists(log_path):
                open(log_path, "w").close()

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(self.log_file),
                logging.FileHandler(self.error_log_path),
            ]
        )

        # Create temp folder
        self.temp_dir = os.path.join(self.output_dir, "temp_files")
        os.makedirs(self.temp_dir, exist_ok=True)

    def run(self):
        try:
            # Build MUSCLE path
            if hasattr(sys, '_MEIPASS'):
                muscle_dir = os.path.join(sys._MEIPASS, 'tools', 'phylogenetic', 'muscle.exe')
            else:
                base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                muscle_dir = os.path.join(base_dir, 'tools', 'phylogenetic', 'muscle.exe')

            # Generate output file name
            seq_file_name = os.path.splitext(os.path.basename(self.seq_file))[0]
            aligned_output = os.path.join(self.output_dir, f"{seq_file_name}.fa.aln")

            # Run MUSCLE alignment
            if self.stop_requested:
                self.stopped_signal.emit()
                return
            self.run_command(f'"{muscle_dir}" -super5 "{self.seq_file}" -output "{aligned_output}" -threads 56')

            # Signal completion
            self.progress_signal.emit("Alignment Complete", aligned_output)

            # Cleanup
            self.cleanup_temp_dir()

        except Exception as e:
            if not self.stop_requested:
                self.log_error(str(e))
                self.progress_signal.emit(f"Error during alignment: {str(e)}", "Check alignment_log_file.log and alignment_error.log for details.")

    def stop(self):
        self.stop_requested = True
        if self.process:
            self.process.terminate()
            self.process.wait()
        self.cleanup_temp_dir()
        self.stopped_signal.emit()

    def log_error(self, message):
        with open(self.error_log_path, "w") as error_log:
            error_log.write(message + "\n")

    def run_command(self, command):
        if self.stop_requested:
            raise RuntimeError("Process stopped by user.")
        try:
            logging.info(f"Running command: {command}")
            with open(self.log_file, "a") as log:
                self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = self.process.communicate()
                log.write(f"Command: {command}\n")
                log.write(f"STDOUT: {stdout}\n")
                if stderr:
                    log.write(f"STDERR: {stderr}\n")
                    logging.error(f"STDERR: {stderr}")
                if self.process.returncode != 0:
                    raise RuntimeError(f"Command failed with return code {self.process.returncode}: {stderr}")
        except Exception as e:
            self.log_error(str(e))
            self.progress_signal.emit("Command encountered an error", "Please check the log for details.")
            logging.error(f"An error occurred while running the command: {e}")
            raise e

    def cleanup_temp_dir(self):
        try:
            shutil.rmtree(self.temp_dir)
            logging.info(f"Successfully removed temporary directory: {self.temp_dir}")
        except Exception as e:
            logging.error(f"Failed to remove temporary directory: {e}")

class AlignApp(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.last_output_file = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Genome Wide WorkBench")
        self.setWindowIcon(QIcon('src/image.png'))
        self.setGeometry(100, 100, 800, 600)

        # Header
        self.header_label = QLabel("BioAlignX")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.header_label.setStyleSheet("""
            QLabel {
                background-color: #2C3E50;
                color: white;
                padding: 20px;
                border-radius: 12px;
            }
        """)
        self.header_label.setFixedHeight(80)

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        self.layout.addWidget(self.header_label)

        # Spacer
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer)

        # File selection
        self.input_width = 400
        self.file_layout = QHBoxLayout()
        self.seq_file_display = QLineEdit(self)
        self.seq_file_display.setReadOnly(True)
        self.seq_file_display.setPlaceholderText("No sequence file chosen")
        self.seq_file_display.setFixedWidth(self.input_width)
        self.seq_file_display.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2C3E50;
                padding: 5px;
                font-size: 14px;
                border-radius: 4px;
            }
        """)
        self.file_layout.addWidget(self.seq_file_display)

        self.load_seq_file_button = QPushButton("Select FASTA File")
        self.load_seq_file_button.setFixedSize(200, 50)
        self.load_seq_file_button.setIcon(QIcon("upload_icon.png"))
        self.load_seq_file_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                color: white;
                background-color: #2C3E50;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            QPushButton:pressed {
                background-color: #34495E;
            }
        """)
        self.load_seq_file_button.clicked.connect(self.open_seq_file_dialog)
        self.file_layout.addWidget(self.load_seq_file_button)
        self.layout.addLayout(self.file_layout)

        # Output directory
        self.dir_layout = QHBoxLayout()
        self.dir_display = QLineEdit(self)
        self.dir_display.setReadOnly(True)
        self.dir_display.setPlaceholderText("No output directory chosen")
        self.dir_display.setFixedWidth(self.input_width)
        self.dir_display.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2C3E50;
                padding: 5px;
                font-size: 14px;
                border-radius: 4px;
            }
        """)
        self.dir_layout.addWidget(self.dir_display)

        self.load_output_button = QPushButton("Select Output Directory")
        self.load_output_button.setFixedSize(200, 50)
        self.load_output_button.setIcon(QIcon("folder_icon.png"))
        self.load_output_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                color: white;
                background-color: #2C3E50;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            QPushButton:pressed {
                background-color: #34495E;
            }
        """)
        self.load_output_button.clicked.connect(self.open_output_dir_dialog)
        self.dir_layout.addWidget(self.load_output_button)
        self.layout.addLayout(self.dir_layout)

        # Button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()

        # Submit button
        self.align_button = QPushButton("Align")
        self.align_button.setFixedSize(150, 40)
        self.align_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                color: white;
                background-color: #2C3E50;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            QPushButton:pressed {
                background-color: #34495E;
            }
        """)
        self.align_button.clicked.connect(self.start_alignment)
        self.button_layout.addWidget(self.align_button)

        # Stop button
        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedSize(150, 40)
        self.stop_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                color: white;
                background-color: #2C3E50;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            QPushButton:pressed {
                background-color: #34495E;
            }
            QPushButton:disabled {
                background-color: #A0A0A0;
            }
        """)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_process)
        self.button_layout.addWidget(self.stop_button)

        self.button_layout.addStretch()
        self.layout.addLayout(self.button_layout)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)

        # Visualization buttons (hidden initially)
        self.visualization_layout = QHBoxLayout()
        self.visualization_layout.addStretch()
        
        self.aliview_button = QPushButton("View in AliView")
        self.aliview_button.setFixedSize(150, 40)
        self.aliview_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                color: white;
                background-color: #27AE60;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2ECC71;
            }
            QPushButton:pressed {
                background-color: #2ECC71;
            }
            QPushButton:disabled {
                background-color: #A0A0A0;
            }
        """)
        self.aliview_button.setEnabled(False)
        self.aliview_button.clicked.connect(self.open_aliview)
        self.visualization_layout.addWidget(self.aliview_button)
        
        self.dendroscope_button = QPushButton("View in Dendroscope")
        self.dendroscope_button.setFixedSize(150, 40)
        self.dendroscope_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                color: white;
                background-color: #2980B9;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3498DB;
            }
            QPushButton:pressed {
                background-color: #3498DB;
            }
            QPushButton:disabled {
                background-color: #A0A0A0;
            }
        """)
        self.dendroscope_button.setEnabled(False)
        self.dendroscope_button.clicked.connect(self.open_dendroscope)
        self.visualization_layout.addWidget(self.dendroscope_button)
        
        self.visualization_layout.addStretch()
        self.layout.addLayout(self.visualization_layout)

        # Final spacer
        self.layout.addItem(spacer)

        self.setLayout(self.layout)

    def open_seq_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Sequence FASTA File", "", "FASTA Files (*.fa *.fasta);;All Files (*)")
        if file_name:
            self.seq_file_display.setText(file_name)

    def open_output_dir_dialog(self):
        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if output_dir:
            self.dir_display.setText(output_dir)

    def start_alignment(self):
        seq_file = self.seq_file_display.text()
        output_dir = self.dir_display.text()

        if not seq_file or not output_dir:
            QMessageBox.warning(self, "Input Error", "Please provide a sequence file and output directory.")
            return

        self.align_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.aliview_button.setEnabled(False)
        self.dendroscope_button.setEnabled(False)
        self.thread = AlignThread(seq_file, output_dir)
        self.thread.progress_signal.connect(self.on_progress)
        self.thread.stopped_signal.connect(self.on_stopped)
        self.thread.start()

    def stop_process(self):
        if self.thread:
            self.thread.stop()

    def on_stopped(self):
        self.stop_button.setEnabled(False)
        self.align_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        QMessageBox.information(self, "Process Stopped", "The alignment process was stopped by the user.")

    def on_progress(self, message, file_path):
        self.stop_button.setEnabled(False)
        self.align_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.last_output_file = file_path
        
        # Enable visualization buttons
        self.aliview_button.setEnabled(True)
        self.dendroscope_button.setEnabled(True)
        
        QMessageBox.information(self, "Process Completed", f"{message}\nOutput file: {file_path}")

    def open_aliview(self):
        if self.last_output_file and os.path.exists(self.last_output_file):
            # Open AliView website or launch application if installed
            webbrowser.open("https://ormbunkar.se/aliview/")
        else:
            QMessageBox.warning(self, "File Not Found", "The alignment output file doesn't exist.")

    def open_dendroscope(self):
        if self.last_output_file and os.path.exists(self.last_output_file):
            # Open Dendroscope website or launch application if installed
            webbrowser.open("https://software-ab.informatik.uni-tuebingen.de/download/dendroscope/welcome.html")
        else:
            QMessageBox.warning(self, "File Not Found", "The alignment output file doesn't exist.")

    def closeEvent(self, event):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Exit Application")
        msg_box.setText("Are you sure you want to quit the application?")
        msg_box.setIcon(QMessageBox.Question)
        yes_button = msg_box.addButton("Yes", QMessageBox.YesRole)
        minimize_button = msg_box.addButton("Minimize", QMessageBox.NoRole)
        no_button = msg_box.addButton("No", QMessageBox.RejectRole)
        msg_box.exec()
        if msg_box.clickedButton() == yes_button:
            if self.thread and self.thread.isRunning():
                self.thread.stop()
                # Wait for the thread to finish stopping
                self.thread.wait()
            event.accept()
        elif msg_box.clickedButton() == minimize_button:
            event.ignore()
            self.showMinimized()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication([])
    window = AlignApp()
    window.show()
    app.exec()