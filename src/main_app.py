import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QStackedWidget, QFrame, QMenuBar, QMenu, QMessageBox, QComboBox,
    QSizePolicy, QSpacerItem, QScrollArea, QGroupBox
)
from PySide6.QtGui import QIcon, QPalette, QAction
from PySide6.QtCore import Qt
from pathlib import Path
import shutil
import os

def get_resource_path(relative_path):
    """Get the absolute path to a resource, handling both development and PyInstaller environments."""
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.parent
    return str(base_path / relative_path)

class ToolWindow(QMainWindow):
    """Main window for individual tools."""
    def __init__(self, tool_name):
        super().__init__()
        self.setWindowTitle(tool_name)
        self.setWindowIcon(QIcon(get_resource_path('src/image.png')))
        
        # Dynamically adjust size based on the screen size
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        window_width = int(screen_geometry.width() * 0.8)
        window_height = int(screen_geometry.height() * 0.8)
        self.setMinimumSize(800, 600)
        self.resize(window_width, window_height)
        
        # Center the window
        self.center_window()

        # Set central widget
        label = QLabel(f"{tool_name} Tool", self)
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

    def center_window(self):
        """Centers the window dynamically."""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

class WelcomeScreen(QWidget):
    """Welcome screen displayed on app launch."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Get the current system palette to detect light/dark mode
        palette = self.palette()
        is_dark_mode = palette.color(QPalette.WindowText).lightness() < 128

        # Title label
        title = QLabel("Welcome to the Genome Wide Workbench")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 30px; font-weight: bold; color: {'#000000' if is_dark_mode else '#FFFFFF'}; margin-bottom: 0px;")
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(title)

        # Info label
        info = QLabel(
            "This application provides a suite of bioinformatics tools for genomic data analysis.\n\n"
            "To get started:\n"
            "1. Select a tool from the sidebar on the left.\n"
            "2. Use the Data tab in the top menu to explore example data files.\n"
            "3. Refer to the About menu in the top menu for documentation, help, and contact details."
        )
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet(f"font-size: 14px; font-weight: normal; color: {'#000000' if is_dark_mode else '#FFFFFF'};")
        info.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(info)

class DataInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Get the current system palette to detect light/dark mode
        palette = self.palette()
        is_dark_mode = palette.color(QPalette.WindowText).lightness() < 128

        # Title Label
        title_label = QLabel("About Data Tab")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {'#000000' if is_dark_mode else '#FFFFFF'};")
        layout.addWidget(title_label)

        # Info Label
        info_label = QLabel(
            "This application allows you to analyze genomic data using various bioinformatics tools.\n\n"
            "Example Data:\n"
            "1. Open the file and paste the sequence present in the FASTA Formatter app.\n"
            "2. For Primer Designing, the example file use this seq_primer.fasta.\n"
            "3. For Alignment and Alignment & Trimming, use a FASTA format file either use cds.fa ,pep.fa\n"
            "4. Phylogenetic analysis: use align_test.fasta and probe.fasta.\n"
            "5. For Ka/Ks analysis, the required files are:\n"
            "   - Paralog file in .txt format (tab-separated).\n"
            "   - Coding sequence in FASTA format.\n"
            "   - Protein file in FASTA format.\n"
            "6. Phylogenetic Tree: use align.fasta file.\n"
            "7. Tree: use align.fasta file.\n"
            "8. Homologous Pair Finder: Choose the diamond.exe file and select the input file to create the database. \n"
            "After the database is created, go to the BLASTP section of the Homologous Pair Finder, choose the diamond.exe, the database, and the query file.\n"
            "9. HmmerBuild: Choose the Aligment Protein file. \n"
            "10. Hmmersearch Choose the HMM profile and choose the protein Sequence file"
            "11. Gene Density Map Choose the GFF/GFF3 , protein file and index file"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet(f"font-size: 14px; font-weight: normal; color: {'#000000' if is_dark_mode else '#FFFFFF'};")
        layout.addWidget(info_label)

        # Example data files section
        example_data_label = QLabel("Example Data Files:")
        example_data_label.setAlignment(Qt.AlignLeft)
        example_data_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {'#000000' if is_dark_mode else '#FFFFFF'};")
        layout.addWidget(example_data_label)

        # Scrollable area for buttons
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Main widget to hold all the buttons
        button_widget = QWidget()
        button_layout = QVBoxLayout()

        # Grouping files into categories
        file_groups = {
            "KA/KS Analysis": [
                ("cds.fa", "fa"),
                ("pep.fa", "fasta"),
                ("paralogs.txt", "txt"),
            ],
            "Fasta Formatter": [
                ("fasta_formater.txt", "txt"),
            ],
            " BioAlignX, AlignSeq Pro, and Phylogenetic Analysis": [
                ("cds.fa", "fa"),
                ("pep.fa", "fasta"),
                ("probe.fasta","fasta")
            ],
            "Phylogenetic Tree Builder": [
                ("align.fasta", "fasta"),
            ],
            "GenePrimer and GenePrimer X": [
                ("seq_primer.fasta", "fasta")],
            "Gene Density Map": [
                ("gff_file.gff3", "gff3"),
                ("pep_NLR.fasta", "fasta"),
                ("genome.fai", "fai"),],
            "Gene Expression Analyzer": [
                ("expression.xlsx", 'xlsx'),
                ("heatmap.fasta", "fasta"),],
            "Homologus Pair Finder": [
                ("diamond.exe", 'exe'),
                ("pep.fa", "fa"),
            ],
            "HmmerBuild and HmmerSearch": [
                ("pep.fa", "fa"),
                ("hmm_profile.hmm","hmm"),
                ("pep_NLR.fasta","fasta")
            ]
            
        }

        # Adding buttons for each category
        for group, files in file_groups.items():
            group_box = QGroupBox(group)
            group_box.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {'#000000' if is_dark_mode else '#FFFFFF'};")
            group_layout = QHBoxLayout()
            for filename, filetype in files:
                button = QPushButton(filename)
                button.setStyleSheet("""
                    QPushButton {
                        font-size: 14px;
                        color: white;
                        background-color: #2C3E50;
                        border: none;
                        border-radius: 4px;
                        padding: 5px 10px;
                    }
                    QPushButton:hover {
                        background-color: #34495E;
                    }
                """)
                button.clicked.connect(lambda _, f=filename: self.download_example_data(f))
                group_layout.addWidget(button)
            group_box.setLayout(group_layout)
            button_layout.addWidget(group_box)

        button_widget.setLayout(button_layout)
        scroll_area.setWidget(button_widget)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def download_example_data(self, filename):
        source_filepath = Path(get_resource_path('data')) / filename
        downloads_folder = Path.home() / "Downloads" / filename

        try:
            if source_filepath.exists():
                shutil.copy(source_filepath, downloads_folder)
                QMessageBox.information(self, "Download Successful",
                                        f"{filename} has been downloaded to your Downloads folder.")
            else:
                QMessageBox.warning(self, "File Not Found", f"{filename} not found in the data directory.")
        except Exception as e:
            QMessageBox.critical(self, "Download Failed", f"An error occurred: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genome Wide Workbench")
        self.setWindowIcon(QIcon(get_resource_path('src/image.png')))
        self.setGeometry(200, 200, 800, 600)

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Horizontal layout for sidebar and content
        content_layout = QHBoxLayout()

        # Sidebar for tools
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("background-color: #2C3E50;")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(5)

        # Sidebar title
        sidebar_title = QLabel("Tools")
        sidebar_title.setAlignment(Qt.AlignCenter)
        sidebar_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; padding: 4px;")
        sidebar_layout.addWidget(sidebar_title)

        # List of all tools
        tools = [
            "AlignSeq Pro",
            "BioAlignX",
            "BlastXPlorer",
            "FASTA Formatter",
            "Gene Density MAP",
            "Gene Expression Analyzer",
            "GenePrimer",
            "GenePrimer X",
            "HMMerBuild",
            "HMMerSearch",
            "Homologus Pair Finder",
            "KaKs Analyzer",
            "Phylogenetic Analysis",
            "Phylogenetic Tree Builder"
        ]

        # Add tool buttons to sidebar
        for tool in tools:
            button = QPushButton(tool)
            button.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    color: white;
                    background-color: #34495E;
                    border: none;
                    border-radius: 4px;
                    padding: 6px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #3E5C76;
                }
            """)
            button.clicked.connect(lambda _, t=tool: self.open_tool(t))
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()
        content_layout.addWidget(self.sidebar)

        # Stacked widget for content
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget, stretch=1)

        main_layout.addLayout(content_layout)

        # Spacer to push footer down
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)

        # Footer
        self.footer = QLabel("© 2025 Genome Wide Workbench. All rights reserved.")
        self.footer.setAlignment(Qt.AlignCenter)
        self.footer.setStyleSheet("background-color: #2C3E50; color: white; padding: 10px;")
        self.footer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        main_layout.addWidget(self.footer)

        self.create_menu_bar()
        self.setStyleSheet(self.get_stylesheet())

        self.tool_windows = {}
        self.show_welcome_screen()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("background-color: #2C3E50; color: white;")

        # Home menu
        home_menu = QMenu("Home", self)
        home_menu.addAction(QAction("Welcome", self, triggered=self.show_welcome_screen))
        menu_bar.addMenu(home_menu)

        # Data menu
        data_menu = QMenu("Data", self)
        data_menu.addAction(QAction("Data Tab", self, triggered=self.show_data_tab))
        menu_bar.addMenu(data_menu)

        # Tool category menus
        tool_categories = {
            "Mining": ["BlastXPlorer", "HMMerBuild", "HMMerSearch","FASTA Formatter"],
            "Classification": ["AlignSeq Pro", "BioAlignX", "Phylogenetic Analysis", "Phylogenetic Tree Builder"],
            "Gene Density Map": ["Gene Density MAP"],
            "Evolutionary Analysis": ["Homologus Pair Finder", "KaKs Analyzer"],
            "Primer Design": ["GenePrimer", "GenePrimer X"],
            "Visualization": ["Gene Expression Analyzer"]
        }

        # Add category menus before About
        for category, tools in tool_categories.items():
            category_menu = QMenu(category, self)
            for tool in tools:
                action = QAction(tool, self)
                action.triggered.connect(lambda _, t=tool: self.open_tool(t))
                category_menu.addAction(action)
            menu_bar.addMenu(category_menu)

        # About menu
        about_menu = QMenu("About", self)
        about_menu.addAction(QAction("About", self, triggered=self.show_about))
        about_menu.addAction(QAction("Documentation", self, triggered=self.show_documentation))
        about_menu.addAction(QAction("Contact", self, triggered=self.show_contact))
        about_menu.addAction(QAction("Help", self, triggered=self.show_help))
        menu_bar.addMenu(about_menu)

    def show_welcome_screen(self):
        welcome_widget = WelcomeScreen()
        self.stacked_widget.addWidget(welcome_widget)
        self.stacked_widget.setCurrentWidget(welcome_widget)

    def show_data_tab(self):
        data_widget = DataInfoWidget()
        self.stacked_widget.addWidget(data_widget)
        self.stacked_widget.setCurrentWidget(data_widget)

    def open_tool(self, tool_name):
        """Switch to a specific tool view, creating it if necessary."""
        if tool_name not in self.tool_windows:
            # Lazy imports for tool modules
            if tool_name == "FASTA Formatter":
                from fasta_formatter import FastaFilterTool
                tool_widget = FastaFilterTool()
            elif tool_name == "GenePrimer":
                from primer_designing_basic import Primer3App
                tool_widget = Primer3App()
            elif tool_name == "GenePrimer X":
                from primer_designing_adv import Primer3App_adv
                tool_widget = Primer3App_adv()
            elif tool_name == "BlastXPlorer":
                from blast import Blast
                tool_widget = Blast()
            elif tool_name == "KaKs Analyzer":
                from kaks import SequenceAnalysisApp
                tool_widget = SequenceAnalysisApp()
            elif tool_name == "AlignSeq Pro":
                from align_triming import FastaApp
                tool_widget = FastaApp()
            elif tool_name == "BioAlignX":
                from align import AlignApp
                tool_widget = AlignApp()
            elif tool_name == "Phylogenetic Analysis":
                from phylogenetic_analysis import FastaApp
                tool_widget = FastaApp()
            elif tool_name == "Phylogenetic Tree Builder":
                from tree import FastaAppTree
                tool_widget = FastaAppTree()
            elif tool_name == "Gene Density MAP":
                from loci_map import GFFFilterApp
                tool_widget = GFFFilterApp()
            elif tool_name == "Homologus Pair Finder":
                from homologus_pair import DiamondApp
                tool_widget = DiamondApp()
            elif tool_name == "Gene Expression Analyzer":
                from heatmap import HeatmapApp
                tool_widget = HeatmapApp()
            elif tool_name == "HMMerBuild":
                from hmm_build import HMMBuildApp
                tool_widget = HMMBuildApp()
            elif tool_name == "HMMerSearch":
                from hmm_search import HMMSearchApp
                tool_widget = HMMSearchApp()
            else:
                tool_widget = ToolWindow(tool_name)
            
            self.stacked_widget.addWidget(tool_widget)
            self.tool_windows[tool_name] = tool_widget
        
        self.stacked_widget.setCurrentWidget(self.tool_windows[tool_name])

    def show_about(self):
        QMessageBox.information(self, "About", "Genome Wide WorkBench v1.0 - A bioinformatics toolkit.")

    def show_documentation(self):
        QMessageBox.information(self, "Documentation", "For documentation, visit our github.")

    def show_contact(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Contact")
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setText('Contact us at: <a href="mailto:evolutionarybiologylabuaf@gmail.com">evolutionarybiologylabuaf@gmail.com</a>')
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def show_help(self):
        QMessageBox.information(self, "Help", "Refer to the documentation or contact support.")

    def get_stylesheet(self):
        return """
    QPushButton {
        font-size: 14px;
        padding: 10px;
        color: #FFFFFF;
        background-color: #2C3E50;
        border: none;
    }
    QPushButton:hover {
        background-color: #34495E;
    }
    QWidget#footer {
        font-size: 14px;
        color: #FFFFFF;
        background-color: #2C3E50;
        padding: 5px;
    }
        """

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())