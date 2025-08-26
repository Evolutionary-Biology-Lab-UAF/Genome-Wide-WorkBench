# # import sys
# # import os
# # import logging
# # from PySide6.QtWidgets import (
# #     QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
# #     QTextEdit, QComboBox, QFileDialog, QMessageBox
# # )
# # from PySide6.QtCore import Qt, QSize, QThread, Signal
# # from PySide6.QtGui import QFont, QIcon
# # import re
# # import pandas as pd
# # import csv
# # import subprocess

# # def setup_logging(output_directory):
# #     log_file = os.path.join(output_directory, "gene_density_map.log")
# #     logging.basicConfig(
# #         filename=log_file,
# #         level=logging.INFO,
# #         format='%(asctime)s - %(levelname)s - %(message)s'
# #     )
# #     return logging.getLogger()

# # def create_csv_from_txt(txt_file, species_name, output_directory):
# #     logger = setup_logging(output_directory)
# #     output_file = os.path.join(output_directory, f"{species_name}_bin.csv")
# #     headers = ["Chr", "Start", "End", "Value", "Bin1", "Bin2"]
    
# #     try:
# #         with open(output_file, mode='w', newline='') as file:
# #             writer = csv.writer(file)
# #             writer.writerow(headers)
# #     except PermissionError:
# #         logger.error(f"Permission denied: Cannot write to {output_file}. Please check the file permissions.")
# #         return None
# #     except Exception as e:
# #         logger.error(f"Error creating CSV file {output_file}: {e}")
# #         return None

# #     data = []
# #     with open(txt_file, mode='r') as file:
# #         for line in file:
# #             columns = line.strip().split()
# #             if len(columns) >= 4:
# #                 columns[0] = species_name
# #                 data.append(columns + ["", ""])
# #             else:
# #                 logger.warning(f"Skipping line due to unexpected column count: {line}")

# #     with open(output_file, mode='a', newline='') as file:
# #         writer = csv.writer(file)
# #         writer.writerows(data)

# #     try:
# #         df = pd.read_csv(output_file)
# #         df["Bin1"] = range(0, len(df))
# #         df["Bin2"] = range(1, len(df) + 1)
# #         df.to_csv(output_file, index=False)
# #     except Exception as e:
# #         logger.error(f"Error reading or writing CSV file: {e}")
# #         return None

# #     karyotype_file = os.path.join(output_directory, f"{species_name}_Karyotype.csv")
# #     try:
# #         karyotype_data = pd.DataFrame({
# #             "Chr": [species_name],
# #             "Start": [0],
# #             "End": [df["Bin1"].iloc[-1]]
# #         })
# #         karyotype_data.to_csv(karyotype_file, index=False)
# #     except Exception as e:
# #         logger.error(f"Error creating Karyotype file: {e}")
# #         return None

# #     try:
# #         df = df[df["Value"].astype(float) != 0]
# #     except ValueError as e:
# #         logger.error(f"Error converting 'Value' column to float: {e}")
# #         return None

# #     df["Start"] = df["Bin1"]
# #     df["End"] = df["Bin2"]
# #     df.drop(columns=["Bin1", "Bin2"], inplace=True)

# #     try:
# #         df.to_csv(output_file, index=False)
# #         logger.info(f"Processing completed. CSV saved at: {output_file}")
# #         logger.info(f"Karyotype saved at: {karyotype_file}")
# #     except Exception as e:
# #         logger.error(f"Error saving the final CSV file: {e}")
# #         return None

# #     return output_file, karyotype_file

# # def convert_count_to_txt(count_file):
# #     logger = logging.getLogger()
# #     txt_file = count_file.replace('.count', '.txt')
    
# #     try:
# #         with open(count_file, 'r') as infile, open(txt_file, 'w') as outfile:
# #             for line in infile:
# #                 outfile.write(line)
# #         logger.info(f"Successfully converted {count_file} to {txt_file}.")
# #         return txt_file
# #     except Exception as e:
# #         logger.error(f"Error converting file: {e}")
# #         return None

# # # def find_r_executable():
# # #     if getattr(sys, 'frozen', False):
# # #         # r_exe = os.path.join(sys._MEIPASS, "R", "bin", "Rscript.exe")
# # #         base_path = sys._MEIPASS
# # #         r_exe = os.path.join(base_path, "_internal", "src", "R", "bin", "Rscript.exe")
# # #     else:
# # #         r_exe = os.path.join(os.path.dirname(__file__), "R", "bin", "Rscript.exe")
# # #     if not os.path.exists(r_exe):
# # #         return None
# # #     return r_exe
# # # def find_r_executable():
# # #     logger = setup_logging(os.getcwd())
# # #     if getattr(sys, 'frozen', False):
# # #         # Adjust path to match the bundled structure (_internal/src/R)
# # #         base_path = sys._MEIPASS
# # #         r_exe = os.path.join(base_path, "_internal", "src", "R", "bin", "Rscript.exe")
# # #         logger.info(f"Checking R executable at: {r_exe}")
# # #     else:
# # #         r_exe = os.path.join(os.path.dirname(__file__), "R", "bin", "Rscript.exe")
# # #         logger.info(f"Development mode: Checking R executable at: {r_exe}")
# # #     if not os.path.exists(r_exe):
# # #         logger.error(f"R executable not found at: {r_exe}")
# # #         return None
# # #     return r_exe
# # def find_r_executable():
# #     logger = setup_logging(os.getcwd())
# #     if getattr(sys, 'frozen', False):
# #         base_path = sys._MEIPASS
# #         logger.info(f"sys._MEIPASS: {base_path}")
# #         r_exe = os.path.join(base_path, "R", "bin", "Rscript.exe")
# #         logger.info(f"Checking R executable at: {r_exe}")
# #         if not os.path.exists(r_exe):
# #             logger.error(f"R executable not found at: {r_exe}")
# #             return None
# #         return r_exe
# #     else:
# #         r_exe = os.path.join(os.path.dirname(__file__), "R", "bin", "Rscript.exe")
# #         logger.info(f"Development mode: Checking R executable at: {r_exe}")
# #         if not os.path.exists(r_exe):
# #             logger.error(f"R executable not found at: {r_exe}")
# #             return None
# #         return r_exe

# # def get_resource_path(relative_path):
# #     if hasattr(sys, '_MEIPASS'):
# #         return os.path.join(sys._MEIPASS, relative_path)
# #     return os.path.join(os.path.dirname(__file__), relative_path)

# # def process_overlap(bed_file, coord_file, output_directory, specie_name):
# #     logger = setup_logging(output_directory)
# #     output_file = os.path.join(output_directory, f"{specie_name}_chr.count")
# #     try:
# #         if not os.path.exists(bed_file):
# #             return f"Error: BED file not found: {bed_file}"
# #         if not os.path.exists(coord_file):
# #             return f"Error: Coordinate file not found: {coord_file}"

# #         r_exe = find_r_executable()
# #         if not r_exe:
# #             return "Error: Bundled R executable not found. Ensure R is included in the application folder."

# #         r_script = get_resource_path("intersect.R")
# #         if not os.path.exists(r_script):
# #             return f"Error: R script not found at {r_script}"

# #         r_home = os.path.dirname(os.path.dirname(r_exe))
# #         os.environ["R_HOME"] = r_home
# #         os.environ["R_LIBS"] = os.path.join(r_home, "library")

# #         result = subprocess.run(
# #             [r_exe, r_script, bed_file, coord_file, output_file],
# #             check=True, text=True, capture_output=True
# #         )

# #         logger.info("R script output: %s", result.stdout)
# #         logger.info("R script errors (if any): %s", result.stderr)

# #         if not os.path.exists(output_file):
# #             return f"Error: Output count file was not created: {output_file}"

# #         return output_file

# #     except subprocess.CalledProcessError as e:
# #         return f"Error executing R script: {e.stderr}"
# #     except Exception as e:
# #         return f"An unexpected error occurred: {e}"

# # def extract_attribute(attribute_column, selected_key):
# #     match = re.search(f"{selected_key}=([^;]+)", attribute_column, re.IGNORECASE)
# #     if match:
# #         return match.group(1)
# #     return None

# # def cut_columns_in_place(file_path, columns_to_keep):
# #     logger = logging.getLogger()
# #     try:
# #         with open(file_path, 'r') as f:
# #             lines = f.readlines()
# #         with open(file_path, 'w') as f:
# #             for line in lines:
# #                 if line.startswith('#'):
# #                     f.write(line)
# #                     continue
# #                 columns = line.strip().split('\t')
# #                 filtered_columns = [columns[i - 1] for i in columns_to_keep if i - 1 < len(columns)]
# #                 f.write('\t'.join(filtered_columns) + '\n')
# #     except Exception as e:
# #         logger.error(f"Error during column cutting: {e}")

# # def matching_genes(rgenes_file, genelist_file, output_file):
# #     logger = logging.getLogger()
# #     try:
# #         with open(rgenes_file, 'r') as rfile:
# #             rgenes_list = {line.strip() for line in rfile}
# #         with open(genelist_file, 'r') as gfile, open(output_file, 'w') as outfile:
# #             for line in gfile:
# #                 if line.startswith('#'):
# #                     continue
# #                 columns = line.strip().split('\t')
# #                 if len(columns) < 6:
# #                     continue
# #                 gene_id = columns[5]
# #                 if normalize_id_to_underscores(gene_id) in rgenes_list:
# #                     outfile.write(line)
# #         if os.path.getsize(output_file) == 0:
# #             return "Error: No matches found! Please ensure the last column of 'genelist' and 'rgenes.list' match."
# #         cut_columns_in_place(output_file, [1, 3, 4])
# #         return True
# #     except Exception as e:
# #         return f"Error matching genes: {e}"

# # def normalize_id_to_underscores(id_str):
# #     return id_str.replace('.', '_')

# # def process_gff(input_file, output_file, feature_type="mRNA", selected_attribute="ID"):
# #     logger = logging.getLogger()
# #     try:
# #         with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
# #             for line in infile:
# #                 if line.startswith('#'):
# #                     continue
# #                 columns = line.strip().split('\t')
# #                 if len(columns) < 9:
# #                     continue
# #                 if columns[2].lower() == feature_type.lower():
# #                     selected_columns = [columns[0], columns[2], columns[3], columns[4], columns[6]]
# #                     attribute_value = extract_attribute(columns[8], selected_attribute)
# #                     if attribute_value:
# #                         attribute_value = normalize_id_to_underscores(attribute_value)
# #                     selected_columns.append(attribute_value if attribute_value else "Unknown")
# #                     outfile.write('\t'.join(selected_columns) + '\n')
# #         return True
# #     except Exception as e:
# #         return f"Error processing GFF file: {e}"

# # def process_fasta(fasta_file, output_file):
# #     logger = logging.getLogger()
# #     try:
# #         with open(fasta_file, 'r') as infile, open(output_file, 'w') as outfile:
# #             for line in infile:
# #                 if line.startswith('>'):
# #                     header = line.strip().replace('>', '')
# #                     normalized_header = normalize_id_to_underscores(header)
# #                     outfile.write(f"{normalized_header}\n")
# #         return True
# #     except Exception as e:
# #         return f"Error processing FASTA file: {e}"

# # def process_fai(fai_file, output_directory, specie_name, window_size=5000):
# #     logger = setup_logging(output_directory)
# #     output_file = os.path.join(output_directory, f"{specie_name}_chr.size")
# #     try:
# #         with open(fai_file, 'r') as infile, open(output_file, 'w') as outfile:
# #             for line in infile:
# #                 columns = line.split('\t')
# #                 if len(columns) < 2:
# #                     raise ValueError(f"Invalid line in .fai file: {line.strip()}")
# #                 chr_name = columns[0]
# #                 chr_size = columns[1]
# #                 outfile.write(f"{chr_name}\t{chr_size}\n")
# #         if not os.path.exists(output_file):
# #             return f"Error: Output file was not created: {output_file}"
# #         r_exe = find_r_executable()
# #         if not r_exe:
# #             return "Error: Bundled R executable not found. Ensure R is included in the application folder."
# #         r_script = get_resource_path("make_windows.R")
# #         if not os.path.exists(r_script):
# #             return f"Error: R script not found at {r_script}"
# #         r_home = os.path.dirname(os.path.dirname(r_exe))
# #         os.environ["R_HOME"] = r_home
# #         os.environ["R_LIBS"] = os.path.join(r_home, "library")
# #         output_bed_file = os.path.join(output_directory, f"{specie_name}_windows.bed")
# #         result = subprocess.run(
# #             [r_exe, r_script, output_file, str(window_size), output_bed_file],
# #             check=True, text=True, capture_output=True
# #         )
# #         if not os.path.exists(output_bed_file):
# #             return f"Error: Output BED file was not created: {output_bed_file}"
# #         logger.info("R script executed successfully.")
# #         return True
# #     except ValueError as ve:
# #         return f"Error processing .fai file: {ve}"
# #     except FileNotFoundError:
# #         return f"Error: .fai file not found: {fai_file}"
# #     except subprocess.CalledProcessError as e:
# #         return f"Error executing R script: {e.stderr}"
# #     except Exception as e:
# #         return f"An unexpected error occurred: {e}"

# # class Worker(QThread):
# #     update_genelist_preview = Signal(str)
# #     update_fasta_preview = Signal(str)
# #     update_rgenes_coordlist_preview = Signal(str)
# #     finished = Signal(bool, str)

# #     def __init__(self, gff_file, fasta_file, fai_file, specie_name, output_directory, feature_type, selected_attribute):
# #         super().__init__()
# #         self.gff_file = gff_file
# #         self.fasta_file = fasta_file
# #         self.fai_file = fai_file
# #         self.specie_name = specie_name
# #         self.output_directory = output_directory
# #         self.feature_type = feature_type
# #         self.selected_attribute = selected_attribute
# #         self.process = None
# #         self.stop_requested = False
# #         self.logger = setup_logging(output_directory)

# #     def run(self):
# #         try:
# #             # Process GFF file
# #             gff_output_file = os.path.join(self.output_directory, "genelist")
# #             gff_result = process_gff(self.gff_file, gff_output_file, self.feature_type, self.selected_attribute)
# #             if gff_result is not True:
# #                 self.finished.emit(False, gff_result)
# #                 return
# #             self.update_genelist_preview.emit(self.get_preview(gff_output_file))
# #             if self.stop_requested:
# #                 self.finished.emit(False, "Process stopped by user.")
# #                 return

# #             # Process FASTA file
# #             fasta_output_file = os.path.join(self.output_directory, "rgenes.list")
# #             fasta_result = process_fasta(self.fasta_file, fasta_output_file)
# #             if fasta_result is not True:
# #                 self.finished.emit(False, fasta_result)
# #                 return
# #             self.update_fasta_preview.emit(self.get_preview(fasta_output_file))
# #             if self.stop_requested:
# #                 self.finished.emit(False, "Process stopped by user.")
# #                 return

# #             # Match genes
# #             rgenes_coord_output = os.path.join(self.output_directory, "rgenes_coord.list")
# #             grep_result = matching_genes(fasta_output_file, gff_output_file, rgenes_coord_output)
# #             if grep_result is not True:
# #                 self.finished.emit(False, grep_result)
# #                 return
# #             if os.path.getsize(rgenes_coord_output) == 0:
# #                 self.finished.emit(False, "No matching entries found. Please ensure the last columns of 'genelist' and 'rgenes.list' match.")
# #                 return
# #             self.update_rgenes_coordlist_preview.emit(self.get_preview(rgenes_coord_output))
# #             if self.stop_requested:
# #                 self.finished.emit(False, "Process stopped by user.")
# #                 return

# #             # Process FAI file
# #             fai_result = process_fai(self.fai_file, self.output_directory, self.specie_name)
# #             if fai_result is not True:
# #                 self.finished.emit(False, fai_result)
# #                 return
# #             if self.stop_requested:
# #                 self.finished.emit(False, "Process stopped by user.")
# #                 return

# #             # Process overlap
# #             bed_file = os.path.join(self.output_directory, f"{self.specie_name}_windows.bed")
# #             coord_file = os.path.join(self.output_directory, "rgenes_coord.list")
# #             r_exe = find_r_executable()
# #             if not r_exe:
# #                 self.finished.emit(False, "Error: Bundled R executable not found. Ensure R is included in the application folder.")
# #                 return
# #             r_script = get_resource_path("intersect.R")
# #             if not os.path.exists(r_script):
# #                 self.finished.emit(False, f"Error: R script not found at {r_script}")
# #                 return
# #             r_home = os.path.dirname(os.path.dirname(r_exe))
# #             os.environ["R_HOME"] = r_home
# #             os.environ["R_LIBS"] = os.path.join(r_home, "library")
# #             output_file = os.path.join(self.output_directory, f"{self.specie_name}_chr.count")
# #             cmd = [r_exe, r_script, bed_file, coord_file, output_file]
# #             self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
# #             stdout, stderr = self.process.communicate()
# #             if self.stop_requested:
# #                 self.finished.emit(False, "Process stopped by user.")
# #                 return
# #             if self.process.returncode != 0:
# #                 self.finished.emit(False, f"Error executing R script for overlap: {stderr}")
# #                 return
# #             if not os.path.exists(output_file):
# #                 self.finished.emit(False, f"Error: Output count file was not created: {output_file}")
# #                 return

# #             # Convert count to txt
# #             txt_file = convert_count_to_txt(output_file)
# #             if txt_file is None:
# #                 self.finished.emit(False, "Error: Conversion to .txt file failed.")
# #                 return
# #             if self.stop_requested:
# #                 self.finished.emit(False, "Process stopped by user.")
# #                 return

# #             # Create CSV
# #             csv_file, karyotype_file = create_csv_from_txt(txt_file, self.specie_name, self.output_directory)
# #             if not csv_file:
# #                 self.finished.emit(False, "Error creating CSV file.")
# #                 return
# #             if self.stop_requested:
# #                 self.finished.emit(False, "Process stopped by user.")
# #                 return

# #             # Generate ideogram
# #             r_script = get_resource_path("generate_ideogram.R")
# #             if not os.path.exists(r_script):
# #                 self.finished.emit(False, f"Error: R script not found at {r_script}")
# #                 return
# #             cmd = [r_exe, r_script, karyotype_file, csv_file, self.output_directory]
# #             self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
# #             stdout, stderr = self.process.communicate()
# #             if self.stop_requested:
# #                 self.finished.emit(False, "Process stopped by user.")
# #                 return
# #             if self.process.returncode != 0:
# #                 self.finished.emit(False, f"Error generating ideogram: {stderr}")
# #                 return

# #             self.finished.emit(True, f"Processing completed successfully!\nFiles saved in: {self.output_directory}")

# #         except Exception as e:
# #             self.finished.emit(False, f"Unexpected error: {str(e)}")

# #     def stop(self):
# #         """Request to stop the process."""
# #         self.stop_requested = True
# #         if self.process:
# #             self.process.terminate()

# #     def get_preview(self, file_path):
# #         preview_lines = []
# #         try:
# #             with open(file_path, 'r') as f:
# #                 for _ in range(5):
# #                     line = f.readline()
# #                     if not line:
# #                         break
# #                     preview_lines.append(line.strip())
# #         except Exception as e:
# #             return "Error reading preview."
# #         return "\n".join(preview_lines)

# # class GFFFilterApp(QMainWindow):
# #     def __init__(self):
# #         super().__init__()
# #         self.setWindowTitle("Genome Wide WorkBench")
# #         self.setWindowIcon(QIcon('src/image.png'))
# #         self.setGeometry(100, 100, 1000, 1000)

# #         self.header_label = QLabel("Gene Density Map")
# #         self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
# #         self.header_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
# #         self.header_label.setStyleSheet("""
# #             QLabel {
# #                 background-color: #2C3E50;
# #                 color: white;
# #                 padding: 10px;
# #                 border-radius: 10px;
# #             }
# #         """)

# #         layout = QVBoxLayout()
# #         layout.addWidget(self.header_label)

# #         self.file_layout = QHBoxLayout()
# #         self.input_label = QLabel("Select GFF3/GFF File:")
# #         self.file_layout.addWidget(self.input_label)
# #         self.input_button = QPushButton("Browse GFF3")
# #         self.input_button.setFixedSize(180, 50)
# #         self.input_button.setStyleSheet("""
# #             QPushButton {
# #                 font-size: 16px;
# #                 color: white;
# #                 background-color: #2C3E50;
# #                 border: none;
# #                 text-align: left;
# #                 padding: 5px 10px;
# #             }
# #             QPushButton:hover {
# #                 background-color: #34495E;
# #             }
# #             QPushButton:pressed {
# #                 background-color: #34495E;
# #             }
# #         """)
# #         self.input_button.clicked.connect(self.browse_input_file)
# #         self.file_layout.addWidget(self.input_button)
# #         layout.addLayout(self.file_layout)

# #         self.feature_layout = QHBoxLayout()
# #         self.feature_label = QLabel("Select Feature Type of GFF:")
# #         self.feature_layout.addWidget(self.feature_label)
# #         self.feature_combo = QComboBox()
# #         self.feature_combo.addItems(["mRNA", "gene", "CDS"])
# #         self.feature_combo.setFixedSize(180, 40)
# #         self.feature_layout.addWidget(self.feature_combo)
# #         layout.addLayout(self.feature_layout)

# #         self.attribute_layout = QHBoxLayout()
# #         self.attribute_label = QLabel("Select Attribute to Extract of GFF:")
# #         self.attribute_layout.addWidget(self.attribute_label)
# #         self.attribute_combo = QComboBox()
# #         self.attribute_combo.addItems(["ID", "Parent", "Name", "Custom"])
# #         self.attribute_combo.currentIndexChanged.connect(self.handle_custom_attribute)
# #         self.attribute_combo.setFixedSize(180, 50)
# #         self.attribute_layout.addWidget(self.attribute_combo)
# #         layout.addLayout(self.attribute_layout)

# #         self.custom_attribute_layout = QHBoxLayout()
# #         self.custom_attribute_label = QLabel("Enter Custom Attribute:")
# #         self.custom_attribute_input = QLineEdit()
# #         self.custom_attribute_label.hide()
# #         self.custom_attribute_input.hide()
# #         self.custom_attribute_input.setFixedSize(180, 50)
# #         self.custom_attribute_layout.addWidget(self.custom_attribute_label)
# #         self.custom_attribute_layout.addWidget(self.custom_attribute_input)
# #         layout.addLayout(self.custom_attribute_layout)

# #         self.fasta_layout = QHBoxLayout()
# #         self.fasta_label = QLabel("Select FASTA File to Extract Headers:")
# #         self.fasta_layout.addWidget(self.fasta_label)
# #         self.fasta_button = QPushButton("Browse FASTA...")
# #         self.fasta_button.setFixedSize(180, 50)
# #         self.fasta_button.setStyleSheet("""
# #             QPushButton {
# #                 font-size: 16px;
# #                 color: white;
# #                 background-color: #2C3E50;
# #                 border: none;
# #                 text-align: left;
# #                 padding: 5px 10px;
# #             }
# #             QPushButton:hover {
# #                 background-color: #34495E;
# #             }
# #             QPushButton:pressed {
# #                 background-color: #34495E;
# #             }
# #         """)
# #         self.fasta_button.clicked.connect(self.browse_fasta_file)
# #         self.fasta_layout.addWidget(self.fasta_button)
# #         layout.addLayout(self.fasta_layout)

# #         self.fai_layout = QHBoxLayout()
# #         self.fai_label = QLabel("Select index(.fai) File:")
# #         self.fai_layout.addWidget(self.fai_label)
# #         self.fai_button = QPushButton("Browse index(.fai)")
# #         self.fai_button.setFixedSize(180, 50)
# #         self.fai_button.setStyleSheet("""
# #             QPushButton {
# #                 font-size: 16px;
# #                 color: white;
# #                 background-color: #2C3E50;
# #                 border: none;
# #                 text-align: left;
# #                 padding: 5px 10px;
# #             }
# #             QPushButton:hover {
# #                 background-color: #34495E;
# #             }
# #             QPushButton:pressed {
# #                 background-color: #34495E;
# #             }
# #         """)
# #         self.fai_button.clicked.connect(self.browse_fai_file)
# #         self.fai_layout.addWidget(self.fai_button)
# #         layout.addLayout(self.fai_layout)

# #         self.specie_layout = QHBoxLayout()
# #         self.specie_label = QLabel("Enter Species Name:")
# #         self.specie_layout.addWidget(self.specie_label)
# #         self.specie_input = QLineEdit()
# #         self.specie_input.setFixedSize(180, 50)
# #         self.specie_layout.addWidget(self.specie_input)
# #         layout.addLayout(self.specie_layout)

# #         self.output_layout = QHBoxLayout()
# #         self.output_dir_label = QLabel("Select Output Directory:")
# #         self.output_layout.addWidget(self.output_dir_label)
# #         self.output_dir_button = QPushButton("Choose Directory")
# #         self.output_dir_button.setFixedSize(180, 50)
# #         self.output_dir_button.setStyleSheet("""
# #             QPushButton {
# #                 font-size: 16px;
# #                 color: white;
# #                 background-color: #2C3E50;
# #                 border: none;
# #                 text-align: left;
# #                 padding: 5px 10px;
# #             }
# #             QPushButton:hover {
# #                 background-color: #34495E;
# #             }
# #             QPushButton:pressed {
# #                 background-color: #34495E;
# #             }
# #         """)
# #         self.output_dir_button.clicked.connect(self.browse_output_directory)
# #         self.output_layout.addWidget(self.output_dir_button)
# #         layout.addLayout(self.output_layout)

# #         self.button_layout = QHBoxLayout()
# #         self.run_button = QPushButton("Submit")
# #         self.run_button.setFixedSize(200, 40)
# #         self.run_button.setStyleSheet("""
# #             QPushButton {
# #                 font-size: 16px;
# #                 color: white;
# #                 background-color: #2C3E50;
# #                 border: none;
# #                 text-align: left;
# #                 padding: 5px 10px;
# #             }
# #             QPushButton:hover {
# #                 background-color: #34495E;
# #             }
# #             QPushButton:pressed {
# #                 background-color: #34495E;
# #             }
# #         """)
# #         self.run_button.clicked.connect(self.run_filter)
# #         self.button_layout.addWidget(self.run_button)

# #         self.stop_button = QPushButton("Stop")
# #         self.stop_button.setFixedSize(200, 40)
# #         self.stop_button.setEnabled(False)
# #         self.stop_button.setStyleSheet("""
# #             QPushButton {
# #                 font-size: 16px;
# #                 color: white;
# #                 background-color: #2C3E50;
# #                 border: none;
# #                 text-align: left;
# #                 padding: 5px 10px;
# #             }
# #             QPushButton:disabled {
# #                 background-color: #A0A0A0;
# #             }
# #             QPushButton:hover {
# #                 background-color: #34495E;
# #             }
# #             QPushButton:pressed {
# #                 background-color: #34495E;
# #             }
# #         """)
# #         self.stop_button.clicked.connect(self.stop_process)
# #         self.button_layout.addWidget(self.stop_button)

# #         layout.addLayout(self.button_layout)

# #         self.genelist_preview_label = QLabel("Genelist Preview:")
# #         layout.addWidget(self.genelist_preview_label)
# #         self.genelist_preview = QTextEdit()
# #         self.genelist_preview.setReadOnly(True)
# #         layout.addWidget(self.genelist_preview)

# #         self.fasta_preview_label = QLabel("FASTA Headers Preview:")
# #         layout.addWidget(self.fasta_preview_label)
# #         self.fasta_preview = QTextEdit()
# #         self.fasta_preview.setReadOnly(True)
# #         layout.addWidget(self.fasta_preview)

# #         self.rgenes_coordlist_preview_label = QLabel("Rgenes_coordlist Preview:")
# #         layout.addWidget(self.rgenes_coordlist_preview_label)
# #         self.rgenes_coordlist_preview = QTextEdit()
# #         self.rgenes_coordlist_preview.setReadOnly(True)
# #         layout.addWidget(self.rgenes_coordlist_preview)

# #         container = QWidget()
# #         container.setLayout(layout)
# #         self.setCentralWidget(container)

# #         self.gff_file = None
# #         self.output_directory = None
# #         self.fasta_file = None
# #         self.fai_file = None
# #         self.specie_name = None
# #         self.worker = None

# #     def browse_input_file(self):
# #         file_dialog = QFileDialog()
# #         file_paths, _ = file_dialog.getOpenFileNames(self, "Select GFF3 Files", "", "GFF3 Files (*.gff3);;All Files (*)")
# #         if file_paths:
# #             self.gff_file = file_paths[0]
# #             self.input_label.setText(f"Selected GFF3 File: {self.gff_file}")

# #     def browse_output_directory(self):
# #         dir_dialog = QFileDialog()
# #         dir_path = dir_dialog.getExistingDirectory(self, "Select Output Directory")
# #         if dir_path:
# #             self.output_directory = dir_path
# #             self.output_dir_label.setText(f"Selected Directory: {dir_path}")

# #     def browse_fasta_file(self):
# #         file_dialog = QFileDialog()
# #         file_path, _ = file_dialog.getOpenFileName(self, "Select FASTA File", "", "FASTA Files (*.fasta);;All Files (*)")
# #         if file_path:
# #             self.fasta_file = file_path
# #             self.fasta_label.setText(f"Selected FASTA File: {file_path}")

# #     def browse_fai_file(self):
# #         file_dialog = QFileDialog()
# #         file_path, _ = file_dialog.getOpenFileName(self, "Select .fai File", "", "FAI Files (*.fai)")
# #         if file_path:
# #             self.fai_file = file_path
# #             self.fai_label.setText(f"Selected .fai File: {file_path}")

# #     def handle_custom_attribute(self):
# #         if self.attribute_combo.currentText() == "Custom":
# #             self.custom_attribute_label.show()
# #             self.custom_attribute_input.show()
# #         else:
# #             self.custom_attribute_label.hide()
# #             self.custom_attribute_input.hide()

# #     def run_filter(self):
# #         if not all([self.gff_file, self.fasta_file, self.output_directory, self.fai_file, self.specie_input.text()]):
# #             QMessageBox.critical(self, "Error", "Please ensure all inputs are selected.")
# #             return

# #         QMessageBox.information(self, "Analysis Started", "Your analysis is running.")

# #         selected_feature = self.feature_combo.currentText()
# #         selected_attribute = self.attribute_combo.currentText()
# #         if selected_attribute == "Custom":
# #             selected_attribute = self.custom_attribute_input.text()

# #         specie_name = self.specie_input.text()

# #         self.worker = Worker(self.gff_file, self.fasta_file, self.fai_file, specie_name, self.output_directory, selected_feature, selected_attribute)
# #         self.worker.update_genelist_preview.connect(self.genelist_preview.setPlainText)
# #         self.worker.update_fasta_preview.connect(self.fasta_preview.setPlainText)
# #         self.worker.update_rgenes_coordlist_preview.connect(self.rgenes_coordlist_preview.setPlainText)
# #         self.worker.finished.connect(self.on_finished)
# #         self.worker.start()
# #         self.stop_button.setEnabled(True)

# #     def stop_process(self):
# #         if self.worker:
# #             self.worker.stop()
# #         self.stop_button.setEnabled(False)

# #     def on_finished(self, success, message):
# #         self.stop_button.setEnabled(False)
# #         if success:
# #             QMessageBox.information(self, "Analysis Completed", message)
# #         else:
# #             QMessageBox.critical(self, "Analysis Completed", message)

# #     def closeEvent(self, event):
# #         msg_box = QMessageBox(self)
# #         msg_box.setWindowTitle("Exit Application")
# #         msg_box.setText("Are you sure you want to quit the application?")
# #         msg_box.setIcon(QMessageBox.Question)
# #         yes_button = msg_box.addButton("Yes", QMessageBox.YesRole)
# #         minimize_button = msg_box.addButton("Minimize", QMessageBox.NoRole)
# #         no_button = msg_box.addButton("No", QMessageBox.RejectRole)
# #         msg_box.exec()
# #         if msg_box.clickedButton() == yes_button:
# #             event.accept()
# #         elif msg_box.clickedButton() == minimize_button:
# #             event.ignore()
# #             self.showMinimized()
# #         else:
# #             event.ignore()

# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     window = GFFFilterApp()
# #     window.show()
# #     sys.exit(app.exec())
# import sys
# import os
# import logging
# from PySide6.QtWidgets import (
#     QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
#     QTextEdit, QComboBox, QFileDialog, QMessageBox
# )
# from PySide6.QtCore import Qt, QSize, QThread, Signal
# from PySide6.QtGui import QFont, QIcon
# import re
# import pandas as pd
# import csv
# import subprocess

# def setup_logging(output_directory):
#     log_file = os.path.join(output_directory, "gene_density_map.log")
#     logging.basicConfig(
#         filename=log_file,
#         level=logging.INFO,
#         format='%(asctime)s - %(levelname)s - %(message)s'
#     )
#     return logging.getLogger()

# def create_csv_from_txt(txt_file, species_name, output_directory):
#     logger = setup_logging(output_directory)
#     output_file = os.path.join(output_directory, f"{species_name}_bin.csv")
#     headers = ["Chr", "Start", "End", "Value", "Bin1", "Bin2"]
    
#     try:
#         with open(output_file, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(headers)
#     except PermissionError:
#         logger.error(f"Permission denied: Cannot write to {output_file}. Please check the file permissions.")
#         return None
#     except Exception as e:
#         logger.error(f"Error creating CSV file {output_file}: {e}")
#         return None

#     data = []
#     with open(txt_file, mode='r') as file:
#         for line in file:
#             columns = line.strip().split()
#             if len(columns) >= 4:
#                 columns[0] = species_name
#                 data.append(columns + ["", ""])
#             else:
#                 logger.warning(f"Skipping line due to unexpected column count: {line}")

#     with open(output_file, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerows(data)

#     try:
#         df = pd.read_csv(output_file)
#         df["Bin1"] = range(0, len(df))
#         df["Bin2"] = range(1, len(df) + 1)
#         df.to_csv(output_file, index=False)
#     except Exception as e:
#         logger.error(f"Error reading or writing CSV file: {e}")
#         return None

#     karyotype_file = os.path.join(output_directory, f"{species_name}_Karyotype.csv")
#     try:
#         karyotype_data = pd.DataFrame({
#             "Chr": [species_name],
#             "Start": [0],
#             "End": [df["Bin1"].iloc[-1]]
#         })
#         karyotype_data.to_csv(karyotype_file, index=False)
#     except Exception as e:
#         logger.error(f"Error creating Karyotype file: {e}")
#         return None

#     try:
#         df = df[df["Value"].astype(float) != 0]
#     except ValueError as e:
#         logger.error(f"Error converting 'Value' column to float: {e}")
#         return None

#     df["Start"] = df["Bin1"]
#     df["End"] = df["Bin2"]
#     df.drop(columns=["Bin1", "Bin2"], inplace=True)

#     try:
#         df.to_csv(output_file, index=False)
#         logger.info(f"Processing completed. CSV saved at: {output_file}")
#         logger.info(f"Karyotype saved at: {karyotype_file}")
#     except Exception as e:
#         logger.error(f"Error saving the final CSV file: {e}")
#         return None

#     return output_file, karyotype_file

# def convert_count_to_txt(count_file):
#     logger = logging.getLogger()
#     txt_file = count_file.replace('.count', '.txt')
    
#     try:
#         with open(count_file, 'r') as infile, open(txt_file, 'w') as outfile:
#             for line in infile:
#                 outfile.write(line)
#         logger.info(f"Successfully converted {count_file} to {txt_file}.")
#         return txt_file
#     except Exception as e:
#         logger.error(f"Error converting file: {e}")
#         return None
# # old
# # def find_r_executable():
# #     if getattr(sys, 'frozen', False):
# #         r_exe = os.path.join(sys._MEIPASS, "R", "bin", "Rscript.exe")
# #     else:
# #         r_exe = os.path.join(os.path.dirname(__file__), "R", "bin", "Rscript.exe")
# #     if not os.path.exists(r_exe):
# #         return None
# #     return r_exe
# def find_r_executable():
#     logger = logging.getLogger()
#     if getattr(sys, 'frozen', False):
#         base_path = sys._MEIPASS
#         possible_paths = [
#             os.path.normpath(os.path.join(base_path, "src", "R", "bin", "Rscript.exe")),  # Expected path
#             os.path.normpath(os.path.join(base_path, "R", "bin", "Rscript.exe")),  # Fallback
#             os.path.normpath(os.path.join(os.path.dirname(sys.executable), "src", "R", "bin", "Rscript.exe")),
#             os.path.normpath(os.path.join(os.path.dirname(sys.executable), "R", "bin", "Rscript.exe"))
#         ]
#     else:
#         base_path = os.path.dirname(__file__)
#         possible_paths = [
#             os.path.normpath(os.path.join(base_path, "R", "bin", "Rscript.exe"))
#         ]
#     logger.info(f"Base path: {base_path}")
#     logger.info(f"Executable directory: {os.path.dirname(sys.executable)}")
    
#     for r_exe in possible_paths:
#         logger.info(f"Checking R executable at: {r_exe}")
#         if os.path.exists(r_exe):
#             logger.info(f"Found R executable at: {r_exe}")
#             return r_exe
#         logger.error(f"R executable not found at: {r_exe}")
#         r_dir = os.path.dirname(r_exe)
#         if os.path.exists(r_dir):
#             logger.info(f"Contents of {r_dir}: {os.listdir(r_dir)}")
#         else:
#             logger.error(f"Directory does not exist: {r_dir}")
    
#     # Log entire sys._MEIPASS structure
#     if getattr(sys, 'frozen', False):
#         logger.info(f"Listing all files in sys._MEIPASS: {base_path}")
#         for root, dirs, files in os.walk(base_path):
#             for file in files:
#                 logger.info(f"Found file: {os.path.join(root, file)}")
    
#     logger.error("No R executable found in any possible paths")
#     return None
# def get_resource_path(relative_path):
#     if hasattr(sys, '_MEIPASS'):
#         return os.path.join(sys._MEIPASS, relative_path)
#     return os.path.join(os.path.dirname(__file__), relative_path)

# def process_overlap(bed_file, coord_file, output_directory, specie_name):
#     logger = setup_logging(output_directory)
#     output_file = os.path.join(output_directory, f"{specie_name}_chr.count")
#     try:
#         if not os.path.exists(bed_file):
#             return f"Error: BED file not found: {bed_file}"
#         if not os.path.exists(coord_file):
#             return f"Error: Coordinate file not found: {coord_file}"

#         r_exe = find_r_executable()
#         if not r_exe:
#             return "Error: Bundled R executable not found. Ensure R is included in the application folder."

#         r_script = get_resource_path("intersect.R")
#         if not os.path.exists(r_script):
#             return f"Error: R script not found at {r_script}"

#         r_home = os.path.dirname(os.path.dirname(r_exe))
#         os.environ["R_HOME"] = r_home
#         os.environ["R_LIBS"] = os.path.join(r_home, "library")

#         result = subprocess.run(
#             [r_exe, r_script, bed_file, coord_file, output_file],
#             check=True, text=True, capture_output=True
#         )

#         logger.info("R script output: %s", result.stdout)
#         logger.info("R script errors (if any): %s", result.stderr)

#         if not os.path.exists(output_file):
#             return f"Error: Output count file was not created: {output_file}"

#         return output_file

#     except subprocess.CalledProcessError as e:
#         return f"Error executing R script: {e.stderr}"
#     except Exception as e:
#         return f"An unexpected error occurred: {e}"

# def extract_attribute(attribute_column, selected_key):
#     match = re.search(f"{selected_key}=([^;]+)", attribute_column, re.IGNORECASE)
#     if match:
#         return match.group(1)
#     return None

# def cut_columns_in_place(file_path, columns_to_keep):
#     logger = logging.getLogger()
#     try:
#         with open(file_path, 'r') as f:
#             lines = f.readlines()
#         with open(file_path, 'w') as f:
#             for line in lines:
#                 if line.startswith('#'):
#                     f.write(line)
#                     continue
#                 columns = line.strip().split('\t')
#                 filtered_columns = [columns[i - 1] for i in columns_to_keep if i - 1 < len(columns)]
#                 f.write('\t'.join(filtered_columns) + '\n')
#     except Exception as e:
#         logger.error(f"Error during column cutting: {e}")

# def matching_genes(rgenes_file, genelist_file, output_file):
#     logger = logging.getLogger()
#     try:
#         with open(rgenes_file, 'r') as rfile:
#             rgenes_list = {line.strip() for line in rfile}
#         with open(genelist_file, 'r') as gfile, open(output_file, 'w') as outfile:
#             for line in gfile:
#                 if line.startswith('#'):
#                     continue
#                 columns = line.strip().split('\t')
#                 if len(columns) < 6:
#                     continue
#                 gene_id = columns[5]
#                 if normalize_id_to_underscores(gene_id) in rgenes_list:
#                     outfile.write(line)
#         if os.path.getsize(output_file) == 0:
#             return "Error: No matches found! Please ensure the last column of 'genelist' and 'rgenes.list' match."
#         cut_columns_in_place(output_file, [1, 3, 4])
#         return True
#     except Exception as e:
#         return f"Error matching genes: {e}"

# def normalize_id_to_underscores(id_str):
#     return id_str.replace('.', '_')

# def process_gff(input_file, output_file, feature_type="mRNA", selected_attribute="ID"):
#     logger = logging.getLogger()
#     try:
#         with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
#             for line in infile:
#                 if line.startswith('#'):
#                     continue
#                 columns = line.strip().split('\t')
#                 if len(columns) < 9:
#                     continue
#                 if columns[2].lower() == feature_type.lower():
#                     selected_columns = [columns[0], columns[2], columns[3], columns[4], columns[6]]
#                     attribute_value = extract_attribute(columns[8], selected_attribute)
#                     if attribute_value:
#                         attribute_value = normalize_id_to_underscores(attribute_value)
#                     selected_columns.append(attribute_value if attribute_value else "Unknown")
#                     outfile.write('\t'.join(selected_columns) + '\n')
#         return True
#     except Exception as e:
#         return f"Error processing GFF file: {e}"

# def process_fasta(fasta_file, output_file):
#     logger = logging.getLogger()
#     try:
#         with open(fasta_file, 'r') as infile, open(output_file, 'w') as outfile:
#             for line in infile:
#                 if line.startswith('>'):
#                     header = line.strip().replace('>', '')
#                     normalized_header = normalize_id_to_underscores(header)
#                     outfile.write(f"{normalized_header}\n")
#         return True
#     except Exception as e:
#         return f"Error processing FASTA file: {e}"

# def process_fai(fai_file, output_directory, specie_name, window_size=5000):
#     logger = setup_logging(output_directory)
#     output_file = os.path.join(output_directory, f"{specie_name}_chr.size")
#     try:
#         with open(fai_file, 'r') as infile, open(output_file, 'w') as outfile:
#             for line in infile:
#                 columns = line.split('\t')
#                 if len(columns) < 2:
#                     raise ValueError(f"Invalid line in .fai file: {line.strip()}")
#                 chr_name = columns[0]
#                 chr_size = columns[1]
#                 outfile.write(f"{chr_name}\t{chr_size}\n")
#         if not os.path.exists(output_file):
#             return f"Error: Output file was not created: {output_file}"
#         r_exe = find_r_executable()
#         if not r_exe:
#             return "Error: Bundled R executable not found. Ensure R is included in the application folder."
#         r_script = get_resource_path("make_windows.R")
#         if not os.path.exists(r_script):
#             return f"Error: R script not found at {r_script}"
#         r_home = os.path.dirname(os.path.dirname(r_exe))
#         os.environ["R_HOME"] = r_home
#         os.environ["R_LIBS"] = os.path.join(r_home, "library")
#         output_bed_file = os.path.join(output_directory, f"{specie_name}_windows.bed")
#         result = subprocess.run(
#             [r_exe, r_script, output_file, str(window_size), output_bed_file],
#             check=True, text=True, capture_output=True
#         )
#         if not os.path.exists(output_bed_file):
#             return f"Error: Output BED file was not created: {output_bed_file}"
#         logger.info("R script executed successfully.")
#         return True
#     except ValueError as ve:
#         return f"Error processing .fai file: {ve}"
#     except FileNotFoundError:
#         return f"Error: .fai file not found: {fai_file}"
#     except subprocess.CalledProcessError as e:
#         return f"Error executing R script: {e.stderr}"
#     except Exception as e:
#         return f"An unexpected error occurred: {e}"

# class Worker(QThread):
#     update_genelist_preview = Signal(str)
#     update_fasta_preview = Signal(str)
#     update_rgenes_coordlist_preview = Signal(str)
#     finished = Signal(bool, str)

#     def __init__(self, gff_file, fasta_file, fai_file, specie_name, output_directory, feature_type, selected_attribute):
#         super().__init__()
#         self.gff_file = gff_file
#         self.fasta_file = fasta_file
#         self.fai_file = fai_file
#         self.specie_name = specie_name
#         self.output_directory = output_directory
#         self.feature_type = feature_type
#         self.selected_attribute = selected_attribute
#         self.process = None
#         self.stop_requested = False
#         self.logger = setup_logging(output_directory)

#     def run(self):
#         try:
#             # Process GFF file
#             gff_output_file = os.path.join(self.output_directory, "genelist")
#             gff_result = process_gff(self.gff_file, gff_output_file, self.feature_type, self.selected_attribute)
#             if gff_result is not True:
#                 self.finished.emit(False, gff_result)
#                 return
#             self.update_genelist_preview.emit(self.get_preview(gff_output_file))
#             if self.stop_requested:
#                 self.finished.emit(False, "Process stopped by user.")
#                 return

#             # Process FASTA file
#             fasta_output_file = os.path.join(self.output_directory, "rgenes.list")
#             fasta_result = process_fasta(self.fasta_file, fasta_output_file)
#             if fasta_result is not True:
#                 self.finished.emit(False, fasta_result)
#                 return
#             self.update_fasta_preview.emit(self.get_preview(fasta_output_file))
#             if self.stop_requested:
#                 self.finished.emit(False, "Process stopped by user.")
#                 return

#             # Match genes
#             rgenes_coord_output = os.path.join(self.output_directory, "rgenes_coord.list")
#             grep_result = matching_genes(fasta_output_file, gff_output_file, rgenes_coord_output)
#             if grep_result is not True:
#                 self.finished.emit(False, grep_result)
#                 return
#             if os.path.getsize(rgenes_coord_output) == 0:
#                 self.finished.emit(False, "No matching entries found. Please ensure the last columns of 'genelist' and 'rgenes.list' match.")
#                 return
#             self.update_rgenes_coordlist_preview.emit(self.get_preview(rgenes_coord_output))
#             if self.stop_requested:
#                 self.finished.emit(False, "Process stopped by user.")
#                 return

#             # Process FAI file
#             fai_result = process_fai(self.fai_file, self.output_directory, self.specie_name)
#             if fai_result is not True:
#                 self.finished.emit(False, fai_result)
#                 return
#             if self.stop_requested:
#                 self.finished.emit(False, "Process stopped by user.")
#                 return

#             # Process overlap
#             bed_file = os.path.join(self.output_directory, f"{self.specie_name}_windows.bed")
#             coord_file = os.path.join(self.output_directory, "rgenes_coord.list")
#             r_exe = find_r_executable()
#             if not r_exe:
#                 self.finished.emit(False, "Error: Bundled R executable not found. Ensure R is included in the application folder.")
#                 return
#             r_script = get_resource_path("intersect.R")
#             if not os.path.exists(r_script):
#                 self.finished.emit(False, f"Error: R script not found at {r_script}")
#                 return
#             r_home = os.path.dirname(os.path.dirname(r_exe))
#             os.environ["R_HOME"] = r_home
#             os.environ["R_LIBS"] = os.path.join(r_home, "library")
#             output_file = os.path.join(self.output_directory, f"{self.specie_name}_chr.count")
#             cmd = [r_exe, r_script, bed_file, coord_file, output_file]
#             self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#             stdout, stderr = self.process.communicate()
#             if self.stop_requested:
#                 self.finished.emit(False, "Process stopped by user.")
#                 return
#             if self.process.returncode != 0:
#                 self.finished.emit(False, f"Error executing R script for overlap: {stderr}")
#                 return
#             if not os.path.exists(output_file):
#                 self.finished.emit(False, f"Error: Output count file was not created: {output_file}")
#                 return

#             # Convert count to txt
#             txt_file = convert_count_to_txt(output_file)
#             if txt_file is None:
#                 self.finished.emit(False, "Error: Conversion to .txt file failed.")
#                 return
#             if self.stop_requested:
#                 self.finished.emit(False, "Process stopped by user.")
#                 return

#             # Create CSV
#             csv_file, karyotype_file = create_csv_from_txt(txt_file, self.specie_name, self.output_directory)
#             if not csv_file:
#                 self.finished.emit(False, "Error creating CSV file.")
#                 return
#             if self.stop_requested:
#                 self.finished.emit(False, "Process stopped by user.")
#                 return

#             # Generate ideogram
#             r_script = get_resource_path("generate_ideogram.R")
#             if not os.path.exists(r_script):
#                 self.finished.emit(False, f"Error: R script not found at {r_script}")
#                 return
#             cmd = [r_exe, r_script, karyotype_file, csv_file, self.output_directory]
#             self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#             stdout, stderr = self.process.communicate()
#             if self.stop_requested:
#                 self.finished.emit(False, "Process stopped by user.")
#                 return
#             if self.process.returncode != 0:
#                 self.finished.emit(False, f"Error generating ideogram: {stderr}")
#                 return

#             self.finished.emit(True, f"Processing completed successfully!\nFiles saved in: {self.output_directory}")

#         except Exception as e:
#             self.finished.emit(False, f"Unexpected error: {str(e)}")

#     def stop(self):
#         """Request to stop the process."""
#         self.stop_requested = True
#         if self.process:
#             self.process.terminate()

#     def get_preview(self, file_path):
#         preview_lines = []
#         try:
#             with open(file_path, 'r') as f:
#                 for _ in range(5):
#                     line = f.readline()
#                     if not line:
#                         break
#                     preview_lines.append(line.strip())
#         except Exception as e:
#             return "Error reading preview."
#         return "\n".join(preview_lines)

# class GFFFilterApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Genome Wide WorkBench")
#         self.setWindowIcon(QIcon('src/image.png'))
#         self.setGeometry(100, 100, 1000, 1000)

#         self.header_label = QLabel("Gene Density Map")
#         self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.header_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
#         self.header_label.setStyleSheet("""
#             QLabel {
#                 background-color: #2C3E50;
#                 color: white;
#                 padding: 10px;
#                 border-radius: 10px;
#             }
#         """)

#         layout = QVBoxLayout()
#         layout.addWidget(self.header_label)

#         self.file_layout = QHBoxLayout()
#         self.input_label = QLabel("Select GFF3/GFF File:")
#         self.file_layout.addWidget(self.input_label)
#         self.input_button = QPushButton("Browse GFF3")
#         self.input_button.setFixedSize(180, 50)
#         self.input_button.setStyleSheet("""
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
#         self.input_button.clicked.connect(self.browse_input_file)
#         self.file_layout.addWidget(self.input_button)
#         layout.addLayout(self.file_layout)

#         self.feature_layout = QHBoxLayout()
#         self.feature_label = QLabel("Select Feature Type of GFF:")
#         self.feature_layout.addWidget(self.feature_label)
#         self.feature_combo = QComboBox()
#         self.feature_combo.addItems(["mRNA", "gene", "CDS"])
#         self.feature_combo.setFixedSize(180, 40)
#         self.feature_layout.addWidget(self.feature_combo)
#         layout.addLayout(self.feature_layout)

#         self.attribute_layout = QHBoxLayout()
#         self.attribute_label = QLabel("Select Attribute to Extract of GFF:")
#         self.attribute_layout.addWidget(self.attribute_label)
#         self.attribute_combo = QComboBox()
#         self.attribute_combo.addItems(["ID", "Parent", "Name", "Custom"])
#         self.attribute_combo.currentIndexChanged.connect(self.handle_custom_attribute)
#         self.attribute_combo.setFixedSize(180, 50)
#         self.attribute_layout.addWidget(self.attribute_combo)
#         layout.addLayout(self.attribute_layout)

#         self.custom_attribute_layout = QHBoxLayout()
#         self.custom_attribute_label = QLabel("Enter Custom Attribute:")
#         self.custom_attribute_input = QLineEdit()
#         self.custom_attribute_label.hide()
#         self.custom_attribute_input.hide()
#         self.custom_attribute_input.setFixedSize(180, 50)
#         self.custom_attribute_layout.addWidget(self.custom_attribute_label)
#         self.custom_attribute_layout.addWidget(self.custom_attribute_input)
#         layout.addLayout(self.custom_attribute_layout)

#         self.fasta_layout = QHBoxLayout()
#         self.fasta_label = QLabel("Select FASTA File to Extract Headers:")
#         self.fasta_layout.addWidget(self.fasta_label)
#         self.fasta_button = QPushButton("Browse FASTA...")
#         self.fasta_button.setFixedSize(180, 50)
#         self.fasta_button.setStyleSheet("""
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
#         self.fasta_button.clicked.connect(self.browse_fasta_file)
#         self.fasta_layout.addWidget(self.fasta_button)
#         layout.addLayout(self.fasta_layout)

#         self.fai_layout = QHBoxLayout()
#         self.fai_label = QLabel("Select index(.fai) File:")
#         self.fai_layout.addWidget(self.fai_label)
#         self.fai_button = QPushButton("Browse index(.fai)")
#         self.fai_button.setFixedSize(180, 50)
#         self.fai_button.setStyleSheet("""
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
#         self.fai_button.clicked.connect(self.browse_fai_file)
#         self.fai_layout.addWidget(self.fai_button)
#         layout.addLayout(self.fai_layout)

#         self.specie_layout = QHBoxLayout()
#         self.specie_label = QLabel("Enter Species Name:")
#         self.specie_layout.addWidget(self.specie_label)
#         self.specie_input = QLineEdit()
#         self.specie_input.setFixedSize(180, 50)
#         self.specie_layout.addWidget(self.specie_input)
#         layout.addLayout(self.specie_layout)

#         self.output_layout = QHBoxLayout()
#         self.output_dir_label = QLabel("Select Output Directory:")
#         self.output_layout.addWidget(self.output_dir_label)
#         self.output_dir_button = QPushButton("Choose Directory")
#         self.output_dir_button.setFixedSize(180, 50)
#         self.output_dir_button.setStyleSheet("""
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
#         self.output_dir_button.clicked.connect(self.browse_output_directory)
#         self.output_layout.addWidget(self.output_dir_button)
#         layout.addLayout(self.output_layout)

#         self.button_layout = QHBoxLayout()
#         self.run_button = QPushButton("Submit")
#         self.run_button.setFixedSize(200, 40)
#         self.run_button.setStyleSheet("""
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
#         self.run_button.clicked.connect(self.run_filter)
#         self.button_layout.addWidget(self.run_button)

#         self.stop_button = QPushButton("Stop")
#         self.stop_button.setFixedSize(200, 40)
#         self.stop_button.setEnabled(False)
#         self.stop_button.setStyleSheet("""
#             QPushButton {
#                 font-size: 16px;
#                 color: white;
#                 background-color: #2C3E50;
#                 border: none;
#                 text-align: left;
#                 padding: 5px 10px;
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
#         self.stop_button.clicked.connect(self.stop_process)
#         self.button_layout.addWidget(self.stop_button)

#         layout.addLayout(self.button_layout)

#         self.genelist_preview_label = QLabel("Genelist Preview:")
#         layout.addWidget(self.genelist_preview_label)
#         self.genelist_preview = QTextEdit()
#         self.genelist_preview.setReadOnly(True)
#         layout.addWidget(self.genelist_preview)

#         self.fasta_preview_label = QLabel("FASTA Headers Preview:")
#         layout.addWidget(self.fasta_preview_label)
#         self.fasta_preview = QTextEdit()
#         self.fasta_preview.setReadOnly(True)
#         layout.addWidget(self.fasta_preview)

#         self.rgenes_coordlist_preview_label = QLabel("Rgenes_coordlist Preview:")
#         layout.addWidget(self.rgenes_coordlist_preview_label)
#         self.rgenes_coordlist_preview = QTextEdit()
#         self.rgenes_coordlist_preview.setReadOnly(True)
#         layout.addWidget(self.rgenes_coordlist_preview)

#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)

#         self.gff_file = None
#         self.output_directory = None
#         self.fasta_file = None
#         self.fai_file = None
#         self.specie_name = None
#         self.worker = None

#     def browse_input_file(self):
#         file_dialog = QFileDialog()
#         file_paths, _ = file_dialog.getOpenFileNames(self, "Select GFF3 Files", "", "GFF3 Files (*.gff3);;All Files (*)")
#         if file_paths:
#             self.gff_file = file_paths[0]
#             self.input_label.setText(f"Selected GFF3 File: {self.gff_file}")

#     def browse_output_directory(self):
#         dir_dialog = QFileDialog()
#         dir_path = dir_dialog.getExistingDirectory(self, "Select Output Directory")
#         if dir_path:
#             self.output_directory = dir_path
#             self.output_dir_label.setText(f"Selected Directory: {dir_path}")

#     def browse_fasta_file(self):
#         file_dialog = QFileDialog()
#         file_path, _ = file_dialog.getOpenFileName(self, "Select FASTA File", "", "FASTA Files (*.fasta);;All Files (*)")
#         if file_path:
#             self.fasta_file = file_path
#             self.fasta_label.setText(f"Selected FASTA File: {file_path}")

#     def browse_fai_file(self):
#         file_dialog = QFileDialog()
#         file_path, _ = file_dialog.getOpenFileName(self, "Select .fai File", "", "FAI Files (*.fai)")
#         if file_path:
#             self.fai_file = file_path
#             self.fai_label.setText(f"Selected .fai File: {file_path}")

#     def handle_custom_attribute(self):
#         if self.attribute_combo.currentText() == "Custom":
#             self.custom_attribute_label.show()
#             self.custom_attribute_input.show()
#         else:
#             self.custom_attribute_label.hide()
#             self.custom_attribute_input.hide()

#     def run_filter(self):
#         if not all([self.gff_file, self.fasta_file, self.output_directory, self.fai_file, self.specie_input.text()]):
#             QMessageBox.critical(self, "Error", "Please ensure all inputs are selected.")
#             return

#         QMessageBox.information(self, "Analysis Started", "Your analysis is running.")

#         selected_feature = self.feature_combo.currentText()
#         selected_attribute = self.attribute_combo.currentText()
#         if selected_attribute == "Custom":
#             selected_attribute = self.custom_attribute_input.text()

#         specie_name = self.specie_input.text()

#         self.worker = Worker(self.gff_file, self.fasta_file, self.fai_file, specie_name, self.output_directory, selected_feature, selected_attribute)
#         self.worker.update_genelist_preview.connect(self.genelist_preview.setPlainText)
#         self.worker.update_fasta_preview.connect(self.fasta_preview.setPlainText)
#         self.worker.update_rgenes_coordlist_preview.connect(self.rgenes_coordlist_preview.setPlainText)
#         self.worker.finished.connect(self.on_finished)
#         self.worker.start()
#         self.stop_button.setEnabled(True)

#     def stop_process(self):
#         if self.worker:
#             self.worker.stop()
#         self.stop_button.setEnabled(False)

#     def on_finished(self, success, message):
#         self.stop_button.setEnabled(False)
#         if success:
#             QMessageBox.information(self, "Analysis Completed", message)
#         else:
#             QMessageBox.critical(self, "Analysis Completed", message)

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

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = GFFFilterApp()
#     window.show()
#     sys.exit(app.exec())

import sys
import os
import logging
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QTextEdit, QComboBox, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QSize, QThread, Signal
from PySide6.QtGui import QFont, QIcon
import re
import pandas as pd
import csv
import subprocess

def setup_logging(output_directory):
    log_file = os.path.join(output_directory, "gene_density_map.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger()

def create_csv_from_txt(txt_file, species_name, output_directory, window_size=5000):
    logger = setup_logging(output_directory)
    output_file = os.path.join(output_directory, f"{species_name}_bin.csv")
    headers = ["Chr", "Start", "End", "Value", "Bin1", "Bin2"]
    
    try:
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
    except PermissionError:
        logger.error(f"Permission denied: Cannot write to {output_file}. Please check the file permissions.")
        return None
    except Exception as e:
        logger.error(f"Error creating CSV file {output_file}: {e}")
        return None

    data = []
    with open(txt_file, mode='r') as file:
        for line in file:
            columns = line.strip().split()
            if len(columns) >= 4:
                columns[0] = species_name
                data.append(columns + ["", ""])
            else:
                logger.warning(f"Skipping line due to unexpected column count: {line}")

    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    try:
        df = pd.read_csv(output_file)
        # Use window_size for bin calculations
        df["Bin1"] = [i * window_size for i in range(0, len(df))]
        df["Bin2"] = [(i + 1) * window_size for i in range(0, len(df))]
        df.to_csv(output_file, index=False)
    except Exception as e:
        logger.error(f"Error reading or writing CSV file: {e}")
        return None

    karyotype_file = os.path.join(output_directory, f"{species_name}_Karyotype.csv")
    try:
        karyotype_data = pd.DataFrame({
            "Chr": [species_name],
            "Start": [0],
            "End": [df["Bin2"].iloc[-1]]  # Use last bin end position
        })
        karyotype_data.to_csv(karyotype_file, index=False)
    except Exception as e:
        logger.error(f"Error creating Karyotype file: {e}")
        return None

    try:
        df = df[df["Value"].astype(float) != 0]
    except ValueError as e:
        logger.error(f"Error converting 'Value' column to float: {e}")
        return None

    df["Start"] = df["Bin1"]
    df["End"] = df["Bin2"]
    df.drop(columns=["Bin1", "Bin2"], inplace=True)

    try:
        df.to_csv(output_file, index=False)
        logger.info(f"Processing completed. CSV saved at: {output_file}")
        logger.info(f"Karyotype saved at: {karyotype_file}")
    except Exception as e:
        logger.error(f"Error saving the final CSV file: {e}")
        return None

    return output_file, karyotype_file

def convert_count_to_txt(count_file):
    logger = logging.getLogger()
    txt_file = count_file.replace('.count', '.txt')
    
    try:
        with open(count_file, 'r') as infile, open(txt_file, 'w') as outfile:
            for line in infile:
                outfile.write(line)
        logger.info(f"Successfully converted {count_file} to {txt_file}.")
        return txt_file
    except Exception as e:
        logger.error(f"Error converting file: {e}")
        return None

def find_r_executable():
    logger = logging.getLogger()
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        possible_paths = [
            os.path.normpath(os.path.join(base_path, "src", "R", "bin", "Rscript.exe")),  # Expected path
            os.path.normpath(os.path.join(base_path, "R", "bin", "Rscript.exe")),  # Fallback
            os.path.normpath(os.path.join(os.path.dirname(sys.executable), "src", "R", "bin", "Rscript.exe")),
            os.path.normpath(os.path.join(os.path.dirname(sys.executable), "R", "bin", "Rscript.exe"))
        ]
    else:
        base_path = os.path.dirname(__file__)
        possible_paths = [
            os.path.normpath(os.path.join(base_path, "R", "bin", "Rscript.exe"))
        ]
    logger.info(f"Base path: {base_path}")
    logger.info(f"Executable directory: {os.path.dirname(sys.executable)}")
    
    for r_exe in possible_paths:
        logger.info(f"Checking R executable at: {r_exe}")
        if os.path.exists(r_exe):
            logger.info(f"Found R executable at: {r_exe}")
            return r_exe
        logger.error(f"R executable not found at: {r_exe}")
        r_dir = os.path.dirname(r_exe)
        if os.path.exists(r_dir):
            logger.info(f"Contents of {r_dir}: {os.listdir(r_dir)}")
        else:
            logger.error(f"Directory does not exist: {r_dir}")
    
    # Log entire sys._MEIPASS structure
    if getattr(sys, 'frozen', False):
        logger.info(f"Listing all files in sys._MEIPASS: {base_path}")
        for root, dirs, files in os.walk(base_path):
            for file in files:
                logger.info(f"Found file: {os.path.join(root, file)}")
    
    logger.error("No R executable found in any possible paths")
    return None

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

def process_overlap(bed_file, coord_file, output_directory, specie_name):
    logger = setup_logging(output_directory)
    output_file = os.path.join(output_directory, f"{specie_name}_chr.count")
    try:
        if not os.path.exists(bed_file):
            return f"Error: BED file not found: {bed_file}"
        if not os.path.exists(coord_file):
            return f"Error: Coordinate file not found: {coord_file}"

        r_exe = find_r_executable()
        if not r_exe:
            return "Error: Bundled R executable not found. Ensure R is included in the application folder."

        r_script = get_resource_path("intersect.R")
        if not os.path.exists(r_script):
            return f"Error: R script not found at {r_script}"

        r_home = os.path.dirname(os.path.dirname(r_exe))
        os.environ["R_HOME"] = r_home
        os.environ["R_LIBS"] = os.path.join(r_home, "library")

        result = subprocess.run(
            [r_exe, r_script, bed_file, coord_file, output_file],
            check=True, text=True, capture_output=True
        )

        logger.info("R script output: %s", result.stdout)
        logger.info("R script errors (if any): %s", result.stderr)

        if not os.path.exists(output_file):
            return f"Error: Output count file was not created: {output_file}"

        return output_file

    except subprocess.CalledProcessError as e:
        return f"Error executing R script: {e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def extract_attribute(attribute_column, selected_key):
    match = re.search(f"{selected_key}=([^;]+)", attribute_column, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def cut_columns_in_place(file_path, columns_to_keep):
    logger = logging.getLogger()
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        with open(file_path, 'w') as f:
            for line in lines:
                if line.startswith('#'):
                    f.write(line)
                    continue
                columns = line.strip().split('\t')
                filtered_columns = [columns[i - 1] for i in columns_to_keep if i - 1 < len(columns)]
                f.write('\t'.join(filtered_columns) + '\n')
    except Exception as e:
        logger.error(f"Error during column cutting: {e}")

def matching_genes(rgenes_file, genelist_file, output_file):
    logger = logging.getLogger()
    try:
        with open(rgenes_file, 'r') as rfile:
            rgenes_list = {line.strip() for line in rfile}
        with open(genelist_file, 'r') as gfile, open(output_file, 'w') as outfile:
            for line in gfile:
                if line.startswith('#'):
                    continue
                columns = line.strip().split('\t')
                if len(columns) < 6:
                    continue
                gene_id = columns[5]
                if normalize_id_to_underscores(gene_id) in rgenes_list:
                    outfile.write(line)
        if os.path.getsize(output_file) == 0:
            return "Error: No matches found! Please ensure the last column of 'genelist' and 'rgenes.list' match."
        cut_columns_in_place(output_file, [1, 3, 4])
        return True
    except Exception as e:
        return f"Error matching genes: {e}"

def normalize_id_to_underscores(id_str):
    return id_str.replace('.', '_')

def process_gff(input_file, output_file, feature_type="mRNA", selected_attribute="ID"):
    logger = logging.getLogger()
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                if line.startswith('#'):
                    continue
                columns = line.strip().split('\t')
                if len(columns) < 9:
                    continue
                if columns[2].lower() == feature_type.lower():
                    selected_columns = [columns[0], columns[2], columns[3], columns[4], columns[6]]
                    attribute_value = extract_attribute(columns[8], selected_attribute)
                    if attribute_value:
                        attribute_value = normalize_id_to_underscores(attribute_value)
                    selected_columns.append(attribute_value if attribute_value else "Unknown")
                    outfile.write('\t'.join(selected_columns) + '\n')
        return True
    except Exception as e:
        return f"Error processing GFF file: {e}"

def process_fasta(fasta_file, output_file):
    logger = logging.getLogger()
    try:
        with open(fasta_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                if line.startswith('>'):
                    header = line.strip().replace('>', '')
                    normalized_header = normalize_id_to_underscores(header)
                    outfile.write(f"{normalized_header}\n")
        return True
    except Exception as e:
        return f"Error processing FASTA file: {e}"

def process_fai(fai_file, output_directory, specie_name, window_size=5000):
    logger = setup_logging(output_directory)
    output_file = os.path.join(output_directory, f"{specie_name}_chr.size")
    try:
        with open(fai_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                columns = line.split('\t')
                if len(columns) < 2:
                    raise ValueError(f"Invalid line in .fai file: {line.strip()}")
                chr_name = columns[0]
                chr_size = columns[1]
                outfile.write(f"{chr_name}\t{chr_size}\n")
        if not os.path.exists(output_file):
            return f"Error: Output file was not created: {output_file}"
        r_exe = find_r_executable()
        if not r_exe:
            return "Error: Bundled R executable not found. Ensure R is included in the application folder."
        r_script = get_resource_path("make_windows.R")
        if not os.path.exists(r_script):
            return f"Error: R script not found at {r_script}"
        r_home = os.path.dirname(os.path.dirname(r_exe))
        os.environ["R_HOME"] = r_home
        os.environ["R_LIBS"] = os.path.join(r_home, "library")
        output_bed_file = os.path.join(output_directory, f"{specie_name}_windows.bed")
        result = subprocess.run(
            [r_exe, r_script, output_file, str(window_size), output_bed_file],
            check=True, text=True, capture_output=True,  encoding="utf-8" 
        )
        if not os.path.exists(output_bed_file):
            return f"Error: Output BED file was not created: {output_bed_file}"
        logger.info("R script executed successfully.")
        return True
    except ValueError as ve:
        return f"Error processing .fai file: {ve}"
    except FileNotFoundError:
        return f"Error: .fai file not found: {fai_file}"
    except subprocess.CalledProcessError as e:
        return f"Error executing R script: {e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

class Worker(QThread):
    update_genelist_preview = Signal(str)
    update_fasta_preview = Signal(str)
    update_rgenes_coordlist_preview = Signal(str)
    finished = Signal(bool, str)

    def __init__(self, gff_file, fasta_file, fai_file, specie_name, output_directory, feature_type, selected_attribute, window_size):
        super().__init__()
        self.gff_file = gff_file
        self.fasta_file = fasta_file
        self.fai_file = fai_file
        self.specie_name = specie_name
        self.output_directory = output_directory
        self.feature_type = feature_type
        self.selected_attribute = selected_attribute
        self.window_size = window_size
        self.process = None
        self.stop_requested = False
        self.logger = setup_logging(output_directory)

    def run(self):
        try:
            # Process GFF file
            gff_output_file = os.path.join(self.output_directory, "genelist")
            gff_result = process_gff(self.gff_file, gff_output_file, self.feature_type, self.selected_attribute)
            if gff_result is not True:
                self.finished.emit(False, gff_result)
                return
            self.update_genelist_preview.emit(self.get_preview(gff_output_file))
            if self.stop_requested:
                self.finished.emit(False, "Process stopped by user.")
                return

            # Process FASTA file
            fasta_output_file = os.path.join(self.output_directory, "rgenes.list")
            fasta_result = process_fasta(self.fasta_file, fasta_output_file)
            if fasta_result is not True:
                self.finished.emit(False, fasta_result)
                return
            self.update_fasta_preview.emit(self.get_preview(fasta_output_file))
            if self.stop_requested:
                self.finished.emit(False, "Process stopped by user.")
                return

            # Match genes
            rgenes_coord_output = os.path.join(self.output_directory, "rgenes_coord.list")
            grep_result = matching_genes(fasta_output_file, gff_output_file, rgenes_coord_output)
            if grep_result is not True:
                self.finished.emit(False, grep_result)
                return
            if os.path.getsize(rgenes_coord_output) == 0:
                self.finished.emit(False, "No matching entries found. Please ensure the last columns of 'genelist' and 'rgenes.list' match.")
                return
            self.update_rgenes_coordlist_preview.emit(self.get_preview(rgenes_coord_output))
            if self.stop_requested:
                self.finished.emit(False, "Process stopped by user.")
                return

            # Process FAI file with window size
            fai_result = process_fai(self.fai_file, self.output_directory, self.specie_name, self.window_size)
            if fai_result is not True:
                self.finished.emit(False, fai_result)
                return
            if self.stop_requested:
                self.finished.emit(False, "Process stopped by user.")
                return

            # Process overlap
            bed_file = os.path.join(self.output_directory, f"{self.specie_name}_windows.bed")
            coord_file = os.path.join(self.output_directory, "rgenes_coord.list")
            r_exe = find_r_executable()
            if not r_exe:
                self.finished.emit(False, "Error: Bundled R executable not found. Ensure R is included in the application folder.")
                return
            r_script = get_resource_path("intersect.R")
            if not os.path.exists(r_script):
                self.finished.emit(False, f"Error: R script not found at {r_script}")
                return
            r_home = os.path.dirname(os.path.dirname(r_exe))
            os.environ["R_HOME"] = r_home
            os.environ["R_LIBS"] = os.path.join(r_home, "library")
            output_file = os.path.join(self.output_directory, f"{self.specie_name}_chr.count")
            cmd = [r_exe, r_script, bed_file, coord_file, output_file]
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = self.process.communicate()
            if self.stop_requested:
                self.finished.emit(False, "Process stopped by user.")
                return
            if self.process.returncode != 0:
                self.finished.emit(False, f"Error executing R script for overlap: {stderr}")
                return
            if not os.path.exists(output_file):
                self.finished.emit(False, f"Error: Output count file was not created: {output_file}")
                return

            # Convert count to txt
            txt_file = convert_count_to_txt(output_file)
            if txt_file is None:
                self.finished.emit(False, "Error: Conversion to .txt file failed.")
                return
            if self.stop_requested:
                self.finished.emit(False, "Process stopped by user.")
                return

            # Create CSV with window size
            csv_file, karyotype_file = create_csv_from_txt(txt_file, self.specie_name, self.output_directory, self.window_size)
            if not csv_file:
                self.finished.emit(False, "Error creating CSV file.")
                return
            if self.stop_requested:
                self.finished.emit(False, "Process stopped by user.")
                return

            # Generate ideogram
            r_script = get_resource_path("generate_ideogram.R")
            if not os.path.exists(r_script):
                self.finished.emit(False, f"Error: R script not found at {r_script}")
                return
            cmd = [r_exe, r_script, karyotype_file, csv_file, self.output_directory]
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = self.process.communicate()
            if self.stop_requested:
                self.finished.emit(False, "Process stopped by user.")
                return
            if self.process.returncode != 0:
                self.finished.emit(False, f"Error generating ideogram: {stderr}")
                return

            self.finished.emit(True, f"Processing completed successfully!\nFiles saved in: {self.output_directory}")

        except Exception as e:
            self.finished.emit(False, f"Unexpected error: {str(e)}")

    def stop(self):
        """Request to stop the process."""
        self.stop_requested = True
        if self.process:
            self.process.terminate()

    def get_preview(self, file_path):
        preview_lines = []
        try:
            with open(file_path, 'r') as f:
                for _ in range(5):
                    line = f.readline()
                    if not line:
                        break
                    preview_lines.append(line.strip())
        except Exception as e:
            return "Error reading preview."
        return "\n".join(preview_lines)

class GFFFilterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genome Wide WorkBench")
        self.setWindowIcon(QIcon('src/image.png'))
        self.setGeometry(100, 100, 1000, 1000)

        self.header_label = QLabel("Gene Density Map")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.header_label.setStyleSheet("""
            QLabel {
                background-color: #2C3E50;
                color: white;
                padding: 10px;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.header_label)

        self.file_layout = QHBoxLayout()
        self.input_label = QLabel("Select GFF3/GFF File:")
        self.file_layout.addWidget(self.input_label)
        self.input_button = QPushButton("Browse GFF3")
        self.input_button.setFixedSize(180, 50)
        self.input_button.setStyleSheet("""
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
        self.input_button.clicked.connect(self.browse_input_file)
        self.file_layout.addWidget(self.input_button)
        layout.addLayout(self.file_layout)

        self.feature_layout = QHBoxLayout()
        self.feature_label = QLabel("Select Feature Type of GFF:")
        self.feature_layout.addWidget(self.feature_label)
        self.feature_combo = QComboBox()
        self.feature_combo.addItems(["mRNA", "gene", "CDS"])
        self.feature_combo.setFixedSize(180, 40)
        self.feature_layout.addWidget(self.feature_combo)
        layout.addLayout(self.feature_layout)

        self.attribute_layout = QHBoxLayout()
        self.attribute_label = QLabel("Select Attribute to Extract of GFF:")
        self.attribute_layout.addWidget(self.attribute_label)
        self.attribute_combo = QComboBox()
        self.attribute_combo.addItems(["ID", "Parent", "Name", "Custom"])
        self.attribute_combo.currentIndexChanged.connect(self.handle_custom_attribute)
        self.attribute_combo.setFixedSize(180, 50)
        self.attribute_layout.addWidget(self.attribute_combo)
        layout.addLayout(self.attribute_layout)

        self.custom_attribute_layout = QHBoxLayout()
        self.custom_attribute_label = QLabel("Enter Custom Attribute:")
        self.custom_attribute_input = QLineEdit()
        self.custom_attribute_label.hide()
        self.custom_attribute_input.hide()
        self.custom_attribute_input.setFixedSize(180, 50)
        self.custom_attribute_layout.addWidget(self.custom_attribute_label)
        self.custom_attribute_layout.addWidget(self.custom_attribute_input)
        layout.addLayout(self.custom_attribute_layout)

        self.fasta_layout = QHBoxLayout()
        self.fasta_label = QLabel("Select FASTA File to Extract Headers:")
        self.fasta_layout.addWidget(self.fasta_label)
        self.fasta_button = QPushButton("Browse FASTA...")
        self.fasta_button.setFixedSize(180, 50)
        self.fasta_button.setStyleSheet("""
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
        self.fasta_button.clicked.connect(self.browse_fasta_file)
        self.fasta_layout.addWidget(self.fasta_button)
        layout.addLayout(self.fasta_layout)

        self.fai_layout = QHBoxLayout()
        self.fai_label = QLabel("Select index(.fai) File:")
        self.fai_layout.addWidget(self.fai_label)
        self.fai_button = QPushButton("Browse index(.fai)")
        self.fai_button.setFixedSize(180, 50)
        self.fai_button.setStyleSheet("""
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
        self.fai_button.clicked.connect(self.browse_fai_file)
        self.fai_layout.addWidget(self.fai_button)
        layout.addLayout(self.fai_layout)

        self.specie_layout = QHBoxLayout()
        self.specie_label = QLabel("Enter Species Name:")
        self.specie_layout.addWidget(self.specie_label)
        self.specie_input = QLineEdit()
        self.specie_input.setFixedSize(180, 50)
        self.specie_layout.addWidget(self.specie_input)
        layout.addLayout(self.specie_layout)

        # Add window size input
        self.window_size_layout = QHBoxLayout()
        self.window_size_label = QLabel("Window Size (bp):")
        self.window_size_layout.addWidget(self.window_size_label)
        self.window_size_input = QLineEdit()
        self.window_size_input.setFixedSize(180, 50)
        self.window_size_input.setText("5000")  # Default value
        self.window_size_layout.addWidget(self.window_size_input)
        layout.addLayout(self.window_size_layout)

        self.output_layout = QHBoxLayout()
        self.output_dir_label = QLabel("Select Output Directory:")
        self.output_layout.addWidget(self.output_dir_label)
        self.output_dir_button = QPushButton("Choose Directory")
        self.output_dir_button.setFixedSize(180, 50)
        self.output_dir_button.setStyleSheet("""
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
        self.output_dir_button.clicked.connect(self.browse_output_directory)
        self.output_layout.addWidget(self.output_dir_button)
        layout.addLayout(self.output_layout)

        self.button_layout = QHBoxLayout()
        self.run_button = QPushButton("Submit")
        self.run_button.setFixedSize(200, 40)
        self.run_button.setStyleSheet("""
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
        self.run_button.clicked.connect(self.run_filter)
        self.button_layout.addWidget(self.run_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedSize(200, 40)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                color: white;
                background-color: #2C3E50;
                border: none;
                text-align: left;
                padding: 5px 10px;
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
        self.stop_button.clicked.connect(self.stop_process)
        self.button_layout.addWidget(self.stop_button)

        layout.addLayout(self.button_layout)

        self.genelist_preview_label = QLabel("Genelist Preview:")
        layout.addWidget(self.genelist_preview_label)
        self.genelist_preview = QTextEdit()
        self.genelist_preview.setReadOnly(True)
        layout.addWidget(self.genelist_preview)

        self.fasta_preview_label = QLabel("FASTA Headers Preview:")
        layout.addWidget(self.fasta_preview_label)
        self.fasta_preview = QTextEdit()
        self.fasta_preview.setReadOnly(True)
        layout.addWidget(self.fasta_preview)

        self.rgenes_coordlist_preview_label = QLabel("Rgenes_coordlist Preview:")
        layout.addWidget(self.rgenes_coordlist_preview_label)
        self.rgenes_coordlist_preview = QTextEdit()
        self.rgenes_coordlist_preview.setReadOnly(True)
        layout.addWidget(self.rgenes_coordlist_preview)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.gff_file = None
        self.output_directory = None
        self.fasta_file = None
        self.fai_file = None
        self.specie_name = None
        self.worker = None

    def browse_input_file(self):
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(self, "Select GFF3 Files", "", "GFF3 Files (*.gff3);;All Files (*)")
        if file_paths:
            self.gff_file = file_paths[0]
            self.input_label.setText(f"Selected GFF3 File: {self.gff_file}")

    def browse_output_directory(self):
        dir_dialog = QFileDialog()
        dir_path = dir_dialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_directory = dir_path
            self.output_dir_label.setText(f"Selected Directory: {dir_path}")

    def browse_fasta_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select FASTA File", "", "FASTA Files (*.fasta);;All Files (*)")
        if file_path:
            self.fasta_file = file_path
            self.fasta_label.setText(f"Selected FASTA File: {file_path}")

    def browse_fai_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select .fai File", "", "FAI Files (*.fai)")
        if file_path:
            self.fai_file = file_path
            self.fai_label.setText(f"Selected .fai File: {file_path}")

    def handle_custom_attribute(self):
        if self.attribute_combo.currentText() == "Custom":
            self.custom_attribute_label.show()
            self.custom_attribute_input.show()
        else:
            self.custom_attribute_label.hide()
            self.custom_attribute_input.hide()

    def run_filter(self):
        if not all([self.gff_file, self.fasta_file, self.output_directory, self.fai_file, self.specie_input.text()]):
            QMessageBox.critical(self, "Error", "Please ensure all inputs are selected.")
            return
            
        # Validate window size
        try:
            window_size = int(self.window_size_input.text())
            if window_size <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Error", "Window size must be a positive integer.")
            return

        QMessageBox.information(self, "Analysis Started", "Your analysis is running.")

        selected_feature = self.feature_combo.currentText()
        selected_attribute = self.attribute_combo.currentText()
        if selected_attribute == "Custom":
            selected_attribute = self.custom_attribute_input.text()

        specie_name = self.specie_input.text()

        self.worker = Worker(
            self.gff_file, 
            self.fasta_file, 
            self.fai_file, 
            specie_name, 
            self.output_directory, 
            selected_feature, 
            selected_attribute,
            window_size  # Pass user-defined window size
        )
        self.worker.update_genelist_preview.connect(self.genelist_preview.setPlainText)
        self.worker.update_fasta_preview.connect(self.fasta_preview.setPlainText)
        self.worker.update_rgenes_coordlist_preview.connect(self.rgenes_coordlist_preview.setPlainText)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
        self.stop_button.setEnabled(True)

    def stop_process(self):
        if self.worker:
            self.worker.stop()
        self.stop_button.setEnabled(False)

    def on_finished(self, success, message):
        self.stop_button.setEnabled(False)
        if success:
            QMessageBox.information(self, "Analysis Completed", message)
        else:
            QMessageBox.critical(self, "Analysis Completed", message)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GFFFilterApp()
    window.show()
    sys.exit(app.exec())
