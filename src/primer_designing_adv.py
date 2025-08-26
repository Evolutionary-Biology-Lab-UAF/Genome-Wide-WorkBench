import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QScrollArea, QCheckBox, QMessageBox
,QComboBox,QTextEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
import primer3

class Primer3App_adv(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genome Wide WorkBench")
        self.setWindowIcon(QIcon('src/image.png'))

        # self.setGeometry(100, 100, 500, 500)
        self.setGeometry(100, 100, 1000, 1000)


        # Color constants
        self.default_text_color = "#000000"  # Default text color (black for light mode)
        self.highlight_color = "#FFEB99"      # Highlight color for matching search

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
        self.header_label = QLabel("GenePrimer X")
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
        self.scroll_layout.addWidget(self.header_label)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search primer parameters...")
        self.search_bar.setFixedWidth(350)
        self.search_bar.setStyleSheet("""
        QLineEdit {
        border: 1px solid #2C3E50;
        padding: 6px;
        font-size: 14px;
        border-radius: 5px;
    }
        """)
        self.search_bar.textChanged.connect(self.search_parameters)
        self.scroll_layout.addWidget(self.search_bar)

        # Horizontal layout for file upload
        self.file_upload_layout = QHBoxLayout()
        self.file_upload_layout.setSpacing(10)

        # Instruction label
        self.instruction_label = QLabel("Upload a FASTA file:")
        self.instruction_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.file_upload_layout.addWidget(self.instruction_label)

        # File name display
        self.file_name_display = QLineEdit()
        self.file_name_display.setPlaceholderText("No file selected")
        self.file_name_display.setReadOnly(True)
        self.file_name_display.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2C3E50;
                padding: 5px;
                font-size: 12px;
                border-radius: 5px;
            }
        """)
        self.file_upload_layout.addWidget(self.file_name_display)

        # Load file button
        self.load_button = QPushButton("Load FASTA File")
        self.load_button.setIcon(QIcon("upload_icon.png"))  # Use an icon file for upload, if available
        self.load_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.load_button.setStyleSheet("""
 QPushButton {
        font-size: 16px;
        color: white;
        background-color: #2C3E50;
        border: none;
        text-align: left;
        padding: 10px 20px;
    }
    QPushButton:hover {
        background-color: #34495E;  /* Darker blue-gray on hover */
    }
        QPushButton:pressed {
            background-color: #34495E;
        }
""")
        self.load_button.clicked.connect(self.load_file)
        self.file_upload_layout.addWidget(self.load_button)

        # Add file upload layout to main layout
        self.scroll_layout.addLayout(self.file_upload_layout)

        # Primer3 settings form
        self.settings_form = QVBoxLayout()
        self.settings_form.setSpacing(10)

        self.settings_widgets = {}
        self.default_params = self.get_primer3_settings()
        # Calculate the maximum width needed for the labels
        max_label_width = max(len(param) for param in self.default_params.keys()) * 8

        # Create parameter fields
        for param, value in self.default_params.items():
            param_layout = QHBoxLayout()
            param_label = QLabel(param)
            param_label.setFont(QFont('Arial', 10))
            param_label.setFixedWidth(max_label_width)  # Set fixed width based on calculated max width
            param_label.setObjectName(param)
            param_layout.addWidget(param_label)

            if param.startswith("PRIMER_PICK"):
                checkbox = QCheckBox()
                checkbox.setChecked(bool(value))
                checkbox.setFixedWidth(150)
                param_layout.addWidget(checkbox)
                self.settings_widgets[param] = checkbox
            elif param == "PRIMER_EXPLAIN_FLAG":
                
                checkbox = QCheckBox()
                checkbox.setChecked(bool(value))
                checkbox.setFixedWidth(150)
                param_layout.addWidget(checkbox)
                self.settings_widgets[param] = checkbox
            elif param == "PRIMER_LIB_AMBIGUITY_CODES_CONSENSUS":
                
                checkbox = QCheckBox()
                checkbox.setChecked(bool(value))
                checkbox.setFixedWidth(150)
                param_layout.addWidget(checkbox)
                self.settings_widgets[param] = checkbox
            elif param == "PRIMER_LIBERAL_BASE":
                
                checkbox = QCheckBox()
                checkbox.setChecked(bool(value))
                checkbox.setFixedWidth(150)
                param_layout.addWidget(checkbox)
                self.settings_widgets[param] = checkbox
            elif param == "PRIMER_TM_FORMULA":
                
                checkbox = QCheckBox()
                checkbox.setChecked(bool(value))
                checkbox.setFixedWidth(150)
                param_layout.addWidget(checkbox)
                self.settings_widgets[param] = checkbox

            else:
                line_edit = QLineEdit(str(value))
                line_edit.setFixedWidth(150)
                line_edit.setStyleSheet("border: 1px solid #007BFF; border-radius: 5px;")
                self.settings_widgets[param] = line_edit
                param_layout.addWidget(line_edit)

            self.settings_form.addLayout(param_layout)

        self.scroll_layout.addLayout(self.settings_form)

        # Run Primer3 button
        self.run_primer_button = QPushButton("Run Primer Design")
        self.run_primer_button.setFixedSize(200, 50)
        self.run_primer_button.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        self.run_primer_button.setStyleSheet("""
 QPushButton {
        font-size: 16px;
        color: white;
        background-color: #2C3E50;
        border: none;
        text-align: left;
        padding: 10px 20px;
    }
    QPushButton:hover {
        background-color: #34495E;  /* Darker blue-gray on hover */
    }
        QPushButton:pressed {
            background-color: #34495E;
        }        """)
        self.run_primer_button.clicked.connect(self.run_primer3)
        self.scroll_layout.addWidget(self.run_primer_button)

        # Add spacer at the end to push content upwards
        self.scroll_layout.addStretch()

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open FASTA File", "", "FASTA Files (*.fasta *.fa *.fna *.ffn *.faa *.frn)")
        if file_name:
            self.file_name_display.setText(file_name)
            self.file_path = file_name  # Store the file path

    
    def get_user_params(self):
        user_params = {}
        for param, widget in self.settings_widgets.items():
            if isinstance(widget, QLineEdit):
                user_params[param] = widget.text()
            elif isinstance(widget, QComboBox):
                user_params[param] = widget.currentText()
            elif isinstance(widget, QCheckBox):
                user_params[param] = int(widget.isChecked())
        return user_params

    def search_parameters(self):
        search_text = self.search_bar.text().lower()
        for param, widget in self.settings_widgets.items():
            label = self.findChild(QLabel, param)
            if search_text and search_text in param.lower():
                label.setStyleSheet(f"""
                    background-color: {self.highlight_color};
                    color: #000000;
                    font-weight: bold;
                """)
            else:
                # Reset to default text color and style
                label.setStyleSheet(f"""
                    color: {self.default_text_color};
                    background-color: transparent;
                    font-weight: normal;
                """)

    def run_primer3(self):
        # QMessageBox.information(self, "Run Primer Design", "Primer design parameters are saved and ready to run.")
        primer_results = None  # Initialize the variable
        if not self.file_path:
            self.show_error_dialog("No File Selected", "Please load a FASTA file before running Primer Designing.")
            return

        try:
            # Read the FASTA file
            with open(self.file_path, 'r') as file:
                sequence_lines = file.read().splitlines()

            if len(sequence_lines) < 2 or not sequence_lines[0].startswith('>'):
                self.show_error_dialog("Invalid Sequence File", "The FASTA file must contain a header line starting with '>' followed by the sequence.")
                return  # Exit the method if the input is invalid

            sequence_id = sequence_lines[0].lstrip('>')
            sequence = ''.join(sequence_lines[1:])

            user_params = self.get_user_params()
            params = self.get_primer3_settings()
            params.update(user_params)

            primer_results = primer3.bindings.design_primers({
                'SEQUENCE_ID': sequence_id,
                'SEQUENCE_TEMPLATE': sequence,
            }, params)

            # Open the results window only if primer_results is successfully obtained
            if primer_results:
                self.results_window = ResultWindow(sequence_id, sequence, primer_results)
                self.results_window.show()

        except Exception as e:
            # Show the full traceback in a message box
            error_message = f"An error occurred:\n{str(e)}"
            QMessageBox.critical(self, "Error", error_message)

    def show_error_dialog(self, title, message):
        QMessageBox.critical(self, title, message)

    
    def get_primer3_settings(self):
        default_params = {
        "PRIMER_PICK_LEFT_PRIMER": 1,
        "PRIMER_PICK_INTERNAL_OLIGO": 0,  # Enable internal oligo picking  # default is 0
        "PRIMER_PICK_RIGHT_PRIMER": 1,
        "PRIMER_FIRST_BASE_INDEX": 1,
        "PRIMER_MIN_SIZE": 18, 
        "PRIMER_OPT_SIZE": 20,
        "PRIMER_MAX_SIZE": 23,
        "PRIMER_MIN_TM": 57.0,   
        "PRIMER_OPT_TM": 59.0,   
        "PRIMER_MAX_TM": 62.0,  
        "PRIMER_PAIR_MAX_DIFF_TM": 5.0,
        "PRIMER_MIN_GC": 30.0,
        "PRIMER_OPT_GC_PERCENT": 50.0,
        "PRIMER_MAX_GC": 70.0,
        "PRIMER_PRODUCT_SIZE_RANGE": "150-250 100-300 301-400 401-500 501-600 601-700 701-850 851-1000",  
        "PRIMER_NUM_RETURN": 5, 
        "PRIMER_MAX_END_STABILITY": 9.0,  
        "PRIMER_THERMODYNAMIC_OLIGO_ALIGNMENT": 1,
        "PRIMER_THERMODYNAMIC_TEMPLATE_ALIGNMENT": 0,
        "PRIMER_LIBERAL_BASE": 1,
        "PRIMER_LIB_AMBIGUITY_CODES_CONSENSUS": 0,
        "PRIMER_LOWERCASE_MASKING": 0,
        "PRIMER_PICK_ANYWAY": 0,
        "PRIMER_EXPLAIN_FLAG": 1,
        "PRIMER_MASK_TEMPLATE": 0,
        "PRIMER_TASK": "generic",
        "PRIMER_MASK_FAILURE_RATE": 0.1,
        "PRIMER_MASK_5P_DIRECTION": 1,
        "PRIMER_MASK_3P_DIRECTION": 0,
        "PRIMER_MIN_QUALITY": 0,
        "PRIMER_MIN_END_QUALITY": 0,
        "PRIMER_QUALITY_RANGE_MIN": 0,
        "PRIMER_QUALITY_RANGE_MAX": 100,
        "PRIMER_TM_FORMULA": 1,   # default value 1  
        "PRIMER_PRODUCT_MIN_TM": -1000000.0,
        "PRIMER_PRODUCT_OPT_TM": 0.0,
        "PRIMER_PRODUCT_MAX_TM": 1000000.0,
        "PRIMER_MAX_LIBRARY_MISPRIMING": 12.00,
        "PRIMER_PAIR_MAX_LIBRARY_MISPRIMING": 20.00,
        "PRIMER_MAX_SELF_ANY_TH": 45.0,
        "PRIMER_MAX_SELF_END_TH": 35.0,
        "PRIMER_PAIR_MAX_COMPL_ANY_TH": 45.0,
        "PRIMER_PAIR_MAX_COMPL_END_TH": 35.0,
        "PRIMER_MAX_HAIRPIN_TH": 24.0,
        "PRIMER_MAX_SELF_ANY": 8.00,
        "PRIMER_MAX_SELF_END": 3.00,
        "PRIMER_PAIR_MAX_COMPL_ANY": 8.00,
        "PRIMER_PAIR_MAX_COMPL_END": 3.00,
        "PRIMER_MAX_TEMPLATE_MISPRIMING_TH": 40.00,
        "PRIMER_PAIR_MAX_TEMPLATE_MISPRIMING_TH": 70.00,
        "PRIMER_MAX_TEMPLATE_MISPRIMING": 12.00,
        "PRIMER_PAIR_MAX_TEMPLATE_MISPRIMING": 24.00,
        "PRIMER_MAX_NS_ACCEPTED": 0,
        "PRIMER_MAX_POLY_X": 4,   
        "PRIMER_INSIDE_PENALTY": -1.0,
        "PRIMER_OUTSIDE_PENALTY": 0,
        "PRIMER_GC_CLAMP": 0,
        "PRIMER_MAX_END_GC": 5,
        "PRIMER_MIN_LEFT_THREE_PRIME_DISTANCE": 3,
        "PRIMER_MIN_RIGHT_THREE_PRIME_DISTANCE": 3,
        "PRIMER_MIN_5_PRIME_OVERLAP_OF_JUNCTION": 7,
        "PRIMER_MIN_3_PRIME_OVERLAP_OF_JUNCTION": 4,
        "PRIMER_SALT_MONOVALENT": 50.0,
        "PRIMER_SALT_CORRECTIONS": 1,
        "PRIMER_SALT_DIVALENT": 1.5,
        "PRIMER_DNTP_CONC": 0.6,
        "PRIMER_DNA_CONC": 50.0,
        "PRIMER_SEQUENCING_SPACING": 500,
        "PRIMER_SEQUENCING_INTERVAL": 250,
        "PRIMER_SEQUENCING_LEAD": 50,
        "PRIMER_SEQUENCING_ACCURACY": 20,
        "PRIMER_WT_SIZE_LT": 1.0,
        "PRIMER_WT_SIZE_GT": 1.0,
        "PRIMER_WT_TM_LT": 1.0,
        "PRIMER_WT_TM_GT": 1.0,
        "PRIMER_WT_GC_PERCENT_LT": 0.0,
        "PRIMER_WT_GC_PERCENT_GT": 0.0,
        "PRIMER_WT_SELF_ANY_TH": 0.0,
        "PRIMER_WT_SELF_END_TH": 0.0,
        "PRIMER_WT_HAIRPIN_TH": 0.0,  #0
        "PRIMER_WT_TEMPLATE_MISPRIMING_TH": 0.0,
        "PRIMER_WT_SELF_ANY": 0.0,
        "PRIMER_WT_SELF_END": 0.0,
        "PRIMER_WT_TEMPLATE_MISPRIMING": 0.0,
        "PRIMER_WT_NUM_NS": 0.0,
        # "PRIMER_WT_LIBRARY_MISPRIMING": 0.0,
        # "PRIMER_WT_SEQ_QUAL": 0.0,
        "PRIMER_WT_END_QUAL": 0.0,
        "PRIMER_WT_POS_PENALTY": 0.0,
        "PRIMER_WT_END_STABILITY": 0.0,
        "PRIMER_WT_MASK_FAILURE_RATE": 0.0,
        # "PRIMER_PAIR_WT_PRODUCT_SIZE_LT": 0.0,
        # "PRIMER_PAIR_WT_PRODUCT_SIZE_GT": 0.0,
        "PRIMER_PAIR_WT_PRODUCT_TM_LT": 0.0,
        "PRIMER_PAIR_WT_PRODUCT_TM_GT": 0.0,
        "PRIMER_PAIR_WT_COMPL_ANY_TH": 0.0,
        "PRIMER_PAIR_WT_COMPL_END_TH": 0.0,
        "PRIMER_PAIR_WT_TEMPLATE_MISPRIMING_TH": 0.0,
        "PRIMER_PAIR_WT_COMPL_ANY": 0.0,
        "PRIMER_PAIR_WT_COMPL_END": 0.0,
        "PRIMER_PAIR_WT_TEMPLATE_MISPRIMING": 0.0,
        "PRIMER_PAIR_WT_DIFF_TM": 0.0,
        "PRIMER_PAIR_WT_LIBRARY_MISPRIMING": 0.0,
        "PRIMER_PAIR_WT_PR_PENALTY": 1.0,
        "PRIMER_PAIR_WT_IO_PENALTY": 0.0,
        "PRIMER_INTERNAL_MIN_SIZE": 18,
        "PRIMER_INTERNAL_OPT_SIZE": 20,
        "PRIMER_INTERNAL_MAX_SIZE": 27,
        "PRIMER_INTERNAL_MIN_TM": 57.0,
        "PRIMER_INTERNAL_OPT_TM": 60.0,
        "PRIMER_INTERNAL_MAX_TM": 63.0,
        "PRIMER_INTERNAL_MIN_GC": 20.0,
        "PRIMER_INTERNAL_OPT_GC_PERCENT": 50.0,
        "PRIMER_INTERNAL_MAX_GC": 80.0,
        "PRIMER_INTERNAL_MAX_SELF_ANY_TH": 47.00,
        "PRIMER_INTERNAL_MAX_SELF_END_TH": 47.00,
        "PRIMER_INTERNAL_MAX_HAIRPIN_TH": 47.00,
        "PRIMER_INTERNAL_MAX_SELF_ANY": 12.00,
        "PRIMER_INTERNAL_MAX_SELF_END": 12.00,
        # "PRIMER_INTERNAL_MIN_QUALITY": 0,
        "PRIMER_INTERNAL_MAX_NS_ACCEPTED": 0,
        "PRIMER_INTERNAL_MAX_POLY_X": 5,
        "PRIMER_INTERNAL_MAX_LIBRARY_MISHYB": 12.00,
        "PRIMER_INTERNAL_SALT_MONOVALENT": 50.0,
        "PRIMER_INTERNAL_DNA_CONC": 50.0,
        "PRIMER_INTERNAL_SALT_DIVALENT": 1.5,
        "PRIMER_INTERNAL_DNTP_CONC": 0.0,
        "PRIMER_INTERNAL_WT_SIZE_LT": 1.0,
        "PRIMER_INTERNAL_WT_SIZE_GT": 1.0,
        "PRIMER_INTERNAL_WT_TM_LT": 1.0,
        "PRIMER_INTERNAL_WT_TM_GT": 1.0,
        "PRIMER_INTERNAL_WT_GC_PERCENT_LT": 0.0,
        "PRIMER_INTERNAL_WT_GC_PERCENT_GT": 0.0,
        "PRIMER_INTERNAL_WT_SELF_ANY_TH": 0.0,
        "PRIMER_INTERNAL_WT_SELF_END_TH": 0.0,
        "PRIMER_INTERNAL_WT_HAIRPIN_TH": 0.0,
        "PRIMER_INTERNAL_WT_NUM_NS": 0.0,
        "PRIMER_INTERNAL_WT_LIBRARY_MISHYB": 0.0,
        "PRIMER_INTERNAL_WT_SEQ_QUAL": 0.0,
        "PRIMER_INTERNAL_WT_END_QUAL": 0.0,
        "PRIMER_INTERNAL_WT_TEMPLATE_MISHYB": 0.0,
        "PRIMER_INTERNAL_WT_POS_PENALTY": 0.0,
        "PRIMER_INTERNAL_MAX_TEMPLATE_MISHYB_TH": 0.00,
        "PRIMER_INTERNAL_WT_TEMPLATE_MISHYB_TH": 0.00
    }


        return default_params


    def get_user_params(self):
        user_params = {}
        for param, widget in self.settings_widgets.items():
            if isinstance(widget, QLineEdit):
                user_params[param] = widget.text()
            elif isinstance(widget, QComboBox):
                user_params[param] = widget.currentText()
            elif isinstance(widget, QCheckBox):
                user_params[param] = int(widget.isChecked())
        return user_params
        

class ResultWindow(QMainWindow):
    def __init__(self, sequence_id=None, sequence=None, primer_results=None):
        super().__init__()
        self.setWindowTitle("Primer Design Results")
        self.setWindowIcon(QIcon('src/image.png'))

        self.setGeometry(100, 100, 500, 500)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)

        # Title label
        self.header_label = QLabel("Primer Design Results")
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
        self.main_layout.addWidget(self.header_label)

        # Scroll area for results
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        # Scroll area widget contents
        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        # Display primer details
        if sequence_id and sequence and primer_results:
            self.display_primer_details(sequence_id, sequence, primer_results)

#         # Download button
        self.download_button = QPushButton("Download Results")
        self.download_button.setFixedSize(200, 50)
        self.download_button.setStyleSheet("""
 QPushButton {
        font-size: 16px;
        color: white;
        background-color: #2C3E50;
        border: none;
        text-align: left;
        padding: 10px 20px;
    }
    QPushButton:hover {
        background-color: #34495E;  /* Darker blue-gray on hover */
    }
        QPushButton:pressed {
            background-color: #34495E;
        }
                                                   """)
        self.download_button.clicked.connect(self.download_results)
        self.main_layout.addWidget(self.download_button)

    def display_primer_details(self, sequence_id, sequence, primer_results):
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)

        result_text = f"SEQUENCE_ID: {sequence_id}\n"
        result_text += f"Sequence:\n{self.format_sequence(sequence)}\n\n"

        num_primers = primer_results.get('PRIMER_PAIR_NUM_RETURNED', 0)
        for i in range(num_primers):
            result_text += f"Primer pair {i + 1}:\n"
            result_text += f"{self.format_primer_details(primer_results, i)}\n\n"

        explanations = ['PRIMER_INTERNAL_EXPLAIN', 'PRIMER_LEFT_EXPLAIN', 'PRIMER_RIGHT_EXPLAIN', 'PRIMER_PAIR_EXPLAIN']
        for explanation in explanations:
            result_text += f"{explanation}: {primer_results.get(explanation, 'N/A')}\n"

        self.result_text = result_text
        text_edit.setPlainText(result_text)
        self.scroll_layout.addWidget(text_edit)
    def format_sequence(self, sequence, line_length=60):
        formatted_sequence = ""
        for i in range(0, len(sequence), line_length):
            line_number = i + 1
            line_sequence = sequence[i:i+line_length]
            formatted_sequence += f"{line_number:5} {line_sequence}\n"
        return formatted_sequence



    def format_primer_details(self, primer_results, i):
      # Table headers for readability
      headers = (
        f"{'Parameter':<20} {'Left Primer':<20} {'Right Primer':<20} {'Internal Oligo':<20}\n"
        + "-" * 80 + "\n"
    )

    # Table rows with formatted data
      rows = [
        ("Start", primer_results.get(f'PRIMER_LEFT_{i}', [None, None])[0],
         primer_results.get(f'PRIMER_RIGHT_{i}', [None, None])[0],
         primer_results.get(f'PRIMER_INTERNAL_{i}', [None, None])[0]),

        ("Length", primer_results.get(f'PRIMER_LEFT_{i}', [None, None])[1],
         primer_results.get(f'PRIMER_RIGHT_{i}', [None, None])[1],
         primer_results.get(f'PRIMER_INTERNAL_{i}', [None, None])[1]),

        ("Tm (°C)", primer_results.get(f'PRIMER_LEFT_{i}_TM', 'N/A'),
         primer_results.get(f'PRIMER_RIGHT_{i}_TM', 'N/A'),
         primer_results.get(f'PRIMER_INTERNAL_{i}_TM', 'N/A')),

        ("GC%", primer_results.get(f'PRIMER_LEFT_{i}_GC_PERCENT', 'N/A'),
         primer_results.get(f'PRIMER_RIGHT_{i}_GC_PERCENT', 'N/A'),
         primer_results.get(f'PRIMER_INTERNAL_{i}_GC_PERCENT', 'N/A')),

        ("Self Comp (any)", primer_results.get(f'PRIMER_LEFT_{i}_SELF_ANY_TH', 'N/A'),
         primer_results.get(f'PRIMER_RIGHT_{i}_SELF_ANY_TH', 'N/A'),
         primer_results.get(f'PRIMER_INTERNAL_{i}_SELF_ANY_TH', 'N/A')),

        ("Self Comp (3' end)", primer_results.get(f'PRIMER_LEFT_{i}_SELF_END_TH', 'N/A'),
         primer_results.get(f'PRIMER_RIGHT_{i}_SELF_END_TH', 'N/A'),
         primer_results.get(f'PRIMER_INTERNAL_{i}_SELF_END_TH', 'N/A')),

        ("Hairpin Stability", primer_results.get(f'PRIMER_LEFT_{i}_HAIRPIN_TH', 'N/A'),
         primer_results.get(f'PRIMER_RIGHT_{i}_HAIRPIN_TH', 'N/A'),
         primer_results.get(f'PRIMER_INTERNAL_{i}_HAIRPIN_TH', 'N/A')),

        ("Sequence", primer_results.get(f'PRIMER_LEFT_{i}_SEQUENCE', 'N/A'),
         primer_results.get(f'PRIMER_RIGHT_{i}_SEQUENCE', 'N/A'),
         primer_results.get(f'PRIMER_INTERNAL_{i}_SEQUENCE', 'N/A')),
    ]

    # Product details
      pair_details = (
        f"\n{'Pair Details':<20} {'Value':<20}\n"
        + "-" * 40 + "\n"
        + f"{'Product Size':<20} {primer_results.get(f'PRIMER_PAIR_{i}_PRODUCT_SIZE', 'N/A')}\n"
        + f"{'Pair Any Th Compl':<20} {primer_results.get(f'PRIMER_PAIR_{i}_COMPL_ANY_TH', 'N/A')}\n"
        + f"{'Pair 3\' Th Compl':<20} {primer_results.get(f'PRIMER_PAIR_{i}_COMPL_END_TH', 'N/A')}\n"
    )

    # Build table by formatting each row
      table = headers
      for label, left, right, internal in rows:
          table += f"{label:<20} {str(left):<20} {str(right):<20} {str(internal):<20}\n"

      return table + pair_details



    def download_results(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.result_text)
    def closeEvent(self, event):
    # Create the message box
      msg_box = QMessageBox(self)
      msg_box.setWindowTitle("Close Window")
      msg_box.setText("Do you want to close, minimize, or cancel?")
    
    # Add standard buttons
      close_button = msg_box.addButton(QMessageBox.Close)
      cancel_button = msg_box.addButton(QMessageBox.Cancel)
    
    # Add a custom "Minimize" button
      minimize_button = QPushButton("Minimize")
      msg_box.addButton(minimize_button, QMessageBox.ActionRole)
    
    # Execute the message box and get the user's response
      msg_box.exec()
    
    # Handle the user's choice
      if msg_box.clickedButton() == close_button:
        event.accept()  # Close the window
      elif msg_box.clickedButton() == minimize_button:
        self.showMinimized()  # Minimize the window
        event.ignore()  # Ignore the close event
      else:
        event.ignore()  # Cancel the close event

def main():
    app = QApplication(sys.argv)
    window = Primer3App_adv()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
