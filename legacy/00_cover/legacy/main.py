#!/usr/bin/env python3
"""
Module 0: Cover Page
J1 - Data Center Thermodynamic Modeling Tool

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

This module generates a professional cover page for the J1 system.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from pathlib import Path
import numpy as np
import warnings
import sys
import os
warnings.filterwarnings('ignore')

# Add the parent directory to the path to find modules
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from modules.j1_plotting import J1AnalysisBase
except ImportError:
    # Fallback if modules not available
    class J1AnalysisBase:
        def __init__(self):
            self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            self.style = 'default'

class CoverPageGenerator(J1AnalysisBase):
    """
    Cover Page Generator for J1 System.
Uses the J1AnalysisBase for all plotting, style, and color configuration.
    """
    def __init__(self):
        super().__init__()
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.data_center_specs = {
            "name": "Harrisburg Data Center",
            "location": "Harrisburg, PA",
            "dimensions": {
                "white_space": {"length": 34, "width": 44, "height": 7},
                "ceiling_height": 7
            },
            "layout": {
                "rows": 4,
                "servers": 44,
                "crac_units": {
                    "main": 1,
                    "supplemental": 4
                }
            }
        }
        self.modules_included = [
            "Module 0 - Cover Page",
            "Module 1 - Conference Paper 1 SIMBUILD 2027",
            "  Submodule 1.0A - Abstract",
            "  Submodule 1.0B - Graphical Abstract",
            "  Submodule 1.1 - Performance Curve Optimization Figure",
            "Appendix - Background Materials"
        ]
    
    def create_data_center_visualization(self, ax):
        """Create a clean data center layout visualization"""
        # Data center outline
        dc_rect = patches.Rectangle((0.1, 0.1), 0.8, 0.6, 
                                  linewidth=2, edgecolor='black', 
                                  facecolor='white')
        ax.add_patch(dc_rect)
        
        # CRAC units (top)
        crac_width = 0.15
        crac_height = 0.08
        crac_y = 0.75
        
        # Main CRAC (black)
        main_crac = patches.Rectangle((0.35, crac_y), crac_width, crac_height,
                                    linewidth=2, edgecolor='black',
                                    facecolor='black', alpha=0.8)
        ax.add_patch(main_crac)
        ax.text(0.425, crac_y + 0.04, 'Main\nCRAC', ha='center', va='center', 
               fontsize=8, weight='bold', color='white', fontfamily='Arial')
        
        # Supplemental CRACs (gray)
        for i in range(4):
            x_pos = 0.1 + i * 0.2
            supp_crac = patches.Rectangle((x_pos, crac_y), crac_width, crac_height,
                                        linewidth=1, edgecolor='black',
                                        facecolor='#666666', alpha=0.7)
            ax.add_patch(supp_crac)
            ax.text(x_pos + 0.075, crac_y + 0.04, f'Supp\n{i+1}', ha='center', va='center',
                   fontsize=7, weight='bold', color='white', fontfamily='Arial')
        
        # Server racks (rows) - clean grid
        rack_width = 0.12
        rack_height = 0.08
        for row in range(4):
            y_pos = 0.55 - row * 0.12
            for col in range(11):
                x_pos = 0.12 + col * 0.07
                rack = patches.Rectangle((x_pos, y_pos), rack_width, rack_height,
                                       linewidth=0.5, edgecolor='black',
                                       facecolor='white', alpha=1.0)
                ax.add_patch(rack)
        
        # Labels
        ax.text(0.5, 0.85, 'Data Center Layout', ha='center', va='center',
               fontsize=12, weight='bold', color='black', fontfamily='Arial')
        ax.text(0.5, 0.02, '44 Servers | 4 Rows | 5 CRAC Units', ha='center', va='center',
               fontsize=10, color='black', fontfamily='Arial')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    
    def create_performance_chart(self, ax):
        """Create a clean performance visualization"""
        # Mathematical performance curves
        x = np.linspace(0.5, 1.5, 20)
        y1 = 0.8 + 0.2 * x  # Main CRAC: linear relationship
        y2 = 0.9 + 0.1 * x + 0.05 * x**2  # Supplemental CRACs: quadratic relationship
        
        ax.plot(x, y1, color='black', linewidth=2.5, 
               label='Main CRAC', marker='o', markersize=4, markeredgecolor='black')
        ax.plot(x, y2, color='#666666', linewidth=2.5,
               label='Supplemental CRACs', marker='s', markersize=4, markeredgecolor='black')
        
        ax.set_xlabel('Flow Fraction', fontsize=10, color='black', fontfamily='Arial')
        ax.set_ylabel('Capacity Multiplier', fontsize=10, color='black', fontfamily='Arial')
        ax.set_title('CRAC Performance Curves', fontsize=12, weight='bold', 
                    color='black', fontfamily='Arial')
        ax.legend(fontsize=8, framealpha=1.0, edgecolor='black', prop={'family': 'Arial'})
        ax.grid(True, alpha=0.3, color='black')
        ax.set_facecolor('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('black')
        ax.spines['bottom'].set_color('black')
    
    def generate_cover_page(self) -> str:
        """Generate professional cover page with clean mathematical layout"""
        print("Generating cover page...")
        
        # Create figure with clean layout
        fig = plt.figure(figsize=(12, 16))
        fig.patch.set_facecolor('white')
        
        # Main title area
        ax_title = plt.axes([0.1, 0.85, 0.8, 0.12])
        ax_title.axis('off')
        
        # Main title with mathematical notation
        ax_title.text(0.5, 0.8, 'J1', 
                     fontsize=36, weight='bold', ha='center', va='center',
                     color='black', fontfamily='Arial')
        ax_title.text(0.5, 0.6, 'Computer Room Cooling System to the n', 
                     fontsize=18, ha='center', va='center',
                     color='black', fontfamily='Arial')
        ax_title.text(0.5, 0.4, 'Multi-System Modeling of Data Center Cooling', 
                     fontsize=16, ha='center', va='center',
                     color='black', fontfamily='Arial')
        ax_title.text(0.5, 0.2, 'Optimizing Control of Five CRAC Units for Energy Efficiency and Runtime in Harrisburg', 
                     fontsize=14, ha='center', va='center',
                     color='black', fontfamily='Arial')
        
        # Author information
        ax_author = plt.axes([0.1, 0.75, 0.8, 0.08])
        ax_author.axis('off')
        
        ax_author.text(0.5, 0.7, 'Author: Michael Maloney', 
                      fontsize=16, weight='bold', ha='center', va='center',
                      color='black', fontfamily='Arial')
        ax_author.text(0.5, 0.4, 'PhD Student - Penn State Architectural Engineering Department', 
                      fontsize=14, ha='center', va='center',
                      color='black', fontfamily='Arial')
        ax_author.text(0.5, 0.1, 'Mechanical System Focus | SIMBUILD 2027 Conference Paper', 
                      fontsize=12, ha='center', va='center',
                      color='black', fontfamily='Arial')
        
        # Data center visualization
        ax_dc = plt.axes([0.05, 0.45, 0.4, 0.25])
        self.create_data_center_visualization(ax_dc)
        
        # Performance chart
        ax_perf = plt.axes([0.55, 0.45, 0.4, 0.25])
        self.create_performance_chart(ax_perf)
        
        # Specifications with mathematical notation
        ax_specs = plt.axes([0.1, 0.25, 0.8, 0.15])
        ax_specs.axis('off')
        
        # Create a clean box for specifications
        specs_box = patches.FancyBboxPatch((0.02, 0.1), 0.96, 0.8,
                                          boxstyle="round,pad=0.02",
                                          facecolor='white',
                                          edgecolor='black',
                                          linewidth=1.5)
        ax_specs.add_patch(specs_box)
        
        ax_specs.text(0.5, 0.9, 'Data Center Specifications', 
                     fontsize=14, weight='bold', ha='center', va='center',
                     color='black', fontfamily='Arial')
        
        specs_text = (
            f"Facility: {self.data_center_specs['name']} | "
            f"Location: {self.data_center_specs['location']}\n"
            f"White Space: {self.data_center_specs['dimensions']['white_space']['length']}' × "
            f"{self.data_center_specs['dimensions']['white_space']['width']}' × "
            f"{self.data_center_specs['dimensions']['white_space']['height']}' | "
            f"Layout: {self.data_center_specs['layout']['rows']} rows, {self.data_center_specs['layout']['servers']} servers\n"
            f"CRAC Units: {self.data_center_specs['layout']['crac_units']['main']} main + "
            f"{self.data_center_specs['layout']['crac_units']['supplemental']} supplemental | "
            f"System Type: 2N · 1 MW | Energy Savings: 15% vs conventional control"
        )
        
        ax_specs.text(0.5, 0.6, specs_text, 
                     fontsize=11, ha='center', va='center',
                     color='black', fontfamily='Arial')
        
        # Modules included
        ax_modules = plt.axes([0.1, 0.08, 0.8, 0.12])
        ax_modules.axis('off')
        
        # Create a clean box for modules
        modules_box = patches.FancyBboxPatch((0.02, 0.1), 0.96, 0.8,
                                            boxstyle="round,pad=0.02",
                                            facecolor='white',
                                            edgecolor='black',
                                            linewidth=1.5)
        ax_modules.add_patch(modules_box)
        
        ax_modules.text(0.5, 0.9, 'Study Contents', 
                       fontsize=14, weight='bold', ha='center', va='center',
                       color='black', fontfamily='Arial')
        
        modules_text = ' | '.join([m.replace('Module ', '').replace('Submodule ', '') for m in self.modules_included])
        ax_modules.text(0.5, 0.5, modules_text, 
                       fontsize=10, ha='center', va='center',
                       color='black', fontfamily='Arial')
        
        # Generation timestamp
        ax_timestamp = plt.axes([0.1, 0.02, 0.8, 0.04])
        ax_timestamp.axis('off')
        ax_timestamp.text(0.5, 0.5, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | J1 v1.0.0', 
                         fontsize=10, ha='center', va='center',
                         color='black', fontfamily='Arial')
        
        # Save as PNG
        png_path = self.output_dir / f"cover_page_{self.timestamp}.png"
        plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        # Generate PDF report
        pdf_path = self.output_dir / f"cover_page_{self.timestamp}.pdf"
        
        with PdfPages(pdf_path) as pdf:
            # Recreate the cover page for PDF
            fig = plt.figure(figsize=(12, 16))
            fig.patch.set_facecolor('white')
            
            # Main title area
            ax_title = plt.axes([0.1, 0.85, 0.8, 0.12])
            ax_title.axis('off')
            
            # Main title
            ax_title.text(0.5, 0.8, 'J1', 
                         fontsize=36, weight='bold', ha='center', va='center',
                         color='black', fontfamily='Arial')
            ax_title.text(0.5, 0.6, 'Computer Room Cooling System to the n', 
                         fontsize=18, ha='center', va='center',
                         color='black', fontfamily='Arial')
            ax_title.text(0.5, 0.4, 'Multi-System Modeling of Data Center Cooling', 
                         fontsize=16, ha='center', va='center',
                         color='black', fontfamily='Arial')
            ax_title.text(0.5, 0.2, 'Optimizing Control of Five CRAC Units for Energy Efficiency and Runtime in Harrisburg', 
                         fontsize=14, ha='center', va='center',
                         color='black', fontfamily='Arial')
            
            # Author information
            ax_author = plt.axes([0.1, 0.75, 0.8, 0.08])
            ax_author.axis('off')
            
            ax_author.text(0.5, 0.7, 'Author: Michael Maloney', 
                          fontsize=16, weight='bold', ha='center', va='center',
                          color='black', fontfamily='Arial')
            ax_author.text(0.5, 0.4, 'PhD Student - Penn State Architectural Engineering Department', 
                          fontsize=14, ha='center', va='center',
                          color='black', fontfamily='Arial')
            ax_author.text(0.5, 0.1, 'Mechanical System Focus | SIMBUILD 2027 Conference Paper', 
                          fontsize=12, ha='center', va='center',
                          color='black', fontfamily='Arial')
            
            # Data center visualization
            ax_dc = plt.axes([0.05, 0.45, 0.4, 0.25])
            self.create_data_center_visualization(ax_dc)
            
            # Performance chart
            ax_perf = plt.axes([0.55, 0.45, 0.4, 0.25])
            self.create_performance_chart(ax_perf)
            
            # Specifications
            ax_specs = plt.axes([0.1, 0.25, 0.8, 0.15])
            ax_specs.axis('off')
            
            # Create a clean box for specifications
            specs_box = patches.FancyBboxPatch((0.02, 0.1), 0.96, 0.8,
                                              boxstyle="round,pad=0.02",
                                              facecolor='white',
                                              edgecolor='black',
                                              linewidth=1.5)
            ax_specs.add_patch(specs_box)
            
            ax_specs.text(0.5, 0.9, 'Data Center Specifications', 
                         fontsize=14, weight='bold', ha='center', va='center',
                         color='black', fontfamily='Arial')
            
            specs_text = (
                f"Facility: {self.data_center_specs['name']} | "
                f"Location: {self.data_center_specs['location']}\n"
                f"White Space: {self.data_center_specs['dimensions']['white_space']['length']}' × "
                f"{self.data_center_specs['dimensions']['white_space']['width']}' × "
                f"{self.data_center_specs['dimensions']['white_space']['height']}' | "
                f"Layout: {self.data_center_specs['layout']['rows']} rows, {self.data_center_specs['layout']['servers']} servers\n"
                f"CRAC Units: {self.data_center_specs['layout']['crac_units']['main']} main + "
                f"{self.data_center_specs['layout']['crac_units']['supplemental']} supplemental | "
                f"System Type: 2N · 1 MW | Energy Savings: 15% vs conventional control"
            )
            
            ax_specs.text(0.5, 0.6, specs_text, 
                         fontsize=11, ha='center', va='center',
                         color='black', fontfamily='Arial')
            
            # Modules included
            ax_modules = plt.axes([0.1, 0.08, 0.8, 0.12])
            ax_modules.axis('off')
            
            # Create a clean box for modules
            modules_box = patches.FancyBboxPatch((0.02, 0.1), 0.96, 0.8,
                                                boxstyle="round,pad=0.02",
                                                facecolor='white',
                                                edgecolor='black',
                                                linewidth=1.5)
            ax_modules.add_patch(modules_box)
            
            ax_modules.text(0.5, 0.9, 'Study Contents', 
                           fontsize=14, weight='bold', ha='center', va='center',
                           color='black', fontfamily='Arial')
            
            modules_text = ' | '.join([m.replace('Module ', '').replace('Submodule ', '') for m in self.modules_included])
            ax_modules.text(0.5, 0.5, modules_text, 
                           fontsize=10, ha='center', va='center',
                           color='black', fontfamily='Arial')
            
            # Generation timestamp
            ax_timestamp = plt.axes([0.1, 0.02, 0.8, 0.04])
            ax_timestamp.axis('off')
            ax_timestamp.text(0.5, 0.5, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | J1 v1.0.0', 
                             fontsize=10, ha='center', va='center',
                             color='black', fontfamily='Arial')
            
            pdf.savefig(fig, facecolor='white')
            plt.close(fig)
        
        print(f"   Saved: {pdf_path}")
        return str(pdf_path) 