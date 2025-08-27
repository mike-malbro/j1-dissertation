#!/usr/bin/env python3
"""
0Z.0A - Read Google Sheets and Download Google Drive Assets
Enhanced read operations with Google Drive download capabilities
"""

import os
import re
import requests
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Optional, Tuple
import gspread
from google.oauth2.service_account import Credentials

class GoogleDriveDownloader:
    """Download Google Drive assets (Drawings, Docs, Sheets) as images"""
    
    def __init__(self, credentials_path: str = "credentials/google_sheets_credentials.json"):
        self.credentials_path = Path(credentials_path)
        self.download_dir = Path("downloads")
        self.download_dir.mkdir(exist_ok=True)
        
    def extract_drive_id(self, url: str) -> Optional[str]:
        """Extract Google Drive ID from various URL formats"""
        patterns = [
            r'/d/([a-zA-Z0-9-_]+)',  # Standard Drive URL
            r'/drawings/d/([a-zA-Z0-9-_]+)',  # Google Drawings
            r'/document/d/([a-zA-Z0-9-_]+)',  # Google Docs
            r'/spreadsheets/d/([a-zA-Z0-9-_]+)',  # Google Sheets
            r'/presentation/d/([a-zA-Z0-9-_]+)',  # Google Slides
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def download_google_drawing(self, url: str, filename: str = None) -> Optional[Path]:
        """Download Google Drawing as PNG"""
        drive_id = self.extract_drive_id(url)
        if not drive_id:
            print(f"❌ Could not extract Drive ID from: {url}")
            return None
            
        # Google Drawing export URL
        export_url = f"https://docs.google.com/drawings/d/{drive_id}/export/png"
        
        try:
            response = requests.get(export_url, timeout=30)
            response.raise_for_status()
            
            if not filename:
                filename = f"drawing_{drive_id}.png"
            
            file_path = self.download_dir / filename
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Downloaded: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"❌ Failed to download {url}: {e}")
            return None
    
    def download_google_doc_as_pdf(self, url: str, filename: str = None) -> Optional[Path]:
        """Download Google Doc as PDF"""
        drive_id = self.extract_drive_id(url)
        if not drive_id:
            return None
            
        export_url = f"https://docs.google.com/document/d/{drive_id}/export?format=pdf"
        
        try:
            response = requests.get(export_url, timeout=30)
            response.raise_for_status()
            
            if not filename:
                filename = f"doc_{drive_id}.pdf"
            
            file_path = self.download_dir / filename
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Downloaded: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"❌ Failed to download {url}: {e}")
            return None

class GoogleSheetReader:
    """Read Google Sheets and extract module data with download links"""
    
    def __init__(self, credentials_path: str = "credentials/google_sheets_credentials.json"):
        self.credentials_path = Path(credentials_path)
        self.scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        self.downloader = GoogleDriveDownloader(credentials_path)
        
    def authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            creds = Credentials.from_service_account_file(
                self.credentials_path, scopes=self.scope
            )
            return gspread.authorize(creds)
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return None
    
    def read_module_sheet(self, sheet_id: str, worksheet_name: str = "Sheet1") -> Dict:
        """Read module data from Google Sheet"""
        client = self.authenticate()
        if not client:
            return {}
        
        try:
            sheet = client.open_by_key(sheet_id).worksheet(worksheet_name)
            data = sheet.get_all_records()
            
            modules = {}
            for row in data:
                if row.get('ACTIVE/INACTIVE') == 'ACTIVE':
                    module_id = row.get('Module ID', '')
                    if module_id:
                        modules[module_id] = {
                            'name': row.get('Name', ''),
                            'type': row.get('Type', ''),
                            'description': row.get('Description', ''),
                            'download_link': row.get('Download Link', ''),
                            'comments': row.get('Comments on Cursor Revision', ''),
                            'active': True
                        }
            
            return modules
            
        except Exception as e:
            print(f"❌ Failed to read sheet: {e}")
            return {}
    
    def download_module_assets(self, modules: Dict) -> Dict:
        """Download all assets for active modules"""
        downloaded_assets = {}
        
        for module_id, module_data in modules.items():
            download_link = module_data.get('download_link', '')
            if download_link:
                print(f"🔄 Processing download link for {module_id}: {download_link}")
                
                # Determine file type and download
                if 'drawings' in download_link:
                    filename = f"{module_id}_drawing.png"
                    file_path = self.downloader.download_google_drawing(download_link, filename)
                elif 'document' in download_link:
                    filename = f"{module_id}_doc.pdf"
                    file_path = self.downloader.download_google_doc_as_pdf(download_link, filename)
                else:
                    print(f"⚠️ Unknown file type for {module_id}: {download_link}")
                    continue
                
                if file_path:
                    downloaded_assets[module_id] = {
                        'file_path': file_path,
                        'original_url': download_link,
                        'module_data': module_data
                    }
        
        return downloaded_assets
    
    def update_module_inputs(self, modules: Dict, assets: Dict) -> None:
        """Update module_inputs.json with downloaded assets"""
        try:
            with open('module_inputs.json', 'r') as f:
                current_data = json.load(f)
            
            # Update modules with asset information
            for module_id, asset_info in assets.items():
                if module_id in current_data['modules']:
                    current_data['modules'][module_id]['asset_file'] = str(asset_info['file_path'])
                    current_data['modules'][module_id]['download_link'] = asset_info['original_url']
            
            # Add metadata about the download session
            current_data['metadata']['last_download'] = datetime.now().isoformat()
            current_data['metadata']['downloaded_assets'] = len(assets)
            
            with open('module_inputs.json', 'w') as f:
                json.dump(current_data, f, indent=2)
            
            print(f"✅ Updated module_inputs.json with {len(assets)} assets")
            
        except Exception as e:
            print(f"❌ Failed to update module_inputs.json: {e}")

def main():
    """Main function to read Google Sheet and download assets"""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Initialize reader
    reader = GoogleSheetReader()
    
    # Read from Google Sheet (you'll need to provide the actual sheet ID)
    sheet_id = "YOUR_GOOGLE_SHEET_ID_HERE"  # Replace with actual sheet ID
    
    print("🔄 Reading Google Sheet...")
    modules = reader.read_module_sheet(sheet_id)
    
    if not modules:
        print("⚠️ No modules found or sheet reading failed")
        modules = {}  # Initialize empty dict instead of returning
        assets = {}   # Initialize empty dict for assets
    
    print(f"✅ Found {len(modules)} active modules")
    
    # Download assets (only if modules exist)
    if modules:
        print("🔄 Downloading assets...")
        assets = reader.download_module_assets(modules)
        
        # Update module_inputs.json
        reader.update_module_inputs(modules, assets)
    else:
        assets = {}  # Empty assets dict
    
    # Generate report
    report_file = output_dir / f"google_sheet_read_0Z.0A_{timestamp}.txt"
    
    with open(report_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("GOOGLE SHEET READ REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Modules Found: {len(modules)}\n")
        f.write(f"Assets Downloaded: {len(assets)}\n\n")
        
        f.write("ACTIVE MODULES:\n")
        f.write("-" * 40 + "\n")
        for module_id, module_data in modules.items():
            f.write(f"{module_id}: {module_data['name']}\n")
            f.write(f"  Type: {module_data['type']}\n")
            f.write(f"  Description: {module_data['description']}\n")
            if module_id in assets:
                f.write(f"  Asset: {assets[module_id]['file_path']}\n")
            f.write("\n")
    
    print(f"✅ Generated report: {report_file}")
    
    # Create PDF report
    try:
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages
        
        pdf_file = output_dir / f"google_sheet_read_0Z.0A_{timestamp}.pdf"
        
        with PdfPages(pdf_file) as pdf:
            fig = plt.figure(figsize=(8.5, 11))
            plt.axis('off')
            
            plt.text(0.5, 0.9, "Google Sheet Read Report", fontsize=20, 
                    ha='center', va='center', fontweight='bold')
            plt.text(0.5, 0.8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                    fontsize=14, ha='center', va='center')
            plt.text(0.5, 0.7, f"Modules Found: {len(modules)}", 
                    fontsize=12, ha='center', va='center')
            plt.text(0.5, 0.6, f"Assets Downloaded: {len(assets)}", 
                    fontsize=12, ha='center', va='center')
            
            # Add asset list
            y_pos = 0.5
            for module_id, asset_info in assets.items():
                plt.text(0.1, y_pos, f"{module_id}: {asset_info['file_path'].name}", 
                        fontsize=10, ha='left', va='center')
                y_pos -= 0.05
            
            pdf.savefig(fig, facecolor='white')
            plt.close(fig)
        
        print(f"✅ Generated PDF: {pdf_file}")
        
    except ImportError:
        print(f"⚠️ Matplotlib not available - created text report only")

if __name__ == "__main__":
    main()
