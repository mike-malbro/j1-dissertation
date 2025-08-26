#!/usr/bin/env python3
"""
S4-Energy Bill Analysis - Data Center Energy Consumption
J1 - Michael Maloneys First Journal Paper

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Notes: This script is designed for PhD-level data analysis, ensuring high precision 
and reproducibility. Legends are placed at the bottom right below the x-axis to avoid 
chart interference, and annotations (e.g., correlation, averages) are positioned at 
the bottom left. This serves as a template for future analyses.

Script Title: Energy Bill Analysis - Meter Doubling Anomaly Investigation
Name: Michael Logan Maloney
"""

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
from modules.j1_plotting import J1AnalysisBase

class EnergyBillAnalyzer(J1AnalysisBase):
    """
    Energy Bill Analysis for Data Center Operations.
    Uses the J1AnalysisBase for all plotting, style, and color configuration.
    """
    def __init__(self):
        super().__init__()
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Energy bill data with meter doubling anomaly
        self.energy_data = {
            'Date': [
                '01/2022', '02/2022', '03/2022', '04/2022', '05/2022', '06/2022',
                '07/2022', '08/2022', '09/2022', '10/2022', '11/2022', '12/2022',
                '01/2023', '02/2023', '03/2023', '04/2023', '05/2023', '06/2023',
                '07/2023', '08/2023', '09/2023', '10/2023', '11/2023', '12/2023',
                '01/2024', '02/2024', '03/2024', '04/2024', '05/2024', '06/2024',
                '07/2024', '08/2024', '09/2024', '10/2024', '11/2024', '12/2024',
                '01/2025', '02/2025', '03/2025', '04/2025'
            ],
            'Metered_Reading': [
                36268, 31214, 34416, 32210, 36657, 36273, 37315, 39895, 34778, 34501, 33630, 33247,
                34728, 33544, 33570, 31679, 37452, 37637, 34578, 41218, 32690, 37111, 34481, 32583,
                39011, 33655, 33700, 36673, 36162, 30658, 43625, 39850, 30539, 31097, 31240, 30222,
                34474, 30479, 34151, 31907
            ],
            'Solar_Assumption': [
                36268, 31214, 34416, 32210, 36657, 36273, 37315, 39895, 34778, 34501, 33630, 33247,
                34728, 33544, 33570, 31679, 37452, 37637, 34578, 41218, 32690, 37111, 34481, 32583,
                39011, 33655, 33700, 36673, 36162, 30658, 43625, 39850, 30539, 31097, 31240, 30222,
                34474, 30479, 34151, 31907
            ],
            'Rate_per_kWh': [0.1] * 40
        }
        self.df = pd.DataFrame(self.energy_data)
        self.df['Solar_Assumption_x2'] = self.df['Solar_Assumption'] * 2
        self.df['Total_kWh'] = self.df['Metered_Reading'] + self.df['Solar_Assumption_x2']
        self.df['Total_Cost'] = self.df['Total_kWh'] * self.df['Rate_per_kWh']
        self.df['Date_parsed'] = pd.to_datetime(self.df['Date'], format='%m/%Y')
        self.df['Year'] = self.df['Date_parsed'].dt.year
        self.df['Month'] = self.df['Date_parsed'].dt.month
        self.df['Quarter'] = self.df['Date_parsed'].dt.quarter

    def analyze_energy_consumption(self):
        """Energy consumption analysis"""
        print("Analyzing Energy Consumption Patterns...")
        
        # Statistical analysis
        stats = {
            'Total_Consumption_kWh': self.df['Total_kWh'].sum(),
            'Average_Monthly_kWh': self.df['Total_kWh'].mean(),
            'Peak_Monthly_kWh': self.df['Total_kWh'].max(),
            'Min_Monthly_kWh': self.df['Total_kWh'].min(),
            'Std_Dev_kWh': self.df['Total_kWh'].std(),
            'Total_Cost': self.df['Total_Cost'].sum(),
            'Average_Monthly_Cost': self.df['Total_Cost'].mean(),
            'Meter_Doubling_Impact': (self.df['Solar_Assumption_x2'].sum() / self.df['Total_kWh'].sum()) * 100
        }
        
        print(f"   Total Consumption: {stats['Total_Consumption_kWh']:,.0f} kWh")
        print(f"   Average Monthly: {stats['Average_Monthly_kWh']:,.0f} kWh")
        print(f"   Total Cost: ${stats['Total_Cost']:,.2f}")
        print(f"   Meter Doubling Impact: {stats['Meter_Doubling_Impact']:.1f}%")
        
        return stats
    
    def create_energy_consumption_trends(self):
        """Create energy consumption trend analysis"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Harrisburg Data Center Energy Consumption Analysis\nMeter Doubling Anomaly Investigation', 
                     fontsize=16, fontweight='bold', y=0.98)
        
        # Figure 1: Monthly Energy Consumption Breakdown
        ax1 = axes[0, 0]
        x = range(len(self.df))
        width = 0.35
        
        ax1.bar(x, self.df['Metered_Reading'], width, label='Metered Reading', 
                color=self.colors['metered'], alpha=0.8)
        ax1.bar(x, self.df['Solar_Assumption_x2'], width, bottom=self.df['Metered_Reading'], 
                label='Solar Assumption × 2', color=self.colors['solar'], alpha=0.8)
        
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Energy Consumption (kWh)')
        ax1.set_title('Monthly Energy Consumption Breakdown')
        ax1.legend(loc='upper right', bbox_to_anchor=(1, 1))
        ax1.grid(True, alpha=0.3)
        
        # Set x-axis labels for every 6 months
        ax1.set_xticks(range(0, len(self.df), 6))
        ax1.set_xticklabels([self.df['Date'].iloc[i] for i in range(0, len(self.df), 6)], rotation=45)
        
        # Figure 2: Total Monthly Consumption Trend
        ax2 = axes[0, 1]
        ax2.plot(range(len(self.df)), self.df['Total_kWh'], 
                color=self.colors['total'], linewidth=2, marker='o', markersize=4)
        ax2.axhline(y=self.df['Total_kWh'].mean(), color=self.colors['mean_line'], 
                   linestyle='--', alpha=0.7, label=f'Average: {self.df["Total_kWh"].mean():,.0f} kWh')
        
        ax2.set_xlabel('Month')
        ax2.set_ylabel('Total Energy Consumption (kWh)')
        ax2.set_title('Total Monthly Energy Consumption Trend')
        ax2.legend(loc='lower right', bbox_to_anchor=(1.0, -0.2), ncol=1)
        ax2.grid(False)
        ax2.text(0.05, -0.2, '', transform=ax2.transAxes, fontsize=10)
        
        # Set x-axis labels
        ax2.set_xticks(range(0, len(self.df), 6))
        ax2.set_xticklabels([self.df['Date'].iloc[i] for i in range(0, len(self.df), 6)], rotation=45)
        
        # Figure 3: Monthly Cost Analysis
        ax3 = axes[1, 0]
        bars = ax3.bar(range(len(self.df)), self.df['Total_Cost'], 
                      color=self.colors['cost'], alpha=0.8)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 50,
                    f'${height:,.0f}', ha='center', va='bottom', fontsize=8, rotation=90)
        
        ax3.set_xlabel('Month')
        ax3.set_ylabel('Monthly Cost ($)')
        ax3.set_title('Monthly Energy Cost Analysis')
        ax3.grid(False)
        
        # Set x-axis labels
        ax3.set_xticks(range(0, len(self.df), 6))
        ax3.set_xticklabels([self.df['Date'].iloc[i] for i in range(0, len(self.df), 6)], rotation=45)
        
        # Figure 4: Meter Doubling Impact Analysis
        ax4 = axes[1, 1]
        metered_pct = (self.df['Metered_Reading'] / self.df['Total_kWh']) * 100
        solar_pct = (self.df['Solar_Assumption_x2'] / self.df['Total_kWh']) * 100
        
        ax4.plot(range(len(self.df)), metered_pct, 
                color=self.colors['metered'], linewidth=2, marker='o', 
                markersize=4, label='Metered Reading %')
        ax4.plot(range(len(self.df)), solar_pct, 
                color=self.colors['solar'], linewidth=2, marker='s', 
                markersize=4, label='Solar Assumption × 2 %')
        
        ax4.set_xlabel('Month')
        ax4.set_ylabel('Percentage of Total Consumption (%)')
        ax4.set_title('Meter Doubling Impact Analysis')
        ax4.legend(loc='lower right', bbox_to_anchor=(1.0, -0.2), ncol=1)
        ax4.grid(False)
        ax4.text(0.05, -0.2, '', transform=ax4.transAxes, fontsize=10)
        
        # Set x-axis labels
        ax4.set_xticks(range(0, len(self.df), 6))
        ax4.set_xticklabels([self.df['Date'].iloc[i] for i in range(0, len(self.df), 6)], rotation=45)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.92)
        
        # Save figure
        fig_path = self.output_dir / f"energy_consumption_analysis_{self.timestamp}.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return fig_path
    
    def create_seasonal_analysis(self):
        """Create seasonal energy consumption analysis"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Seasonal Energy Consumption Analysis\nHarrisburg Data Center', 
                     fontsize=16, fontweight='bold', y=0.98)
        
        # Seasonal aggregation
        seasonal_data = self.df.groupby(['Year', 'Quarter']).agg({
            'Total_kWh': 'sum',
            'Total_Cost': 'sum',
            'Metered_Reading': 'sum',
            'Solar_Assumption_x2': 'sum'
        }).reset_index()
        
        # Figure 1: Quarterly Consumption by Year
        ax1 = axes[0, 0]
        years = sorted(seasonal_data['Year'].unique())
        quarters = [1, 2, 3, 4]
        
        for year in years:
            year_data = seasonal_data[seasonal_data['Year'] == year]
            ax1.plot(year_data['Quarter'], year_data['Total_kWh'], 
                    marker='o', linewidth=2, markersize=6, label=f'Year {year}')
        
        ax1.set_xlabel('Quarter')
        ax1.set_ylabel('Total Energy Consumption (kWh)')
        ax1.set_title('Quarterly Energy Consumption by Year')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_xticks(quarters)
        
        # Figure 2: Monthly Consumption Heatmap
        ax2 = axes[0, 1]
        monthly_pivot = self.df.pivot_table(values='Total_kWh', 
                                          index=self.df['Month'], 
                                          columns=self.df['Year'], 
                                          aggfunc='mean')
        
        sns.heatmap(monthly_pivot, annot=True, fmt='.0f', cmap='YlOrRd', 
                   ax=ax2, cbar_kws={'label': 'Average kWh'})
        ax2.set_title('Monthly Energy Consumption Heatmap')
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Month')
        
        # Figure 3: Cost vs Consumption Correlation
        ax3 = axes[1, 0]
        ax3.scatter(self.df['Total_kWh'], self.df['Total_Cost'], 
                   alpha=0.6, color=self.colors['metered'], s=50)
        
        # Add trend line
        z = np.polyfit(self.df['Total_kWh'], self.df['Total_Cost'], 1)
        p = np.poly1d(z)
        ax3.plot(self.df['Total_kWh'], p(self.df['Total_kWh']), 
                color=self.colors['mean_line'], linestyle='--', alpha=0.8)
        
        ax3.set_xlabel('Energy Consumption (kWh)')
        ax3.set_ylabel('Cost ($)')
        ax3.set_title('Energy Consumption vs Cost Correlation')
        ax3.grid(True, alpha=0.3)
        
        # Figure 4: Meter Doubling Impact Over Time
        ax4 = axes[1, 1]
        impact_over_time = (self.df['Solar_Assumption_x2'] / self.df['Total_kWh']) * 100
        
        ax4.plot(range(len(self.df)), impact_over_time, 
                color=self.colors['solar'], linewidth=2, marker='o', markersize=4)
        ax4.axhline(y=impact_over_time.mean(), color=self.colors['mean_line'], 
                   linestyle='--', alpha=0.7, 
                   label=f'Average Impact: {impact_over_time.mean():.1f}%')
        
        ax4.set_xlabel('Month')
        ax4.set_ylabel('Meter Doubling Impact (%)')
        ax4.set_title('Meter Doubling Impact Over Time')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Set x-axis labels
        ax4.set_xticks(range(0, len(self.df), 6))
        ax4.set_xticklabels([self.df['Date'].iloc[i] for i in range(0, len(self.df), 6)], rotation=45)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.92)
        
        # Save figure
        fig_path = self.output_dir / f"seasonal_analysis_{self.timestamp}.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return fig_path
    
    def create_synthetic_data_component(self):
        """Create synthetic data analysis for anomalous events"""
        print("Creating Synthetic Data Component for Anomalous Events...")
        
        # Generate synthetic data for comparison
        np.random.seed(42)
        synthetic_metered = np.random.normal(self.df['Metered_Reading'].mean(), 
                                           self.df['Metered_Reading'].std(), len(self.df))
        synthetic_solar = np.random.normal(self.df['Solar_Assumption'].mean(), 
                                         self.df['Solar_Assumption'].std(), len(self.df))
        
        synthetic_df = pd.DataFrame({
            'Date': self.df['Date'],
            'Synthetic_Metered': synthetic_metered,
            'Synthetic_Solar': synthetic_solar,
            'Synthetic_Total': synthetic_metered + (synthetic_solar * 2)
        })
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Synthetic Data Analysis for Anomalous Event Investigation\nMeter Doubling Impact Assessment', 
                     fontsize=16, fontweight='bold', y=0.98)
        
        # Figure 1: Actual vs Synthetic Metered Readings
        ax1 = axes[0, 0]
        x = range(len(self.df))
        ax1.plot(x, self.df['Metered_Reading'], 
                color=self.colors['metered'], linewidth=2, marker='o', 
                markersize=4, label='Actual Metered')
        ax1.plot(x, synthetic_df['Synthetic_Metered'], 
                color=self.colors['metered'], linewidth=2, marker='s', 
                markersize=4, label='Synthetic Metered', alpha=0.7)
        
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Energy Consumption (kWh)')
        ax1.set_title('Actual vs Synthetic Metered Readings')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Figure 2: Meter Doubling Impact Comparison
        ax2 = axes[0, 1]
        actual_impact = (self.df['Solar_Assumption_x2'] / self.df['Total_kWh']) * 100
        synthetic_impact = (synthetic_df['Synthetic_Solar'] * 2 / synthetic_df['Synthetic_Total']) * 100
        
        ax2.plot(x, actual_impact, 
                color=self.colors['total'], linewidth=2, marker='o', 
                markersize=4, label='Actual Impact')
        ax2.plot(x, synthetic_impact, 
                color=self.colors['warning'], linewidth=2, marker='s', 
                markersize=4, label='Synthetic Impact', alpha=0.7)
        
        ax2.set_xlabel('Month')
        ax2.set_ylabel('Meter Doubling Impact (%)')
        ax2.set_title('Meter Doubling Impact: Actual vs Synthetic')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Figure 3: Distribution Comparison
        ax3 = axes[1, 0]
        ax3.hist(self.df['Total_kWh'], bins=15, alpha=0.7, 
                color=self.colors['metered'], label='Actual Total', density=True)
        ax3.hist(synthetic_df['Synthetic_Total'], bins=15, alpha=0.7, 
                color=self.colors['info'], label='Synthetic Total', density=True)
        
        ax3.set_xlabel('Total Energy Consumption (kWh)')
        ax3.set_ylabel('Density')
        ax3.set_title('Distribution Comparison: Actual vs Synthetic')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Figure 4: Anomaly Detection
        ax4 = axes[1, 1]
        # Calculate z-scores for anomaly detection
        z_scores = np.abs((self.df['Total_kWh'] - self.df['Total_kWh'].mean()) / self.df['Total_kWh'].std())
        anomalies = z_scores > 2  # Threshold for anomalies
        
        ax4.scatter(range(len(self.df)), self.df['Total_kWh'], 
                   c=anomalies, cmap='RdYlBu_r', s=50, alpha=0.7)
        ax4.axhline(y=self.df['Total_kWh'].mean(), color=self.colors['mean_line'], 
                   linestyle='--', alpha=0.7, label='Mean')
        
        ax4.set_xlabel('Month')
        ax4.set_ylabel('Total Energy Consumption (kWh)')
        ax4.set_title('Anomaly Detection in Energy Consumption')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.92)
        
        # Save figure
        fig_path = self.output_dir / f"synthetic_analysis_{self.timestamp}.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return fig_path
    
    def create_comprehensive_table(self):
        """Create comprehensive data table"""
        fig, ax = plt.subplots(figsize=(16, 10))
        ax.axis('tight')
        ax.axis('off')
        
        # Prepare table data
        table_data = []
        table_data.append(['Date', 'Metered (kWh)', 'Solar × 2 (kWh)', 'Total (kWh)', 'Cost ($)'])
        
        for _, row in self.df.iterrows():
            table_data.append([
                row['Date'],
                f"{row['Metered_Reading']:,.0f}",
                f"{row['Solar_Assumption_x2']:,.0f}",
                f"{row['Total_kWh']:,.0f}",
                f"${row['Total_Cost']:,.2f}"
            ])
        
        # Create table
        table = ax.table(cellText=table_data, colLabels=None, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.5)
        
        # Style the table
        for i in range(len(table_data)):
            for j in range(len(table_data[0])):
                if i == 0:  # Header row
                    table[(i, j)].set_facecolor('#f0f0f0')
                    table[(i, j)].set_text_props(weight='bold', color='white')
                else:  # Data rows
                    if i % 2 == 0:
                        table[(i, j)].set_facecolor(self.colors['info'])
                    else:
                        table[(i, j)].set_facecolor('white')
        
        ax.set_title('Harrisburg Data Center Energy Consumption Data\nMeter Doubling Analysis', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Save table
        table_path = self.output_dir / f"energy_data_table_{self.timestamp}.png"
        plt.savefig(table_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return table_path
    
    def generate_analysis_report(self):
        """Generate analysis report"""
        print("Generating Energy Bill Analysis Report...")
        
        # Perform analysis
        stats = self.analyze_energy_consumption()
        
        # Create all figures
        fig1_path = self.create_energy_consumption_trends()
        fig2_path = self.create_seasonal_analysis()
        fig3_path = self.create_synthetic_data_component()
        table_path = self.create_comprehensive_table()
        
        # Generate PDF report
        from matplotlib.backends.backend_pdf import PdfPages
        
        report_path = self.output_dir / f"energy_bills_analysis_{self.timestamp}.pdf"
        
        with PdfPages(report_path) as pdf:
            # Title page
            fig = plt.figure(figsize=(12, 8))
            plt.axis('off')
            
            plt.text(0.5, 0.8, 'Energy Bill Analysis Report', 
                    fontsize=24, weight='bold', ha='center', va='center')
            plt.text(0.5, 0.7, 'Harrisburg Data Center', 
                    fontsize=18, ha='center', va='center')
            plt.text(0.5, 0.6, 'Meter Doubling Anomaly Investigation', 
                    fontsize=16, ha='center', va='center')
            plt.text(0.5, 0.5, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 
                    fontsize=14, ha='center', va='center')
            plt.text(0.5, 0.4, 'Author: Michael Maloney', 
                    fontsize=12, ha='center', va='center')
            plt.text(0.5, 0.3, 'Penn State Architectural Engineering Department', 
                    fontsize=12, ha='center', va='center')
            
            pdf.savefig(fig)
            plt.close(fig)
            
            # Summary statistics page
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.axis('tight')
            ax.axis('off')
            
            summary_data = [
                ['Metric', 'Value'],
                ['Total Consumption', f"{stats['Total_Consumption_kWh']:,.0f} kWh"],
                ['Average Monthly', f"{stats['Average_Monthly_kWh']:,.0f} kWh"],
                ['Peak Monthly', f"{stats['Peak_Monthly_kWh']:,.0f} kWh"],
                ['Total Cost', f"${stats['Total_Cost']:,.2f}"],
                ['Average Monthly Cost', f"${stats['Average_Monthly_Cost']:,.2f}"],
                ['Meter Doubling Impact', f"{stats['Meter_Doubling_Impact']:.1f}%"],
                ['Analysis Period', 'January 2022 - April 2025'],
                ['Data Points', f"{len(self.df)} months"]
            ]
            
            table = ax.table(cellText=summary_data, colLabels=None, cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(12)
            table.scale(1, 2)
            
            ax.set_title('Energy Consumption Summary Statistics', fontsize=16, weight='bold', pad=20)
            
            pdf.savefig(fig)
            plt.close(fig)
        
        print(f"   Saved: {report_path}")
        return str(report_path) 