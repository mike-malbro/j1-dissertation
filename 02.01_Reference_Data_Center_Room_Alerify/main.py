#!/usr/bin/env python3
"""
Module 02.01 - Reference Data Center Room Alerify
Michael Logan Maloney PhD Dissertation Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Reference data center room analysis.
"""

import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def generate_reference_data_center():
    """Generate Reference Data Center analysis"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title
    title_text = "Reference Data Center Room Alerify"
    ax.text(4.25, 10, title_text, fontsize=18, fontweight='bold', 
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Description
    description = [
        "Reference data center room analysis for comparison and",
        "validation of the Harrisburg Data Center study.",
        "",
        "Analysis Components:",
        "• Room layout and specifications",
        "• Equipment configuration",
        "• Performance characteristics",
        "• Energy efficiency metrics",
        "• Control system analysis",
        "• Optimization results"
    ]
    
    # Position description
    for i, line in enumerate(description):
        y_pos = 8.5 - (i * 0.4)
        ax.text(4.25, y_pos, line, fontsize=11, fontweight='normal', 
                ha='center', va='center', fontfamily='Arial', color='black')
    
    # Submodules
    submodules = [
        "Submodules:",
        "• 02.01.01: Summary",
        "• 02.01.02: Equipment Analysis",
        "• 02.01.03: Performance Data",
        "• 02.01.04: Energy Analysis",
        "• 02.01.05: Thermal Analysis",
        "• 02.01.06: Control Analysis",
        "• 02.01.07: Optimization Results",
        "• 02.01.08: Conclusions"
    ]
    
    for i, line in enumerate(submodules):
        y_pos = 4.5 - (i * 0.3)
        ax.text(4.25, y_pos, line, fontsize=10, fontweight='normal',
                ha='center', va='center', fontfamily='Arial', color='gray')
    
    # Page number
    ax.text(4.25, 0.5, "1", fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Timestamp
    timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ax.text(1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Module identifier
    module_text = "Module: 02.01 - Reference Data Center Room Alerify"
    ax.text(1, 0.1, module_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Save as PDF
    output_file = output_dir / f"reference_data_center_02.01_{timestamp}.pdf"
    with PdfPages(output_file) as pdf:
        pdf.savefig(fig, dpi=300, bbox_inches='tight')
    
    plt.close()
    
    print(f"✅ Reference data center generated: {output_file}")
    return str(output_file)

def main():
    """Main function to generate Reference Data Center"""
    print("🏢 Generating Reference Data Center Analysis...")
    
    try:
        output_file = generate_reference_data_center()
        print(f"📄 Reference data center created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating Reference data center: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
