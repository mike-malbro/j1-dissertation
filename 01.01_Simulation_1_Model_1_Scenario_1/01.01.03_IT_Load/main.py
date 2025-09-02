#!/usr/bin/env python3
"""
Module: 01.02.02 - J1 IT Load
Description: Python script generates PNG of IT load analysis, then inserts into PDF as Figure.
Author: Michael Logan Maloney
Timestamp: 2025-08-29
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

def generate_it_load_analysis():
    """
    Generate IT load analysis and create professional PNG figure.
    Returns the path to the generated PNG file.
    """
    # Input Parameters
    TIME_STEPS = 1440  # Total simulation steps (minutes in a day)
    CONSTANT_LOAD = 30.0  # Steady IT load in kW
    SPIKE_LOAD = 60.0  # Peak load during spikes in kW
    SPIKE_DURATION = 720  # Length of each spike in steps
    SPIKE_INTERVAL = 1440  # Time between spike starts in steps
    
    def generate_it_load_data():
        """Generate synthetic IT load data for data center simulation."""
        time = pd.date_range(start='2025-07-15 00:00', periods=TIME_STEPS, freq='min')
        Q_IT_constant = np.full(TIME_STEPS, CONSTANT_LOAD)
        Q_IT_spikes = np.zeros(TIME_STEPS)
        
        for t in range(0, TIME_STEPS, SPIKE_INTERVAL):
            end = min(t + SPIKE_DURATION, TIME_STEPS)
            Q_IT_spikes[t:end] = SPIKE_LOAD - CONSTANT_LOAD
        
        Q_IT_total = Q_IT_constant + Q_IT_spikes
        
        df = pd.DataFrame({
            'Time': time,
            'Total_Load': Q_IT_total,
            'Constant_Load': Q_IT_constant,
            'Spike_Load': Q_IT_spikes
        })
        df.set_index('Time', inplace=True)
        return df
    
    def analyze_load_data(df):
        """Perform statistical analysis of IT load data."""
        stats_dict = {
            'Number of Data Points': len(df),
            'Time Range Start': df.index.min().strftime('%Y-%m-%d %H:%M:%S'),
            'Time Range End': df.index.max().strftime('%Y-%m-%d %H:%M:%S'),
            'Mean Total Load (kW)': df['Total_Load'].mean(),
            'Mean Constant Load (kW)': df['Constant_Load'].mean(),
            'Mean Spike Load (kW)': df['Spike_Load'][df['Spike_Load'] > 0].mean(),
            'Total Energy (kWh)': df['Total_Load'].sum() / 60,
            'Constant Energy (kWh)': df['Constant_Load'].sum() / 60,
            'Spike Energy (kWh)': df['Spike_Load'].sum() / 60,
            'Peak-to-Constant Ratio': df['Total_Load'].max() / df['Constant_Load'].mean(),
            'Spike Frequency (per day)': TIME_STEPS / SPIKE_INTERVAL,
            'Spike Duration (minutes)': SPIKE_DURATION
        }
        return stats_dict
    
    # Generate data and statistics
    df = generate_it_load_data()
    stats_dict = analyze_load_data(df)
    
    # Set professional styling with higher quality
    sns.set_style("whitegrid")
    plt.rcParams['font.size'] = 14
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 12
    plt.rcParams['figure.dpi'] = 600
    plt.rcParams['savefig.dpi'] = 600
    
    # Create hours array for x-axis
    hours = np.arange(TIME_STEPS) / 60.0
    
    # Create the main IT Load Profile figure with higher resolution
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Plot the IT load profile
    ax.plot(hours, df['Total_Load'], color='#2E86AB', linewidth=2.5, label='Total IT Load')
    ax.plot(hours, df['Constant_Load'], color='#A23B72', linewidth=2, linestyle='--', alpha=0.7, label='Constant Load (30 kW)')
    
    # Add spike load overlay
    spike_mask = df['Spike_Load'] > 0
    if spike_mask.any():
        ax.fill_between(hours, df['Constant_Load'], df['Total_Load'], 
                       where=spike_mask, alpha=0.3, color='#F18F01', label='AI Training Spike Load')
    
    # Customize the plot
    ax.set_xlabel('Time (hours)', fontweight='bold')
    ax.set_ylabel('IT Load (kW)', fontweight='bold')
    ax.set_title('J1 - Data Center IT Load Profile\nHarrisburg Case Study: 30 kW Base + 12hr 60 kW AI Training Load', 
                fontsize=18, fontweight='bold', pad=20)
    
    # Set axis limits and ticks
    ax.set_xlim(0, 24)
    ax.set_xticks(np.arange(0, 25, 4))
    ax.set_ylim(0, 70)
    ax.grid(True, alpha=0.3)
    
    # Add statistical annotations
    stats_text = f"Mean Load: {stats_dict['Mean Total Load (kW)']:.1f} kW\nPeak Load: {df['Total_Load'].max():.1f} kW\nTotal Energy: {stats_dict['Total Energy (kWh)']:.0f} kWh"
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    # Add legend
    ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
    
    # Tight layout and save
    plt.tight_layout()
    
    # Save as ultra-high-quality PNG
    png_path = "output/it_load_analysis.png"
    plt.savefig(png_path, dpi=600, bbox_inches='tight', facecolor='white', 
                format='png', transparent=False, pad_inches=0.1)
    plt.close()
    
    print(f"✅ IT Load analysis PNG generated: {png_path}")
    return png_path

def generate_it_load_figure():
    """
    Generate the IT Load figure page using the same boilerplate as other figure modules.
    """
    print("📊 Generating IT Load Analysis page...")
    
    # Generate the PNG first
    png_path = generate_it_load_analysis()
    
    # Create PDF page with the generated PNG
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.pyplot as plt
    from PIL import Image
    
    # Create figure with 8.5 x 11 inch page
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Add title
    title_text = "J1 IT Load Analysis"
    ax.text(0.5, 10.5, title_text, fontsize=16, fontweight='bold', 
            ha='center', va='center')
    
    # Load and display the generated PNG
    try:
        img = Image.open(png_path)
        
        # Calculate optimal size to fit page width with margins
        img_width = 7.5  # Large but with margins for centering
        aspect_ratio = img.height / img.width
        img_height = img_width * aspect_ratio
        
        # Ensure image doesn't exceed available vertical space
        max_height = 6.5  # Large but with margins for centering
        if img_height > max_height:
            img_height = max_height
            img_width = img_height / aspect_ratio
        
        # Center the image horizontally and vertically
        x_pos = (8.5 - img_width) / 2  # Center horizontally
        y_pos = (11 - img_height) / 2  # Center vertically
        
        # Add image
        ax.imshow(img, extent=[x_pos, x_pos + img_width, y_pos, y_pos + img_height])
        
        # Add figure number and description
        figure_text = "Figure 1.2.02"
        ax.text(x_pos, y_pos - 0.5, figure_text, fontsize=12, fontweight='bold')
        
        description_text = "Data Center IT Load Profile showing constant 30 kW base load with 12-hour AI training spikes to 60 kW."
        ax.text(x_pos, y_pos - 0.8, description_text, fontsize=10, wrap=True)
        
        # Add source information
        source_text = "Source: Generated by Python analysis script - IT Load Simulation"
        ax.text(x_pos, y_pos - 1.1, source_text, fontsize=9, style='italic')
        
    except Exception as e:
        print(f"❌ Error loading generated PNG: {e}")
        # Fallback text
        ax.text(4.25, 5.5, "IT Load Analysis Figure\n(PNG generation failed)", 
                fontsize=14, ha='center', va='center', 
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    # Add page number and module info
    ax.text(4.25, 0.5, "10", fontsize=10, ha='center', va='center')
    ax.text(0.5, 0.5, "Module: 01.02.02 - J1 IT Load | Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            fontsize=8, ha='left', va='center')
    
    # Save PDF
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"output/it_load_analysis_01.02.02_{timestamp}.pdf"
    
    with PdfPages(pdf_filename) as pdf:
        pdf.savefig(fig, bbox_inches='tight')
    
    plt.close()
    
    print(f"✅ IT Load Analysis page generated: {pdf_filename}")
    return pdf_filename

if __name__ == "__main__":
    try:
        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)
        
        # Generate the IT Load figure
        pdf_path = generate_it_load_figure()
        
        print(f"📄 IT Load Analysis module completed successfully: {pdf_path}")
        
    except Exception as e:
        print(f"❌ Error in IT Load Analysis module: {e}")
        sys.exit(1)
