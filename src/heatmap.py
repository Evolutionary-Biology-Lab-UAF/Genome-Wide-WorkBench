# # import sys
# # import os
# # import pandas as pd
# # from pathlib import Path
# # from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, 
# #                               QLabel, QFileDialog, QMessageBox, QHBoxLayout,
# #                               QLineEdit, QScrollArea, QListWidget, QListWidgetItem,
# #                               QAbstractItemView, QCheckBox, QSpinBox, QComboBox,
# #                               QDialog, QProgressBar)
# # from PySide6.QtCore import QThread, Signal, Qt
# # from PySide6.QtGui import QIcon, QPixmap
# # from Bio import SeqIO
# # import matplotlib
# # matplotlib.use('Agg')
# # from matplotlib.figure import Figure
# # import seaborn as sns
# # import matplotlib.pyplot as plt

# # class ProgressDialog(QDialog):
# #     def __init__(self, parent=None):
# #         super().__init__(parent)
# #         self.setWindowTitle("Processing")
# #         self.setFixedSize(300, 100)
# #         layout = QVBoxLayout()
# #         self.progress_label = QLabel("Generating heatmap...")
# #         self.progress_bar = QProgressBar()
# #         self.progress_bar.setRange(0, 0)  # Indeterminate progress
# #         layout.addWidget(self.progress_label)
# #         layout.addWidget(self.progress_bar)
# #         self.setLayout(layout)

# # class EnhancedHeatmapWorker(QThread):
# #     progress = Signal(str)
# #     finished = Signal(pd.DataFrame)
# #     error = Signal(str)

# #     def __init__(self, fasta_path, xlsx_path, selected_columns, sort_genes):
# #         super().__init__()
# #         self.fasta_path = fasta_path
# #         self.xlsx_path = xlsx_path
# #         self.selected_columns = selected_columns
# #         self.sort_genes = sort_genes

# #     def run(self):
# #         try:
# #             self.progress.emit("Reading FASTA file...")
# #             fasta_ids = [rec.id for rec in SeqIO.parse(self.fasta_path, "fasta")]
            
# #             self.progress.emit("Loading expression data...")
# #             expr = pd.read_excel(self.xlsx_path, index_col=0)
            
# #             self.progress.emit("Filtering genes...")
# #             filtered = expr[expr.index.isin(fasta_ids)]
# #             if filtered.empty:
# #                 raise ValueError("No matching genes found")
            
# #             self.progress.emit("Processing data...")
# #             processed = filtered[self.selected_columns]
            
# #             if self.sort_genes:
# #                 processed['mean'] = processed.mean(axis=1)
# #                 processed = processed.sort_values('mean', ascending=False).drop(columns=['mean'])
            
# #             self.finished.emit(processed)
            
# #         except Exception as e:
# #             self.error.emit(str(e))

# # class HeatmapApp(QWidget):
# #     def __init__(self):
# #         super().__init__()
# #         self.init_ui()
# #         self.current_figure = None
# #         self.processed_data = None
# #         self.progress_dialog = None

# #     def init_ui(self):
# #         if getattr(sys, 'frozen', False):
# #                base_path = sys._MEIPASS
# #         else:
# #                base_path = os.path.abspath(".")

# #         icon_path = os.path.join(base_path, "img.png")
# #         self.setWindowIcon(QIcon(icon_path))

# #         self.setWindowTitle("Gene Expression Analyzer")
# #         self.setWindowIcon(QIcon("src/image.png"))
# #         # self.setWindowIcon(QIcon("genome_wide_workbemch_n.ico"))

# #         self.setMinimumSize(1200, 800)

# #         main_layout = QHBoxLayout()
# #         left_panel = QVBoxLayout()
# #         right_panel = QVBoxLayout()

# #         # File inputs
# #         self.fasta_line_edit = QLineEdit()
# #         self.xlsx_line_edit = QLineEdit()
# #         self.fasta_line_edit.setReadOnly(True)
# #         self.xlsx_line_edit.setReadOnly(True)
        
# #         fasta_layout = self.create_file_input("FASTA File:", self.fasta_line_edit, self.load_fasta)
# #         xlsx_layout = self.create_file_input("XLSX File:", self.xlsx_line_edit, self.load_xlsx)
        
# #         # Heatmap type selection
# #         heatmap_type_layout = QHBoxLayout()
# #         heatmap_type_layout.addWidget(QLabel("Heatmap Type:"))
# #         self.heatmap_type_combo = QComboBox()
# #         self.heatmap_type_combo.addItems(["Standard Heatmap", "Clustered Heatmap"])
# #         heatmap_type_layout.addWidget(self.heatmap_type_combo)

# #         # Column selection list
# #         self.column_list = QListWidget()
# #         self.column_list.setSelectionMode(QAbstractItemView.MultiSelection)
        
# #         # Row selection
# #         row_control = QHBoxLayout()
# #         self.row_spin = QSpinBox()
# #         self.row_spin.setMinimum(1)
# #         self.row_spin.setValue(1)
# #         row_control.addWidget(QLabel("Rows to Display:"))
# #         row_control.addWidget(self.row_spin)

# #         # Color controls
# #         palette_layout = QHBoxLayout()
# #         palette_layout.addWidget(QLabel("Color Palette:"))
# #         self.palette_combo = QComboBox()
# #         # self.palette_combo.addItems(['Reds', 'Blues', 'Greens', 'viridis', 'plasma', 'coolwarm'])
# #         self.palette_combo.addItems(['Reds', 'Blues', 'Greens', 'viridis', 'plasma', 'coolwarm', 'Spectral', 'magma', 'inferno'])

# #         palette_layout.addWidget(self.palette_combo)
        
# #         # Sorting checkbox
# #         self.sort_checkbox = QCheckBox("Sort by highest expression")
# #         self.sort_checkbox.setChecked(True)

# #         # Control buttons
# #         btn_layout = QHBoxLayout()
# #         self.process_btn = QPushButton("Generate Heatmap")
# #         self.process_btn.clicked.connect(self.start_processing)
# #         self.download_btn = QPushButton("Download")
# #         self.download_btn.clicked.connect(self.save_heatmap)
# #         btn_layout.addWidget(self.process_btn)
# #         btn_layout.addWidget(self.download_btn)

# #         # Left panel setup
# #         left_panel.addLayout(fasta_layout)
# #         left_panel.addLayout(xlsx_layout)
# #         left_panel.addLayout(heatmap_type_layout)
# #         left_panel.addWidget(QLabel("Select Columns:"))
# #         left_panel.addWidget(self.column_list)
# #         left_panel.addLayout(row_control)
# #         left_panel.addLayout(palette_layout)
# #         left_panel.addWidget(self.sort_checkbox)
# #         left_panel.addLayout(btn_layout)

# #         # Heatmap display with scroll
# #         scroll = QScrollArea()
# #         self.heatmap_label = QLabel()
# #         self.heatmap_label.setAlignment(Qt.AlignCenter)
# #         scroll.setWidget(self.heatmap_label)
# #         scroll.setWidgetResizable(True)
        
# #         right_panel.addWidget(scroll)
# #         right_panel.addWidget(QLabel("Status:"))
# #         self.status = QLabel()
# #         right_panel.addWidget(self.status)

# #         main_layout.addLayout(left_panel, 30)
# #         main_layout.addLayout(right_panel, 70)
# #         self.setLayout(main_layout)

# #     def create_file_input(self, label, line_edit, handler):
# #         layout = QHBoxLayout()
# #         btn = QPushButton("Browse")
# #         btn.clicked.connect(handler)
# #         layout.addWidget(QLabel(label))
# #         layout.addWidget(line_edit)
# #         layout.addWidget(btn)
# #         return layout

# #     def load_fasta(self):
# #         path, _ = QFileDialog.getOpenFileName(self, "Open FASTA", "", "FASTA (*.fasta)")
# #         if path:
# #             self.fasta_path = path
# #             self.fasta_line_edit.setText(Path(path).name)

# #     def load_xlsx(self):
# #         path, _ = QFileDialog.getOpenFileName(self, "Open XLSX", "", "Excel Files (*.xlsx)")
# #         if path:
# #             self.xlsx_path = path
# #             self.xlsx_line_edit.setText(Path(path).name)
# #             self.load_columns(path)

# #     def load_columns(self, path):
# #         try:
# #             df = pd.read_excel(path, index_col=0)
# #             self.available_columns = df.columns.tolist()
# #             self.column_list.clear()
# #             for col in self.available_columns:
# #                 item = QListWidgetItem(col)
# #                 item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
# #                 item.setCheckState(Qt.Checked)
# #                 self.column_list.addItem(item)
# #             self.selected_columns = self.available_columns.copy()
# #         except Exception as e:
# #             QMessageBox.critical(self, "Error", f"Failed to read columns: {str(e)}")

# #     def update_selected_columns(self):
# #         self.selected_columns = []
# #         for i in range(self.column_list.count()):
# #             item = self.column_list.item(i)
# #             if item.checkState() == Qt.Checked:
# #                 self.selected_columns.append(item.text())

# #     def start_processing(self):
# #         if not hasattr(self, 'fasta_path') or not hasattr(self, 'xlsx_path'):
# #             QMessageBox.warning(self, "Error", "Please select both files")
# #             return

# #         self.update_selected_columns()
# #         if not self.selected_columns:
# #             QMessageBox.warning(self, "Error", "Please select at least one column")
# #             return

# #         # Show progress dialog
# #         self.progress_dialog = ProgressDialog(self)
# #         self.progress_dialog.show()

# #         self.worker = EnhancedHeatmapWorker(
# #             self.fasta_path,
# #             self.xlsx_path,
# #             self.selected_columns,
# #             self.sort_checkbox.isChecked()
# #         )
# #         self.worker.progress.connect(self.update_progress)
# #         self.worker.finished.connect(self.handle_data)
# #         self.worker.error.connect(self.handle_error)
# #         self.worker.start()

# #     def update_progress(self, message):
# #         if self.progress_dialog:
# #             self.progress_dialog.progress_label.setText(message)

# #     def handle_data(self, processed_df):     
# #         self.processed_data = processed_df
# #         max_rows = len(processed_df)
# #         current_value = self.row_spin.value()
# #         new_value = current_value if 1 <= current_value <= max_rows else max_rows
# #         self.row_spin.setMaximum(max_rows)
# #         self.row_spin.setValue(new_value)
# #         self.generate_heatmap()
# #         if self.progress_dialog:
# #             self.progress_dialog.close()

# #     def handle_error(self, message):
# #         if self.progress_dialog:
# #             self.progress_dialog.close()
# #         QMessageBox.critical(self, "Error", message)
# #         self.status.setText("")

# #     def generate_heatmap(self):
# #         if self.processed_data is None:
# #             return

# #         try:
# #             n_rows = self.row_spin.value()
# #             display_data = self.processed_data.head(n_rows)
            
# #             heatmap_type = self.heatmap_type_combo.currentText()
# #             palette_name = self.palette_combo.currentText()

# #             if heatmap_type == "Clustered Heatmap":
# #                 # Create clustered heatmap
# #                 grid = sns.clustermap(
# #                     display_data,
# #                     cmap=palette_name,
# #                     linewidths=0.5,
# #                     linecolor='black',
# #                     figsize=(12, n_rows*0.4),
# #                     yticklabels=True,
# #                     robust=True
# #                 )
# #                 fig = grid.figure
# #             else:
# #                 # Standard heatmap
# #                 fig = Figure(figsize=(12, n_rows*0.4))
# #                 ax = fig.add_subplot(111)
# #                 sns.heatmap(
# #                     display_data,
# #                     cmap=palette_name,
# #                     ax=ax,
# #                     linewidths=0.5,
# #                     linecolor='black',
# #                     cbar_kws={'label': 'Expression Level'},
# #                     yticklabels=True,
# #                     robust=True
# #                 )
# #                 ax.set_title("Gene Expression Heatmap", fontsize=14)
# #                 ax.tick_params(axis='y', labelsize=8)

# #             plt.tight_layout()
# #             temp_path = "heatmap.png"
# #             fig.savefig(temp_path, bbox_inches='tight', dpi=150)
            
# #             pixmap = QPixmap(temp_path)
# #             self.heatmap_label.setPixmap(pixmap)
# #             self.current_figure = fig
# #             self.status.setText(f"Displaying top {n_rows} of {len(self.processed_data)} genes ({heatmap_type})")
# #             plt.close(fig)  # Clean up matplotlib resources

# #         except Exception as e:
# #             self.handle_error(str(e))

# #     def save_heatmap(self):
# #         if not self.current_figure:
# #             QMessageBox.warning(self, "Error", "Generate a heatmap first")
# #             return
# #         path, selected_filter = QFileDialog.getSaveFileName(self, "Save Heatmap", "",         "PNG (*.png);;SVG (*.svg)")
# #         if path:
# #             try:
# #                 # Determine format from filter selection
# #                 if selected_filter == "SVG (*.svg)":
# #                     if not path.lower().endswith('.svg'):
# #                        path += '.svg'


# #                     self.current_figure.savefig(path, format='svg', bbox_inches='tight', dpi=300)
# #                 else:
# #                     if not path.lower().endswith('.png'):
# #                         path += '.png'
# #                     self.current_figure.savefig(path, dpi=300, bbox_inches='tight')


# #                 self.status.setText(f"Heatmap saved to {path}")
# #             except Exception as e:
# #                 self.handle_error(str(e))

# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     window = HeatmapApp()
# #     window.show()
# #     sys.exit(app.exec())


# import sys
# import os
# import pandas as pd
# from pathlib import Path
# from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, 
#                               QLabel, QFileDialog, QMessageBox, QHBoxLayout,
#                               QLineEdit, QScrollArea, QListWidget, QListWidgetItem,
#                               QAbstractItemView, QCheckBox, QSpinBox, QComboBox,
#                               QDialog, QProgressBar)
# from PySide6.QtCore import QThread, Signal, Qt
# from PySide6.QtGui import QIcon, QPixmap, QFont
# from Bio import SeqIO
# import matplotlib
# matplotlib.use('Agg')
# from matplotlib.figure import Figure
# import seaborn as sns
# import matplotlib.pyplot as plt

# class ProgressDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Processing")
#         self.setFixedSize(300, 100)
#         layout = QVBoxLayout()
#         self.progress_label = QLabel("Generating heatmap...")
#         self.progress_bar = QProgressBar()
#         self.progress_bar.setRange(0, 0)  # Indeterminate progress
#         layout.addWidget(self.progress_label)
#         layout.addWidget(self.progress_bar)
#         self.setLayout(layout)

# class EnhancedHeatmapWorker(QThread):
#     progress = Signal(str)
#     finished = Signal(pd.DataFrame)
#     error = Signal(str)

#     def __init__(self, fasta_path, xlsx_path, selected_columns, sort_genes):
#         super().__init__()
#         self.fasta_path = fasta_path
#         self.xlsx_path = xlsx_path
#         self.selected_columns = selected_columns
#         self.sort_genes = sort_genes

#     def run(self):
#         try:
#             self.progress.emit("Reading FASTA file...")
#             fasta_ids = [rec.id for rec in SeqIO.parse(self.fasta_path, "fasta")]
            
#             self.progress.emit("Loading expression data...")
#             expr = pd.read_excel(self.xlsx_path, index_col=0)
            
#             self.progress.emit("Filtering genes...")
#             filtered = expr[expr.index.isin(fasta_ids)]
#             if filtered.empty:
#                 raise ValueError("No matching genes found")
            
#             self.progress.emit("Processing data...")
#             processed = filtered[self.selected_columns]
            
#             if self.sort_genes:
#                 processed['mean'] = processed.mean(axis=1)
#                 processed = processed.sort_values('mean', ascending=False).drop(columns=['mean'])
            
#             self.finished.emit(processed)
            
#         except Exception as e:
#             self.error.emit(str(e))

# class HeatmapApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()
#         self.current_figure = None
#         self.processed_data = None
#         self.progress_dialog = None

#     def init_ui(self):
#         if getattr(sys, 'frozen', False):
#                base_path = sys._MEIPASS
#         else:
#                base_path = os.path.abspath(".")

#         icon_path = os.path.join(base_path, "img.png")
#         self.setWindowIcon(QIcon(icon_path))

#         self.setWindowTitle("Genome Wide Workbench")
#         self.setWindowIcon(QIcon("src/image.png"))

#         self.setMinimumSize(1200, 800)

#         main_layout = QHBoxLayout()
#         left_panel = QVBoxLayout()
#         right_panel = QVBoxLayout()

#         # Header
#         self.header_label = QLabel("Gene Expression Analyzer")
#         self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.header_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
#         self.header_label.setStyleSheet("""
#             QLabel {
#                 background-color: #2C3E50;
#                 color: white;
#                 padding: 10px;
#                 border-radius: 10px;
#             }
#         """)
#         self.header_label.setFixedHeight(150)

#         # File inputs
#         self.fasta_line_edit = QLineEdit()
#         self.xlsx_line_edit = QLineEdit()
#         self.fasta_line_edit.setReadOnly(True)
#         self.xlsx_line_edit.setReadOnly(True)
        
#         fasta_layout = self.create_file_input("FASTA File:", self.fasta_line_edit, self.load_fasta)
#         xlsx_layout = self.create_file_input("XLSX File:", self.xlsx_line_edit, self.load_xlsx)
        
#         # Heatmap type selection
#         heatmap_type_layout = QHBoxLayout()
#         heatmap_type_layout.addWidget(QLabel("Heatmap Type:"))
#         self.heatmap_type_combo = QComboBox()
#         self.heatmap_type_combo.addItems(["Standard Heatmap", "Clustered Heatmap"])
#         heatmap_type_layout.addWidget(self.heatmap_type_combo)

#         # Column selection list
#         self.column_list = QListWidget()
#         self.column_list.setSelectionMode(QAbstractItemView.MultiSelection)
        
#         # Row selection
#         row_control = QHBoxLayout()
#         self.row_spin = QSpinBox()
#         self.row_spin.setMinimum(1)
#         self.row_spin.setValue(1)
#         row_control.addWidget(QLabel("Rows to Display:"))
#         row_control.addWidget(self.row_spin)

#         # Color controls
#         palette_layout = QHBoxLayout()
#         palette_layout.addWidget(QLabel("Color Palette:"))
#         self.palette_combo = QComboBox()
#         self.palette_combo.addItems(['Reds', 'Blues', 'Greens', 'viridis', 'plasma', 'coolwarm', 'Spectral', 'magma', 'inferno'])
#         palette_layout.addWidget(self.palette_combo)
        
#         # Sorting checkbox
#         self.sort_checkbox = QCheckBox("Sort by highest expression")
#         self.sort_checkbox.setChecked(True)

#         # Control buttons
#         btn_layout = QHBoxLayout()
#         self.process_btn = QPushButton("Generate Heatmap")
#         self.process_btn.clicked.connect(self.start_processing)
#         self.download_btn = QPushButton("Download")
#         self.download_btn.clicked.connect(self.save_heatmap)
#         btn_layout.addWidget(self.process_btn)
#         btn_layout.addWidget(self.download_btn)

#         # Left panel setup
#         left_panel.addWidget(self.header_label)
#         left_panel.addLayout(fasta_layout)
#         left_panel.addLayout(xlsx_layout)
#         left_panel.addLayout(heatmap_type_layout)
#         left_panel.addWidget(QLabel("Select Columns:"))
#         left_panel.addWidget(self.column_list)
#         left_panel.addLayout(row_control)
#         left_panel.addLayout(palette_layout)
#         left_panel.addWidget(self.sort_checkbox)
#         left_panel.addLayout(btn_layout)

#         # Heatmap display with scroll
#         scroll = QScrollArea()
#         self.heatmap_label = QLabel()
#         self.heatmap_label.setAlignment(Qt.AlignCenter)
#         scroll.setWidget(self.heatmap_label)
#         scroll.setWidgetResizable(True)
        
#         right_panel.addWidget(scroll)
#         right_panel.addWidget(QLabel("Status:"))
#         self.status = QLabel()
#         right_panel.addWidget(self.status)

#         main_layout.addLayout(left_panel, 30)
#         main_layout.addLayout(right_panel, 70)
#         self.setLayout(main_layout)

#     def create_file_input(self, label, line_edit, handler):
#         layout = QHBoxLayout()
#         btn = QPushButton("Browse")
#         btn.clicked.connect(handler)
#         layout.addWidget(QLabel(label))
#         layout.addWidget(line_edit)
#         layout.addWidget(btn)
#         return layout

#     def load_fasta(self):
#         path, _ = QFileDialog.getOpenFileName(self, "Open FASTA", "", "FASTA (*.fasta)")
#         if path:
#             self.fasta_path = path
#             self.fasta_line_edit.setText(Path(path).name)

#     def load_xlsx(self):
#         path, _ = QFileDialog.getOpenFileName(self, "Open XLSX", "", "Excel Files (*.xlsx)")
#         if path:
#             self.xlsx_path = path
#             self.xlsx_line_edit.setText(Path(path).name)
#             self.load_columns(path)

#     def load_columns(self, path):
#         try:
#             df = pd.read_excel(path, index_col=0)
#             self.available_columns = df.columns.tolist()
#             self.column_list.clear()
#             for col in self.available_columns:
#                 item = QListWidgetItem(col)
#                 item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
#                 item.setCheckState(Qt.Checked)
#                 self.column_list.addItem(item)
#             self.selected_columns = self.available_columns.copy()
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Failed to read columns: {str(e)}")

#     def update_selected_columns(self):
#         self.selected_columns = []
#         for i in range(self.column_list.count()):
#             item = self.column_list.item(i)
#             if item.checkState() == Qt.Checked:
#                 self.selected_columns.append(item.text())

#     def start_processing(self):
#         if not hasattr(self, 'fasta_path') or not hasattr(self, 'xlsx_path'):
#             QMessageBox.warning(self, "Error", "Please select both files")
#             return

#         self.update_selected_columns()
#         if not self.selected_columns:
#             QMessageBox.warning(self, "Error", "Please select at least one column")
#             return

#         # Show progress dialog
#         self.progress_dialog = ProgressDialog(self)
#         self.progress_dialog.show()

#         self.worker = EnhancedHeatmapWorker(
#             self.fasta_path,
#             self.xlsx_path,
#             self.selected_columns,
#             self.sort_checkbox.isChecked()
#         )
#         self.worker.progress.connect(self.update_progress)
#         self.worker.finished.connect(self.handle_data)
#         self.worker.error.connect(self.handle_error)
#         self.worker.start()

#     def update_progress(self, message):
#         if self.progress_dialog:
#             self.progress_dialog.progress_label.setText(message)

#     def handle_data(self, processed_df):     
#         self.processed_data = processed_df
#         max_rows = len(processed_df)
#         current_value = self.row_spin.value()
#         new_value = current_value if 1 <= current_value <= max_rows else max_rows
#         self.row_spin.setMaximum(max_rows)
#         self.row_spin.setValue(new_value)
#         self.generate_heatmap()
#         if self.progress_dialog:
#             self.progress_dialog.close()

#     def handle_error(self, message):
#         if self.progress_dialog:
#             self.progress_dialog.close()
#         QMessageBox.critical(self, "Error", message)
#         self.status.setText("")

#     def generate_heatmap(self):
#         if self.processed_data is None:
#             return

#         try:
#             n_rows = self.row_spin.value()
#             display_data = self.processed_data.head(n_rows)
            
#             heatmap_type = self.heatmap_type_combo.currentText()
#             palette_name = self.palette_combo.currentText()

#             if heatmap_type == "Clustered Heatmap":
#                 # Create clustered heatmap
#                 grid = sns.clustermap(
#                     display_data,
#                     cmap=palette_name,
#                     linewidths=0.5,
#                     linecolor='black',
#                     figsize=(12, n_rows*0.4),
#                     yticklabels=True,
#                     robust=True
#                 )
#                 fig = grid.figure
#             else:
#                 # Standard heatmap
#                 fig = Figure(figsize=(12, n_rows*0.4))
#                 ax = fig.add_subplot(111)
#                 sns.heatmap(
#                     display_data,
#                     cmap=palette_name,
#                     ax=ax,
#                     linewidths=0.5,
#                     linecolor='black',
#                     cbar_kws={'label': 'Expression Level'},
#                     yticklabels=True,
#                     robust=True
#                 )
#                 ax.set_title("Gene Expression Heatmap", fontsize=14)
#                 ax.tick_params(axis='y', labelsize=8)

#             plt.tight_layout()
#             temp_path = "heatmap.png"
#             fig.savefig(temp_path, bbox_inches='tight', dpi=150)
            
#             pixmap = QPixmap(temp_path)
#             self.heatmap_label.setPixmap(pixmap)
#             self.current_figure = fig
#             self.status.setText(f"Displaying top {n_rows} of {len(self.processed_data)} genes ({heatmap_type})")
#             plt.close(fig)  # Clean up matplotlib resources

#         except Exception as e:
#             self.handle_error(str(e))

#     def save_heatmap(self):
#         if not self.current_figure:
#             QMessageBox.warning(self, "Error", "Generate a heatmap first")
#             return
#         path, selected_filter = QFileDialog.getSaveFileName(self, "Save Heatmap", "", "PNG (*.png);;SVG (*.svg)")
#         if path:
#             try:
#                 # Determine format from filter selection
#                 if selected_filter == "SVG (*.svg)":
#                     if not path.lower().endswith('.svg'):
#                        path += '.svg'
#                     self.current_figure.savefig(path, format='svg', bbox_inches='tight', dpi=300)
#                 else:
#                     if not path.lower().endswith('.png'):
#                         path += '.png'
#                     self.current_figure.savefig(path, dpi=300, bbox_inches='tight')
#                 self.status.setText(f"Heatmap saved to {path}")
#             except Exception as e:
#                 self.handle_error(str(e))

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = HeatmapApp()
#     window.show()
#     sys.exit(app.exec())



import sys
import os
import pandas as pd
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, 
                              QLabel, QFileDialog, QMessageBox, QHBoxLayout,
                              QLineEdit, QScrollArea, QListWidget, QListWidgetItem,
                              QAbstractItemView, QCheckBox, QSpinBox, QComboBox,
                              QDialog, QProgressBar)
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QIcon, QPixmap, QFont
from Bio import SeqIO
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
import seaborn as sns
import matplotlib.pyplot as plt

class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Processing")
        self.setFixedSize(300, 100)
        layout = QVBoxLayout()
        self.progress_label = QLabel("Generating heatmap...")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

class XlsxLoadingWorker(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        try:
            df = pd.read_excel(self.path, index_col=0)
            self.finished.emit(self.path)
        except Exception as e:
            self.error.emit(str(e))

class EnhancedHeatmapWorker(QThread):
    progress = Signal(str)
    finished = Signal(pd.DataFrame)
    error = Signal(str)

    def __init__(self, fasta_path, xlsx_path, selected_columns, sort_genes):
        super().__init__()
        self.fasta_path = fasta_path
        self.xlsx_path = xlsx_path
        self.selected_columns = selected_columns
        self.sort_genes = sort_genes

    def run(self):
        try:
            self.progress.emit("Reading FASTA file...")
            fasta_ids = [rec.id for rec in SeqIO.parse(self.fasta_path, "fasta")]
            
            self.progress.emit("Loading expression data...")
            expr = pd.read_excel(self.xlsx_path, index_col=0)
            
            self.progress.emit("Filtering genes...")
            filtered = expr[expr.index.isin(fasta_ids)]
            if filtered.empty:
                raise ValueError("No matching genes found")
            
            self.progress.emit("Processing data...")
            processed = filtered[self.selected_columns]
            
            if self.sort_genes:
                processed['mean'] = processed.mean(axis=1)
                processed = processed.sort_values('mean', ascending=False).drop(columns=['mean'])
            
            self.finished.emit(processed)
            
        except Exception as e:
            self.error.emit(str(e))

class HeatmapApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_figure = None
        self.processed_data = None
        self.progress_dialog = None
        self.xlsx_path = None
        self.upload_msg = None

    def init_ui(self):
        if getattr(sys, 'frozen', False):
               base_path = sys._MEIPASS
        else:
               base_path = os.path.abspath(".")

        icon_path = os.path.join(base_path, "img.png")
        self.setWindowIcon(QIcon(icon_path))

        self.setWindowTitle("Genome Wide Workbench")
        self.setWindowIcon(QIcon("src/image.png"))

        self.setGeometry(100, 100, 1000, 1000)

        main_layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()

        # Header
        self.header_label = QLabel("Gene Expression Analyzer")
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

        # File inputs
        self.fasta_line_edit = QLineEdit()
        self.xlsx_line_edit = QLineEdit()
        self.fasta_line_edit.setReadOnly(True)
        self.xlsx_line_edit.setReadOnly(True)
        
        fasta_layout = self.create_file_input("FASTA File:", self.fasta_line_edit, self.load_fasta)
        xlsx_layout = self.create_file_input("XLSX File:", self.xlsx_line_edit, self.load_xlsx)
        
        # Heatmap type selection
        heatmap_type_layout = QHBoxLayout()
        heatmap_type_layout.addWidget(QLabel("Heatmap Type:"))
        self.heatmap_type_combo = QComboBox()
        self.heatmap_type_combo.addItems(["Standard Heatmap", "Clustered Heatmap"])
        heatmap_type_layout.addWidget(self.heatmap_type_combo)

        # Column selection list
        self.column_list = QListWidget()
        self.column_list.setSelectionMode(QAbstractItemView.MultiSelection)
        
        # Row selection
        row_control = QHBoxLayout()
        self.row_spin = QSpinBox()
        self.row_spin.setMinimum(1)
        self.row_spin.setValue(1)
        row_control.addWidget(QLabel("Rows to Display:"))
        row_control.addWidget(self.row_spin)

        # Color controls
        palette_layout = QHBoxLayout()
        palette_layout.addWidget(QLabel("Color Palette:"))
        self.palette_combo = QComboBox()
        self.palette_combo.addItems(['Reds', 'Blues', 'Greens', 'viridis', 'plasma', 'coolwarm', 'Spectral', 'magma', 'inferno'])
        palette_layout.addWidget(self.palette_combo)
        
        # Sorting checkbox
        self.sort_checkbox = QCheckBox("Sort by highest expression")
        self.sort_checkbox.setChecked(True)

        # Control buttons
        btn_layout = QHBoxLayout()
        self.process_btn = QPushButton("Generate Heatmap")
        self.process_btn.clicked.connect(self.start_processing)
        self.download_btn = QPushButton("Download")
        self.download_btn.clicked.connect(self.save_heatmap)
        btn_layout.addWidget(self.process_btn)
        btn_layout.addWidget(self.download_btn)

        # Left panel setup
        left_panel.addWidget(self.header_label)
        left_panel.addLayout(fasta_layout)
        left_panel.addLayout(xlsx_layout)
        left_panel.addLayout(heatmap_type_layout)
        left_panel.addWidget(QLabel("Select Columns:"))
        left_panel.addWidget(self.column_list)
        left_panel.addLayout(row_control)
        left_panel.addLayout(palette_layout)
        left_panel.addWidget(self.sort_checkbox)
        left_panel.addLayout(btn_layout)

        # Heatmap display with scroll
        scroll = QScrollArea()
        self.heatmap_label = QLabel()
        self.heatmap_label.setAlignment(Qt.AlignCenter)
        scroll.setWidget(self.heatmap_label)
        scroll.setWidgetResizable(True)
        
        right_panel.addWidget(scroll)
        right_panel.addWidget(QLabel("Status:"))
        self.status = QLabel()
        right_panel.addWidget(self.status)

        main_layout.addLayout(left_panel, 30)
        main_layout.addLayout(right_panel, 70)
        self.setLayout(main_layout)

    def create_file_input(self, label, line_edit, handler):
        layout = QHBoxLayout()
        btn = QPushButton("Browse")
        btn.clicked.connect(handler)
        layout.addWidget(QLabel(label))
        layout.addWidget(line_edit)
        layout.addWidget(btn)
        return layout

    def load_fasta(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open FASTA", "", "FASTA (*.fasta)")
        if path:
            self.fasta_path = path
            self.fasta_line_edit.setText(Path(path).name)

    def load_xlsx(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open XLSX", "", "Excel Files (*.xlsx)")
        if path:
            # Show "Uploading..." message with cancel option
            self.upload_msg = QMessageBox(self)
            self.upload_msg.setWindowTitle("Uploading")
            self.upload_msg.setText("Uploading XLSX file, please wait...")
            self.upload_msg.setStandardButtons(QMessageBox.Cancel)
            self.upload_msg.buttonClicked.connect(self.cancel_upload)
            self.upload_msg.show()

            # Start worker thread for XLSX loading
            self.xlsx_worker = XlsxLoadingWorker(path)
            self.xlsx_worker.finished.connect(self.xlsx_loaded)
            self.xlsx_worker.error.connect(self.xlsx_load_error)
            self.xlsx_worker.start()

    def cancel_upload(self, button):
        if button.text() == "Cancel" and self.xlsx_worker.isRunning():
            self.xlsx_worker.terminate()
            if self.upload_msg:
                self.upload_msg.close()
            self.status.setText("Upload cancelled by user")

    def xlsx_loaded(self, path):
        self.xlsx_path = path
        self.xlsx_line_edit.setText(Path(path).name)
        self.load_columns(path)
        if self.upload_msg:
            self.upload_msg.close()

    def xlsx_load_error(self, error_message):
        if self.upload_msg:
            self.upload_msg.close()
        QMessageBox.critical(self, "Error", f"Failed to load XLSX file: {error_message}")

    def load_columns(self, path):
        try:
            df = pd.read_excel(path, index_col=0)
            self.available_columns = df.columns.tolist()
            self.column_list.clear()
            for col in self.available_columns:
                item = QListWidgetItem(col)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Checked)
                self.column_list.addItem(item)
            self.selected_columns = self.available_columns.copy()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read columns: {str(e)}")

    def update_selected_columns(self):
        self.selected_columns = []
        for i in range(self.column_list.count()):
            item = self.column_list.item(i)
            if item.checkState() == Qt.Checked:
                self.selected_columns.append(item.text())

    def start_processing(self):
        if not hasattr(self, 'fasta_path') or not hasattr(self, 'xlsx_path'):
            QMessageBox.warning(self, "Error", "Please select both files")
            return

        self.update_selected_columns()
        if not self.selected_columns:
            QMessageBox.warning(self, "Error", "Please select at least one column")
            return

        # Show progress dialog
        self.progress_dialog = ProgressDialog(self)
        self.progress_dialog.show()

        self.worker = EnhancedHeatmapWorker(
            self.fasta_path,
            self.xlsx_path,
            self.selected_columns,
            self.sort_checkbox.isChecked()
        )
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.handle_data)
        self.worker.error.connect(self.handle_error)
        self.worker.start()

    def update_progress(self, message):
        if self.progress_dialog:
            self.progress_dialog.progress_label.setText(message)

    def handle_data(self, processed_df):     
        self.processed_data = processed_df
        max_rows = len(processed_df)
        current_value = self.row_spin.value()
        new_value = current_value if 1 <= current_value <= max_rows else max_rows
        self.row_spin.setMaximum(max_rows)
        self.row_spin.setValue(new_value)
        self.generate_heatmap()
        if self.progress_dialog:
            self.progress_dialog.close()

    def handle_error(self, message):
        if self.progress_dialog:
            self.progress_dialog.close()
        QMessageBox.critical(self, "Error", message)
        self.status.setText("")

    def generate_heatmap(self):
        if self.processed_data is None:
            return

        try:
            n_rows = self.row_spin.value()
            display_data = self.processed_data.head(n_rows)
            
            heatmap_type = self.heatmap_type_combo.currentText()
            palette_name = self.palette_combo.currentText()

            if heatmap_type == "Clustered Heatmap":
                # Create clustered heatmap
                grid = sns.clustermap(
                    display_data,
                    cmap=palette_name,
                    linewidths=0.5,
                    linecolor='black',
                    figsize=(12, n_rows*0.4),
                    yticklabels=True,
                    robust=True
                )
                fig = grid.figure
            else:
                # Standard heatmap
                fig = Figure(figsize=(12, n_rows*0.4))
                ax = fig.add_subplot(111)
                sns.heatmap(
                    display_data,
                    cmap=palette_name,
                    ax=ax,
                    linewidths=0.5,
                    linecolor='black',
                    cbar_kws={'label': 'Expression Level'},
                    yticklabels=True,
                    robust=True
                )
                ax.set_title("Gene Expression Heatmap", fontsize=14)
                ax.tick_params(axis='y', labelsize=8)

            plt.tight_layout()
            temp_path = "heatmap.png"
            fig.savefig(temp_path, bbox_inches='tight', dpi=150)
            
            pixmap = QPixmap(temp_path)
            self.heatmap_label.setPixmap(pixmap)
            self.current_figure = fig
            self.status.setText(f"Displaying top {n_rows} of {len(self.processed_data)} genes ({heatmap_type})")
            plt.close(fig)  # Clean up matplotlib resources

        except Exception as e:
            self.handle_error(str(e))

    def save_heatmap(self):
        if not self.current_figure:
            QMessageBox.warning(self, "Error", "Generate a heatmap first")
            return
        path, selected_filter = QFileDialog.getSaveFileName(self, "Save Heatmap", "", "PNG (*.png);;SVG (*.svg)")
        if path:
            try:
                # Determine format from filter selection
                if selected_filter == "SVG (*.svg)":
                    if not path.lower().endswith('.svg'):
                       path += '.svg'
                    self.current_figure.savefig(path, format='svg', bbox_inches='tight', dpi=300)
                else:
                    if not path.lower().endswith('.png'):
                        path += '.png'
                    self.current_figure.savefig(path, dpi=300, bbox_inches='tight')
                self.status.setText(f"Heatmap saved to {path}")
            except Exception as e:
                self.handle_error(str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeatmapApp()
    window.show()
    sys.exit(app.exec())