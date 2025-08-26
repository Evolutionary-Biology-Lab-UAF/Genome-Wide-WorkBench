# import sys
# import os
# import subprocess
# import pandas as pd
# from PySide6.QtWidgets import (
#     QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget,
#     QLabel, QLineEdit, QFormLayout, QMessageBox, QHBoxLayout, QComboBox
# )
# from PySide6.QtGui import QIcon, QFont
# from PySide6.QtCore import QThread, Signal, Qt

# class Worker(QThread):
#     finished = Signal()
#     error = Signal(str)

#     def __init__(self, command, log_file):
#         super().__init__()
#         self.command = command
#         self.log_file = log_file

#     # def run(self):
#     #     try:
#     #         result = subprocess.run(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     #         with open(self.log_file, 'a') as log:
#     #             log.write("=== DIAMOND Command ===\n")
#     #             log.write(" ".join(self.command) + "\n")
#     #             log.write("=== Output ===\n")
#     #             log.write(result.stdout if result.stdout else "No output.\n")
#     #             log.write("=== Errors ===\n")
#     #             log.write(result.stderr if result.stderr else "No errors.\n")
#     #         if result.returncode != 0:
#     #             self.error.emit(result.stderr)
#     #         else:
#     #             self.finished.emit()
#     #     except Exception as e:
#     #         with open(self.log_file, 'a') as log:
#     #             log.write(f"\nException occurred: {str(e)}\n")
#     #         self.error.emit(str(e))
#     def run(self):
#       try:
#         result = subprocess.run(
#             self.command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )

#         # Log everything
#         with open(self.log_file, 'a') as log:
#             log.write("=== DIAMOND Command ===\n")
#             log.write(" ".join(self.command) + "\n")
#             log.write("=== Output ===\n")
#             log.write(result.stdout if result.stdout else "No output.\n")
#             log.write("=== Errors ===\n")
#             log.write(result.stderr if result.stderr else "No errors.\n")

#         # Define error-indicative keywords
#         error_keywords = ["error", "failed", "exception", "segmentation fault"]

#         # Check if there's a real error
#         is_error = (
#             result.returncode != 0 and
#             any(word in result.stderr.lower() for word in error_keywords)
#         )

#         if is_error:
#             self.error.emit(result.stderr)
#         else:
#             self.finished.emit()

#       except Exception as e:
#         with open(self.log_file, 'a') as log:
#             log.write(f"\nException occurred: {str(e)}\n")
#         self.error.emit(str(e))


# class DiamondHomology(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Genome Wide WorkBench")
#         self.setWindowIcon(QIcon('src/image.png'))
#         self.setGeometry(100, 100, 1000, 1000)

#         # Header
#         self.header_label = QLabel("Homologus Pair Finder")
#         self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.header_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
#         self.header_label.setStyleSheet("""
#             QLabel {
#                 background-color: #2C3E50;
#                 color: white;
#                 padding: 20px;
#                 border-radius: 12px;
#             }
#         """)

#         # Buttons and Inputs
#         self.query_button = QPushButton("Load Query FASTA")
#         self.query_button.setIcon(QIcon('upload_icon.png'))
#         self.query_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 16px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 padding: 10px 20px;
#             }
#             QPushButton:hover {
#                 background-color: #34495E;
#             }
#         """)
#         self.query_button.clicked.connect(self.load_query_file)

#         self.ref_button = QPushButton("Load Reference FASTA")
#         self.ref_button.setIcon(QIcon('upload_icon.png'))
#         self.ref_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 16px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 padding: 10px 20px;
#             }
#             QPushButton:hover {
#                 background-color: #34495E;
#             }
#         """)
#         self.ref_button.clicked.connect(self.load_ref_file)

#         self.dir_button = QPushButton("Choose Output Directory")
#         self.dir_button.setIcon(QIcon('folder_icon.png'))
#         self.dir_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 16px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 padding: 10px 20px;
#             }
#             QPushButton:hover {
#                 background-color: #34495E;
#             }
#         """)
#         self.dir_button.clicked.connect(self.choose_directory)

#         self.query_display = QLineEdit()
#         self.query_display.setReadOnly(True)
#         self.query_display.setPlaceholderText("No query file chosen")
#         self.query_display.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.ref_display = QLineEdit()
#         self.ref_display.setReadOnly(True)
#         self.ref_display.setPlaceholderText("No reference file chosen")
#         self.ref_display.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.output_dir_display = QLineEdit()
#         self.output_dir_display.setReadOnly(True)
#         self.output_dir_display.setPlaceholderText("No directory chosen")
#         self.output_dir_display.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.evalue_input = QLineEdit("1e-5")
#         self.evalue_input.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.identity_input = QLineEdit("30")
#         self.identity_input.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.threads_input = QLineEdit("4")
#         self.threads_input.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.mode_combo = QComboBox()
#         self.mode_combo.addItems(["fast", "sensitive", "more-sensitive"])
#         self.mode_combo.setStyleSheet("""
#             QComboBox {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.align_type_combo = QComboBox()
#         self.align_type_combo.addItems(["blastp", "blastx"])
#         self.align_type_combo.setStyleSheet("""
#             QComboBox {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.output_file_input = QLineEdit("homologous_pairs.xlsx")
#         self.output_file_input.setPlaceholderText("Enter output file name (default: homologous_pairs.xlsx)")
#         self.output_file_input.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.run_button = QPushButton("Run")
#         self.run_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 16px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 padding: 10px 20px;
#             }
#             QPushButton:hover {
#                 background-color: #34495E;
#             }
#         """)
#         self.run_button.setEnabled(False)
#         self.run_button.clicked.connect(self.run_diamond)

#         # Layout
#         main_layout = QVBoxLayout()
#         main_layout.addWidget(self.header_label)

#         form_layout = QFormLayout()
#         query_layout = QHBoxLayout()
#         query_layout.addWidget(self.query_button)
#         query_layout.addWidget(self.query_display)
#         form_layout.addRow(QLabel("Query FASTA File:"), query_layout)

#         ref_layout = QHBoxLayout()
#         ref_layout.addWidget(self.ref_button)
#         ref_layout.addWidget(self.ref_display)
#         form_layout.addRow(QLabel("Reference FASTA File:"), ref_layout)

#         dir_layout = QHBoxLayout()
#         dir_layout.addWidget(self.dir_button)
#         dir_layout.addWidget(self.output_dir_display)
#         form_layout.addRow(QLabel("Output Directory:"), dir_layout)

#         form_layout.addRow(QLabel("Output File Name:"), self.output_file_input)
#         form_layout.addRow(QLabel("Alignment Type:"), self.align_type_combo)
#         form_layout.addRow(QLabel("Sensitivity Mode:"), self.mode_combo)
#         form_layout.addRow(QLabel("E-value Threshold:"), self.evalue_input)
#         form_layout.addRow(QLabel("Min Identity (%):"), self.identity_input)
#         form_layout.addRow(QLabel("Number of Threads:"), self.threads_input)

#         main_layout.addLayout(form_layout)

#         button_layout = QHBoxLayout()
#         button_layout.addWidget(self.run_button)
#         button_layout.addStretch()

#         main_layout.addLayout(button_layout)
#         main_layout.addStretch()

#         container = QWidget()
#         container.setLayout(main_layout)
#         self.setCentralWidget(container)

#     def load_query_file(self):
#         file_name, _ = QFileDialog.getOpenFileName(
#             self, "Open Query FASTA", "", "FASTA Files (*.fa *.fasta);;All Files (*)"
#         )
#         if file_name:
#             self.query_display.setText(file_name)
#             self.check_inputs()

#     def load_ref_file(self):
#         file_name, _ = QFileDialog.getOpenFileName(
#             self, "Open Reference FASTA", "", "FASTA Files (*.fa *.fasta);;All Files (*)"
#         )
#         if file_name:
#             self.ref_display.setText(file_name)
#             self.check_inputs()

#     def choose_directory(self):
#         directory = QFileDialog.getExistingDirectory(self, "Choose Output Directory")
#         if directory:
#             self.output_dir_display.setText(directory)
#             self.check_inputs()

#     def check_inputs(self):
#         if (self.query_display.text() and self.ref_display.text() and
#             self.output_dir_display.text()):
#             self.run_button.setEnabled(True)
#         else:
#             self.run_button.setEnabled(False)

#     def run_diamond(self):
#         query_file = self.query_display.text()
#         ref_file = self.ref_display.text()
#         output_dir = self.output_dir_display.text()
#         evalue = self.evalue_input.text()
#         identity = self.identity_input.text()
#         threads = self.threads_input.text()
#         mode = self.mode_combo.currentText()
#         align_type = self.align_type_combo.currentText()
#         output_file_name = self.output_file_input.text() or "homologous_pairs.xlsx"

#         if not all([query_file, ref_file, output_dir, evalue, identity, threads]):
#             QMessageBox.warning(self, "Input Error", "Please provide all necessary inputs.")
#             return

#         if not os.path.exists(query_file) or not os.path.exists(ref_file):
#             QMessageBox.critical(self, "Error", "Input file not found.")
#             return

#         if not os.path.exists(output_dir):
#             os.makedirs(output_dir)

#         # Use get_resource_path to locate diamond.exe
#         diamond_path = self.get_resource_path('tools/dimond/diamond.exe') if hasattr(sys, '_MEIPASS') else os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools', 'dimond', 'diamond.exe')
#         if not os.path.exists(diamond_path):
#             QMessageBox.critical(self, "Error", f"DIAMOND executable not found at: {diamond_path}")
#             return

#         log_file = os.path.join(output_dir, "Homologus_Pair_error.log")
#         with open(log_file, 'w'):
#             pass

#         # Show single start message
#         QMessageBox.information(self, "Analysis Started", "Homologus Pair Finder process is running...")

#         # Step 1: Create DIAMOND database
#         db_name = os.path.join(output_dir, "ref_db")
#         makedb_command = [
#             diamond_path, "makedb",
#             "--in", ref_file,
#             "-d", db_name
#         ]

#         self.worker = Worker(makedb_command, log_file)
#         self.worker.finished.connect(lambda: self.run_diamond_alignment(query_file, db_name, output_dir, evalue, identity, threads, mode, align_type, log_file, output_file_name))
#         self.worker.error.connect(lambda error: self.show_completion_message(f"Error: {error}"))
#         self.worker.start()

#     def run_diamond_alignment(self, query_file, db_name, output_dir, evalue, identity, threads, mode, align_type, log_file, output_file_name):
#         diamond_path = self.get_resource_path('tools/dimond/diamond.exe') if hasattr(sys, '_MEIPASS') else os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools', 'dimond', 'diamond.exe')

#         output_file = os.path.join(output_dir, "diamond_results.m8")
#         align_command = [
#             diamond_path, align_type,
#             "-d", db_name,
#             "-q", query_file,
#             "-o", output_file,
#             "-e", evalue,
#             "--min-score", str(float(identity) * 2),  # Approximate score for identity
#             "-p", threads,
#             "--" + mode,
#             "-f", "6",  # Tabular output
#             "qseqid", "sseqid", "pident", "length", "evalue", "bitscore"
#         ]

#         self.worker = Worker(align_command, log_file)
#         self.worker.finished.connect(lambda: self.process_results(output_file, output_dir, log_file, output_file_name))
#         self.worker.error.connect(lambda error: self.show_completion_message(f"Error: {error}"))
#         self.worker.start()

#     def process_results(self, output_file, output_dir, log_file, output_file_name):
#         try:
#             # Read DIAMOND tabular output
#             columns = ["QueryID", "RefID", "Identity", "Length", "Evalue", "BitScore"]
#             results = pd.read_csv(output_file, sep="\t", names=columns)

#             # Filter out self-alignments (where QueryID == RefID)
#             results = results[results["QueryID"] != results["RefID"]]

#             # Filter homologous pairs (e.g., identity > threshold)
#             identity_threshold = float(self.identity_input.text())
#             filtered_results = results[results["Identity"] >= identity_threshold]

#             # Save homologous pairs with user-specified or default file name
#             output_excel = os.path.join(output_dir, output_file_name)
#             with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
#                 filtered_results.to_excel(writer, sheet_name='Homologous Pairs', index=False)
#                 worksheet = writer.sheets['Homologous Pairs']
#                 worksheet.set_column(0, len(columns) - 1, 20)

#             self.show_completion_message(f"Success: Homologous pairs saved to {output_excel}")
#         except Exception as e:
#             with open(log_file, 'a') as log:
#                 log.write(f"Error processing results: {str(e)}\n")
#             self.show_completion_message(f"Error: Failed to process results. See {log_file} for details")

#     def show_completion_message(self, message):
#         """Display a single completion message (success or error)."""
#         QMessageBox.information(self, "Analysis Completed", message)

#     def get_resource_path(self, relative_path):
#         """Get the absolute path to a resource, handling PyInstaller bundling."""
#         if hasattr(sys, '_MEIPASS'):
#             return os.path.join(sys._MEIPASS, relative_path)
#         return os.path.join(os.path.abspath(os.path.dirname(__file__)), relative_path)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = DiamondHomology()
#     window.show()
#     sys.exit(app.exec())

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QTextEdit, QMessageBox, QGroupBox, QGridLayout,
    QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit, QCheckBox, QScrollArea,
    QHBoxLayout, QTabWidget
)
from PySide6.QtCore import QProcess, Qt
from PySide6.QtGui import QIcon, QFont

class DiamondApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genome Wide WorkBench")
        self.setGeometry(100, 100, 1000, 1000)

        # Header
        self.header_label = QLabel("Homologous Pair Finder")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setFont(QFont('Arial', 20, QFont.Bold))
        self.header_label.setStyleSheet("""
            QLabel {
                background-color: #2C3E50;
                color: white;
                padding: 20px;
                border-radius: 12px;
            }
        """)

        # Create main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.header_label)

        # Create tab widget
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Create BLASTP tab
        self.blastp_tab = QWidget()
        self.setup_blastp_tab()
        self.tabs.addTab(self.blastp_tab, "BLASTP")

        # Create makedb tab
        self.makedb_tab = QWidget()
        self.setup_makedb_tab()
        self.tabs.addTab(self.makedb_tab, "Make Database")

        # Apply stylesheet
        self.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                color: white;
                background-color: #2C3E50;
                border: none;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
            QGroupBox {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)

    def setup_blastp_tab(self):
        # Create scroll area for advanced options
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        self.blastp_layout = QVBoxLayout(content_widget)
        scroll.setWidget(content_widget)
        self.blastp_tab.setLayout(QVBoxLayout())
        self.blastp_tab.layout().addWidget(scroll)

        # Step 1: Select diamond.exe
        diamond_group = QGroupBox("Step 1: Select diamond.exe")
        diamond_layout = QHBoxLayout()
        self.diamond_path_label = QLabel("No file selected")
        self.diamond_path_label.setStyleSheet("color: #666; font-style: italic;")
        self.btn_diamond = QPushButton("Upload diamond.exe")
        self.btn_diamond.clicked.connect(self.load_diamond)
        diamond_layout.addWidget(self.btn_diamond)
        diamond_layout.addWidget(self.diamond_path_label)
        diamond_group.setLayout(diamond_layout)
        self.blastp_layout.addWidget(diamond_group)

        # Step 2: Select query
        query_group = QGroupBox("Step 2: Select Query FASTA")
        query_layout = QHBoxLayout()
        self.query_path_label = QLabel("No file selected")
        self.query_path_label.setStyleSheet("color: #666; font-style: italic;")
        self.btn_query = QPushButton("Select Query")
        self.btn_query.clicked.connect(self.load_query)
        self.btn_query.setEnabled(False)
        query_layout.addWidget(self.btn_query)
        query_layout.addWidget(self.query_path_label)
        query_group.setLayout(query_layout)
        self.blastp_layout.addWidget(query_group)

        # Step 3: Select database
        db_group = QGroupBox("Step 3: Select DIAMOND Database")
        db_layout = QHBoxLayout()
        self.db_path_label = QLabel("No file selected")
        self.db_path_label.setStyleSheet("color: #666; font-style: italic;")
        self.btn_db = QPushButton("Select Database")
        self.btn_db.clicked.connect(self.load_db)
        self.btn_db.setEnabled(False)
        db_layout.addWidget(self.btn_db)
        db_layout.addWidget(self.db_path_label)
        db_group.setLayout(db_layout)
        self.blastp_layout.addWidget(db_group)

        # Step 4: Output options
        output_group = QGroupBox("Output Options")
        output_layout = QGridLayout()
        
        self.output_label = QLabel("Output File:")
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("diamond_results.txt")
        self.btn_output = QPushButton("Browse...")
        self.btn_output.clicked.connect(self.select_output_file)
        
        output_layout.addWidget(self.output_label, 0, 0)
        output_layout.addWidget(self.output_edit, 0, 1)
        output_layout.addWidget(self.btn_output, 0, 2)
        
        self.format_label = QLabel("Output Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems([
            "6: BLAST tabular",
            "0: BLAST pairwise",
            "5: BLAST XML",
            "100: DAA",
            "101: SAM",
            "102: Taxonomic classification",
            "103: PAF",
            "104: JSON"
        ])
        
        self.header_label = QLabel("Header for Tabular Output:")
        self.header_combo = QComboBox()
        self.header_combo.addItems(["None", "Simple", "Verbose"])
        self.header_combo.setEnabled(self.format_combo.currentText().startswith("6"))
        
        output_layout.addWidget(self.format_label, 1, 0)
        output_layout.addWidget(self.format_combo, 1, 1, 1, 2)
        output_layout.addWidget(self.header_label, 2, 0)
        output_layout.addWidget(self.header_combo, 2, 1, 1, 2)
        
        output_group.setLayout(output_layout)
        self.blastp_layout.addWidget(output_group)

        # Advanced Options Group
        self.advanced_group = QGroupBox("Advanced Options")
        self.advanced_group.setCheckable(True)
        self.advanced_group.setChecked(False)
        advanced_layout = QGridLayout()

        # Performance Options
        self.threads_label = QLabel("Threads:")
        self.threads_spin = QSpinBox()
        self.threads_spin.setRange(1, 128)
        self.threads_spin.setValue(max(1, os.cpu_count() // 2))
        advanced_layout.addWidget(self.threads_label, 0, 0)
        advanced_layout.addWidget(self.threads_spin, 0, 1)

        # Sensitivity Options
        self.sensitivity_label = QLabel("Sensitivity:")
        self.sensitivity_combo = QComboBox()
        self.sensitivity_combo.addItems([
            "Default", "Faster", "Fast", "Mid-sensitive", "Sensitive",
            "More-sensitive", "Very-sensitive", "Ultra-sensitive"
        ])
        advanced_layout.addWidget(self.sensitivity_label, 1, 0)
        advanced_layout.addWidget(self.sensitivity_combo, 1, 1)

        # Filtering Options
        self.evalue_label = QLabel("E-value:")
        self.evalue_spin = QDoubleSpinBox()
        self.evalue_spin.setRange(0, 1000)
        self.evalue_spin.setDecimals(10)
        self.evalue_spin.setValue(0.00001)
        advanced_layout.addWidget(self.evalue_label, 2, 0)
        advanced_layout.addWidget(self.evalue_spin, 2, 1)

        self.max_target_label = QLabel("Max Target Seqs:")
        self.max_target_spin = QSpinBox()
        self.max_target_spin.setRange(1, 1000000)
        self.max_target_spin.setValue(25)
        advanced_layout.addWidget(self.max_target_label, 3, 0)
        advanced_layout.addWidget(self.max_target_spin, 3, 1)

        # Alignment Options
        self.id_label = QLabel("Min Identity (%):")
        self.id_spin = QSpinBox()
        self.id_spin.setRange(0, 100)
        self.id_spin.setSpecialValueText("Not set")
        advanced_layout.addWidget(self.id_label, 4, 0)
        advanced_layout.addWidget(self.id_spin, 4, 1)

        self.query_cover_label = QLabel("Min Query Cover (%):")
        self.query_cover_spin = QSpinBox()
        self.query_cover_spin.setRange(0, 100)
        self.query_cover_spin.setSpecialValueText("Not set")
        advanced_layout.addWidget(self.query_cover_label, 5, 0)
        advanced_layout.addWidget(self.query_cover_spin, 5, 1)

        # Redundant pairs option
        self.remove_redundant_check = QCheckBox("Remove Redundant Pairs (keep only canonical)")
        advanced_layout.addWidget(self.remove_redundant_check, 6, 0, 1, 2)

        # Matrix Options
        self.matrix_label = QLabel("Scoring Matrix:")
        self.matrix_combo = QComboBox()
        self.matrix_combo.addItems(["BLOSUM62", "BLOSUM50", "BLOSUM80", "PAM250", "PAM70"])
        advanced_layout.addWidget(self.matrix_label, 0, 2)
        advanced_layout.addWidget(self.matrix_combo, 0, 3)

        # Gap Penalties
        self.gapopen_label = QLabel("Gap Open Penalty:")
        self.gapopen_spin = QSpinBox()
        self.gapopen_spin.setRange(-100, 100)
        self.gapopen_spin.setValue(11)
        advanced_layout.addWidget(self.gapopen_label, 1, 2)
        advanced_layout.addWidget(self.gapopen_spin, 1, 3)

        self.gapextend_label = QLabel("Gap Extend Penalty:")
        self.gapextend_spin = QSpinBox()
        self.gapextend_spin.setRange(-100, 100)
        self.gapextend_spin.setValue(1)
        advanced_layout.addWidget(self.gapextend_label, 2, 2)
        advanced_layout.addWidget(self.gapextend_spin, 2, 3)

        # Masking Options
        self.masking_label = QLabel("Masking:")
        self.masking_combo = QComboBox()
        self.masking_combo.addItems(["tantan", "none", "seg"])
        advanced_layout.addWidget(self.masking_label, 3, 2)
        advanced_layout.addWidget(self.masking_combo, 3, 3)

        # Other Options
        self.comp_stats_label = QLabel("Comp-based Stats:")
        self.comp_stats_combo = QComboBox()
        self.comp_stats_combo.addItems(["0", "1", "2", "3", "4"])
        advanced_layout.addWidget(self.comp_stats_label, 4, 2)
        advanced_layout.addWidget(self.comp_stats_combo, 4, 3)

        self.no_self_hits_check = QCheckBox("No Self Hits")
        advanced_layout.addWidget(self.no_self_hits_check, 5, 2, 1, 2)

        self.advanced_group.setLayout(advanced_layout)
        self.blastp_layout.addWidget(self.advanced_group)

        # Run Button
        self.btn_run = QPushButton("Run BLASTP")
        self.btn_run.clicked.connect(self.run_blastp)
        self.btn_run.setEnabled(False)
        self.blastp_layout.addWidget(self.btn_run)

        # Output Console
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.blastp_layout.addWidget(self.output)

        # QProcess setup
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.read_stdout)
        self.process.readyReadStandardError.connect(self.read_stderr)
        self.process.finished.connect(self.process_finished)

    def setup_makedb_tab(self):
        # Create scroll area for makedb options
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        self.makedb_layout = QVBoxLayout(content_widget)
        scroll.setWidget(content_widget)
        self.makedb_tab.setLayout(QVBoxLayout())
        self.makedb_tab.layout().addWidget(scroll)

        # Step 1: Select diamond.exe
        makedb_diamond_group = QGroupBox("Step 1: Select diamond.exe")
        makedb_diamond_layout = QHBoxLayout()
        self.makedb_diamond_path_label = QLabel("No file selected")
        self.makedb_diamond_path_label.setStyleSheet("color: #666; font-style: italic;")
        self.makedb_btn_diamond = QPushButton("Upload diamond.exe")
        self.makedb_btn_diamond.clicked.connect(self.makedb_load_diamond)
        makedb_diamond_layout.addWidget(self.makedb_btn_diamond)
        makedb_diamond_layout.addWidget(self.makedb_diamond_path_label)
        makedb_diamond_group.setLayout(makedb_diamond_layout)
        self.makedb_layout.addWidget(makedb_diamond_group)

        # Step 2: Select input FASTA
        input_group = QGroupBox("Step 2: Select Input FASTA")
        input_layout = QHBoxLayout()
        self.makedb_input_label = QLabel("No file selected")
        self.makedb_input_label.setStyleSheet("color: #666; font-style: italic;")
        self.makedb_btn_input = QPushButton("Select Input FASTA")
        self.makedb_btn_input.clicked.connect(self.makedb_load_input)
        self.makedb_btn_input.setEnabled(False)
        input_layout.addWidget(self.makedb_btn_input)
        input_layout.addWidget(self.makedb_input_label)
        input_group.setLayout(input_layout)
        self.makedb_layout.addWidget(input_group)

        # Step 3: Output options
        makedb_output_group = QGroupBox("Output Options")
        makedb_output_layout = QGridLayout()
        
        self.makedb_output_label = QLabel("Database Name:")
        self.makedb_output_edit = QLineEdit()
        self.makedb_output_edit.setPlaceholderText("database.dmnd")
        self.makedb_btn_output = QPushButton("Browse...")
        self.makedb_btn_output.clicked.connect(self.makedb_select_output_file)
        
        makedb_output_layout.addWidget(self.makedb_output_label, 0, 0)
        makedb_output_layout.addWidget(self.makedb_output_edit, 0, 1)
        makedb_output_layout.addWidget(self.makedb_btn_output, 0, 2)
        
        makedb_output_group.setLayout(makedb_output_layout)
        self.makedb_layout.addWidget(makedb_output_group)

        # Advanced Options Group
        self.makedb_advanced_group = QGroupBox("Advanced Options")
        self.makedb_advanced_group.setCheckable(True)
        self.makedb_advanced_group.setChecked(False)
        makedb_advanced_layout = QGridLayout()

        # Threads
        self.makedb_threads_label = QLabel("Threads:")
        self.makedb_threads_spin = QSpinBox()
        self.makedb_threads_spin.setRange(1, 128)
        self.makedb_threads_spin.setValue(max(1, os.cpu_count() // 2))
        makedb_advanced_layout.addWidget(self.makedb_threads_label, 0, 0)
        makedb_advanced_layout.addWidget(self.makedb_threads_spin, 0, 1)

        self.makedb_advanced_group.setLayout(makedb_advanced_layout)
        self.makedb_layout.addWidget(self.makedb_advanced_group)

        # Run Button
        self.makedb_btn_run = QPushButton("Create Database")
        self.makedb_btn_run.clicked.connect(self.run_makedb)
        self.makedb_btn_run.setEnabled(False)
        self.makedb_layout.addWidget(self.makedb_btn_run)

        # Output Console
        self.makedb_output = QTextEdit()
        self.makedb_output.setReadOnly(True)
        self.makedb_layout.addWidget(self.makedb_output)

        # QProcess setup
        self.makedb_process = QProcess()
        self.makedb_process.readyReadStandardOutput.connect(self.makedb_read_stdout)
        self.makedb_process.readyReadStandardError.connect(self.makedb_read_stderr)
        self.makedb_process.finished.connect(self.makedb_process_finished)

    def update_header_option(self):
        # Enable header option only for tabular format (6)
        is_tabular = self.format_combo.currentText().startswith("6")
        self.header_combo.setEnabled(is_tabular)
        self.header_label.setEnabled(is_tabular)

    def load_diamond(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select diamond.exe", "", "Executable (*.exe)")
        if path:
            self.diamond_path = path
            self.diamond_path_label.setText(os.path.basename(path))
            self.diamond_path_label.setStyleSheet("color: black; font-style: normal;")
            self.btn_query.setEnabled(True)
            # Also set for makedb tab if not already set
            if not self.makedb_diamond_path_label.text() or self.makedb_diamond_path_label.text() == "No file selected":
                self.makedb_diamond_path_label.setText(os.path.basename(path))
                self.makedb_diamond_path_label.setStyleSheet("color: black; font-style: normal;")
                self.makedb_btn_input.setEnabled(True)

    def makedb_load_diamond(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select diamond.exe", "", "Executable (*.exe)")
        if path:
            self.diamond_path = path  # Share the same diamond path
            self.makedb_diamond_path_label.setText(os.path.basename(path))
            self.makedb_diamond_path_label.setStyleSheet("color: black; font-style: normal;")
            self.makedb_btn_input.setEnabled(True)
            # Also set for blastp tab if not already set
            if not self.diamond_path_label.text() or self.diamond_path_label.text() == "No file selected":
                self.diamond_path_label.setText(os.path.basename(path))
                self.diamond_path_label.setStyleSheet("color: black; font-style: normal;")
                self.btn_query.setEnabled(True)

    def load_query(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Query FASTA", "", "FASTA Files (*.fasta *.fa *.faa)")
        if path:
            self.query_path = path
            self.query_path_label.setText(os.path.basename(path))
            self.query_path_label.setStyleSheet("color: black; font-style: normal;")
            self.btn_db.setEnabled(True)
            # Suggest output filename based on query
            base_name = os.path.splitext(os.path.basename(path))[0]
            self.output_edit.setText(f"{base_name}_diamond_results.txt")

    def makedb_load_input(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Input FASTA", "", "FASTA Files (*.fasta *.fa *.faa)")
        if path:
            self.makedb_input_path = path
            self.makedb_input_label.setText(os.path.basename(path))
            self.makedb_input_label.setStyleSheet("color: black; font-style: normal;")
            self.makedb_btn_run.setEnabled(True)
            # Suggest output filename based on input
            base_name = os.path.splitext(os.path.basename(path))[0]
            self.makedb_output_edit.setText(f"{base_name}.dmnd")

    def load_db(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select DIAMOND DB", "", "DIAMOND DB (*.dmnd)")
        if path:
            self.db_path = path
            self.db_path_label.setText(os.path.basename(path))
            self.db_path_label.setStyleSheet("color: black; font-style: normal;")
            self.btn_run.setEnabled(True)

    def select_output_file(self):
        default_name = self.output_edit.text() or "diamond_results.txt"
        path, _ = QFileDialog.getSaveFileName(self, "Save Output File", default_name, "All Files (*)")
        if path:
            self.output_edit.setText(path)

    def makedb_select_output_file(self):
        default_name = self.makedb_output_edit.text() or "database.dmnd"
        path, _ = QFileDialog.getSaveFileName(self, "Save Database File", default_name, "DIAMOND DB (*.dmnd)")
        if path:
            self.makedb_output_edit.setText(path)

    def run_blastp(self):
        if not all([self.diamond_path, self.query_path, self.db_path]):
            QMessageBox.warning(self, "Missing input", "Please load all required files.")
            return
            
        output_path = self.output_edit.text().strip()
        if not output_path:
            QMessageBox.warning(self, "Output Error", "Please specify an output file.")
            return
            
        self.output_path = output_path
        self.output.clear()
        self.output.append("Starting DIAMOND BLASTP analysis...\n")
        self.output.append(f"DIAMOND path: {self.diamond_path}")
        self.output.append(f"Query file: {self.query_path}")
        self.output.append(f"Database file: {self.db_path}")
        self.output.append(f"Output file: {self.output_path}\n")

        # Build command arguments
        args = ["blastp"]
        
        # Required parameters
        args.extend(["-d", self.db_path])
        args.extend(["-q", self.query_path])
        args.extend(["-o", self.output_path])
        
        # Output format
        fmt = self.format_combo.currentText().split(":")[0].strip()
        args.extend(["--outfmt", fmt])
        
        # Header option (only for tabular format)
        if fmt == "6" and self.header_combo.currentText() != "None":
            header_map = {"Simple": "simple", "Verbose": "verbose"}
            args.extend(["--header", header_map[self.header_combo.currentText()]])
        
        # Performance
        args.extend(["--threads", str(self.threads_spin.value())])
        
        # Sensitivity
        sensitivity_map = {
            "Faster": "--faster",
            "Fast": "--fast",
            "Mid-sensitive": "--mid-sensitive",
            "Sensitive": "--sensitive",
            "More-sensitive": "--more-sensitive",
            "Very-sensitive": "--very-sensitive",
            "Ultra-sensitive": "--ultra-sensitive"
        }
        sens = self.sensitivity_combo.currentText()
        if sens != "Default":
            args.append(sensitivity_map[sens])
        
        # Filtering
        args.extend(["--evalue", str(self.evalue_spin.value())])
        args.extend(["--max-target-seqs", str(self.max_target_spin.value())])
        
        if self.id_spin.value() > 0:
            args.extend(["--id", str(self.id_spin.value())])
        if self.query_cover_spin.value() > 0:
            args.extend(["--query-cover", str(self.query_cover_spin.value())])
        
        # Alignment options
        args.extend(["--matrix", self.matrix_combo.currentText()])
        args.extend(["--gapopen", str(self.gapopen_spin.value())])
        args.extend(["--gapextend", str(self.gapextend_spin.value())])
        
        # Advanced options
        args.extend(["--masking", self.masking_combo.currentText()])
        args.extend(["--comp-based-stats", self.comp_stats_combo.currentText()])
        
        if self.no_self_hits_check.isChecked():
            args.append("--no-self-hits")

        # Show command for debugging
        cmd = f"{self.diamond_path} {' '.join(args)}"
        self.output.append(f"Executing command:\n{cmd}\n")
        
        # Run the process
        self.process.start(self.diamond_path, args)

    def run_makedb(self):
        if not all([self.diamond_path, hasattr(self, 'makedb_input_path')]):
            QMessageBox.warning(self, "Missing input", "Please load all required files.")
            return
            
        output_path = self.makedb_output_edit.text().strip()
        if not output_path:
            QMessageBox.warning(self, "Output Error", "Please specify an output database name.")
            return
            
        self.makedb_output_path = output_path
        self.makedb_output.clear()
        self.makedb_output.append("Starting DIAMOND makedb...\n")
        self.makedb_output.append(f"DIAMOND path: {self.diamond_path}")
        self.makedb_output.append(f"Input file: {self.makedb_input_path}")
        self.makedb_output.append(f"Output database: {self.makedb_output_path}\n")

        # Build command arguments
        args = ["makedb"]
        
        # Required parameters
        args.extend(["--in", self.makedb_input_path])
        args.extend(["--db", self.makedb_output_path])
        
        # Performance options
        args.extend(["--threads", str(self.makedb_threads_spin.value())])

        # Show command for debugging
        cmd = f"{self.diamond_path} {' '.join(args)}"
        self.makedb_output.append(f"Executing command:\n{cmd}\n")
        
        # Run the process
        self.makedb_process.start(self.diamond_path, args)

    def read_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.output.append(data)

    def read_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.output.append(f"<font color='red'>{data}</font>")

    def process_finished(self):
        exit_code = self.process.exitCode()
        if exit_code == 0:
            self.output.append("\n✅ DIAMOND finished successfully!")
            
            # If tabular output and remove redundant pairs is checked
            if (self.format_combo.currentText().startswith("6") and 
                hasattr(self, 'remove_redundant_check') and 
                self.remove_redundant_check.isChecked()):
                
                try:
                    # Read the output file and filter redundant pairs
                    with open(self.output_path, 'r') as f:
                        lines = f.readlines()
                    
                    # Process pairs to keep only canonical ones (a < b)
                    seen_pairs = set()
                    filtered_lines = []
                    
                    for line in lines:
                        if not line.strip():
                            continue
                        parts = line.split('\t')
                        if len(parts) >= 2:
                            qseqid, sseqid = parts[0], parts[1]
                            # Create canonical pair (sorted)
                            pair = tuple(sorted((qseqid, sseqid)))
                            if pair not in seen_pairs:
                                seen_pairs.add(pair)
                                filtered_lines.append(line)
                    
                    # Write filtered results back to file
                    with open(self.output_path, 'w') as f:
                        f.writelines(filtered_lines)
                        
                    self.output.append(f"\nFiltered {len(lines)-len(filtered_lines)} redundant pairs")
                    self.output.append(f"Kept {len(filtered_lines)} unique pairs")
                    
                except Exception as e:
                    self.output.append(f"\n⚠️ Error filtering redundant pairs: {str(e)}")
            
            # Show column headers if tabular output was selected
            if self.format_combo.currentText().startswith("6"):
                self.output.append("\nOutput Format: Tabular (columns explained below)")
                self.output.append("1. qseqid: Query sequence ID")
                self.output.append("2. sseqid: Subject sequence ID")
                self.output.append("3. pident: Percentage of identical matches")
                self.output.append("4. length: Alignment length")
                self.output.append("5. mismatch: Number of mismatches")
                self.output.append("6. gapopen: Number of gap openings")
                self.output.append("7. qstart: Start of alignment in query")
                self.output.append("8. qend: End of alignment in query")
                self.output.append("9. sstart: Start of alignment in subject")
                self.output.append("10. send: End of alignment in subject")
                self.output.append("11. evalue: Expect value")
                self.output.append("12. bitscore: Bit score")
            
            self.output.append(f"\nResults saved to: {self.output_path}")
            QMessageBox.information(self, "BLASTP Complete", 
                                   f"Results saved to:\n{self.output_path}")
        else:
            self.output.append(f"\n❌ DIAMOND failed with exit code {exit_code}")
            QMessageBox.critical(self, "Execution Failed", 
                                "DIAMOND encountered an error. Check output for details.")

    def makedb_read_stdout(self):
        data = self.makedb_process.readAllStandardOutput().data().decode()
        self.makedb_output.append(data)

    def makedb_read_stderr(self):
        data = self.makedb_process.readAllStandardError().data().decode()
        self.makedb_output.append(f"<font color='red'>{data}</font>")

    def makedb_process_finished(self):
        exit_code = self.makedb_process.exitCode()
        if exit_code == 0:
            self.makedb_output.append("\n✅ DIAMOND database created successfully!")
            self.makedb_output.append(f"\nDatabase saved to: {self.makedb_output_path}")
            QMessageBox.information(self, "Database Creation Complete", 
                                   f"Database saved to:\n{self.makedb_output_path}")
            
            # Update the BLASTP tab with the new database if it's in the same directory
            if hasattr(self, 'db_path_label'):
                self.db_path_label.setText(os.path.basename(self.makedb_output_path))
                self.db_path_label.setStyleSheet("color: black; font-style: normal;")
                self.db_path = self.makedb_output_path
                self.btn_run.setEnabled(True)
        else:
            self.makedb_output.append(f"\n❌ DIAMOND makedb failed with exit code {exit_code}")
            QMessageBox.critical(self, "Execution Failed", 
                                "DIAMOND encountered an error. Check output for details.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiamondApp()
    window.show()
    sys.exit(app.exec())