#!/usr/bin/env python3
"""
PDF Asset Integration Helper
Integrate downloaded Google Drive assets into PDF reports

This module provides functions for:
- Inserting images into PDF reports
- Adding captions and metadata
- Managing figure numbering
- Professional formatting
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime
import json
from PIL import Image as PILImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches

class PDFAssetIntegrator:
    """Integrate Google Drive assets into PDF reports with professional formatting"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.figure_counter = 1
        self.assets_db_file = Path("downloads/assets_database.json")
        self.load_assets_database()
        
    def load_assets_database(self):
        """Load assets database if it exists"""
        if self.assets_db_file.exists():
            with open(self.assets_db_file, 'r') as f:
                self.assets_db = json.load(f)
        else:
            self.assets_db = {'assets': {}}
    
    def get_asset_path(self, module_id: str) -> Optional[Path]:
        """Get asset file path for a module"""
        for drive_id, asset_info in self.assets_db['assets'].items():
            if asset_info.get('module_id') == module_id:
                return Path(asset_info['file_path'])
        return None
    
    def create_figure_caption(self, module_id: str, title: str = None) -> str:
        """Create a professional figure caption"""
        if not title:
            title = f"Figure {self.figure_counter}"
        
        caption = f"{title}\n\n"
        
        # Add module-specific description
        module_descriptions = {
            "01.0C": "Problem System Model showing the data center layout and equipment configuration.",
            "01.0B": "Graphical Abstract representing the key concepts and methodology.",
            "01.0A": "Abstract visualization showing the research scope and objectives."
        }
        
        description = module_descriptions.get(module_id, "Figure from Google Drive asset.")
        caption += description
        
        # Add metadata if available
        asset_info = None
        for drive_id, info in self.assets_db['assets'].items():
            if info.get('module_id') == module_id:
                asset_info = info
                break
        
        if asset_info:
            caption += f"\n\nSource: Google Drive asset downloaded on {asset_info.get('downloaded_at', 'Unknown date')}"
        
        return caption
    
    def create_matplotlib_figure_with_asset(self, image_path: Path, caption: str, 
                                          title: str = None) -> plt.Figure:
        """Create a matplotlib figure with the asset image and caption on 8.5x11 page"""
        # Create 8.5x11 inch figure (standard US letter size)
        fig, ax = plt.subplots(figsize=(8.5, 11))
        
        # Load and display image
        img = PILImage.open(image_path)
        ax.imshow(img)
        ax.axis('off')
        
        # Add title at top of page
        if title:
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20, y=0.95)
        
        # Add caption at bottom of page
        ax.text(0.5, 0.02, caption, transform=ax.transAxes, 
                fontsize=10, ha='center', va='bottom',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8))
        
        plt.tight_layout()
        return fig
    
    def integrate_module_asset(self, module_id: str, pdf_path: Path, 
                             title: str = None, caption: str = None) -> bool:
        """Integrate a module's asset into a PDF report"""
        asset_path = self.get_asset_path(module_id)
        if not asset_path or not asset_path.exists():
            print(f"❌ No asset found for module {module_id}")
            return False
        
        if not caption:
            caption = self.create_figure_caption(module_id, title)
        
        print(f"🔄 Integrating asset for {module_id}: {asset_path}")
        
        # Create figure with asset
        fig = self.create_matplotlib_figure_with_asset(asset_path, caption, title)
        
        # Save to PDF
        output_path = self.output_dir / f"figure_{module_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        with PdfPages(output_path) as pdf:
            pdf.savefig(fig, facecolor='white', bbox_inches='tight')
        
        plt.close(fig)
        
        print(f"✅ Created figure PDF: {output_path}")
        self.figure_counter += 1
        return True
    
    def create_comprehensive_report_with_assets(self, module_ids: List[str], 
                                              title: str = "J1 Dissertation Report") -> Path:
        """Create a comprehensive PDF report with all module assets on 8.5x11 pages"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"comprehensive_report_{timestamp}.pdf"
        
        with PdfPages(output_path) as pdf:
            # Title page (8.5x11)
            fig = plt.figure(figsize=(8.5, 11))
            plt.axis('off')
            plt.text(0.5, 0.7, title, fontsize=24, ha='center', va='center', fontweight='bold')
            plt.text(0.5, 0.6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                    fontsize=14, ha='center', va='center')
            plt.text(0.5, 0.5, f"Total Assets: {len(module_ids)}", 
                    fontsize=12, ha='center', va='center')
            pdf.savefig(fig, facecolor='white')
            plt.close(fig)
            
            # Add each module's asset on separate 8.5x11 pages
            for module_id in module_ids:
                asset_path = self.get_asset_path(module_id)
                if asset_path and asset_path.exists():
                    # Create figure with proper numbering
                    figure_title = f"Figure {self.figure_counter}: {module_id}"
                    caption = self.create_figure_caption(module_id, figure_title)
                    fig = self.create_matplotlib_figure_with_asset(asset_path, caption, figure_title)
                    pdf.savefig(fig, facecolor='white', bbox_inches='tight')
                    plt.close(fig)
                    self.figure_counter += 1
        
        print(f"✅ Created comprehensive report: {output_path}")
        return output_path
    
    def get_asset_summary(self) -> Dict:
        """Get summary of all available assets"""
        summary = {
            'total_assets': len(self.assets_db['assets']),
            'modules_with_assets': [],
            'file_types': {},
            'total_size_mb': 0
        }
        
        for drive_id, asset_info in self.assets_db['assets'].items():
            module_id = asset_info.get('module_id')
            if module_id:
                summary['modules_with_assets'].append(module_id)
            
            file_type = asset_info.get('file_type', 'unknown')
            summary['file_types'][file_type] = summary['file_types'].get(file_type, 0) + 1
            
            file_size = asset_info.get('file_size', 0)
            summary['total_size_mb'] += file_size / (1024 * 1024)
        
        summary['total_size_mb'] = round(summary['total_size_mb'], 2)
        return summary

# Convenience functions
def integrate_asset(module_id: str, pdf_path: Path, title: str = None) -> bool:
    """Convenience function to integrate a module's asset"""
    integrator = PDFAssetIntegrator()
    return integrator.integrate_module_asset(module_id, pdf_path, title)

def create_report_with_assets(module_ids: List[str], title: str = None) -> Path:
    """Convenience function to create comprehensive report"""
    integrator = PDFAssetIntegrator()
    return integrator.create_comprehensive_report_with_assets(module_ids, title)

def get_asset_summary() -> Dict:
    """Convenience function to get asset summary"""
    integrator = PDFAssetIntegrator()
    return integrator.get_asset_summary()

if __name__ == "__main__":
    # Test the integration functions
    print("🧪 Testing PDF Asset Integration")
    
    # Example usage
    test_modules = ["01.0C", "01.0B", "01.0A"]
    
    summary = get_asset_summary()
    print(f"📊 Asset Summary: {summary}")
    
    # Create test report
    if summary['modules_with_assets']:
        report_path = create_report_with_assets(summary['modules_with_assets'], "Test Report")
        print(f"✅ Created test report: {report_path}")
    else:
        print("⚠️ No assets available for testing")
