"""
Integration Example: Using Standardized Figure Generator in J1 Module
Author: Michael Maloney
Purpose: Demonstrate how to integrate the figure generator into existing modules
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import sys
sys.path.append(str(Path(__file__).parent))

from figure_generator import FigureGenerator

class DataCenterAnalysisModule:
    """
    Example module showing how to integrate the standardized figure generator
    This demonstrates the professional approach you used in your Liebert analysis
    """
    
    def __init__(self):
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Initialize the standardized figure generator
        self.fig_gen = FigureGenerator(self.output_dir, self.timestamp)
        
        # Module metadata (following your professional approach)
        self.module_title = "Data Center Performance Analysis"
        self.author = "Michael Maloney"
        self.analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def load_and_process_data(self):
        """Load and process data (simulated for this example)"""
        print("Loading and processing data...")
        
        # Generate sample data (replace with your actual data loading)
        np.random.seed(42)
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
        n_points = len(dates)
        
        # Simulate realistic data center data
        # Temperature with seasonal trend and daily variation
        temp_trend = 72 + 8 * np.sin(2 * np.pi * np.arange(n_points) / 365)
        temp_daily = 2 * np.sin(2 * np.pi * np.arange(n_points) / 24)
        temp_noise = np.random.normal(0, 1.5, n_points)
        temperatures = temp_trend + temp_daily + temp_noise
        
        # Humidity (inverse relationship with temperature)
        humidity_base = 45
        humidity_temp_factor = -0.5 * (temperatures - 72)
        humidity_noise = np.random.normal(0, 3, n_points)
        humidities = np.clip(humidity_base + humidity_temp_factor + humidity_noise, 30, 70)
        
        # Power consumption (depends on temperature and humidity)
        power_base = 1200  # kW
        power_temp_factor = 1 + 0.025 * (temperatures - 72)  # 2.5% per degree
        power_humidity_factor = 1 + 0.01 * (humidities - 45) / 45
        power_consumption = power_base * power_temp_factor * power_humidity_factor + np.random.normal(0, 30, n_points)
        
        # Efficiency (COP) - decreases with temperature and humidity
        cop_base = 4.2
        cop_temp_factor = 1 - 0.02 * (temperatures - 72)
        cop_humidity_factor = 1 - 0.005 * (humidities - 45) / 45
        cop_values = cop_base * cop_temp_factor * cop_humidity_factor + np.random.normal(0, 0.08, n_points)
        
        return {
            'dates': dates,
            'temperatures': temperatures,
            'humidities': humidities,
            'power_consumption': power_consumption,
            'cop_values': cop_values
        }
    
    def generate_analysis_figures(self, data):
        """Generate professional analysis figures using standardized generator"""
        print("Generating analysis figures...")
        
        figure_paths = []
        
        # Figure 1: Temperature time series (following your approach)
        print("   Creating Figure 1: Temperature time series...")
        fig1 = self.fig_gen.create_time_series_plot(
            time_data=data['dates'],
            y_data=data['temperatures'],
            title="Data Center Temperature Analysis",
            y_label="Temperature (°F)",
            color=self.fig_gen.colors['temp'],
            add_mean_line=True,
            add_rolling_avg=True,
            window=7
        )
        figure_paths.append(fig1)
        
        # Figure 2: Dual-axis temperature and humidity (like your Figure 0)
        print("   Creating Figure 2: Temperature and humidity relationship...")
        fig2 = self.fig_gen.create_dual_axis_plot(
            time_data=data['dates'],
            y1_data=data['temperatures'],
            y2_data=data['humidities'],
            title="Temperature and Humidity Correlation",
            y1_label="Temperature (°F)",
            y2_label="Humidity (%)",
            y1_color=self.fig_gen.colors['temp'],
            y2_color=self.fig_gen.colors['humidity']
        )
        figure_paths.append(fig2)
        
        # Figure 3: Scatter plot with regression (like your Figure 2)
        print("   Creating Figure 3: Temperature vs humidity scatter plot...")
        fig3 = self.fig_gen.create_scatter_plot(
            x_data=data['temperatures'],
            y_data=data['humidities'],
            title="Temperature vs Humidity Relationship",
            x_label="Temperature (°F)",
            y_label="Humidity (%)",
            color=self.fig_gen.colors['accent'],
            add_regression=True,
            add_stats=True
        )
        figure_paths.append(fig3)
        
        # Figure 4: Temperature distribution histogram (like your Figure 3)
        print("   Creating Figure 4: Temperature distribution...")
        fig4 = self.fig_gen.create_histogram_plot(
            data=data['temperatures'],
            title="Temperature Distribution Analysis",
            x_label="Temperature (°F)",
            color=self.fig_gen.colors['temp'],
            bins=30,
            add_kde=True,
            add_stats=True
        )
        figure_paths.append(fig4)
        
        # Figure 5: Power consumption analysis
        print("   Creating Figure 5: Power consumption analysis...")
        fig5 = self.fig_gen.create_time_series_plot(
            time_data=data['dates'],
            y_data=data['power_consumption'],
            title="Data Center Power Consumption",
            y_label="Power Consumption (kW)",
            color=self.fig_gen.colors['power'],
            add_mean_line=True,
            add_rolling_avg=True,
            window=14
        )
        figure_paths.append(fig5)
        
        # Figure 6: Efficiency analysis
        print("   Creating Figure 6: Efficiency analysis...")
        fig6 = self.fig_gen.create_scatter_plot(
            x_data=data['temperatures'],
            y_data=data['cop_values'],
            title="Temperature vs Efficiency (COP)",
            x_label="Temperature (°F)",
            y_label="Coefficient of Performance",
            color=self.fig_gen.colors['efficiency'],
            add_regression=True,
            add_stats=True
        )
        figure_paths.append(fig6)
        
        # Figure 7: Monthly performance summary
        print("   Creating Figure 7: Monthly performance summary...")
        monthly_data = pd.DataFrame({
            'Date': data['dates'],
            'Temperature': data['temperatures'],
            'Humidity': data['humidities'],
            'Power': data['power_consumption'],
            'COP': data['cop_values']
        })
        monthly_avg = monthly_data.groupby(monthly_data['Date'].dt.month).mean()
        
        fig7 = self.fig_gen.create_bar_plot(
            categories=[f"Month {i}" for i in monthly_avg.index],
            values=monthly_avg['COP'].values,
            title="Monthly Average Efficiency (COP)",
            y_label="Coefficient of Performance",
            color=self.fig_gen.colors['efficiency'],
            add_values=True
        )
        figure_paths.append(fig7)
        
        return figure_paths
    
    def create_summary_statistics(self, data):
        """Create comprehensive summary statistics"""
        print("Calculating summary statistics...")
        
        # Calculate key statistics
        temp_mean = np.mean(data['temperatures'])
        temp_std = np.std(data['temperatures'])
        temp_range = (np.min(data['temperatures']), np.max(data['temperatures']))
        
        humidity_mean = np.mean(data['humidities'])
        humidity_std = np.std(data['humidities'])
        
        power_mean = np.mean(data['power_consumption'])
        power_std = np.std(data['power_consumption'])
        
        cop_mean = np.mean(data['cop_values'])
        cop_std = np.std(data['cop_values'])
        
        # Calculate performance metrics
        temp_in_range = ((data['temperatures'] >= 68) & (data['temperatures'] <= 76)).mean() * 100
        humidity_in_range = ((data['humidities'] >= 40) & (data['humidities'] <= 60)).mean() * 100
        
        return {
            "Analysis Information": "",
            "Module Title": self.module_title,
            "Author": self.author,
            "Analysis Date": self.analysis_date,
            "Data Points": len(data['temperatures']),
            "Date Range": f"{data['dates'][0].strftime('%Y-%m-%d')} to {data['dates'][-1].strftime('%Y-%m-%d')}",
            " ": "",
            "Temperature Statistics": "",
            "  Mean Temperature": f"{temp_mean:.2f} °F",
            "  Temperature Std Dev": f"{temp_std:.2f} °F",
            "  Temperature Range": f"{temp_range[0]:.1f} - {temp_range[1]:.1f} °F",
            "  Temperature in Range (68-76°F)": f"{temp_in_range:.1f}%",
            " ": "",
            "Humidity Statistics": "",
            "  Mean Humidity": f"{humidity_mean:.2f} %",
            "  Humidity Std Dev": f"{humidity_std:.2f} %",
            "  Humidity in Range (40-60%)": f"{humidity_in_range:.1f}%",
            " ": "",
            "Power Statistics": "",
            "  Mean Power Consumption": f"{power_mean:.0f} kW",
            "  Power Std Dev": f"{power_std:.0f} kW",
            "  Min Power": f"{np.min(data['power_consumption']):.0f} kW",
            "  Max Power": f"{np.max(data['power_consumption']):.0f} kW",
            " ": "",
            "Efficiency Statistics": "",
            "  Mean COP": f"{cop_mean:.2f}",
            "  COP Std Dev": f"{cop_std:.2f}",
            "  Min COP": f"{np.min(data['cop_values']):.2f}",
            "  Max COP": f"{np.max(data['cop_values']):.2f}",
            " ": "",
            "Key Findings": "",
            "  Temperature Control": "Good" if temp_in_range > 90 else "Needs Improvement",
            "  Humidity Control": "Good" if humidity_in_range > 90 else "Needs Improvement",
            "  Energy Efficiency": "Excellent" if cop_mean > 4.0 else "Good" if cop_mean > 3.5 else "Needs Improvement"
        }
    
    def generate_comprehensive_report(self):
        """Generate the complete analysis report"""
        print(f"Starting {self.module_title}...")
        
        # Step 1: Load and process data
        data = self.load_and_process_data()
        
        # Step 2: Generate figures
        figure_paths = self.generate_analysis_figures(data)
        
        # Step 3: Create summary statistics
        summary_stats = self.create_summary_statistics(data)
        
        # Step 4: Create summary page
        print("   Creating summary page...")
        summary_fig = self.fig_gen.create_summary_page(
            title=f"{self.module_title} Summary",
            summary_data=summary_stats
        )
        figure_paths.append(summary_fig)
        
        # Step 5: Compile PDF report
        print("   Compiling comprehensive PDF report...")
        pdf_path = self.fig_gen.compile_pdf_report(
            figure_paths=figure_paths,
            title=self.module_title,
            author=self.author
        )
        
        print(f"\n✅ {self.module_title} completed!")
        print(f"📊 Generated {len(figure_paths)} figures")
        print(f"📄 PDF Report: {pdf_path}")
        print(f"📁 All figures saved in: {self.output_dir}")
        
        return pdf_path

def main():
    """Main execution function"""
    analyzer = DataCenterAnalysisModule()
    pdf_path = analyzer.generate_comprehensive_report()
    return pdf_path

if __name__ == "__main__":
    main() 