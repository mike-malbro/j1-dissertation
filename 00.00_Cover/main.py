#!/usr/bin/env python3
"""
Module 00.00 - Cover Page Generation
Michael Logan Maloney PhD Dissertation Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Professional cover page generation.
"""

import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import warnings
warnings.filterwarnings('ignore')

def generate_cover_page():
    """Generate a professional cover page for the dissertation notebook"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.axis('off')
    
    # MAIN TITLE - Centered, large font, bold
    title_text = "PhD Dissertation Notebook"
    ax.text(0.5, 0.86, title_text, fontsize=24, fontweight='bold', 
            ha='center', va='center', fontfamily='Arial', color='black', transform=ax.transAxes)
    
    # SUBTITLE - Centered, medium font
    subtitle_text = "Advanced Data Center Thermodynamic Modeling Framework"
    ax.text(0.5, 0.8, subtitle_text, fontsize=16, fontweight='normal', 
            ha='center', va='center', fontfamily='Arial', color='black', transform=ax.transAxes)
    
    # RESEARCH FOCUS - Centered, medium font
    focus_text = "J1 - An Optimal Load Allocation for Multi CRAC System for Harrisburg DC"
    ax.text(0.5, 0.75, focus_text, fontsize=14, fontweight='normal', 
            ha='center', va='center', fontfamily='Arial', color='black', transform=ax.transAxes)
    
    # AUTHOR INFORMATION - Centered, medium font
    author_info = [
        "Michael Logan Maloney",
        "PhD Student",
        "Pennsylvania State University",
        "Architectural Engineering Department",
        "Mechanical System Focus",
        "Sustainable Buildings and Society Library (SBS Lab)"
    ]
    
    # Position author info with center alignment
    for i, info in enumerate(author_info):
        y_pos = 0.59 - (i * 0.036)
        ax.text(0.5, y_pos, info, fontsize=14, fontweight='normal', 
                ha='center', va='center', fontfamily='Arial', color='black', transform=ax.transAxes)
    
    # ADVISOR INFORMATION - Centered, medium font
    advisor_text = "Advisor: Dr. Wangda Zuo"
    ax.text(0.5, 0.35, advisor_text, fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black', transform=ax.transAxes)
    
    # REPORT GENERATION DATE - Centered, medium font
    date_text = f"Report Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    ax.text(0.5, 0.29, date_text, fontsize=12, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black', transform=ax.transAxes)
    
    # RESEARCH STATUS - Centered, medium font
    status_text = "Status: ADVANCED RESEARCH MODE ACTIVATED"
    ax.text(0.5, 0.24, status_text, fontsize=12, fontweight='bold',
            ha='center', va='center', fontfamily='Arial', color='darkblue', transform=ax.transAxes)
    
    # Page number
    ax.text(0.5, 0.05, "1", fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black', transform=ax.transAxes)
    
    # Timestamp
    timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ax.text(0.06, 0.03, timestamp_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray', transform=ax.transAxes)
    
    # Module identifier
    module_text = "Module: 00.00 - Cover"
    ax.text(0.06, 0.01, module_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray', transform=ax.transAxes)
    
    # Save as PDF
    output_file = output_dir / f"cover_page_{timestamp}.pdf"
    with PdfPages(output_file) as pdf:
        pdf.savefig(fig, dpi=300)
    
    plt.close()
    
    print(f"✅ Cover page generated: {output_file}")
    return str(output_file)

def main():
    """Main function to generate cover page"""
    print("🎨 Generating Main Cover Page...")
    
    try:
        output_file = generate_cover_page()
        print(f"📄 Main cover page created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating cover page: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 