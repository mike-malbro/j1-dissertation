#!/usr/bin/env python3
"""
Submodule 1.3: Supplemental System Substate Graph - Professional Document
CRCS[n] - Conference Paper 1 SIMBUILD 2027

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Professional supplemental system substate graph document.
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def generate_supplemental_substate_document():
    """Generate professional supplemental system substate graph document"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate PDF
    pdf_path = output_dir / f"supplemental_substate_1.3_{timestamp}.pdf"
    
    with PdfPages(pdf_path) as pdf:
        # Create figure with proper margins
        fig = plt.figure(figsize=(8.5, 11))  # Letter size
        plt.axis('off')
        
        # Set font to Arial
        plt.rcParams['font.family'] = 'Arial'
        plt.rcParams['font.sans-serif'] = ['Arial']
        
        # Define proper spacing constants
        TOP_MARGIN = 0.95
        LINE_HEIGHT = 0.05
        SECTION_SPACING = 0.08
        
        # Title - properly positioned
        plt.text(0.5, TOP_MARGIN, 'SUPPLEMENTAL SYSTEM SUBSTATE GRAPH', 
                fontsize=24, weight='bold', ha='center', va='center',
                color='black', fontfamily='Arial', transform=plt.gca().transAxes)
        
        # Conference info - properly positioned
        y_pos = TOP_MARGIN - LINE_HEIGHT
        plt.text(0.5, y_pos, 'SIMBUILD 2027 Conference Paper', 
                fontsize=16, ha='center', va='center',
                color='black', fontfamily='Arial', transform=plt.gca().transAxes)
        
        # Paper title - properly positioned with spacing
        y_pos -= LINE_HEIGHT
        plt.text(0.5, y_pos, 'Multi-System Modeling of Data Center Cooling:', 
                fontsize=18, weight='bold', ha='center', va='center',
                color='black', fontfamily='Arial', transform=plt.gca().transAxes)
        
        y_pos -= LINE_HEIGHT
        plt.text(0.5, y_pos, 'Optimizing Control of Five CRAC Units for Energy Efficiency and Runtime in Harrisburg', 
                fontsize=18, weight='bold', ha='center', va='center',
                color='black', fontfamily='Arial', transform=plt.gca().transAxes)
        
        # Author info - properly positioned
        y_pos -= SECTION_SPACING
        plt.text(0.5, y_pos, 'Author: Michael Maloney', 
                fontsize=14, weight='bold', ha='center', va='center',
                color='black', fontfamily='Arial', transform=plt.gca().transAxes)
        
        y_pos -= LINE_HEIGHT
        plt.text(0.5, y_pos, 'PhD Student - Penn State Architectural Engineering Department', 
                fontsize=12, ha='center', va='center',
                color='black', fontfamily='Arial', transform=plt.gca().transAxes)
        
        y_pos -= LINE_HEIGHT
        plt.text(0.5, y_pos, 'Mechanical System Focus', 
                fontsize=12, ha='center', va='center',
                color='black', fontfamily='Arial', transform=plt.gca().transAxes)
        
        # Supplemental Substate section - properly positioned
        y_pos -= SECTION_SPACING
        plt.text(0.5, y_pos, 'Supplemental System Substate Graph:', 
                fontsize=16, weight='bold', ha='center', va='center',
                color='black', fontfamily='Arial', transform=plt.gca().transAxes)
        
        # Analysis description - properly positioned
        y_pos -= LINE_HEIGHT
        description = """This analysis examines the substate behavior of the four supplemental CRAC units in the Harrisburg Data Center. The substate graph illustrates how individual supplemental units transition between operational modes, coordination patterns, and load distribution strategies to optimize overall system performance."""
        
        # Split description into lines for proper formatting
        words = description.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line + " " + word) <= 60:
                current_line += " " + word if current_line else word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        for line in lines:
            plt.text(0.5, y_pos, line, 
                    fontsize=12, ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            y_pos -= LINE_HEIGHT
        
        # Key details section - properly positioned
        y_pos -= SECTION_SPACING
        plt.text(0.5, y_pos, 'Key Details:', 
                fontsize=14, weight='bold', ha='center', va='center',
                color='black', fontfamily='Arial', transform=plt.gca().transAxes)
        
        key_details = [
            "• Data Center: 2N · 1 MW facility in Harrisburg, Pennsylvania",
            "• CRAC Configuration: 1 primary + 4 supplemental split air conditioners",
            "• Methodology: Modelica-based optimization",
            "• Innovation: Rule-based optimization with CRAC rotation",
            "• Energy Savings: 15% versus conventional control",
            "• Target: Heterogeneous equipment and systems in data centers"
        ]
        
        y_pos -= LINE_HEIGHT
        for detail in key_details:
            plt.text(0.5, y_pos, detail, 
                    fontsize=11, ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            y_pos -= LINE_HEIGHT
        
        # Timestamp - properly positioned at bottom
        plt.text(0.5, 0.05, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 
                fontsize=10, ha='center', va='center',
                color='black', fontfamily='Arial', transform=plt.gca().transAxes)
        
        pdf.savefig(fig, facecolor='white', bbox_inches='tight')
        plt.close(fig)
    
    print(f"✅ Generated supplemental substate document: {pdf_path}")
    return str(pdf_path)

if __name__ == "__main__":
    generate_supplemental_substate_document()
