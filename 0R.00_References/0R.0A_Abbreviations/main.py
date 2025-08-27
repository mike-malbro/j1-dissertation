#!/usr/bin/env python3
"""
0R.0A - Abbreviations
Abbreviations module for the J1 PhD Dissertation
Advanced Data Center Thermodynamic Modeling Framework
"""

import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import warnings
warnings.filterwarnings('ignore')

def generate_abbreviations():
    """Generate comprehensive abbreviations for the J1 PhD Dissertation"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
    ax.axis('off')
    
    # Force the figure to be exactly 8.5 x 11 inches
    fig.set_size_inches(8.5, 11)
    fig.set_dpi(300)
    
    # Remove all margins to use full page
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    
    # Title
    title_text = "Abbreviations and Acronyms"
    ax.text(0.5, 0.95, title_text, fontsize=20, fontweight='bold',
            ha='center', va='center', fontfamily='Arial', color='black', transform=ax.transAxes)
    
    # Subtitle
    subtitle_text = "J1 PhD Dissertation - Advanced Data Center Thermodynamic Modeling Framework"
    ax.text(0.5, 0.91, subtitle_text, fontsize=12, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black', transform=ax.transAxes)
    
    # Abbreviations content
    abbreviations = [
        "AC - Air Conditioning",
        "ACH - Air Changes per Hour",
        "ASHRAE - American Society of Heating, Refrigerating and Air-Conditioning Engineers",
        "CFD - Computational Fluid Dynamics",
        "CFM - Cubic Feet per Minute",
        "COP - Coefficient of Performance",
        "CRAC - Computer Room Air Conditioning",
        "CRAH - Computer Room Air Handler",
        "DC - Data Center",
        "DX - Direct Expansion",
        "EER - Energy Efficiency Ratio",
        "EPA - Environmental Protection Agency",
        "FCU - Fan Coil Unit",
        "GPM - Gallons Per Minute",
        "HFC - Hydrofluorocarbon",
        "HP - Horsepower",
        "HSPF - Heating Seasonal Performance Factor",
        "HVAC - Heating, Ventilation, and Air Conditioning",
        "IT - Information Technology",
        "kW - Kilowatt",
        "kWh - Kilowatt-hour",
        "LBNL - Lawrence Berkeley National Laboratory",
        "MBH - Thousand British Thermal Units per Hour",
        "NIST - National Institute of Standards and Technology",
        "PUE - Power Usage Effectiveness",
        "RAC - Room Air Conditioning",
        "RPM - Revolutions Per Minute",
        "SEER - Seasonal Energy Efficiency Ratio",
        "SLA - Service Level Agreement",
        "TCO - Total Cost of Ownership",
        "UPS - Uninterruptible Power Supply",
        "VAV - Variable Air Volume",
        "VFD - Variable Frequency Drive",
        "W - Watt",
        "W/m² - Watts per Square Meter",
        "°C - Degrees Celsius",
        "°F - Degrees Fahrenheit",
        "% - Percent",
        "ΔT - Temperature Difference",
        "η - Efficiency",
        "ρ - Density",
        "μ - Dynamic Viscosity",
        "ν - Kinematic Viscosity"
    ]
    
    # Position abbreviations in two columns
    y_start = 0.86
    line_height = 0.027
    col_width = 0.4
    left_margin = 0.06
    
    for i, abbr in enumerate(abbreviations):
        y_pos = y_start - (i * line_height)
        if y_pos < 0.05:  # Don't go below page margin
            break
            
        # Determine column (left or right)
        if i < len(abbreviations) // 2:
            x_pos = left_margin
        else:
            x_pos = left_margin + col_width
            
        ax.text(x_pos, y_pos, abbr, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='black', transform=ax.transAxes)
    
    # Page number
    ax.text(0.5, 0.05, "1", fontsize=14, fontweight='normal',
            ha='center', va='center', fontfamily='Arial', color='black', transform=ax.transAxes)
    
    # Timestamp
    timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ax.text(0.06, 0.03, timestamp_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray', transform=ax.transAxes)
    
    # Module identifier
    module_text = "Module: 0R.0A - Abbreviations"
    ax.text(0.06, 0.01, module_text, fontsize=10, fontweight='normal',
            ha='left', va='center', fontfamily='Arial', color='gray', transform=ax.transAxes)
    
    # Save as PDF
    output_file = output_dir / f"abbreviations_0R.0A_{timestamp}.pdf"
    with PdfPages(output_file) as pdf:
        pdf.savefig(fig, dpi=300)
    
    plt.close()
    
    print(f"✅ Abbreviations generated: {output_file}")
    return str(output_file)

def main():
    """Main function to generate abbreviations"""
    print("📝 Generating Abbreviations...")
    
    try:
        output_file = generate_abbreviations()
        print(f"📄 Abbreviations created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating abbreviations: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
