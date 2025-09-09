#!/usr/bin/env python3
"""
Module 01.0E - Model Library
Michael Logan Maloney PhD Dissertation Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Model Library module with Google Spreadsheet integration.
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
warnings.filterwarnings('ignore')

def download_model_library_csv():
    """Download model_library tab as CSV - RELIABLE METHOD"""
    
    # Google Spreadsheet URL
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1q_i0d0X4bdCIv_1Cr6pmbcj4iRqMcsYiPjCxK62E1cA/edit?gid=1907094472#gid=1907094472"
    
    # Extract the spreadsheet ID from the URL
    spreadsheet_id = "1q_i0d0X4bdCIv_1Cr6pmbcj4iRqMcsYiPjCxK62E1cA"
    
    # CSV URL for model_library tab
    csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv&sheet=model_library"
    
    try:
        print(f"📥 Downloading model_library tab as CSV...")
        # Download the CSV data
        response = requests.get(csv_url, timeout=30)
        response.raise_for_status()
        
        # Parse CSV data
        csv_data = response.text
        
        # Save raw CSV to downloads directory for reference
        downloads_dir = Path(__file__).parent / ".." / ".." / "downloads"
        downloads_dir.mkdir(exist_ok=True)
        
        csv_path = downloads_dir / "01.0E_model_library.csv"
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(csv_data)
        
        print(f"✅ Downloaded model_library CSV: {csv_path}")
        
        # Parse the CSV data
        df = pd.read_csv(io.StringIO(csv_data))
        
        # Clean up the data
        df = df.dropna(how='all')  # Remove completely empty rows
        df = df.fillna('')  # Replace NaN with empty string
        
        print(f"✅ Model library data: {len(df)} rows, {len(df.columns)} columns")
        print(f"📊 Columns: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error downloading model_library CSV: {e}")
        return None

def create_model_library_table_image(df):
    """Create a clean table image from the model library data"""
    
    try:
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.axis('tight')
        ax.axis('off')
        
        # Create table data
        table_data = []
        # Add header
        table_data.append(['ID', 'Index', 'Prefix', 'Description'])
        
        # Add data rows
        for _, row in df.iterrows():
            table_data.append([
                row['ID'],
                row['Index'], 
                row['Prefix'],
                row['Desc']
            ])
        
        # Create table
        table = ax.table(cellText=table_data, 
                        cellLoc='left',
                        loc='center',
                        colWidths=[0.5, 0.1, 0.1, 0.3])
        
        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 2.5)
        
        # Style header row
        for i in range(4):
            table[(0, i)].set_facecolor('#f0f0f0')
            table[(0, i)].set_text_props(weight='bold')
        
        # Save as image
        downloads_dir = Path(__file__).parent / ".." / ".." / "downloads"
        downloads_dir.mkdir(exist_ok=True)
        
        jpg_path = downloads_dir / "01.0E_model_library.jpg"
        plt.savefig(jpg_path, dpi=150, bbox_inches='tight', format='jpg')
        plt.close()
        
        print(f"✅ Created model library table image: {jpg_path}")
        return jpg_path
        
    except Exception as e:
        print(f"❌ Error creating table image: {e}")
        return None

def generate_model_library_page():
    """Generate Model Library page with integrated model_library tab data"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Download model_library tab as CSV and create table image
    df = download_model_library_csv()
    if df is not None:
        jpg_path = create_model_library_table_image(df)
    else:
        jpg_path = None
    
    # Google Spreadsheet link
    spreadsheet_link = "https://docs.google.com/spreadsheets/d/1q_i0d0X4bdCIv_1Cr6pmbcj4iRqMcsYiPjCxK62E1cA/edit?gid=1907094472#gid=1907094472"
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title - Left justified with book-style spacing
    title_text = "Model Library"
    ax.text(0.1, 9.9, title_text, fontsize=18, fontweight='bold', 
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # Add the Model Library image - prominently displayed with book-style spacing
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
            ax.text(0.1, y_pos - 0.5, "Table 1", fontsize=14, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial', color='black')
            
            # Small one-sentence description with reduced spacing
            ax.text(0.1, y_pos - 0.8, "Model library data from Google Sheet 'model_library'.", 
                    fontsize=12, fontweight='normal', ha='left', va='center', 
                    fontfamily='Arial', color='black')
            
            # Google Spreadsheet link - small and clean with reduced spacing
            ax.text(0.1, y_pos - 1.1, f"Source: {spreadsheet_link}", fontsize=9, fontweight='normal',
                    ha='left', va='center', fontfamily='Arial', color='blue',
                    url=spreadsheet_link, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
            
        except Exception as e:
            print(f"⚠️ Warning: Could not load model library image: {e}")
            # Add placeholder text with book spacing
            ax.text(0.1, 6, "Model Library Spreadsheet", fontsize=14, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial', color='gray')
            ax.text(0.1, 5.5, "(Model Library will be integrated from Google Spreadsheet)", fontsize=10,
                    ha='left', va='center', fontfamily='Arial', color='gray')
            ax.text(0.1, 5.2, f"Source: {spreadsheet_link}", fontsize=9, fontweight='normal',
                    ha='left', va='center', fontfamily='Arial', color='blue',
                    url=spreadsheet_link, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    else:
        # Add placeholder text with book spacing
        ax.text(0.1, 6, "Model Library Spreadsheet", fontsize=14, fontweight='bold',
                ha='left', va='center', fontfamily='Arial', color='gray')
        ax.text(0.1, 5.5, "(Model Library will be integrated from Google Spreadsheet)", fontsize=10,
                ha='left', va='center', fontfamily='Arial', color='gray')
        ax.text(0.1, 5.2, f"Source: {spreadsheet_link}", fontsize=9, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='blue',
                url=spreadsheet_link, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    # Page number - centered
    ax.text(4.25, 0.8, "8", fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Timestamp - left justified
    timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ax.text(0.1, 0.6, timestamp_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Module identifier - left justified
    module_text = "Module: 01.0E - Model Library"
    ax.text(0.1, 0.4, module_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Save as PDF
    output_file = output_dir / f"model_library_01.0E_{timestamp}.pdf"
    with PdfPages(output_file) as pdf:
        pdf.savefig(fig, dpi=300)
    
    plt.close()
    
    print(f"✅ Model Library page generated: {output_file}")
    return str(output_file)

def main():
    """Main function to generate Model Library page"""
    print("📚 Generating Model Library page...")
    
    try:
        output_file = generate_model_library_page()
        print(f"📄 Model Library page created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating Model Library page: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
