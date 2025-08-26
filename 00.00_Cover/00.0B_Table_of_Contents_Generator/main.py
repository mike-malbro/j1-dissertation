#!/usr/bin/env python3
"""
Table of Contents Generator - 00.0B
Michael Logan Maloney PhD Dissertation Notebook
Table of Contents generator based on active modules
"""

import os
import sys
import yaml
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def load_config():
    """Load configuration from config.yaml"""
    config_file = Path("config.yaml")
    if config_file.exists():
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    return {}

def get_active_modules():
    """Get list of active modules from the structure"""
    # Define the module structure based on the Google Sheet
    modules = {
        '00.00': {'name': 'Cover', 'type': 'Module', 'active': True},
        '00.0A': {'name': 'Cover Generator', 'type': 'Submodule', 'active': True},
        '00.0B': {'name': 'Table of Contents Generator', 'type': 'Submodule', 'active': True},
        '01.00': {'name': 'J1 - Journal 1', 'type': 'Module', 'active': True},
        '01.0A': {'name': 'Abstract', 'type': 'Submodule', 'active': True},
        '01.0B': {'name': 'Graphical Abstract', 'type': 'Submodule', 'active': True},
        '0R.00': {'name': 'References', 'type': 'Module', 'active': True},
        '0R.0A': {'name': 'Abbreviations', 'type': 'Submodule', 'active': True},
        '0R.01': {'name': 'J1 References', 'type': 'Submodule', 'active': True},
        '0R.0Z': {'name': 'General References', 'type': 'Submodule', 'active': True},
        '0R.0F': {'name': 'Figures', 'type': 'Submodule', 'active': True},
        '0R.0C': {'name': 'Calculations', 'type': 'Submodule', 'active': True},
        '0Z.00': {'name': 'Google Sheet Helper Functions', 'type': 'Module', 'active': True},
        '0Z.0A': {'name': 'Read', 'type': 'Submodule', 'active': True},
        '0Z.0B': {'name': 'Write', 'type': 'Submodule', 'active': True},
        '0Z.0X': {'name': 'Misc Google Sheet Interactive Scripts', 'type': 'Submodule', 'active': True}
    }
    
    return {k: v for k, v in modules.items() if v['active']}

def generate_table_of_contents():
    """Generate a professional table of contents"""
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Get active modules
    active_modules = get_active_modules()
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title
    title_text = "Table of Contents"
    ax.text(4.25, 10.5, title_text, fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial')

    subtitle_text = "Michael Logan Maloney PhD Dissertation Notebook"
    ax.text(4.25, 10, subtitle_text, fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial')

    # Generate TOC entries
    y_position = 9
    page_number = 1

    # Group modules by their main module
    main_modules = {}
    for module_id, module_info in active_modules.items():
        if module_id == 'main.py':
            continue

        main_id_prefix = module_id.split('.')[0]
        main_id = main_id_prefix + '.00' # Assuming main modules end with .00

        # Handle cases where the main module itself is listed (e.g., 00.00)
        if module_id == main_id:
            if main_id not in main_modules:
                main_modules[main_id] = []
            main_modules[main_id].insert(0, (module_id, module_info)) # Ensure main module is first
        else:
            if main_id not in main_modules:
                main_modules[main_id] = []
            main_modules[main_id].append((module_id, module_info))

    # Sort main modules by ID
    sorted_main_modules = sorted(main_modules.items())

    for main_id, submodules in sorted_main_modules:
        # Add main module
        main_module_info = active_modules.get(main_id, {'name': 'Unknown', 'type': 'Module'})
        main_text = f"{main_id} {main_module_info['name']}"
        ax.text(0.5, y_position, main_text, fontsize=14, fontweight='normal',
                ha='left', va='center', fontfamily='Arial')
        ax.text(7.5, y_position, str(page_number), fontsize=14, fontweight='normal',
                ha='right', va='center', fontfamily='Arial')
        y_position -= 0.4
        page_number += 1

        # Add submodules
        # Sort submodules to ensure consistent order
        sorted_submodules = sorted([s for s in submodules if s[0] != main_id])
        for sub_id, sub_info in sorted_submodules:
            sub_text = f"  {sub_id} {sub_info['name']}"
            ax.text(0.5, y_position, sub_text, fontsize=14, fontweight='normal',
                    ha='left', va='center', fontfamily='Arial')
            ax.text(7.5, y_position, str(page_number), fontsize=14, fontweight='normal',
                    ha='right', va='center', fontfamily='Arial')
            y_position -= 0.3
            page_number += 1

        y_position -= 0.2  # Extra space between main modules

    # Footer information
    footer_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ax.text(4.25, 0.5, footer_text, fontsize=10, fontweight='normal',
            ha='center', va='center', fontfamily='Arial')

    # Page number
    ax.text(4.25, 0.3, "2", fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial')

    # Module identifier
    module_text = "Module: 00.0B - Table of Contents Generator"
    ax.text(4.25, 0.1, module_text, fontsize=10, fontweight='normal',
            ha='center', va='center', fontfamily='Arial')
    
    # Save as PDF
    output_file = output_dir / f"table_of_contents_00.0B_{timestamp}.pdf"
    with PdfPages(output_file) as pdf:
        pdf.savefig(fig, dpi=300, bbox_inches='tight')
    
    plt.close()
    
    print(f"✅ Table of contents generated: {output_file}")
    return str(output_file)

def main():
    """Main function to generate table of contents"""
    print("📋 Generating Table of Contents...")
    
    try:
        output_file = generate_table_of_contents()
        print(f"📄 Table of contents created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating table of contents: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
