"""
Demonstration of Standardized Figure Generator
Author: Michael Maloney
Purpose: Show how to use the professional figure generator for J1 project
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import sys
sys.path.append(str(Path(__file__).parent))

from figure_generator import FigureGenerator

def generate_demo_figures():
    """Generate demonstration figures using the standardized generator"""
    
    # Setup
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Initialize figure generator
    fig_gen = FigureGenerator(output_dir, timestamp)
    
    print("Generating demonstration figures...")
    
    # Generate sample data
    np.random.seed(42)  # For reproducibility
    
    # Time series data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    n_points = len(dates)
    
    # Temperature data (with seasonal trend)
    temp_trend = 70 + 15 * np.sin(2 * np.pi * np.arange(n_points) / 365)
    temp_noise = np.random.normal(0, 2, n_points)
    temperatures = temp_trend + temp_noise
    
    # Humidity data (inverse relationship with temperature)
    humidity_trend = 50 - 20 * np.sin(2 * np.pi * np.arange(n_points) / 365)
    humidity_noise = np.random.normal(0, 5, n_points)
    humidities = np.clip(humidity_trend + humidity_noise, 20, 80)
    
    # Power consumption data
    power_base = 1000  # kW
    power_temp_factor = 1 + 0.02 * (temperatures - 70)  # 2% increase per degree above 70°F
    power_humidity_factor = 1 + 0.01 * (humidities - 50) / 50  # 1% increase per 50% humidity change
    power_consumption = power_base * power_temp_factor * power_humidity_factor + np.random.normal(0, 50, n_points)
    
    # Efficiency data (COP)
    cop_base = 4.0
    cop_temp_factor = 1 - 0.015 * (temperatures - 70)  # Decreases with temperature
    cop_humidity_factor = 1 - 0.005 * (humidities - 50) / 50  # Decreases with humidity
    cop_values = cop_base * cop_temp_factor * cop_humidity_factor + np.random.normal(0, 0.1, n_points)
    
    figure_paths = []
    
    # 1. Time series plot - Temperature
    print("   Creating temperature time series...")
    temp_fig = fig_gen.create_time_series_plot(
        time_data=dates,
        y_data=temperatures,
        title="Data Center Temperature Over Time",
        y_label="Temperature (°F)",
        color=fig_gen.colors['temp'],
        add_mean_line=True,
        add_rolling_avg=True,
        window=7
    )
    figure_paths.append(temp_fig)
    
    # 2. Dual-axis plot - Temperature and Humidity
    print("   Creating dual-axis temperature/humidity plot...")
    dual_fig = fig_gen.create_dual_axis_plot(
        time_data=dates,
        y1_data=temperatures,
        y2_data=humidities,
        title="Temperature and Humidity Relationship",
        y1_label="Temperature (°F)",
        y2_label="Humidity (%)",
        y1_color=fig_gen.colors['temp'],
        y2_color=fig_gen.colors['humidity']
    )
    figure_paths.append(dual_fig)
    
    # 3. Scatter plot - Temperature vs Humidity
    print("   Creating temperature vs humidity scatter plot...")
    scatter_fig = fig_gen.create_scatter_plot(
        x_data=temperatures,
        y_data=humidities,
        title="Temperature vs Humidity Correlation",
        x_label="Temperature (°F)",
        y_label="Humidity (%)",
        color=fig_gen.colors['accent'],
        add_regression=True,
        add_stats=True
    )
    figure_paths.append(scatter_fig)
    
    # 4. Histogram - Temperature distribution
    print("   Creating temperature distribution histogram...")
    hist_fig = fig_gen.create_histogram_plot(
        data=temperatures,
        title="Temperature Distribution Analysis",
        x_label="Temperature (°F)",
        color=fig_gen.colors['temp'],
        bins=30,
        add_kde=True,
        add_stats=True
    )
    figure_paths.append(hist_fig)
    
    # 5. Time series - Power consumption
    print("   Creating power consumption time series...")
    power_fig = fig_gen.create_time_series_plot(
        time_data=dates,
        y_data=power_consumption,
        title="Data Center Power Consumption",
        y_label="Power Consumption (kW)",
        color=fig_gen.colors['power'],
        add_mean_line=True,
        add_rolling_avg=True,
        window=14
    )
    figure_paths.append(power_fig)
    
    # 6. Scatter plot - Temperature vs Power
    print("   Creating temperature vs power scatter plot...")
    temp_power_fig = fig_gen.create_scatter_plot(
        x_data=temperatures,
        y_data=power_consumption,
        title="Temperature vs Power Consumption",
        x_label="Temperature (°F)",
        y_label="Power Consumption (kW)",
        color=fig_gen.colors['efficiency'],
        add_regression=True,
        add_stats=True
    )
    figure_paths.append(temp_power_fig)
    
    # 7. Bar plot - Monthly averages
    print("   Creating monthly averages bar plot...")
    monthly_data = pd.DataFrame({
        'Date': dates,
        'Temperature': temperatures,
        'Humidity': humidities,
        'Power': power_consumption,
        'COP': cop_values
    })
    monthly_avg = monthly_data.groupby(monthly_data['Date'].dt.month).mean()
    
    bar_fig = fig_gen.create_bar_plot(
        categories=[f"Month {i}" for i in monthly_avg.index],
        values=monthly_avg['Temperature'].values,
        title="Monthly Average Temperature",
        y_label="Temperature (°F)",
        color=fig_gen.colors['temp'],
        add_values=True
    )
    figure_paths.append(bar_fig)
    
    # 8. Summary page
    print("   Creating summary page...")
    summary_data = {
        "Total Data Points": len(temperatures),
        "Date Range": f"{dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')}",
        "Temperature Statistics": "",
        "  Mean Temperature": f"{np.mean(temperatures):.2f} °F",
        "  Temperature Std Dev": f"{np.std(temperatures):.2f} °F",
        "  Min Temperature": f"{np.min(temperatures):.2f} °F",
        "  Max Temperature": f"{np.max(temperatures):.2f} °F",
        "Humidity Statistics": "",
        "  Mean Humidity": f"{np.mean(humidities):.2f} %",
        "  Humidity Std Dev": f"{np.std(humidities):.2f} %",
        "Power Statistics": "",
        "  Mean Power": f"{np.mean(power_consumption):.2f} kW",
        "  Power Std Dev": f"{np.std(power_consumption):.2f} kW",
        "Efficiency Statistics": "",
        "  Mean COP": f"{np.mean(cop_values):.2f}",
        "  COP Std Dev": f"{np.std(cop_values):.2f}"
    }
    
    summary_fig = fig_gen.create_summary_page(
        title="Data Center Performance Summary",
        summary_data=summary_data
    )
    figure_paths.append(summary_fig)
    
    # 9. Compile PDF report
    print("   Compiling PDF report...")
    pdf_path = fig_gen.compile_pdf_report(
        figure_paths=figure_paths,
        title="J1 Figure Generator Demonstration",
        author="Michael Maloney"
    )
    
    print(f"\n✅ Demonstration completed!")
    print(f"📊 Generated {len(figure_paths)} figures")
    print(f"📄 PDF Report: {pdf_path}")
    print(f"📁 All figures saved in: {output_dir}")
    
    return pdf_path

if __name__ == "__main__":
    generate_demo_figures() 