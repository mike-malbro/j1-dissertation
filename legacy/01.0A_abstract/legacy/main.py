#!/usr/bin/env python3
"""
Submodule 1.0A: Abstract
J1 - Conference Paper 1 SIMBUILD 2027

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

This module generates the abstract for the SIMBUILD 2027 conference paper.
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from pathlib import Path
import warnings
import sys
warnings.filterwarnings('ignore')

# Add the parent directory to the path to find modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from modules.j1_plotting import J1AnalysisBase
except ImportError:
    # Fallback if modules not available
    class J1AnalysisBase:
        def __init__(self):
            self.colors = {
                'primary': '#1f77b4',
                'secondary': '#ff7f0e',
                'accent': '#2ca02c',
                'text': '#333333'
            }
            self.style = 'default'

class AbstractGenerator(CRCSAnalysisBase):
    """
    Abstract Generator for SIMBUILD 2027 Conference Paper.
    Uses the CRCSAnalysisBase for all plotting, style, and color configuration.
    """
    def __init__(self):
        super().__init__()
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.abstract_text = """Effective data center cooling requires precise control of Computer Room Air Conditioning (CRAC) units to balance energy efficiency and equipment runtime. This paper employs Modelica to optimize a multi-CRAC system—one primary unit and four supplemental split air conditioners—for a 2N · 1 MW data center modeled after a reference facility located in Harrisburg, Pennsylvania. Current Models consider single type CRAC systems which may limit potential performance and reliability optimization of data centers. The Modelica model will contain a rule based optimization based on optimal performance for each CRAC Main and 4 Supplemental Units with rotation. Current Steady State Results indicate (15%) energy savings potential versus conventional control. This work can enhance future building performance research on heterogeneous equipment and systems in data centers."""
        self.paper_details = {
            "title": "Multi-System Modeling of Data Center Cooling: Optimizing Control of Five CRAC Units for Energy Efficiency and Runtime in Harrisburg",
            "conference": "SIMBUILD 2027",
            "author": "Michael Maloney",
            "affiliation": "Penn State Architectural Engineering Department",
            "focus": "Mechanical System Focus",
            "data_center": "Harrisburg Data Center, Pennsylvania",
            "system_type": "2N · 1 MW data center",
            "crac_configuration": "1 primary + 4 supplemental split air conditioners",
            "methodology": "Modelica-based optimization",
            "energy_savings": "15% versus conventional control",
            "key_innovation": "Rule-based optimization with CRAC rotation"
        }
    
    def generate_abstract_page(self) -> str:
        """Generate abstract page"""
        print("Generating abstract page...")
        
        # Generate PDF report
        pdf_path = self.output_dir / f"abstract_1.0A_{self.timestamp}.pdf"
        
        with PdfPages(pdf_path) as pdf:
            # Abstract page
            fig = plt.figure(figsize=(12, 16))
            plt.axis('off')
            
            # Title
            plt.text(0.5, 0.95, 'ABSTRACT', 
                    fontsize=20, weight='bold', ha='center', va='center',
                    color=self.colors['primary'])
            
            # Conference info
            plt.text(0.5, 0.9, f'{self.paper_details["conference"]} Conference Paper', 
                    fontsize=14, ha='center', va='center',
                    color=self.colors['secondary'])
            
            # Paper title
            plt.text(0.5, 0.85, self.paper_details["title"], 
                    fontsize=12, weight='bold', ha='center', va='center',
                    color=self.colors['primary'])
            
            # Author info
            plt.text(0.5, 0.8, f'{self.paper_details["author"]}', 
                    fontsize=12, ha='center', va='center',
                    color=self.colors['primary'])
            plt.text(0.5, 0.76, f'{self.paper_details["affiliation"]}', 
                    fontsize=11, ha='center', va='center',
                    color=self.colors['primary'])
            plt.text(0.5, 0.72, f'{self.paper_details["focus"]}', 
                    fontsize=11, ha='center', va='center',
                    color=self.colors['primary'])
            
            # Abstract text
            plt.text(0.5, 0.65, 'Abstract:', 
                    fontsize=14, weight='bold', ha='center', va='center',
                    color=self.colors['primary'])
            
            # Format abstract text for better readability
            abstract_lines = self.abstract_text.split('. ')
            formatted_abstract = '.\n\n'.join(abstract_lines)
            
            plt.text(0.1, 0.55, formatted_abstract, 
                    fontsize=11, ha='left', va='top',
                    color=self.colors['primary'], wrap=True,
                    transform=plt.gca().transAxes)
            
            # Key details
            plt.text(0.1, 0.25, 'Key Details:', 
                    fontsize=14, weight='bold', ha='left', va='top',
                    color=self.colors['primary'], transform=plt.gca().transAxes)
            
            details_text = (
                f"• Data Center: {self.paper_details['data_center']}\n"
                f"• System Type: {self.paper_details['system_type']}\n"
                f"• CRAC Configuration: {self.paper_details['crac_configuration']}\n"
                f"• Methodology: {self.paper_details['methodology']}\n"
                f"• Energy Savings: {self.paper_details['energy_savings']}\n"
                f"• Key Innovation: {self.paper_details['key_innovation']}"
            )
            
            plt.text(0.1, 0.15, details_text, 
                    fontsize=10, ha='left', va='top',
                    color=self.colors['secondary'], fontfamily='monospace',
                    transform=plt.gca().transAxes)
            
            # Generation timestamp
            plt.text(0.5, 0.05, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 
                    fontsize=10, ha='center', va='center',
                    color=self.colors['info'])
            
            pdf.savefig(fig)
            plt.close(fig)
        
        print(f"   Saved: {pdf_path}")
        return str(pdf_path) 