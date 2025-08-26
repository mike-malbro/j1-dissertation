#!/usr/bin/env python3
"""
Create Comprehensive PDF from All Module Outputs
J1 Advanced Engineering Notebook

Combines all latest PDF outputs into a single comprehensive study
"""

import os
import glob
from pathlib import Path
from datetime import datetime
import subprocess
import sys

def create_comprehensive_pdf():
    """Create comprehensive PDF from all latest module outputs"""
    
    base_dir = Path(__file__).parent
    output_dir = base_dir / "output"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Find all latest PDFs (from today's runs)
    pdf_files = []
    
    # Get all PDFs from today's runs
    today_pattern = f"*{datetime.now().strftime('%Y%m%d')}*.pdf"
    
    # Search in all module output directories
    for pdf_file in base_dir.rglob(today_pattern):
        if "output" in str(pdf_file):
            pdf_files.append(str(pdf_file))
    
    if not pdf_files:
        print("❌ No PDF files found from today's runs")
        return None
    
    # Sort by timestamp to get the latest versions
    pdf_files.sort()
    
    print(f"📄 Found {len(pdf_files)} PDF files to combine:")
    for pdf in pdf_files:
        print(f"   📄 {pdf}")
    
    # Create comprehensive PDF filename
            comprehensive_pdf = output_dir / f"j1_comprehensive_study_{timestamp}.pdf"
    
    try:
        # Use pdftk to combine PDFs (if available)
        cmd = ["pdftk"] + pdf_files + ["cat", "output", str(comprehensive_pdf)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Created comprehensive PDF: {comprehensive_pdf}")
            return str(comprehensive_pdf)
        else:
            print(f"❌ pdftk failed: {result.stderr}")
            return None
            
    except FileNotFoundError:
        print("❌ pdftk not found, trying alternative method...")
        
        # Alternative: use Python to create a simple combined PDF
        try:
            from PyPDF2 import PdfMerger
            
            merger = PdfMerger()
            
            for pdf_file in pdf_files:
                merger.append(pdf_file)
            
            merger.write(str(comprehensive_pdf))
            merger.close()
            
            print(f"✅ Created comprehensive PDF: {comprehensive_pdf}")
            return str(comprehensive_pdf)
            
        except ImportError:
            print("❌ PyPDF2 not available")
            return None

if __name__ == "__main__":
    pdf_path = create_comprehensive_pdf()
    if pdf_path:
        print(f"🎉 Comprehensive PDF created: {pdf_path}")
    else:
        print("❌ Failed to create comprehensive PDF")



