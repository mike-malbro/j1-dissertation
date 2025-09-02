#!/usr/bin/env python3
"""
Module Status Overview - 00.0A
Michael Logan Maloney PhD Dissertation Notebook
Comprehensive overview of all active and inactive modules
"""
import json
import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def load_module_config():
    """Load module configuration from module_inputs.json"""
    try:
        config_file = Path(__file__).parent / ".." / ".." / "module_inputs.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            print(f"⚠️ module_inputs.json not found at {config_file}")
            return {}
    except Exception as e:
        print(f"⚠️ Error loading module config: {e}")
        return {}

def generate_module_status_overview():
    """Generate a comprehensive module status overview"""
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    module_config = load_module_config()
    
    if not module_config:
        print("❌ Failed to load module configuration")
        return None
    
    print(f"📊 Loaded {len(module_config.get('modules', {}))} modules from configuration")
    
    # Create PDF version using PdfPages
    pdf_file = output_dir / f"module_status_overview_{timestamp}.pdf"
    
    with PdfPages(pdf_file) as pdf:
        # Create a new figure for the PDF with correct 8.5 x 11 size
        fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
        ax.set_xlim(0, 8.5)
        ax.set_ylim(0, 11)
        ax.axis('off')
        
        # Title
        title_text = "Module Status Overview"
        ax.text(4.25, 10.5, title_text, fontsize=16, fontweight='bold',
                ha='center', va='center', fontfamily='Arial')

        subtitle_text = "Michael Logan Maloney PhD Dissertation Notebook"
        ax.text(4.25, 10, subtitle_text, fontsize=12, fontweight='normal',
                ha='center', va='center', fontfamily='Arial')
        
        timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ax.text(4.25, 9.7, timestamp_text, fontsize=10, fontweight='normal',
                ha='center', va='center', fontfamily='Arial')

        # Summary statistics
        total_modules = len(module_config.get('modules', {}))
        active_modules = sum(1 for module in module_config.get('modules', {}).values() 
                           if module.get('active', False))
        inactive_modules = total_modules - active_modules
        
        summary_text = f"Total Modules: {total_modules} | Active: {active_modules} | Inactive: {inactive_modules}"
        ax.text(4.25, 9.4, summary_text, fontsize=10, fontweight='bold',
                ha='center', va='center', fontfamily='Arial')

        # Column headers
        ax.text(0.5, 9.0, "Module ID", fontsize=11, fontweight='bold',
                ha='left', va='center', fontfamily='Arial')
        ax.text(2.0, 9.0, "Module Name", fontsize=11, fontweight='bold',
                ha='left', va='center', fontfamily='Arial')
        ax.text(6.5, 9.0, "Status", fontsize=11, fontweight='bold',
                ha='center', va='center', fontfamily='Arial')
        
        # Separator line
        ax.axhline(y=8.8, xmin=0.05, xmax=0.95, color='black', linewidth=0.5)

        # Generate overview entries
        y_position = 8.5
        modules_processed = 0
        
        # Process modules in order
        for module_id, module_info in sorted(module_config.get('modules', {}).items()):
            if module_id in ['main.py', 'module_inputs.json']:
                continue  # Skip system files
                
            module_name = module_info.get('name', 'Unknown')
            module_type = module_info.get('type', 'Unknown')
            module_status = module_info.get('active', False)
            
            print(f"  📝 Processing: {module_id} - {module_name} ({module_type}) - {module_status}")
            
            # Color code based on status
            status_color = 'green' if module_status else 'red'
            status_text = 'ACTIVE' if module_status else 'INACTIVE'
            
            # Determine indentation based on module type
            if module_type == 'Module':
                # Main module - bold
                ax.text(0.5, y_position, f"{module_id}", fontsize=11, fontweight='bold',
                        ha='left', va='center', fontfamily='Arial')
                ax.text(2.0, y_position, f"{module_name}", fontsize=11, fontweight='bold',
                        ha='left', va='center', fontfamily='Arial')
                ax.text(6.5, y_position, f"{status_text}", fontsize=11, fontweight='bold',
                        ha='center', va='center', fontfamily='Arial', color=status_color)
                y_position -= 0.3
            else:
                # Submodule - normal weight, indented
                ax.text(0.8, y_position, f"  {module_id}", fontsize=10, fontweight='normal',
                        ha='left', va='center', fontfamily='Arial')
                ax.text(2.5, y_position, f"{module_name}", fontsize=10, fontweight='normal',
                        ha='left', va='center', fontfamily='Arial')
                ax.text(6.5, y_position, f"{status_text}", fontsize=10, fontweight='normal',
                        ha='center', va='center', fontfamily='Arial', color=status_color)
                y_position -= 0.25
            
            modules_processed += 1
            
            # Check if we need a new page
            if y_position < 1.0:
                # Save current page and start new one
                pdf.savefig(fig, bbox_inches='tight', dpi=300)
                plt.close()
                
                # Create second page
                fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
                ax.set_xlim(0, 8.5)
                ax.set_ylim(0, 11)
                ax.axis('off')
                
                # Page 2 header
                ax.text(4.25, 10.5, "Module Status Overview (Continued)", fontsize=16, fontweight='bold',
                        ha='center', va='center', fontfamily='Arial')
                ax.text(4.25, 10, "Michael Logan Maloney PhD Dissertation Notebook", fontsize=12, fontweight='normal',
                        ha='center', va='center', fontfamily='Arial')
                
                y_position = 9.5

        # Legend
        legend_y = 1.5
        ax.text(0.5, legend_y, "Legend:", fontsize=10, fontweight='bold',
                ha='left', va='center', fontfamily='Arial')
        ax.text(0.5, legend_y - 0.2, "• ACTIVE: Module will be executed and included in final PDF", fontsize=9, fontweight='normal',
                ha='left', va='center', fontfamily='Arial')
        ax.text(0.5, legend_y - 0.4, "• INACTIVE: Module will be skipped during execution", fontsize=9, fontweight='normal',
                ha='left', va='center', fontfamily='Arial')
        ax.text(0.5, legend_y - 0.6, "• Module ID format: XX.YY where XX = main module, YY = submodule", fontsize=9, fontweight='normal',
                ha='left', va='center', fontfamily='Arial')

        print(f"📊 Processed {modules_processed} modules, saving PDF...")
        
        # Save the final page with high DPI and proper sizing
        pdf.savefig(fig, bbox_inches='tight', dpi=300)
        plt.close()
    
    print(f"✅ PDF saved: {pdf_file}")
    
    # Also save as PNG for reference (simplified version)
    png_file = output_dir / f"module_status_overview_{timestamp}.png"
    
    # Create a new figure for PNG
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title
    ax.text(4.25, 10.5, title_text, fontsize=16, fontweight='bold',
            ha='center', va='center', fontfamily='Arial')
    ax.text(4.25, 10, subtitle_text, fontsize=12, fontweight='normal',
            ha='center', va='center', fontfamily='Arial')
    ax.text(4.25, 9.7, timestamp_text, fontsize=10, fontweight='normal',
            ha='center', va='center', fontfamily='Arial')
    ax.text(4.25, 9.4, summary_text, fontsize=10, fontweight='bold',
            ha='center', va='center', fontfamily='Arial')
    
    # Column headers
    ax.text(0.5, 9.0, "Module ID", fontsize=11, fontweight='bold',
            ha='left', va='center', fontfamily='Arial')
    ax.text(2.0, 9.0, "Module Name", fontsize=11, fontweight='bold',
            ha='left', va='center', fontfamily='Arial')
    ax.text(6.5, 9.0, "Status", fontsize=11, fontweight='bold',
            ha='center', va='center', fontfamily='Arial')
    
    # Separator line
    ax.axhline(y=8.8, xmin=0.05, xmax=0.95, color='black', linewidth=0.5)
    
    # Generate overview entries for PNG
    y_position = 8.5
    for module_id, module_info in sorted(module_config.get('modules', {}).items()):
        if module_id in ['main.py', 'module_inputs.json']:
            continue
            
        module_name = module_info.get('name', 'Unknown')
        module_type = module_info.get('type', 'Unknown')
        module_status = module_info.get('active', False)
        
        status_color = 'green' if module_status else 'red'
        status_text = 'ACTIVE' if module_status else 'INACTIVE'
        
        if module_type == 'Module':
            ax.text(0.5, y_position, f"{module_id}", fontsize=11, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial')
            ax.text(2.0, y_position, f"{module_name}", fontsize=11, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial')
            ax.text(6.5, y_position, f"{status_text}", fontsize=11, fontweight='bold',
                    ha='center', va='center', fontfamily='Arial', color=status_color)
            y_position -= 0.3
        else:
            ax.text(0.8, y_position, f"  {module_id}", fontsize=10, fontweight='normal',
                    ha='left', va='center', fontfamily='Arial')
            ax.text(2.5, y_position, f"{module_name}", fontsize=10, fontweight='normal',
                    ha='left', va='center', fontfamily='Arial')
            ax.text(6.5, y_position, f"{status_text}", fontsize=10, fontweight='normal',
                    ha='center', va='center', fontfamily='Arial', color=status_color)
            y_position -= 0.25
    
    # Legend for PNG
    legend_y = 1.5
    ax.text(0.5, legend_y, "Legend:", fontsize=10, fontweight='bold',
            ha='left', va='center', fontfamily='Arial')
    ax.text(0.5, legend_y - 0.2, "• ACTIVE: Module will be executed and included in final PDF", fontsize=9, fontweight='normal',
            ha='left', va='center', fontfamily='Arial')
    ax.text(0.5, legend_y - 0.4, "• INACTIVE: Module will be skipped during execution", fontsize=9, fontweight='normal',
            ha='left', va='center', fontfamily='Arial')
    ax.text(0.5, legend_y - 0.6, "• Module ID format: XX.YY where XX = main module, YY = submodule", fontsize=9, fontweight='normal',
            ha='left', va='center', fontfamily='Arial')
    
    plt.savefig(png_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Module Status Overview generated: {png_file} and {pdf_file}")
    return pdf_file

def main():
    """Main function to generate module status overview"""
    print("📋 Generating Module Status Overview...")
    try:
        output_file = generate_module_status_overview()
        if output_file:
            print(f"📄 Module Status Overview created successfully: {output_file}")
            return {"status": "success", "output_file": str(output_file)}
        else:
            print("❌ Failed to generate Module Status Overview")
            return {"status": "error", "message": "Generation failed"}
    except Exception as e:
        print(f"❌ Error generating Module Status Overview: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    main()
