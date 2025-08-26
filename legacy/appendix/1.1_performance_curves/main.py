#!/usr/bin/env python3
"""
S1-Performance Curve Optimization - CRAC System Analysis
J1 - Michael Maloneys First Journal Paper

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Notes: This script is designed for PhD-level data analysis, ensuring high precision 
and reproducibility. Uses the centralized J1Plotting system for all styling and colors.

Script Title: Performance Curve Analysis - CRAC System Optimization
Name: Michael Logan Maloney
"""

import sys
from pathlib import Path
sys.path.append('/Users/michaelmaloney/Desktop/Michael Logan Maloney.Ph.D. Dissertation Notebook/MLM J1 - Michael Maloneys First Journal Paper/modules')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
try:
    from scipy.stats import linregress
except ImportError:
    def linregress(x, y):
        n = len(x)
        x_mean, y_mean = np.mean(x), np.mean(y)
        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sqrt(np.sum((x - x_mean)**2) * np.sum((y - y_mean)**2))
        r_value = numerator / denominator if denominator != 0 else 0
        return type('obj', (object,), {
            'slope': 0, 'intercept': 0, 'r_value': r_value, 'p_value': 0, 'std_err': 0
        })()
from crcs_plotting import J1AnalysisBase

class PerformanceCurveAnalyzer(J1AnalysisBase):
    """
    CRAC Performance Curve Analysis for SIMBUILD 2027.
    Uses the J1AnalysisBase for all plotting, style, and color configuration.
    """
    def __init__(self):
        super().__init__()
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Define performance curve coefficients from Modelica records
        # Curve_II (Main CRAC, labeled A)
        self.curve_ii_capFunFF = [0.8, 0.2, 0, 0]
        self.curve_ii_EIRFunFF = [1.1552, -0.1808, 0.0256, 0]
        self.curve_ii_ffMin = 0.5
        self.curve_ii_ffMax = 1.5
        
        # Curve_III (Supplemental CRACs, labeled B, B1, B2, B3, B4)
        self.curve_iii_capFunFF = [0.47278589, 1.2433415, -1.0387055, 0.32257813]
        self.curve_iii_EIRFunFF = [1.0079484, 0.34544129, -0.6922891, 0.33889943]
        self.curve_iii_ffMin = 0.5
        self.curve_iii_ffMax = 1.5
        
        # Define configurations
        self.configs = [
            {'label': 'Main only (A)', 'num_main': 1, 'num_supp': 0},
            {'label': 'Supplemental only (B series)', 'num_main': 0, 'num_supp': 1},
            {'label': 'A + B1 (1 Supp)', 'num_main': 1, 'num_supp': 1},
            {'label': 'A + B1 + B2 (2 Supp)', 'num_main': 1, 'num_supp': 2},
            {'label': 'A + B1 + B2 + B3 (3 Supp)', 'num_main': 1, 'num_supp': 3},
            {'label': 'A + B1 + B2 + B3 + B4 (4 Supp)', 'num_main': 1, 'num_supp': 4}
        ]
        
    def capFunFF(self, ff, coef):
        """Calculate capacity multiplier as function of flow fraction"""
        return coef[0] + coef[1]*ff + coef[2]*ff**2 + coef[3]*ff**3
    
    def EIRFunFF(self, ff, coef):
        """Calculate EIR multiplier as function of flow fraction"""
        return coef[0] + coef[1]*ff + coef[2]*ff**2 + coef[3]*ff**3
    
    def calculate_performance_curves(self):
        """Calculate performance curves for all configurations"""
        print("Calculating performance curves...")
        
        # Generate flow fraction range
        ff_range = np.linspace(min(self.curve_ii_ffMin, self.curve_iii_ffMin),
                              max(self.curve_ii_ffMax, self.curve_iii_ffMax), 50)
        
        # Precompute individual curves as NumPy arrays
        cap_ii = np.array([self.capFunFF(ff, self.curve_ii_capFunFF) for ff in ff_range])
        eir_ii = np.array([self.EIRFunFF(ff, self.curve_ii_EIRFunFF) for ff in ff_range])
        cap_iii = np.array([self.capFunFF(ff, self.curve_iii_capFunFF) for ff in ff_range])
        eir_iii = np.array([self.EIRFunFF(ff, self.curve_iii_EIRFunFF) for ff in ff_range])
        
        # Calculate overall statistics for summary
        avg_cap_ii = np.mean(cap_ii)
        avg_eir_ii = np.mean(eir_ii)
        avg_cap_iii = np.mean(cap_iii)
        avg_eir_iii = np.mean(eir_iii)
        ff_min = min(self.curve_ii_ffMin, self.curve_iii_ffMin)
        ff_max = max(self.curve_ii_ffMax, self.curve_iii_ffMax)
        num_ff_points = len(ff_range)
        
        print(f"   Flow fraction range: {ff_min:.1f} to {ff_max:.1f}")
        print(f"   Number of points: {num_ff_points}")
        print(f"   Main CRAC avg capacity: {avg_cap_ii:.3f}")
        print(f"   Main CRAC avg EIR: {avg_eir_ii:.3f}")
        print(f"   Supp CRAC avg capacity: {avg_cap_iii:.3f}")
        print(f"   Supp CRAC avg EIR: {avg_eir_iii:.3f}")
        
        return {
            'ff_range': ff_range,
            'cap_ii': cap_ii,
            'eir_ii': eir_ii,
            'cap_iii': cap_iii,
            'eir_iii': eir_iii,
            'avg_cap_ii': avg_cap_ii,
            'avg_eir_ii': avg_eir_ii,
            'avg_cap_iii': avg_cap_iii,
            'avg_eir_iii': avg_eir_iii,
            'ff_min': ff_min,
            'ff_max': ff_max,
            'num_ff_points': num_ff_points
        }
    
    def create_capacity_plot(self, config, curves_data, config_index):
        """Create capacity plot for a specific configuration - ONE PAGE"""
        print(f"Creating capacity plot for {config['label']}...")
        
        num_m = config['num_main']
        num_s = config['num_supp']
        label = config['label']
        
        if num_m + num_s == 0:
            return None
        
        # Compute system capacity multiplier
        cap_sys = (num_m * curves_data['cap_ii'] + num_s * curves_data['cap_iii']) / (num_m + num_s)
        
        # Create figure with full page layout
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Plot system capacity
        ax.plot(curves_data['ff_range'], cap_sys, label='System', 
               color=self.colors['system'], linewidth=2)
        
        # Plot individual components
        if num_m > 0:
            ax.plot(curves_data['ff_range'], curves_data['cap_ii'], label='Main CRAC (A)', 
                   color=self.colors['main_crac'], linewidth=2)
        if num_s > 0:
            ax.plot(curves_data['ff_range'], curves_data['cap_iii'], label='Supplemental CRAC (B)', 
                   color=self.colors['supp_crac'], linewidth=2)
        
        # Styling with professional positioning
        ax.set_xlabel('Flow Fraction')
        ax.set_ylabel('Capacity Multiplier')
        ax.set_title(f'Figure {config_index}: Cooling Capacity vs Flow Fraction', fontsize=16)
        
        # Grid and spines
        ax.grid(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Legend with professional positioning
        self.add_legend(ax)
        self.add_annotation(ax, '', (0.05, -0.2), (0.05, -0.2))
        
        # Add key values annotation
        idx_nom = np.argmin(np.abs(curves_data['ff_range'] - 1.0))
        nom_cap = cap_sys[idx_nom]
        
        self.add_annotation(ax, f'Nominal Point (FF=1.0):\nCapacity = {nom_cap:.3f}', 
                          (1.0, nom_cap), (1.1, nom_cap + 0.1))
        
        self.finalize_figure(fig, ax)
        
        # Save figure
        fig_path = self.output_dir / f"capacity_{config_index}_{config['label'].replace(' ', '_').replace('(', '').replace(')', '')}_{self.timestamp}.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return str(fig_path)
    
    def create_eir_plot(self, config, curves_data, config_index):
        """Create EIR plot for a specific configuration - ONE PAGE"""
        print(f"Creating EIR plot for {config['label']}...")
        
        num_m = config['num_main']
        num_s = config['num_supp']
        label = config['label']
        
        if num_m + num_s == 0:
            return None
        
        # Compute system EIR multiplier
        cap_sys = (num_m * curves_data['cap_ii'] + num_s * curves_data['cap_iii']) / (num_m + num_s)
        power_sys = (num_m * curves_data['cap_ii'] * curves_data['eir_ii']) + (num_s * curves_data['cap_iii'] * curves_data['eir_iii'])
        eir_sys = power_sys / (num_m * curves_data['cap_ii'] + num_s * curves_data['cap_iii'])
        
        # Create figure with full page layout
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Plot system EIR
        ax.plot(curves_data['ff_range'], eir_sys, label='System', 
               color=self.colors['system'], linewidth=3, marker='o', markersize=6)
        
        # Plot individual components
        if num_m > 0:
            ax.plot(curves_data['ff_range'], curves_data['eir_ii'], label='Main CRAC (A)', 
                   color=self.colors['main_crac'], linestyle='--', linewidth=2, marker='s', markersize=4)
        if num_s > 0:
            ax.plot(curves_data['ff_range'], curves_data['eir_iii'], label='Supplemental CRAC (B)', 
                   color=self.colors['supp_crac'], linestyle='--', linewidth=2, marker='^', markersize=4)
        
        # Styling with better text positioning
        ax.set_xlabel('Flow Fraction')
        ax.set_ylabel('EIR Multiplier')
        ax.set_title(f'Figure {config_index + 0.5}: EIR vs Flow Fraction\n{label}', fontsize=18, fontweight='bold')
        
        # Grid and spines
        ax.grid(True, alpha=0.3, color=self.colors['grid'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(self.colors['grid'])
        ax.spines['bottom'].set_color(self.colors['grid'])
        
        # Increase tick label sizes
        ax.tick_params(axis='both', which='major', labelsize=14)
        
        # Legend with better positioning and larger text
        self.add_legend(ax, loc='upper left', bbox_to_anchor=(0.02, 0.98))
        
        # Add key values annotation with better positioning
        idx_nom = np.argmin(np.abs(curves_data['ff_range'] - 1.0))
        nom_eir = eir_sys[idx_nom]
        
        # Position annotation to avoid overlap
        if nom_eir > 1.0:
            xytext_pos = (1.1, nom_eir + 0.08)
        else:
            xytext_pos = (1.1, nom_eir - 0.08)
            
        self.add_annotation(ax, f'Nominal Point (FF=1.0):\nEIR = {nom_eir:.3f}', 
                          (1.0, nom_eir), xytext_pos)
        
        self.finalize_figure(fig, ax)
        
        # Save figure
        fig_path = self.output_dir / f"eir_{config_index}_{config['label'].replace(' ', '_').replace('(', '').replace(')', '')}_{self.timestamp}.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return str(fig_path)
    
    def create_summary_table(self, curves_data):
        """Create comprehensive summary table - ONE PAGE"""
        print("Creating summary table...")
        
        fig, ax = plt.subplots(figsize=(12, 10))
        ax.axis('tight')
        ax.axis('off')
        
        # Prepare table data
        table_data = [
            ['Metric', 'Value', 'Units', 'Status'],
            ['Flow Fraction Range', f"{curves_data['ff_min']:.1f} - {curves_data['ff_max']:.1f}", 'dimensionless', 'Defined'],
            ['Number of FF Points', f"{curves_data['num_ff_points']}", 'points', 'Calculated'],
            ['Configurations Analyzed', f"{len(self.configs)}", 'configs', 'Complete'],
            ['', '', '', ''],
            ['Main CRAC (A) Statistics', '', '', ''],
            ['Avg Capacity Multiplier', f"{curves_data['avg_cap_ii']:.3f}", 'dimensionless', 'Calculated'],
            ['Avg EIR Multiplier', f"{curves_data['avg_eir_ii']:.3f}", 'dimensionless', 'Calculated'],
            ['Capacity Coefficients', f"{self.curve_ii_capFunFF}", 'array', 'Defined'],
            ['EIR Coefficients', f"{self.curve_ii_EIRFunFF}", 'array', 'Defined'],
            ['', '', '', ''],
            ['Supplemental CRAC (B) Statistics', '', '', ''],
            ['Avg Capacity Multiplier', f"{curves_data['avg_cap_iii']:.3f}", 'dimensionless', 'Calculated'],
            ['Avg EIR Multiplier', f"{curves_data['avg_eir_iii']:.3f}", 'dimensionless', 'Calculated'],
            ['Capacity Coefficients', f"{self.curve_iii_capFunFF}", 'array', 'Defined'],
            ['EIR Coefficients', f"{self.curve_iii_EIRFunFF}", 'array', 'Defined'],
            ['', '', '', ''],
            ['Analysis Parameters', '', '', ''],
            ['Assumptions', 'Equal nominal capacities', 'text', 'Defined'],
            ['Uniform FF', 'Across all units', 'text', 'Applied'],
            ['Implications', 'Staged configs blend linearity', 'text', 'Observed'],
            ['Modelica Integration', 'Ready for simulation', 'text', 'Prepared']
        ]
        
        # Create table with better styling
        table = ax.table(cellText=table_data, cellLoc='left', loc='center',
                        colWidths=[0.25, 0.35, 0.15, 0.25])
        
        # Style the table with larger fonts
        table.auto_set_font_size(False)
        table.set_fontsize(13)
        table.scale(1, 2.2)
        
        # Apply professional table styling
        self.style_table(table, header_rows=(0,), section_rows=(4, 11, 17), alt_row_start=1)
        
        ax.set_title('CRAC Performance Curve Analysis Summary\nSIMBUILD 2027 Conference Paper', 
                    fontsize=18, fontweight='bold', pad=30)
        
        self.finalize_figure(fig, ax)
        
        # Save table
        table_path = self.output_dir / f"summary_table_{self.timestamp}.png"
        plt.savefig(table_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return str(table_path)
    
    def generate_performance_report(self):
        """Generate comprehensive performance analysis report with one page per figure"""
        print("Generating Performance Curve Analysis Report...")
        
        # Calculate performance curves
        curves_data = self.calculate_performance_curves()
        
        # Create all visualizations
        fig_paths = {
            'summary_table': self.create_summary_table(curves_data)
        }
        
        # Generate configuration plots - ONE PAGE PER FIGURE
        for i, config in enumerate(self.configs):
            # Capacity plot
            cap_path = self.create_capacity_plot(config, curves_data, i)
            if cap_path:
                fig_paths[f'capacity_{i}'] = cap_path
            
            # EIR plot
            eir_path = self.create_eir_plot(config, curves_data, i)
            if eir_path:
                fig_paths[f'eir_{i}'] = eir_path
        
        # Generate PDF report with one page per figure
        report_path = self.output_dir / f"performance_curves_1.1_{self.timestamp}.pdf"
        
        with PdfPages(report_path) as pdf:
            # Title page
            fig = plt.figure(figsize=(12, 10))
            plt.axis('off')
            
            plt.text(0.5, 0.8, 'CRAC Performance Curve Analysis Report', 
                    fontsize=24, weight='bold', ha='center', va='center')
            plt.text(0.5, 0.7, 'SIMBUILD 2027 Conference Paper - Submodule 1.1', 
                    fontsize=18, ha='center', va='center')
            plt.text(0.5, 0.6, 'Performance Curve Optimization Figure', 
                    fontsize=16, ha='center', va='center')
            plt.text(0.5, 0.5, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 
                    fontsize=14, ha='center', va='center')
            plt.text(0.5, 0.4, 'Author: Michael Maloney', 
                    fontsize=12, ha='center', va='center')
            plt.text(0.5, 0.3, 'Penn State Architectural Engineering Department', 
                    fontsize=12, ha='center', va='center')
            
            pdf.savefig(fig, facecolor='white')
            plt.close(fig)
            
            # Summary statistics page
            fig, ax = plt.subplots(figsize=(12, 10))
            ax.axis('tight')
            ax.axis('off')
            
            summary_text = (
                f"Analysis Summary\n\n"
                f"Flow Fraction Range: {curves_data['ff_min']:.1f} to {curves_data['ff_max']:.1f}\n"
                f"Number of FF Points: {curves_data['num_ff_points']}\n"
                f"Configurations Analyzed: {len(self.configs)}\n\n"
                f"Main CRAC (A) Statistics:\n"
                f"  Avg Capacity Multiplier: {curves_data['avg_cap_ii']:.3f}\n"
                f"  Avg EIR Multiplier: {curves_data['avg_eir_ii']:.3f}\n\n"
                f"Supplemental CRAC (B) Statistics:\n"
                f"  Avg Capacity Multiplier: {curves_data['avg_cap_iii']:.3f}\n"
                f"  Avg EIR Multiplier: {curves_data['avg_eir_iii']:.3f}\n\n"
                f"Analysis Parameters:\n"
                f"  Assumptions: Equal nominal capacities; uniform FF across units\n"
                f"  Implications: Staged configs blend linearity; useful for Modelica sims\n\n"
                f"Report Structure:\n"
                f"  - One page per figure for optimal readability\n"
                f"  - Separate capacity and EIR plots for each configuration\n"
                f"  - Clean Arial fonts with black text\n"
                f"  - Mathematical precision in all visualizations"
            )
            
            plt.text(0.1, 0.9, summary_text, fontsize=12, va='top', 
                    transform=ax.transAxes)
            
            ax.set_title('CRAC Performance Curve Analysis Summary', fontsize=16, weight='bold', pad=20)
            
            pdf.savefig(fig, facecolor='white')
            plt.close(fig)
        
        print(f"   Saved: {report_path}")
        return str(report_path) 