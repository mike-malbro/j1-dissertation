#!/usr/bin/env python3
"""
Module 01.01.01 - Data Center DX Cooled Model
Michael Logan Maloney PhD Dissertation Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Data Center DX Cooled Model with Google Drawing integration.
"""

import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

def generate_data_center_dx_cooled_model():
    """Generate Data Center DX Cooled Model page with integrated Google Drawing"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Path to downloaded asset
    asset_path = Path(__file__).parent / ".." / ".." / "downloads" / "01.02_asset.png"
    
    # Google Drawing link
    drawing_link = "https://docs.google.com/drawings/d/1P6be-G9qq5yPdPBGwFF-H38EXmlyKe2j0QvuKAm04kg/edit"
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title - Left justified with book-style spacing (like 01.00)
    title_text = "Data Center DX Cooled Model"
    ax.text(0.1, 9.9, title_text, fontsize=18, fontweight='bold', 
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # Subtitle
    subtitle_text = "mo_01_Data Center_DX cooled_without_ASE_1N_homogenous"
    ax.text(0.1, 9.5, subtitle_text, fontsize=14, fontweight='normal', 
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # Add the Google Drawing - prominently displayed with book-style spacing
    if asset_path.exists():
        try:
            img = Image.open(asset_path)
            
            # Calculate optimal size to fit page width with margins
            img_width = 6.5  # Slightly smaller for better spacing
            aspect_ratio = img.height / img.width
            img_height = img_width * aspect_ratio
            
            # Ensure image doesn't exceed available vertical space
            max_height = 4.5  # Reduced for better book spacing
            if img_height > max_height:
                img_height = max_height
                img_width = img_height / aspect_ratio
            
            # Center the image horizontally
            x_pos = (8.5 - img_width) / 2
            # Position image below title with book-style spacing (like 01.00)
            y_pos = 7.5 - img_height  # More space from title
            
            # Add image
            ax.imshow(img, extent=[x_pos, x_pos + img_width, y_pos, y_pos + img_height])
            
            # Figure number - clean and simple with book spacing
            ax.text(0.1, y_pos - 0.8, "Figure 5", fontsize=14, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial', color='black')
            
            # Small one-sentence description with book spacing
            ax.text(0.1, y_pos - 1.2, "Data center DX cooled model for 1N homogeneous system analysis.", 
                    fontsize=12, fontweight='normal', ha='left', va='center', 
                    fontfamily='Arial', color='black')
            
            # Google Drawing link - small and clean with book spacing
            ax.text(0.1, y_pos - 1.6, f"Source: {drawing_link}", fontsize=9, fontweight='normal',
                    ha='left', va='center', fontfamily='Arial', color='blue',
                    url=drawing_link, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
            
        except Exception as e:
            print(f"⚠️ Warning: Could not load image: {e}")
            # Add placeholder text with book spacing
            ax.text(0.1, 6, "Data Center DX Cooled Model Image", fontsize=14, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial', color='gray')
            ax.text(0.1, 5.5, "(Image will be integrated from Google Drawing)", fontsize=10,
                    ha='left', va='center', fontfamily='Arial', color='gray')
            ax.text(0.1, 5.2, f"Source: {drawing_link}", fontsize=9, fontweight='normal',
                    ha='left', va='center', fontfamily='Arial', color='blue',
                    url=drawing_link, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    else:
        # Add placeholder text with book spacing
        ax.text(0.1, 6, "Data Center DX Cooled Model Image", fontsize=14, fontweight='bold',
                ha='left', va='center', fontfamily='Arial', color='gray')
        ax.text(0.1, 5.5, "(Image will be integrated from Google Drawing)", fontsize=10,
                ha='left', va='center', fontfamily='Arial', color='gray')
        ax.text(0.1, 5.2, f"Source: {drawing_link}", fontsize=9, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='blue',
                url=drawing_link, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    # Model Description
    model_title = "Model Description:"
    ax.text(0.1, 4.5, model_title, fontsize=12, fontweight='bold',
            ha='left', va='center', fontfamily='Arial', color='black')
    
    model_desc = [
        "• DX (Direct Expansion) cooling system",
        "• 1N homogeneous configuration",
        "• Without ASE (Air Side Economizer)",
        "• Baseline cooling performance analysis",
        "• Energy efficiency evaluation"
    ]
    
    for i, desc in enumerate(model_desc):
        y_pos = 4.2 - (i * 0.25)
        ax.text(0.1, y_pos, desc, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='black')
    
    # Technical Specifications
    specs_title = "Technical Specifications:"
    ax.text(0.1, 2.8, specs_title, fontsize=12, fontweight='bold',
            ha='left', va='center', fontfamily='Arial', color='black')
    
    specs = [
        "• Cooling Type: Direct Expansion (DX)",
        "• Redundancy: 1N (No redundancy)",
        "• Economizer: Disabled",
        "• Configuration: Homogeneous",
        "• Analysis: Steady-state performance"
    ]
    
    for i, spec in enumerate(specs):
        y_pos = 2.5 - (i * 0.25)
        ax.text(0.1, y_pos, spec, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='black')
    
    # Page number - centered like 01.00
    ax.text(4.25, 0.5, "9", fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Timestamp - left justified like 01.00
    timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ax.text(0.1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Module identifier - left justified like 01.00
    module_text = "Module: 01.02 - Data Center DX Cooled Model"
    ax.text(0.1, 0.1, module_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Save as PDF
    output_file = output_dir / f"data_center_dx_cooled_01.02_{timestamp}.pdf"
    with PdfPages(output_file) as pdf:
        pdf.savefig(fig, dpi=300)
    
    plt.close()
    
    print(f"✅ Data Center DX Cooled Model generated: {output_file}")
    return str(output_file)

def main():
    """Main function to generate Data Center DX Cooled Model"""
    print("🎨 Generating Data Center DX Cooled Model...")
    
    try:
        output_file = generate_data_center_dx_cooled_model()
        print(f"📄 Data Center DX Cooled Model created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating Data Center DX Cooled Model: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
