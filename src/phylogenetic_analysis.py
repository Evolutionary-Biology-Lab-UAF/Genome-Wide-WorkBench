# import os
# import re
# import logging
# import subprocess
# from PySide6.QtWidgets import (
#     QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog,
#     QProgressBar, QMessageBox, QLineEdit, QHBoxLayout, QSizePolicy, QSpacerItem, QComboBox
# )
# from PySide6.QtCore import QThread, Signal, Qt, QSize
# from PySide6.QtGui import QFont, QIcon
# from Bio import SeqIO
# import sys
# import tempfile
# import shutil

# class RenameThread(QThread):
#     progress_signal = Signal(str, str)  # Message, output file path
#     stopped_signal = Signal()  # New signal for user-initiated stop

#     def __init__(self, seq_file, ref_seq_file, output_dir, bootstrap_value=None, model=None, user_selected_model=False):
#         super().__init__()
#         self.seq_file = seq_file
#         self.ref_seq_file = ref_seq_file
#         self.output_dir = output_dir
#         self.bootstrap_value = bootstrap_value
#         self.model = model
#         self.user_selected_model = user_selected_model
#         self.error_log_path = os.path.join(self.output_dir, "phylogenetic_error.log")
#         self.log_file = os.path.join(self.output_dir, "phylogenetic_log_file.log")
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
#             # Build tool paths
#             if hasattr(sys, '_MEIPASS'):
#                 muscle_dir = os.path.join(sys._MEIPASS, 'tools', 'phylogenetic', 'muscle.exe')
#                 trimal_dir = os.path.join(sys._MEIPASS, 'tools', 'phylogenetic', 'trimal.exe')
#                 gblocks_dir = os.path.join(sys._MEIPASS, 'tools', 'phylogenetic', 'gblocks.exe')
#                 iqtree_dir = os.path.join(sys._MEIPASS, 'tools', 'phylogenetic', 'iqtree2.exe')
#             else:
#                 base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#                 muscle_dir = os.path.join(base_dir, 'tools', 'phylogenetic', 'muscle.exe')
#                 trimal_dir = os.path.join(base_dir, 'tools', 'phylogenetic', 'trimal.exe')
#                 gblocks_dir = os.path.join(base_dir, 'tools', 'phylogenetic', 'gblocks.exe')
#                 iqtree_dir = os.path.join(base_dir, 'tools', 'phylogenetic', 'iqtree2.exe')

#             # Generate output file names
#             seq_file_name = os.path.splitext(os.path.basename(self.seq_file))[0]
#             ref_seq_file_name = os.path.splitext(os.path.basename(self.ref_seq_file))[0]

#             # Prepare file paths
#             seq_modify_path = os.path.join(self.temp_dir, f"{seq_file_name}_modify_headers.fa")
#             ref_seq_modify_path = os.path.join(self.temp_dir, f"{ref_seq_file_name}_modify_headers.fa")
#             seq_formatted_path = os.path.join(self.temp_dir, f"{seq_file_name}_formatted_headers.fa")
#             ref_formatted_path = os.path.join(self.temp_dir, f"{ref_seq_file_name}_formatted_headers.fa")
#             concatenated_path = os.path.join(self.temp_dir, f"{seq_file_name}_RefAndCandidates.fa")

#             # Rename duplicates and format files
#             self.rename_duplicates(self.seq_file, seq_modify_path)
#             self.rename_duplicates(self.ref_seq_file, ref_seq_modify_path)
#             self.format_file(seq_modify_path, seq_formatted_path)
#             self.format_file(ref_seq_modify_path, ref_formatted_path)
#             self.concatenate_files(seq_formatted_path, ref_formatted_path, concatenated_path)

#             # File paths for MUSCLE and TRIMAL steps
#             seq_aln_file = os.path.join(self.temp_dir, f"{seq_file_name}_1_candidates_sequences.fa.aln")
#             ref_aln_file = os.path.join(self.temp_dir, f"{seq_file_name}_1_reference_sequences.fa.aln")
#             seq_trimmed_file = os.path.join(self.temp_dir, f"{seq_file_name}_1_candidates.fa.aln.trim50")
#             seq_trimmed_file_2 = os.path.join(self.temp_dir, f"{seq_file_name}_2_candidates.fa.aln.trim50.aln.trim")
#             seq_trimmed_file_3 = os.path.join(self.temp_dir, f"{seq_file_name}_3_candidates.fa.aln.trim50.aln.trim")
#             seq_trimmed_file_4 = os.path.join(self.temp_dir, f"{seq_file_name}_4_candidates.fa.aln.trim50.aln.trim")
#             seq_trimmed_file_5 = os.path.join(self.temp_dir, f"{seq_file_name}_5_candidates.fa.aln.trim50.aln.trim")
#             seq_trimmed_file_6 = os.path.join(self.temp_dir, f"{seq_file_name}_6_candidates.fa.aln.trim50.aln.trim")
#             seq_trimmed_file_7 = os.path.join(self.temp_dir, f"{seq_file_name}_7_candidates.fa.aln.trim50.aln.trim")
#             seq_file_2 = os.path.join(self.temp_dir, f"{seq_file_name}_2_candidates.fa.aln.trim50.aln")
#             seq_file_3 = os.path.join(self.temp_dir, f"{seq_file_name}_3_candidates.fa.aln.trim50.aln")
#             seq_file_4 = os.path.join(self.temp_dir, f"{seq_file_name}_4_candidates.fa.aln.trim50.aln")
#             seq_file_5 = os.path.join(self.temp_dir, f"{seq_file_name}_5_candidates.fa.aln.trim50.aln")
#             seq_file_6 = os.path.join(self.temp_dir, f"{seq_file_name}_6_candidates.fa.aln.trim50.aln")
#             seq_file_7 = os.path.join(self.temp_dir, f"{seq_file_name}_7_candidates.fa.aln.trim50.aln")
#             seq_file_8 = os.path.join(self.temp_dir, f"{seq_file_name}_8_candidates.fa.aln.trim50.aln")
#             seq_file_con = os.path.join(self.temp_dir, f"{seq_file_name}_RefAndcandidates.fa")
#             seq_file_bp = os.path.join(self.temp_dir, f"{seq_file_name}_bp_RefAndcandidates.fa.aln")
#             gblocks_output_file = os.path.join(self.temp_dir, f"{seq_file_name}_RefAndcandidates.fa.aln-gb")
#             gblock_file = os.path.join(self.output_dir, f"{seq_file_name}_file_gb_MSA.fa")
#             ref_trimmed_file = os.path.join(self.temp_dir, f"{seq_file_name}_1_reference.fa.aln.trim50")
#             trimmed_candidates_file = os.path.join(self.temp_dir, f"{seq_file_name}_trimmed_candidates_file")
#             trimmed_reference_file = os.path.join(self.temp_dir, f"{seq_file_name}_trimmed_reference.fa")
#             filtered_2_candidates = os.path.join(self.temp_dir, f"{seq_file_name}_filtered_2_candidates.fa")
#             filtered_3_candidates = os.path.join(self.temp_dir, f"{seq_file_name}_filtered_3_candidates.fa")
#             filtered_4_candidates = os.path.join(self.temp_dir, f"{seq_file_name}_filtered_4_candidates.fa")
#             filtered_5_candidates = os.path.join(self.temp_dir, f"{seq_file_name}_filtered_5_candidates.fa")
#             filtered_6_candidates = os.path.join(self.temp_dir, f"{seq_file_name}_filtered_6_candidates.fa")
#             filtered_7_candidates = os.path.join(self.temp_dir, f"{seq_file_name}_filtered_7_candidates.fa")

#             # Step 1: MUSCLE alignment
#             if self.stop_requested:
#                 self.stopped_signal.emit()
#                 return
#             self.run_command(f'"{muscle_dir}" -super5 "{seq_formatted_path}" -output "{seq_aln_file}" -threads 56')
#             self.run_command(f'"{muscle_dir}" -super5 "{ref_formatted_path}" -output "{ref_aln_file}" -threads 56')

#             # Step 1: TRIMAL trimming
#             if self.stop_requested:
#                 self.stopped_signal.emit()
#                 return
#             self.run_command(f'"{trimal_dir}" -in "{seq_aln_file}" -out "{seq_trimmed_file}" -htmlout "{os.path.join(self.temp_dir, seq_file_name + "_output1.html")}" -resoverlap 0.75 -seqoverlap 50')
#             self.remove_short_sequences(seq_trimmed_file, trimmed_candidates_file)
#             self.run_command(f'"{trimal_dir}" -in "{ref_aln_file}" -out "{ref_trimmed_file}" -htmlout "{os.path.join(self.temp_dir, seq_file_name + "_output1.1.html")}" -resoverlap 0.75 -seqoverlap 50')
#             self.remove_short_sequences(ref_trimmed_file, trimmed_reference_file)

#             # Step 2
#             if self.stop_requested:
#                 self.stopped_signal.emit()
#                 return
#             self.run_command(f'"{muscle_dir}" -super5 "{trimmed_candidates_file}" -output "{seq_file_2}" -threads 56')
#             self.run_command(f'"{trimal_dir}" -in "{seq_file_2}" -out "{seq_trimmed_file_2}" -htmlout "{os.path.join(self.temp_dir, seq_file_name + "_output2.html")}" -gt 0.5')
#             self.remove_short_sequences(seq_trimmed_file_2, filtered_2_candidates)

#             # Step 3
#             if self.stop_requested:
#                 self.stopped_signal.emit()
#                 return
#             self.run_command(f'"{muscle_dir}" -super5 "{filtered_2_candidates}" -output "{seq_file_3}" -threads 56')
#             self.run_command(f'"{trimal_dir}" -in "{seq_file_3}" -out "{seq_trimmed_file_3}" -htmlout "{os.path.join(self.temp_dir, seq_file_name + "_output3.html")}" -resoverlap 0.50 -seqoverlap 45')
#             self.remove_short_sequences(seq_trimmed_file_3, filtered_3_candidates)

#             # Step 4
#             if self.stop_requested:
#                 self.stopped_signal.emit()
#                 return
#             self.run_command(f'"{muscle_dir}" -super5 "{filtered_3_candidates}" -output "{seq_file_4}" -threads 56')
#             self.run_command(f'"{trimal_dir}" -in "{seq_file_4}" -out "{seq_trimmed_file_4}" -htmlout "{os.path.join(self.temp_dir, f"{seq_file_name}_output4.html")}" -resoverlap 0.50 -seqoverlap 45')
#             self.remove_short_sequences(seq_trimmed_file_4, filtered_4_candidates)

#             # Step 5
#             if self.stop_requested:
#                 self.stopped_signal.emit()
#                 return
#             self.run_command(f'"{muscle_dir}" -super5 "{filtered_4_candidates}" -output "{seq_file_5}" -threads 56')
#             self.run_command(f'"{trimal_dir}" -in "{seq_file_5}" -out "{seq_trimmed_file_5}" -htmlout "{os.path.join(self.temp_dir, f"{seq_file_name}_output5.html")}" -resoverlap 0.55 -seqoverlap 50')
#             self.remove_short_sequences(seq_trimmed_file_5, filtered_5_candidates)

#             # Step 6
#             if self.stop_requested:
#                 self.stopped_signal.emit()
#                 return
#             self.run_command(f'"{muscle_dir}" -super5 "{filtered_5_candidates}" -output "{seq_file_6}" -threads 56')
#             self.run_command(f'"{trimal_dir}" -in "{seq_file_6}" -out "{seq_trimmed_file_6}" -htmlout "{os.path.join(self.temp_dir, f"{seq_file_name}_output6.html")}" -resoverlap 0.55 -seqoverlap 60')
#             self.remove_short_sequences(seq_trimmed_file_6, filtered_6_candidates)

#             # Step 7
#             if self.stop_requested:
#                 self.stopped_signal.emit()
#                 return
#             self.run_command(f'"{muscle_dir}" -super5 "{filtered_6_candidates}" -output "{seq_file_7}" -threads 56')
#             self.run_command(f'"{trimal_dir}" -in "{seq_file_7}" -out "{seq_trimmed_file_7}" -htmlout "{os.path.join(self.temp_dir, f"{seq_file_name}_output7.html")}" -resoverlap 0.55 -seqoverlap 65')
#             self.remove_short_sequences(seq_trimmed_file_7, filtered_7_candidates)

#             # Step 8
#             if self.stop_requested:
#                 self.stopped_signal.emit()
#                 return
#             self.run_command(f'"{muscle_dir}" -super5 "{filtered_7_candidates}" -output "{seq_file_8}" -threads 56')

#             # Step 9: Concatenate
#             if self.stop_requested:
#                 self.stopped_signal.emit()
#                 return
#             self.concatenate_files(seq_file_8, trimmed_reference_file, seq_file_con)

#             # Step 10: MUSCLE on concatenated file
#             if self.stop_requested:
#                 self.stopped_signal.emit()
#                 return
#             self.run_command(f'"{muscle_dir}" -super5 "{seq_file_con}" -output "{seq_file_bp}" -threads 56')

#             # Step 11: Modify headers
#             modified_output_file = os.path.join(self.output_dir, f"{seq_file_name}_RefAndcandidates.fa.aln")
#             self.modify_headers(seq_file_bp, modified_output_file)
#             num_seqs = self.count_seq(modified_output_file)
#             half_num_seqs = (num_seqs // 2) + 1

#             # Step 12: GBlocks
#             if self.stop_requested:
#                 self.stopped_signal.emit()
#                 return
#             self.run_gblocks(gblocks_dir, modified_output_file, gblock_file, half_num_seqs)

#             # Step 13: IQTree
#             if self.stop_requested:
#                 self.stopped_signal.emit()
#                 return
#             iqtree_command = f'"{iqtree_dir}" -s "{gblock_file}" -nt "AUTO"'
#             if self.bootstrap_value:
#                 iqtree_command += f" -b {self.bootstrap_value}"
#             if self.model:
#                 iqtree_command += f' -m "{self.model}"'
#             self.run_command(iqtree_command)

#             # Parse best-fit model
#             best_fit_model = self.extract_best_fit_model()
#             if not self.user_selected_model and best_fit_model:
#                 self.progress_signal.emit("Analysis Complete", f"Best-fit model: {best_fit_model}\nOutput: {gblock_file}")
#             elif not best_fit_model:
#                 self.progress_signal.emit("Analysis Complete", f"Output: {gblock_file}")

#             # Move IQTree outputs to temp
#             iqtree_files = [
#                 f"{gblock_file}.bionj", f"{gblock_file}.ckp.gz", f"{gblock_file}.model.gz",
#                 f"{gblock_file}.iqtree", f"{gblock_file}.mldist", f"{gblock_file}.log"
#             ]
#             for iqtree_file in iqtree_files:
#                 self.move_to_temp(iqtree_file)

#             # Cleanup
#             self.cleanup_temp_dir()

#         except Exception as e:
#             if not self.stop_requested:  # Only log errors if not stopped by user
#                 self.log_error(str(e))
#                 self.progress_signal.emit(f"Error during execution: {str(e)}", "Check log_file.log and error.log for details.")

#     def stop(self):
#         self.stop_requested = True
#         if self.process:
#             self.process.terminate()
#             self.process.wait()
#         self.cleanup_temp_dir()  # Clean up temp files on stop
#         self.stopped_signal.emit()

#     def extract_best_fit_model(self):
#         try:
#             with open(self.log_file, "r") as log_file:
#                 for line in log_file:
#                     if "Best-fit model:" in line:
#                         return line.split("Best-fit model:")[1].strip()
#         except Exception as e:
#             logging.error(f"Failed to read or parse log file: {e}")
#         return None

#     def rename_duplicates(self, input_file, output_file):
#         header_count = {}
#         renamed_records = []
#         with open(input_file, "r") as in_file:
#             for record in SeqIO.parse(in_file, "fasta"):
#                 header = record.id
#                 if header not in header_count:
#                     header_count[header] = 1
#                     new_header = header
#                 else:
#                     header_count[header] += 1
#                     new_header = f"{header}_{header_count[header]}"
#                 renamed_records.append(f">{new_header}\n{record.seq}")
#         with open(output_file, "w") as out_file:
#             out_file.write("\n".join(renamed_records))
#         logging.info(f"Renamed sequences written to {output_file}")

#     def format_file(self, input_file, formatted_file):
#         with open(input_file, "r") as infile, open(formatted_file, "w") as outfile:
#             for line in infile:
#                 if line.startswith(">"):
#                     line = re.sub(r"\|\*\|", "_", line)
#                     line = re.sub(r" .*", "", line)
#                 outfile.write(line)

#     def concatenate_files(self, file1, file2, output_file):
#         with open(output_file, "w") as out_f:
#             for file in [file1, file2]:
#                 with open(file, "r") as f:
#                     out_f.write(f.read())
#         logging.info(f"Concatenated file written to {output_file}")

#     def count_seq(self, input_file):
#         return sum(1 for _ in SeqIO.parse(input_file, "fasta"))

#     def remove_short_sequences(self, input_file, output_file, min_len=3):
#         try:
#             has_valid_sequence = False
#             with open(output_file, "w") as out_file:
#                 for record in SeqIO.parse(input_file, "fasta"):
#                     seq = str(record.seq).replace("-", "")
#                     if len(seq) >= min_len:
#                         SeqIO.write(record, out_file, "fasta")
#                         has_valid_sequence = True
#             if not has_valid_sequence:
#                 logging.warning(f"No sequences longer than {min_len} found. Program will now terminate.")
#                 sys.exit(1)
#         except Exception as e:
#             logging.error(f"An error occurred: {e}")
#             sys.exit(1)

#     def modify_headers(self, input_file, output_file):
#         with open(input_file, "r") as infile, open(output_file, "w") as outfile:
#             for line in infile:
#                 if line.startswith(">"):
#                     line = re.sub(r" .*\n", "\n", line)
#                 outfile.write(line)

#     def log_error(self, message):
#         with open(self.error_log_path, "w") as error_log:
#             error_log.write(message + "\n")

#     def run_command(self, command, is_gblocks=False):
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
#                     if self.process.returncode == 1 and is_gblocks:
#                         logging.info("Gblocks returned 1 but it is treated as success.")
#                     else:
#                         raise RuntimeError(f"Command failed with return code {self.process.returncode}: {stderr}")
#         except Exception as e:
#             self.log_error(str(e))
#             self.progress_signal.emit("Command encountered an error", "Please check the log for details.")
#             logging.error(f"An error occurred while running the command: {e}")
#             raise e

#     def run_gblocks(self, gblocks_dir, modified_output_file, gblock_file, half_num_seqs):
#         command = f'"{gblocks_dir}" "{modified_output_file}" -t=p -b1={half_num_seqs} -b2={half_num_seqs} -b3=8 -b4=5 -b5=a'
#         self.run_command(command, is_gblocks=True)
#         original_gb_file = f"{modified_output_file}-gb"
#         original_htm_file = f"{modified_output_file}-gb.htm"
#         if os.path.exists(original_gb_file):
#             output_gb_file_in_output_dir = os.path.join(self.temp_dir, os.path.basename(original_gb_file))
#             shutil.move(original_gb_file, output_gb_file_in_output_dir)
#             logging.info(f"Moved Gblocks output to {output_gb_file_in_output_dir}")
#             self.modify_gblocks_output(output_gb_file_in_output_dir, gblock_file)
#         else:
#             logging.error(f"Gblocks output file not found: {original_gb_file}")
#         if os.path.exists(original_htm_file):
#             output_htm_file_in_output_dir = os.path.join(self.temp_dir, os.path.basename(original_htm_file))
#             shutil.move(original_htm_file, output_htm_file_in_output_dir)
#             logging.info(f"Moved Gblocks HTML summary to {output_htm_file_in_output_dir}")
#         else:
#             logging.error(f"Gblocks HTML summary file not found: {original_htm_file}")

#     def modify_gblocks_output(self, input_file, output_file):
#         try:
#             with open(input_file, "r") as infile, open(output_file, "w") as outfile:
#                 for line in infile:
#                     if not line.startswith(">") and line.strip():
#                         updated_line = re.sub(r"\s+", "", line)
#                         outfile.write(updated_line + "\n")
#                     else:
#                         outfile.write(line)
#         except Exception as e:
#             logging.error(f"Error modifying GBlocks output: {e}")

#     def cleanup_temp_dir(self):
#         try:
#             shutil.rmtree(self.temp_dir)
#             logging.info(f"Successfully removed temporary directory: {self.temp_dir}")
#         except Exception as e:
#             logging.error(f"Failed to remove temporary directory: {e}")

#     def move_to_temp(self, file_path):
#         if os.path.exists(file_path):
#             shutil.move(file_path, self.temp_dir)
#             logging.info(f"Moved {file_path} to {self.temp_dir}")

# class FastaApp(QWidget):
#     DNA_MODELS = ["HKY", "GTR", "JC", "TN", "SYM"]
#     PROTEIN_MODELS = ["LG", "EHO", "GTR20"]

#     def __init__(self):
#         super().__init__()
#         self.thread = None
#         self.init_ui()

#     def init_ui(self):
#         self.setWindowTitle("Genome Wide WorkBench")
#         self.setWindowIcon(QIcon('src/image.png'))
#         self.setGeometry(100, 100, 1000, 800)

#         # Header
#         self.header_label = QLabel("Phylogenetic Analysis")
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
#         self.header_label.setFixedHeight(100)

#         # Main layout
#         self.layout = QVBoxLayout()
#         self.layout.setContentsMargins(0, 0, 0, 0)
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

#         self.load_seq_file_button = QPushButton("Select Sequence FASTA File")
#         self.load_seq_file_button.setFixedSize(240, 70)
#         self.load_seq_file_button.setIcon(QIcon("upload_icon.png"))
#         self.load_seq_file_button.setStyleSheet("""
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
#         self.load_seq_file_button.clicked.connect(self.open_seq_file_dialog)
#         self.file_layout.addWidget(self.load_seq_file_button)
#         self.layout.addLayout(self.file_layout)

#         # Reference sequence
#         self.ref_file_layout = QHBoxLayout()
#         self.ref_seq_file_display = QLineEdit(self)
#         self.ref_seq_file_display.setReadOnly(True)
#         self.ref_seq_file_display.setPlaceholderText("No reference file chosen")
#         self.ref_seq_file_display.setFixedWidth(self.input_width)
#         self.ref_seq_file_display.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 5px;
#                 font-size: 14px;
#                 border-radius: 4px;
#             }
#         """)
#         self.ref_file_layout.addWidget(self.ref_seq_file_display)

#         self.load_ref_seq_file_button = QPushButton("Select Reference FASTA File")
#         self.load_ref_seq_file_button.setFixedSize(240, 70)
#         self.load_ref_seq_file_button.setIcon(QIcon("upload_icon.png"))
#         self.load_ref_seq_file_button.setStyleSheet("""
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
#         self.load_ref_seq_file_button.clicked.connect(self.open_ref_seq_file_dialog)
#         self.ref_file_layout.addWidget(self.load_ref_seq_file_button)
#         self.layout.addLayout(self.ref_file_layout)

#         # Output directory
#         self.dir_layout = QHBoxLayout()
#         self.dir_display = QLineEdit(self)
#         self.dir_display.setReadOnly(True)
#         self.dir_display.setPlaceholderText("No output directory chosen")
#         self.dir_display.setFixedWidth(self.input_width)
#         self.dir_display.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 10px;
#                 font-size: 14px;
#                 border-radius: 4px;
#             }
#         """)
#         self.dir_layout.addWidget(self.dir_display)

#         self.load_output_button = QPushButton("Select Output Directory")
#         self.load_output_button.setFixedSize(240, 70)
#         self.load_output_button.setIcon(QIcon("folder_icon.png"))
#         self.load_output_button.setStyleSheet("""
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
#         self.load_output_button.clicked.connect(self.open_output_dir_dialog)
#         self.dir_layout.addWidget(self.load_output_button)
#         self.layout.addLayout(self.dir_layout)

#         # Bootstrap value
#         self.bootstrap_layout = QHBoxLayout()
#         self.bootstrap_layout.addStretch(1)
#         self.bootstrap_label = QLabel("Bootstrap Value (optional):")
#         self.bootstrap_label.setStyleSheet("font-size: 16px; padding: 10px;")
#         self.bootstrap_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.bootstrap_layout.addWidget(self.bootstrap_label)
#         self.bootstrap_layout.addSpacing(400)
#         self.bootstrap_input = QLineEdit(self)
#         self.bootstrap_input.setPlaceholderText("Leave empty for default")
#         self.bootstrap_input.setFixedWidth(230)
#         self.bootstrap_input.setStyleSheet("""
#             QLineEdit {
#                 border: 1px solid #2C3E50;
#                 padding: 10px;
#                 font-size: 14px;
#                 border-radius: 4px;
#             }
#         """)
#         self.bootstrap_layout.addWidget(self.bootstrap_input)
#         self.bootstrap_layout.addStretch(1)
#         self.layout.addLayout(self.bootstrap_layout)

#         # Model selection
#         self.model_layout = QHBoxLayout()
#         self.model_layout.addStretch(1)
#         self.model_label = QLabel("Model Selection (optional):")
#         self.model_label.setStyleSheet("font-size: 16px; padding: 10px;")
#         self.model_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.model_layout.addWidget(self.model_label)
#         self.model_layout.addSpacing(400)
#         self.model_combo = QComboBox(self)
#         self.model_combo.setFixedWidth(200)
#         self.model_combo.currentTextChanged.connect(self.toggle_custom_model_input)
#         self.model_layout.addWidget(self.model_combo)
#         self.model_layout.addStretch(1)
#         self.custom_model_input = QLineEdit(self)
#         self.custom_model_input.setPlaceholderText("Enter custom model if needed")
#         self.custom_model_input.setVisible(False)
#         self.model_layout.addWidget(self.custom_model_input)
#         self.layout.addLayout(self.model_layout)

#         # Button layout
#         self.button_layout = QHBoxLayout()
#         self.button_layout.addStretch()

#         # Submit button
#         self.rename_button = QPushButton("Submit")
#         self.rename_button.setFixedSize(200, 50)
#         self.rename_button.setStyleSheet("""
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
#         self.rename_button.clicked.connect(self.start_renaming)
#         self.button_layout.addWidget(self.rename_button)

#         # Stop button
#         self.stop_button = QPushButton("Stop")
#         self.stop_button.setFixedSize(200, 50)
#         self.stop_button.setStyleSheet("""
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
#             self.update_model_dropdown(file_name)

#     def open_ref_seq_file_dialog(self):
#         file_name, _ = QFileDialog.getOpenFileName(self, "Open Reference FASTA File", "", "FASTA Files (*.fa *.fasta);;All Files (*)")
#         if file_name:
#             self.ref_seq_file_display.setText(file_name)

#     def open_output_dir_dialog(self):
#         output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
#         if output_dir:
#             self.dir_display.setText(output_dir)

#     def update_model_dropdown(self, file_name):
#         is_dna = self.is_dna_sequence(file_name)
#         self.model_combo.clear()
#         models = self.DNA_MODELS if is_dna else self.PROTEIN_MODELS
#         self.model_combo.addItem("")
#         self.model_combo.addItems(models)
#         self.model_combo.addItem("Other...")

#     def is_dna_sequence(self, file_name):
#         try:
#             with open(file_name, "r") as f:
#                 for line in f:
#                     if line.startswith(">"):
#                         continue
#                     if any(char in line for char in "EFILPQZ"):
#                         return False
#             return True
#         except Exception as e:
#             QMessageBox.warning(self, "File Error", f"Error reading sequence file: {e}")
#             return True

#     def toggle_custom_model_input(self, text):
#         self.custom_model_input.setVisible(text == "Other...")
#         if text != "Other...":
#             self.custom_model_input.clear()

#     def start_renaming(self):
#         seq_file = self.seq_file_display.text()
#         ref_seq_file = self.ref_seq_file_display.text()
#         output_dir = self.dir_display.text()
#         bootstrap_value = self.bootstrap_input.text()
#         selected_model = self.model_combo.currentText()

#         if selected_model == "Other...":
#             selected_model = self.custom_model_input.text().strip() or None

#         if not seq_file or not ref_seq_file or not output_dir:
#             QMessageBox.warning(self, "Input Error", "Please provide all required input files and output directory.")
#             return
#         if bootstrap_value and not bootstrap_value.isdigit():
#             QMessageBox.warning(self, "Input Error", "Bootstrap value must be a positive integer.")
#             return

#         user_selected_model = bool(selected_model)

#         self.rename_button.setEnabled(False)
#         self.stop_button.setEnabled(True)
#         self.progress_bar.setVisible(True)
#         self.thread = RenameThread(
#             seq_file, ref_seq_file, output_dir,
#             bootstrap_value=int(bootstrap_value) if bootstrap_value else None,
#             model=selected_model,
#             user_selected_model=user_selected_model
#         )
#         self.thread.progress_signal.connect(self.on_progress)
#         self.thread.stopped_signal.connect(self.on_stopped)
#         self.thread.start()

#     def stop_process(self):
#         if self.thread:
#             self.thread.stop()

#     def on_stopped(self):
#         self.stop_button.setEnabled(False)
#         self.rename_button.setEnabled(True)
#         self.progress_bar.setVisible(False)
#         QMessageBox.information(self, "Process Stopped", "The process was stopped by the user.")

#     def on_progress(self, message, file_path):
#         self.stop_button.setEnabled(False)
#         self.rename_button.setEnabled(True)
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
#             if self.thread:
#                 self.thread.stop()
#             event.accept()
#         elif msg_box.clickedButton() == minimize_button:
#             event.ignore()
#             self.showMinimized()
#         else:
#             event.ignore()
#         self.seq_file_display.setText("No file chosen")
#         self.ref_seq_file_display.setText("No file chosen")
#         self.dir_display.setText("No directory chosen")
#         self.rename_button.setEnabled(False)

# if __name__ == "__main__":
#     app = QApplication([])
#     window = FastaApp()
#     window.show()
#     app.exec()



import os
import re
import logging
import subprocess
import webbrowser
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog,
    QProgressBar, QMessageBox, QLineEdit, QHBoxLayout, QSizePolicy, QSpacerItem, QComboBox
)
from PySide6.QtCore import QThread, Signal, Qt, QSize
from PySide6.QtGui import QFont, QIcon
from Bio import SeqIO
import sys
import tempfile
import shutil

class RenameThread(QThread):
    progress_signal = Signal(str, str)  # Message, output file path
    stopped_signal = Signal()  # New signal for user-initiated stop

    def __init__(self, seq_file, ref_seq_file, output_dir, bootstrap_value=None, model=None, user_selected_model=False):
        super().__init__()
        self.seq_file = seq_file
        self.ref_seq_file = ref_seq_file
        self.output_dir = output_dir
        self.bootstrap_value = bootstrap_value
        self.model = model
        self.user_selected_model = user_selected_model
        self.error_log_path = os.path.join(self.output_dir, "phylogenetic_error.log")
        self.log_file = os.path.join(self.output_dir, "phylogenetic_log_file.log")
        self.process = None
        self.stop_requested = False
        self.output_tree_file = None  # Store the final tree file path

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
            # Build tool paths
            if hasattr(sys, '_MEIPASS'):
                muscle_dir = os.path.join(sys._MEIPASS, 'tools', 'phylogenetic', 'muscle.exe')
                trimal_dir = os.path.join(sys._MEIPASS, 'tools', 'phylogenetic', 'trimal.exe')
                gblocks_dir = os.path.join(sys._MEIPASS, 'tools', 'phylogenetic', 'gblocks.exe')
                iqtree_dir = os.path.join(sys._MEIPASS, 'tools', 'phylogenetic', 'iqtree2.exe')
            else:
                base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                muscle_dir = os.path.join(base_dir, 'tools', 'phylogenetic', 'muscle.exe')
                trimal_dir = os.path.join(base_dir, 'tools', 'phylogenetic', 'trimal.exe')
                gblocks_dir = os.path.join(base_dir, 'tools', 'phylogenetic', 'gblocks.exe')
                iqtree_dir = os.path.join(base_dir, 'tools', 'phylogenetic', 'iqtree2.exe')

            # Generate output file names
            seq_file_name = os.path.splitext(os.path.basename(self.seq_file))[0]
            ref_seq_file_name = os.path.splitext(os.path.basename(self.ref_seq_file))[0]

            # Prepare file paths
            seq_modify_path = os.path.join(self.temp_dir, f"{seq_file_name}_modify_headers.fa")
            ref_seq_modify_path = os.path.join(self.temp_dir, f"{ref_seq_file_name}_modify_headers.fa")
            seq_formatted_path = os.path.join(self.temp_dir, f"{seq_file_name}_formatted_headers.fa")
            ref_formatted_path = os.path.join(self.temp_dir, f"{ref_seq_file_name}_formatted_headers.fa")
            concatenated_path = os.path.join(self.temp_dir, f"{seq_file_name}_RefAndCandidates.fa")

            # Rename duplicates and format files
            self.rename_duplicates(self.seq_file, seq_modify_path)
            self.rename_duplicates(self.ref_seq_file, ref_seq_modify_path)
            self.format_file(seq_modify_path, seq_formatted_path)
            self.format_file(ref_seq_modify_path, ref_formatted_path)
            self.concatenate_files(seq_formatted_path, ref_formatted_path, concatenated_path)

            # File paths for MUSCLE and TRIMAL steps
            seq_aln_file = os.path.join(self.temp_dir, f"{seq_file_name}_1_candidates_sequences.fa.aln")
            ref_aln_file = os.path.join(self.temp_dir, f"{seq_file_name}_1_reference_sequences.fa.aln")
            seq_trimmed_file = os.path.join(self.temp_dir, f"{seq_file_name}_1_candidates.fa.aln.trim50")
            seq_trimmed_file_2 = os.path.join(self.temp_dir, f"{seq_file_name}_2_candidates.fa.aln.trim50.aln.trim")
            seq_trimmed_file_3 = os.path.join(self.temp_dir, f"{seq_file_name}_3_candidates.fa.aln.trim50.aln.trim")
            seq_trimmed_file_4 = os.path.join(self.temp_dir, f"{seq_file_name}_4_candidates.fa.aln.trim50.aln.trim")
            seq_trimmed_file_5 = os.path.join(self.temp_dir, f"{seq_file_name}_5_candidates.fa.aln.trim50.aln.trim")
            seq_trimmed_file_6 = os.path.join(self.temp_dir, f"{seq_file_name}_6_candidates.fa.aln.trim50.aln.trim")
            seq_trimmed_file_7 = os.path.join(self.temp_dir, f"{seq_file_name}_7_candidates.fa.aln.trim50.aln.trim")
            seq_file_2 = os.path.join(self.temp_dir, f"{seq_file_name}_2_candidates.fa.aln.trim50.aln")
            seq_file_3 = os.path.join(self.temp_dir, f"{seq_file_name}_3_candidates.fa.aln.trim50.aln")
            seq_file_4 = os.path.join(self.temp_dir, f"{seq_file_name}_4_candidates.fa.aln.trim50.aln")
            seq_file_5 = os.path.join(self.temp_dir, f"{seq_file_name}_5_candidates.fa.aln.trim50.aln")
            seq_file_6 = os.path.join(self.temp_dir, f"{seq_file_name}_6_candidates.fa.aln.trim50.aln")
            seq_file_7 = os.path.join(self.temp_dir, f"{seq_file_name}_7_candidates.fa.aln.trim50.aln")
            seq_file_8 = os.path.join(self.temp_dir, f"{seq_file_name}_8_candidates.fa.aln.trim50.aln")
            seq_file_con = os.path.join(self.temp_dir, f"{seq_file_name}_RefAndcandidates.fa")
            seq_file_bp = os.path.join(self.temp_dir, f"{seq_file_name}_bp_RefAndcandidates.fa.aln")
            gblocks_output_file = os.path.join(self.temp_dir, f"{seq_file_name}_RefAndcandidates.fa.aln-gb")
            gblock_file = os.path.join(self.output_dir, f"{seq_file_name}_file_gb_MSA.fa")
            ref_trimmed_file = os.path.join(self.temp_dir, f"{seq_file_name}_1_reference.fa.aln.trim50")
            trimmed_candidates_file = os.path.join(self.temp_dir, f"{seq_file_name}_trimmed_candidates_file")
            trimmed_reference_file = os.path.join(self.temp_dir, f"{seq_file_name}_trimmed_reference.fa")
            filtered_2_candidates = os.path.join(self.temp_dir, f"{seq_file_name}_filtered_2_candidates.fa")
            filtered_3_candidates = os.path.join(self.temp_dir, f"{seq_file_name}_filtered_3_candidates.fa")
            filtered_4_candidates = os.path.join(self.temp_dir, f"{seq_file_name}_filtered_4_candidates.fa")
            filtered_5_candidates = os.path.join(self.temp_dir, f"{seq_file_name}_filtered_5_candidates.fa")
            filtered_6_candidates = os.path.join(self.temp_dir, f"{seq_file_name}_filtered_6_candidates.fa")
            filtered_7_candidates = os.path.join(self.temp_dir, f"{seq_file_name}_filtered_7_candidates.fa")

            # Step 1: MUSCLE alignment
            if self.stop_requested:
                self.stopped_signal.emit()
                return
            self.run_command(f'"{muscle_dir}" -super5 "{seq_formatted_path}" -output "{seq_aln_file}" -threads 56')
            self.run_command(f'"{muscle_dir}" -super5 "{ref_formatted_path}" -output "{ref_aln_file}" -threads 56')

            # Step 1: TRIMAL trimming
            if self.stop_requested:
                self.stopped_signal.emit()
                return
            self.run_command(f'"{trimal_dir}" -in "{seq_aln_file}" -out "{seq_trimmed_file}" -htmlout "{os.path.join(self.temp_dir, seq_file_name + "_output1.html")}" -resoverlap 0.75 -seqoverlap 50')
            self.remove_short_sequences(seq_trimmed_file, trimmed_candidates_file)
            self.run_command(f'"{trimal_dir}" -in "{ref_aln_file}" -out "{ref_trimmed_file}" -htmlout "{os.path.join(self.temp_dir, seq_file_name + "_output1.1.html")}" -resoverlap 0.75 -seqoverlap 50')
            self.remove_short_sequences(ref_trimmed_file, trimmed_reference_file)

            # Step 2
            if self.stop_requested:
                self.stopped_signal.emit()
                return
            self.run_command(f'"{muscle_dir}" -super5 "{trimmed_candidates_file}" -output "{seq_file_2}" -threads 56')
            self.run_command(f'"{trimal_dir}" -in "{seq_file_2}" -out "{seq_trimmed_file_2}" -htmlout "{os.path.join(self.temp_dir, seq_file_name + "_output2.html")}" -gt 0.5')
            self.remove_short_sequences(seq_trimmed_file_2, filtered_2_candidates)

            # Step 3
            if self.stop_requested:
                self.stopped_signal.emit()
                return
            self.run_command(f'"{muscle_dir}" -super5 "{filtered_2_candidates}" -output "{seq_file_3}" -threads 56')
            self.run_command(f'"{trimal_dir}" -in "{seq_file_3}" -out "{seq_trimmed_file_3}" -htmlout "{os.path.join(self.temp_dir, seq_file_name + "_output3.html")}" -resoverlap 0.50 -seqoverlap 45')
            self.remove_short_sequences(seq_trimmed_file_3, filtered_3_candidates)

            # Step 4
            if self.stop_requested:
                self.stopped_signal.emit()
                return
            self.run_command(f'"{muscle_dir}" -super5 "{filtered_3_candidates}" -output "{seq_file_4}" -threads 56')
            self.run_command(f'"{trimal_dir}" -in "{seq_file_4}" -out "{seq_trimmed_file_4}" -htmlout "{os.path.join(self.temp_dir, f"{seq_file_name}_output4.html")}" -resoverlap 0.50 -seqoverlap 45')
            self.remove_short_sequences(seq_trimmed_file_4, filtered_4_candidates)

            # Step 5
            if self.stop_requested:
                self.stopped_signal.emit()
                return
            self.run_command(f'"{muscle_dir}" -super5 "{filtered_4_candidates}" -output "{seq_file_5}" -threads 56')
            self.run_command(f'"{trimal_dir}" -in "{seq_file_5}" -out "{seq_trimmed_file_5}" -htmlout "{os.path.join(self.temp_dir, f"{seq_file_name}_output5.html")}" -resoverlap 0.55 -seqoverlap 50')
            self.remove_short_sequences(seq_trimmed_file_5, filtered_5_candidates)

            # Step 6
            if self.stop_requested:
                self.stopped_signal.emit()
                return
            self.run_command(f'"{muscle_dir}" -super5 "{filtered_5_candidates}" -output "{seq_file_6}" -threads 56')
            self.run_command(f'"{trimal_dir}" -in "{seq_file_6}" -out "{seq_trimmed_file_6}" -htmlout "{os.path.join(self.temp_dir, f"{seq_file_name}_output6.html")}" -resoverlap 0.55 -seqoverlap 60')
            self.remove_short_sequences(seq_trimmed_file_6, filtered_6_candidates)

            # Step 7
            if self.stop_requested:
                self.stopped_signal.emit()
                return
            self.run_command(f'"{muscle_dir}" -super5 "{filtered_6_candidates}" -output "{seq_file_7}" -threads 56')
            self.run_command(f'"{trimal_dir}" -in "{seq_file_7}" -out "{seq_trimmed_file_7}" -htmlout "{os.path.join(self.temp_dir, f"{seq_file_name}_output7.html")}" -resoverlap 0.55 -seqoverlap 65')
            self.remove_short_sequences(seq_trimmed_file_7, filtered_7_candidates)

            # Step 8
            if self.stop_requested:
                self.stopped_signal.emit()
                return
            self.run_command(f'"{muscle_dir}" -super5 "{filtered_7_candidates}" -output "{seq_file_8}" -threads 56')

            # Step 9: Concatenate
            if self.stop_requested:
                self.stopped_signal.emit()
                return
            self.concatenate_files(seq_file_8, trimmed_reference_file, seq_file_con)

            # Step 10: MUSCLE on concatenated file
            if self.stop_requested:
                self.stopped_signal.emit()
                return
            self.run_command(f'"{muscle_dir}" -super5 "{seq_file_con}" -output "{seq_file_bp}" -threads 56')

            # Step 11: Modify headers
            modified_output_file = os.path.join(self.output_dir, f"{seq_file_name}_RefAndcandidates.fa.aln")
            self.modify_headers(seq_file_bp, modified_output_file)
            num_seqs = self.count_seq(modified_output_file)
            half_num_seqs = (num_seqs // 2) + 1

            # Step 12: GBlocks
            if self.stop_requested:
                self.stopped_signal.emit()
                return
            self.run_gblocks(gblocks_dir, modified_output_file, gblock_file, half_num_seqs)

            # Step 13: IQTree
            if self.stop_requested:
                self.stopped_signal.emit()
                return
            iqtree_command = f'"{iqtree_dir}" -s "{gblock_file}" -nt "AUTO"'
            if self.bootstrap_value:
                iqtree_command += f" -b {self.bootstrap_value}"
            if self.model:
                iqtree_command += f' -m "{self.model}"'
            self.run_command(iqtree_command)

            # Store the tree file path
            self.output_tree_file = f"{gblock_file}.treefile"

            # Parse best-fit model
            best_fit_model = self.extract_best_fit_model()
            if not self.user_selected_model and best_fit_model:
                self.progress_signal.emit("Analysis Complete", f"Best-fit model: {best_fit_model}\nOutput: {gblock_file}")
            elif not best_fit_model:
                self.progress_signal.emit("Analysis Complete", f"Output: {gblock_file}")

            # Move IQTree outputs to temp
            iqtree_files = [
                f"{gblock_file}.bionj", f"{gblock_file}.ckp.gz", f"{gblock_file}.model.gz",
                f"{gblock_file}.iqtree", f"{gblock_file}.mldist", f"{gblock_file}.log"
            ]
            for iqtree_file in iqtree_files:
                self.move_to_temp(iqtree_file)

            # Cleanup
            self.cleanup_temp_dir()

        except Exception as e:
            if not self.stop_requested:  # Only log errors if not stopped by user
                self.log_error(str(e))
                self.progress_signal.emit(f"Error during execution: {str(e)}", "Check log_file.log and error.log for details.")

    def stop(self):
        self.stop_requested = True
        if self.process:
            self.process.terminate()
            self.process.wait()
        self.cleanup_temp_dir()  # Clean up temp files on stop
        self.stopped_signal.emit()

    def extract_best_fit_model(self):
        try:
            with open(self.log_file, "r") as log_file:
                for line in log_file:
                    if "Best-fit model:" in line:
                        return line.split("Best-fit model:")[1].strip()
        except Exception as e:
            logging.error(f"Failed to read or parse log file: {e}")
        return None

    def rename_duplicates(self, input_file, output_file):
        header_count = {}
        renamed_records = []
        with open(input_file, "r") as in_file:
            for record in SeqIO.parse(in_file, "fasta"):
                header = record.id
                if header not in header_count:
                    header_count[header] = 1
                    new_header = header
                else:
                    header_count[header] += 1
                    new_header = f"{header}_{header_count[header]}"
                renamed_records.append(f">{new_header}\n{record.seq}")
        with open(output_file, "w") as out_file:
            out_file.write("\n".join(renamed_records))
        logging.info(f"Renamed sequences written to {output_file}")

    def format_file(self, input_file, formatted_file):
        with open(input_file, "r") as infile, open(formatted_file, "w") as outfile:
            for line in infile:
                if line.startswith(">"):
                    line = re.sub(r"\|\*\|", "_", line)
                    line = re.sub(r" .*", "", line)
                outfile.write(line)

    def concatenate_files(self, file1, file2, output_file):
        with open(output_file, "w") as out_f:
            for file in [file1, file2]:
                with open(file, "r") as f:
                    out_f.write(f.read())
        logging.info(f"Concatenated file written to {output_file}")

    def count_seq(self, input_file):
        return sum(1 for _ in SeqIO.parse(input_file, "fasta"))

    def remove_short_sequences(self, input_file, output_file, min_len=3):
        try:
            has_valid_sequence = False
            with open(output_file, "w") as out_file:
                for record in SeqIO.parse(input_file, "fasta"):
                    seq = str(record.seq).replace("-", "")
                    if len(seq) >= min_len:
                        SeqIO.write(record, out_file, "fasta")
                        has_valid_sequence = True
            if not has_valid_sequence:
                logging.warning(f"No sequences longer than {min_len} found. Program will now terminate.")
                sys.exit(1)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            sys.exit(1)

    def modify_headers(self, input_file, output_file):
        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            for line in infile:
                if line.startswith(">"):
                    line = re.sub(r" .*\n", "\n", line)
                outfile.write(line)

    def log_error(self, message):
        with open(self.error_log_path, "w") as error_log:
            error_log.write(message + "\n")

    def run_command(self, command, is_gblocks=False):
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
                    if self.process.returncode == 1 and is_gblocks:
                        logging.info("Gblocks returned 1 but it is treated as success.")
                    else:
                        raise RuntimeError(f"Command failed with return code {self.process.returncode}: {stderr}")
        except Exception as e:
            self.log_error(str(e))
            self.progress_signal.emit("Command encountered an error", "Please check the log for details.")
            logging.error(f"An error occurred while running the command: {e}")
            raise e

    def run_gblocks(self, gblocks_dir, modified_output_file, gblock_file, half_num_seqs):
        command = f'"{gblocks_dir}" "{modified_output_file}" -t=p -b1={half_num_seqs} -b2={half_num_seqs} -b3=8 -b4=5 -b5=a'
        self.run_command(command, is_gblocks=True)
        original_gb_file = f"{modified_output_file}-gb"
        original_htm_file = f"{modified_output_file}-gb.htm"
        if os.path.exists(original_gb_file):
            output_gb_file_in_output_dir = os.path.join(self.temp_dir, os.path.basename(original_gb_file))
            shutil.move(original_gb_file, output_gb_file_in_output_dir)
            logging.info(f"Moved Gblocks output to {output_gb_file_in_output_dir}")
            self.modify_gblocks_output(output_gb_file_in_output_dir, gblock_file)
        else:
            logging.error(f"Gblocks output file not found: {original_gb_file}")
        if os.path.exists(original_htm_file):
            output_htm_file_in_output_dir = os.path.join(self.temp_dir, os.path.basename(original_htm_file))
            shutil.move(original_htm_file, output_htm_file_in_output_dir)
            logging.info(f"Moved Gblocks HTML summary to {output_htm_file_in_output_dir}")
        else:
            logging.error(f"Gblocks HTML summary file not found: {original_htm_file}")

    def modify_gblocks_output(self, input_file, output_file):
        try:
            with open(input_file, "r") as infile, open(output_file, "w") as outfile:
                for line in infile:
                    if not line.startswith(">") and line.strip():
                        updated_line = re.sub(r"\s+", "", line)
                        outfile.write(updated_line + "\n")
                    else:
                        outfile.write(line)
        except Exception as e:
            logging.error(f"Error modifying GBlocks output: {e}")

    def cleanup_temp_dir(self):
        try:
            shutil.rmtree(self.temp_dir)
            logging.info(f"Successfully removed temporary directory: {self.temp_dir}")
        except Exception as e:
            logging.error(f"Failed to remove temporary directory: {e}")

    def move_to_temp(self, file_path):
        if os.path.exists(file_path):
            shutil.move(file_path, self.temp_dir)
            logging.info(f"Moved {file_path} to {self.temp_dir}")

class FastaApp(QWidget):
    DNA_MODELS = ["HKY", "GTR", "JC", "TN", "SYM"]
    PROTEIN_MODELS = ["LG", "EHO", "GTR20"]

    def __init__(self):
        super().__init__()
        self.thread = None
        self.last_output_file = None
        self.last_tree_file = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Genome Wide WorkBench")
        self.setWindowIcon(QIcon('src/image.png'))
        self.setGeometry(100, 100, 1000, 800)

        # Header
        self.header_label = QLabel("Phylogenetic Analysis")
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
        self.header_label.setFixedHeight(100)

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
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

        self.load_seq_file_button = QPushButton("Select Sequence FASTA File")
        self.load_seq_file_button.setFixedSize(240, 70)
        self.load_seq_file_button.setIcon(QIcon("upload_icon.png"))
        self.load_seq_file_button.setStyleSheet("""
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
        self.load_seq_file_button.clicked.connect(self.open_seq_file_dialog)
        self.file_layout.addWidget(self.load_seq_file_button)
        self.layout.addLayout(self.file_layout)

        # Reference sequence
        self.ref_file_layout = QHBoxLayout()
        self.ref_seq_file_display = QLineEdit(self)
        self.ref_seq_file_display.setReadOnly(True)
        self.ref_seq_file_display.setPlaceholderText("No reference file chosen")
        self.ref_seq_file_display.setFixedWidth(self.input_width)
        self.ref_seq_file_display.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2C3E50;
                padding: 5px;
                font-size: 14px;
                border-radius: 4px;
            }
        """)
        self.ref_file_layout.addWidget(self.ref_seq_file_display)

        self.load_ref_seq_file_button = QPushButton("Select Reference FASTA File")
        self.load_ref_seq_file_button.setFixedSize(240, 70)
        self.load_ref_seq_file_button.setIcon(QIcon("upload_icon.png"))
        self.load_ref_seq_file_button.setStyleSheet("""
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
        self.load_ref_seq_file_button.clicked.connect(self.open_ref_seq_file_dialog)
        self.ref_file_layout.addWidget(self.load_ref_seq_file_button)
        self.layout.addLayout(self.ref_file_layout)

        # Output directory
        self.dir_layout = QHBoxLayout()
        self.dir_display = QLineEdit(self)
        self.dir_display.setReadOnly(True)
        self.dir_display.setPlaceholderText("No output directory chosen")
        self.dir_display.setFixedWidth(self.input_width)
        self.dir_display.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2C3E50;
                padding: 10px;
                font-size: 14px;
                border-radius: 4px;
            }
        """)
        self.dir_layout.addWidget(self.dir_display)

        self.load_output_button = QPushButton("Select Output Directory")
        self.load_output_button.setFixedSize(240, 70)
        self.load_output_button.setIcon(QIcon("folder_icon.png"))
        self.load_output_button.setStyleSheet("""
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
        self.load_output_button.clicked.connect(self.open_output_dir_dialog)
        self.dir_layout.addWidget(self.load_output_button)
        self.layout.addLayout(self.dir_layout)

        # Bootstrap value
        self.bootstrap_layout = QHBoxLayout()
        self.bootstrap_layout.addStretch(1)
        self.bootstrap_label = QLabel("Bootstrap Value (optional):")
        self.bootstrap_label.setStyleSheet("font-size: 16px; padding: 10px;")
        self.bootstrap_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bootstrap_layout.addWidget(self.bootstrap_label)
        self.bootstrap_layout.addSpacing(400)
        self.bootstrap_input = QLineEdit(self)
        self.bootstrap_input.setPlaceholderText("Leave empty for default")
        self.bootstrap_input.setFixedWidth(230)
        self.bootstrap_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2C3E50;
                padding: 10px;
                font-size: 14px;
                border-radius: 4px;
            }
        """)
        self.bootstrap_layout.addWidget(self.bootstrap_input)
        self.bootstrap_layout.addStretch(1)
        self.layout.addLayout(self.bootstrap_layout)

        # Model selection
        self.model_layout = QHBoxLayout()
        self.model_layout.addStretch(1)
        self.model_label = QLabel("Model Selection (optional):")
        self.model_label.setStyleSheet("font-size: 16px; padding: 10px;")
        self.model_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.model_layout.addWidget(self.model_label)
        self.model_layout.addSpacing(400)
        self.model_combo = QComboBox(self)
        self.model_combo.setFixedWidth(200)
        self.model_combo.currentTextChanged.connect(self.toggle_custom_model_input)
        self.model_layout.addWidget(self.model_combo)
        self.model_layout.addStretch(1)
        self.custom_model_input = QLineEdit(self)
        self.custom_model_input.setPlaceholderText("Enter custom model if needed")
        self.custom_model_input.setVisible(False)
        self.model_layout.addWidget(self.custom_model_input)
        self.layout.addLayout(self.model_layout)

        # Button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()

        # Submit button
        self.rename_button = QPushButton("Submit")
        self.rename_button.setFixedSize(200, 50)
        self.rename_button.setStyleSheet("""
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
        self.rename_button.clicked.connect(self.start_renaming)
        self.button_layout.addWidget(self.rename_button)

        # Stop button
        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedSize(200, 50)
        self.stop_button.setStyleSheet("""
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
        
        self.aliview_button = QPushButton("View Alignment in AliView")
        self.aliview_button.setFixedSize(200, 50)
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
        
        self.dendroscope_button = QPushButton("View Tree in Dendroscope")
        self.dendroscope_button.setFixedSize(200, 50)
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
            self.update_model_dropdown(file_name)

    def open_ref_seq_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Reference FASTA File", "", "FASTA Files (*.fa *.fasta);;All Files (*)")
        if file_name:
            self.ref_seq_file_display.setText(file_name)

    def open_output_dir_dialog(self):
        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if output_dir:
            self.dir_display.setText(output_dir)

    def update_model_dropdown(self, file_name):
        is_dna = self.is_dna_sequence(file_name)
        self.model_combo.clear()
        models = self.DNA_MODELS if is_dna else self.PROTEIN_MODELS
        self.model_combo.addItem("")
        self.model_combo.addItems(models)
        self.model_combo.addItem("Other...")

    def is_dna_sequence(self, file_name):
        try:
            with open(file_name, "r") as f:
                for line in f:
                    if line.startswith(">"):
                        continue
                    if any(char in line for char in "EFILPQZ"):
                        return False
            return True
        except Exception as e:
            QMessageBox.warning(self, "File Error", f"Error reading sequence file: {e}")
            return True

    def toggle_custom_model_input(self, text):
        self.custom_model_input.setVisible(text == "Other...")
        if text != "Other...":
            self.custom_model_input.clear()

    def start_renaming(self):
        seq_file = self.seq_file_display.text()
        ref_seq_file = self.ref_seq_file_display.text()
        output_dir = self.dir_display.text()
        bootstrap_value = self.bootstrap_input.text()
        selected_model = self.model_combo.currentText()

        if selected_model == "Other...":
            selected_model = self.custom_model_input.text().strip() or None

        if not seq_file or not ref_seq_file or not output_dir:
            QMessageBox.warning(self, "Input Error", "Please provide all required input files and output directory.")
            return
        if bootstrap_value and not bootstrap_value.isdigit():
            QMessageBox.warning(self, "Input Error", "Bootstrap value must be a positive integer.")
            return

        user_selected_model = bool(selected_model)

        self.rename_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.aliview_button.setEnabled(False)
        self.dendroscope_button.setEnabled(False)
        self.thread = RenameThread(
            seq_file, ref_seq_file, output_dir,
            bootstrap_value=int(bootstrap_value) if bootstrap_value else None,
            model=selected_model,
            user_selected_model=user_selected_model
        )
        self.thread.progress_signal.connect(self.on_progress)
        self.thread.stopped_signal.connect(self.on_stopped)
        self.thread.start()

    def stop_process(self):
        if self.thread:
            self.thread.stop()

    def on_stopped(self):
        self.stop_button.setEnabled(False)
        self.rename_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        QMessageBox.information(self, "Process Stopped", "The process was stopped by the user.")

    def on_progress(self, message, file_path):
        self.stop_button.setEnabled(False)
        self.rename_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.last_output_file = file_path
        self.last_tree_file = self.thread.output_tree_file if hasattr(self.thread, 'output_tree_file') else None
        
        # Enable visualization buttons if we have the files
        self.aliview_button.setEnabled(os.path.exists(self.last_output_file))
        self.dendroscope_button.setEnabled(self.last_tree_file and os.path.exists(self.last_tree_file))
        
        QMessageBox.information(self, "Process Completed", f"{message}\nOutput file: {file_path}")

    def open_aliview(self):
        if self.last_output_file and os.path.exists(self.last_output_file):
            # Open AliView website or launch application if installed
            webbrowser.open("https://ormbunkar.se/aliview/")
        else:
            QMessageBox.warning(self, "File Not Found", "The alignment output file doesn't exist.")

    def open_dendroscope(self):
        if self.last_tree_file and os.path.exists(self.last_tree_file):
            # Open Dendroscope website or launch application if installed
            webbrowser.open("https://software-ab.informatik.uni-tuebingen.de/download/dendroscope/welcome.html")
        else:
            QMessageBox.warning(self, "File Not Found", "The phylogenetic tree file doesn't exist.")

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
            if self.thread:
                self.thread.stop()
            event.accept()
        elif msg_box.clickedButton() == minimize_button:
            event.ignore()
            self.showMinimized()
        else:
            event.ignore()
        self.seq_file_display.setText("No file chosen")
        self.ref_seq_file_display.setText("No file chosen")
        self.dir_display.setText("No directory chosen")
        self.rename_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication([])
    window = FastaApp()
    window.show()
    app.exec()