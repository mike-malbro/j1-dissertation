# Professional Formatting Guide for J1 System

## 🎯 **Your Professional Colab Style - Incorporated!**

Based on your **"S1-Libert Cooling Unit - Temperature/Humidity Time Series Data Analysis"** script, this guide shows how to apply your professional formatting to the entire CRCS system.

## 📋 **Key Professional Elements from Your Style:**

### **1. Script Header Structure**
```python
#!/usr/bin/env python3
"""
S1-Libert Cooling Unit - Temperature/Humidity Time Series Data Analysis
J1 - Michael Maloneys First Journal Paper

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
```

### **2. Professional Import Structure**
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates
import datetime
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set seaborn style
sns.set_style("white")
```

### **3. Professional Color Palette**
```python
self.colors = {
    'temperature': 'tab:blue',
    'humidity': 'tab:orange',
    'regression': 'red',
    'mean_line': 'red',
    'median_line': 'green',
    'grid': 'black'
}
```

### **4. Professional Plot Styling**
- **Legends**: Placed at bottom right below x-axis to avoid chart interference
- **Annotations**: Positioned at bottom left (correlation, averages)
- **Grid**: Clean, minimal interference
- **Fonts**: Professional, readable
- **Colors**: Consistent, publication-ready

### **5. Professional Figure Structure**
```python
def create_raw_data_plot(self, df: pd.DataFrame) -> str:
    """Create Figure 0: Raw Data (scatter plot)"""
    print("Creating raw data plot...")
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.scatter(df.index, df['Temperature'], color=self.colors['temperature'], 
               label='Temperature (°F)')
    ax2 = ax1.twinx()
    ax2.scatter(df.index, df['Humidity'], color=self.colors['humidity'], 
               label='Humidity (%)')
    
    # Professional styling
    ax1.set_ylabel('Temperature (°F)')
    ax2.set_ylabel('Humidity (%)')
    ax2.set_ylim(0, 100)
    ax1.set_xlabel('Time')
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(False)
    ax2.grid(False)
    
    # Professional legend placement
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
```

## 🔧 **How to Apply to All J1 Modules:**

### **Step 1: Update Module Headers**
Replace all module headers with your professional style:
```python
#!/usr/bin/env python3
"""
[Module Name] - [Specific Analysis]
J1 - Michael Maloneys First Journal Paper

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Notes: This script is designed for PhD-level data analysis, ensuring high precision 
and reproducibility. [Specific analysis notes]

Script Title: [Specific Script Title]
Name: Michael Logan Maloney
"""
```

### **Step 2: Standardize Imports**
Use your import structure in all modules:
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
try:
    from scipy.stats import linregress
except ImportError:
    # Manual correlation calculation if scipy not available
    def linregress(x, y):
        # ... manual implementation
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates
import datetime
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set seaborn style
sns.set_style("white")
```

### **Step 3: Apply Professional Plotting**
- Use your color palette
- Apply your legend positioning
- Use your annotation placement
- Follow your figure sizing and styling

### **Step 4: Standardize Output Format**
```python
def generate_comprehensive_report(self) -> str:
    """Generate comprehensive analysis report"""
    print("Starting comprehensive analysis...")
    
    # Your professional analysis flow
    # 1. Load data
    # 2. Calculate statistics
    # 3. Create professional plots
    # 4. Generate PDF report
    
    return str(report_pdf)
```

## 📊 **Professional Analysis Flow:**

### **1. Data Loading**
```python
def load_data(self, file_id: str = None) -> pd.DataFrame:
    """Load data from Google Drive or generate synthetic data"""
    if file_id:
        # Your Google Drive loading logic
        url = f'https://drive.google.com/uc?export=download&id={file_id}'
        # ... your professional data loading
    else:
        # Generate synthetic data
        df = self.generate_synthetic_data()
    return df
```

### **2. Statistics Calculation**
```python
def calculate_statistics(self, df: pd.DataFrame) -> dict:
    """Calculate comprehensive statistics"""
    print("Calculating statistics...")
    
    # Your professional statistical analysis
    temp_mean = df['Temperature'].mean()
    temp_std = df['Temperature'].std()
    # ... comprehensive statistics
    
    print(f"   Temperature: {temp_mean:.2f}°F ± {temp_std:.2f}°F")
    # ... professional output formatting
    
    return stats
```

### **3. Professional Plotting**
```python
def create_professional_plot(self, df: pd.DataFrame, stats: dict) -> str:
    """Create professional plot with your styling"""
    print("Creating professional plot...")
    
    # Your professional plotting approach
    fig, ax1 = plt.subplots(figsize=(12, 6))
    # ... your styling
    
    # Professional legend placement
    fig.legend(handles, labels, loc='lower right', 
              bbox_to_anchor=(1.0, -0.2), ncol=1)
    
    # Professional annotation placement
    ax1.text(0.05, -0.2, '', transform=ax1.transAxes, fontsize=10)
    
    return str(fig_path)
```

## 🎨 **Your Professional Standards:**

### **Visual Elements:**
- **Legends**: Bottom right, below x-axis
- **Annotations**: Bottom left (correlations, averages)
- **Grid**: Clean, minimal interference
- **Colors**: Consistent, publication-ready
- **Fonts**: Professional, readable
- **Sizing**: Appropriate for publication

### **Code Structure:**
- **Clear headers**: Script title, author, purpose
- **Comprehensive imports**: All necessary libraries
- **Professional documentation**: PhD-level analysis notes
- **Error handling**: Robust data loading
- **Clean output**: Professional formatting

### **Analysis Flow:**
- **Data loading**: Google Drive integration
- **Statistics**: Comprehensive analysis
- **Visualization**: Publication-ready plots
- **Documentation**: Professional reporting

## 🚀 **Implementation Plan:**

### **Phase 1: Update Existing Modules**
1. **Performance Curves**: Apply your professional styling
2. **Legacy Scripts**: Update with your format
3. **Main Orchestrator**: Professional output formatting

### **Phase 2: Create New Modules**
1. **Rack Temperature Analysis**: Your professional approach
2. **PDU Analysis**: Your professional styling
3. **Energy Bills**: Your professional format

### **Phase 3: Standardize System**
1. **Figure Generator**: Incorporate your styling
2. **PDF Compilation**: Professional formatting
3. **Documentation**: Your professional standards

## ✅ **Benefits of Your Style:**

- **Publication-ready**: Professional academic standards
- **Consistent**: Uniform across all modules
- **Reproducible**: PhD-level precision
- **Clean**: Minimal chart interference
- **Professional**: Ready for Dr. Wangda Zuo

Your professional formatting style is now the **gold standard** for the entire J1 system! 🎯 