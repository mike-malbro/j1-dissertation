#!/usr/bin/env python3
"""
Module 01.05 - Results Summary
Michael Logan Maloney PhD Dissertation Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Results summary for Simulation 1 baseline AI scenario.
"""

import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def generate_results_summary():
    """Generate Results Summary for Simulation 1"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title
    title_text = "Simulation 1 Results Summary"
    ax.text(4.25, 10, title_text, fontsize=18, fontweight='bold', 
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Subtitle
    subtitle_text = "Baseline AI - No Performance Curve"
    ax.text(4.25, 9.3, subtitle_text, fontsize=14, fontweight='normal', 
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Description
    description = [
        "Comprehensive summary of Simulation 1 results for the",
        "heterogeneous data center cooling system analysis.",
        "",
        "Key Findings:",
        "• Annual energy consumption patterns",
        "• Weekly operational efficiency",
        "• Critical day performance",
        "• System optimization opportunities",
        "• Cost-benefit analysis",
        "• Recommendations for improvement"
    ]
    
    # Position description
    for i, line in enumerate(description):
        y_pos = 8.5 - (i * 0.35)
        ax.text(4.25, y_pos, line, fontsize=11, fontweight='normal', 
                ha='center', va='center', fontfamily='Arial', color='black')
    
    # Summary sections
    sections = [
        "Summary Sections:",
        "• Executive Summary",
        "• Key Performance Indicators",
        "• Energy Efficiency Analysis",
        "• Cost Analysis",
        "• Optimization Recommendations",
        "• Future Research Directions"
    ]
    
    for i, line in enumerate(sections):
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
    module_text = "Module: 01.05 - Results Summary"
    ax.text(1, 0.1, module_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Save as PDF
    output_file = output_dir / f"results_summary_01.05_{timestamp}.pdf"
    with PdfPages(output_file) as pdf:
        pdf.savefig(fig, dpi=300, bbox_inches='tight')
    
    plt.close()
    
    print(f"✅ Results summary generated: {output_file}")
    return str(output_file)

def main():
    """Main function to generate Results Summary"""
    print("📊 Generating Results Summary...")
    
    try:
        output_file = generate_results_summary()
        print(f"📄 Results summary created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating Results summary: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
