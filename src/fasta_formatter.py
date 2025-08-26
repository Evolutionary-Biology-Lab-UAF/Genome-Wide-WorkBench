# import sys
# import re
# from PySide6.QtWidgets import (
#     QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, 
#     QHBoxLayout, QWidget, QLabel, QComboBox, QFileDialog, QMessageBox, QScrollArea
# )
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QIcon, QFont

# class FastaValidatorApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Genome Wide WorkBench")
#         self.setWindowIcon(QIcon('src/image.png'))

#         self.setGeometry(100, 100, 1000, 1000)

#         # Central widget
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)

#         # Main layout
#         self.main_layout = QVBoxLayout(self.central_widget)

#         # Scroll area for main content
#         self.scroll_area = QScrollArea()
#         self.scroll_area.setWidgetResizable(True)
#         self.main_layout.addWidget(self.scroll_area)

#         # Scroll area widget contents
#         self.scroll_content = QWidget()
#         self.scroll_area.setWidget(self.scroll_content)
#         self.scroll_layout = QVBoxLayout(self.scroll_content)

#         # Title label
#         self.header_label = QLabel("FASTA Formatter")
#         self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.header_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
#         self.header_label.setStyleSheet("""QLabel {
#             background-color: #2C3E50;
#             color: white;
#             padding: 20px;
#             border-radius: 12px;
#         }""")
#         self.scroll_layout.addWidget(self.header_label)

#         # Text area for FASTA input
#         self.sequence_input = QTextEdit(self)
#         self.sequence_input.setPlaceholderText("Paste your FASTA sequence here...")
#         self.scroll_layout.addWidget(self.sequence_input)

#         # Validation label
#         self.validation_label = QLabel("")
#         self.scroll_layout.addWidget(self.validation_label)

#         # Format dropdown
#         self.format_dropdown = QComboBox(self)
#         self.format_dropdown.addItems([".fasta", ".fa", ".txt", ".fna"])
#         self.scroll_layout.addWidget(self.format_dropdown)

#         # Buttons layout
#         self.button_layout = QHBoxLayout()
#         self.validate_button = QPushButton("Format", self)
#         self.validate_button.clicked.connect(self.format_sequences)
#         self.save_button = QPushButton("Save & Download", self)
#         self.save_button.clicked.connect(self.save_and_download)
#         self.load_button = QPushButton("Load File", self)  # New Load button
#         self.load_button.clicked.connect(self.load_file)  # Connect the Load button to the function
#         self.button_layout.addWidget(self.load_button)
#         self.button_layout.addWidget(self.validate_button)
#         self.button_layout.addWidget(self.save_button)
#         self.scroll_layout.addLayout(self.button_layout)

#         # Set button styles
#         self.set_button_styles(self.validate_button)
#         self.set_button_styles(self.save_button)
#         self.set_button_styles(self.load_button)  # Style for the new Load button

#         # Add spacer at the end to push content upwards
#         self.scroll_layout.addStretch()

#     def set_button_styles(self, button):
#         button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
#         button.setStyleSheet("""
#     QPushButton {
#         font-size: 16px;
#         color: white;
#         background-color: #2C3E50;
#         border: none;
#         text-align: left;
#         padding: 10px 20px;
#     }
#     QPushButton:hover {
#         background-color: #34495E;
#     }
#         QPushButton:pressed {
#             background-color: #34495E;
#         }""")

#     def load_file(self):
#         # Open file dialog to select a FASTA file
#         file_path, _ = QFileDialog.getOpenFileName(self, "Open FASTA File", "", "FASTA Files (*.fasta *.fa *.txt *.fna)")
#         if not file_path:
#             return  # If no file is selected, exit the function

#         # Read the content of the file and display it in the sequence_input
#         with open(file_path, "r") as file:
#             fasta_content = file.read()

#         self.sequence_input.setPlainText(fasta_content)  # Load content into text area

#     def format_sequences(self):
#         fasta_text = self.sequence_input.toPlainText().strip()
        
#         if not fasta_text:
#             self.validation_label.setText("Error: No input provided.")
#             return

#         # Split input into lines
#         lines = fasta_text.splitlines()
#         formatted_sequences = []
        
#         current_header = None
#         current_sequence = ""

#         for line in lines:
#             line = line.strip()
#             if line.startswith(">"):  # New header
#                 if current_header:
#                     # If we already have a current header, add the previous sequence
#                     formatted_sequences.append(f"{current_header}\n{self.clean_sequence(current_sequence)}")
#                 current_header = line  # Set new header
#                 current_sequence = ""  # Reset sequence for new header
#             else:
#                 current_sequence += line  # Append sequence lines

#         # Add the last sequence if it exists
#         if current_header and current_sequence:
#             formatted_sequences.append(f"{current_header}\n{self.clean_sequence(current_sequence)}")

#         # Join all formatted sequences into a single string
#         cleaned_fasta = "\n".join(formatted_sequences)
#         self.sequence_input.setPlainText(cleaned_fasta)  # Update the text area

#         # Validate sequences
#         self.validate_sequences(formatted_sequences)

#     def clean_sequence(self, sequence):
#         # Remove spaces and special characters from the sequence
#         return re.sub(r"[^ACGTUacgtu]", "", sequence.replace(" ", "").replace("\n", ""))

#     def validate_sequences(self, formatted_sequences):
#         valid_dna = True
#         valid_rna = True
#         valid_protein = True
        
#         for seq in formatted_sequences:
#             header, sequence = seq.split("\n", 1)
#             # Check sequence types
#             if self.is_dna(sequence):
#                 valid_dna = True
#                 valid_rna = False
#                 valid_protein = False
#             elif self.is_rna(sequence):
#                 valid_dna = False
#                 valid_rna = True
#                 valid_protein = False
#             elif self.is_protein(sequence):
#                 valid_dna = False
#                 valid_rna = False
#                 valid_protein = True
#             else:
#                 valid_dna = False
#                 valid_rna = False
#                 valid_protein = False

#         if valid_dna:
#             self.validation_label.setText("Valid DNA sequences.")
#         elif valid_rna:
#             self.validation_label.setText("Valid RNA sequences.")
#         elif valid_protein:
#             self.validation_label.setText("Valid Protein sequences.")
#         else:
#             self.validation_label.setText("Error: No valid sequence type found.")

#     def is_dna(self, sequence):
#         return bool(re.match("^[ACGTacgt]+$", sequence))

#     def is_rna(self, sequence):
#         return bool(re.match("^[ACGUacgu]+$", sequence))

#     def is_protein(self, sequence):
#         return bool(re.match("^[ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy]+$", sequence))

#     def save_and_download(self):
#         # Open save dialog
#         save_path, _ = QFileDialog.getSaveFileName(
#             self, "Save File", "", f"FASTA Files (*{self.format_dropdown.currentText()})"
#         )
#         if not save_path:
#             return
        
#         # Save validated and cleaned sequence
#         with open(save_path, "w") as file:
#             file.write(self.sequence_input.toPlainText())
        
#         QMessageBox.information(self, "Success", "File saved successfully!")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = FastaValidatorApp()
#     window.show()
#     sys.exit(app.exec())


# import sys
# import os
# import pandas as pd
# from Bio import SeqIO
# from PySide6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QPushButton,
#     QFileDialog, QLabel, QTextEdit, QGroupBox,
#     QRadioButton, QButtonGroup, QProgressBar
# )
# from PySide6.QtCore import Qt

# class FastaFilterTool(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("FASTA Filter Tool - XLSX/TXT Edition")
#         self.setGeometry(100, 100, 900, 750)
        
#         # Main layout
#         layout = QVBoxLayout()
        
#         # File selection group
#         file_group = QGroupBox("Step 1: Select Input Files")
#         file_layout = QVBoxLayout()
        
#         # FASTA Input
#         self.fasta_label = QLabel("No FASTA file selected")
#         self.fasta_label.setStyleSheet("color: #666; font-style: italic;")
#         btn_fasta = QPushButton("Select Query FASTA (.fasta/.fa)")
#         btn_fasta.setStyleSheet("QPushButton { background-color: #3498db; color: white; }")
#         btn_fasta.clicked.connect(self.load_fasta)
        
#         # BLAST Input (XLSX)
#         self.blast_label = QLabel("No BLAST file selected (.xlsx)")
#         self.blast_label.setStyleSheet("color: #666; font-style: italic;")
#         btn_blast = QPushButton("Select BLAST Results (.xlsx)")
#         btn_blast.setStyleSheet("QPushButton { background-color: #2ecc71; color: white; }")
#         btn_blast.clicked.connect(self.load_blast)
        
#         # HMMER Input (TXT)
#         self.hmmer_label = QLabel("No HMMER file selected (.txt)")
#         self.hmmer_label.setStyleSheet("color: #666; font-style: italic;")
#         btn_hmmer = QPushButton("Select HMMER Results (.txt)")
#         btn_hmmer.setStyleSheet("QPushButton { background-color: #e74c3c; color: white; }")
#         btn_hmmer.clicked.connect(self.load_hmmer)
        
#         file_layout.addWidget(btn_fasta)
#         file_layout.addWidget(self.fasta_label)
#         file_layout.addWidget(btn_blast)
#         file_layout.addWidget(self.blast_label)
#         file_layout.addWidget(btn_hmmer)
#         file_layout.addWidget(self.hmmer_label)
#         file_group.setLayout(file_layout)
        
#         # Filter options group
#         filter_group = QGroupBox("Step 2: Select Filter Method")
#         filter_layout = QVBoxLayout()
        
#         self.option_blast = QRadioButton("Sequences with BLAST hits (from .xlsx)")
#         self.option_hmmer = QRadioButton("Sequences with HMMER hits (from .txt)") 
#         self.option_both = QRadioButton("Sequences with BOTH BLAST AND HMMER hits")
#         self.option_either = QRadioButton("Sequences with EITHER BLAST OR HMMER hits")
        
#         self.option_group = QButtonGroup()
#         self.option_group.addButton(self.option_blast)
#         self.option_group.addButton(self.option_hmmer)
#         self.option_group.addButton(self.option_both)
#         self.option_group.addButton(self.option_either)
#         self.option_blast.setChecked(True)
        
#         filter_layout.addWidget(self.option_blast)
#         filter_layout.addWidget(self.option_hmmer)
#         filter_layout.addWidget(self.option_both)
#         filter_layout.addWidget(self.option_either)
#         filter_group.setLayout(filter_layout)
        
#         # Progress bar
#         self.progress = QProgressBar()
#         self.progress.setAlignment(Qt.AlignCenter)
#         self.progress.setStyleSheet("""
#             QProgressBar {
#                 border: 2px solid grey;
#                 border-radius: 5px;
#                 text-align: center;
#             }
#             QProgressBar::chunk {
#                 background-color: #3498db;
#                 width: 10px;
#             }
#         """)
        
#         # Output console
#         self.output = QTextEdit()
#         self.output.setReadOnly(True)
#         self.output.setStyleSheet("""
#             QTextEdit {
#                 background-color: #f8f9fa;
#                 border: 1px solid #ddd;
#                 padding: 5px;
#             }
#         """)
        
#         # Run button
#         btn_run = QPushButton("Generate Filtered FASTA")
#         btn_run.setStyleSheet("""
#             QPushButton {
#                 background-color: #27ae60;
#                 color: white;
#                 font-weight: bold;
#                 padding: 10px;
#                 border-radius: 5px;
#             }
#             QPushButton:hover {
#                 background-color: #2ecc71;
#             }
#             QPushButton:disabled {
#                 background-color: #95a5a6;
#             }
#         """)
#         btn_run.clicked.connect(self.run_filter)
#         self.btn_run = btn_run
        
#         # Add widgets to layout
#         layout.addWidget(file_group)
#         layout.addWidget(filter_group)
#         layout.addWidget(self.progress)
#         layout.addWidget(btn_run)
#         layout.addWidget(self.output)
        
#         self.setLayout(layout)
#         self.update_ui_state()
    
#     def load_fasta(self):
#         path, _ = QFileDialog.getOpenFileName(
#             self, "Select FASTA File", "",
#             "FASTA Files (*.fasta *.fa);;All Files (*)"
#         )
#         if path:
#             self.fasta_path = path
#             self.fasta_label.setText(f"✓ {os.path.basename(path)}")
#             self.fasta_label.setStyleSheet("color: #27ae60; font-style: normal;")
#             self.update_ui_state()
    
#     def load_blast(self):
#         path, _ = QFileDialog.getOpenFileName(
#             self, "Select BLAST XLSX File", "",
#             "Excel Files (*.xlsx);;All Files (*)"
#         )
#         if path:
#             self.blast_path = path
#             self.blast_label.setText(f"✓ {os.path.basename(path)}")
#             self.blast_label.setStyleSheet("color: #27ae60; font-style: normal;")
#             self.update_ui_state()
    
#     def load_hmmer(self):
#         path, _ = QFileDialog.getOpenFileName(
#             self, "Select HMMER TXT File", "",
#             "Text Files (*.txt);;All Files (*)"
#         )
#         if path:
#             self.hmmer_path = path
#             self.hmmer_label.setText(f"✓ {os.path.basename(path)}")
#             self.hmmer_label.setStyleSheet("color: #27ae60; font-style: normal;")
#             self.update_ui_state()
    
#     def update_ui_state(self):
#         """Enable/disable options based on loaded files"""
#         blast_loaded = hasattr(self, 'blast_path')
#         hmmer_loaded = hasattr(self, 'hmmer_path')
        
#         self.option_blast.setEnabled(blast_loaded)
#         self.option_hmmer.setEnabled(hmmer_loaded)
#         self.option_both.setEnabled(blast_loaded and hmmer_loaded)
#         self.option_either.setEnabled(blast_loaded and hmmer_loaded)
        
#         # Enable run button only when FASTA and at least one other file is loaded
#         self.btn_run.setEnabled(hasattr(self, 'fasta_path') and (blast_loaded or hmmer_loaded))
    
#     def parse_blast_xlsx(self):
#         """Parse BLAST results from XLSX file with error handling"""
#         try:
#             # Try reading Excel file
#             df = pd.read_excel(self.blast_path)
            
#             # Check for required column
#             if 'QuerySeq.ID' not in df.columns:
#                 self.output.append("❌ Error: BLAST file missing 'QuerySeq.ID' column")
#                 return set()
                
#             return set(df['QuerySeq.ID'].dropna().unique())
            
#         except Exception as e:
#             self.output.append(f"❌ BLAST XLSX Error: {str(e)}")
#             return set()
    
#     def parse_hmmer_txt(self):
#         """Parse HMMER results from TXT file with error handling"""
#         hmmer_seqs = set()
#         try:
#             with open(self.hmmer_path, 'r', encoding='utf-8') as f:
#                 for line in f:
#                     line = line.strip()
#                     if line and not line.startswith('#'):
#                         parts = line.split()
#                         if parts:  # Skip empty lines
#                             hmmer_seqs.add(parts[0])  # Target name
#             return hmmer_seqs
            
#         except Exception as e:
#             self.output.append(f"❌ HMMER TXT Error: {str(e)}")
#             return set()
    
#     def run_filter(self):
#         if not hasattr(self, 'fasta_path'):
#             self.output.append("❌ Error: No FASTA file selected!")
#             return
            
#         self.output.clear()
#         self.progress.setValue(0)
#         self.output.append("🚀 Starting FASTA filtering process...")
        
#         try:
#             # Parse input files with progress updates
#             self.output.append("\n🔍 Parsing input files...")
#             self.progress.setValue(10)
            
#             blast_seqs = set()
#             if hasattr(self, 'blast_path'):
#                 blast_seqs = self.parse_blast_xlsx()
#                 self.output.append(f"  - Found {len(blast_seqs)} BLAST hits")
            
#             hmmer_seqs = set()
#             if hasattr(self, 'hmmer_path'):
#                 hmmer_seqs = self.parse_hmmer_txt()
#                 self.output.append(f"  - Found {len(hmmer_seqs)} HMMER hits")
            
#             self.progress.setValue(30)
            
#             # Determine filter logic
#             if self.option_blast.isChecked():
#                 selected_seqs = blast_seqs
#                 method = "blast_only"
#                 method_display = "BLAST hits only"
#                 self.output.append("\n🔧 Filter: Keeping sequences with BLAST hits")
#             elif self.option_hmmer.isChecked():
#                 selected_seqs = hmmer_seqs
#                 method = "hmmer_only"
#                 method_display = "HMMER hits only"
#                 self.output.append("\n🔧 Filter: Keeping sequences with HMMER hits")
#             elif self.option_both.isChecked():
#                 selected_seqs = blast_seqs & hmmer_seqs
#                 method = "both"
#                 method_display = "BOTH BLAST AND HMMER hits"
#                 self.output.append("\n🔧 Filter: Keeping sequences with BOTH BLAST AND HMMER hits")
#             else:
#                 selected_seqs = blast_seqs | hmmer_seqs
#                 method = "either"
#                 method_display = "EITHER BLAST OR HMMER hits"
#                 self.output.append("\n🔧 Filter: Keeping sequences with EITHER BLAST OR HMMER hits")
            
#             # Generate output filename
#             base_name = os.path.splitext(os.path.basename(self.fasta_path))[0]
#             output_path = f"{base_name}_filtered_{method}.fasta"
            
#             # Filter FASTA
#             self.output.append(f"\n✂️ Filtering FASTA file...")
#             self.progress.setValue(40)
            
#             total = 0
#             kept = 0
            
#             with open(output_path, 'w', encoding='utf-8') as out:
#                 for record in SeqIO.parse(self.fasta_path, "fasta"):
#                     total += 1
#                     if record.id in selected_seqs:
#                         SeqIO.write(record, out, "fasta")
#                         kept += 1
                    
#                     # Update progress every 100 sequences
#                     if total % 100 == 0:
#                         progress_value = 40 + int(50 * (total/max(1,len(selected_seqs))))
#                         self.progress.setValue(min(progress_value, 90))
#                         self.output.append(f"  - Processed {total} sequences...")
            
#             # Generate statistics report with safe encoding
#             stats_path = f"{base_name}_filter_stats.txt"
#             try:
#                 with open(stats_path, 'w', encoding='utf-8') as f:
#                     f.write("FASTA Filtering Report\n")
#                     f.write("="*40 + "\n")
#                     f.write(f"Input FASTA: {os.path.basename(self.fasta_path)}\n")
#                     if hasattr(self, 'blast_path'):
#                         f.write(f"BLAST file: {os.path.basename(self.blast_path)}\n")
#                     if hasattr(self, 'hmmer_path'):
#                         f.write(f"HMMER file: {os.path.basename(self.hmmer_path)}\n")
#                     f.write(f"\nFilter Method: {method_display}\n")
#                     f.write(f"Total sequences: {total}\n")
#                     f.write(f"Sequences kept: {kept} ({kept/total:.1%})\n")
#                     if hasattr(self, 'blast_path'):
#                         f.write(f"Unique BLAST hits: {len(blast_seqs)}\n")
#                     if hasattr(self, 'hmmer_path'):
#                         f.write(f"Unique HMMER hits: {len(hmmer_seqs)}\n")
#                     if hasattr(self, 'blast_path') and hasattr(self, 'hmmer_path'):
#                         f.write(f"Overlap (BOTH): {len(blast_seqs & hmmer_seqs)}\n")
#             except UnicodeEncodeError:
#                 # Fallback for systems with strict encoding requirements
#                 with open(stats_path, 'w', encoding='ascii', errors='replace') as f:
#                     f.write("FASTA Filtering Report\n")
#                     f.write("="*40 + "\n")
#                     f.write(f"Input FASTA: {os.path.basename(self.fasta_path)}\n")
#                     if hasattr(self, 'blast_path'):
#                         f.write(f"BLAST file: {os.path.basename(self.blast_path)}\n")
#                     if hasattr(self, 'hmmer_path'):
#                         f.write(f"HMMER file: {os.path.basename(self.hmmer_path)}\n")
#                     f.write(f"\nFilter Method: {method_display}\n")
#                     f.write(f"Total sequences: {total}\n")
#                     f.write(f"Sequences kept: {kept} ({kept/total:.1%})\n")
#                     if hasattr(self, 'blast_path'):
#                         f.write(f"Unique BLAST hits: {len(blast_seqs)}\n")
#                     if hasattr(self, 'hmmer_path'):
#                         f.write(f"Unique HMMER hits: {len(hmmer_seqs)}\n")
#                     if hasattr(self, 'blast_path') and hasattr(self, 'hmmer_path'):
#                         f.write(f"Overlap (BOTH): {len(blast_seqs & hmmer_seqs)}\n")
            
#             self.progress.setValue(100)
#             self.output.append(f"\n✅ Successfully created filtered FASTA file!")
#             self.output.append(f"📄 Output file: {output_path}")
#             self.output.append(f"📊 Statistics saved to: {stats_path}")
#             self.output.append(f"\nSummary:")
#             self.output.append(f"- Total sequences: {total}")
#             self.output.append(f"- Sequences kept: {kept} ({kept/total:.1%})")
            
#         except Exception as e:
#             self.progress.setValue(0)
#             self.output.append(f"\n❌ Error during processing: {str(e)}")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = FastaFilterTool()
#     window.show()
#     sys.exit(app.exec())
# import sys
# import os
# import re
# import pandas as pd
# from Bio import SeqIO
# from PySide6.QtWidgets import (
#     QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout,
#     QHBoxLayout, QWidget, QLabel, QComboBox, QFileDialog,
#     QMessageBox, QScrollArea, QTabWidget, QRadioButton,
#     QButtonGroup, QProgressBar, QCheckBox, QGroupBox
# )
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QIcon, QFont

# class FastaFilterTool(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Genome Wide WorkBench")
#         self.setWindowIcon(QIcon('src/image.png'))
#         self.setGeometry(100, 100, 1000, 1000)

#         # Central widget
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)

#         # Main layout
#         self.main_layout = QVBoxLayout(self.central_widget)

#         # Scroll area for main content
#         self.scroll_area = QScrollArea()
#         self.scroll_area.setWidgetResizable(True)
#         self.main_layout.addWidget(self.scroll_area)

#         # Scroll area widget contents
#         self.scroll_content = QWidget()
#         self.scroll_area.setWidget(self.scroll_content)
#         self.scroll_layout = QVBoxLayout(self.scroll_content)

#         # Title label
#         self.header_label = QLabel("FASTA Filter Tool")
#         self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.header_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
#         self.header_label.setStyleSheet("""QLabel {
#             background-color: #2C3E50;
#             color: white;
#             padding: 20px;
#             border-radius: 12px;
#         }""")
#         self.scroll_layout.addWidget(self.header_label)

#         # Create tab widget
#         self.tabs = QTabWidget()
#         self.scroll_layout.addWidget(self.tabs)

#         # Create tabs
#         self.tab1 = QWidget()
#         self.tab2 = QWidget()
#         self.tab3 = QWidget()
        
#         self.tabs.addTab(self.tab1, "BLAST/HMMER Filter")
#         self.tabs.addTab(self.tab2, "Header List Filter")
#         self.tabs.addTab(self.tab3, "Sequence Validator")

#         # Setup all tabs
#         self.setup_blast_hmmer_tab()
#         self.setup_header_list_tab()
#         self.setup_validator_tab()

#         # Add spacer at the end to push content upwards
#         self.scroll_layout.addStretch()

#     def set_button_styles(self, button):
#         button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
#         button.setStyleSheet("""
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

#     def setup_blast_hmmer_tab(self):
#         """Setup the BLAST/HMMER filtering tab"""
#         layout = QVBoxLayout(self.tab1)

#         # File selection group
#         file_group = QGroupBox("Input Files")
#         file_layout = QVBoxLayout()
        
#         # FASTA Input
#         self.fasta_label = QLabel("No FASTA file selected")
#         self.fasta_label.setStyleSheet("color: #666; font-style: italic;")
#         btn_fasta = QPushButton("Select Query FASTA (.fasta/.fa)")
#         self.set_button_styles(btn_fasta)
#         btn_fasta.clicked.connect(self.load_fasta)
        
#         # BLAST Input (XLSX)
#         self.blast_label = QLabel("No BLAST file selected (.xlsx)")
#         self.blast_label.setStyleSheet("color: #666; font-style: italic;")
#         btn_blast = QPushButton("Select BLAST Results (.xlsx)")
#         self.set_button_styles(btn_blast)
#         btn_blast.clicked.connect(self.load_blast)
        
#         # HMMER Input (TXT)
#         self.hmmer_label = QLabel("No HMMER file selected (.txt)")
#         self.hmmer_label.setStyleSheet("color: #666; font-style: italic;")
#         btn_hmmer = QPushButton("Select HMMER Results (.txt)")
#         self.set_button_styles(btn_hmmer)
#         btn_hmmer.clicked.connect(self.load_hmmer)
        
#         file_layout.addWidget(btn_fasta)
#         file_layout.addWidget(self.fasta_label)
#         file_layout.addWidget(btn_blast)
#         file_layout.addWidget(self.blast_label)
#         file_layout.addWidget(btn_hmmer)
#         file_layout.addWidget(self.hmmer_label)
#         file_group.setLayout(file_layout)
        
#         # Filter options group
#         filter_group = QGroupBox("Filter Method")
#         filter_layout = QVBoxLayout()
        
#         self.option_blast = QRadioButton("BLAST hits only")
#         self.option_hmmer = QRadioButton("HMMER hits only") 
#         self.option_both = QRadioButton("Both BLAST AND HMMER hits")
#         self.option_either = QRadioButton("Either BLAST OR HMMER hits")
        
#         self.option_group = QButtonGroup()
#         self.option_group.addButton(self.option_blast)
#         self.option_group.addButton(self.option_hmmer)
#         self.option_group.addButton(self.option_both)
#         self.option_group.addButton(self.option_either)
#         self.option_blast.setChecked(True)
        
#         filter_layout.addWidget(self.option_blast)
#         filter_layout.addWidget(self.option_hmmer)
#         filter_layout.addWidget(self.option_both)
#         filter_layout.addWidget(self.option_either)
#         filter_group.setLayout(filter_layout)
        
#         # Progress bar
#         self.progress = QProgressBar()
#         self.progress.setAlignment(Qt.AlignCenter)
#         self.progress.setStyleSheet("""
#             QProgressBar {
#                 border: 2px solid #2C3E50;
#                 border-radius: 5px;
#                 text-align: center;
#             }
#             QProgressBar::chunk {
#                 background-color: #27ae60;
#             }
#         """)
        
#         # Output console
#         self.output = QTextEdit()
#         self.output.setReadOnly(True)
        
#         # Run button
#         btn_run = QPushButton("Generate Filtered FASTA")
#         self.set_button_styles(btn_run)
#         btn_run.clicked.connect(self.run_blast_hmmer_filter)
#         self.btn_run = btn_run
        
#         # Add widgets to layout
#         layout.addWidget(file_group)
#         layout.addWidget(filter_group)
#         layout.addWidget(self.progress)
#         layout.addWidget(btn_run)
#         layout.addWidget(self.output)

#     def setup_header_list_tab(self):
#         """Setup the header list filtering tab"""
#         layout = QVBoxLayout(self.tab2)
        
#         # File selection group
#         file_group = QGroupBox("Input Files")
#         file_layout = QVBoxLayout()
        
#         # FASTA Input
#         self.hl_fasta_label = QLabel("No FASTA file selected")
#         self.hl_fasta_label.setStyleSheet("color: #666; font-style: italic;")
#         btn_fasta = QPushButton("Select Query FASTA (.fasta/.fa)")
#         self.set_button_styles(btn_fasta)
#         btn_fasta.clicked.connect(self.load_hl_fasta)
        
#         # Header List Input
#         self.header_list_label = QLabel("No header list file selected (.txt)")
#         self.header_list_label.setStyleSheet("color: #666; font-style: italic;")
#         btn_header = QPushButton("Select Header List (.txt)")
#         self.set_button_styles(btn_header)
#         btn_header.clicked.connect(self.load_header_list)
        
#         file_layout.addWidget(btn_fasta)
#         file_layout.addWidget(self.hl_fasta_label)
#         file_layout.addWidget(btn_header)
#         file_layout.addWidget(self.header_list_label)
#         file_group.setLayout(file_layout)
        
#         # Options group
#         options_group = QGroupBox("Filter Options")
#         options_layout = QVBoxLayout()
        
#         self.case_sensitive = QCheckBox("Case-sensitive matching")
#         self.case_sensitive.setChecked(False)
        
#         self.partial_match = QCheckBox("Allow partial header matches")
#         self.partial_match.setChecked(False)
        
#         options_layout.addWidget(self.case_sensitive)
#         options_layout.addWidget(self.partial_match)
#         options_group.setLayout(options_layout)
        
#         # Progress bar
#         self.hl_progress = QProgressBar()
#         self.hl_progress.setAlignment(Qt.AlignCenter)
#         self.hl_progress.setStyleSheet("""
#             QProgressBar {
#                 border: 2px solid #2C3E50;
#                 border-radius: 5px;
#                 text-align: center;
#             }
#             QProgressBar::chunk {
#                 background-color: #27ae60;
#             }
#         """)
        
#         # Output console
#         self.hl_output = QTextEdit()
#         self.hl_output.setReadOnly(True)
        
#         # Run button
#         btn_run = QPushButton("Generate Filtered FASTA")
#         self.set_button_styles(btn_run)
#         btn_run.clicked.connect(self.run_header_list_filter)
#         self.hl_btn_run = btn_run
        
#         # Add widgets to layout
#         layout.addWidget(file_group)
#         layout.addWidget(options_group)
#         layout.addWidget(self.hl_progress)
#         layout.addWidget(btn_run)
#         layout.addWidget(self.hl_output)

#     def setup_validator_tab(self):
#         """Setup the sequence validator tab"""
#         layout = QVBoxLayout(self.tab3)
        
#         # Text area for FASTA input
#         self.sequence_input = QTextEdit()
#         self.sequence_input.setPlaceholderText("Paste your FASTA sequence here...")
        
#         # Validation label
#         self.validation_label = QLabel("")
#         self.validation_label.setStyleSheet("color: #E74C3C;")
        
#         # Format dropdown
#         self.format_dropdown = QComboBox()
#         self.format_dropdown.addItems([".fasta", ".fa", ".txt", ".fna"])
        
#         # Buttons layout
#         button_layout = QHBoxLayout()
#         self.load_button = QPushButton("Load File")
#         self.set_button_styles(self.load_button)
#         self.load_button.clicked.connect(self.load_file)
        
#         self.validate_button = QPushButton("Validate")
#         self.set_button_styles(self.validate_button)
#         self.validate_button.clicked.connect(self.validate_sequences)
        
#         self.save_button = QPushButton("Save")
#         self.set_button_styles(self.save_button)
#         self.save_button.clicked.connect(self.save_file)
        
#         button_layout.addWidget(self.load_button)
#         button_layout.addWidget(self.validate_button)
#         button_layout.addWidget(self.save_button)
        
#         # Output console
#         self.validator_output = QTextEdit()
#         self.validator_output.setReadOnly(True)
        
#         # Add widgets to layout
#         layout.addWidget(self.sequence_input)
#         layout.addWidget(self.validation_label)
#         layout.addWidget(self.format_dropdown)
#         layout.addLayout(button_layout)
#         layout.addWidget(self.validator_output)

#     def load_fasta(self):
#         path, _ = QFileDialog.getOpenFileName(
#             self, "Select FASTA File", "",
#             "FASTA Files (*.fasta *.fa);;All Files (*)"
#         )
#         if path:
#             self.fasta_path = path
#             self.fasta_label.setText(f"✓ {os.path.basename(path)}")
#             self.fasta_label.setStyleSheet("color: #27ae60; font-style: normal;")
#             self.update_ui_state()

#     def load_blast(self):
#         path, _ = QFileDialog.getOpenFileName(
#             self, "Select BLAST XLSX File", "",
#             "Excel Files (*.xlsx);;All Files (*)"
#         )
#         if path:
#             self.blast_path = path
#             self.blast_label.setText(f"✓ {os.path.basename(path)}")
#             self.blast_label.setStyleSheet("color: #27ae60; font-style: normal;")
#             self.update_ui_state()

#     def load_hmmer(self):
#         path, _ = QFileDialog.getOpenFileName(
#             self, "Select HMMER TXT File", "",
#             "Text Files (*.txt);;All Files (*)"
#         )
#         if path:
#             self.hmmer_path = path
#             self.hmmer_label.setText(f"✓ {os.path.basename(path)}")
#             self.hmmer_label.setStyleSheet("color: #27ae60; font-style: normal;")
#             self.update_ui_state()

#     def load_hl_fasta(self):
#         path, _ = QFileDialog.getOpenFileName(
#             self, "Select FASTA File", "",
#             "FASTA Files (*.fasta *.fa);;All Files (*)"
#         )
#         if path:
#             self.hl_fasta_path = path
#             self.hl_fasta_label.setText(f"✓ {os.path.basename(path)}")
#             self.hl_fasta_label.setStyleSheet("color: #27ae60; font-style: normal;")
#             self.update_hl_ui_state()

#     def load_header_list(self):
#         path, _ = QFileDialog.getOpenFileName(
#             self, "Select Header List File", "",
#             "Text Files (*.txt);;All Files (*)"
#         )
#         if path:
#             self.header_list_path = path
#             self.header_list_label.setText(f"✓ {os.path.basename(path)}")
#             self.header_list_label.setStyleSheet("color: #27ae60; font-style: normal;")
#             self.update_hl_ui_state()

#     def load_file(self):
#         path, _ = QFileDialog.getOpenFileName(
#             self, "Open FASTA File", "",
#             "FASTA Files (*.fasta *.fa *.txt *.fna)"
#         )
#         if path:
#             with open(path, "r") as file:
#                 fasta_content = file.read()
#             self.sequence_input.setPlainText(fasta_content)

#     def update_ui_state(self):
#         blast_loaded = hasattr(self, 'blast_path')
#         hmmer_loaded = hasattr(self, 'hmmer_path')
        
#         self.option_blast.setEnabled(blast_loaded)
#         self.option_hmmer.setEnabled(hmmer_loaded)
#         self.option_both.setEnabled(blast_loaded and hmmer_loaded)
#         self.option_either.setEnabled(blast_loaded and hmmer_loaded)
        
#         self.btn_run.setEnabled(hasattr(self, 'fasta_path') and (blast_loaded or hmmer_loaded))

#     def update_hl_ui_state(self):
#         fasta_loaded = hasattr(self, 'hl_fasta_path')
#         header_loaded = hasattr(self, 'header_list_path')
#         self.hl_btn_run.setEnabled(fasta_loaded and header_loaded)

#     def parse_blast_xlsx(self):
#         try:
#             df = pd.read_excel(self.blast_path)
#             if 'QuerySeq.ID' not in df.columns:
#                 self.output.append("❌ Error: BLAST file missing 'QuerySeq.ID' column")
#                 return set()
#             return set(df['QuerySeq.ID'].dropna().unique())
#         except Exception as e:
#             self.output.append(f"❌ BLAST XLSX Error: {str(e)}")
#             return set()

#     def parse_hmmer_txt(self):
#         hmmer_seqs = set()
#         try:
#             with open(self.hmmer_path, 'r', encoding='utf-8') as f:
#                 for line in f:
#                     line = line.strip()
#                     if line and not line.startswith('#'):
#                         parts = line.split()
#                         if parts:
#                             hmmer_seqs.add(parts[0])
#             return hmmer_seqs
#         except Exception as e:
#             self.output.append(f"❌ HMMER TXT Error: {str(e)}")
#             return set()

#     def parse_header_list(self):
#         headers = set()
#         try:
#             with open(self.header_list_path, 'r', encoding='utf-8') as f:
#                 for line in f:
#                     line = line.strip()
#                     if line:
#                         if not self.case_sensitive.isChecked():
#                             line = line.lower()
#                         headers.add(line)
#             return headers
#         except Exception as e:
#             self.hl_output.append(f"❌ Header List Error: {str(e)}")
#             return set()

#     def run_blast_hmmer_filter(self):
#         if not hasattr(self, 'fasta_path'):
#             self.output.append("❌ Error: No FASTA file selected!")
#             return
            
#         self.output.clear()
#         self.progress.setValue(0)
#         self.output.append("🚀 Starting FASTA filtering process...")
        
#         try:
#             self.output.append("\n🔍 Parsing input files...")
#             self.progress.setValue(10)
            
#             blast_seqs = set()
#             if hasattr(self, 'blast_path'):
#                 blast_seqs = self.parse_blast_xlsx()
#                 self.output.append(f"  - Found {len(blast_seqs)} BLAST hits")
            
#             hmmer_seqs = set()
#             if hasattr(self, 'hmmer_path'):
#                 hmmer_seqs = self.parse_hmmer_txt()
#                 self.output.append(f"  - Found {len(hmmer_seqs)} HMMER hits")
            
#             self.progress.setValue(30)
            
#             if self.option_blast.isChecked():
#                 selected_seqs = blast_seqs
#                 method = "blast_only"
#                 self.output.append("\n🔧 Filter: Keeping sequences with BLAST hits")
#             elif self.option_hmmer.isChecked():
#                 selected_seqs = hmmer_seqs
#                 method = "hmmer_only"
#                 self.output.append("\n🔧 Filter: Keeping sequences with HMMER hits")
#             elif self.option_both.isChecked():
#                 selected_seqs = blast_seqs & hmmer_seqs
#                 method = "both"
#                 self.output.append("\n🔧 Filter: Keeping sequences with BOTH BLAST AND HMMER hits")
#             else:
#                 selected_seqs = blast_seqs | hmmer_seqs
#                 method = "either"
#                 self.output.append("\n🔧 Filter: Keeping sequences with EITHER BLAST OR HMMER hits")
            
#             base_name = os.path.splitext(os.path.basename(self.fasta_path))[0]
#             output_path = f"{base_name}_filtered_{method}.fasta"
            
#             self.output.append(f"\n✂️ Filtering FASTA file...")
#             self.progress.setValue(40)
            
#             total = 0
#             kept = 0
            
#             with open(output_path, 'w', encoding='utf-8') as out:
#                 for record in SeqIO.parse(self.fasta_path, "fasta"):
#                     total += 1
#                     if record.id in selected_seqs:
#                         SeqIO.write(record, out, "fasta")
#                         kept += 1
                    
#                     if total % 100 == 0:
#                         progress_value = 40 + int(50 * (total/max(1,len(selected_seqs))))
#                         self.progress.setValue(min(progress_value, 90))
#                         self.output.append(f"  - Processed {total} sequences...")
            
#             stats_path = f"{base_name}_filter_stats.txt"
#             with open(stats_path, 'w', encoding='utf-8') as f:
#                 f.write("FASTA Filtering Report\n")
#                 f.write("="*40 + "\n")
#                 f.write(f"Input FASTA: {os.path.basename(self.fasta_path)}\n")
#                 if hasattr(self, 'blast_path'):
#                     f.write(f"BLAST file: {os.path.basename(self.blast_path)}\n")
#                 if hasattr(self, 'hmmer_path'):
#                     f.write(f"HMMER file: {os.path.basename(self.hmmer_path)}\n")
#                 f.write(f"\nFilter Method: {method.replace('_', ' ').title()}\n")
#                 f.write(f"Total sequences: {total}\n")
#                 f.write(f"Sequences kept: {kept} ({kept/total:.1%})\n")
            
#             self.progress.setValue(100)
#             self.output.append(f"\n✅ Successfully created filtered FASTA file!")
#             self.output.append(f"📄 Output file: {output_path}")
            
#         except Exception as e:
#             self.progress.setValue(0)
#             self.output.append(f"\n❌ Error during processing: {str(e)}")

#     def run_header_list_filter(self):
#         if not hasattr(self, 'hl_fasta_path'):
#             self.hl_output.append("❌ Error: No FASTA file selected!")
#             return
#         if not hasattr(self, 'header_list_path'):
#             self.hl_output.append("❌ Error: No header list file selected!")
#             return
            
#         self.hl_output.clear()
#         self.hl_progress.setValue(0)
#         self.hl_output.append("🚀 Starting header list filtering process...")
        
#         try:
#             self.hl_output.append("\n🔍 Parsing header list file...")
#             self.hl_progress.setValue(20)
            
#             target_headers = self.parse_header_list()
#             if not target_headers:
#                 self.hl_output.append("❌ Error: No valid headers found in the list!")
#                 return
                
#             self.hl_output.append(f"  - Found {len(target_headers)} headers in the list")
            
#             case_sensitive = self.case_sensitive.isChecked()
#             partial_match = self.partial_match.isChecked()
            
#             base_name = os.path.splitext(os.path.basename(self.hl_fasta_path))[0]
#             output_path = f"{base_name}_filtered_by_header_list.fasta"
            
#             self.hl_output.append(f"\n✂️ Filtering FASTA file...")
#             self.hl_progress.setValue(40)
            
#             total = 0
#             kept = 0
            
#             with open(output_path, 'w', encoding='utf-8') as out:
#                 for record in SeqIO.parse(self.hl_fasta_path, "fasta"):
#                     total += 1
#                     header_to_check = record.id if case_sensitive else record.id.lower()
                    
#                     match_found = False
#                     if partial_match:
#                         for target in target_headers:
#                             if target in header_to_check:
#                                 match_found = True
#                                 break
#                     else:
#                         match_found = header_to_check in target_headers
                    
#                     if match_found:
#                         SeqIO.write(record, out, "fasta")
#                         kept += 1
                    
#                     if total % 100 == 0:
#                         progress_value = 40 + int(50 * (total/len(target_headers)))
#                         self.hl_progress.setValue(min(progress_value, 90))
#                         self.hl_output.append(f"  - Processed {total} sequences...")
            
#             stats_path = f"{base_name}_header_filter_stats.txt"
#             with open(stats_path, 'w', encoding='utf-8') as f:
#                 f.write("Header List Filtering Report\n")
#                 f.write("="*40 + "\n")
#                 f.write(f"Input FASTA: {os.path.basename(self.hl_fasta_path)}\n")
#                 f.write(f"Header list: {os.path.basename(self.header_list_path)}\n")
#                 f.write(f"\nFilter Parameters:\n")
#                 f.write(f"- Case-sensitive: {'Yes' if case_sensitive else 'No'}\n")
#                 f.write(f"- Partial matches: {'Yes' if partial_match else 'No'}\n")
#                 f.write(f"\nResults:\n")
#                 f.write(f"Total sequences: {total}\n")
#                 f.write(f"Sequences kept: {kept} ({kept/total:.1%})\n")
            
#             self.hl_progress.setValue(100)
#             self.hl_output.append(f"\n✅ Successfully created filtered FASTA file!")
#             self.hl_output.append(f"📄 Output file: {output_path}")
            
#         except Exception as e:
#             self.hl_progress.setValue(0)
#             self.hl_output.append(f"\n❌ Error during processing: {str(e)}")

#     def validate_sequences(self):
#         fasta_text = self.sequence_input.toPlainText().strip()
        
#         if not fasta_text:
#             self.validation_label.setText("Error: No input provided.")
#             return

#         try:
#             sequences = []
#             current_header = ""
#             current_seq = ""
            
#             for line in fasta_text.splitlines():
#                 if line.startswith(">"):
#                     if current_header:
#                         sequences.append((current_header, current_seq))
#                     current_header = line.strip()
#                     current_seq = ""
#                 else:
#                     current_seq += line.strip()
            
#             if current_header:
#                 sequences.append((current_header, current_seq))
            
#             dna_count = 0
#             rna_count = 0
#             protein_count = 0
#             invalid_count = 0
            
#             for header, seq in sequences:
#                 if self.is_dna(seq):
#                     dna_count += 1
#                 elif self.is_rna(seq):
#                     rna_count += 1
#                 elif self.is_protein(seq):
#                     protein_count += 1
#                 else:
#                     invalid_count += 1
            
#             result_text = []
#             if dna_count:
#                 result_text.append(f"DNA sequences: {dna_count}")
#             if rna_count:
#                 result_text.append(f"RNA sequences: {rna_count}")
#             if protein_count:
#                 result_text.append(f"Protein sequences: {protein_count}")
#             if invalid_count:
#                 result_text.append(f"Invalid sequences: {invalid_count}")
            
#             self.validation_label.setText(" | ".join(result_text))
#             self.validator_output.setPlainText("\n".join(result_text))
            
#         except Exception as e:
#             self.validation_label.setText(f"Error: {str(e)}")

#     def is_dna(self, sequence):
#         return bool(re.match("^[ACGTacgt]+$", sequence))

#     def is_rna(self, sequence):
#         return bool(re.match("^[ACGUacgu]+$", sequence))

#     def is_protein(self, sequence):
#         return bool(re.match("^[ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy]+$", sequence))

#     def save_file(self):
#         save_path, _ = QFileDialog.getSaveFileName(
#             self, "Save File", "",
#             f"FASTA Files (*{self.format_dropdown.currentText()})"
#         )
#         if not save_path:
#             return
        
#         with open(save_path, "w") as file:
#             file.write(self.sequence_input.toPlainText())
        
#         QMessageBox.information(self, "Success", "File saved successfully!")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = FastaFilterTool()
#     window.show()
#     sys.exit(app.exec())




import sys
import os
import re
import pandas as pd
from Bio import SeqIO
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QLabel, QComboBox, QFileDialog,
    QMessageBox, QScrollArea, QTabWidget, QRadioButton,
    QButtonGroup, QProgressBar, QCheckBox, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont

class FastaFilterTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genome Wide WorkBench")
        self.setWindowIcon(QIcon('src/image.png'))
        self.setGeometry(100, 100, 1000, 1000)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)

        # Scroll area for main content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        # Scroll area widget contents
        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        # Title label
        self.header_label = QLabel("FASTA Filter Tool")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        self.header_label.setStyleSheet("""QLabel {
            background-color: #2C3E50;
            color: white;
            padding: 20px;
            border-radius: 12px;
        }""")
        self.scroll_layout.addWidget(self.header_label)

        # Create tab widget
        self.tabs = QTabWidget()
        self.scroll_layout.addWidget(self.tabs)

        # Create tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        
        self.tabs.addTab(self.tab1, "BLAST/HMMER Filter")
        self.tabs.addTab(self.tab2, "Header List Filter")
        self.tabs.addTab(self.tab3, "Sequence Validator")

        # Setup all tabs
        self.setup_blast_hmmer_tab()
        self.setup_header_list_tab()
        self.setup_validator_tab()

        # Add spacer at the end to push content upwards
        self.scroll_layout.addStretch()

    def set_button_styles(self, button):
        button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        button.setStyleSheet("""
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

    def setup_blast_hmmer_tab(self):
        """Setup the BLAST/HMMER filtering tab"""
        layout = QVBoxLayout(self.tab1)

        # File selection group
        file_group = QGroupBox("Input Files")
        file_layout = QVBoxLayout()
        
        # FASTA Input
        self.fasta_label = QLabel("No FASTA file selected")
        self.fasta_label.setStyleSheet("color: #666; font-style: italic;")
        btn_fasta = QPushButton("Select Query FASTA (.fasta/.fa)")
        self.set_button_styles(btn_fasta)
        btn_fasta.clicked.connect(self.load_fasta)
        
        # BLAST Input (XLSX)
        self.blast_label = QLabel("No BLAST file selected (.xlsx)")
        self.blast_label.setStyleSheet("color: #666; font-style: italic;")
        btn_blast = QPushButton("Select BLAST Results (.xlsx)")
        self.set_button_styles(btn_blast)
        btn_blast.clicked.connect(self.load_blast)
        
        # HMMER Input (TXT)
        self.hmmer_label = QLabel("No HMMER file selected (.txt)")
        self.hmmer_label.setStyleSheet("color: #666; font-style: italic;")
        btn_hmmer = QPushButton("Select HMMER Results (.txt)")
        self.set_button_styles(btn_hmmer)
        btn_hmmer.clicked.connect(self.load_hmmer)
        
        # Output directory selection
        self.output_dir_label = QLabel("Output directory: Not selected")
        self.output_dir_label.setStyleSheet("color: #666; font-style: italic;")
        btn_output_dir = QPushButton("Select Output Directory")
        self.set_button_styles(btn_output_dir)
        btn_output_dir.clicked.connect(self.select_output_dir)
        
        file_layout.addWidget(btn_fasta)
        file_layout.addWidget(self.fasta_label)
        file_layout.addWidget(btn_blast)
        file_layout.addWidget(self.blast_label)
        file_layout.addWidget(btn_hmmer)
        file_layout.addWidget(self.hmmer_label)
        file_layout.addWidget(btn_output_dir)
        file_layout.addWidget(self.output_dir_label)
        file_group.setLayout(file_layout)
        
        # Filter options group
        filter_group = QGroupBox("Filter Method")
        filter_layout = QVBoxLayout()
        
        self.option_blast = QRadioButton("BLAST hits only")
        self.option_hmmer = QRadioButton("HMMER hits only") 
        self.option_both = QRadioButton("Both BLAST AND HMMER hits")
        self.option_either = QRadioButton("Either BLAST OR HMMER hits")
        
        self.option_group = QButtonGroup()
        self.option_group.addButton(self.option_blast)
        self.option_group.addButton(self.option_hmmer)
        self.option_group.addButton(self.option_both)
        self.option_group.addButton(self.option_either)
        self.option_blast.setChecked(True)
        
        filter_layout.addWidget(self.option_blast)
        filter_layout.addWidget(self.option_hmmer)
        filter_layout.addWidget(self.option_both)
        filter_layout.addWidget(self.option_either)
        filter_group.setLayout(filter_layout)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignCenter)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #2C3E50;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
            }
        """)
        
        # Output console
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        
        # Run button
        btn_run = QPushButton("Generate Filtered FASTA")
        self.set_button_styles(btn_run)
        btn_run.clicked.connect(self.run_blast_hmmer_filter)
        self.btn_run = btn_run
        
        # Add widgets to layout
        layout.addWidget(file_group)
        layout.addWidget(filter_group)
        layout.addWidget(self.progress)
        layout.addWidget(btn_run)
        layout.addWidget(self.output)

    def setup_header_list_tab(self):
        """Setup the header list filtering tab"""
        layout = QVBoxLayout(self.tab2)
        
        # File selection group
        file_group = QGroupBox("Input Files")
        file_layout = QVBoxLayout()
        
        # FASTA Input
        self.hl_fasta_label = QLabel("No FASTA file selected")
        self.hl_fasta_label.setStyleSheet("color: #666; font-style: italic;")
        btn_fasta = QPushButton("Select Query FASTA (.fasta/.fa)")
        self.set_button_styles(btn_fasta)
        btn_fasta.clicked.connect(self.load_hl_fasta)
        
        # Header List Input
        self.header_list_label = QLabel("No header list file selected (.txt)")
        self.header_list_label.setStyleSheet("color: #666; font-style: italic;")
        btn_header = QPushButton("Select Header List (.txt)")
        self.set_button_styles(btn_header)
        btn_header.clicked.connect(self.load_header_list)
        
        # Output directory selection
        self.hl_output_dir_label = QLabel("Output directory: Not selected")
        self.hl_output_dir_label.setStyleSheet("color: #666; font-style: italic;")
        btn_output_dir = QPushButton("Select Output Directory")
        self.set_button_styles(btn_output_dir)
        btn_output_dir.clicked.connect(self.select_hl_output_dir)
        
        file_layout.addWidget(btn_fasta)
        file_layout.addWidget(self.hl_fasta_label)
        file_layout.addWidget(btn_header)
        file_layout.addWidget(self.header_list_label)
        file_layout.addWidget(btn_output_dir)
        file_layout.addWidget(self.hl_output_dir_label)
        file_group.setLayout(file_layout)
        
        # Options group
        options_group = QGroupBox("Filter Options")
        options_layout = QVBoxLayout()
        
        self.case_sensitive = QCheckBox("Case-sensitive matching")
        self.case_sensitive.setChecked(False)
        
        self.partial_match = QCheckBox("Allow partial header matches")
        self.partial_match.setChecked(False)
        
        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(self.partial_match)
        options_group.setLayout(options_layout)
        
        # Progress bar
        self.hl_progress = QProgressBar()
        self.hl_progress.setAlignment(Qt.AlignCenter)
        self.hl_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #2C3E50;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
            }
        """)
        
        # Output console
        self.hl_output = QTextEdit()
        self.hl_output.setReadOnly(True)
        
        # Run button
        btn_run = QPushButton("Generate Filtered FASTA")
        self.set_button_styles(btn_run)
        btn_run.clicked.connect(self.run_header_list_filter)
        self.hl_btn_run = btn_run
        
        # Add widgets to layout
        layout.addWidget(file_group)
        layout.addWidget(options_group)
        layout.addWidget(self.hl_progress)
        layout.addWidget(btn_run)
        layout.addWidget(self.hl_output)

    def setup_validator_tab(self):
        """Setup the sequence validator tab"""
        layout = QVBoxLayout(self.tab3)
        
        # Text area for FASTA input
        self.sequence_input = QTextEdit()
        self.sequence_input.setPlaceholderText("Paste your FASTA sequence here...")
        
        # Validation label
        self.validation_label = QLabel("")
        self.validation_label.setStyleSheet("color: #E74C3C;")
        
        # Format dropdown
        self.format_dropdown = QComboBox()
        self.format_dropdown.addItems([".fasta", ".fa", ".txt", ".fna"])
        
        # Buttons layout
        button_layout = QHBoxLayout()
        self.load_button = QPushButton("Load File")
        self.set_button_styles(self.load_button)
        self.load_button.clicked.connect(self.load_file)
        
        self.validate_button = QPushButton("Validate")
        self.set_button_styles(self.validate_button)
        self.validate_button.clicked.connect(self.validate_sequences)
        
        self.save_button = QPushButton("Save")
        self.set_button_styles(self.save_button)
        self.save_button.clicked.connect(self.save_file)
        
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.validate_button)
        button_layout.addWidget(self.save_button)
        
        # Output console
        self.validator_output = QTextEdit()
        self.validator_output.setReadOnly(True)
        
        # Add widgets to layout
        layout.addWidget(self.sequence_input)
        layout.addWidget(self.validation_label)
        layout.addWidget(self.format_dropdown)
        layout.addLayout(button_layout)
        layout.addWidget(self.validator_output)

    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_dir = dir_path
            self.output_dir_label.setText(f"✓ Output directory: {dir_path}")
            self.output_dir_label.setStyleSheet("color: #27ae60; font-style: normal;")

    def select_hl_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.hl_output_dir = dir_path
            self.hl_output_dir_label.setText(f"✓ Output directory: {dir_path}")
            self.hl_output_dir_label.setStyleSheet("color: #27ae60; font-style: normal;")

    def load_fasta(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select FASTA File", "",
            "FASTA Files (*.fasta *.fa);;All Files (*)"
        )
        if path:
            self.fasta_path = path
            self.fasta_label.setText(f"✓ {os.path.basename(path)}")
            self.fasta_label.setStyleSheet("color: #27ae60; font-style: normal;")
            self.update_ui_state()

    def load_blast(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select BLAST XLSX File", "",
            "Excel Files (*.xlsx);;All Files (*)"
        )
        if path:
            self.blast_path = path
            self.blast_label.setText(f"✓ {os.path.basename(path)}")
            self.blast_label.setStyleSheet("color: #27ae60; font-style: normal;")
            self.update_ui_state()

    def load_hmmer(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select HMMER TXT File", "",
            "Text Files (*.txt);;All Files (*)"
        )
        if path:
            self.hmmer_path = path
            self.hmmer_label.setText(f"✓ {os.path.basename(path)}")
            self.hmmer_label.setStyleSheet("color: #27ae60; font-style: normal;")
            self.update_ui_state()

    def load_hl_fasta(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select FASTA File", "",
            "FASTA Files (*.fasta *.fa);;All Files (*)"
        )
        if path:
            self.hl_fasta_path = path
            self.hl_fasta_label.setText(f"✓ {os.path.basename(path)}")
            self.hl_fasta_label.setStyleSheet("color: #27ae60; font-style: normal;")
            self.update_hl_ui_state()

    def load_header_list(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Header List File", "",
            "Text Files (*.txt);;All Files (*)"
        )
        if path:
            self.header_list_path = path
            self.header_list_label.setText(f"✓ {os.path.basename(path)}")
            self.header_list_label.setStyleSheet("color: #27ae60; font-style: normal;")
            self.update_hl_ui_state()

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open FASTA File", "",
            "FASTA Files (*.fasta *.fa *.txt *.fna)"
        )
        if path:
            with open(path, "r") as file:
                fasta_content = file.read()
            self.sequence_input.setPlainText(fasta_content)

    def update_ui_state(self):
        blast_loaded = hasattr(self, 'blast_path')
        hmmer_loaded = hasattr(self, 'hmmer_path')
        
        self.option_blast.setEnabled(blast_loaded)
        self.option_hmmer.setEnabled(hmmer_loaded)
        self.option_both.setEnabled(blast_loaded and hmmer_loaded)
        self.option_either.setEnabled(blast_loaded and hmmer_loaded)
        
        self.btn_run.setEnabled(hasattr(self, 'fasta_path') and (blast_loaded or hmmer_loaded))

    def update_hl_ui_state(self):
        fasta_loaded = hasattr(self, 'hl_fasta_path')
        header_loaded = hasattr(self, 'header_list_path')
        self.hl_btn_run.setEnabled(fasta_loaded and header_loaded)

    def parse_blast_xlsx(self):
        try:
            df = pd.read_excel(self.blast_path)
            if 'QuerySeq.ID' not in df.columns:
                self.output.append("❌ Error: BLAST file missing 'QuerySeq.ID' column")
                return set()
            return set(df['QuerySeq.ID'].dropna().unique())
        except Exception as e:
            self.output.append(f"❌ BLAST XLSX Error: {str(e)}")
            return set()

    def parse_hmmer_txt(self):
        hmmer_seqs = set()
        try:
            with open(self.hmmer_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split()
                        if parts:
                            hmmer_seqs.add(parts[0])
            return hmmer_seqs
        except Exception as e:
            self.output.append(f"❌ HMMER TXT Error: {str(e)}")
            return set()

    def parse_header_list(self):
        headers = set()
        try:
            with open(self.header_list_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        if not self.case_sensitive.isChecked():
                            line = line.lower()
                        headers.add(line)
            return headers
        except Exception as e:
            self.hl_output.append(f"❌ Header List Error: {str(e)}")
            return set()

    def run_blast_hmmer_filter(self):
        if not hasattr(self, 'fasta_path'):
            self.output.append("❌ Error: No FASTA file selected!")
            return
            
        self.output.clear()
        self.progress.setValue(0)
        self.output.append("🚀 Starting FASTA filtering process...")
        
        try:
            self.output.append("\n🔍 Parsing input files...")
            self.progress.setValue(10)
            
            blast_seqs = set()
            if hasattr(self, 'blast_path'):
                blast_seqs = self.parse_blast_xlsx()
                self.output.append(f"  - Found {len(blast_seqs)} BLAST hits")
            
            hmmer_seqs = set()
            if hasattr(self, 'hmmer_path'):
                hmmer_seqs = self.parse_hmmer_txt()
                self.output.append(f"  - Found {len(hmmer_seqs)} HMMER hits")
            
            self.progress.setValue(30)
            
            if self.option_blast.isChecked():
                selected_seqs = blast_seqs
                method = "blast_only"
                self.output.append("\n🔧 Filter: Keeping sequences with BLAST hits")
            elif self.option_hmmer.isChecked():
                selected_seqs = hmmer_seqs
                method = "hmmer_only"
                self.output.append("\n🔧 Filter: Keeping sequences with HMMER hits")
            elif self.option_both.isChecked():
                selected_seqs = blast_seqs & hmmer_seqs
                method = "both"
                self.output.append("\n🔧 Filter: Keeping sequences with BOTH BLAST AND HMMER hits")
            else:
                selected_seqs = blast_seqs | hmmer_seqs
                method = "either"
                self.output.append("\n🔧 Filter: Keeping sequences with EITHER BLAST OR HMMER hits")
            
            base_name = os.path.splitext(os.path.basename(self.fasta_path))[0]
            
            # Use selected output directory if available, otherwise use current directory
            if hasattr(self, 'output_dir'):
                output_path = os.path.join(self.output_dir, f"{base_name}_filtered_{method}.fasta")
                stats_path = os.path.join(self.output_dir, f"{base_name}_filter_stats.txt")
            else:
                output_path = f"{base_name}_filtered_{method}.fasta"
                stats_path = f"{base_name}_filter_stats.txt"
            
            self.output.append(f"\n✂️ Filtering FASTA file...")
            self.progress.setValue(40)
            
            total = 0
            kept = 0
            
            with open(output_path, 'w', encoding='utf-8') as out:
                for record in SeqIO.parse(self.fasta_path, "fasta"):
                    total += 1
                    if record.id in selected_seqs:
                        SeqIO.write(record, out, "fasta")
                        kept += 1
                    
                    if total % 100 == 0:
                        progress_value = 40 + int(50 * (total/max(1,len(selected_seqs))))
                        self.progress.setValue(min(progress_value, 90))
                        self.output.append(f"  - Processed {total} sequences...")
            
            with open(stats_path, 'w', encoding='utf-8') as f:
                f.write("FASTA Filtering Report\n")
                f.write("="*40 + "\n")
                f.write(f"Input FASTA: {os.path.basename(self.fasta_path)}\n")
                if hasattr(self, 'blast_path'):
                    f.write(f"BLAST file: {os.path.basename(self.blast_path)}\n")
                if hasattr(self, 'hmmer_path'):
                    f.write(f"HMMER file: {os.path.basename(self.hmmer_path)}\n")
                f.write(f"\nFilter Method: {method.replace('_', ' ').title()}\n")
                f.write(f"Total sequences: {total}\n")
                f.write(f"Sequences kept: {kept} ({kept/total:.1%})\n")
            
            self.progress.setValue(100)
            self.output.append(f"\n✅ Successfully created filtered FASTA file!")
            self.output.append(f"📄 Output file: {output_path}")
            
        except Exception as e:
            self.progress.setValue(0)
            self.output.append(f"\n❌ Error during processing: {str(e)}")

    def run_header_list_filter(self):
        if not hasattr(self, 'hl_fasta_path'):
            self.hl_output.append("❌ Error: No FASTA file selected!")
            return
        if not hasattr(self, 'header_list_path'):
            self.hl_output.append("❌ Error: No header list file selected!")
            return
            
        self.hl_output.clear()
        self.hl_progress.setValue(0)
        self.hl_output.append("🚀 Starting header list filtering process...")
        
        try:
            self.hl_output.append("\n🔍 Parsing header list file...")
            self.hl_progress.setValue(20)
            
            target_headers = self.parse_header_list()
            if not target_headers:
                self.hl_output.append("❌ Error: No valid headers found in the list!")
                return
                
            self.hl_output.append(f"  - Found {len(target_headers)} headers in the list")
            
            case_sensitive = self.case_sensitive.isChecked()
            partial_match = self.partial_match.isChecked()
            
            base_name = os.path.splitext(os.path.basename(self.hl_fasta_path))[0]
            
            # Use selected output directory if available, otherwise use current directory
            if hasattr(self, 'hl_output_dir'):
                output_path = os.path.join(self.hl_output_dir, f"{base_name}_filtered_by_header_list.fasta")
                stats_path = os.path.join(self.hl_output_dir, f"{base_name}_header_filter_stats.txt")
            else:
                output_path = f"{base_name}_filtered_by_header_list.fasta"
                stats_path = f"{base_name}_header_filter_stats.txt"
            
            self.hl_output.append(f"\n✂️ Filtering FASTA file...")
            self.hl_progress.setValue(40)
            
            total = 0
            kept = 0
            
            with open(output_path, 'w', encoding='utf-8') as out:
                for record in SeqIO.parse(self.hl_fasta_path, "fasta"):
                    total += 1
                    header_to_check = record.id if case_sensitive else record.id.lower()
                    
                    match_found = False
                    if partial_match:
                        for target in target_headers:
                            if target in header_to_check:
                                match_found = True
                                break
                    else:
                        match_found = header_to_check in target_headers
                    
                    if match_found:
                        SeqIO.write(record, out, "fasta")
                        kept += 1
                    
                    if total % 100 == 0:
                        progress_value = 40 + int(50 * (total/len(target_headers)))
                        self.hl_progress.setValue(min(progress_value, 90))
                        self.hl_output.append(f"  - Processed {total} sequences...")
            
            with open(stats_path, 'w', encoding='utf-8') as f:
                f.write("Header List Filtering Report\n")
                f.write("="*40 + "\n")
                f.write(f"Input FASTA: {os.path.basename(self.hl_fasta_path)}\n")
                f.write(f"Header list: {os.path.basename(self.header_list_path)}\n")
                f.write(f"\nFilter Parameters:\n")
                f.write(f"- Case-sensitive: {'Yes' if case_sensitive else 'No'}\n")
                f.write(f"- Partial matches: {'Yes' if partial_match else 'No'}\n")
                f.write(f"\nResults:\n")
                f.write(f"Total sequences: {total}\n")
                f.write(f"Sequences kept: {kept} ({kept/total:.1%})\n")
            
            self.hl_progress.setValue(100)
            self.hl_output.append(f"\n✅ Successfully created filtered FASTA file!")
            self.hl_output.append(f"📄 Output file: {output_path}")
            
        except Exception as e:
            self.hl_progress.setValue(0)
            self.hl_output.append(f"\n❌ Error during processing: {str(e)}")

    def validate_sequences(self):
        fasta_text = self.sequence_input.toPlainText().strip()
        
        if not fasta_text:
            self.validation_label.setText("Error: No input provided.")
            return

        try:
            sequences = []
            current_header = ""
            current_seq = ""
            
            for line in fasta_text.splitlines():
                if line.startswith(">"):
                    if current_header:
                        sequences.append((current_header, current_seq))
                    current_header = line.strip()
                    current_seq = ""
                else:
                    current_seq += line.strip()
            
            if current_header:
                sequences.append((current_header, current_seq))
            
            dna_count = 0
            rna_count = 0
            protein_count = 0
            invalid_count = 0
            
            for header, seq in sequences:
                if self.is_dna(seq):
                    dna_count += 1
                elif self.is_rna(seq):
                    rna_count += 1
                elif self.is_protein(seq):
                    protein_count += 1
                else:
                    invalid_count += 1
            
            result_text = []
            if dna_count:
                result_text.append(f"DNA sequences: {dna_count}")
            if rna_count:
                result_text.append(f"RNA sequences: {rna_count}")
            if protein_count:
                result_text.append(f"Protein sequences: {protein_count}")
            if invalid_count:
                result_text.append(f"Invalid sequences: {invalid_count}")
            
            self.validation_label.setText(" | ".join(result_text))
            self.validator_output.setPlainText("\n".join(result_text))
            
        except Exception as e:
            self.validation_label.setText(f"Error: {str(e)}")

    def is_dna(self, sequence):
        return bool(re.match("^[ACGTacgt]+$", sequence))

    def is_rna(self, sequence):
        return bool(re.match("^[ACGUacgu]+$", sequence))

    def is_protein(self, sequence):
        return bool(re.match("^[ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy]+$", sequence))

    def save_file(self):
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", "",
            f"FASTA Files (*{self.format_dropdown.currentText()})"
        )
        if not save_path:
            return
        
        with open(save_path, "w") as file:
            file.write(self.sequence_input.toPlainText())
        
        QMessageBox.information(self, "Success", "File saved successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FastaFilterTool()
    window.show()
    sys.exit(app.exec())
