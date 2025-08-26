# import sys
# import pandas as pd
# import logging
# import os
# import shutil
# import subprocess
# from PySide6.QtWidgets import (
#     QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget,
#     QLabel, QLineEdit, QFormLayout, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QComboBox
# )
# from PySide6.QtGui import QIcon, QFont
# from PySide6.QtCore import QSize, QPropertyAnimation, QEasingCurve, Qt
# from PySide6.QtCore import QThread, Signal  

# class Worker(QThread):
#     finished = Signal()
#     error = Signal(str)

#     def __init__(self, command, log_file):
#         super().__init__()
#         self.command = command
#         self.log_file = log_file
#         self.process = None
#         self.stop_requested = False

#     def run(self):
#         try:
#             self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#             self.process.wait()
#             if self.stop_requested:
#                 self.error.emit("Process stopped by user")
#                 return
#             result = self.process
#             if result.returncode != 0:
#                 with open(self.log_file, 'a') as log:
#                     log.write("=== BLAST Command ===\n")
#                     log.write("\n=== BLAST Command Error Output ===\n")
#                     log.write(result.stderr if result.stderr else 'No errors.\n')
#                 self.error.emit(result.stderr)
#         except Exception as e:
#             with open(self.log_file, 'a') as log:
#                 log.write(f"\nException occurred: {str(e)}\n")
#             self.error.emit(str(e))

#     def stop(self):
#         self.stop_requested = True
#         if self.process:
#             self.process.terminate()

# class Blast(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Genome Wide WorkBench")
#         self.setWindowIcon(QIcon('src/image.png'))
#         self.resizeToHalfScreen()
#         self.is_dark_theme = False

#         self.header_label = QLabel("BlastXPlorer")
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

#         self.load_button = QPushButton("Load FASTA File")
#         self.load_button.setIcon(QIcon('upload_icon.png'))
#         self.load_button.setIconSize(QSize(16, 16))
#         self.load_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
#         self.load_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 16px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 text-align: left;
#                 padding: 5px 10px;
#             }
#             QPushButton:hover {
#                 background-color: #34495E;
#             }
#             QPushButton:pressed {
#                 background-color: #34495E;
#             }
#         """)
#         self.load_button.clicked.connect(self.load_file)

#         self.query_button = QPushButton("Load Query File")
#         self.query_button.setIcon(QIcon('upload_icon.png'))
#         self.query_button.setIconSize(QSize(16, 16))
#         self.query_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
#         self.query_button.setFixedSize(200, 40)
#         self.query_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 16px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 text-align: left;
#                 padding: 5px 10px;
#             }
#             QPushButton:hover {
#                 background-color: #34495E;
#             }
#             QPushButton:pressed {
#                 background-color: #34495E;
#             }
#         """)
#         self.query_button.clicked.connect(self.load_query_file)

#         self.choose_dir_button = QPushButton("Choose Output Directory")
#         self.choose_dir_button.setIcon(QIcon('folder_icon.png'))
#         self.choose_dir_button.setIconSize(QSize(16, 16))
#         self.choose_dir_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
#         self.choose_dir_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 16px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 text-align: left;
#                 padding: 10px 20px;
#             }
#             QPushButton:hover {
#                 background-color: #34495E;
#             }
#             QPushButton:pressed {
#                 background-color: #34495E;
#             }
#         """)
#         self.choose_dir_button.clicked.connect(self.choose_directory)

#         self.file_name_display = QLineEdit(self)
#         self.file_name_display.setReadOnly(True)
#         self.file_name_display.setPlaceholderText("No file chosen")
#         self.file_name_display.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.query_file_display = QLineEdit(self)
#         self.query_file_display.setReadOnly(True)
#         self.query_file_display.setPlaceholderText("No query file chosen")
#         self.query_file_display.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.output_dir_display = QLineEdit(self)
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

#         self.download_file_name_input = QLineEdit(self)
#         self.download_file_name_input.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.file_name_input = QLineEdit()
#         self.file_name_input.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.evalue_input = QLineEdit("0.00001")
#         self.evalue_input.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.word_size_input = QLineEdit("11")
#         self.word_size_input.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.num_threads_input = QLineEdit("1")
#         self.num_threads_input.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.db_type_combo = QComboBox()
#         self.db_type_combo.addItems(["Nucleotide", "Protein"])
#         self.db_type_combo.setStyleSheet("""
#             QComboBox {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)

#         self.blast_type_combo = QComboBox()
#         self.blast_type_combo.addItems(["blastn", "blastp", "blastx", "tblastx", "tblastn"])
#         self.blast_type_combo.setStyleSheet("""
#             QComboBox {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)
#         self.blast_type_combo.currentIndexChanged.connect(self.update_word_size)
#         self.blast_type_combo.currentIndexChanged.connect(self.update_matrix_combo)

#         self.matrix_combo = QComboBox()
#         self.matrix_combo.addItems(["BLOSUM80", "BLOSUM62", "BLOSUM50", "BLOSUM45", "PAM250", "BLOSUM90", "PAM30", "PAM70", "IDENTITY"])
#         self.matrix_combo.setCurrentText("BLOSUM62")
#         self.matrix_combo.setStyleSheet("""
#             QComboBox {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 12px;
#                 border-radius: 4px;
#             }
#         """)
#         self.matrix_combo.setEnabled(False)

#         self.make_db_button = QPushButton("Make BLAST DB")
#         self.make_db_button.setFixedSize(200, 50)
#         self.make_db_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 16px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 text-align: left;
#                 padding: 10px 20px;
#             }
#             QPushButton:hover {
#                 background-color: #34495E;
#             }
#             QPushButton:pressed {
#                 background-color: #34495E;
#             }
#         """)
#         self.make_db_button.setEnabled(False)
#         self.make_db_button.clicked.connect(self.make_db)

#         self.run_blast_button = QPushButton("Run BLAST")
#         self.run_blast_button.setFixedSize(200, 50)
#         self.run_blast_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 16px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 text-align: left;
#                 padding: 10px 20px;
#             }
#             QPushButton:hover {
#                 background-color: #34495E;
#             }
#             QPushButton:pressed {
#                 background-color: #34495E;
#             }
#         """)
#         self.run_blast_button.setEnabled(False)
#         self.run_blast_button.clicked.connect(self.blast_nucleotide)

#         self.stop_button = QPushButton("Stop")
#         self.stop_button.setFixedSize(200, 50)
#         self.stop_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 16px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 text-align: center;
#                 padding: 10px 20px;
#             }
#             QPushButton:disabled {
#                 background-color: #A0A0A0;
#             }
#             QPushButton:hover {
#                 background-color: #34495E;
#             }
#             QPushButton:pressed {
#                 background-color: #34495E;
#             }
#         """)
#         self.stop_button.setEnabled(False)
#         self.stop_button.clicked.connect(self.stop_process)

#         self.animation = QPropertyAnimation(self.make_db_button, b"size")
#         self.animation.setDuration(300)
#         self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)

#         self.theme_toggle_button = QPushButton("Switch to Dark Mode")
#         self.theme_toggle_button.setFixedSize(150, 30)
#         self.theme_toggle_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 16px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 text-align: left;
#                 padding: 10px 20px;
#             }
#             QPushButton:hover {
#                 background-color: #34495E;
#             }
#             QPushButton:pressed {
#                 background-color: #34495E;
#             }
#         """)

#         main_layout = QVBoxLayout()
#         main_layout.addWidget(self.header_label)
        
#         file_form_layout = QFormLayout()
#         load_layout = QHBoxLayout()
#         load_layout.addWidget(self.load_button)
#         load_layout.addWidget(self.file_name_display)
#         file_form_layout.addRow(QLabel("Upload the FASTA file for DB creation:"), load_layout)
        
#         query_layout = QHBoxLayout()
#         query_layout.addWidget(self.query_button)
#         query_layout.addWidget(self.query_file_display)
#         file_form_layout.addRow(QLabel("Upload the Query file for BLAST:"), query_layout)
        
#         dir_layout = QHBoxLayout()
#         dir_layout.addWidget(self.choose_dir_button)
#         dir_layout.addWidget(self.output_dir_display)
#         file_form_layout.addRow(QLabel("Choose Output Directory for Results:"), dir_layout)
#         file_form_layout.addRow(QLabel("Database Type:"), self.db_type_combo)
#         file_form_layout.addRow(QLabel("BLAST Type:"), self.blast_type_combo)
#         file_form_layout.addRow(QLabel("Matrix (for BLASTP):"), self.matrix_combo)
#         file_form_layout.addRow(QLabel("Provide Name for creation of DB files:"), self.file_name_input)
#         file_form_layout.addRow(QLabel("E-value:"), self.evalue_input)
#         file_form_layout.addRow(QLabel("Word Size:"), self.word_size_input)
#         file_form_layout.addRow(QLabel("Number of Threads:"), self.num_threads_input)
#         file_form_layout.addRow(QLabel("Result File Name (Optional):"), self.download_file_name_input)
#         main_layout.addLayout(file_form_layout)

#         button_layout = QHBoxLayout()
#         button_layout.addWidget(self.make_db_button, alignment=Qt.AlignmentFlag.AlignLeft)
#         button_layout.addWidget(self.run_blast_button, alignment=Qt.AlignmentFlag.AlignLeft)
#         button_layout.addWidget(self.stop_button, alignment=Qt.AlignmentFlag.AlignLeft)
    
#         main_layout.addLayout(button_layout)
#         container = QWidget()
#         container.setLayout(main_layout)
#         self.setCentralWidget(container)

#     def resizeToHalfScreen(self):
#         screen = QApplication.primaryScreen().geometry()
#         self.setGeometry(screen.width() // 4, screen.height() // 4, screen.width() // 2, screen.height() // 2)

#     def load_file(self):
#         file_name, _ = QFileDialog.getOpenFileName(self, "Open FASTA File", "", "FASTA Files (*.fasta *.fa *.fna *.ffn *.faa *.frn)")
#         if file_name:
#             self.file_name_display.setText(file_name)
#             self.make_db_button.setEnabled(True)
    
#     def load_query_file(self):
#         file_name, _ = QFileDialog.getOpenFileName(self, "Open Query File", "", "FASTA Files (*.fasta *.fa *.fna *.ffn *.faa *.frn)")
#         if file_name:
#             self.query_file_display.setText(file_name)
#             self.run_blast_button.setEnabled(True)

#     def choose_directory(self):
#         directory = QFileDialog.getExistingDirectory(self, "Choose Output Directory")
#         if directory:
#             self.output_dir_display.setText(directory)

#     def make_db(self):
#         fasta_file = self.file_name_display.text()
#         db_type = self.db_type_combo.currentText().lower()
#         db_type = 'nucl' if db_type == 'nucleotide' else 'prot'
#         db_name = self.file_name_input.text()
#         output_dir = self.output_dir_display.text()

#         if not fasta_file or not db_name or not output_dir:
#             QMessageBox.warning(self, "Input Error", "Please provide all necessary inputs.")
#             return

#         if hasattr(sys, '_MEIPASS'):
#             blast_dir = os.path.join(sys._MEIPASS, 'tools', 'blast')
#         else:
#             base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#             blast_dir = os.path.join(base_dir, 'tools', 'blast')

#         makeblastdb_path = os.path.join(blast_dir, 'makeblastdb.exe')
#         if not os.path.exists(makeblastdb_path):
#             QMessageBox.critical(self, "Error", f"makeblastdb tool not found at: {makeblastdb_path}")
#             return

#         if not os.path.exists(fasta_file):
#             QMessageBox.critical(self, "Error", "FASTA file not found.")
#             return

#         if not os.path.exists(output_dir):
#             os.makedirs(output_dir)

#         log_file = os.path.join(output_dir, "blast_errors.log")
#         with open(log_file, 'w'):
#             pass    

#         QMessageBox.information(self, "Analysis Started", "Your analysis is running.")
#         self.make_db_button.setEnabled(False)
#         self.stop_button.setEnabled(True)

#         makeblastdb_command = [
#             makeblastdb_path,
#             '-in', fasta_file,
#             '-dbtype', db_type,
#             '-out', os.path.join(output_dir, db_name)
#         ]

#         self.worker = Worker(makeblastdb_command, log_file)
#         self.worker.finished.connect(lambda: self.handle_makeblastdb_completion(log_file))
#         self.worker.error.connect(lambda error: self.handle_error(error, log_file))
#         self.worker.start()

#     def handle_makeblastdb_completion(self, log_file):
#         self.make_db_button.setEnabled(True)
#         self.stop_button.setEnabled(False)
#         try:
#             with open(log_file, 'r') as f:
#                 error_content = f.read().strip()
#             if error_content:
#                 raise ValueError("BLAST database creation failed. Check the log for details.")
#             QMessageBox.information(self, "Success", "BLAST database created successfully.")
#         except Exception as e:
#             logging.error(f"Error during BLAST database creation: {str(e)}")
#             QMessageBox.critical(self, "Error", f"BLAST database creation failed, see 'blast_errors.log' in the directory: {log_file}")

#     def handle_error(self, error, log_file):
#         self.make_db_button.setEnabled(True)
#         self.run_blast_button.setEnabled(True)
#         self.stop_button.setEnabled(False)
#         logging.error(f"Operation failed. Error: {error}")
#         with open(log_file, 'a') as log:
#             log.write(f"Error: {error}\n")
#         QMessageBox.critical(self, "Error", f"Operation failed. Check {log_file} for details.")

#     def update_word_size(self):
#         blast_type = self.blast_type_combo.currentText()
#         if blast_type in ["blastp", "tblastn", "blastx", "tblastx"]:
#             self.word_size_input.setText("3")
#         else:
#             self.word_size_input.setText("11")

#     def blast_nucleotide(self):
#         query_file = self.query_file_display.text()
#         db_name = self.file_name_input.text()
#         output_dir = self.output_dir_display.text()
#         evalue = self.evalue_input.text()
#         word_size = self.word_size_input.text()
#         num_threads = self.num_threads_input.text()
#         blast_type = self.blast_type_combo.currentText()
#         matrix = self.matrix_combo.currentText()

#         if blast_type in ["blastp"] and self.db_type_combo.currentText() == "Nucleotide":
#             QMessageBox.warning(self, "Input Error", "You must choose a Protein database for blastp.")
#             return
#         elif blast_type in ["blastn"] and self.db_type_combo.currentText() == "Protein":
#             QMessageBox.warning(self, "Input Error", "You must choose a Nucleotide database for blastn.")
#             return
#         elif blast_type in ["blastx"] and self.db_type_combo.currentText() == "Nucleotide":
#             QMessageBox.warning(self, "Input Error", "You must choose a Protein database for blastx.")
#             return
#         elif blast_type in ["tblastn"] and self.db_type_combo.currentText() == "Protein":
#             QMessageBox.warning(self, "Input Error", "You must choose a Nucleotide database for tblastn.")
#             return
#         elif blast_type in ["tblastx"] and self.db_type_combo.currentText() == "Protein":
#             QMessageBox.warning(self, "Input Error", "You must choose a Nucleotide database for tblastx.")
#             return

#         if blast_type in ["tblastn", "blastp", "blastx"] and int(word_size) >= 8:
#             QMessageBox.warning(self, "Input Error", "Word size must be less than 8 for tblastn, blastp, or blastx.")
#             return
#         elif blast_type in ["tblastx"] and int(word_size) >= 6:
#             QMessageBox.warning(self, "Input Error", "Word size must be less than 6 for tblastx.")
#             return
#         elif blast_type in ["blastn"] and int(word_size) < 4:
#             QMessageBox.warning(self, "Input Error", "Word size must be more than 4 for blastn.")
#             return

#         if not query_file or not db_name or not output_dir or not evalue or not word_size or not num_threads:
#             QMessageBox.warning(self, "Input Error", "Please provide all necessary inputs.")
#             return

#         QMessageBox.information(self, "Analysis Started", "Your analysis is running.")
#         self.run_blast_button.setEnabled(False)
#         self.stop_button.setEnabled(True)

#         db_path = os.path.join(output_dir, db_name)
#         output_file_name = self.download_file_name_input.text()
#         output_file = os.path.join(output_dir, f"{output_file_name}.txt")

#         log_file = os.path.join(output_dir, "blast_errors.log")
#         with open(log_file, 'w'):
#             pass

#         if hasattr(sys, '_MEIPASS'):
#             blast_dir = os.path.join(sys._MEIPASS, 'tools', 'blast')
#         else:
#             base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#             blast_dir = os.path.join(base_dir, 'tools', 'blast')

#         blast_command = [
#             os.path.join(blast_dir, blast_type),
#             '-query', query_file,
#             '-db', db_path,
#             '-evalue', evalue,
#             '-word_size', word_size,
#             '-num_threads', num_threads,
#             '-out', output_file,
#             '-outfmt', "6 qseqid sseqid qlen qstart qend length pident evalue bitscore nident gaps sstrand qcovhsp qseq sseq"
#         ]

#         if blast_type == "blastp":
#             blast_command.append('-matrix')
#             blast_command.append(matrix)

#         self.worker = Worker(blast_command, log_file)
#         self.worker.finished.connect(lambda: self.handle_blast_completion(output_file, log_file))
#         self.worker.error.connect(lambda error: self.handle_error(error, log_file))
#         self.worker.start()

#     def handle_blast_completion(self, output_file, log_file):
#         self.run_blast_button.setEnabled(True)
#         self.stop_button.setEnabled(False)
#         try:
#             if os.path.exists(log_file):
#                 with open(log_file, 'r') as f:
#                     error_content = f.read().strip()
#                 if error_content:
#                     raise ValueError("BLAST search failed with errors. Please check the log.")
#             self.process_blast_results(output_file)
#             QMessageBox.information(self, "Success", "BLAST search completed successfully.")
#         except Exception as e:
#             logging.error(f"Error during BLAST search: {str(e)}")
#             QMessageBox.critical(self, "Error", f"Failed to process BLAST results. See 'blast_errors.log' in the directory: {log_file}")

#     def on_blast_success(self, output_file):
#         self.run_blast_button.setEnabled(True)
#         self.stop_button.setEnabled(False)
#         try:
#             self.process_blast_results(output_file)
#             QMessageBox.information(self, "Success", "BLAST search completed successfully.")
#         except Exception as e:
#             logging.error(f"Error processing BLAST results: {str(e)}")
#             QMessageBox.critical(self, "Error", f"Failed to process BLAST results. Error: {str(e)}")

#     def process_blast_results(self, output_file):
#         columns = ["QuerySeq.ID", "SubjectSeqID", "QueryLength", "QueryStart", "QueryEnd", "AlignmentLength", 
#                    "Percentage of Identical Matches", "E-value", "Bit Score", "Number of Identical Matches", 
#                    "Gaps", "SubjectStrand", "Query Coverage per HSP", "Query Sequence", "Subject Sequence"]
#         blast_results = pd.read_csv(output_file, sep="\t", names=columns)
#         blast_results["Query Coverage (%)"] = (blast_results["QueryEnd"] - blast_results["QueryStart"] + 1) / blast_results["QueryLength"] * 100
#         blast_results = blast_results[["QuerySeq.ID", "SubjectSeqID", "QueryLength", "QueryStart", "QueryEnd", 
#                                       "AlignmentLength", "Percentage of Identical Matches", "E-value", 
#                                       "Bit Score", "Number of Identical Matches", "Gaps", "SubjectStrand", 
#                                       "Query Coverage per HSP", "Query Sequence", "Subject Sequence", 
#                                       "Query Coverage (%)"]]
#         excel_output_file = os.path.join(os.path.dirname(output_file), f"{os.path.splitext(os.path.basename(output_file))[0]}_results.xlsx")
#         with pd.ExcelWriter(excel_output_file, engine='xlsxwriter') as writer:
#             blast_results.to_excel(writer, sheet_name='BLAST Results', index=False)
#             workbook = writer.book
#             worksheet = writer.sheets['BLAST Results']
#             header_format = workbook.add_format({'bold': True, 'font_size': 12})
#             for col_num, value in enumerate(blast_results.columns.values):
#                 worksheet.write(0, col_num, value, header_format)
#             worksheet.set_column(0, len(blast_results.columns) - 1, 20)
#         QMessageBox.information(self, "Success", f"BLAST results saved to {excel_output_file}.")

#     def run_command(self, command):
#         self.worker = Worker(command)
#         self.worker.finished.connect(self.on_blast_completed)
#         self.worker.error.connect(self.on_blast_error)
#         self.worker.start()
    
#     def on_blast_completed(self):
#         self.run_blast_button.setEnabled(True)
#         self.stop_button.setEnabled(False)
#         QMessageBox.information(self, "Success", "BLAST completed successfully.")

#     def on_blast_error(self, error_message):
#         self.run_blast_button.setEnabled(True)
#         self.make_db_button.setEnabled(True)
#         self.stop_button.setEnabled(False)
#         QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")

#     def update_matrix_combo(self):
#         if self.blast_type_combo.currentText() == "blastp":
#             self.matrix_combo.setEnabled(True)
#         else:
#             self.matrix_combo.setEnabled(False)
#             self.matrix_combo.setCurrentText("BLOSUM62")

#     def stop_process(self):
#         if self.worker:
#             self.worker.stop()
#         self.make_db_button.setEnabled(True)
#         self.run_blast_button.setEnabled(True)
#         self.stop_button.setEnabled(False)
#         QMessageBox.information(self, "Process Stopped", "The BLAST process has been stopped.")

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
#             event.accept()
#         elif msg_box.clickedButton() == minimize_button:
#             event.ignore()
#             self.showMinimized()
#         else:
#             event.ignore()
#         self.file_name_display.setText("No file chosen")
#         self.query_file_display.setText("No file chosen")
#         self.output_dir_display.setText("No directory chosen")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Blast()
#     window.show()
#     sys.exit(app.exec())

import sys
import pandas as pd
import logging
import os
import shutil
import subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget,
    QLabel, QLineEdit, QFormLayout, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QComboBox
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import QSize, QPropertyAnimation, QEasingCurve, Qt
from PySide6.QtCore import QThread, Signal  

class Worker(QThread):
    finished = Signal()
    error = Signal(str)

    def __init__(self, command, log_file):
        super().__init__()
        self.command = command
        self.log_file = log_file
        self.process = None
        self.stop_requested = False

    def run(self):
        try:
            self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.process.wait()
            if self.stop_requested:
                self.error.emit("Process stopped by user")
                return
            result = self.process
            if result.returncode != 0:
                with open(self.log_file, 'a') as log:
                    log.write("=== BLAST Command ===\n")
                    log.write("\n=== BLAST Command Error Output ===\n")
                    log.write(result.stderr if result.stderr else 'No errors.\n')
                self.error.emit(result.stderr)
        except Exception as e:
            with open(self.log_file, 'a') as log:
                log.write(f"\nException occurred: {str(e)}\n")
            self.error.emit(str(e))

    def stop(self):
        self.stop_requested = True
        if self.process:
            self.process.terminate()

class Blast(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genome Wide WorkBench")
        self.setWindowIcon(QIcon('src/image.png'))
        self.resizeToHalfScreen()
        self.is_dark_theme = False

        self.header_label = QLabel("BlastXPlorer")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        self.header_label.setStyleSheet("""
            QLabel {
                background-color: #2C3E50;
                color: white;
                padding: 20px;
                border-radius: 12px;
            }
        """)

        self.load_button = QPushButton("Load FASTA File")
        self.load_button.setIcon(QIcon('upload_icon.png'))
        self.load_button.setIconSize(QSize(16, 16))
        self.load_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.load_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                color: white;
                background-color: #2C3E50;
                border: none;
                text-align: left;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            QPushButton:pressed {
                background-color: #34495E;
            }
        """)
        self.load_button.clicked.connect(self.load_file)

        self.query_button = QPushButton("Load Query File")
        self.query_button.setIcon(QIcon('upload_icon.png'))
        self.query_button.setIconSize(QSize(16, 16))
        self.query_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.query_button.setFixedSize(200, 40)
        self.query_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                color: white;
                background-color: #2C3E50;
                border: none;
                text-align: left;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            QPushButton:pressed {
                background-color: #34495E;
            }
        """)
        self.query_button.clicked.connect(self.load_query_file)

        self.choose_dir_button = QPushButton("Choose Output Directory")
        self.choose_dir_button.setIcon(QIcon('folder_icon.png'))
        self.choose_dir_button.setIconSize(QSize(16, 16))
        self.choose_dir_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.choose_dir_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                color: white;
                background-color: #2C3E50;
                border: none;
                text-align: left;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            QPushButton:pressed {
                background-color: #34495E;
            }
        """)
        self.choose_dir_button.clicked.connect(self.choose_directory)

        self.file_name_display = QLineEdit(self)
        self.file_name_display.setReadOnly(True)
        self.file_name_display.setPlaceholderText("No file chosen")
        self.file_name_display.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2C3E50;
                padding: 5px;
                font-size: 12px;
                border-radius: 4px;
            }
        """)

        self.query_file_display = QLineEdit(self)
        self.query_file_display.setReadOnly(True)
        self.query_file_display.setPlaceholderText("No query file chosen")
        self.query_file_display.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2C3E50;
                padding: 5px;
                font-size: 12px;
                border-radius: 4px;
            }
        """)

        self.output_dir_display = QLineEdit(self)
        self.output_dir_display.setReadOnly(True)
        self.output_dir_display.setPlaceholderText("No directory chosen")
        self.output_dir_display.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2C3E50;
                padding: 5px;
                font-size: 12px;
                border-radius: 4px;
            }
        """)

        self.download_file_name_input = QLineEdit(self)
        self.download_file_name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2C3E50;
                padding: 5px;
                font-size: 12px;
                border-radius: 4px;
            }
        """)

        self.file_name_input = QLineEdit()
        self.file_name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2C3E50;
                padding: 5px;
                font-size: 12px;
                border-radius: 4px;
            }
        """)

        self.evalue_input = QLineEdit("0.00001")
        self.evalue_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2C3E50;
                padding: 5px;
                font-size: 12px;
                border-radius: 4px;
            }
        """)

        self.word_size_input = QLineEdit("11")
        self.word_size_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2C3E50;
                padding: 5px;
                font-size: 12px;
                border-radius: 4px;
            }
        """)

        self.num_threads_input = QLineEdit("1")
        self.num_threads_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2C3E50;
                padding: 5px;
                font-size: 12px;
                border-radius: 4px;
            }
        """)

        self.db_type_combo = QComboBox()
        self.db_type_combo.addItems(["Nucleotide", "Protein"])
        self.db_type_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #2C3E50;
                padding: 5px;
                font-size: 12px;
                border-radius: 4px;
            }
        """)

        self.blast_type_combo = QComboBox()
        self.blast_type_combo.addItems(["blastn", "blastp", "blastx", "tblastx", "tblastn"])
        self.blast_type_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #2C3E50;
                padding: 5px;
                font-size: 12px;
                border-radius: 4px;
            }
        """)
        self.blast_type_combo.currentIndexChanged.connect(self.update_word_size)
        self.blast_type_combo.currentIndexChanged.connect(self.update_matrix_combo)

        self.matrix_combo = QComboBox()
        self.matrix_combo.addItems(["BLOSUM80", "BLOSUM62", "BLOSUM50", "BLOSUM45", "PAM250", "BLOSUM90", "PAM30", "PAM70", "IDENTITY"])
        self.matrix_combo.setCurrentText("BLOSUM62")
        self.matrix_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #2C3E50;
                padding: 5px;
                font-size: 12px;
                border-radius: 4px;
            }
        """)
        self.matrix_combo.setEnabled(False)

        self.make_db_button = QPushButton("Make BLAST DB")
        self.make_db_button.setFixedSize(200, 50)
        self.make_db_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                color: white;
                background-color: #2C3E50;
                border: none;
                text-align: left;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            QPushButton:pressed {
                background-color: #34495E;
            }
        """)
        self.make_db_button.setEnabled(False)
        self.make_db_button.clicked.connect(self.make_db)

        self.run_blast_button = QPushButton("Run BLAST")
        self.run_blast_button.setFixedSize(200, 50)
        self.run_blast_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                color: white;
                background-color: #2C3E50;
                border: none;
                text-align: left;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            QPushButton:pressed {
                background-color: #34495E;
            }
        """)
        self.run_blast_button.setEnabled(False)
        self.run_blast_button.clicked.connect(self.blast_nucleotide)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedSize(200, 50)
        self.stop_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                color: white;
                background-color: #2C3E50;
                border: none;
                text-align: center;
                padding: 10px 20px;
            }
            QPushButton:disabled {
                background-color: #A0A0A0;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            QPushButton:pressed {
                background-color: #34495E;
            }
        """)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_process)

        self.animation = QPropertyAnimation(self.make_db_button, b"size")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)

        self.theme_toggle_button = QPushButton("Switch to Dark Mode")
        self.theme_toggle_button.setFixedSize(150, 30)
        self.theme_toggle_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                color: white;
                background-color: #2C3E50;
                border: none;
                text-align: left;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            QPushButton:pressed {
                background-color: #34495E;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header_label)
        
        file_form_layout = QFormLayout()
        load_layout = QHBoxLayout()
        load_layout.addWidget(self.load_button)
        load_layout.addWidget(self.file_name_display)
        file_form_layout.addRow(QLabel("Upload the FASTA file for DB creation:"), load_layout)
        
        query_layout = QHBoxLayout()
        query_layout.addWidget(self.query_button)
        query_layout.addWidget(self.query_file_display)
        file_form_layout.addRow(QLabel("Upload the Query file for BLAST:"), query_layout)
        
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.choose_dir_button)
        dir_layout.addWidget(self.output_dir_display)
        file_form_layout.addRow(QLabel("Choose Output Directory for Results:"), dir_layout)
        file_form_layout.addRow(QLabel("Database Type:"), self.db_type_combo)
        file_form_layout.addRow(QLabel("BLAST Type:"), self.blast_type_combo)
        file_form_layout.addRow(QLabel("Matrix (for BLASTP):"), self.matrix_combo)
        file_form_layout.addRow(QLabel("Provide Name for creation of DB files:"), self.file_name_input)
        file_form_layout.addRow(QLabel("E-value:"), self.evalue_input)
        file_form_layout.addRow(QLabel("Word Size:"), self.word_size_input)
        file_form_layout.addRow(QLabel("Number of Threads:"), self.num_threads_input)
        file_form_layout.addRow(QLabel("Result File Name (Optional):"), self.download_file_name_input)
        main_layout.addLayout(file_form_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.make_db_button, alignment=Qt.AlignmentFlag.AlignLeft)
        button_layout.addWidget(self.run_blast_button, alignment=Qt.AlignmentFlag.AlignLeft)
        button_layout.addWidget(self.stop_button, alignment=Qt.AlignmentFlag.AlignLeft)
    
        main_layout.addLayout(button_layout)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def resizeToHalfScreen(self):
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen.width() // 4, screen.height() // 4, screen.width() // 2, screen.height() // 2)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open FASTA File", "", "FASTA Files (*.fasta *.fa *.fna *.ffn *.faa *.frn)")
        if file_name:
            self.file_name_display.setText(file_name)
            self.make_db_button.setEnabled(True)
    
    def load_query_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Query File", "", "FASTA Files (*.fasta *.fa *.fna *.ffn *.faa *.frn)")
        if file_name:
            self.query_file_display.setText(file_name)
            self.run_blast_button.setEnabled(True)

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Choose Output Directory")
        if directory:
            self.output_dir_display.setText(directory)

    def check_sequence_type(self, fasta_file):
        """Check if the FASTA file contains protein or nucleotide sequences."""
        nucleotide_bases = set('ACGTUNRYKMSWBDHVNacgtunrykmswbdhvn')
        protein_amino_acids = set('ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy')
        
        sequence = ""
        try:
            with open(fasta_file, 'r') as f:
                for line in f:
                    if not line.startswith('>'):
                        sequence += line.strip()
            if not sequence:
                return None  # Empty sequence
            sequence = sequence.upper()
            total_chars = len(sequence)
            nucleotide_count = sum(1 for char in sequence if char in nucleotide_bases)
            nucleotide_ratio = nucleotide_count / total_chars if total_chars > 0 else 0
            
            # If >90% of characters are nucleotide bases, classify as nucleotide
            if nucleotide_ratio > 0.9:
                return 'nucl'
            else:
                return 'prot'
        except Exception as e:
            logging.error(f"Error reading FASTA file: {str(e)}")
            return None

    def make_db(self):
        fasta_file = self.file_name_display.text()
        db_type = self.db_type_combo.currentText().lower()
        db_type = 'nucl' if db_type == 'nucleotide' else 'prot'
        db_name = self.file_name_input.text()
        output_dir = self.output_dir_display.text()

        if not fasta_file or not db_name or not output_dir:
            QMessageBox.warning(self, "Input Error", "Please provide all necessary inputs.")
            return

        # Check sequence type
        sequence_type = self.check_sequence_type(fasta_file)
        if sequence_type is None:
            QMessageBox.critical(self, "Error", "Unable to read or analyze the FASTA file. Please ensure it is valid.")
            return
        if sequence_type != db_type:
            QMessageBox.critical(self, "Input Error", f"The FASTA file contains {sequence_type} sequences, but you selected {db_type} as the database type. Please select the correct database type.")
            return

        if hasattr(sys, '_MEIPASS'):
            blast_dir = os.path.join(sys._MEIPASS, 'tools', 'blast')
        else:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            blast_dir = os.path.join(base_dir, 'tools', 'blast')

        makeblastdb_path = os.path.join(blast_dir, 'makeblastdb.exe')
        if not os.path.exists(makeblastdb_path):
            QMessageBox.critical(self, "Error", f"makeblastdb tool not found at: {makeblastdb_path}")
            return

        if not os.path.exists(fasta_file):
            QMessageBox.critical(self, "Error", "FASTA file not found.")
            return

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        log_file = os.path.join(output_dir, "blast_errors.log")
        with open(log_file, 'w'):
            pass    

        QMessageBox.information(self, "Analysis Started", "Your analysis is running.")
        self.make_db_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        makeblastdb_command = [
            makeblastdb_path,
            '-in', fasta_file,
            '-dbtype', db_type,
            '-out', os.path.join(output_dir, db_name)
        ]

        self.worker = Worker(makeblastdb_command, log_file)
        self.worker.finished.connect(lambda: self.handle_makeblastdb_completion(log_file))
        self.worker.error.connect(lambda error: self.handle_error(error, log_file))
        self.worker.start()

    def handle_makeblastdb_completion(self, log_file):
        self.make_db_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        try:
            with open(log_file, 'r') as f:
                error_content = f.read().strip()
            if error_content:
                raise ValueError("BLAST database creation failed. Check the log for details.")
            QMessageBox.information(self, "Success", "BLAST database created successfully.")
        except Exception as e:
            logging.error(f"Error during BLAST database creation: {str(e)}")
            QMessageBox.critical(self, "Error", f"BLAST database creation failed, see 'blast_errors.log' in the directory: {log_file}")

    def handle_error(self, error, log_file):
        self.make_db_button.setEnabled(True)
        self.run_blast_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        logging.error(f"Operation failed. Error: {error}")
        with open(log_file, 'a') as log:
            log.write(f"Error: {error}\n")
        QMessageBox.critical(self, "Error", f"Operation failed. Check {log_file} for details.")

    def update_word_size(self):
        blast_type = self.blast_type_combo.currentText()
        if blast_type in ["blastp", "tblastn", "blastx", "tblastx"]:
            self.word_size_input.setText("3")
        else:
            self.word_size_input.setText("11")

    def blast_nucleotide(self):
        query_file = self.query_file_display.text()
        db_name = self.file_name_input.text()
        output_dir = self.output_dir_display.text()
        evalue = self.evalue_input.text()
        word_size = self.word_size_input.text()
        num_threads = self.num_threads_input.text()
        blast_type = self.blast_type_combo.currentText()
        matrix = self.matrix_combo.currentText()

        if blast_type in ["blastp"] and self.db_type_combo.currentText() == "Nucleotide":
            QMessageBox.warning(self, "Input Error", "You must choose a Protein database for blastp.")
            return
        elif blast_type in ["blastn"] and self.db_type_combo.currentText() == "Protein":
            QMessageBox.warning(self, "Input Error", "You must choose a Nucleotide database for blastn.")
            return
        elif blast_type in ["blastx"] and self.db_type_combo.currentText() == "Nucleotide":
            QMessageBox.warning(self, "Input Error", "You must choose a Protein database for blastx.")
            return
        elif blast_type in ["tblastn"] and self.db_type_combo.currentText() == "Protein":
            QMessageBox.warning(self, "Input Error", "You must choose a Nucleotide database for tblastn.")
            return
        elif blast_type in ["tblastx"] and self.db_type_combo.currentText() == "Protein":
            QMessageBox.warning(self, "Input Error", "You must choose a Nucleotide database for tblastx.")
            return

        if blast_type in ["tblastn", "blastp", "blastx"] and int(word_size) >= 8:
            QMessageBox.warning(self, "Input Error", "Word size must be less than 8 for tblastn, blastp, or blastx.")
            return
        elif blast_type in ["tblastx"] and int(word_size) >= 6:
            QMessageBox.warning(self, "Input Error", "Word size must be less than 6 for tblastx.")
            return
        elif blast_type in ["blastn"] and int(word_size) < 4:
            QMessageBox.warning(self, "Input Error", "Word size must be more than 4 for blastn.")
            return

        if not query_file or not db_name or not output_dir or not evalue or not word_size or not num_threads:
            QMessageBox.warning(self, "Input Error", "Please provide all necessary inputs.")
            return

        QMessageBox.information(self, "Analysis Started", "Your analysis is running.")
        self.run_blast_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        db_path = os.path.join(output_dir, db_name)
        output_file_name = self.download_file_name_input.text()
        output_file = os.path.join(output_dir, f"{output_file_name}.txt")

        log_file = os.path.join(output_dir, "blast_errors.log")
        with open(log_file, 'w'):
            pass

        if hasattr(sys, '_MEIPASS'):
            blast_dir = os.path.join(sys._MEIPASS, 'tools', 'blast')
        else:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            blast_dir = os.path.join(base_dir, 'tools', 'blast')

        blast_command = [
            os.path.join(blast_dir, blast_type),
            '-query', query_file,
            '-db', db_path,
            '-evalue', evalue,
            '-word_size', word_size,
            '-num_threads', num_threads,
            '-out', output_file,
            '-outfmt', "6 qseqid sseqid qlen qstart qend length pident evalue bitscore nident gaps sstrand qcovhsp qseq sseq"
        ]

        if blast_type == "blastp":
            blast_command.append('-matrix')
            blast_command.append(matrix)

        self.worker = Worker(blast_command, log_file)
        self.worker.finished.connect(lambda: self.handle_blast_completion(output_file, log_file))
        self.worker.error.connect(lambda error: self.handle_error(error, log_file))
        self.worker.start()

    def handle_blast_completion(self, output_file, log_file):
        self.run_blast_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    error_content = f.read().strip()
                if error_content:
                    raise ValueError("BLAST search failed with errors. Please check the log.")
            self.process_blast_results(output_file)
            QMessageBox.information(self, "Success", "BLAST search completed successfully.")
        except Exception as e:
            logging.error(f"Error during BLAST search: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to process BLAST results. See 'blast_errors.log' in the directory: {log_file}")

    def on_blast_success(self, output_file):
        self.run_blast_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        try:
            self.process_blast_results(output_file)
            QMessageBox.information(self, "Success", "BLAST search completed successfully.")
        except Exception as e:
            logging.error(f"Error processing BLAST results: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to process BLAST results. Error: {str(e)}")

    def process_blast_results(self, output_file):
        columns = ["QuerySeq.ID", "SubjectSeqID", "QueryLength", "QueryStart", "QueryEnd", "AlignmentLength", 
                   "Percentage of Identical Matches", "E-value", "Bit Score", "Number of Identical Matches", 
                   "Gaps", "SubjectStrand", "Query Coverage per HSP", "Query Sequence", "Subject Sequence"]
        blast_results = pd.read_csv(output_file, sep="\t", names=columns)
        blast_results["Query Coverage (%)"] = (blast_results["QueryEnd"] - blast_results["QueryStart"] + 1) / blast_results["QueryLength"] * 100
        blast_results = blast_results[["QuerySeq.ID", "SubjectSeqID", "QueryLength", "QueryStart", "QueryEnd", 
                                      "AlignmentLength", "Percentage of Identical Matches", "E-value", 
                                      "Bit Score", "Number of Identical Matches", "Gaps", "SubjectStrand", 
                                      "Query Coverage per HSP", "Query Sequence", "Subject Sequence", 
                                      "Query Coverage (%)"]]
        excel_output_file = os.path.join(os.path.dirname(output_file), f"{os.path.splitext(os.path.basename(output_file))[0]}_results.xlsx")
        with pd.ExcelWriter(excel_output_file, engine='xlsxwriter') as writer:
            blast_results.to_excel(writer, sheet_name='BLAST Results', index=False)
            workbook = writer.book
            worksheet = writer.sheets['BLAST Results']
            header_format = workbook.add_format({'bold': True, 'font_size': 12})
            for col_num, value in enumerate(blast_results.columns.values):
                worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(0, len(blast_results.columns) - 1, 20)
        QMessageBox.information(self, "Success", f"BLAST results saved to {excel_output_file}.")

    def run_command(self, command):
        self.worker = Worker(command)
        self.worker.finished.connect(self.on_blast_completed)
        self.worker.error.connect(self.on_blast_error)
        self.worker.start()
    
    def on_blast_completed(self):
        self.run_blast_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        QMessageBox.information(self, "Success", "BLAST completed successfully.")

    def on_blast_error(self, error_message):
        self.run_blast_button.setEnabled(True)
        self.make_db_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")

    def update_matrix_combo(self):
        if self.blast_type_combo.currentText() == "blastp":
            self.matrix_combo.setEnabled(True)
        else:
            self.matrix_combo.setEnabled(False)
            self.matrix_combo.setCurrentText("BLOSUM62")

    def stop_process(self):
        if self.worker:
            self.worker.stop()
        self.make_db_button.setEnabled(True)
        self.run_blast_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        QMessageBox.information(self, "Process Stopped", "The BLAST process has been stopped.")

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
            event.accept()
        elif msg_box.clickedButton() == minimize_button:
            event.ignore()
            self.showMinimized()
        else:
            event.ignore()
        self.file_name_display.setText("No file chosen")
        self.query_file_display.setText("No file chosen")
        self.output_dir_display.setText("No directory chosen")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Blast()
    window.show()
    sys.exit(app.exec())