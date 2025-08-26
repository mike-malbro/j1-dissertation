#!/usr/bin/env python3
"""
Module 01.01 - Simulation 1: Model_1_Scenario_1
Michael Logan Maloney PhD Dissertation Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Baseline AI - No Performance Curve. Data: Energy, Power, Room Temperature, 
Supply and Return Water Temperature, PUE.
"""

import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def generate_simulation_overview():
    """Generate Simulation 1 overview page"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title
    title_text = "Simulation 1: Model_1_Scenario_1"
    ax.text(4.25, 10, title_text, fontsize=18, fontweight='bold', 
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Subtitle
    subtitle_text = "Baseline AI - No Performance Curve"
    ax.text(4.25, 9.3, subtitle_text, fontsize=14, fontweight='normal', 
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Description
    description = [
        "This simulation module analyzes the baseline performance of the",
        "heterogeneous data center cooling system without performance curves.",
        "",
        "Key Parameters:",
        "• Energy consumption analysis",
        "• Power demand patterns",
        "• Room temperature profiles",
        "• Supply and return water temperatures",
        "• Power Usage Effectiveness (PUE)",
        "",
        "Submodules:",
        "• 01.02: Annual simulation analysis",
        "• 01.03: Typical week analysis", 
        "• 01.04: Critical day analysis",
        "• 01.05: Results summary"
    ]
    
    # Position description
    for i, line in enumerate(description):
        y_pos = 8.5 - (i * 0.35)
        ax.text(4.25, y_pos, line, fontsize=11, fontweight='normal', 
                ha='center', va='center', fontfamily='Arial', color='black')
    
    # Data Center Specifications
    specs_title = "Harrisburg Data Center Specifications:"
    ax.text(1, 3.5, specs_title, fontsize=12, fontweight='bold',
            ha='left', va='center', fontfamily='Arial', color='black')
    
    specs = [
        "• Facility: Harrisburg Data Center (2N · 1 MW)",
        "• Location: Harrisburg, Pennsylvania",
        "• Layout: 4 rows, 44 servers",
        "• CRAC System: 1 main unit + 4 supplemental split air conditioners",
        "• White Space: 34' × 44' × 7'"
    ]
    
    for i, spec in enumerate(specs):
        y_pos = 3.2 - (i * 0.3)
        ax.text(1, y_pos, spec, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='black')
    
    # Page number
    ax.text(4.25, 0.5, "1", fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Timestamp
    timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ax.text(1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Module identifier
    module_text = "Module: 01.01 - Simulation 1: Model_1_Scenario_1"
    ax.text(1, 0.1, module_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Save as PDF
    output_file = output_dir / f"simulation_1_overview_01.01_{timestamp}.pdf"
    with PdfPages(output_file) as pdf:
        pdf.savefig(fig, dpi=300, bbox_inches='tight')
    
    plt.close()
    
    print(f"✅ Simulation 1 overview generated: {output_file}")
    return str(output_file)

def main():
    """Main function to generate Simulation 1 overview"""
    print("🎨 Generating Simulation 1 Overview...")
    
    try:
        output_file = generate_simulation_overview()
        print(f"📄 Simulation 1 overview created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating Simulation 1 overview: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
