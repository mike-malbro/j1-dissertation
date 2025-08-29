#!/usr/bin/env python3
"""
Module 00.0S - Schedule
Michael Logan Maloney PhD Dissertation Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Schedule module with Google Spreadsheet integration.
Downloads spreadsheet, converts to PDF, then to JPG, and inserts into document.
"""

import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
import warnings
import requests
import pandas as pd
import io
import base64
from pdf2image import convert_from_path
warnings.filterwarnings('ignore')

def download_google_spreadsheet_as_pdf():
    """Download Google Spreadsheet as PDF"""
    
    # Google Spreadsheet URL
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1IGyQ-Jq-aq6kek80Q1rGnb0eoOUqBPVSolDzVZdJI-s/edit?usp=sharing"
    
    # Extract the spreadsheet ID from the URL
    spreadsheet_id = "1IGyQ-Jq-aq6kek80Q1rGnb0eoOUqBPVSolDzVZdJI-s"
    
    # Convert to PDF download URL
    pdf_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=pdf"
    
    try:
        # Download the PDF
        response = requests.get(pdf_url)
        response.raise_for_status()
        
        # Save PDF to downloads directory
        downloads_dir = Path(__file__).parent / ".." / "downloads"
        downloads_dir.mkdir(exist_ok=True)
        
        pdf_path = downloads_dir / "00.0S_schedule.pdf"
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Downloaded schedule PDF: {pdf_path}")
        return pdf_path
        
    except Exception as e:
        print(f"❌ Error downloading spreadsheet as PDF: {e}")
        return None

def convert_pdf_to_jpg(pdf_path):
    """Convert PDF to JPG image"""
    
    try:
        # Convert PDF to images using pdf2image
        images = convert_from_path(pdf_path, dpi=150)
        
        if images:
            # Take the first page
            image = images[0]
            
            # Save as JPG
            jpg_path = pdf_path.parent / "00.0S_schedule.jpg"
            image.save(jpg_path, 'JPEG', quality=95)
            
            print(f"✅ Converted PDF to JPG: {jpg_path}")
            return jpg_path
        else:
            print("❌ No pages found in PDF")
            return None
        
    except Exception as e:
        print(f"❌ Error converting PDF to JPG: {e}")
        # Fallback to placeholder image
        try:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, 'Schedule Spreadsheet\n(PDF Conversion Failed)', 
                    ha='center', va='center', fontsize=16, transform=ax.transAxes)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            # Save as JPG
            jpg_path = pdf_path.parent / "00.0S_schedule.jpg"
            plt.savefig(jpg_path, dpi=150, bbox_inches='tight', format='jpg')
            plt.close()
            
            print(f"⚠️ Created fallback JPG: {jpg_path}")
            return jpg_path
            
        except Exception as fallback_error:
            print(f"❌ Error creating fallback image: {fallback_error}")
            return None

def generate_schedule_page():
    """Generate Schedule page with integrated Google Spreadsheet"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Download spreadsheet as PDF and convert to JPG
    pdf_path = download_google_spreadsheet_as_pdf()
    if pdf_path:
        jpg_path = convert_pdf_to_jpg(pdf_path)
    else:
        jpg_path = None
    
    # Google Spreadsheet link
    spreadsheet_link = "https://docs.google.com/spreadsheets/d/1IGyQ-Jq-aq6kek80Q1rGnb0eoOUqBPVSolDzVZdJI-s/edit?usp=sharing"
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title - Left justified with book-style spacing
    title_text = "Schedule"
    ax.text(0.1, 9.9, title_text, fontsize=18, fontweight='bold', 
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # Add the Schedule image - prominently displayed with book-style spacing
    if jpg_path and jpg_path.exists():
        try:
            img = Image.open(jpg_path)
            
            # Calculate optimal size to fit page width with margins
            img_width = 8.0  # Much larger to fill page width
            aspect_ratio = img.height / img.width
            img_height = img_width * aspect_ratio
            
            # Ensure image doesn't exceed available vertical space
            max_height = 7.0  # Much larger to fill page height
            if img_height > max_height:
                img_height = max_height
                img_width = img_height / aspect_ratio
            
            # Position image to fill most of the page
            x_pos = 0.25  # Small left margin
            # Position image closer to title to reduce whitespace
            y_pos = 2.0  # Fixed position near bottom
            
            # Add image
            ax.imshow(img, extent=[x_pos, x_pos + img_width, y_pos, y_pos + img_height])
            
            # Figure number - clean and simple with reduced spacing
            ax.text(0.1, y_pos - 0.5, "Schedule", fontsize=14, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial', color='black')
            
            # Small one-sentence description with reduced spacing
            ax.text(0.1, y_pos - 0.8, "Project schedule and timeline overview.", 
                    fontsize=12, fontweight='normal', ha='left', va='center', 
                    fontfamily='Arial', color='black')
            
            # Google Spreadsheet link - small and clean with reduced spacing
            ax.text(0.1, y_pos - 1.1, f"Source: {spreadsheet_link}", fontsize=9, fontweight='normal',
                    ha='left', va='center', fontfamily='Arial', color='blue',
                    url=spreadsheet_link, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
            
        except Exception as e:
            print(f"⚠️ Warning: Could not load schedule image: {e}")
            # Add placeholder text with book spacing
            ax.text(0.1, 6, "Schedule Spreadsheet", fontsize=14, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial', color='gray')
            ax.text(0.1, 5.5, "(Schedule will be integrated from Google Spreadsheet)", fontsize=10,
                    ha='left', va='center', fontfamily='Arial', color='gray')
            ax.text(0.1, 5.2, f"Source: {spreadsheet_link}", fontsize=9, fontweight='normal',
                    ha='left', va='center', fontfamily='Arial', color='blue',
                    url=spreadsheet_link, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    else:
        # Add placeholder text with book spacing
        ax.text(0.1, 6, "Schedule Spreadsheet", fontsize=14, fontweight='bold',
                ha='left', va='center', fontfamily='Arial', color='gray')
        ax.text(0.1, 5.5, "(Schedule will be integrated from Google Spreadsheet)", fontsize=10,
                ha='left', va='center', fontfamily='Arial', color='gray')
        ax.text(0.1, 5.2, f"Source: {spreadsheet_link}", fontsize=9, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='blue',
                url=spreadsheet_link, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    # Page number - centered
    ax.text(4.25, 0.5, "3", fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Timestamp - left justified
    timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ax.text(0.1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Module identifier - left justified
    module_text = "Module: 00.0S - Schedule"
    ax.text(0.1, 0.1, module_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Save as PDF
    output_file = output_dir / f"schedule_00.0S_{timestamp}.pdf"
    with PdfPages(output_file) as pdf:
        pdf.savefig(fig, dpi=300)
    
    plt.close()
    
    print(f"✅ Schedule page generated: {output_file}")
    return str(output_file)

def main():
    """Main function to generate Schedule page"""
    print("📅 Generating Schedule page...")
    
    try:
        output_file = generate_schedule_page()
        print(f"📄 Schedule page created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating Schedule page: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
