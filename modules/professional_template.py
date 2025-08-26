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
import seaborn as sns
try:
    from scipy.stats import linregress
except ImportError:
    # Manual correlation calculation if scipy not available
    def linregress(x, y):
        n = len(x)
        x_mean, y_mean = np.mean(x), np.mean(y)
        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sqrt(np.sum((x - x_mean)**2) * np.sum((y - y_mean)**2))
        r_value = numerator / denominator if denominator != 0 else 0
        return type('obj', (object,), {
            'slope': 0, 'intercept': 0, 'r_value': r_value, 'p_value': 0, 'std_err': 0
        })()
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates
import datetime
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set seaborn style
sns.set_style("white")

class ProfessionalDataAnalyzer:
    """Professional Data Analysis Template for J1 System"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # Professional color palette
        self.colors = {
            'temperature': 'tab:blue',
            'humidity': 'tab:orange',
            'regression': 'red',
            'mean_line': 'red',
            'median_line': 'green',
            'grid': 'black'
        }
        
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Analysis parameters
        self.temp_range = (64.4, 80.6)
        self.humidity_range = (40, 60)
        
    def load_data(self, file_id: str = None) -> pd.DataFrame:
        """
        Load data from Google Drive or generate synthetic data
        
        Args:
            file_id: Google Drive file ID for real data
            
        Returns:
            pd.DataFrame: Cleaned and processed data
        """
        if file_id:
            # Load from Google Drive
            url = f'https://drive.google.com/uc?export=download&id={file_id}'
            try:
                df = pd.read_csv(url, sep=',', skiprows=1, parse_dates=[0], 
                               index_col=0, on_bad_lines='skip')
                df = df[['Return_Air_Temperature / 10%', 'Return_Realative_Humidity / 10%']]
                df.columns = ['Temperature', 'Humidity']
                df['Temperature'] = df['Temperature'].str.replace(' °F', '').astype(float)
                df['Humidity'] = df['Humidity'].str.replace('%', '').astype(float)
                df = df[(df['Temperature'] >= 0) & (df['Temperature'] <= 100) & 
                       (df['Humidity'] >= 0) & (df['Humidity'] <= 100)]
            except pd.errors.ParserError as e:
                print(f"ParserError: {e}. Switching to chunked reading...")
                chunk_size = 1000
                chunks = []
                for chunk in pd.read_csv(url, sep=',', chunksize=chunk_size, skiprows=1):
                    chunks.append(chunk)
                df = pd.concat(chunks, ignore_index=True)
                df['Time'] = pd.to_datetime(df['Time'])
                df.set_index('Time', inplace=True)
                df = df[['Return_Air_Temperature / 10%', 'Return_Realative_Humidity / 10%']]
                df.columns = ['Temperature', 'Humidity']
                df['Temperature'] = df['Temperature'].str.replace(' °F', '').astype(float)
                df['Humidity'] = df['Humidity'].str.replace('%', '').astype(float)
                df = df[(df['Temperature'] >= 0) & (df['Temperature'] <= 100) & 
                       (df['Humidity'] >= 0) & (df['Humidity'] <= 100)]
        else:
            # Generate synthetic data
            df = self.generate_synthetic_data()
            
        return df
    
    def generate_synthetic_data(self) -> pd.DataFrame:
        """Generate synthetic data for demonstration"""
        print("Generating synthetic data...")
        
        # Create time series
        start_date = datetime.datetime(2023, 1, 1)
        end_date = datetime.datetime(2024, 12, 31)
        date_range = pd.date_range(start=start_date, end=end_date, freq='H')
        
        # Generate realistic data
        np.random.seed(42)
        base_temp = 72.0
        temp_variation = np.random.normal(0, 3, len(date_range))
        seasonal_temp = 5 * np.sin(2 * np.pi * np.arange(len(date_range)) / (24 * 365))
        temperature = base_temp + temp_variation + seasonal_temp
        
        base_humidity = 50.0
        humidity_variation = np.random.normal(0, 5, len(date_range))
        humidity = base_humidity + humidity_variation - 0.5 * (temperature - base_temp)
        humidity = np.clip(humidity, 30, 70)
        
        df = pd.DataFrame({
            'Temperature': temperature,
            'Humidity': humidity
        }, index=date_range)
        
        print(f"   Generated {len(df)} data points")
        print(f"   Time range: {df.index.min()} to {df.index.max()}")
        
        return df
    
    def calculate_statistics(self, df: pd.DataFrame) -> dict:
        """Calculate comprehensive statistics"""
        print("Calculating statistics...")
        
        temp_mean = df['Temperature'].mean()
        temp_std = df['Temperature'].std()
        humidity_mean = df['Humidity'].mean()
        humidity_std = df['Humidity'].std()
        
        temp_in_range = ((df['Temperature'] >= self.temp_range[0]) & 
                        (df['Temperature'] <= self.temp_range[1])).mean() * 100
        humidity_in_range = ((df['Humidity'] >= self.humidity_range[0]) & 
                           (df['Humidity'] <= self.humidity_range[1])).mean() * 100
        
        num_points = len(df)
        time_start = df.index.min().strftime('%Y-%m-%d %H:%M:%S')
        time_end = df.index.max().strftime('%Y-%m-%d %H:%M:%S')
        
        stats = {
            'temp_mean': temp_mean,
            'temp_std': temp_std,
            'humidity_mean': humidity_mean,
            'humidity_std': humidity_std,
            'temp_in_range': temp_in_range,
            'humidity_in_range': humidity_in_range,
            'num_points': num_points,
            'time_start': time_start,
            'time_end': time_end
        }
        
        print(f"   Temperature: {temp_mean:.2f}°F ± {temp_std:.2f}°F")
        print(f"   Humidity: {humidity_mean:.2f}% ± {humidity_std:.2f}%")
        print(f"   Temperature in range: {temp_in_range:.1f}%")
        print(f"   Humidity in range: {humidity_in_range:.1f}%")
        
        return stats
    
    def create_summary_page(self, stats: dict) -> str:
        """Create professional summary page"""
        print("Creating summary page...")
        
        summary_pdf = self.output_dir / f"summary_{self.timestamp}.pdf"
        
        with PdfPages(summary_pdf) as pdf:
            fig = plt.figure(figsize=(8.5, 11))
            plt.axis('off')
            
            current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            summary_text = (
                f"Data Collection Report Script 1 - Analysis\n"
                f"Name: Michael Logan Maloney\n"
                f"Generated on: {current_date}\n\n"
                f"Number of Data Points: {stats['num_points']}\n"
                f"Time Range: {stats['time_start']} to {stats['time_end']}\n\n"
                f"Statistical Summary:\n"
                f"Average Temperature: {stats['temp_mean']:.2f} °F\n"
                f"Temperature Std Dev: {stats['temp_std']:.2f} °F\n"
                f"Average Humidity: {stats['humidity_mean']:.2f} %\n"
                f"Humidity Std Dev: {stats['humidity_std']:.2f} %\n"
                f"Temperature in Range ({self.temp_range[0]}-{self.temp_range[1]} °F): {stats['temp_in_range']:.2f}%\n"
                f"Humidity in Range ({self.humidity_range[0]}-{self.humidity_range[1]} %): {stats['humidity_in_range']:.2f}%"
            )
            
            plt.text(0.1, 0.9, summary_text, fontsize=12, va='top')
            pdf.savefig()
            plt.close()
        
        return str(summary_pdf)
    
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
        plt.tight_layout()
        
        fig_path = self.output_dir / f"figure_0_raw_data_{self.timestamp}.png"
        fig.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(fig_path)
    
    def create_daily_averages_plot(self, df: pd.DataFrame, stats: dict) -> str:
        """Create Figure 1: Daily Averages (smoothed)"""
        print("Creating daily averages plot...")
        
        daily_df = df.resample('D').mean()
        daily_df['Temperature'] = daily_df['Temperature'].interpolate(method='linear')
        daily_df['Humidity'] = daily_df['Humidity'].interpolate(method='linear')
        smoothed_temp = daily_df['Temperature'].rolling(window=7, min_periods=1).mean()
        smoothed_humidity = daily_df['Humidity'].rolling(window=7, min_periods=1).mean()
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        temp_line, = ax1.plot(daily_df.index, smoothed_temp, color=self.colors['temperature'], 
                             label='Temperature (°F)')
        ax2 = ax1.twinx()
        hum_line, = ax2.plot(daily_df.index, smoothed_humidity, color=self.colors['humidity'], 
                            label='Humidity (%)')
        
        # Add average lines
        ax1.axhline(y=stats['temp_mean'], color=self.colors['mean_line'], linestyle='--', 
                   label=f'Average Temp ({stats["temp_mean"]:.2f} °F)')
        ax2.axhline(y=stats['humidity_mean'], color=self.colors['mean_line'], linestyle='--', 
                   label=f'Average Hum ({stats["humidity_mean"]:.2f} %)')
        
        ax1.set_ylabel('Temperature (°F)')
        ax2.set_ylabel('Humidity (%)')
        ax2.set_ylim(0, 100)
        ax1.set_xlabel('Date')
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
        
        plt.title('Figure 1: Daily Average Temperature and Humidity (Smoothed)', fontsize=16)
        plt.tight_layout()
        
        fig_path = self.output_dir / f"figure_1_daily_averages_{self.timestamp}.png"
        fig.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(fig_path)
    
    def create_correlation_plot(self, df: pd.DataFrame) -> str:
        """Create Figure 2: Temperature vs. Humidity Relationship"""
        print("Creating correlation plot...")
        
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
        plt.tight_layout()
        
        fig_path = self.output_dir / f"figure_2_correlation_{self.timestamp}.png"
        fig.savefig(fig_path, dpi=300, bbox_inches='tight')
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
        fig.savefig(fig_path, dpi=300, bbox_inches='tight')
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
        fig.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(fig_path)
    
    def generate_comprehensive_report(self, file_id: str = None) -> str:
        """Generate comprehensive analysis report"""
        print("Starting comprehensive analysis...")
        
        # Load data
        df = self.load_data(file_id)
        
        # Calculate statistics
        stats = self.calculate_statistics(df)
        
        # Create PDF report
        report_pdf = self.output_dir / f"comprehensive_analysis_{self.timestamp}.pdf"
        
        with PdfPages(report_pdf) as pdf:
            # Summary page
            summary_fig = plt.figure(figsize=(8.5, 11))
            plt.axis('off')
            current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            summary_text = (
                f"Data Collection Report Script 1 - Analysis\n"
                f"Name: Michael Logan Maloney\n"
                f"Generated on: {current_date}\n\n"
                f"Number of Data Points: {stats['num_points']}\n"
                f"Time Range: {stats['time_start']} to {stats['time_end']}\n\n"
                f"Statistical Summary:\n"
                f"Average Temperature: {stats['temp_mean']:.2f} °F\n"
                f"Temperature Std Dev: {stats['temp_std']:.2f} °F\n"
                f"Average Humidity: {stats['humidity_mean']:.2f} %\n"
                f"Humidity Std Dev: {stats['humidity_std']:.2f} %\n"
                f"Temperature in Range ({self.temp_range[0]}-{self.temp_range[1]} °F): {stats['temp_in_range']:.2f}%\n"
                f"Humidity in Range ({self.humidity_range[0]}-{self.humidity_range[1]} %): {stats['humidity_in_range']:.2f}%"
            )
            plt.text(0.1, 0.9, summary_text, fontsize=12, va='top')
            pdf.savefig(summary_fig)
            plt.close()
            
            # Figure 0: Raw Data
            self.create_raw_data_plot(df)
            raw_fig = plt.imread(self.output_dir / f"figure_0_raw_data_{self.timestamp}.png")
            fig = plt.figure(figsize=(12, 6))
            plt.imshow(raw_fig)
            plt.axis('off')
            pdf.savefig(fig)
            plt.close()
            
            # Figure 1: Daily Averages
            self.create_daily_averages_plot(df, stats)
            daily_fig = plt.imread(self.output_dir / f"figure_1_daily_averages_{self.timestamp}.png")
            fig = plt.figure(figsize=(12, 6))
            plt.imshow(daily_fig)
            plt.axis('off')
            pdf.savefig(fig)
            plt.close()
            
            # Figure 2: Correlation
            self.create_correlation_plot(df)
            corr_fig = plt.imread(self.output_dir / f"figure_2_correlation_{self.timestamp}.png")
            fig = plt.figure(figsize=(8, 6))
            plt.imshow(corr_fig)
            plt.axis('off')
            pdf.savefig(fig)
            plt.close()
            
            # Figure 3: Temperature Distribution
            self.create_temperature_distribution(df, stats)
            temp_dist_fig = plt.imread(self.output_dir / f"figure_3_temp_dist_{self.timestamp}.png")
            fig = plt.figure(figsize=(7, 6))
            plt.imshow(temp_dist_fig)
            plt.axis('off')
            pdf.savefig(fig)
            plt.close()
            
            # Figure 4: Humidity Distribution
            self.create_humidity_distribution(df, stats)
            hum_dist_fig = plt.imread(self.output_dir / f"figure_4_humidity_dist_{self.timestamp}.png")
            fig = plt.figure(figsize=(7, 6))
            plt.imshow(hum_dist_fig)
            plt.axis('off')
            pdf.savefig(fig)
            plt.close()
        
        print(f"Report generated: {report_pdf}")
        return str(report_pdf)

def main():
    """Main execution function"""
    print("Starting Professional Data Analysis...")
    
    analyzer = ProfessionalDataAnalyzer()
    
    # Generate comprehensive report
    report_path = analyzer.generate_comprehensive_report()
    
    print(f"Analysis completed!")
    print(f"Report: {report_path}")

if __name__ == "__main__":
    main() 