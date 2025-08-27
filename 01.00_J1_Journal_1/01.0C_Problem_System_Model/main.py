#!/usr/bin/env python3
"""
Module 01.0C - Problem System Model
Michael Logan Maloney PhD Dissertation Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Problem System Model with Google Drawing integration.
"""

import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

def generate_problem_system_model():
    """Generate Problem System Model page with integrated Google Drawing"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Path to downloaded asset
    asset_path = Path(__file__).parent / ".." / ".." / "downloads" / "problem_system_model.png"
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title
    title_text = "Problem System Model"
    ax.text(4.25, 10, title_text, fontsize=18, fontweight='bold', 
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Description
    description = [
        "This figure illustrates the problem system model for the",
        "heterogeneous data center cooling system analysis.",
        "",
        "The model shows the relationship between:",
        "• Main CRAC unit and supplemental units",
        "• Temperature and humidity control zones",
        "• Energy flow and optimization opportunities"
    ]
    
    # Position description
    for i, line in enumerate(description):
        y_pos = 8.5 - (i * 0.4)
        ax.text(4.25, y_pos, line, fontsize=12, fontweight='normal', 
                ha='center', va='center', fontfamily='Arial', color='black')
    
    # Add the Google Drawing if available
    if asset_path.exists():
        try:
            img = Image.open(asset_path)
            # Calculate position and size for the image
            img_width = 6.0
            img_height = 4.0
            x_pos = (8.5 - img_width) / 2
            y_pos = 3.5
            
            # Add image
            ax.imshow(img, extent=[x_pos, x_pos + img_width, y_pos, y_pos + img_height])
            
            # Add caption
            ax.text(4.25, 2.5, "Figure 1: Problem System Model", fontsize=12, fontweight='bold',
                    ha='center', va='center', fontfamily='Arial', color='black')
            
        except Exception as e:
            print(f"⚠️ Warning: Could not load image: {e}")
            # Add placeholder text
            ax.text(4.25, 4, "Problem System Model Image", fontsize=14, fontweight='bold',
                    ha='center', va='center', fontfamily='Arial', color='gray')
            ax.text(4.25, 3.5, "(Image will be integrated from Google Drawing)", fontsize=10,
                    ha='center', va='center', fontfamily='Arial', color='gray')
    else:
        # Add placeholder text
        ax.text(4.25, 4, "Problem System Model Image", fontsize=14, fontweight='bold',
                ha='center', va='center', fontfamily='Arial', color='gray')
        ax.text(4.25, 3.5, "(Image will be integrated from Google Drawing)", fontsize=10,
                ha='center', va='center', fontfamily='Arial', color='gray')
    
    # Page number
    ax.text(4.25, 0.5, "1", fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Timestamp
    timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ax.text(1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Module identifier
    module_text = "Module: 01.0C - Problem System Model"
    ax.text(1, 0.1, module_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Save as PDF
    output_file = output_dir / f"problem_system_model_01.0C_{timestamp}.pdf"
    with PdfPages(output_file) as pdf:
        pdf.savefig(fig, dpi=300)
    
    plt.close()
    
    print(f"✅ Problem System Model generated: {output_file}")
    return str(output_file)

def main():
    """Main function to generate Problem System Model"""
    print("🎨 Generating Problem System Model...")
    
    try:
        output_file = generate_problem_system_model()
        print(f"📄 Problem System Model created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating Problem System Model: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
