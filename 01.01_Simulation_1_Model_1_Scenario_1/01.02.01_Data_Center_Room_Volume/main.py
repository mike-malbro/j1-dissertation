#!/usr/bin/env python3
"""
Module 01.02.01 - J1 Data Center Room Volume
Michael Logan Maloney PhD Dissertation Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Professional figure module with Google Drawing integration.
"""

import sys
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

def create_data_center_room_volume_figure():
    """Create professional figure with Google Drawing integration"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Google Drawing asset path
    asset_path = Path(__file__).parent / ".." / ".." / "downloads" / "01.02.01_asset.png"
    
    # Create professional 8.5 x 11 figure
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title - Left justified with book-style spacing (like 01.00)
    title_text = "J1 Data Center Room Volume"
    ax.text(0.1, 9.9, title_text, fontsize=18, fontweight='bold', 
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # Subtitle
    subtitle_text = "Data Center Room Volume Analysis"
    ax.text(0.1, 9.5, subtitle_text, fontsize=14, fontweight='normal', 
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # Figure number and description
    figure_text = "Figure 1.2.01: Data Center Room Volume"
    ax.text(0.1, 8.5, figure_text, fontsize=12, fontweight='bold', 
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # Description
    description_text = "Data center room volume analysis for Harrisburg facility."
    ax.text(0.1, 8.2, description_text, fontsize=10, fontweight='normal', 
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # Load and display image
    if asset_path.exists():
        try:
            img = Image.open(asset_path)
            
            # Calculate image dimensions to fit on page
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height
            
            # Maximum dimensions on page (with margins)
            max_width = 7.5  # 8.5 - 1 inch margins
            max_height = 6.0  # Leave space for text
            
            # Calculate display dimensions
            if aspect_ratio > (max_width / max_height):
                # Image is wider than tall relative to available space
                display_width = max_width
                display_height = max_width / aspect_ratio
            else:
                # Image is taller than wide relative to available space
                display_height = max_height
                display_width = max_height * aspect_ratio
            
            # Calculate position (center horizontally, below text)
            x_pos = (8.5 - display_width) / 2
            y_pos = 1.5  # Position above bottom margin
            
            # Display image
            ax.imshow(img, extent=[x_pos, x_pos + display_width, y_pos, y_pos + display_height])
            
        except Exception as e:
            print(f"⚠️ Error loading image: {e}")
            # Fallback text if image fails to load
            ax.text(4.25, 4, "Image not available", fontsize=14, ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    else:
        print(f"⚠️ Image not found: {asset_path}")
        # Fallback text if image doesn't exist
        ax.text(4.25, 4, "Image not found", fontsize=14, ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    # Google Drawing link (clickable hyperlink)
    link_text = "Source: Google Drawing"
    link_url = "https://docs.google.com/drawings/d/1ZgghbDOSyghwulohx7NoQ19p9pPdS2nZlsCwmFUxMHA/edit"
    ax.text(0.1, 0.8, link_text, fontsize=10, ha='left', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.8),
            url=link_url)
    
    # Page number
    ax.text(7.5, 0.5, "Page 9", fontsize=10, ha='right', va='center', 
            fontfamily='Arial', color='black')
    
    # Timestamp
    timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ax.text(0.1, 0.5, timestamp_text, fontsize=8, ha='left', va='center', 
            fontfamily='Arial', color='gray')
    
    # Module identifier
    ax.text(4.25, 0.5, "Module: 01.02.01", fontsize=8, ha='center', va='center', 
            fontfamily='Arial', color='gray')
    
    # Save PDF
    pdf_path = output_dir / f"data_center_room_volume_01.02.01_{timestamp}.pdf"
    plt.savefig(pdf_path, dpi=300, bbox_inches='tight', format='pdf')
    plt.close()
    
    print(f"✅ J1 Data Center Room Volume figure created: {pdf_path}")
    return pdf_path

def main():
    """Main execution function"""
    print("🎨 Generating J1 Data Center Room Volume Figure (01.02.01)...")
    
    try:
        pdf_path = create_data_center_room_volume_figure()
        print(f"📄 J1 Data Center Room Volume created successfully: {pdf_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating J1 Data Center Room Volume: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
