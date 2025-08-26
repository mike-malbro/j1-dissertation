#!/usr/bin/env python3
"""
S1-Libert Cooling Unit - Temperature/Humidity Time Series Data Analysis
CRCS[n] - Computer Room Cooling System to the n

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Notes: This script is designed for PhD-level data analysis, ensuring high precision 
and reproducibility. Legends are placed at the bottom right below the x-axis to avoid 
chart interference, and annotations (e.g., correlation, averages) are positioned at 
the bottom left. This serves as a template for future analyses.

Script Title: Data Collection Report Script 1 - D-1yr Analysis
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

class LibertAnalyzer(J1AnalysisBase):
    """
    CRAC Unit Libert Data Analysis for CRCS[n] System.
    Uses the CRCSAnalysisBase for all plotting, style, and color configuration.
    """
    def __init__(self):
        super().__init__()
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.temp_range = (64.4, 80.6)
        self.humidity_range = (40, 60)
        
    def generate_synthetic_data(self) -> pd.DataFrame:
        """Generate synthetic Libert data for demonstration"""
        print("Generating synthetic Libert data...")
        
        # Create time series
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2024, 12, 31)
        date_range = pd.date_range(start=start_date, end=end_date, freq='H')
        
        # Generate synthetic temperature data (realistic CRAC unit data)
        np.random.seed(42)
        base_temp = 72.0
        temp_variation = np.random.normal(0, 3, len(date_range))
        seasonal_temp = 5 * np.sin(2 * np.pi * np.arange(len(date_range)) / (24 * 365))
        temperature = base_temp + temp_variation + seasonal_temp
        
        # Generate synthetic humidity data (correlated with temperature)
        base_humidity = 50.0
        humidity_variation = np.random.normal(0, 5, len(date_range))
        # Inverse correlation with temperature
        humidity = base_humidity + humidity_variation - 0.5 * (temperature - base_temp)
        humidity = np.clip(humidity, 30, 70)  # Keep within realistic bounds
        
        # Create DataFrame
        df = pd.DataFrame({
            'Temperature': temperature,
            'Humidity': humidity
        }, index=date_range)
        
        print(f"   Generated {len(df)} data points")
        print(f"   Time range: {df.index.min()} to {df.index.max()}")
        
        return df
    
    def calculate_statistics(self, df: pd.DataFrame) -> dict:
        """Calculate comprehensive statistics for the dataset"""
        print("Calculating statistics...")
        
        stats = {
            'temp_mean': df['Temperature'].mean(),
            'temp_std': df['Temperature'].std(),
            'temp_median': df['Temperature'].median(),
            'humidity_mean': df['Humidity'].mean(),
            'humidity_std': df['Humidity'].std(),
            'humidity_median': df['Humidity'].median(),
            'temp_in_range': ((df['Temperature'] >= self.temp_range[0]) & 
                             (df['Temperature'] <= self.temp_range[1])).mean() * 100,
            'humidity_in_range': ((df['Humidity'] >= self.humidity_range[0]) & 
                                 (df['Humidity'] <= self.humidity_range[1])).mean() * 100,
            'num_points': len(df),
            'time_start': df.index.min().strftime('%Y-%m-%d %H:%M:%S'),
            'time_end': df.index.max().strftime('%Y-%m-%d %H:%M:%S'),
            'correlation': df['Temperature'].corr(df['Humidity']),
            'temp_min': df['Temperature'].min(),
            'temp_max': df['Temperature'].max(),
            'humidity_min': df['Humidity'].min(),
            'humidity_max': df['Humidity'].max()
        }
        
        print(f"   Temperature: {stats['temp_mean']:.2f}°F ± {stats['temp_std']:.2f}°F")
        print(f"   Humidity: {stats['humidity_mean']:.2f}% ± {stats['humidity_std']:.2f}%")
        print(f"   Temperature in range: {stats['temp_in_range']:.1f}%")
        print(f"   Humidity in range: {stats['humidity_in_range']:.1f}%")
        
        return stats
    
    def create_raw_data_plot(self, df: pd.DataFrame) -> str:
        """Create Figure 0: Raw Data (scatter plot)"""
        print("Creating raw data plot...")
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax1.scatter(df.index, df['Temperature'], color=self.colors['temperature'], 
                   label='Temperature (°F)')
        ax2 = ax1.twinx()
        ax2.scatter(df.index, df['Humidity'], color=self.colors['humidity'], 
                   label='Humidity (%)')
        
        ax1.set_ylabel('Temperature (°F)')
        ax2.set_ylabel('Humidity (%)')
        ax2.set_ylim(0, 100)
        ax1.set_xlabel('Time')
        ax1.xaxis.set_major_locator(mdates.MonthLocator())
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(False)
        ax2.grid(False)
        
        handles1, labels1 = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        all_handles = handles1 + handles2
        all_labels = labels1 + labels2
        fig.legend(all_handles, all_labels, loc='lower right', 
                  bbox_to_anchor=(1.0, -0.2), ncol=1)
        ax1.text(0.05, -0.2, '', transform=ax1.transAxes, fontsize=10)
        
        plt.title('Figure 0: Raw Temperature and Humidity Data', fontsize=16)
        self.finalize_figure(fig, ax1)
        
        fig_path = self.output_dir / f"figure_0_raw_data_{self.timestamp}.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(fig_path)
    
    def create_temperature_analysis(self, df: pd.DataFrame, stats: dict) -> str:
        """Create Figure 1: Daily Averages (smoothed)"""
        print("Creating temperature analysis...")
        
        daily_df = df.resample('D').mean()
        daily_df['Temperature'] = daily_df['Temperature'].interpolate(method='linear')
        smoothed_temp = daily_df['Temperature'].rolling(window=7, min_periods=1).mean()
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        temp_line, = ax1.plot(daily_df.index, smoothed_temp, color=self.colors['temperature'], 
                             label='Temperature (°F)')
        
        # Add average line
        ax1.axhline(y=stats['temp_mean'], color=self.colors['mean_line'], linestyle='--', 
                   label=f'Average Temp ({stats["temp_mean"]:.2f} °F)')
        
        ax1.set_ylabel('Temperature (°F)')
        ax1.set_xlabel('Date')
        ax1.xaxis.set_major_locator(mdates.MonthLocator())
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(False)
        
        handles, labels = ax1.get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower right', bbox_to_anchor=(1.0, -0.2), ncol=1)
        ax1.text(0.05, -0.2, '', transform=ax1.transAxes, fontsize=10)
        
        plt.title('Figure 1: Daily Average Temperature (Smoothed)', fontsize=16)
        self.finalize_figure(fig, ax1)
        
        fig_path = self.output_dir / f"figure_1_temperature_{self.timestamp}.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(fig_path)
    
    def create_humidity_analysis(self, df: pd.DataFrame, stats: dict) -> str:
        """Create Figure 1: Daily Averages (smoothed)"""
        print("Creating humidity analysis...")
        
        daily_df = df.resample('D').mean()
        daily_df['Humidity'] = daily_df['Humidity'].interpolate(method='linear')
        smoothed_humidity = daily_df['Humidity'].rolling(window=7, min_periods=1).mean()
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        hum_line, = ax1.plot(daily_df.index, smoothed_humidity, color=self.colors['humidity'], 
                            label='Humidity (%)')
        
        # Add average line
        ax1.axhline(y=stats['humidity_mean'], color=self.colors['mean_line'], linestyle='--', 
                   label=f'Average Hum ({stats["humidity_mean"]:.2f} %)')
        
        ax1.set_ylabel('Humidity (%)')
        ax1.set_xlabel('Date')
        ax1.set_ylim(0, 100)
        ax1.xaxis.set_major_locator(mdates.MonthLocator())
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(False)
        
        handles, labels = ax1.get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower right', bbox_to_anchor=(1.0, -0.2), ncol=1)
        ax1.text(0.05, -0.2, '', transform=ax1.transAxes, fontsize=10)
        
        plt.title('Figure 1: Daily Average Humidity (Smoothed)', fontsize=16)
        self.finalize_figure(fig, ax1)
        
        fig_path = self.output_dir / f"figure_1_humidity_{self.timestamp}.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(fig_path)
    
    def create_correlation_analysis(self, df: pd.DataFrame, stats: dict) -> str:
        """Create Figure 2: Temperature vs. Humidity Relationship"""
        print("Creating correlation analysis...")
        
        fig, ax1 = plt.subplots(figsize=(8, 6))
        scatter = sns.regplot(x='Temperature', y='Humidity', data=df, color='purple', 
                             scatter_kws={'alpha':0.5}, ax=ax1)
        
        result = linregress(df['Temperature'], df['Humidity'])
        r_value = result.r_value
        ax1.text(0.05, -0.2, f'Correlation: {r_value:.2f}', transform=ax1.transAxes, fontsize=10)
        
        ax1.set_xlabel('Temperature (°F)')
        ax1.set_ylabel('Humidity (%)')
        ax1.set_ylim(0, 100)
        ax1.grid(False)
        
        handles, labels = ax1.get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower right', bbox_to_anchor=(1.0, -0.2), ncol=1)
        plt.title('Figure 2: Temperature vs. Humidity Relationship', fontsize=16)
        self.finalize_figure(fig, ax1)
        
        fig_path = self.output_dir / f"figure_2_correlation_{self.timestamp}.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(fig_path)
    
    def create_temperature_distribution(self, df: pd.DataFrame, stats: dict) -> str:
        """Create Figure 3: Temperature Distribution"""
        print("Creating temperature distribution...")
        
        fig, ax1 = plt.subplots(figsize=(7, 6))
        sns.histplot(df['Temperature'], bins=30, kde=True, color='blue', ax=ax1)
        temp_mean_line = ax1.axvline(stats['temp_mean'], color=self.colors['mean_line'], 
                                    linestyle='--', label='Mean')
        temp_median_line = ax1.axvline(df['Temperature'].median(), color=self.colors['median_line'], 
                                      linestyle='-', label='Median')
        
        ax1.set_title('Figure 3: Temperature Distribution', fontsize=14)
        ax1.set_xlabel('Temperature (°F)')
        ax1.grid(False)
        
        handles, labels = ax1.get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower right', bbox_to_anchor=(1.0, -0.2), ncol=1)
        ax1.text(0.05, -0.2, '', transform=ax1.transAxes, fontsize=10)
        plt.tight_layout()
        
        fig_path = self.output_dir / f"figure_3_temp_dist_{self.timestamp}.png"
        self.finalize_figure(fig, ax1)
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(fig_path)
    
    def create_humidity_distribution(self, df: pd.DataFrame, stats: dict) -> str:
        """Create Figure 4: Humidity Distribution"""
        print("Creating humidity distribution...")
        
        fig, ax1 = plt.subplots(figsize=(7, 6))
        sns.histplot(df['Humidity'], bins=30, kde=True, color='orange', ax=ax1)
        hum_mean_line = ax1.axvline(stats['humidity_mean'], color=self.colors['mean_line'], 
                                   linestyle='--', label='Mean')
        hum_median_line = ax1.axvline(df['Humidity'].median(), color=self.colors['median_line'], 
                                     linestyle='-', label='Median')
        
        ax1.set_title('Figure 4: Humidity Distribution', fontsize=14)
        ax1.set_xlabel('Humidity (%)')
        ax1.set_ylim(0, max(df['Humidity'].max() + 10, 100))
        ax1.grid(False)
        
        handles, labels = ax1.get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower right', bbox_to_anchor=(1.0, -0.2), ncol=1)
        ax1.text(0.05, -0.2, '', transform=ax1.transAxes, fontsize=10)
        plt.tight_layout()
        
        fig_path = self.output_dir / f"figure_4_humidity_dist_{self.timestamp}.png"
        self.finalize_figure(fig, ax1)
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(fig_path)
    
    def create_summary_table(self, stats: dict) -> str:
        """Create comprehensive summary table"""
        print("Creating summary table...")
        
        fig, ax = plt.subplots(figsize=(12, 10))
        ax.axis('tight')
        ax.axis('off')
        
        # Prepare table data
        table_data = [
            ['Metric', 'Value', 'Units', 'Status'],
            ['Data Points', f"{stats['num_points']:,}", 'points', 'Complete'],
            ['Time Range', f"{stats['time_start']} to {stats['time_end']}", 'datetime', 'Full Period'],
            ['', '', '', ''],
            ['Temperature Statistics', '', '', ''],
            ['Mean Temperature', f"{stats['temp_mean']:.2f}", '°F', 'Calculated'],
            ['Temperature Std Dev', f"{stats['temp_std']:.2f}", '°F', 'Calculated'],
            ['Temperature Median', f"{stats['temp_median']:.2f}", '°F', 'Calculated'],
            ['Temperature Range', f"{stats['temp_min']:.1f} - {stats['temp_max']:.1f}", '°F', 'Observed'],
            ['Temperature in Range', f"{stats['temp_in_range']:.1f}", '%', 'Compliance'],
            ['', '', '', ''],
            ['Humidity Statistics', '', '', ''],
            ['Mean Humidity', f"{stats['humidity_mean']:.2f}", '%', 'Calculated'],
            ['Humidity Std Dev', f"{stats['humidity_std']:.2f}", '%', 'Calculated'],
            ['Humidity Median', f"{stats['humidity_median']:.2f}", '%', 'Calculated'],
            ['Humidity Range', f"{stats['humidity_min']:.1f} - {stats['humidity_max']:.1f}", '%', 'Observed'],
            ['Humidity in Range', f"{stats['humidity_in_range']:.1f}", '%', 'Compliance'],
            ['', '', '', ''],
            ['Correlation Analysis', '', '', ''],
            ['Temp-Humidity Correlation', f"{stats['correlation']:.3f}", 'coefficient', 'Calculated']
        ]
        
        # Create table
        table = ax.table(cellText=table_data, colLabels=None, cellLoc='left', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
        
        # Style the table with professional colors
        for i in range(len(table_data)):
            for j in range(len(table_data[0])):
                if i == 0:  # Header row
                    table[(i, j)].set_facecolor('#f0f0f0')
                    table[(i, j)].set_text_props(weight='bold', color='black')
                elif table_data[i][0] in ['Temperature Statistics', 'Humidity Statistics', 'Correlation Analysis']:
                    table[(i, j)].set_facecolor('#e0e0e0')
                    table[(i, j)].set_text_props(weight='bold')
                elif i % 2 == 0:
                    table[(i, j)].set_facecolor('#f8f8f8')
                else:
                    table[(i, j)].set_facecolor('white')
        
        ax.set_title('CRAC Unit Libert Analysis Summary\nComprehensive Statistical Overview', 
                    fontsize=16, fontweight='bold', pad=20)
        self.finalize_figure(fig, ax)
        
        table_path = self.output_dir / f"summary_table_{self.timestamp}.png"
        plt.savefig(table_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(table_path)
    
    def generate_analysis_report(self) -> str:
        """Generate comprehensive Libert analysis report"""
        print("Generating Libert Analysis Report...")
        
        # Generate synthetic data (replace with real data loading when available)
        df = self.generate_synthetic_data()
        stats = self.calculate_statistics(df)
        
        # Create all visualizations
        fig_paths = {
            'raw_data': self.create_raw_data_plot(df),
            'temperature': self.create_temperature_analysis(df, stats),
            'humidity': self.create_humidity_analysis(df, stats),
            'correlation': self.create_correlation_analysis(df, stats),
            'temp_dist': self.create_temperature_distribution(df, stats),
            'humidity_dist': self.create_humidity_distribution(df, stats),
            'summary_table': self.create_summary_table(stats)
        }
        
        # Generate PDF report
        report_path = self.output_dir / f"libert_analysis_{self.timestamp}.pdf"
        
        with PdfPages(report_path) as pdf:
            # Title page
            fig = plt.figure(figsize=(12, 8))
            plt.axis('off')
            
            plt.text(0.5, 0.8, 'CRAC Unit Libert Analysis Report', 
                    fontsize=24, weight='bold', ha='center', va='center')
            plt.text(0.5, 0.7, 'CRCS[n] - Module 03', 
                    fontsize=18, ha='center', va='center')
            plt.text(0.5, 0.6, 'Temperature and Humidity Analysis', 
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
            
            summary_text = (
                f"Analysis Summary\n\n"
                f"Data Points: {stats['num_points']:,}\n"
                f"Time Range: {stats['time_start']} to {stats['time_end']}\n\n"
                f"Temperature Statistics:\n"
                f"  Mean: {stats['temp_mean']:.2f}°F ± {stats['temp_std']:.2f}°F\n"
                f"  Median: {stats['temp_median']:.2f}°F\n"
                f"  Range: {stats['temp_min']:.1f}°F - {stats['temp_max']:.1f}°F\n"
                f"  In Optimal Range: {stats['temp_in_range']:.1f}%\n\n"
                f"Humidity Statistics:\n"
                f"  Mean: {stats['humidity_mean']:.2f}% ± {stats['humidity_std']:.2f}%\n"
                f"  Median: {stats['humidity_median']:.2f}%\n"
                f"  Range: {stats['humidity_min']:.1f}% - {stats['humidity_max']:.1f}%\n"
                f"  In Optimal Range: {stats['humidity_in_range']:.1f}%\n\n"
                f"Correlation Analysis:\n"
                f"  Temperature-Humidity Correlation: {stats['correlation']:.3f}"
            )
            
            plt.text(0.1, 0.9, summary_text, fontsize=12, va='top', 
                    transform=ax.transAxes, fontfamily='monospace')
            
            ax.set_title('CRAC Unit Libert Analysis Summary', fontsize=16, weight='bold', pad=20)
            
            pdf.savefig(fig)
            plt.close(fig)
        
        print(f"   Saved: {report_path}")
        return str(report_path)

# The main function is removed as per the edit hint.
# def main():
#     """Main function"""
#     print("Starting CRAC Unit Libert Analysis...")
#     print("Output directory:", Path(__file__).parent / "output")
    
#     analyzer = LibertAnalyzer()
#     report_path = analyzer.generate_analysis_report()
    
#     print("Libert Analysis completed!")
#     print(f"Report: {report_path}")

# if __name__ == "__main__":
#     main() 