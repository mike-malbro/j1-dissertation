# J1 - Michael Maloney's First Journal Paper
## Advanced Data Center Thermodynamic Modeling Framework

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Research](https://img.shields.io/badge/Research-PhD%20Dissertation-orange.svg)](https://www.ae.psu.edu/)
[![Dynamic](https://img.shields.io/badge/Dynamic-Google%20Sheet%20Driven-brightgreen.svg)](https://github.com/mike-malbro/j1-dissertation)
[![Professional](https://img.shields.io/badge/Professional-LaTeX%20PDF%20Generation-red.svg)](https://www.latex-project.org/)

**Author:** Michael Maloney  
**Institution:** Penn State Architectural Engineering Department  
**Focus:** Mechanical System Engineering  
**Fellowship:** Penn State Fellowship Recipient  
**Target Audience:** Dr. Wangda Zuo, Michael Weter (LBNL National Labs)

---

## 🎯 Project Overview

This repository contains the foundation for **"The World's Latest and Greatest Data Center Thermodynamic Modeling Tool"** - a comprehensive PhD-level research framework focused on data center energy efficiency and Computer Room Air Conditioning (CRAC) system optimization.

### Research Goals
- Develop advanced thermodynamic modeling for heterogeneous CRAC systems
- Implement rule-based optimization with CRAC rotation strategies
- Achieve significant energy savings in data center operations
- Create a foundation for 4-year PhD research journey

### Current Results
- **15% energy savings** versus conventional control
- **Modelica-based optimization** methodology
- **Rule-based optimization** with CRAC rotation
- **Heterogeneous equipment** analysis (1 main + 4 supplemental CRAC units)
- **Professional PDF generation** with LaTeX formatting
- **Figure import boilerplate** for consistent research document layout

---

## 🏗️ Dynamic Modular Architecture

### **Core Philosophy: No Hardcoded Modules**
This system is designed to evolve over your 4-year PhD journey. **All modules are dynamically controlled** through configuration files and Google Sheets, allowing you to:

- **Add new research modules** without touching code
- **Enable/disable modules** based on research phases
- **Reorganize research structure** as your dissertation evolves
- **Collaborate with advisors** through shared Google Sheets
- **Scale research scope** as new ideas emerge

### **Configuration-Driven Design**
```
📁 Project Structure
├── 📄 module_inputs.json          # Dynamic module database
├── 📄 config.yaml                 # Research configuration
├── 🔗 Google Sheet Integration    # ACTIVE/INACTIVE control
├── 📁 00.00_Cover/               # Cover & TOC generation
├── 📁 01.00_J1_Journal_1/        # Main journal paper
├── 📁 0R.00_References/          # References & supporting materials
├── 📁 0Z.00_Google_Sheet_Helper_Functions/  # Data integration
└── 📁 modules/                   # Reusable code components
```

### **Module Categories**

#### **📋 Core Modules (Always Active)**
- **main.py** - Orchestrator that runs all active modules
- **module_inputs.json** - Internal database for module management
- **Google Sheet Integration** - External control system

#### **📄 Document Generation (00.xx)**
- **00.00** - Cover page generation (LaTeX professional formatting)
- **00.0A** - Cover generator with dynamic titles (currently inactive)
- **00.0B** - Table of Contents (auto-generated from active modules)

#### **📊 Research Modules (01.xx)**
- **01.00** - J1 Journal 1 (Main conference paper - LaTeX formatting)
- **01.0A** - Abstract with state-of-art analysis (LaTeX professional layout)
- **01.0B** - Graphical Abstract
- **01.0C** - Problem System Model (Figure import boilerplate)
- **01.0D** - Model Library Diagram (Google Drawing integration)
- **01.0E.1** - Scenario_1 analysis
- **01.01** - Simulation 1: Model_1_Scenario_1 (Baseline AI)
- **01.02** - Annual simulation analysis
- **01.03** - Typical Week analysis
- **01.04** - Critical Day analysis
- **01.05** - Results Summary

#### **📚 Reference Modules (0R.xx)**
- **0R.00** - References module
- **0R.0A** - Abbreviations
- **0R.01** - J1 References
- **0R.0Z** - General References
- **0R.0F** - Figures
- **0R.0C** - Calculations

#### **🔗 Integration Modules (0Z.xx)**
- **0Z.00** - Google Sheet Helper Functions
- **0Z.0A** - Read GSheet & Update Internal DB
- **0Z.0B** - Write to Google Sheets
- **0Z.0X** - Miscellaneous Google Sheet scripts

#### **🏢 Reference Data Centers (02.xx)**
- **02.01** - Reference Data Center Room Alerify
- **02.01.01-08** - Detailed analysis submodules
- **02.0Z** - DX Economizer Sample

---

## 🚀 How It Works

### **1. Dynamic Module Loading**
```python
# System automatically loads active modules from:
# 1. module_inputs.json (local database)
# 2. Google Sheet (external control)
# 3. Only executes modules marked as ACTIVE
```

### **2. Google Sheet Integration**
- **Read Operations (0Z.0A)**: Downloads module status from Google Sheet
- **Write Operations (0Z.0B)**: Updates Google Sheet with results
- **Asset Downloads**: Automatically downloads Google Drawings/Docs as needed

### **3. Module Execution Flow**
```
1. Load module_inputs.json
2. Check Google Sheet for ACTIVE/INACTIVE status
3. Execute only active modules
4. Generate PDFs for each module
5. Compile comprehensive dissertation PDF
6. Update Google Sheet with results
```

---

## 🔧 Configuration Management

### **Adding New Modules**
1. **Update module_inputs.json**:
   ```json
   {
     "NEW_MODULE_ID": {
       "id": "NEW_MODULE_ID",
       "name": "New Research Module",
       "type": "Submodule",
       "active": true,
       "description": "Description of new research component"
     }
   }
   ```

2. **Create module directory** with `main.py`

3. **System automatically picks it up** - no code changes needed!

### **Enabling/Disabling Modules**
- **Local Control**: Edit `module_inputs.json` directly
- **Google Sheet Control**: Update ACTIVE/INACTIVE column
- **Dynamic**: Changes take effect immediately

### **Research Evolution Support**
- **Phase 1**: Focus on core modules (01.00-01.05)
- **Phase 2**: Add reference data centers (02.xx)
- **Phase 3**: Expand with new research areas
- **Phase 4**: Dissertation compilation and defense

---

## 📊 Research Components

### Data Center Specifications
- **Facility:** Harrisburg Data Center (2N · 1 MW)
- **Location:** Harrisburg, Pennsylvania
- **Layout:** 4 rows, 44 servers
- **CRAC System:** 1 main unit + 4 supplemental split air conditioners

### Key Research Areas
- **Abstract Generation:** J1 Concept Development with professional LaTeX formatting
- **Performance Analysis:** CRAC efficiency curves and optimization
- **Scenario Modeling:** Multiple operating condition analysis
- **Figure Generation:** Professional visualization tools with boilerplate templates
- **Data Integration:** Google Sheets connectivity
- **Asset Management:** Automatic Google Drive integration

---

## 🔬 Research Methodology

### Modelica-Based Optimization
- Advanced thermodynamic modeling
- Rule-based CRAC rotation strategies
- Heterogeneous equipment analysis
- Energy efficiency optimization

### Current Innovations
- Multi-CRAC system optimization
- Performance curve analysis
- Reliability and redundancy assessment
- Real-time control strategies

---

## 📈 Output and Results

The framework generates:
- **Professional PDF reports** with comprehensive analysis
- **Performance curves** and efficiency metrics
- **Scenario analysis** for different operating conditions
- **Visual abstracts** for conference presentations
- **Data integration** with Google Sheets for collaboration
- **Automatic asset downloads** from Google Drive
- **Professional LaTeX formatting** for all documents
- **Figure import boilerplate** for consistent research layout

---

## 🎨 Professional Document Generation

### **LaTeX Integration**
- **Professional formatting** for all research documents
- **Consistent typography** and layout across modules
- **Automatic text wrapping** and spacing
- **Professional margins** and page layout

### **Figure Import Boilerplate (01.0C)**
The Problem System Model module serves as a **reusable boilerplate** for figure imports:

**Features:**
- **Image-first layout** with prominent figure display
- **Professional spacing** with book-style margins
- **Text wrapping** to prevent cutoff issues
- **Source attribution** with Google Drawing links
- **Consistent formatting** across all figure modules
- **No overlapping text** or layout issues

**Layout Structure:**
1. **Title** (left-justified, professional positioning)
2. **Image** (centered, maximum width, proper aspect ratio)
3. **Figure Number** (clean, bold formatting)
4. **Description** (one-sentence, secondary importance)
5. **Source Link** (small blue text, Google Drawing attribution)
6. **Page Elements** (timestamp, module ID, page number)

### **Text Handling Improvements**
- **01.0A Style Integration**: Professional text wrapping and spacing
- **No Text Cutoff**: Proper line breaks and positioning
- **Consistent Margins**: Matches 01.00 module positioning
- **Professional Appearance**: Clean, organized research document layout

---

## 🤝 Collaboration & Evolution

### **4-Year PhD Journey Support**
This system is designed to grow with your research:

- **Year 1**: Foundation modules, literature review
- **Year 2**: Core research, data collection
- **Year 3**: Advanced analysis, paper writing
- **Year 4**: Dissertation compilation, defense preparation

### **Advisor Collaboration**
- **Dr. Wangda Zuo** - Primary advisor access through Google Sheets
- **Michael Weter** - LBNL National Labs collaboration
- **Real-time updates** - Advisors can see progress instantly
- **Flexible structure** - Easy to add new research directions

### **Research Timeline**
- **Stage:** Advanced Research - Building Foundation
- **Goal:** 4-Year PhD Journey Foundation
- **Target:** World-class data center modeling tool
- **Evolution:** Dynamic system that adapts to research needs

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Required packages (see `requirements.txt`)
- Google Sheets API credentials
- LaTeX installation (for professional PDF generation)

### Installation
```bash
# Clone the repository
git clone https://github.com/mike-malbro/j1-dissertation.git
cd j1-dissertation

# Install dependencies
pip install -r requirements.txt

# Configure Google Sheets integration
# (See DEVELOPMENT.md for detailed setup)

# Run the main orchestrator
python main.py
```

### **Dynamic Configuration**
1. **Edit module_inputs.json** to add/remove modules
2. **Update Google Sheet** for ACTIVE/INACTIVE control
3. **Run main.py** - system automatically adapts
4. **No code changes needed** for new research modules!

### **Figure Module Template**
To create new figure modules using the boilerplate:
1. **Copy 01.0C_Problem_System_Model** directory
2. **Update module_inputs.json** with new module ID
3. **Replace image path** and description text
4. **Run main.py** - professional figure layout automatically applied

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Penn State Fellowship** for financial support
- **Dr. Wangda Zuo** for academic guidance
- **LBNL National Labs** for research collaboration
- **Penn State Architectural Engineering Department** for resources

---

## 📞 Contact

**Michael Maloney**  
PhD Student - Penn State Architectural Engineering Department  
Email: [your-email@psu.edu]  
Research Focus: Data Center Thermodynamic Modeling

---

## 🔄 Evolution Ready

*This repository represents a **living research framework** designed to evolve over your 4-year PhD journey. The dynamic, modular architecture ensures that as your research grows and changes, the system adapts with you - no hardcoded limitations, no rigid structure, just pure research flexibility.*

*Ready for whatever you throw at it over the next 4 years! 🚀*
