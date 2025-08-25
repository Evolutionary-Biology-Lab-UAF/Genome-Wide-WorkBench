# 🌐 Genome Wide WorkBench (GWW)

**🔬 An integrated, offline, cross-platform platform for multi-omics analysis**  

Genome Wide WorkBench (GWW) brings together essential genomics and proteomics tools into a **single desktop application**.  
It eliminates **fragmented workflows, costly licenses, and internet dependencies**, empowering researchers — especially in **resource-limited environments** — to perform advanced bioinformatics analyses fully **offline**.  

---

![GitHub release](https://img.shields.io/github/v/release/Evolutionary-Biology-Lab-UAF/Genome-Wide-WorkBench?style=flat-square)  
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)  
![Python](https://img.shields.io/badge/Python-3.13+-blue.svg?style=flat-square&logo=python)  
![R](https://img.shields.io/badge/R-4.4+-blue.svg?style=flat-square&logo=r)  

🔗 **Repository**: [Genome-Wide-WorkBench](https://github.com/Evolutionary-Biology-Lab-UAF/Genome-Wide-WorkBench)  
📄 **Manuscript / Preprint**: *Genome Wide WorkBench: Integrated Offline Platform for Multi-Omics Research*  

---

## 🚀 Features

✅ **Sequence Analysis**  
&nbsp;&nbsp;• Multiple Sequence Alignment (MUSCLE5, TrimAl, GBlocks)  
&nbsp;&nbsp;• BLASTXplorer (local BLAST+ with all modes)  
&nbsp;&nbsp;• HMMER search and profile building  

🌳 **Phylogenetics**  
&nbsp;&nbsp;• Automated phylogenetic tree building (IQ-TREE)  
&nbsp;&nbsp;• Tree visualization  

🧬 **Evolutionary Analysis**  
&nbsp;&nbsp;• Homologous pair finder (DIAMOND)  
&nbsp;&nbsp;• Ka/Ks Analysis (KaKs_Calculator + PAL2NAL)  

📊 **Genomics Visualization**  
&nbsp;&nbsp;• Gene density maps  
&nbsp;&nbsp;• Gene expression heatmaps  

🧪 **Primer Design**  
&nbsp;&nbsp;• Primer3 integration (basic & advanced settings)  

🛠️ **Utility Tools**  
&nbsp;&nbsp;• FASTA formatter, validator, and filter  
&nbsp;&nbsp;• Example datasets & Quick Start guide  

---

## 📦 Installation

### Requirements
- Python ≥ 3.13.2  
- R ≥ 4.4.1  
- Pre-packaged dependencies:  
  `BLAST+`, `HMMER`, `IQ-TREE`, `MUSCLE5`, `DIAMOND`, `ClustalW`, `TrimAl`, `Pal2Nal`, `GBlocks`, `Primer3`  

### Steps
```bash
# 1. Clone the repository
git clone https://github.com/Evolutionary-Biology-Lab-UAF/Genome-Wide-WorkBench.git
cd Genome-Wide-WorkBench

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python gww.py
📖 Usage

Launch the GUI:

python gww.py


Choose the desired module:

🔎 Mining Suite → Run BLAST/HMMER searches

🌳 Classification Suite → Align sequences & build phylogenies

🧬 Evolutionary Analysis → Perform Ka/Ks analysis

📊 Visualization Tab → Expression heatmaps & gene density maps

🧪 Primer Design Tab → Design primers with Primer3

Explore the examples/ folder for demo datasets.

🧪 Case Study

Applied GWW to 13 Vigna species to study NLRome evolution:

🌱 Identified 128–655 candidate NLR genes per species

🔬 Confirmed NB-ARC domain conservation

📉 Ka/Ks analysis showed purifying selection as the dominant evolutionary force

🌳 Phylogenetic reconstruction revealed lineage-specific expansions

👥 Authors

Noor ul Eman
University of Agriculture, Department of Computer Science – Bioinformatics

Evolutionary Biology Lab, UAF

🤝 Contributing

💡 Contributions, issues, and feature requests are welcome!
Please open an Issue
 or submit a Pull Request.

📜 License

This project is licensed under the MIT License – see the LICENSE
 file for details.

🔗 Citation

If you use Genome Wide WorkBench (GWW) in your research, please cite:

Noor ul Eman et al. (2025). Genome Wide WorkBench: Integrated Offline Platform for Multi-Omics Research.

✨ GWW provides a comprehensive, cost-free solution for reproducible, large-scale genomics research — anywhere, anytime.


