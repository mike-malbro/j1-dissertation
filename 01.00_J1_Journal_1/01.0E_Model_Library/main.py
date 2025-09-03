#!/usr/bin/env python3
"""
Submodule 1.0E: Model Library - Professional Document
J1 - Conference Paper 1 SIMBUILD 2027

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Professional model library with Google Sheet data integration.
Downloads data from "model_library" sheet, processes into table, and displays in document.
"""

import sys
import io
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import requests
import warnings
warnings.filterwarnings('ignore')

def download_google_sheet_data():
    """Download data from Google Sheet 'model_library' tab"""
    
    # Google Spreadsheet URL
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1q_i0d0X4bdCIv_1Cr6pmbcj4iRqMcsYiPjCxK62E1cA/edit?gid=1907094472#gid=1907094472"
    
    # Extract the spreadsheet ID from the URL
    spreadsheet_id = "1q_i0d0X4bdCIv_1Cr6pmbcj4iRqMcsYiPjCxK62E1cA"
    
    # Convert to CSV download URL (this will get the "model_library" sheet)
    csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv&sheet=model_library"
    
    try:
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
        
        # Parse CSV into pandas DataFrame
        df = pd.read_csv(io.StringIO(csv_data))
        
        return df
        
    except Exception as e:
        print(f"❌ Error downloading spreadsheet data: {e}")
        return None

def process_model_library_data(df):
    """Process the model library data into a clean format"""
    
    if df is None or df.empty:
        return None
    
    try:
        # Clean column names (remove any whitespace and special characters)
        df.columns = df.columns.str.strip().str.replace('\n', ' ').str.replace('\r', ' ')
        
        # Remove any completely empty rows
        df = df.dropna(how='all')
        
        # Reset index after cleaning
        df = df.reset_index(drop=True)
        
        print(f"✅ Processed model library data: {len(df)} rows, {len(df.columns)} columns")
        print(f"📊 Columns: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error processing data: {e}")
        return None

def create_model_library_table(df):
    """Create an ultra-clean, professional LaTeX-style table from the real model_library data"""
    
    if df is None or df.empty:
        print("❌ No data to create table from")
        return None
    
    try:
        # Clean and prepare data for professional table display
        display_df = df.copy()
        
        # Clean column names for better display
        clean_columns = []
        for col in display_df.columns:
            # Clean column names - remove special characters and make readable
            clean_col = str(col).replace('_', ' ').title()
            clean_columns.append(clean_col)
        
        # Clean and format data values
        clean_data = []
        for _, row in display_df.iterrows():
            clean_row = []
            for value in row:
                if pd.isna(value):
                    clean_row.append('N/A')
                else:
                    # Clean the text and format for display
                    clean_value = str(value).strip()
                    # Truncate very long text but keep it readable
                    if len(clean_value) > 60:
                        clean_value = clean_value[:57] + '...'
                    clean_row.append(clean_value)
            clean_data.append(clean_row)
        
        # Create figure for the professional table
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.axis('tight')
        ax.axis('off')
        
        # Create table with professional styling
        table = ax.table(cellText=clean_data, colLabels=clean_columns, 
                        cellLoc='left', loc='center',
                        bbox=[0, 0, 1, 1])
        
        # Professional table styling
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        
        # Set professional column widths based on content
        num_cols = len(clean_columns)
        col_widths = [1.0 / num_cols] * num_cols  # Equal width columns
        
        for i, width in enumerate(col_widths):
            for j in range(len(clean_data) + 1):
                table[(j, i)].set_width(width)
        
        # Style header row - professional black text on light gray background
        for i in range(len(clean_columns)):
            table[(0, i)].set_facecolor('#f8f9fa')  # Light gray header
            table[(0, i)].set_text_props(weight='bold', color='black', 
                                        family='Arial', size=10)
            # Professional borders
            table[(0, i)].set_edgecolor('black')
            table[(0, i)].set_linewidth(1.0)
        
        # Style data rows - ultra-clean professional appearance
        for i in range(1, len(clean_data) + 1):
            for j in range(len(clean_columns)):
                # Ultra-clean black text
                table[(i, j)].set_text_props(weight='normal', color='black', 
                                            family='Arial', size=9)
                # Clean white background with subtle borders
                table[(i, j)].set_facecolor('white')
                table[(i, j)].set_edgecolor('#e0e0e0')  # Very light gray borders
                table[(i, j)].set_linewidth(0.5)
        
        # Professional table layout
        plt.tight_layout(pad=0.3)
        
        # Save as high-quality professional image
        table_path = Path(__file__).parent / "output" / "model_library_table.png"
        table_path.parent.mkdir(exist_ok=True)
        plt.savefig(table_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"✅ Created ultra-clean professional LaTeX-style table from real model_library data: {table_path}")
        return table_path
        
    except Exception as e:
        print(f"❌ Error creating professional table: {e}")
        return None

def generate_model_library_document():
    """Generate Model Library page with integrated Google Sheet data"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Download and process Google Sheet data from 'model_library' tab
    print(f"📥 Downloading fresh Model Library data from 'model_library' tab...")
    df = download_google_sheet_data()
    
    if df is not None:
        # Process the data
        processed_df = process_model_library_data(df)
        
        # Create table visualization from real data
        table_path = create_model_library_table(processed_df)
    else:
        processed_df = None
        table_path = None
    
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
    
    # Add the Model Library table - prominently displayed
    if table_path and table_path.exists():
        try:
            from PIL import Image
            img = Image.open(table_path)
            
            # Calculate optimal size to fit page width with margins
            img_width = 7.5  # Large to show table details
            aspect_ratio = img.height / img.width
            img_height = img_width * aspect_ratio
            
            # Ensure image doesn't exceed available vertical space
            max_height = 6.5  # Large to show table details
            if img_height > max_height:
                img_height = max_height
                img_width = img_height / aspect_ratio
            
            # Center the image horizontally
            x_pos = (8.5 - img_width) / 2
            # Position image below title with book-style spacing
            y_pos = 8 - img_height
            
            # Add image
            ax.imshow(img, extent=[x_pos, x_pos + img_width, y_pos, y_pos + img_height])
            
            # Figure number - clean and simple with book spacing
            ax.text(0.1, y_pos - 0.8, "Figure 4", fontsize=14, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial', color='black')
            
            # Small one-sentence description with book spacing
            ax.text(0.1, y_pos - 1.2, "Model library data from Google Sheet 'model_library'.", 
                    fontsize=12, fontweight='normal', ha='left', va='center', 
                    fontfamily='Arial', color='black')
            
            # Google Spreadsheet link - small and clean with book spacing
            ax.text(0.1, y_pos - 1.6, f"Source: {spreadsheet_link}", fontsize=9, fontweight='normal',
                    ha='left', va='center', fontfamily='Arial', color='blue',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
            
            print(f"✅ Fresh Model Library table loaded successfully")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not load table image: {e}")
            # Add placeholder text with book spacing
            ax.text(0.1, 6, "Model Library Table", fontsize=14, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial', color='gray')
            ax.text(0.1, 5.5, "(Table will be integrated from Google Sheet data)", fontsize=10,
                    ha='left', va='center', fontfamily='Arial', color='gray')
            ax.text(0.1, 5.2, f"Source: {spreadsheet_link}", fontsize=9, fontweight='normal',
                    ha='left', va='center', fontfamily='Arial', color='blue',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    else:
        # Add placeholder text with book spacing
        ax.text(0.1, 6, "Model Library Table", fontsize=14, fontweight='bold',
                ha='left', va='center', fontfamily='Arial', color='gray')
        ax.text(0.1, 5.5, "(Table will be integrated from Google Sheet data)", fontsize=10,
                ha='left', va='center', fontfamily='Arial', color='gray')
        ax.text(0.1, 5.2, f"Source: {spreadsheet_link}", fontsize=9, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='blue',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    # Add data summary if available
    if processed_df is not None:
        summary_text = f"Data Summary: {len(processed_df)} models, {len(processed_df.columns)} attributes"
        ax.text(0.1, 4.5, summary_text, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='black')
        
        # Show column names
        columns_text = f"Columns: {', '.join(processed_df.columns)}"
        ax.text(0.1, 4.2, columns_text, fontsize=9, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='gray')
    else:
        # Fallback if no data
        summary_text = "Data Summary: No data available"
        ax.text(0.1, 4.5, summary_text, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='red')
    
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
        output_file = generate_model_library_document()
        print(f"📄 Model Library page created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating Model Library page: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
