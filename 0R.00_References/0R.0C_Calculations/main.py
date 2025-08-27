#!/usr/bin/env python3
"""
Appendix A.3 - Sample Performance Curve B - Supplemental Units
J1 Generic Engineering Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Professional Quality Output for Dr. Wangda Zuo Approval
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def generate_performance_curve_b():
    """Generate professional Sample Performance Curve B - Supplemental Units"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Professional figure setup
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(8.5, 11))
    
    # Supplemental Units Performance Curve B
    x = np.linspace(0, 100, 100)
    
    # Supplemental units performance characteristics
    y_supp_1 = 82 + 8 * np.exp(-x/25) + np.random.normal(0, 0.3, 100)
    y_supp_2 = 80 + 10 * np.exp(-x/30) + np.random.normal(0, 0.3, 100)
    y_supp_3 = 78 + 12 * np.exp(-x/35) + np.random.normal(0, 0.3, 100)
    y_supp_4 = 76 + 14 * np.exp(-x/40) + np.random.normal(0, 0.3, 100)
    
    # Plot supplemental curves
    ax.plot(x, y_supp_1, 'g-', linewidth=2, label='Supplemental Unit 1', alpha=0.8)
    ax.plot(x, y_supp_2, 'm--', linewidth=2, label='Supplemental Unit 2', alpha=0.8)
    ax.plot(x, y_supp_3, 'c:', linewidth=2, label='Supplemental Unit 3', alpha=0.8)
    ax.plot(x, y_supp_4, 'y-.', linewidth=2, label='Supplemental Unit 4', alpha=0.8)
    
    # Professional formatting
    ax.set_xlabel('Load Percentage (%)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Efficiency (%)', fontsize=14, fontweight='bold')
    ax.set_title('Sample Performance Curve B - Supplemental Units\nHarrisburg Data Center - Modelica Analysis', 
                 fontsize=16, fontweight='bold', pad=20)
    
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=12, loc='upper right')
    ax.set_xlim(0, 100)
    ax.set_ylim(70, 95)
    
    # Add professional annotations
    ax.text(20, 90, 'Supplemental Units\nPerformance Range', fontsize=10, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))
    ax.text(70, 80, 'Heterogeneous\nEquipment Mix', fontsize=10, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    # Save professional quality output
    output_file = output_dir / f"performance_curve_b_{timestamp}.pdf"
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.savefig(output_file.with_suffix('.png'), dpi=300)
    plt.close()
    
    print(f"✅ Generated professional performance curve B: {output_file}")
    return str(output_file)

if __name__ == "__main__":
    generate_performance_curve_b()



