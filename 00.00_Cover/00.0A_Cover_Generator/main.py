#!/usr/bin/env python3
"""
Cover Generator - 00.0A
Michael Logan Maloney PhD Dissertation Notebook
Cover page generator with customizable title and date
"""

import os
import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def generate_cover_page():
    """Generate a professional cover page for the dissertation notebook"""
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create figure with professional styling - NO BORDER
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # MAIN TITLE - Left aligned, Arial font
    title_text = "Report"
    ax.text(1, 9.5, title_text, fontsize=16, fontweight='normal', 
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # AUTHOR INFORMATION - Left aligned, Arial font
    author_info = [
        "Author: Michael Logan Maloney",
        "Position: PhD Student",
        "Institution: Pennsylvania State University",
        "Department: Architectural Engineering",
        "Laboratory: Sustainable Buildings and Societies Laboratory (SBS Lab)",
        "Advisor: Dr. Wangda Zuo"
    ]
    
    # Position author info with left alignment
    for i, info in enumerate(author_info):
        y_pos = 8.5 - (i * 0.4)
        ax.text(1, y_pos, info, fontsize=14, fontweight='normal', 
                ha='left', va='center', fontfamily='Arial', color='black')
    
    # REPORT GENERATION DATE - Left aligned, Arial font
    date_text = f"Report Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    ax.text(1, 5.5, date_text, fontsize=14, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # Page number
    ax.text(4.25, 0.5, "1", fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Timestamp
    timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ax.text(1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Module identifier
    module_text = "Module: 00.0A - Cover Generator"
    ax.text(1, 0.1, module_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Save as PDF
    output_file = output_dir / f"cover_page_00.0A_{timestamp}.pdf"
    with PdfPages(output_file) as pdf:
        pdf.savefig(fig, dpi=300)
    
    plt.close()
    
    print(f"✅ Cover page generated: {output_file}")
    return str(output_file)

def main():
    """Main function to generate cover page"""
    print("🎨 Generating Cover Page...")
    
    try:
        output_file = generate_cover_page()
        print(f"📄 Cover page created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating cover page: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
