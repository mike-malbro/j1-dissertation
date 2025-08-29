#!/usr/bin/env python3
"""
Module 01.02.00 - Simulation Input Summary
Michael Logan Maloney PhD Dissertation Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Simulation input parameters and configuration summary for Model 2 Scenario 1.
"""

import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import warnings
warnings.filterwarnings('ignore')

def generate_simulation_input_summary():
    """Generate Simulation Input Summary page"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Title - Left justified with book-style spacing (like 01.00)
    title_text = "Simulation Input Summary"
    ax.text(0.1, 9.9, title_text, fontsize=18, fontweight='bold', 
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # Subtitle
    subtitle_text = "Model_2_Scenario_1 Configuration Parameters"
    ax.text(0.1, 9.5, subtitle_text, fontsize=14, fontweight='normal', 
            ha='left', va='center', fontfamily='Arial', color='black')
    
    # Data Center Specifications
    dc_title = "Data Center Specifications:"
    ax.text(0.1, 8.8, dc_title, fontsize=12, fontweight='bold',
            ha='left', va='center', fontfamily='Arial', color='black')
    
    dc_specs = [
        "• Facility: Harrisburg Data Center (2N · 1 MW)",
        "• Location: Harrisburg, Pennsylvania",
        "• White Space: 34' × 44' × 7'",
        "• Layout: 4 rows, 44 servers",
        "• Total IT Load: 1 MW",
        "• Redundancy: 2N configuration"
    ]
    
    for i, spec in enumerate(dc_specs):
        y_pos = 8.5 - (i * 0.25)
        ax.text(0.1, y_pos, spec, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='black')
    
    # CRAC System Configuration
    crac_title = "CRAC System Configuration:"
    ax.text(0.1, 6.8, crac_title, fontsize=12, fontweight='bold',
            ha='left', va='center', fontfamily='Arial', color='black')
    
    crac_specs = [
        "• Primary CRAC: 1 main unit",
        "• Supplemental Units: 4 split air conditioners",
        "• Total Cooling Capacity: 1.2 MW",
        "• Cooling Type: Direct Expansion (DX)",
        "• Control Strategy: Performance Curve/Staging",
        "• Performance Curves: Advanced staging optimization"
    ]
    
    for i, spec in enumerate(crac_specs):
        y_pos = 6.5 - (i * 0.25)
        ax.text(0.1, y_pos, spec, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='black')
    
    # Simulation Parameters
    sim_title = "Simulation Parameters:"
    ax.text(0.1, 4.8, sim_title, fontsize=12, fontweight='bold',
            ha='left', va='center', fontfamily='Arial', color='black')
    
    sim_params = [
        "• Analysis Type: Performance curve analysis",
        "• Time Period: Annual analysis",
        "• Load Distribution: Staging-based allocation",
        "• Optimization Target: Staging efficiency",
        "• Baseline Comparison: Model 1 (Rule-based)",
        "• Expected Improvement: Enhanced staging control"
    ]
    
    for i, param in enumerate(sim_params):
        y_pos = 4.5 - (i * 0.25)
        ax.text(0.1, y_pos, param, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='black')
    
    # Modelica Framework
    modelica_title = "Modelica Framework Details:"
    ax.text(0.1, 2.8, modelica_title, fontsize=12, fontweight='bold',
            ha='left', va='center', fontfamily='Arial', color='black')
    
    modelica_details = [
        "• Modeling Language: Modelica",
        "• Framework: Heterogeneous multi-CRAC system",
        "• Components: Thermodynamic models",
        "• Integration: Performance curve analysis",
        "• Validation: Reference facility comparison"
    ]
    
    for i, detail in enumerate(modelica_details):
        y_pos = 2.5 - (i * 0.25)
        ax.text(0.1, y_pos, detail, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='black')
    
    # Page number - centered like 01.00
    ax.text(4.25, 0.5, "12", fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black')
    
    # Timestamp - left justified like 01.00
    timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ax.text(0.1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Module identifier - left justified like 01.00
    module_text = "Module: 01.02.00 - Simulation Input Summary"
    ax.text(0.1, 0.1, module_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray')
    
    # Save as PDF
    output_file = output_dir / f"simulation_input_summary_01.02.00_{timestamp}.pdf"
    with PdfPages(output_file) as pdf:
        pdf.savefig(fig, dpi=300)
    
    plt.close()
    
    print(f"✅ Simulation Input Summary generated: {output_file}")
    return str(output_file)

def main():
    """Main function to generate Simulation Input Summary"""
    print("🎨 Generating Simulation Input Summary...")
    
    try:
        output_file = generate_simulation_input_summary()
        print(f"📄 Simulation Input Summary created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating Simulation Input Summary: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
