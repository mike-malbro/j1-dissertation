#!/usr/bin/env python3
"""
Module: 01.02.01 - Model
Description: Model - Download Link: https://docs.google.com/drawings/d/1Gnj8q1U-MqWTPZfZLIMfJChh5iMW2DC3f9drRm8MhNU/edit. Insert png into pdf as Figure.
Author: Michael Logan Maloney
Timestamp: 2025-08-29
"""

import os
import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

def generate_model_figure():
    """
    Generate the Model figure page using the same boilerplate as other figure modules.
    """
    print("📊 Generating Model page...")
    
    # Create PDF page with the model image
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.pyplot as plt
    from PIL import Image
    
    # Create figure with 8.5 x 11 inch page
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Add title
    title_text = "Model"
    ax.text(0.5, 10.5, title_text, fontsize=16, fontweight='bold', 
            ha='center', va='center')
    
    # Load and display the model image
    try:
        # Try to load from downloads directory
        img_path = Path(__file__).parent / ".." / ".." / "downloads" / "01.02.01_asset.png"
        
        if not img_path.exists():
            print(f"⚠️ Model image not found at {img_path}, creating placeholder")
            # Create a placeholder image
            placeholder_img = Image.new('RGB', (800, 600), color='lightgray')
            placeholder_img.save(img_path)
        
        img = Image.open(img_path)
        
        # Calculate optimal size to fit page width with margins
        img_width = 7.5  # Large but with margins for centering
        aspect_ratio = img.height / img.width
        img_height = img_width * aspect_ratio
        
        # Ensure image doesn't exceed available vertical space
        max_height = 6.5  # Large but with margins for centering
        if img_height > max_height:
            img_height = max_height
            img_width = img_height / aspect_ratio
        
        # Center the image horizontally and vertically
        x_pos = (8.5 - img_width) / 2  # Center horizontally
        y_pos = (11 - img_height) / 2  # Center vertically
        
        # Add image
        ax.imshow(img, extent=[x_pos, x_pos + img_width, y_pos, y_pos + img_height])
        
        # Add figure number and description
        figure_text = "Figure 1.2.01"
        ax.text(x_pos, y_pos - 0.5, figure_text, fontsize=12, fontweight='bold')
        
        description_text = "Simulation 2 Model - Performance Curve/Staging Analysis."
        ax.text(x_pos, y_pos - 0.8, description_text, fontsize=10, wrap=True)
        
        # Add source information with clickable link
        source_text = "Source: https://docs.google.com/drawings/d/1Gnj8q1U-MqWTPZfZLIMfJChh5iMW2DC3f9drRm8MhNU/edit"
        ax.text(x_pos, y_pos - 1.1, source_text, fontsize=9, style='italic',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7))
        
    except Exception as e:
        print(f"❌ Error loading model image: {e}")
        # Fallback text
        ax.text(4.25, 5.5, "Model Figure\n(Image loading failed)", 
                fontsize=14, ha='center', va='center', 
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    # Add page number and module info
    ax.text(4.25, 0.5, "13", fontsize=10, ha='center', va='center')
    ax.text(0.5, 0.5, "Module: 01.02.01 - Model | Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            fontsize=8, ha='left', va='center')
    
    # Save PDF
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"output/model_01.02.01_{timestamp}.pdf"
    
    with PdfPages(pdf_filename) as pdf:
        pdf.savefig(fig, bbox_inches='tight')
    
    plt.close()
    
    print(f"✅ Model page generated: {pdf_filename}")
    return pdf_filename

if __name__ == "__main__":
    try:
        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)
        
        # Generate the Model figure
        pdf_path = generate_model_figure()
        
        print(f"📄 Model module completed successfully: {pdf_path}")
        
    except Exception as e:
        print(f"❌ Error in Model module: {e}")
        sys.exit(1)
