#!/usr/bin/env python3
"""
Module 01.02.03 - Room Temperature Versus Timestep Figure
Michael Logan Maloney PhD Dissertation Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Professional PhD-level figure generation with high precision and reproducibility.
Legends placed at bottom right below x-axis to avoid chart interference.
Annotations positioned at bottom left for statistical information.
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates
from datetime import datetime
from pathlib import Path
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

def download_fresh_csv_data():
    """Download fresh CSV data from Google Drive"""
    try:
        # Import Google Drive helpers
        sys.path.append(str(Path(__file__).parent / ".." / ".." / "0Z.00_Google_Sheet_Helper_Functions"))
        from google_drive_helpers import download_asset
        
        # Google Drive CSV link - Simulation 2 Data Source
        csv_url = "https://drive.google.com/file/d/1M3j1jGtYs6W3xJhjLGt5IbbQOoQ5mAKq/view?usp=drive_link"
        
        print(f"📥 Downloading fresh CSV data from Google Drive: {csv_url}")
        
        # Download the CSV file
        csv_path = download_asset(
            url=csv_url,
            module_id="01.02.03",
            filename="simulation_data.csv"
        )
        
        if csv_path and Path(csv_path).exists():
            print(f"✅ Fresh CSV downloaded successfully: {csv_path}")
            return csv_path
        else:
            print(f"⚠️ Google Drive download failed")
            return None
            
    except Exception as e:
        print(f"⚠️ Google Drive error: {e}")
        return None

def load_simulation_data():
    """Load simulation data from CSV with fresh download"""
    try:
        # Step 1: Try to download fresh data from Google Drive
        fresh_csv_path = download_fresh_csv_data()
        
        # Use the freshly downloaded CSV if available, otherwise fallback
        if fresh_csv_path:
            csv_path = fresh_csv_path
        else:
            # Fallback to downloads directory
            csv_path = Path(__file__).parent / ".." / ".." / "downloads" / "simulation_data.csv"
            
            if not csv_path.exists():
                # Final fallback to 01.02.02 output
                csv_path = Path(__file__).parent / ".." / "01.02.02_Simulation_Data_CSV" / "output" / "simulation_data.csv"
        
        if csv_path.exists():
            print(f"📊 Loading simulation data from: {csv_path}")
            df = pd.read_csv(csv_path)
            print(f"📊 CSV loaded successfully. Shape: {df.shape}, Columns: {df.columns.tolist()}")
            
            # Handle different CSV formats
            if 'timestep' in df.columns and 'room_temperature' in df.columns:
                # Original format
                print(f"📊 Using original CSV format")
                # Convert to datetime index for professional plotting
                start_time = pd.Timestamp('2024-01-01 00:00:00')
                time_index = [start_time + pd.Timedelta(hours=t) for t in df['timestep']]
                df.index = time_index
                
                # Rename columns for consistency
                df = df.rename(columns={'room_temperature': 'Temperature'})
                
                # Add Hour column for analysis (timesteps are in 0.25-hour increments)
                df['Hour'] = df['timestep']  # This is already in hours (0.0, 0.25, 0.5, etc.)
                
            elif 'Time|min' in df.columns and 'roo.rooVol.T|°C' in df.columns:
                # New format (version 2)
                print(f"📊 Using new CSV format (version 2)")
                # Rename columns for consistency
                df = df.rename(columns={
                    'Time|min': 'timestep',
                    'roo.rooVol.T|°C': 'Temperature'
                })
                
                # Convert timestep from minutes to hours
                df['timestep'] = df['timestep'] / 60.0
                
                # Convert to datetime index for professional plotting
                start_time = pd.Timestamp('2024-01-01 00:00:00')
                time_index = [start_time + pd.Timedelta(hours=t) for t in df['timestep']]
                df.index = time_index
                
                # Add Hour column for analysis
                df['Hour'] = df['timestep']
                
            else:
                print(f"⚠️ Unknown CSV format, columns: {df.columns.tolist()}")
                raise ValueError(f"Unknown CSV format")
            
            print(f"📊 Data processing complete. Final shape: {df.shape}")
            return df
        else:
            print(f"⚠️ No simulation data found, generating sample data")
            return generate_sample_data()
            
    except Exception as e:
        print(f"⚠️ Error loading data: {e}, generating sample data")
        return generate_sample_data()

def generate_sample_data():
    """Generate professional sample room temperature data for demonstration"""
    print("📊 Generating professional sample room temperature data...")
    
    # Generate realistic timesteps (24 hours with 15-minute intervals)
    timesteps = np.arange(0, 24, 0.25)  # 96 data points
    
    # Generate realistic room temperature data with daily cycles and noise
    base_temp = 22.0  # Base temperature in Celsius
    daily_variation = 2.5 * np.sin(2 * np.pi * timesteps / 24)  # Daily cycle
    load_variation = 1.0 * np.sin(2 * np.pi * timesteps / 8)  # Load variation
    random_variation = np.random.normal(0, 0.3, len(timesteps))  # Controlled noise
    
    room_temperature = base_temp + daily_variation + load_variation + random_variation
    
    # Create professional DataFrame with datetime index
    start_time = pd.Timestamp('2024-01-01 00:00:00')
    time_index = [start_time + pd.Timedelta(hours=t) for t in timesteps]
    
    df = pd.DataFrame({
        'Temperature': room_temperature,
        'Hour': timesteps,
        'Day_Period': ['Day' if 6 <= t <= 18 else 'Night' for t in timesteps]
    }, index=time_index)
    
    return df

def create_room_temperature_figure(df):
    """Create simple temperature versus timestep plots for 6 different time periods"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Define the 6 time periods based on day numbers (1-365 for the year)
    time_periods = [
        {
            'id': 'ts_01_ANNUAL',
            'name': 'Annual Analysis',
            'start_day': 1,
            'end_day': 365,
            'description': 'Full year temperature analysis (January 1 - December 31)'
        },
        {
            'id': 'ts_02_TYPICALWEEK1_summer',
            'name': 'Typical Week 1 - Summer',
            'start_day': 157,
            'end_day': 163,
            'description': 'Summer week analysis (July 22 - July 28)'
        },
        {
            'id': 'ts_03_TYPICALWEEK2_spring',
            'name': 'Typical Week 2 - Spring',
            'start_day': 248,
            'end_day': 254,
            'description': 'Spring week analysis (April 22 - April 28)'
        },
        {
            'id': 'ts_04_TYPICALWEEK3_fall',
            'name': 'Typical Week 3 - Fall',
            'start_day': 65,
            'end_day': 71,
            'description': 'Fall week analysis (October 22 - October 28)'
        },
        {
            'id': 'ts_05_TYPICALWEEK4_winter',
            'name': 'Typical Week 4 - Winter',
            'start_day': 338,
            'end_day': 344,
            'description': 'Winter week analysis (January 22 - January 28)'
        },
        {
            'id': 'ts_06_CRITICALday',
            'name': 'Critical Day',
            'start_day': 169,
            'end_day': 169,
            'description': 'Critical day analysis (July 16)'
        }
    ]
    
    # Step 1: Calculate global min and max for consistent y-axis scaling
    global_temp_min = df['Temperature'].min()
    global_temp_max = df['Temperature'].max()
    
    # Add some padding to the y-axis limits
    temp_range = global_temp_max - global_temp_min
    y_min = global_temp_min - (temp_range * 0.05)  # 5% padding below
    y_max = global_temp_max + (temp_range * 0.05)  # 5% padding above
    
    print(f"📊 Global temperature range: {global_temp_min:.2f}°C to {global_temp_max:.2f}°C")
    print(f"📊 Y-axis limits: {y_min:.2f}°C to {y_max:.2f}°C")
    
    # Step 2: Generate high-quality PNGs for each time period
    png_files = []
    
    # Process Annual Analysis (single plot)
    annual_period = time_periods[0]
    start_hour = (annual_period['start_day'] - 1) * 24
    end_hour = annual_period['end_day'] * 24
    annual_data = df[(df['Hour'] >= start_hour) & (df['Hour'] <= end_hour)].copy()
    annual_data['Relative_Time'] = (annual_data['Hour'] - start_hour) / 24
    annual_data['Relative_Time_Minutes'] = annual_data['Relative_Time'] * 24 * 60
    
    # Create minute-by-minute timesteps for annual
    start_minutes = annual_data['Relative_Time_Minutes'].min()
    end_minutes = annual_data['Relative_Time_Minutes'].max()
    minute_timesteps = np.arange(start_minutes, end_minutes + 1, 1)
    
    # Interpolate temperature data to minute resolution
    from scipy.interpolate import interp1d
    f_interp = interp1d(annual_data['Relative_Time_Minutes'], annual_data['Temperature'], 
                       kind='linear', fill_value='extrapolate')
    temperature_minutes = f_interp(minute_timesteps)
    
    # Create Annual Analysis plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(minute_timesteps, temperature_minutes, 'b-', linewidth=1, label='Room Temperature', alpha=0.8)
    ax.axhline(y=25, color='red', linestyle='--', linewidth=1.5, label='Setpoint (25°C)')
    ax.set_xlabel('Timestep (Minutes)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Temperature (°C)', fontsize=14, fontweight='bold')
    ax.set_title(f'{annual_period["name"]} - Temperature vs Timestep (Minute Resolution)', fontsize=16, fontweight='bold')
    ax.set_ylim(y_min, y_max)  # Use global y-axis limits
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=10)
    period_info = f"Period: Day {annual_period['start_day']} - Day {annual_period['end_day']} | Resolution: 1 minute"
    ax.text(0.02, 0.98, period_info, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    plt.tight_layout()
    annual_png = output_dir / f"{annual_period['id']}_{timestamp}.png"
    plt.savefig(annual_png, dpi=300, bbox_inches='tight')
    plt.close()
    png_files.append(annual_png)
    print(f"✅ Generated PNG for {annual_period['name']}: {annual_period['id']}_{timestamp}.png")
    
    # Process 4 Typical Weeks (2x2 layout)
    weekly_periods = time_periods[1:5]  # Summer, Spring, Fall, Winter
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    for i, period in enumerate(weekly_periods):
        start_hour = (period['start_day'] - 1) * 24
        end_hour = period['end_day'] * 24
        period_data = df[(df['Hour'] >= start_hour) & (df['Hour'] <= end_hour)].copy()
        period_data['Relative_Time'] = (period_data['Hour'] - start_hour) / 24
        period_data['Relative_Time_Minutes'] = period_data['Relative_Time'] * 24 * 60
        
        # Create minute-by-minute timesteps
        start_minutes = period_data['Relative_Time_Minutes'].min()
        end_minutes = period_data['Relative_Time_Minutes'].max()
        minute_timesteps = np.arange(start_minutes, end_minutes + 1, 1)
        
        # Interpolate temperature data
        f_interp = interp1d(period_data['Relative_Time_Minutes'], period_data['Temperature'], 
                           kind='linear', fill_value='extrapolate')
        temperature_minutes = f_interp(minute_timesteps)
        
        # Plot on subplot
        ax = axes[i]
        ax.plot(minute_timesteps, temperature_minutes, 'b-', linewidth=1, label='Room Temperature', alpha=0.8)
        ax.axhline(y=25, color='red', linestyle='--', linewidth=1.5, label='Setpoint (25°C)')
        ax.set_xlabel('Timestep (Minutes)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Temperature (°C)', fontsize=12, fontweight='bold')
        ax.set_title(f'{period["name"]} (Days {period["start_day"]}-{period["end_day"]})', fontsize=14, fontweight='bold')
        ax.set_ylim(y_min, y_max)  # Use global y-axis limits
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right', fontsize=8)
        
        print(f"📊 Found {len(period_data)} data points for {period['name']} (days {period['start_day']}-{period['end_day']})")
    
    plt.tight_layout()
    weekly_png = output_dir / f"weekly_comparison_{timestamp}.png"
    plt.savefig(weekly_png, dpi=300, bbox_inches='tight')
    plt.close()
    png_files.append(weekly_png)
    print(f"✅ Generated PNG for Weekly Comparison: weekly_comparison_{timestamp}.png")
    
    # Process Critical Day (single plot)
    critical_period = time_periods[5]
    start_hour = (critical_period['start_day'] - 1) * 24
    end_hour = critical_period['end_day'] * 24
    critical_data = df[(df['Hour'] >= start_hour) & (df['Hour'] <= end_hour)].copy()
    critical_data['Relative_Time'] = (critical_data['Hour'] - start_hour) / 24
    critical_data['Relative_Time_Minutes'] = critical_data['Relative_Time'] * 24 * 60
    
    # Create minute-by-minute timesteps for critical day
    start_minutes = critical_data['Relative_Time_Minutes'].min()
    end_minutes = critical_data['Relative_Time_Minutes'].max()
    minute_timesteps = np.arange(start_minutes, end_minutes + 1, 1)
    
    # Interpolate temperature data
    f_interp = interp1d(critical_data['Relative_Time_Minutes'], critical_data['Temperature'], 
                       kind='linear', fill_value='extrapolate')
    temperature_minutes = f_interp(minute_timesteps)
    
    # Create Critical Day plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(minute_timesteps, temperature_minutes, 'b-', linewidth=1, label='Room Temperature', alpha=0.8)
    ax.axhline(y=25, color='red', linestyle='--', linewidth=1.5, label='Setpoint (25°C)')
    ax.set_xlabel('Timestep (Minutes)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Temperature (°C)', fontsize=14, fontweight='bold')
    ax.set_title(f'{critical_period["name"]} - Temperature vs Timestep (Minute Resolution)', fontsize=16, fontweight='bold')
    ax.set_ylim(y_min, y_max)  # Use global y-axis limits
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=10)
    period_info = f"Period: Day {critical_period['start_day']} - Day {critical_period['end_day']} | Resolution: 1 minute"
    ax.text(0.02, 0.98, period_info, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    plt.tight_layout()
    critical_png = output_dir / f"{critical_period['id']}_{timestamp}.png"
    plt.savefig(critical_png, dpi=300, bbox_inches='tight')
    plt.close()
    png_files.append(critical_png)
    print(f"✅ Generated PNG for {critical_period['name']}: {critical_period['id']}_{timestamp}.png")
    
    # Step 2: Create multi-page PDF with new layout (like Module 01.0B)
    output_file = output_dir / f"room_temperature_figure_01.02.03_{timestamp}.pdf"
    
    with PdfPages(output_file) as pdf:
        
        # Page 1: Annual Analysis
        fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
        ax.set_xlim(0, 8.5)
        ax.set_ylim(0, 11)
        ax.axis('off')
        
        # Title - Left justified with book-style spacing (like 01.0B)
        title_text = f"Room Temperature Analysis - {annual_period['name']}"
        ax.text(0.1, 9.9, title_text, fontsize=18, fontweight='bold', 
                ha='left', va='center', fontfamily='Arial', color='black')
        
        # Add the Annual PNG - prominently displayed like 01.0B
        try:
            img = Image.open(annual_png)
            
            # Calculate optimal size to fit page width with margins (like 01.0B)
            img_width = 6.5
            aspect_ratio = img.height / img.width
            img_height = img_width * aspect_ratio
            
            # Ensure image doesn't exceed available vertical space
            max_height = 5.5  # Larger for single image
            if img_height > max_height:
                img_height = max_height
                img_width = img_height / aspect_ratio
            
            # Center the image horizontally
            x_pos = (8.5 - img_width) / 2
            y_pos = 8 - img_height  # Position below title
            
            # Add image
            ax.imshow(img, extent=[x_pos, x_pos + img_width, y_pos, y_pos + img_height])
            
            # Figure number and description (like 01.0B)
            ax.text(0.1, y_pos - 0.8, "Figure 1", fontsize=14, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial', color='black')
            
            ax.text(0.1, y_pos - 1.2, annual_period['description'], 
                    fontsize=12, fontweight='normal', ha='left', va='center', 
                    fontfamily='Arial', color='black')
            
        except Exception as e:
            print(f"⚠️ Warning: Could not load annual image: {e}")
        
        # Page number - centered like 01.0B
        ax.text(4.25, 0.5, "15", fontsize=14, fontweight='normal',
                ha='center', va='center', fontfamily='Arial', color='black')
        
        # Timestamp - left justified like 01.0B
        timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ax.text(0.1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='gray')
        
        # Module identifier - left justified like 01.0B
        module_text = "Module: 01.02.03 - Room Temperature Analysis"
        ax.text(0.1, 0.1, module_text, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='gray')
        
        pdf.savefig(fig, dpi=300)
        plt.close()
        
        # Page 2: Weekly Comparison (2x2 layout)
        fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
        ax.set_xlim(0, 8.5)
        ax.set_ylim(0, 11)
        ax.axis('off')
        
        # Title - Left justified with book-style spacing (like 01.0B)
        title_text = "Room Temperature Analysis - Weekly Comparison"
        ax.text(0.1, 9.9, title_text, fontsize=18, fontweight='bold', 
                ha='left', va='center', fontfamily='Arial', color='black')
        
        # Add the Weekly Comparison PNG - prominently displayed like 01.0B
        try:
            img = Image.open(weekly_png)
            
            # Calculate optimal size to fit page width with margins (like 01.0B)
            img_width = 6.5
            aspect_ratio = img.height / img.width
            img_height = img_width * aspect_ratio
            
            # Ensure image doesn't exceed available vertical space
            max_height = 5.5  # Larger for single image
            if img_height > max_height:
                img_height = max_height
                img_width = img_height / aspect_ratio
            
            # Center the image horizontally
            x_pos = (8.5 - img_width) / 2
            y_pos = 8 - img_height  # Position below title
            
            # Add image
            ax.imshow(img, extent=[x_pos, x_pos + img_width, y_pos, y_pos + img_height])
            
            # Figure number and description (like 01.0B)
            ax.text(0.1, y_pos - 0.8, "Figure 2", fontsize=14, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial', color='black')
            
            ax.text(0.1, y_pos - 1.2, "Comparison of four typical weeks: Summer, Spring, Fall, and Winter", 
                    fontsize=12, fontweight='normal', ha='left', va='center', 
                    fontfamily='Arial', color='black')
            
        except Exception as e:
            print(f"⚠️ Warning: Could not load weekly comparison image: {e}")
        
        # Page number - centered like 01.0B
        ax.text(4.25, 0.5, "16", fontsize=14, fontweight='normal',
                ha='center', va='center', fontfamily='Arial', color='black')
        
        # Timestamp - left justified like 01.0B
        timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ax.text(0.1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='gray')
        
        # Module identifier - left justified like 01.0B
        module_text = "Module: 01.02.03 - Room Temperature Analysis"
        ax.text(0.1, 0.1, module_text, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='gray')
        
        pdf.savefig(fig, dpi=300)
        plt.close()
        
        # Page 3: Critical Day
        fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
        ax.set_xlim(0, 8.5)
        ax.set_ylim(0, 11)
        ax.axis('off')
        
        # Title - Left justified with book-style spacing (like 01.0B)
        title_text = f"Room Temperature Analysis - {critical_period['name']}"
        ax.text(0.1, 9.9, title_text, fontsize=18, fontweight='bold', 
                ha='left', va='center', fontfamily='Arial', color='black')
        
        # Add the Critical Day PNG - prominently displayed like 01.0B
        try:
            img = Image.open(critical_png)
            
            # Calculate optimal size to fit page width with margins (like 01.0B)
            img_width = 6.5
            aspect_ratio = img.height / img.width
            img_height = img_width * aspect_ratio
            
            # Ensure image doesn't exceed available vertical space
            max_height = 5.5  # Larger for single image
            if img_height > max_height:
                img_height = max_height
                img_width = img_height / aspect_ratio
            
            # Center the image horizontally
            x_pos = (8.5 - img_width) / 2
            y_pos = 8 - img_height  # Position below title
            
            # Add image
            ax.imshow(img, extent=[x_pos, x_pos + img_width, y_pos, y_pos + img_height])
            
            # Figure number and description (like 01.0B)
            ax.text(0.1, y_pos - 0.8, "Figure 3", fontsize=14, fontweight='bold',
                    ha='left', va='center', fontfamily='Arial', color='black')
            
            ax.text(0.1, y_pos - 1.2, critical_period['description'], 
                    fontsize=12, fontweight='normal', ha='left', va='center', 
                    fontfamily='Arial', color='black')
            
        except Exception as e:
            print(f"⚠️ Warning: Could not load critical day image: {e}")
        
        # Page number - centered like 01.0B
        ax.text(4.25, 0.5, "17", fontsize=14, fontweight='normal',
                ha='center', va='center', fontfamily='Arial', color='black')
        
        # Timestamp - left justified like 01.0B
        timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ax.text(0.1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='gray')
        
        # Module identifier - left justified like 01.0B
        module_text = "Module: 01.02.03 - Room Temperature Analysis"
        ax.text(0.1, 0.1, module_text, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='gray')
        
        pdf.savefig(fig, dpi=300)
        plt.close()
    
    print(f"✅ Room Temperature Analysis generated: {output_file}")
    print(f"📊 High-quality PNGs created: {len(png_files)} files")
    return str(output_file)
    
    # Step 2: Create multi-page PDF with one figure per page (like Module 01.0B)
    output_file = output_dir / f"room_temperature_figure_01.02.03_{timestamp}.pdf"
    
    with PdfPages(output_file) as pdf:
        
        # Page 1: Time Series Plot
        fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
        ax.set_xlim(0, 8.5)
        ax.set_ylim(0, 11)
        ax.axis('off')
        
        # Title - Left justified with book-style spacing (like 01.0B)
        title_text = "Room Temperature Analysis"
        ax.text(0.1, 9.9, title_text, fontsize=18, fontweight='bold', 
                ha='left', va='center', fontfamily='Arial', color='black')
        
        # Add the Time Series PNG - prominently displayed like 01.0B
        if time_series_png.exists():
            try:
                img = Image.open(time_series_png)
                
                # Calculate optimal size to fit page width with margins (like 01.0B)
                img_width = 6.5
                aspect_ratio = img.height / img.width
                img_height = img_width * aspect_ratio
                
                # Ensure image doesn't exceed available vertical space
                max_height = 5.5  # Larger for single image
                if img_height > max_height:
                    img_height = max_height
                    img_width = img_height / aspect_ratio
                
                # Center the image horizontally
                x_pos = (8.5 - img_width) / 2
                y_pos = 8 - img_height  # Position below title
                
                # Add image
                ax.imshow(img, extent=[x_pos, x_pos + img_width, y_pos, y_pos + img_height])
                
                # Figure number and description (like 01.0B)
                ax.text(0.1, y_pos - 0.8, "Figure 1", fontsize=14, fontweight='bold',
                        ha='left', va='center', fontfamily='Arial', color='black')
                
                ax.text(0.1, y_pos - 1.2, "Room temperature time series analysis with target and limit lines.", 
                        fontsize=12, fontweight='normal', ha='left', va='center', 
                        fontfamily='Arial', color='black')
                
            except Exception as e:
                print(f"⚠️ Warning: Could not load time series image: {e}")
        
        # Page number - centered like 01.0B
        ax.text(4.25, 0.5, "15", fontsize=14, fontweight='normal',
                ha='center', va='center', fontfamily='Arial', color='black')
        
        # Timestamp - left justified like 01.0B
        timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ax.text(0.1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='gray')
        
        # Module identifier - left justified like 01.0B
        module_text = "Module: 01.02.03 - Room Temperature Analysis"
        ax.text(0.1, 0.1, module_text, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='gray')
        
        pdf.savefig(fig, dpi=300)
        plt.close()
        
        # Page 2: Distribution Plot
        fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
        ax.set_xlim(0, 8.5)
        ax.set_ylim(0, 11)
        ax.axis('off')
        
        # Title - Left justified with book-style spacing (like 01.0B)
        title_text = "Room Temperature Analysis"
        ax.text(0.1, 9.9, title_text, fontsize=18, fontweight='bold', 
                ha='left', va='center', fontfamily='Arial', color='black')
        
        # Add the Distribution PNG - prominently displayed like 01.0B
        if distribution_png.exists():
            try:
                img = Image.open(distribution_png)
                
                # Calculate optimal size to fit page width with margins (like 01.0B)
                img_width = 6.5
                aspect_ratio = img.height / img.width
                img_height = img_width * aspect_ratio
                
                # Ensure image doesn't exceed available vertical space
                max_height = 5.5  # Larger for single image
                if img_height > max_height:
                    img_height = max_height
                    img_width = img_height / aspect_ratio
                
                # Center the image horizontally
                x_pos = (8.5 - img_width) / 2
                y_pos = 8 - img_height  # Position below title
                
                # Add image
                ax.imshow(img, extent=[x_pos, x_pos + img_width, y_pos, y_pos + img_height])
                
                # Figure number and description (like 01.0B)
                ax.text(0.1, y_pos - 0.8, "Figure 2", fontsize=14, fontweight='bold',
                        ha='left', va='center', fontfamily='Arial', color='black')
                
                ax.text(0.1, y_pos - 1.2, "Temperature distribution histogram with statistical measures.", 
                        fontsize=12, fontweight='normal', ha='left', va='center', 
                        fontfamily='Arial', color='black')
                
            except Exception as e:
                print(f"⚠️ Warning: Could not load distribution image: {e}")
        
        # Page number - centered like 01.0B
        ax.text(4.25, 0.5, "16", fontsize=14, fontweight='normal',
                ha='center', va='center', fontfamily='Arial', color='black')
        
        # Timestamp - left justified like 01.0B
        timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ax.text(0.1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='gray')
        
        # Module identifier - left justified like 01.0B
        module_text = "Module: 01.02.03 - Room Temperature Analysis"
        ax.text(0.1, 0.1, module_text, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='gray')
        
        pdf.savefig(fig, dpi=300)
        plt.close()
        
        # Page 3: Daily Pattern Plot
        fig, ax = plt.subplots(figsize=(8.5, 11), facecolor='white')
        ax.set_xlim(0, 8.5)
        ax.set_ylim(0, 11)
        ax.axis('off')
        
        # Title - Left justified with book-style spacing (like 01.0B)
        title_text = "Room Temperature Analysis"
        ax.text(0.1, 9.9, title_text, fontsize=18, fontweight='bold', 
                ha='left', va='center', fontfamily='Arial', color='black')
        
        # Add the Pattern PNG - prominently displayed like 01.0B
        if pattern_png.exists():
            try:
                img = Image.open(pattern_png)
                
                # Calculate optimal size to fit page width with margins (like 01.0B)
                img_width = 6.5
                aspect_ratio = img.height / img.width
                img_height = img_width * aspect_ratio
                
                # Ensure image doesn't exceed available vertical space
                max_height = 5.5  # Larger for single image
                if img_height > max_height:
                    img_height = max_height
                    img_width = img_height / aspect_ratio
                
                # Center the image horizontally
                x_pos = (8.5 - img_width) / 2
                y_pos = 8 - img_height  # Position below title
                
                # Add image
                ax.imshow(img, extent=[x_pos, x_pos + img_width, y_pos, y_pos + img_height])
                
                # Figure number and description (like 01.0B)
                ax.text(0.1, y_pos - 0.8, "Figure 3", fontsize=14, fontweight='bold',
                        ha='left', va='center', fontfamily='Arial', color='black')
                
                ax.text(0.1, y_pos - 1.2, "Daily temperature pattern with hourly means.", 
                        fontsize=12, fontweight='normal', ha='left', va='center', 
                        fontfamily='Arial', color='black')
                
            except Exception as e:
                print(f"⚠️ Warning: Could not load pattern image: {e}")
        
        # Page number - centered like 01.0B
        ax.text(4.25, 0.5, "17", fontsize=14, fontweight='normal',
                ha='center', va='center', fontfamily='Arial', color='black')
        
        # Timestamp - left justified like 01.0B
        timestamp_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ax.text(0.1, 0.3, timestamp_text, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='gray')
        
        # Module identifier - left justified like 01.0B
        module_text = "Module: 01.02.03 - Room Temperature Analysis"
        ax.text(0.1, 0.1, module_text, fontsize=10, fontweight='normal',
                ha='left', va='center', fontfamily='Arial', color='gray')
        
        pdf.savefig(fig, dpi=300)
        plt.close()
    
    print(f"✅ Room Temperature Analysis generated: {output_file}")
    print(f"📊 High-quality PNGs created: {len(png_files)} files")
    return str(output_file)

def main():
    """Main function to generate Room Temperature Figure"""
    print("🎨 Generating Room Temperature Versus Timestep Figure (Simulation 2 - NEW DATA)...")
    
    try:
        # Load simulation data
        df = load_simulation_data()
        
        if df is not None:
            # Generate the figure
            output_file = create_room_temperature_figure(df)
            print(f"📄 Room Temperature Figure created successfully: {output_file}")
            return True
        else:
            print(f"❌ Failed to load simulation data")
            return False
            
    except Exception as e:
        print(f"❌ Error generating Room Temperature Figure: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
