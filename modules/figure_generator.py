"""
Standardized Figure Generator for CRCS[n] Project
Author: Michael Maloney
Purpose: Professional, consistent figure generation with PhD-level precision
Uses the centralized CRCSPlotting system for all styling and colors.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')
from modules.j1_plotting import J1AnalysisBase

class FigureGenerator(J1AnalysisBase):
    """
    Professional figure generator with standardized styling and layout.
    Uses the J1AnalysisBase for all plotting, style, and color configuration.
    Incorporates PhD-level best practices for data visualization.
    """
    
    def __init__(self, output_dir: Path, timestamp: str):
        super().__init__()
        self.output_dir = output_dir
        self.timestamp = timestamp
    
    def create_scatter_plot(self, 
                          x_data: np.ndarray, 
                          y_data: np.ndarray,
                          title: str,
                          x_label: str,
                          y_label: str,
                          color: str = 'black',
                          alpha: float = 0.6,
                          figsize: Tuple[int, int] = (12, 8),
                          add_regression: bool = False,
                          add_stats: bool = True) -> str:
        """
        Create professional scatter plot with optional regression line
        
        Args:
            x_data: X-axis data
            y_data: Y-axis data  
            title: Plot title
            x_label: X-axis label
            y_label: Y-axis label
            color: Point color
            alpha: Transparency
            figsize: Figure size
            add_regression: Add regression line
            add_stats: Add correlation statistics
            
        Returns:
            Path to saved figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create scatter plot
        scatter = ax.scatter(x_data, y_data, color=color, alpha=alpha, s=30)
        
        # Add regression line if requested
        if add_regression:
            try:
                from scipy.stats import linregress
                slope, intercept, r_value, p_value, std_err = linregress(x_data, y_data)
                line_x = np.array([x_data.min(), x_data.max()])
                line_y = slope * line_x + intercept
                ax.plot(line_x, line_y, color='red', linestyle='--', linewidth=2, 
                       label=f'R² = {r_value**2:.3f}')
                ax.legend(fontsize=12, framealpha=1.0, edgecolor='black', 
                         loc='upper left', bbox_to_anchor=(0.02, 0.98))
            except ImportError:
                print("Warning: scipy not available, skipping regression line")
        
        # Add statistics annotation
        if add_stats:
            try:
                from scipy.stats import pearsonr
                corr, p_val = pearsonr(x_data, y_data)
                stats_text = f'Correlation: {corr:.3f}\nP-value: {p_val:.3e}'
            except ImportError:
                # Manual correlation calculation
                x_mean, y_mean = np.mean(x_data), np.mean(y_data)
                numerator = np.sum((x_data - x_mean) * (y_data - y_mean))
                denominator = np.sqrt(np.sum((x_data - x_mean)**2) * np.sum((y_data - y_mean)**2))
                corr = numerator / denominator if denominator != 0 else 0
                stats_text = f'Correlation: {corr:.3f}'
            
            ax.text(0.05, 0.95, stats_text, transform=ax.transAxes, 
                   fontsize=11, fontfamily='Arial', color='black',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black'),
                   verticalalignment='top')
        
        # Styling
        ax.set_xlabel(x_label, fontsize=14, fontfamily='Arial', color='black', labelpad=10)
        ax.set_ylabel(y_label, fontsize=14, fontfamily='Arial', color='black', labelpad=10)
        ax.set_title(title, fontsize=16, fontweight='bold', fontfamily='Arial', color='black', pad=20)
        
        # Grid and spines
        ax.grid(True, alpha=0.3, color='black')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('black')
        ax.spines['bottom'].set_color('black')
        
        # Tick parameters
        ax.tick_params(axis='both', which='major', labelsize=12, color='black')
        
        plt.tight_layout(pad=2.0)
        
        # Save figure
        fig_path = self.output_dir / f"scatter_{title.lower().replace(' ', '_').replace(':', '')}_{self.timestamp}.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return str(fig_path)
    
    def create_time_series_plot(self,
                               time_data: pd.DatetimeIndex,
                               y_data: np.ndarray,
                               title: str,
                               y_label: str,
                               color: str = 'black',
                               figsize: Tuple[int, int] = (12, 6),
                               add_mean_line: bool = True,
                               add_rolling_avg: bool = False,
                               window: int = 7) -> str:
        """
        Create professional time series plot
        
        Args:
            time_data: Time index
            y_data: Y-axis data
            title: Plot title
            y_label: Y-axis label
            color: Line color
            figsize: Figure size
            add_mean_line: Add horizontal mean line
            add_rolling_avg: Add rolling average
            window: Rolling window size
            
        Returns:
            Path to saved figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot main data
        ax.plot(time_data, y_data, color=color, linewidth=1.5, alpha=0.8, label='Raw Data')
        
        # Add rolling average if requested
        if add_rolling_avg:
            rolling_avg = pd.Series(y_data, index=time_data).rolling(window=window, min_periods=1).mean()
            ax.plot(time_data, rolling_avg, color='red', linewidth=2, label=f'{window}-point Rolling Average')
        
        # Add mean line if requested
        if add_mean_line:
            mean_val = np.mean(y_data)
            ax.axhline(y=mean_val, color='red', linestyle='--', linewidth=2, 
                      label=f'Mean ({mean_val:.2f})')
        
        # Styling
        ax.set_xlabel('Time', fontsize=14, fontfamily='Arial', color='black', labelpad=10)
        ax.set_ylabel(y_label, fontsize=14, fontfamily='Arial', color='black', labelpad=10)
        ax.set_title(title, fontsize=16, fontweight='bold', fontfamily='Arial', color='black', pad=20)
        
        # Date formatting
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
        ax.tick_params(axis='x', rotation=45)
        
        # Grid and spines
        ax.grid(True, alpha=0.3, color='black')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('black')
        ax.spines['bottom'].set_color('black')
        
        # Legend
        if add_mean_line or add_rolling_avg:
            ax.legend(fontsize=12, framealpha=1.0, edgecolor='black', 
                     loc='upper right', bbox_to_anchor=(0.98, 0.98))
        
        # Tick parameters
        ax.tick_params(axis='both', which='major', labelsize=12, color='black')
        
        plt.tight_layout(pad=2.0)
        
        # Save figure
        fig_path = self.output_dir / f"timeseries_{title.lower().replace(' ', '_').replace(':', '')}_{self.timestamp}.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return str(fig_path)
    
    def create_dual_axis_plot(self,
                             time_data: pd.DatetimeIndex,
                             y1_data: np.ndarray,
                             y2_data: np.ndarray,
                             title: str,
                             y1_label: str,
                             y2_label: str,
                             y1_color: str = 'black',
                             y2_color: str = '#666666',
                             figsize: Tuple[int, int] = (12, 6)) -> str:
        """
        Create professional dual-axis time series plot
        
        Args:
            time_data: Time index
            y1_data: Primary Y-axis data
            y2_data: Secondary Y-axis data
            title: Plot title
            y1_label: Primary Y-axis label
            y2_label: Secondary Y-axis label
            y1_color: Primary line color
            y2_color: Secondary line color
            figsize: Figure size
            
        Returns:
            Path to saved figure
        """
        fig, ax1 = plt.subplots(figsize=figsize)
        
        # Primary axis
        line1 = ax1.plot(time_data, y1_data, color=y1_color, linewidth=2, label=y1_label)
        ax1.set_xlabel('Time', fontsize=14, fontfamily='Arial', color='black', labelpad=10)
        ax1.set_ylabel(y1_label, fontsize=14, fontfamily='Arial', color=y1_color, labelpad=10)
        ax1.tick_params(axis='y', labelcolor=y1_color)
        
        # Secondary axis
        ax2 = ax1.twinx()
        line2 = ax2.plot(time_data, y2_data, color=y2_color, linewidth=2, label=y2_label)
        ax2.set_ylabel(y2_label, fontsize=14, fontfamily='Arial', color=y2_color, labelpad=10)
        ax2.tick_params(axis='y', labelcolor=y2_color)
        
        # Title
        ax1.set_title(title, fontsize=16, fontweight='bold', fontfamily='Arial', color='black', pad=20)
        
        # Date formatting
        ax1.xaxis.set_major_locator(mdates.MonthLocator())
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
        ax1.tick_params(axis='x', rotation=45)
        
        # Grid and spines
        ax1.grid(True, alpha=0.3, color='black')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['left'].set_color(y1_color)
        ax1.spines['bottom'].set_color('black')
        
        # Legend
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, fontsize=12, framealpha=1.0, edgecolor='black', 
                  loc='upper right', bbox_to_anchor=(0.98, 0.98))
        
        # Tick parameters
        ax1.tick_params(axis='both', which='major', labelsize=12, color='black')
        ax2.tick_params(axis='both', which='major', labelsize=12, color='black')
        
        plt.tight_layout(pad=2.0)
        
        # Save figure
        fig_path = self.output_dir / f"dual_axis_{title.lower().replace(' ', '_').replace(':', '')}_{self.timestamp}.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return str(fig_path)
    
    def create_histogram_plot(self,
                             data: np.ndarray,
                             title: str,
                             x_label: str,
                             color: str = 'black',
                             bins: int = 30,
                             figsize: Tuple[int, int] = (10, 6),
                             add_kde: bool = True,
                             add_stats: bool = True) -> str:
        """
        Create professional histogram plot
        
        Args:
            data: Data to plot
            title: Plot title
            x_label: X-axis label
            color: Bar color
            bins: Number of bins
            figsize: Figure size
            add_kde: Add kernel density estimation
            add_stats: Add statistical annotations
            
        Returns:
            Path to saved figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create histogram
        if add_kde:
            sns.histplot(data, bins=bins, kde=True, color=color, ax=ax, alpha=0.7)
        else:
            ax.hist(data, bins=bins, color=color, alpha=0.7, edgecolor='black')
        
        # Add mean and median lines
        mean_val = np.mean(data)
        median_val = np.median(data)
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean ({mean_val:.2f})')
        ax.axvline(median_val, color='green', linestyle='-', linewidth=2, label=f'Median ({median_val:.2f})')
        
        # Add statistics annotation
        if add_stats:
            std_val = np.std(data)
            stats_text = f'Mean: {mean_val:.2f}\nStd: {std_val:.2f}\nN: {len(data)}'
            ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, 
                   fontsize=11, fontfamily='Arial', color='black',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black'),
                   verticalalignment='top', horizontalalignment='right')
        
        # Styling
        ax.set_xlabel(x_label, fontsize=14, fontfamily='Arial', color='black', labelpad=10)
        ax.set_ylabel('Frequency', fontsize=14, fontfamily='Arial', color='black', labelpad=10)
        ax.set_title(title, fontsize=16, fontweight='bold', fontfamily='Arial', color='black', pad=20)
        
        # Grid and spines
        ax.grid(True, alpha=0.3, color='black')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('black')
        ax.spines['bottom'].set_color('black')
        
        # Legend
        ax.legend(fontsize=12, framealpha=1.0, edgecolor='black', 
                 loc='upper right', bbox_to_anchor=(0.98, 0.98))
        
        # Tick parameters
        ax.tick_params(axis='both', which='major', labelsize=12, color='black')
        
        plt.tight_layout(pad=2.0)
        
        # Save figure
        fig_path = self.output_dir / f"histogram_{title.lower().replace(' ', '_').replace(':', '')}_{self.timestamp}.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return str(fig_path)
    
    def create_bar_plot(self,
                       categories: List[str],
                       values: List[float],
                       title: str,
                       y_label: str,
                       color: str = 'black',
                       figsize: Tuple[int, int] = (10, 6),
                       add_values: bool = True) -> str:
        """
        Create professional bar plot
        
        Args:
            categories: Category labels
            values: Bar values
            title: Plot title
            y_label: Y-axis label
            color: Bar color
            figsize: Figure size
            add_values: Add value labels on bars
            
        Returns:
            Path to saved figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create bar plot
        bars = ax.bar(categories, values, color=color, alpha=0.7, edgecolor='black')
        
        # Add value labels on bars
        if add_values:
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                       f'{value:.2f}', ha='center', va='bottom', 
                       fontsize=11, fontfamily='Arial', color='black')
        
        # Styling
        ax.set_xlabel('Categories', fontsize=14, fontfamily='Arial', color='black', labelpad=10)
        ax.set_ylabel(y_label, fontsize=14, fontfamily='Arial', color='black', labelpad=10)
        ax.set_title(title, fontsize=16, fontweight='bold', fontfamily='Arial', color='black', pad=20)
        
        # Rotate x-axis labels if needed
        if len(categories) > 5:
            ax.tick_params(axis='x', rotation=45)
        
        # Grid and spines
        ax.grid(True, alpha=0.3, color='black', axis='y')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('black')
        ax.spines['bottom'].set_color('black')
        
        # Tick parameters
        ax.tick_params(axis='both', which='major', labelsize=12, color='black')
        
        plt.tight_layout(pad=2.0)
        
        # Save figure
        fig_path = self.output_dir / f"bar_{title.lower().replace(' ', '_').replace(':', '')}_{self.timestamp}.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return str(fig_path)
    
    def create_summary_page(self, 
                          title: str,
                          summary_data: Dict[str, Any],
                          figsize: Tuple[int, int] = (12, 16)) -> str:
        """
        Create professional summary page
        
        Args:
            title: Page title
            summary_data: Dictionary of summary statistics
            figsize: Figure size
            
        Returns:
            Path to saved figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        ax.axis('off')
        
        # Title
        ax.text(0.5, 0.95, title, fontsize=20, fontweight='bold', 
               fontfamily='Arial', color='black', ha='center', va='center')
        
        # Summary text
        y_pos = 0.85
        for key, value in summary_data.items():
            if isinstance(value, (int, float)):
                text = f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}"
            else:
                text = f"{key}: {value}"
            
            ax.text(0.1, y_pos, text, fontsize=12, fontfamily='Arial', 
                   color='black', ha='left', va='center')
            y_pos -= 0.05
        
        # Save figure
        fig_path = self.output_dir / f"summary_{title.lower().replace(' ', '_').replace(':', '')}_{self.timestamp}.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return str(fig_path)
    
    def compile_pdf_report(self, 
                          figure_paths: List[str],
                          title: str,
                          author: str = "Michael Maloney") -> str:
        """
        Compile all figures into a professional PDF report
        
        Args:
            figure_paths: List of paths to figures
            title: Report title
            author: Report author
            
        Returns:
            Path to compiled PDF
        """
        pdf_path = self.output_dir / f"{title.lower().replace(' ', '_')}_{self.timestamp}.pdf"
        
        with PdfPages(pdf_path) as pdf:
            # Title page
            fig = plt.figure(figsize=(12, 16))
            plt.axis('off')
            
            plt.text(0.5, 0.8, title, fontsize=24, fontweight='bold', 
                    fontfamily='Arial', color='black', ha='center', va='center')
            plt.text(0.5, 0.7, f"Author: {author}", fontsize=16, 
                    fontfamily='Arial', color='black', ha='center', va='center')
            plt.text(0.5, 0.6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                    fontsize=14, fontfamily='Arial', color='black', ha='center', va='center')
            
            pdf.savefig(fig, facecolor='white')
            plt.close(fig)
            
            # Add each figure
            for i, fig_path in enumerate(figure_paths):
                if Path(fig_path).exists():
                    fig = plt.figure(figsize=(12, 8))
                    img = plt.imread(fig_path)
                    plt.imshow(img)
                    plt.axis('off')
                    plt.title(f"Figure {i+1}", fontsize=16, fontweight='bold', 
                             fontfamily='Arial', color='black', pad=20)
                    pdf.savefig(fig, facecolor='white')
                    plt.close(fig)
        
        return str(pdf_path) 