# import sys
# import os
# import subprocess
# import logging
# import zipfile
# import shutil
# from Bio import SeqIO
# import pandas as pd
# from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, 
#                                QLabel, QFileDialog, QProgressBar, QMessageBox, QLineEdit, QHBoxLayout,QSizePolicy,QSpacerItem)
# from PySide6.QtCore import QThread, Signal, Qt, QSize
# from PySide6.QtGui import QFont, QIcon
# # Set up directories for logs and outputs
# # Update directories for logs and outputs to be outside the application directory
# HOME_DIR = os.path.expanduser("~")  # User's home directory
# EXTERNAL_DIR = os.path.join(HOME_DIR, "KAKS_Tool")

# LOGS_DIR = os.path.join(EXTERNAL_DIR, "logs")
# OUTPUT_DIR = os.path.join(EXTERNAL_DIR, "output")

# # Create the external base directory and subdirectories if they don't exist
# os.makedirs(LOGS_DIR, exist_ok=True)
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # Update logging configuration
# LOG_FILE = os.path.join(LOGS_DIR, "kaks_error.log")
# # Clear the log file before setting up logging
# if os.path.exists(LOG_FILE):
#     with open(LOG_FILE, "w") as log_file:
#         log_file.truncate(0)  # Ensure the file is empty at the start

# logging.basicConfig(
#     filename=LOG_FILE,
#     level=logging.ERROR,
#     filemode='w',  # Overwrite the file at the start of each run
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )



# # clustalw_path = "clustalw2.exe"
# # pal2nal_path = "pal2nal.exe"
# # # perl_path = "perl.exe"
# # axtconvertor_path = "AXTConvertor.exe"
# # kaks_calculator_path = "KaKs_Calculator.exe"
# # Define paths for tools, considering PyInstaller's _MEIPASS attribute
# if hasattr(sys, '_MEIPASS'):
#     base_dir = os.path.join(sys._MEIPASS, 'tools')
# else:
#     base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tools'))

# clustalw_path = os.path.join(base_dir, 'clustalw2.exe')
# pal2nal_path = os.path.join(base_dir, 'pal2nal.exe')
# axtconvertor_path = os.path.join(base_dir, 'AXTConvertor.exe')
# kaks_calculator_path = os.path.join(base_dir, 'KaKs_Calculator.exe')


# class FileHandler:
#     def __init__(self, file_path):
#         self.file_path = file_path

#     # def read_lines(self):
#     #     """Read lines from a file."""
#     #     if not os.path.exists(self.file_path):
#     #         logging.error(f"Error: File '{self.file_path}' does not exist.")
#     #         return None
#     #     with open(self.file_path, "r", encoding="utf-8") as f:
#     #     # with open(self.file_path,'r', encoding='ISO-8859-1') as f:
#     #     # with open(self.file_path_file, 'r', encoding='utf-8', errors='ignore') as f:


#     #         return f.readlines()

#     def read_lines(self):
#         """Read lines from a file and handle encoding errors."""
#         if not os.path.exists(self.file_path):
#             logging.error(f"Error: File '{self.file_path}' does not exist.")
#             return None
        
#         try:
#             with open(self.file_path, "r", encoding="utf-8") as f:
#                 return f.readlines()
#         except UnicodeDecodeError as e:
#             logging.error(f"Error: File '{self.file_path}' is not UTF-8 encoded. {e}")
#             return None
#         except Exception as e:
#             logging.error(f"Error reading the file: {e}")
#             return None

    


# class SequenceExtractor:
#     def __init__(self, fasta_file):
#         self.fasta_file = fasta_file

#     def extract_sequences(self, header_list, output_filename):
#         """Extract sequences from a FASTA file based on the header list."""
#         extracted_sequences = []
#         with open(self.fasta_file, "r") as fasta_in, open(output_filename, "w") as fasta_out:
#             existing_headers = set()
#             for record in SeqIO.parse(fasta_in, "fasta"):
#                 if record.id in header_list and record.id not in existing_headers:
#                     SeqIO.write(record, fasta_out, "fasta")
#                     existing_headers.add(record.id)
#                     extracted_sequences.append(record)
#         return extracted_sequences

# class SequenceAligner:
#     @staticmethod
#     def run_clustalw(clustalw_path, input_file, output_file):
#         """Run ClustalW for sequence alignment."""
#         cmd = f'"{clustalw_path}" -infile="{input_file}" -OUTFILE="{output_file}"'
#         try:
#             results = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
#             if results.returncode != 0:
#                 logging.error(f"Error running command: {cmd}")
#                 logging.error(f"Error running ClustalW: {results.stderr}")
#                 return False
#             logging.info("ClustalW execution successful.")
#             return True
#         except Exception as e:
#             logging.error(f"Error running ClustalW: {e}")
#             return False

# class Pal2NalRunner:
#     @staticmethod
#     def run_pal2nal(input_alignment_file, input_cds_file, output_codon_alignment_file):
#         """Run pal2nal.pl to align coding sequences."""
#         command = [
#             # perl_path,
#             pal2nal_path,
#             input_alignment_file,
#             input_cds_file,
#             "-nogap"
#         ]
#         try:
#             with open(output_codon_alignment_file, "w") as output_file:
#                 subprocess.run(command, stdout=output_file, stderr=subprocess.PIPE, check=True)
#             logging.info("pal2nal execution successful.")
#             return True
#         except subprocess.CalledProcessError as e:
#             logging.error(f"Error running command: {' '.join(command)}")
#             logging.error(f"Error running pal2nal.pl: {e}")
#             return False

# class AxtConvertor:
#     @staticmethod
#     def run_axt_convertor(input_codon_alignment_file, output_axt_file):
#         """Convert codon alignment to AXT format."""
#         try:
#             result_axt = subprocess.run([axtconvertor_path, input_codon_alignment_file, output_axt_file], capture_output=True, text=True, check=False)
#             if result_axt.returncode != 0:
#                 logging.warning(f"AXTConvertor returned a non-zero exit code: {result_axt.returncode}")
#             if result_axt.stderr:
#                 logging.error(f"Error running AXTConvertor: {result_axt.stderr}")
#             if os.path.isfile(output_axt_file):
#                 logging.info("AXTConvertor execution successful.")
#                 return True
#             else:
#                 logging.error("AXTConvertor failed to produce the output file.")
#                 return False
#         except Exception as e:
#             logging.error(f"Exception occurred while running AXTConvertor: {e}")
#             return False

# class KaksCalculator:
#     @staticmethod
#     def run_kaks_calculator(output_axt_file, output_kaks_file):
#         """Run KaKs_Calculator to calculate Ka/Ks values."""
#         try:
#             result_kaks = subprocess.run([kaks_calculator_path, "-i", output_axt_file, "-o", output_kaks_file], capture_output=True, text=True, check=True)
#             logging.info("KaKs_Calculator execution successful.")
#             return True
#         except subprocess.CalledProcessError as e:
#             logging.error(f"Error running KaKs_Calculator: {e}")
#             return False

# class AnalysisRunner:
#     def __init__(self, input_file, cds_fasta_file, pep_fasta_file):
#         self.input_file = input_file
#         self.cds_fasta_file = cds_fasta_file
#         self.pep_fasta_file = pep_fasta_file

#     def run_analysis(self, header_list):
#         dfs_kaks = []
#         lines = FileHandler(self.input_file).read_lines()
#         if lines:
#             num_lines = len(lines)

#             # OUTPUT_DIR = "output"
#             # if os.path.exists(OUTPUT_DIR):
#             #     shutil.rmtree(OUTPUT_DIR)  # Delete the output directory if it exists
#             # os.makedirs(OUTPUT_DIR, exist_ok=True)  # Create a new output directory
#             if os.path.exists(OUTPUT_DIR):
#                 shutil.rmtree(OUTPUT_DIR)
#             os.makedirs(OUTPUT_DIR, exist_ok=True)


#             output_files = [generate_filename(OUTPUT_DIR, "row", i) for i in range(1, num_lines + 1)]
#             column_1_files = [generate_filename(OUTPUT_DIR, f"{i}_row_column_1", i) for i in range(1, num_lines + 1)]
#             column_2_files = [generate_filename(OUTPUT_DIR, f"{i}_row_column_2", i) for i in range(1, num_lines + 1)]
#             pair_list_files = [generate_filename(OUTPUT_DIR, f"{i}_pairs.list", i) for i in range(1, num_lines + 1)]
#             cds_files = [generate_filename(OUTPUT_DIR, f"{i}_p2_cds", i, extension=".fa") for i in range(1, num_lines + 1)]
#             pep_files = [generate_filename(OUTPUT_DIR, f"{i}_p2_pep", i, extension=".fa") for i in range(1, num_lines + 1)]
#             clustal_files = [os.path.join(OUTPUT_DIR, f"{i}_p2_pep.aln") for i in range(1, num_lines + 1)]
#             pal2nal_files = [os.path.join(OUTPUT_DIR, f"{i}_p2_cod.aln") for i in range(1, num_lines + 1)]
#             axt_files = [os.path.join(OUTPUT_DIR, f"{i}_p2.axt") for i in range(1, num_lines + 1)]
#             kaks_files = [os.path.join(OUTPUT_DIR, f"{i}_p2.kaks") for i in range(1, num_lines + 1)]

#             for i, line in enumerate(lines, 1):
#                 columns = line.split()
#                 if len(columns) < 2:
#                     logging.warning(f"Line {i} has fewer than two columns.")
#                     continue
#                 write_to_file(output_files[i - 1], line)
#                 write_to_file(column_1_files[i - 1], columns[0])
#                 write_to_file(column_2_files[i - 1], columns[1])
#                 write_to_file(pair_list_files[i - 1], f"{columns[0]}\n{columns[1]}")

#             for i, query_file in enumerate(pair_list_files, 1):
#                 header_list = set()
#                 with open(query_file, "r") as f:
#                     for line in f:
#                         line = line.strip()
#                         header_list.add(line)
#                 output_filename_cds = cds_files[i - 1]
#                 output_filename_pep = pep_files[i - 1]
#                 extracted_sequences_pep = SequenceExtractor(self.pep_fasta_file).extract_sequences(header_list, output_filename_pep)
#                 extracted_sequences_cds = SequenceExtractor(self.cds_fasta_file).extract_sequences(header_list, output_filename_cds)

#                 input_file = pep_files[i - 1]
#                 output_file = clustal_files[i - 1]
#                 if not SequenceAligner.run_clustalw(clustalw_path, input_file, output_file):
#                     logging.error(f"Error running ClustalW for query file: {query_file}")

#                 input_alignment_file = clustal_files[i - 1]
#                 input_cds_file = cds_files[i - 1]
#                 output_codon_alignment_file = pal2nal_files[i - 1]
#                 if not Pal2NalRunner.run_pal2nal(input_alignment_file, input_cds_file, output_codon_alignment_file):
#                     logging.error(f"Error running pal2nal.pl for query file: {query_file}")

#                 output_axt_file = axt_files[i - 1]
#                 if not AxtConvertor.run_axt_convertor(output_codon_alignment_file, output_axt_file):
#                     logging.error(f"Error running Axt Convertor for query file: {query_file}")

#                 output_kaks_file = kaks_files[i - 1]
#                 if os.path.exists(output_axt_file):
#                     if not KaksCalculator.run_kaks_calculator(output_axt_file, output_kaks_file):
#                         logging.error(f"Error running Kaks Calculator for query file: {query_file}")
#                     else:
#                         df_kaks = pd.read_csv(output_kaks_file, sep='\t')
#                         dfs_kaks.append(df_kaks)

#             if dfs_kaks:
#                 combined_df = pd.concat(dfs_kaks)
#                 excel_filename = os.path.join(OUTPUT_DIR, "combined_kaks_data.xlsx")
#                 combined_df.to_excel(excel_filename, index=False)

#                 all_files = [self.input_file, self.cds_fasta_file, self.pep_fasta_file] + output_files + column_1_files + column_2_files + pair_list_files + cds_files + pep_files + clustal_files + pal2nal_files + axt_files + kaks_files

#                 zip_file_path = os.path.join(OUTPUT_DIR, "output_files.zip")
#                 with zipfile.ZipFile(zip_file_path, "w") as zipf:
#                     for file_path in all_files:
#                         if os.path.exists(file_path):
#                             if file_path in kaks_files:
#                                 folder_name = "Kaks_Files"
#                                 arcname = os.path.join(folder_name, os.path.basename(file_path))
#                             else:
#                                 arcname = os.path.basename(file_path)
#                             zipf.write(file_path, arcname=arcname)
#                         else:
#                             logging.warning(f"File not found: {file_path}")
#                 with zipfile.ZipFile(zip_file_path, "a") as zipf:
#                     excel_folder_name = "combined_kaks_data"
#                     arcname = os.path.join(excel_folder_name, "combined_kaks_data.xlsx")
#                     zipf.write(excel_filename, arcname=arcname)
#                 return True
#         return False

# def generate_filename(OUTPUT_DIR, base, i, extension=".txt"):
#     """Generate a filename based on base, index i, and optional extension."""
#     return os.path.join(OUTPUT_DIR, f"{base}_{i}{extension}")

# # def write_to_file(filename, data, as_bytes=False):
# #     """Write data to a file."""
# #     mode = "wb" if as_bytes else "w"
# #     with open(filename, mode) as f:
# #         if as_bytes:
# #             f.write(data)
# #         else:
# #             f.write(data)
# def write_to_file(filename, data, as_bytes=False):
#     """Write data to a file as either bytes or text."""
#     mode = "wb" if as_bytes else "w"
    
#     try:
#         with open(filename, mode, encoding=None if as_bytes else "utf-8") as f:
#             if as_bytes:
#                 # Ensure the data is bytes before writing
#                 if isinstance(data, str):
#                     data = data.encode("utf-8")
#                 f.write(data)
#             else:
#                 f.write(data)
#     except UnicodeEncodeError as e:
#         logging.error(f"Error encoding data for file '{filename}': {e}")
#     except Exception as e:
#         logging.error(f"Error writing data to file '{filename}': {e}")



# class Worker(QThread):
#     progressChanged = Signal(int)
#     analysisFinished = Signal(bool)

#     def __init__(self, input_file, cds_file, pep_file):
#         super().__init__()
#         self.input_file = input_file
#         self.cds_file = cds_file
#         self.pep_file = pep_file

#     def run(self):
#         header_list = []  # Define  header list here
#         analysis_runner = AnalysisRunner(self.input_file, self.cds_file, self.pep_file)
#         success = analysis_runner.run_analysis(header_list)
#         self.analysisFinished.emit(success)

# class SequenceAnalysisApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()

#     def init_ui(self):
#         self.setWindowTitle("Genomics WorkBench")
#         self.setWindowIcon(QIcon('src/image.png'))

#         self.resize(900, 600)  # Set window size

#         # Create and style the header label
#         self.header_label = QLabel(" KA/KS Analysis Tool")
#         self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.header_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))  # Adjust font size
#         self.header_label.setStyleSheet("""
#             QLabel {
#                 background-color:  #2C3E50;  /* Header background color */
#                 color: white;                 /* Header text color */
#                 padding: 10px;                /* Padding around text */
#                 border-radius: 10px;         /* Rounded corners */
#             }
#         """)
#         self.header_label.setFixedHeight(150)  # Fixed height for the header

#         # Create the main layout
#         layout = QVBoxLayout()

#         # Add the header label to the layout
#         layout.addWidget(self.header_label)

#         # Create a layout for Paralogs file
#         self.paralogs_layout = QHBoxLayout()
#         self.paralogs_file_label = QLabel('Upload Paralogs File:', self)
#         self.paralogs_file_label.setFont(QFont("Arial", 14))  
#         self.paralogs_layout.addWidget(self.paralogs_file_label)
#         self.paralogs_file_button = QPushButton('Browse', self)
#         self.paralogs_file_button.setStyleSheet("""
#             QPushButton {
#                 background-color: #2C3E50; 
#                 color: white; 
#                 padding: 10px; 
#                 font-size: 14px;
#                 border-radius: 5px;
#             }
#         """)
#         self.paralogs_file_button.setFixedSize(120, 40)  # Set button size
#         self.paralogs_file_button.clicked.connect(self.load_paralogs_file)
#         self.paralogs_layout.addWidget(self.paralogs_file_button)

#         self.paralogs_file_path_label = QLabel('', self)  # Label to show selected file path
#         self.paralogs_file_path_label.setFixedWidth(400)  # Fixed width for file path label
#         self.paralogs_file_path_label.setWordWrap(True)  # Allow word wrap if text exceeds width
#         self.paralogs_layout.addWidget(self.paralogs_file_path_label)

#         layout.addLayout(self.paralogs_layout)

#         # Create a layout for CDS file
#         self.cds_layout = QHBoxLayout()
#         self.cds_file_label = QLabel('Upload CDS File:', self)
#         self.cds_file_label.setFont(QFont("Arial", 14))  
#         self.cds_layout.addWidget(self.cds_file_label)

#         self.cds_file_button = QPushButton('Browse', self)
#         self.cds_file_button.setStyleSheet("""
#             QPushButton {
#                 background-color: #2C3E50; 
#                 color: white; 
#                 padding: 10px; 
#                 font-size: 14px;
#                 border-radius: 5px;
#             }
#         """)
#         self.cds_file_button.setFixedSize(120, 40)  # Set button size
#         self.cds_file_button.clicked.connect(self.load_cds_file)
#         self.cds_layout.addWidget(self.cds_file_button)
#         self.cds_file_path_label = QLabel('', self)  # Label to show selected file path
#         self.cds_file_path_label.setFixedWidth(400)  # Fixed width for file path label
#         self.cds_file_path_label.setWordWrap(True)  # Allow word wrap if text exceeds width
#         self.cds_layout.addWidget(self.cds_file_path_label)

#         layout.addLayout(self.cds_layout)

#         # Create a layout for Protein file
#         self.protein_layout = QHBoxLayout()
#         self.protein_file_label = QLabel('Upload Protein File:', self)
#         self.protein_file_label.setFont(QFont("Arial", 14))  
#         self.protein_layout.addWidget(self.protein_file_label)

#         self.protein_file_button = QPushButton('Browse', self)
#         self.protein_file_label.setFont(QFont("Arial", 14))  
#         self.protein_file_button.setStyleSheet("""
#             QPushButton {
#                 background-color: #2C3E50; 
#                 color: white; 
#                 padding: 10px; 
#                 font-size: 14px;
#                 border-radius: 5px;
#             }
#         """)
#         self.protein_file_button.setFixedSize(120, 40)  # Set button size
#         self.protein_file_button.clicked.connect(self.load_protein_file)
#         self.protein_layout.addWidget(self.protein_file_button)

#         self.protein_file_path_label = QLabel('', self)  # Label to show selected file path
#         self.protein_file_path_label.setFixedWidth(400)  # Fixed width for file path label
#         self.protein_file_path_label.setWordWrap(True)  # Allow word wrap if text exceeds width
#         self.protein_layout.addWidget(self.protein_file_path_label)
#         layout.addLayout(self.protein_layout)

#         # self.run_button = QPushButton('RUN Analysis', self)
#         # self.run_button.setStyleSheet("background-color:  #2C3E50; color: white;")  # Change color for run button
#         # self.run_button.clicked.connect(self.run_analysis)
#         # layout.addWidget(self.run_button)
#         self.run_button = QPushButton('RUN Analysis', self)
#         self.run_button.setStyleSheet("""
#             QPushButton {
#                 background-color: #2C3E50; 
#                 color: white; 
#                 padding: 8px; 
#                 font-size: 16px;
#                 border-radius: 8px;
#             }
#         """)
#         self.run_button.setFixedSize(200, 50)  # Increase the size of the Run button
#         self.run_button.clicked.connect(self.run_analysis)
#         layout.addWidget(self.run_button, alignment=Qt.AlignmentFlag.AlignCenter)


#         # Progress bar setup
#         self.progress_bar = QProgressBar(self)
#         self.progress_bar.setRange(0, 0)  # Indeterminate state (running)
#         self.progress_bar.setVisible(False)  # Hidden until the analysis starts
#         layout.addWidget(self.progress_bar)

#         self.download_button = QPushButton('Download', self)
#         self.download_button.setStyleSheet("""
#             QPushButton {
#                 background-color: #2C3E50; 
#                 color: white; 
#                 padding: 10px; 
#                 font-size: 16px;
#                 border-radius: 8px;
#             }
#         """)
#         self.download_button.setFixedSize(200, 50)  # Adjust button size
#         self.download_button.setEnabled(False)
#         self.download_button.clicked.connect(self.download_files)
#         layout.addWidget(self.download_button, alignment=Qt.AlignmentFlag.AlignCenter)


#         self.setLayout(layout)

#         self.paralogs_file_path = None
#         self.cds_file_path = None
#         self.protein_file_path = None
#         self.worker_thread = None

#     def load_paralogs_file(self):
#         file, _ = QFileDialog.getOpenFileName(self, 'Open Paralogs File', '', 'Text Files (*.txt);;All Files (*)')
#         if file:
#             self.paralogs_file_path = file
#             self.paralogs_file_path_label.setText(file)  # Update the label with the file path

#     def load_cds_file(self):
#         file, _ = QFileDialog.getOpenFileName(self, 'Open CDS File', '', 'FASTA Files (*.fa *.fasta);;All Files (*)')
#         if file:
#             self.cds_file_path = file
#             self.cds_file_path_label.setText(file)  # Update the label with the file path

#     def load_protein_file(self):
#         file, _ = QFileDialog.getOpenFileName(self, 'Open Protein File', '', 'FASTA Files (*.fa *.fasta);;All Files (*)')
#         if file:
#             self.protein_file_path = file
#             self.protein_file_path_label.setText(file)  # Update the label with the file path

#     def run_analysis(self):
#         if not self.paralogs_file_path or not self.cds_file_path or not self.protein_file_path:
#             QMessageBox.warning(self, 'Error', 'Please upload all required files before running the analysis.')
#             return

#         # Show the progress bar when analysis starts
#         self.progress_bar.setVisible(True)

#         self.worker_thread = Worker(self.paralogs_file_path, self.cds_file_path, self.protein_file_path)
#         self.worker_thread.progressChanged.connect(self.update_progress)
#         self.worker_thread.analysisFinished.connect(self.analysis_finished)
#         self.worker_thread.start()

#     def update_progress(self, value):
#         pass  # No need to update the value in indeterminate mode

#     def analysis_finished(self, success):
#         self.progress_bar.setVisible(False)  # Hide the progress bar after completion

#         if success:
#             QMessageBox.information(self, 'Success', 'Analysis completed successfully. Download the output files.')
#             self.download_button.setEnabled(True)
#         else:
#             QMessageBox.critical(self, 'Error', 
#                      'An error occurred during the analysis.\n'
#                      'Please ensure that the paralogs, CDS, and PEP files are properly matched.\n'
#                      'Please ensure that no special character in your file.\n'
#                      'Check the logs (kaks_error.log and output dir) in your home KAKS_Tool dir  for more details.')

#     # def download_files(self):
#     #     zip_file_path, _ = QFileDialog.getSaveFileName(self, 'Save Zip File', '', 'Zip Files (*.zip);;All Files (*)')
#     #     if zip_file_path:
#     #         if not zip_file_path.endswith('.zip'):
#     #             zip_file_path += '.zip'
#     #         output_zip_path = os.path.join("output", "output_files.zip")
#     #         os.rename(output_zip_path, zip_file_path)
#     #         QMessageBox.information(self, 'Download', f'Files have been saved to: {zip_file_path}')
#     def download_files(self):
#         try:
#         # Let user select the save location
#            zip_file_path, _ = QFileDialog.getSaveFileName(
#             self, 'Save Zip File', '', 'Zip Files (*.zip);;All Files (*)'
#         )
#            if zip_file_path:
#             # Ensure the file has a .zip extension
#               if not zip_file_path.endswith('.zip'):
#                   zip_file_path += '.zip'

#             # Define the source path
#               source_zip_path = os.path.join(os.path.expanduser("~"), "kAKS_Tool","output", "output_files.zip")

#             # Check if the source file exists
#               if not os.path.exists(source_zip_path):
#                   QMessageBox.warning(self, 'Error', f'The zip file does not exist: {source_zip_path}')
#                   return

#             # Copy the file to the selected location
#               shutil.copy(source_zip_path, zip_file_path)

#             # Inform the user of successful download
#               QMessageBox.information(self, 'Download', f'Files have been saved to: {zip_file_path}')
#         except Exception as e:
#            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = SequenceAnalysisApp()
#     ex.show()
#     sys.exit(app.exec())





import sys
import os
import subprocess
import logging
import zipfile
import shutil
from Bio import SeqIO
import pandas as pd
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, 
                               QLabel, QFileDialog, QProgressBar, QMessageBox, QLineEdit, QHBoxLayout,QSizePolicy,QSpacerItem)
from PySide6.QtCore import QThread, Signal, Qt, QSize
from PySide6.QtGui import QFont, QIcon

# Set up directories for logs and outputs
HOME_DIR = os.path.expanduser("~")
EXTERNAL_DIR = os.path.join(HOME_DIR, "KAKS_Tool")
LOGS_DIR = os.path.join(EXTERNAL_DIR, "logs")
OUTPUT_DIR = os.path.join(EXTERNAL_DIR, "output")

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "kaks_error.log")
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as log_file:
        log_file.truncate(0)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS, 'tools')
else:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tools'))

clustalw_path = os.path.join(base_dir, 'clustalw2.exe')
pal2nal_path = os.path.join(base_dir, 'pal2nal.exe')
axtconvertor_path = os.path.join(base_dir, 'AXTConvertor.exe')
kaks_calculator_path = os.path.join(base_dir, 'KaKs_Calculator.exe')

class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_lines(self):
        if not os.path.exists(self.file_path):
            logging.error(f"Error: File '{self.file_path}' does not exist.")
            return None
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return f.readlines()
        except UnicodeDecodeError as e:
            logging.error(f"Error: File '{self.file_path}' is not UTF-8 encoded. {e}")
            return None
        except Exception as e:
            logging.error(f"Error reading the file: {e}")
            return None

class SequenceExtractor:
    def __init__(self, fasta_file):
        self.fasta_file = fasta_file

    def extract_sequences(self, header_list, output_filename):
        extracted_sequences = []
        with open(self.fasta_file, "r") as fasta_in, open(output_filename, "w") as fasta_out:
            existing_headers = set()
            for record in SeqIO.parse(fasta_in, "fasta"):
                if record.id in header_list and record.id not in existing_headers:
                    SeqIO.write(record, fasta_out, "fasta")
                    existing_headers.add(record.id)
                    extracted_sequences.append(record)
        return extracted_sequences

class SequenceAligner:
    @staticmethod
    def run_clustalw(clustalw_path, input_file, output_file):
        cmd = f'"{clustalw_path}" -infile="{input_file}" -OUTFILE="{output_file}"'
        try:
            results = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
            if results.returncode != 0:
                logging.error(f"Error running command: {cmd}")
                logging.error(f"Error running ClustalW: {results.stderr}")
                return False
            logging.info("ClustalW execution successful.")
            return True
        except Exception as e:
            logging.error(f"Error running ClustalW: {e}")
            return False

class Pal2NalRunner:
    @staticmethod
    def run_pal2nal(input_alignment_file, input_cds_file, output_codon_alignment_file):
        command = [pal2nal_path, input_alignment_file, input_cds_file, "-nogap"]
        try:
            with open(output_codon_alignment_file, "w") as output_file:
                subprocess.run(command, stdout=output_file, stderr=subprocess.PIPE, check=True)
            logging.info("pal2nal execution successful.")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running command: {' '.join(command)}")
            logging.error(f"Error running pal2nal.pl: {e}")
            return False

class AxtConvertor:
    @staticmethod
    def run_axt_convertor(input_codon_alignment_file, output_axt_file):
        try:
            result_axt = subprocess.run([axtconvertor_path, input_codon_alignment_file, output_axt_file], capture_output=True, text=True, check=False)
            if result_axt.returncode != 0:
                logging.warning(f"AXTConvertor returned a non-zero exit code: {result_axt.returncode}")
            if result_axt.stderr:
                logging.error(f"Error running AXTConvertor: {result_axt.stderr}")
            if os.path.isfile(output_axt_file):
                logging.info("AXTConvertor execution successful.")
                return True
            else:
                logging.error("AXTConvertor failed to produce the output file.")
                return False
        except Exception as e:
            logging.error(f"Exception occurred while running AXTConvertor: {e}")
            return False

class KaksCalculator:
    @staticmethod
    def run_kaks_calculator(output_axt_file, output_kaks_file):
        try:
            result_kaks = subprocess.run([kaks_calculator_path, "-i", output_axt_file, "-o", output_kaks_file], capture_output=True, text=True, check=True)
            logging.info("KaKs_Calculator execution successful.")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running KaKs_Calculator: {e}")
            return False

class AnalysisRunner:
    def __init__(self, input_file, cds_fasta_file, pep_fasta_file, output_dir):
        self.input_file = input_file
        self.cds_fasta_file = cds_fasta_file
        self.pep_fasta_file = pep_fasta_file
        self.output_dir = output_dir

    def run_analysis(self, header_list):
        dfs_kaks = []
        lines = FileHandler(self.input_file).read_lines()
        if lines:
            num_lines = len(lines)
            if os.path.exists(self.output_dir):
                shutil.rmtree(self.output_dir)
            os.makedirs(self.output_dir, exist_ok=True)

            output_files = [generate_filename(self.output_dir, "row", i) for i in range(1, num_lines + 1)]
            column_1_files = [generate_filename(self.output_dir, f"{i}_row_column_1", i) for i in range(1, num_lines + 1)]
            column_2_files = [generate_filename(self.output_dir, f"{i}_row_column_2", i) for i in range(1, num_lines + 1)]
            pair_list_files = [generate_filename(self.output_dir, f"{i}_pairs.list", i) for i in range(1, num_lines + 1)]
            cds_files = [generate_filename(self.output_dir, f"{i}_p2_cds", i, extension=".fa") for i in range(1, num_lines + 1)]
            pep_files = [generate_filename(self.output_dir, f"{i}_p2_pep", i, extension=".fa") for i in range(1, num_lines + 1)]
            clustal_files = [os.path.join(self.output_dir, f"{i}_p2_pep.aln") for i in range(1, num_lines + 1)]
            pal2nal_files = [os.path.join(self.output_dir, f"{i}_p2_cod.aln") for i in range(1, num_lines + 1)]
            axt_files = [os.path.join(self.output_dir, f"{i}_p2.axt") for i in range(1, num_lines + 1)]
            kaks_files = [os.path.join(self.output_dir, f"{i}_p2.kaks") for i in range(1, num_lines + 1)]

            for i, line in enumerate(lines, 1):
                columns = line.split()
                if len(columns) < 2:
                    logging.warning(f"Line {i} has fewer than two columns.")
                    continue
                write_to_file(output_files[i - 1], line)
                write_to_file(column_1_files[i - 1], columns[0])
                write_to_file(column_2_files[i - 1], columns[1])
                write_to_file(pair_list_files[i - 1], f"{columns[0]}\n{columns[1]}")

            for i, query_file in enumerate(pair_list_files, 1):
                header_list = set()
                with open(query_file, "r") as f:
                    for line in f:
                        line = line.strip()
                        header_list.add(line)
                output_filename_cds = cds_files[i - 1]
                output_filename_pep = pep_files[i - 1]
                extracted_sequences_pep = SequenceExtractor(self.pep_fasta_file).extract_sequences(header_list, output_filename_pep)
                extracted_sequences_cds = SequenceExtractor(self.cds_fasta_file).extract_sequences(header_list, output_filename_cds)

                input_file = pep_files[i - 1]
                output_file = clustal_files[i - 1]
                if not SequenceAligner.run_clustalw(clustalw_path, input_file, output_file):
                    logging.error(f"Error running ClustalW for query file: {query_file}")

                input_alignment_file = clustal_files[i - 1]
                input_cds_file = cds_files[i - 1]
                output_codon_alignment_file = pal2nal_files[i - 1]
                if not Pal2NalRunner.run_pal2nal(input_alignment_file, input_cds_file, output_codon_alignment_file):
                    logging.error(f"Error running pal2nal.pl for query file: {query_file}")

                output_axt_file = axt_files[i - 1]
                if not AxtConvertor.run_axt_convertor(output_codon_alignment_file, output_axt_file):
                    logging.error(f"Error running Axt Convertor for query file: {query_file}")

                output_kaks_file = kaks_files[i - 1]
                if os.path.exists(output_axt_file):
                    if not KaksCalculator.run_kaks_calculator(output_axt_file, output_kaks_file):
                        logging.error(f"Error running Kaks Calculator for query file: {query_file}")
                    else:
                        df_kaks = pd.read_csv(output_kaks_file, sep='\t')
                        dfs_kaks.append(df_kaks)

            if dfs_kaks:
                combined_df = pd.concat(dfs_kaks)
                excel_filename = os.path.join(self.output_dir, "combined_kaks_data.xlsx")
                combined_df.to_excel(excel_filename, index=False)

                all_files = [self.input_file, self.cds_fasta_file, self.pep_fasta_file] + output_files + column_1_files + column_2_files + pair_list_files + cds_files + pep_files + clustal_files + pal2nal_files + axt_files + kaks_files

                zip_file_path = os.path.join(self.output_dir, "output_files.zip")
                with zipfile.ZipFile(zip_file_path, "w") as zipf:
                    for file_path in all_files:
                        if os.path.exists(file_path):
                            if file_path in kaks_files:
                                folder_name = "Kaks_Files"
                                arcname = os.path.join(folder_name, os.path.basename(file_path))
                            else:
                                arcname = os.path.basename(file_path)
                            zipf.write(file_path, arcname=arcname)
                        else:
                            logging.warning(f"File not found: {file_path}")
                with zipfile.ZipFile(zip_file_path, "a") as zipf:
                    excel_folder_name = "combined_kaks_data"
                    arcname = os.path.join(excel_folder_name, "combined_kaks_data.xlsx")
                    zipf.write(excel_filename, arcname=arcname)
                return True
        return False

def generate_filename(OUTPUT_DIR, base, i, extension=".txt"):
    return os.path.join(OUTPUT_DIR, f"{base}_{i}{extension}")

def write_to_file(filename, data, as_bytes=False):
    mode = "wb" if as_bytes else "w"
    try:
        with open(filename, mode, encoding=None if as_bytes else "utf-8") as f:
            if as_bytes:
                if isinstance(data, str):
                    data = data.encode("utf-8")
                f.write(data)
            else:
                f.write(data)
    except UnicodeEncodeError as e:
        logging.error(f"Error encoding data for file '{filename}': {e}")
    except Exception as e:
        logging.error(f"Error writing data to file '{filename}': {e}")

class Worker(QThread):
    progressChanged = Signal(int)
    analysisFinished = Signal(bool)

    def __init__(self, input_file, cds_file, pep_file, output_dir):
        super().__init__()
        self.input_file = input_file
        self.cds_file = cds_file
        self.pep_file = pep_file
        self.output_dir = output_dir
        self.process = None
        self.stop_requested = False

    def run(self):
        header_list = []
        analysis_runner = AnalysisRunner(self.input_file, self.cds_file, self.pep_file, self.output_dir)
        success = analysis_runner.run_analysis(header_list)
        if self.stop_requested:
            self.analysisFinished.emit(False)
            return
        self.analysisFinished.emit(success)

    def stop(self):
        self.stop_requested = True
        if self.process:
            self.process.terminate()

class SequenceAnalysisApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Genome Wide WorkBench")
        self.setWindowIcon(QIcon('src/image.png'))
        self.setGeometry(100, 100, 1000, 1000)

        self.header_label = QLabel("KaKs Analyzer")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.header_label.setStyleSheet("""
            QLabel {
                background-color: #2C3E50;
                color: white;
                padding: 10px;
                border-radius: 10px;
            }
        """)
        self.header_label.setFixedHeight(150)

        layout = QVBoxLayout()
        layout.addWidget(self.header_label)

        self.paralogs_layout = QHBoxLayout()
        self.paralogs_file_label = QLabel('Upload Paralogs File:', self)
        self.paralogs_file_label.setFont(QFont("Arial", 14))
        self.paralogs_layout.addWidget(self.paralogs_file_label)
        self.paralogs_file_button = QPushButton('Browse', self)
        self.paralogs_file_button.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
        self.paralogs_file_button.setFixedSize(120, 40)
        self.paralogs_file_button.clicked.connect(self.load_paralogs_file)
        self.paralogs_layout.addWidget(self.paralogs_file_button)
        self.paralogs_file_path_label = QLabel('', self)
        self.paralogs_file_path_label.setFixedWidth(400)
        self.paralogs_file_path_label.setWordWrap(True)
        self.paralogs_layout.addWidget(self.paralogs_file_path_label)
        layout.addLayout(self.paralogs_layout)

        self.cds_layout = QHBoxLayout()
        self.cds_file_label = QLabel('Upload CDS File:', self)
        self.cds_file_label.setFont(QFont("Arial", 14))
        self.cds_layout.addWidget(self.cds_file_label)
        self.cds_file_button = QPushButton('Browse', self)
        self.cds_file_button.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
        self.cds_file_button.setFixedSize(120, 40)
        self.cds_file_button.clicked.connect(self.load_cds_file)
        self.cds_layout.addWidget(self.cds_file_button)
        self.cds_file_path_label = QLabel('', self)
        self.cds_file_path_label.setFixedWidth(400)
        self.cds_file_path_label.setWordWrap(True)
        self.cds_layout.addWidget(self.cds_file_path_label)
        layout.addLayout(self.cds_layout)

        self.protein_layout = QHBoxLayout()
        self.protein_file_label = QLabel('Upload Protein File:', self)
        self.protein_file_label.setFont(QFont("Arial", 14))
        self.protein_layout.addWidget(self.protein_file_label)
        self.protein_file_button = QPushButton('Browse', self)
        self.protein_file_button.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
        self.protein_file_button.setFixedSize(120, 40)
        self.protein_file_button.clicked.connect(self.load_protein_file)
        self.protein_layout.addWidget(self.protein_file_button)
        self.protein_file_path_label = QLabel('', self)
        self.protein_file_path_label.setFixedWidth(400)
        self.protein_file_path_label.setWordWrap(True)
        self.protein_layout.addWidget(self.protein_file_path_label)
        layout.addLayout(self.protein_layout)

        self.output_layout = QHBoxLayout()
        self.output_dir_label = QLabel('Select Output Directory:', self)
        self.output_dir_label.setFont(QFont("Arial", 14))
        self.output_layout.addWidget(self.output_dir_label)
        self.output_dir_button = QPushButton('Browse', self)
        self.output_dir_button.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
        self.output_dir_button.setFixedSize(120, 40)
        self.output_dir_button.clicked.connect(self.select_output_dir)
        self.output_layout.addWidget(self.output_dir_button)
        self.output_dir_path_label = QLabel('', self)
        self.output_dir_path_label.setFixedWidth(400)
        self.output_dir_path_label.setWordWrap(True)
        self.output_layout.addWidget(self.output_dir_path_label)
        layout.addLayout(self.output_layout)

        self.run_button = QPushButton('RUN Analysis', self)
        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                padding: 8px;
                font-size: 16px;
                border-radius: 8px;
            }
        """)
        self.run_button.setFixedSize(200, 50)
        self.run_button.clicked.connect(self.run_analysis)
        layout.addWidget(self.run_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                padding: 8px;
                font-size: 16px;
                border-radius: 8px;
            }
            QPushButton:disabled {
                background-color: #A0A0A0;
            }
        """)
        self.stop_button.setFixedSize(200, 50)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_analysis)
        layout.addWidget(self.stop_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.download_button = QPushButton('Download', self)
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                padding: 10px;
                font-size: 16px;
                border-radius: 8px;
            }
        """)
        self.download_button.setFixedSize(200, 50)
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self.download_files)
        layout.addWidget(self.download_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

        self.paralogs_file_path = None
        self.cds_file_path = None
        self.protein_file_path = None
        self.output_dir = OUTPUT_DIR
        self.worker_thread = None

    def load_paralogs_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Open Paralogs File', '', 'Text Files (*.txt);;All Files (*)')
        if file:
            self.paralogs_file_path = file
            self.paralogs_file_path_label.setText(file)

    def load_cds_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Open CDS File', '', 'FASTA Files (*.fa *.fasta);;All Files (*)')
        if file:
            self.cds_file_path = file
            self.cds_file_path_label.setText(file)

    def load_protein_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Open Protein File', '', 'FASTA Files (*.fa *.fasta);;All Files (*)')
        if file:
            self.protein_file_path = file
            self.protein_file_path_label.setText(file)

    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Output Directory', '')
        if dir_path:
            self.output_dir = dir_path
            self.output_dir_path_label.setText(dir_path)

    def run_analysis(self):
        if not self.paralogs_file_path or not self.cds_file_path or not self.protein_file_path or not self.output_dir:
            QMessageBox.warning(self, 'Error', 'Please upload all required files and select an output directory before running the analysis.')
            return

        self.progress_bar.setVisible(True)
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.worker_thread = Worker(self.paralogs_file_path, self.cds_file_path, self.protein_file_path, self.output_dir)
        self.worker_thread.progressChanged.connect(self.update_progress)
        self.worker_thread.analysisFinished.connect(self.analysis_finished)
        self.worker_thread.start()

    def update_progress(self, value):
        pass

    def analysis_finished(self, success):
        self.progress_bar.setVisible(False)
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        if success:
            QMessageBox.information(self, 'Success', 'Analysis completed successfully. Download the output files.')
            self.download_button.setEnabled(True)
        else:
            QMessageBox.critical(self, 'Error', 
                     'An error occurred during the analysis.\n'
                     'Please ensure that the paralogs, CDS, and PEP files are properly matched.\n'
                     'Please ensure that no special character in your file.\n'
                     'Check the logs (kaks_error.log and output dir) in your home KAKS_Tool dir  for more details.')

    def download_files(self):
        try:
            zip_file_path, _ = QFileDialog.getSaveFileName(
                self, 'Save Zip File', '', 'Zip Files (*.zip);;All Files (*)'
            )
            if zip_file_path:
                if not zip_file_path.endswith('.zip'):
                    zip_file_path += '.zip'
                source_zip_path = os.path.join(self.output_dir, "output_files.zip")
                if not os.path.exists(source_zip_path):
                    QMessageBox.warning(self, 'Error', f'The zip file does not exist: {source_zip_path}')
                    return
                shutil.copy(source_zip_path, zip_file_path)
                QMessageBox.information(self, 'Download', f'Files have been saved to: {zip_file_path}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')

    def stop_analysis(self):
        if self.worker_thread:
            self.worker_thread.stop()
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        QMessageBox.information(self, 'Process Stopped', 'The KA/KS analysis process has been stopped.')
        self.download_button.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SequenceAnalysisApp()
    ex.show()
    sys.exit(app.exec())