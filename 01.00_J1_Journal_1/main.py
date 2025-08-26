#!/usr/bin/env python3
"""
Module 01.00 - J1 Journal 1 Cover Page
Michael Logan Maloney PhD Dissertation Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

J1 - The first Journal Paper. This will be the most important.
As much of the future work will look at this as a base.
"""

import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import warnings
warnings.filterwarnings('ignore')

def generate_j1_cover_page():
    """Generate a professional J1 cover page matching the main cover format"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create figure with professional styling - NO BORDER
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # MAIN TITLE - Left aligned, smaller font, unbold
    title_text = "J1 - Journal 1"
    ax.text(1, 9, title_text, fontsize=14, fontweight='normal', 
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # SUBTITLE - Left aligned, smaller font, unbold
    subtitle_text = "Multi-System Modeling of Data Center Cooling"
    ax.text(1, 8.5, subtitle_text, fontsize=14, fontweight='normal', 
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # AUTHOR INFORMATION - Left aligned, smaller font, unbold
    author_info = [
        "Author: Michael Maloney",
        "Institution: Pennsylvania State University",
        "Department: Architectural Engineering"
    ]
    
    # Position author info with left alignment
    for i, info in enumerate(author_info):
        y_pos = 7.5 - (i * 0.5)
        ax.text(1, y_pos, info, fontsize=14, fontweight='normal', 
                ha='left', va='center', fontfamily='Arial', color='black')
    
    # PAPER DESCRIPTION - Left aligned, smaller font, unbold
    description_text = "The first Journal Paper. This will be the most important."
    ax.text(1, 6, description_text, fontsize=14, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='black')
    
    description_text2 = "As much of the future work will look at this as a base."
    ax.text(1, 5.5, description_text2, fontsize=14, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # REPORT GENERATION DATE - Left aligned, smaller font, unbold
    date_text = f"Report Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    ax.text(1, 4.5, date_text, fontsize=14, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # Page number
    ax.text(4.25, 0.5, "3", fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Timestamp
    timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ax.text(1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Module identifier
    module_text = "Module: 01.00 - J1 Journal 1"
    ax.text(1, 0.1, module_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Save as PDF
    output_file = output_dir / f"journal_1_01.00_{timestamp}.pdf"
    with PdfPages(output_file) as pdf:
        pdf.savefig(fig, dpi=300, bbox_inches='tight')
    
    plt.close()
    
    print(f"✅ J1 cover page generated: {output_file}")
    return str(output_file)

def main():
    """Main function to generate J1 cover page"""
    print("🎨 Generating J1 Journal 1 Cover Page...")
    
    try:
        output_file = generate_j1_cover_page()
        print(f"📄 J1 cover page created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating J1 cover page: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
