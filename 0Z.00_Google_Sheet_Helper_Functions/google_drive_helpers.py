#!/usr/bin/env python3
"""
Google Drive Helper Functions
Comprehensive helper functions for Google Drive operations in J1 PhD Dissertation

This module provides reusable functions for:
- Downloading Google Drawings as PNG
- Downloading Google Docs as PDF
- Extracting Drive IDs from URLs
- Managing downloaded assets
- Integration with module system
"""

import os
import re
import requests
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union
import gspread
from google.oauth2.service_account import Credentials
from PIL import Image
import io

class GoogleDriveHelpers:
    """Comprehensive Google Drive helper functions for J1 system"""
    
    def __init__(self, credentials_path: str = "credentials/google_sheets_credentials.json"):
        self.credentials_path = Path(credentials_path)
        self.download_dir = Path("downloads")
        self.download_dir.mkdir(exist_ok=True)
        self.assets_db_file = self.download_dir / "assets_database.json"
        self.load_assets_database()
        
    def load_assets_database(self):
        """Load or create assets database"""
        if self.assets_db_file.exists():
            with open(self.assets_db_file, 'r') as f:
                self.assets_db = json.load(f)
        else:
            self.assets_db = {
                'assets': {},
                'metadata': {
                    'created': datetime.now().isoformat(),
                    'total_downloads': 0,
                    'last_updated': datetime.now().isoformat()
                }
            }
    
    def save_assets_database(self):
        """Save assets database"""
        self.assets_db['metadata']['last_updated'] = datetime.now().isoformat()
        with open(self.assets_db_file, 'w') as f:
            json.dump(self.assets_db, f, indent=2)
    
    def extract_drive_id(self, url: str) -> Optional[str]:
        """Extract Google Drive ID from various URL formats"""
        patterns = [
            r'/d/([a-zA-Z0-9-_]+)',  # Standard Drive URL
            r'/drawings/d/([a-zA-Z0-9-_]+)',  # Google Drawings
            r'/document/d/([a-zA-Z0-9-_]+)',  # Google Docs
            r'/spreadsheets/d/([a-zA-Z0-9-_]+)',  # Google Sheets
            r'/presentation/d/([a-zA-Z0-9-_]+)',  # Google Slides
            r'/forms/d/([a-zA-Z0-9-_]+)',  # Google Forms
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_file_type_from_url(self, url: str) -> str:
        """Determine file type from Google Drive URL"""
        if 'drawings' in url:
            return 'drawing'
        elif 'document' in url:
            return 'document'
        elif 'spreadsheets' in url:
            return 'spreadsheet'
        elif 'presentation' in url:
            return 'presentation'
        elif 'forms' in url:
            return 'form'
        elif 'file/d/' in url:
            return 'file'
        else:
            return 'unknown'
    
    def download_google_drawing(self, url: str, filename: str = None, module_id: str = None) -> Optional[Path]:
        """Download Google Drawing as PNG with metadata tracking"""
        drive_id = self.extract_drive_id(url)
        if not drive_id:
            print(f"❌ Could not extract Drive ID from: {url}")
            return None
        
        # Always download fresh content for drawings (no caching)
        print(f"🔄 Downloading fresh drawing content for {drive_id}")
        
        # Google Drawing export URL
        export_url = f"https://docs.google.com/drawings/d/{drive_id}/export/png"
        
        try:
            # Use proper headers to mimic browser behavior
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'image/png,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': f'https://docs.google.com/drawings/d/{drive_id}/edit',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            # Follow redirects and use proper timeout
            response = requests.get(export_url, headers=headers, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            if not filename:
                filename = f"drawing_{drive_id}.png"
            
            file_path = self.download_dir / filename
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            # Update database
            self.assets_db['assets'][drive_id] = {
                'file_path': str(file_path),
                'original_url': url,
                'file_type': 'drawing',
                'module_id': module_id,
                'downloaded_at': datetime.now().isoformat(),
                'file_size': len(response.content)
            }
            self.assets_db['metadata']['total_downloads'] += 1
            self.save_assets_database()
            
            print(f"✅ Fresh drawing downloaded: {file_path} ({len(response.content)} bytes)")
            return file_path
            
        except Exception as e:
            print(f"❌ Failed to download {url}: {e}")
            return None
    
    def download_google_doc_as_pdf(self, url: str, filename: str = None, module_id: str = None) -> Optional[Path]:
        """Download Google Doc as PDF with metadata tracking"""
        drive_id = self.extract_drive_id(url)
        if not drive_id:
            return None
        
        # Check if already downloaded
        if drive_id in self.assets_db['assets']:
            existing_path = Path(self.assets_db['assets'][drive_id]['file_path'])
            if existing_path.exists():
                print(f"✅ Already downloaded: {existing_path}")
                return existing_path
        
        export_url = f"https://docs.google.com/document/d/{drive_id}/export?format=pdf"
        
        try:
            response = requests.get(export_url, timeout=30)
            response.raise_for_status()
            
            if not filename:
                filename = f"doc_{drive_id}.pdf"
            
            file_path = self.download_dir / filename
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            # Update database
            self.assets_db['assets'][drive_id] = {
                'file_path': str(file_path),
                'original_url': url,
                'file_type': 'document',
                'module_id': module_id,
                'downloaded_at': datetime.now().isoformat(),
                'file_size': len(response.content)
            }
            self.assets_db['metadata']['total_downloads'] += 1
            self.save_assets_database()
            
            print(f"✅ Downloaded: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"❌ Failed to download {url}: {e}")
            return None
    
    def download_google_sheet_as_pdf(self, url: str, filename: str = None, module_id: str = None) -> Optional[Path]:
        """Download Google Sheet as PDF with metadata tracking"""
        drive_id = self.extract_drive_id(url)
        if not drive_id:
            return None
        
        export_url = f"https://docs.google.com/spreadsheets/d/{drive_id}/export?format=pdf"
        
        try:
            response = requests.get(export_url, timeout=30)
            response.raise_for_status()
            
            if not filename:
                filename = f"sheet_{drive_id}.pdf"
            
            file_path = self.download_dir / filename
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            # Update database
            self.assets_db['assets'][drive_id] = {
                'file_path': str(file_path),
                'original_url': url,
                'file_type': 'spreadsheet',
                'module_id': module_id,
                'downloaded_at': datetime.now().isoformat(),
                'file_size': len(response.content)
            }
            self.assets_db['metadata']['total_downloads'] += 1
            self.save_assets_database()
            
            print(f"✅ Downloaded: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"❌ Failed to download {url}: {e}")
            return None
    
    def download_google_file(self, url: str, filename: str = None, module_id: str = None) -> Optional[Path]:
        """Download Google Drive file (CSV, etc.) directly"""
        drive_id = self.extract_drive_id(url)
        if not drive_id:
            print(f"❌ Could not extract Drive ID from: {url}")
            return None
        
        # For CSV files, always download fresh (don't cache)
        if filename and filename.endswith('.csv'):
            print(f"📥 CSV file detected - forcing fresh download")
        else:
            # Check if already downloaded (for non-CSV files)
            if drive_id in self.assets_db['assets']:
                existing_path = Path(self.assets_db['assets'][drive_id]['file_path'])
                if existing_path.exists():
                    print(f"✅ Already downloaded: {existing_path}")
                    return existing_path
        
        # Generate filename if not provided
        if not filename:
            filename = f"google_file_{drive_id}.csv"
        
        # Create module-specific directory
        if module_id:
            module_dir = self.download_dir / module_id
            module_dir.mkdir(exist_ok=True)
            file_path = module_dir / filename
        else:
            file_path = self.download_dir / filename
        
        try:
            # Convert Google Drive URL to direct download URL
            direct_url = f"https://drive.google.com/uc?export=download&id={drive_id}"
            
            print(f"📥 Downloading file from: {direct_url}")
            response = requests.get(direct_url, stream=True)
            response.raise_for_status()
            
            # Write file
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Get file size
            file_size = file_path.stat().st_size
            
            # Update assets database
            self.assets_db['assets'][drive_id] = {
                'file_path': str(file_path),
                'file_type': 'file',
                'module_id': module_id,
                'filename': filename,
                'file_size': file_size,
                'downloaded_at': datetime.now().isoformat(),
                'url': url
            }
            self.save_assets_database()
            
            print(f"✅ File downloaded successfully: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"❌ Failed to download file {url}: {e}")
            return None
    
    def download_asset(self, url: str, module_id: str = None, filename: str = None) -> Optional[Path]:
        """Universal download function that determines file type and downloads appropriately"""
        file_type = self.get_file_type_from_url(url)
        
        if file_type == 'drawing':
            return self.download_google_drawing(url, filename, module_id)
        elif file_type == 'document':
            return self.download_google_doc_as_pdf(url, filename, module_id)
        elif file_type == 'spreadsheet':
            return self.download_google_sheet_as_pdf(url, filename, module_id)
        elif file_type == 'file':
            return self.download_google_file(url, filename, module_id)
        else:
            print(f"⚠️ Unsupported file type: {file_type}")
            return None
    
    def get_asset_info(self, drive_id: str) -> Optional[Dict]:
        """Get information about a downloaded asset"""
        return self.assets_db['assets'].get(drive_id)
    
    def list_downloaded_assets(self, module_id: str = None) -> List[Dict]:
        """List all downloaded assets, optionally filtered by module"""
        assets = []
        for drive_id, asset_info in self.assets_db['assets'].items():
            if module_id is None or asset_info.get('module_id') == module_id:
                assets.append({
                    'drive_id': drive_id,
                    **asset_info
                })
        return assets
    
    def cleanup_old_assets(self, days_old: int = 30) -> int:
        """Clean up assets older than specified days"""
        cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        removed_count = 0
        
        for drive_id, asset_info in list(self.assets_db['assets'].items()):
            downloaded_at = datetime.fromisoformat(asset_info['downloaded_at']).timestamp()
            if downloaded_at < cutoff_date:
                file_path = Path(asset_info['file_path'])
                if file_path.exists():
                    file_path.unlink()
                del self.assets_db['assets'][drive_id]
                removed_count += 1
        
        self.save_assets_database()
        print(f"🧹 Cleaned up {removed_count} old assets")
        return removed_count
    
    def validate_asset(self, file_path: Union[str, Path]) -> bool:
        """Validate that a downloaded asset is still accessible"""
        file_path = Path(file_path)
        if not file_path.exists():
            return False
        
        try:
            if file_path.suffix.lower() == '.png':
                with Image.open(file_path) as img:
                    img.verify()
            elif file_path.suffix.lower() == '.pdf':
                # Basic PDF validation
                with open(file_path, 'rb') as f:
                    header = f.read(4)
                    return header == b'%PDF'
            return True
        except Exception:
            return False
    
    def get_asset_statistics(self) -> Dict:
        """Get statistics about downloaded assets"""
        total_assets = len(self.assets_db['assets'])
        total_size = sum(asset.get('file_size', 0) for asset in self.assets_db['assets'].values())
        
        file_types = {}
        for asset in self.assets_db['assets'].values():
            file_type = asset.get('file_type', 'unknown')
            file_types[file_type] = file_types.get(file_type, 0) + 1
        
        return {
            'total_assets': total_assets,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'file_types': file_types,
            'last_updated': self.assets_db['metadata']['last_updated']
        }

# Convenience functions for easy use
def download_google_drawing(url: str, filename: str = None, module_id: str = None) -> Optional[Path]:
    """Convenience function to download Google Drawing"""
    helper = GoogleDriveHelpers()
    return helper.download_google_drawing(url, filename, module_id)

def download_google_doc(url: str, filename: str = None, module_id: str = None) -> Optional[Path]:
    """Convenience function to download Google Doc as PDF"""
    helper = GoogleDriveHelpers()
    return helper.download_google_doc_as_pdf(url, filename, module_id)

def download_asset(url: str, module_id: str = None, filename: str = None) -> Optional[Path]:
    """Convenience function to download any Google Drive asset"""
    helper = GoogleDriveHelpers()
    return helper.download_asset(url, module_id, filename)

def get_asset_statistics() -> Dict:
    """Convenience function to get asset statistics"""
    helper = GoogleDriveHelpers()
    return helper.get_asset_statistics()

def list_assets(module_id: str = None) -> List[Dict]:
    """Convenience function to list downloaded assets"""
    helper = GoogleDriveHelpers()
    return helper.list_downloaded_assets(module_id)

if __name__ == "__main__":
    # Test the helper functions
    print("🧪 Testing Google Drive Helper Functions")
    
    # Example usage
    test_url = "https://docs.google.com/drawings/d/1Mx3Uug0W3zOUvEeE9tmppbM0gTn-0mD_vgZJv6hXcCo/edit"
    
    print(f"Testing download: {test_url}")
    result = download_asset(test_url, module_id="01.0C", filename="test_drawing.png")
    
    if result:
        print(f"✅ Successfully downloaded: {result}")
    else:
        print("❌ Download failed")
    
    # Show statistics
    stats = get_asset_statistics()
    print(f"📊 Asset Statistics: {stats}")
