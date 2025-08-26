# J1 Standardized Figure Generator

## Overview

This module provides a professional, standardized figure generation system for the J1 project. It incorporates PhD-level best practices for data visualization and ensures consistent, high-quality output across all modules.

## Key Features

- **Professional Styling**: Arial fonts, black/white/gray color scheme, clean layouts
- **Consistent Formatting**: Standardized font sizes, spacing, and annotations
- **PhD-Level Precision**: Statistical annotations, correlation analysis, error handling
- **Modular Design**: Easy to integrate into any J1 module
- **PDF Compilation**: Automatic compilation of figures into professional reports

## Quick Start

### Basic Usage

```python
from pathlib import Path
from datetime import datetime
from modules.figure_generator import FigureGenerator

# Initialize
output_dir = Path("output")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
fig_gen = FigureGenerator(output_dir, timestamp)

# Create a scatter plot
fig_path = fig_gen.create_scatter_plot(
    x_data=temperatures,
    y_data=humidities,
    title="Temperature vs Humidity",
    x_label="Temperature (°F)",
    y_label="Humidity (%)",
    add_regression=True,
    add_stats=True
)
```

### Complete Example

```python
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from modules.figure_generator import FigureGenerator

def analyze_data_center_performance():
    # Setup
    output_dir = Path("output")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fig_gen = FigureGenerator(output_dir, timestamp)
    
    # Generate sample data
    dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
    temperatures = 70 + 10 * np.random.randn(len(dates))
    humidities = 50 + 15 * np.random.randn(len(dates))
    
    figure_paths = []
    
    # 1. Time series plot
    fig1 = fig_gen.create_time_series_plot(
        time_data=dates,
        y_data=temperatures,
        title="Data Center Temperature Over Time",
        y_label="Temperature (°F)",
        add_mean_line=True,
        add_rolling_avg=True
    )
    figure_paths.append(fig1)
    
    # 2. Scatter plot with regression
    fig2 = fig_gen.create_scatter_plot(
        x_data=temperatures,
        y_data=humidities,
        title="Temperature vs Humidity Correlation",
        x_label="Temperature (°F)",
        y_label="Humidity (%)",
        add_regression=True,
        add_stats=True
    )
    figure_paths.append(fig2)
    
    # 3. Compile PDF report
    pdf_path = fig_gen.compile_pdf_report(
        figure_paths=figure_paths,
        title="Data Center Analysis Report",
        author="Michael Maloney"
    )
    
    return pdf_path
```

## Available Plot Types

### 1. Scatter Plot (`create_scatter_plot`)
- **Purpose**: Correlation analysis between two variables
- **Features**: Optional regression line, statistical annotations
- **Best for**: Temperature vs humidity, power vs efficiency, etc.

```python
fig_gen.create_scatter_plot(
    x_data=temperatures,
    y_data=humidities,
    title="Temperature vs Humidity",
    x_label="Temperature (°F)",
    y_label="Humidity (%)",
    color='black',
    alpha=0.6,
    add_regression=True,
    add_stats=True
)
```

### 2. Time Series Plot (`create_time_series_plot`)
- **Purpose**: Temporal data analysis
- **Features**: Mean lines, rolling averages, date formatting
- **Best for**: Temperature over time, power consumption trends

```python
fig_gen.create_time_series_plot(
    time_data=dates,
    y_data=temperatures,
    title="Temperature Over Time",
    y_label="Temperature (°F)",
    add_mean_line=True,
    add_rolling_avg=True,
    window=7
)
```

### 3. Dual-Axis Plot (`create_dual_axis_plot`)
- **Purpose**: Compare two variables with different scales
- **Features**: Two Y-axes, synchronized time axis
- **Best for**: Temperature and humidity, power and efficiency

```python
fig_gen.create_dual_axis_plot(
    time_data=dates,
    y1_data=temperatures,
    y2_data=humidities,
    title="Temperature and Humidity",
    y1_label="Temperature (°F)",
    y2_label="Humidity (%)",
    y1_color='blue',
    y2_color='orange'
)
```

### 4. Histogram Plot (`create_histogram_plot`)
- **Purpose**: Distribution analysis
- **Features**: KDE overlay, statistical annotations
- **Best for**: Temperature distribution, efficiency analysis

```python
fig_gen.create_histogram_plot(
    data=temperatures,
    title="Temperature Distribution",
    x_label="Temperature (°F)",
    bins=30,
    add_kde=True,
    add_stats=True
)
```

### 5. Bar Plot (`create_bar_plot`)
- **Purpose**: Categorical data comparison
- **Features**: Value labels, automatic rotation
- **Best for**: Monthly averages, CRAC unit comparisons

```python
fig_gen.create_bar_plot(
    categories=["Jan", "Feb", "Mar"],
    values=[70.2, 72.1, 68.9],
    title="Monthly Average Temperature",
    y_label="Temperature (°F)",
    add_values=True
)
```

### 6. Summary Page (`create_summary_page`)
- **Purpose**: Statistical overview
- **Features**: Formatted text layout
- **Best for**: Report summaries, key findings

```python
summary_data = {
    "Total Data Points": 1000,
    "Mean Temperature": "72.5 °F",
    "Temperature Std Dev": "3.2 °F"
}

fig_gen.create_summary_page(
    title="Analysis Summary",
    summary_data=summary_data
)
```

## Color Palette

The system uses a professional black/white/gray color scheme:

```python
colors = {
    'primary': 'black',
    'secondary': '#333333',
    'accent': '#666666',
    'temp': '#1f77b4',      # Blue for temperature
    'humidity': '#ff7f0e',  # Orange for humidity
    'power': '#2ca02c',     # Green for power
    'efficiency': '#d62728', # Red for efficiency
    'capacity': '#9467bd',  # Purple for capacity
    'eir': '#8c564b'        # Brown for EIR
}
```

## Professional Standards

### Font Specifications
- **Family**: Arial (professional, readable)
- **Title**: 16-18pt, bold
- **Axis Labels**: 14pt
- **Tick Labels**: 12pt
- **Annotations**: 11-13pt

### Layout Standards
- **Figure Size**: 12x8 inches (standard)
- **DPI**: 300 (publication quality)
- **Padding**: 2.0 (generous spacing)
- **Grid**: Alpha 0.3 (subtle)

### Statistical Annotations
- **Correlation**: Pearson correlation coefficient
- **P-values**: Scientific notation
- **Regression**: R² values
- **Statistics**: Mean, median, standard deviation

## Integration with J1 Modules

### In Your Module's main.py

```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "modules"))

from figure_generator import FigureGenerator

class YourModule:
    def __init__(self):
        self.output_dir = Path("output")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.fig_gen = FigureGenerator(self.output_dir, self.timestamp)
    
    def generate_figures(self):
        # Your figure generation code here
        figure_paths = []
        
        # Create figures...
        
        # Compile PDF
        pdf_path = self.fig_gen.compile_pdf_report(
            figure_paths=figure_paths,
            title="Your Module Report",
            author="Michael Maloney"
        )
        
        return pdf_path
```

## Best Practices

### 1. Consistent Naming
```python
# Good
title="Temperature vs Humidity Correlation"
x_label="Temperature (°F)"
y_label="Humidity (%)"

# Avoid
title="Temp vs Hum"
x_label="Temp"
y_label="Hum"
```

### 2. Appropriate Plot Types
- **Correlations**: Use scatter plots with regression
- **Time trends**: Use time series plots
- **Distributions**: Use histograms with KDE
- **Comparisons**: Use bar plots
- **Multiple variables**: Use dual-axis plots

### 3. Statistical Rigor
```python
# Always include statistical context
add_regression=True,  # For correlations
add_stats=True,       # For distributions
add_mean_line=True,   # For time series
```

### 4. Professional Presentation
```python
# Use consistent colors
color=fig_gen.colors['temp']  # Instead of hardcoded colors

# Include proper labels
title="Data Center Temperature Analysis"  # Descriptive
x_label="Temperature (°F)"               # With units
```

## Demonstration

Run the demonstration script to see all plot types in action:

```bash
cd "MLM J1 - Michael Maloneys First Journal Paper/modules"
python figure_demo.py
```

This will generate:
- 8 different types of figures
- A comprehensive PDF report
- Sample data center analysis

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure the modules directory is in your Python path
2. **Font Issues**: Arial font must be available on your system
3. **Memory Issues**: Close figures with `plt.close()` after saving
4. **Path Issues**: Use `Path` objects for cross-platform compatibility

### Performance Tips

1. **Batch Processing**: Generate all figures, then compile PDF
2. **Memory Management**: Close figures immediately after saving
3. **File Organization**: Use descriptive filenames with timestamps

## Future Enhancements

- [ ] 3D plotting capabilities
- [ ] Interactive plot generation
- [ ] Custom color schemes
- [ ] Advanced statistical annotations
- [ ] Export to multiple formats (SVG, EPS)

---

**Author**: Michael Maloney  
**Purpose**: PhD-level data visualization for J1 project  
**Version**: 1.0.0 