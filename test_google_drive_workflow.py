#!/usr/bin/env python3
"""
Test Google Drive Download Workflow
Demonstrates the complete workflow for downloading Google Drive assets and integrating into PDF
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "0Z.00_Google_Sheet_Helper_Functions"))

from google_drive_helpers import download_asset, get_asset_statistics, list_assets
from pdf_asset_integration import integrate_asset, create_report_with_assets, get_asset_summary

def test_google_drive_workflow():
    """Test the complete Google Drive download workflow"""
    print("🧪 Testing Google Drive Download Workflow")
    print("=" * 60)
    
    # Your specific Google Drawing URL from the module
    test_url = "https://docs.google.com/drawings/d/1Mx3Uug0W3zOUvEeE9tmppbM0gTn-0mD_vgZJv6hXcCo/edit"
    module_id = "01.0C"
    
    print(f"📥 Downloading asset for module {module_id}")
    print(f"URL: {test_url}")
    
    # Step 1: Download the asset
    asset_path = download_asset(
        url=test_url,
        module_id=module_id,
        filename="problem_system_model.png"
    )
    
    if asset_path:
        print(f"✅ Successfully downloaded: {asset_path}")
        
        # Step 2: Show asset statistics
        print("\n📊 Asset Statistics:")
        stats = get_asset_statistics()
        print(f"  Total assets: {stats['total_assets']}")
        print(f"  Total size: {stats['total_size_mb']} MB")
        print(f"  File types: {stats['file_types']}")
        
        # Step 3: List assets for this module
        print(f"\n📋 Assets for module {module_id}:")
        module_assets = list_assets(module_id=module_id)
        for asset in module_assets:
            print(f"  - {asset['file_path']} ({asset['file_type']})")
        
        # Step 4: Integrate into PDF
        print(f"\n📄 Integrating asset into PDF...")
        pdf_path = Path("output/test_report.pdf")
        success = integrate_asset(
            module_id=module_id,
            pdf_path=pdf_path,
            title="Problem System Model"
        )
        
        if success:
            print(f"✅ Successfully integrated into PDF")
        else:
            print("❌ Failed to integrate into PDF")
        
        # Step 5: Create comprehensive report
        print(f"\n📚 Creating comprehensive report...")
        report_path = create_report_with_assets(
            module_ids=[module_id],
            title="J1 Dissertation Test Report"
        )
        
        if report_path:
            print(f"✅ Created comprehensive report: {report_path}")
        
        # Step 6: Show asset summary
        print(f"\n📈 Asset Summary:")
        summary = get_asset_summary()
        print(f"  Modules with assets: {summary['modules_with_assets']}")
        print(f"  File types: {summary['file_types']}")
        
    else:
        print("❌ Failed to download asset")
    
    print("\n" + "=" * 60)
    print("🎉 Google Drive Workflow Test Complete!")

def test_helper_functions():
    """Test individual helper functions"""
    print("\n🔧 Testing Helper Functions")
    print("-" * 40)
    
    # Test asset statistics
    stats = get_asset_statistics()
    print(f"Asset Statistics: {stats}")
    
    # Test asset listing
    assets = list_assets()
    print(f"Total assets found: {len(assets)}")
    
    # Test asset summary
    summary = get_asset_summary()
    print(f"Asset Summary: {summary}")

if __name__ == "__main__":
    # Run the complete workflow test
    test_google_drive_workflow()
    
    # Run helper function tests
    test_helper_functions()
