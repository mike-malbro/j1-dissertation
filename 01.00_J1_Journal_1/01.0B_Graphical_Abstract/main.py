#!/usr/bin/env python3
"""
Submodule 1.0B: Graphical Abstract - Professional Document
J1 - Conference Paper 1 SIMBUILD 2027

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Professional graphical abstract with Google Drawing integration.
"""

import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

# Add Google Drive helpers to path
sys.path.append(str(Path(__file__).parent / ".." / ".." / "0Z.00_Google_Sheet_Helper_Functions"))
from google_drive_helpers import download_asset

def generate_graphical_abstract_document():
    """Generate professional graphical abstract with Google Drawing integration"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Google Drawing link
    drawing_link = "https://docs.google.com/drawings/d/1-E-Lo4s4F6iZ2LfmdsQgRWTP4AhyuyQTUKa7lW4ucHM/edit"
    
    # Download fresh Google Drawing asset
    print(f"📥 Downloading fresh Graphical Abstract from Google Drive...")
    asset_path = download_asset(
        url=drawing_link,
        module_id="01.0B",
        filename="01.0B_asset.png"
    )
    
    if not asset_path or not asset_path.exists():
        print(f"❌ Failed to download fresh asset for 01.0B")
        # Fallback to existing asset if download fails
        asset_path = Path(__file__).parent / ".." / ".." / "downloads" / "01.0B_asset.png"
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title - Left justified with book-style spacing (like 01.00)
    title_text = "Graphical Abstract"
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
            ax.text(0.1, y_pos - 0.8, "Figure 2", fontsize=14, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial', color='black')
            
            # Small one-sentence description with book spacing
            ax.text(0.1, y_pos - 1.2, "Graphical abstract for heterogeneous data center cooling system analysis.", 
                    fontsize=12, fontweight='normal', ha='left', va='center', 
                    fontfamily='Arial', color='black')
            
            # Google Drawing link - small and clean with book spacing
            ax.text(0.1, y_pos - 1.6, f"Source: {drawing_link}", fontsize=9, fontweight='normal',
                    ha='left', va='center', fontfamily='Arial', color='blue',
                    url=drawing_link, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
            
            print(f"✅ Fresh Graphical Abstract loaded successfully")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not load image: {e}")
            # Add placeholder text with book spacing
            ax.text(0.1, 6, "Graphical Abstract Image", fontsize=14, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial', color='gray')
            ax.text(0.1, 5.5, "(Image will be integrated from Google Drawing)", fontsize=10,
                    ha='left', va='center', fontfamily='Arial', color='gray')
            ax.text(0.1, 5.2, f"Source: {drawing_link}", fontsize=9, fontweight='normal',
                    ha='left', va='center', fontfamily='Arial', color='blue',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    else:
        # Add placeholder text with book spacing
        ax.text(0.1, 6, "Graphical Abstract Image", fontsize=14, fontweight='bold',
                ha='left', va='center', fontfamily='Arial', color='gray')
        ax.text(0.1, 5.5, "(Image will be integrated from Google Drawing)", fontsize=10,
                ha='left', va='center', fontfamily='Arial', color='gray')
        ax.text(0.1, 5.2, f"Source: {drawing_link}", fontsize=9, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='blue',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    # Page number - centered like 01.00
    ax.text(4.25, 0.5, "6", fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Timestamp - left justified like 01.00
    timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ax.text(0.1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Module identifier - left justified like 01.00
    module_text = "Module: 01.0B - Graphical Abstract"
    ax.text(0.1, 0.1, module_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Save as PDF
    output_file = output_dir / f"graphical_abstract_01.0B_{timestamp}.pdf"
    with PdfPages(output_file) as pdf:
        pdf.savefig(fig, dpi=300)
    
    plt.close()
    
    print(f"✅ Graphical Abstract generated: {output_file}")
    return str(output_file)

def main():
    """Main function to generate Graphical Abstract"""
    print("🎨 Generating Graphical Abstract...")
    
    try:
        output_file = generate_graphical_abstract_document()
        print(f"📄 Graphical Abstract created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating Graphical Abstract: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 