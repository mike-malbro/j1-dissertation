#!/usr/bin/env python3
"""
Module 01.0D - Model Library Diagram
Michael Logan Maloney PhD Dissertation Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Model Library Diagram with Google Drawing integration.
"""

import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

def generate_model_library_diagram():
    """Generate Model Library Diagram page with integrated Google Drawing"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Path to downloaded asset
    asset_path = Path(__file__).parent / ".." / ".." / "downloads" / "01.0D_asset.png"
    
    # Google Drawing link
    drawing_link = "https://docs.google.com/drawings/d/1la5TOLOvfLjC9-IUAdIHMXR63o-SdUFJeVahzvAO0Fk/edit"
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title - Left justified with book-style spacing (like 01.00)
    title_text = "Model Library Diagram"
    ax.text(0.1, 9.9, title_text, fontsize=18, fontweight='bold', 
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
            max_height = 5.5  # Reduced for better book spacing
            if img_height > max_height:
                img_height = max_height
                img_width = img_height / aspect_ratio
            
            # Center the image horizontally
            x_pos = (8.5 - img_width) / 2
            # Position image below title with book-style spacing (like 01.00)
            y_pos = 8 - img_height  # More space from title
            
            # Add image
            ax.imshow(img, extent=[x_pos, x_pos + img_width, y_pos, y_pos + img_height])
            
            # Figure number - clean and simple with book spacing
            ax.text(0.1, y_pos - 0.8, "Figure 3", fontsize=14, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial', color='black')
            
            # Small one-sentence description with book spacing
            ax.text(0.1, y_pos - 1.2, "Model library diagram for data center thermodynamic modeling framework.", 
                    fontsize=12, fontweight='normal', ha='left', va='center', 
                    fontfamily='Arial', color='black')
            
            # Google Drawing link - small and clean with book spacing
            ax.text(0.1, y_pos - 1.6, f"Source: {drawing_link}", fontsize=9, fontweight='normal',
                    ha='left', va='center', fontfamily='Arial', color='blue',
                    url=drawing_link, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
            
        except Exception as e:
            print(f"⚠️ Warning: Could not load image: {e}")
            # Add placeholder text with book spacing
            ax.text(0.1, 6, "Model Library Diagram Image", fontsize=14, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial', color='gray')
            ax.text(0.1, 5.5, "(Image will be integrated from Google Drawing)", fontsize=10,
                    ha='left', va='center', fontfamily='Arial', color='gray')
            ax.text(0.1, 5.2, f"Source: {drawing_link}", fontsize=9, fontweight='normal',
                    ha='left', va='center', fontfamily='Arial', color='blue',
                    url=drawing_link, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    else:
        # Add placeholder text with book spacing
        ax.text(0.1, 6, "Model Library Diagram Image", fontsize=14, fontweight='bold',
                ha='left', va='center', fontfamily='Arial', color='gray')
        ax.text(0.1, 5.5, "(Image will be integrated from Google Drawing)", fontsize=10,
                ha='left', va='center', fontfamily='Arial', color='gray')
        ax.text(0.1, 5.2, f"Source: {drawing_link}", fontsize=9, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='blue',
                url=drawing_link, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    # Page number - centered like 01.00
    ax.text(4.25, 0.5, "7", fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Timestamp - left justified like 01.00
    timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ax.text(0.1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Module identifier - left justified like 01.00
    module_text = "Module: 01.0D - Model Library Diagram"
    ax.text(0.1, 0.1, module_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Save as PDF
    output_file = output_dir / f"model_library_diagram_01.0D_{timestamp}.pdf"
    with PdfPages(output_file) as pdf:
        pdf.savefig(fig, dpi=300)
    
    plt.close()
    
    print(f"✅ Model Library Diagram generated: {output_file}")
    return str(output_file)

def main():
    """Main function to generate Model Library Diagram"""
    print("🎨 Generating Model Library Diagram...")
    
    try:
        output_file = generate_model_library_diagram()
        print(f"📄 Model Library Diagram created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating Model Library Diagram: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
