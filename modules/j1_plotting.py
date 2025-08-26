"""
j1_plotting.py
Centralized plotting and style helpers for the J1 system.
Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department

This module provides a professional, consistent plotting style and helper functions
for all J1 analysis modules. Import and use in any module to ensure publication-ready
figures and tables.
"""

import matplotlib.pyplot as plt
import seaborn as sns

class J1Plotting:
    """
    Centralized plotting and style configuration for J1.
    Usage:
        from j1_plotting import J1Plotting
        J1Plotting.set_style()
        colors = J1Plotting.colors
    """
    # Professional color palette
    colors = {
        'temperature': 'tab:blue',
        'humidity': 'tab:orange',
        'regression': 'red',
        'mean_line': 'red',
        'median_line': 'green',
        'grid': 'black',
        'main_crac': 'tab:blue',
        'supp_crac': 'tab:orange',
        'system': 'red',
        'metered': 'tab:blue',
        'solar': 'tab:orange',
        'total': 'red',
        'cost': 'green',
        'background': 'white',
        'table_header': '#f0f0f0',
        'table_section': '#e0e0e0',
        'table_row_alt': '#f8f8f8',
    }

    @staticmethod
    def set_style():
        """
        Set matplotlib and seaborn style parameters to the J1 professional standard.
        """
        sns.set_style("white")
        plt.rcParams['font.family'] = 'Arial'
        plt.rcParams['font.size'] = 12
        plt.rcParams['axes.linewidth'] = 1.0
        plt.rcParams['axes.edgecolor'] = J1Plotting.colors['grid']
        plt.rcParams['axes.labelcolor'] = 'black'
        plt.rcParams['xtick.color'] = 'black'
        plt.rcParams['ytick.color'] = 'black'
        plt.rcParams['figure.facecolor'] = J1Plotting.colors['background']
        plt.rcParams['axes.facecolor'] = J1Plotting.colors['background']
        plt.rcParams['text.color'] = 'black'

    @staticmethod
    def add_legend(ax, loc='lower right', bbox_to_anchor=(1.0, -0.2), ncol=1, fontsize=12):
        """
        Add a professional legend to the given axis.
        """
        handles, labels = ax.get_legend_handles_labels()
        ax.figure.legend(handles, labels, loc=loc, bbox_to_anchor=bbox_to_anchor, ncol=ncol, fontsize=fontsize)

    @staticmethod
    def add_annotation(ax, text, xy, xytext, color='black', fontsize=10):
        """
        Add a professional annotation with arrow to the given axis.
        """
        ax.annotate(text, xy=xy, xytext=xytext,
                    arrowprops=dict(arrowstyle='->', color=color, lw=2),
                    fontsize=fontsize, bbox=dict(boxstyle='round,pad=0.5', facecolor='white'))

    @staticmethod
    def style_table(table, header_rows=(0,), section_rows=(), alt_row_start=1):
        """
        Style a matplotlib table with professional colors.
        header_rows: tuple of row indices for header
        section_rows: tuple of row indices for section headers
        alt_row_start: first row index for alternating row color
        """
        for i in range(len(table._cells)//len(table._cells[0])):
            for j in range(len(table._cells[0])):
                if i in header_rows:
                    table[(i, j)].set_facecolor(J1Plotting.colors['table_header'])
                    table[(i, j)].set_text_props(weight='bold', color='black')
                elif i in section_rows:
                    table[(i, j)].set_facecolor(J1Plotting.colors['table_section'])
                    table[(i, j)].set_text_props(weight='bold')
                elif (i - alt_row_start) % 2 == 0:
                    table[(i, j)].set_facecolor(J1Plotting.colors['table_row_alt'])
                else:
                    table[(i, j)].set_facecolor('white')

    @staticmethod
    def finalize_figure(fig, ax=None, tight=True):
        """
        Finalize and layout the figure for saving or display.
        """
        if tight:
            fig.tight_layout()
        if ax is not None:
            ax.figure = fig

# Optionally, a base class for analysis modules
class J1AnalysisBase:
    """
    Base class for J1 analysis modules to provide plotting helpers and style.
    """
    def __init__(self):
        J1Plotting.set_style()
        self.colors = J1Plotting.colors

    def add_legend(self, ax, **kwargs):
        J1Plotting.add_legend(ax, **kwargs)

    def add_annotation(self, ax, text, xy, xytext, **kwargs):
        J1Plotting.add_annotation(ax, text, xy, xytext, **kwargs)

    def style_table(self, table, **kwargs):
        J1Plotting.style_table(table, **kwargs)

    def finalize_figure(self, fig, ax=None, **kwargs):
        J1Plotting.finalize_figure(fig, ax, **kwargs)