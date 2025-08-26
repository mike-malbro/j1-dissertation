#!/usr/bin/env python3
"""
CRCS[n] Scenario Analysis Module
Comprehensive analysis of different CRAC unit configurations

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

This module provides detailed analysis of different CRAC unit scenarios
including Scenario 1 (A only) and Scenario 2 (B1+B2+B3+B4).
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent / "data"))
sys.path.append(str(Path(__file__).parent.parent.parent / "modules"))

from scenario_modeling import ScenarioModeling
from crcs_plotting import J1AnalysisBase
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import json
from typing import List, Dict, Any

class ScenarioAnalysis(J1AnalysisBase):
    """Comprehensive scenario analysis for CRAC unit configurations"""
    
    def __init__(self):
        super().__init__()
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize scenario modeling
        self.scenario_model = ScenarioModeling()
        
        # Data center specifications
        self.data_center_specs = {
            "name": "Harrisburg Data Center",
            "location": "Harrisburg, PA",
            "dimensions": {
                "white_space": {"length": 34, "width": 44, "height": 7},
                "ceiling_height": 7
            },
            "layout": {
                "rows": 4,
                "servers": 44,
                "crac_units": {
                    "main": 1,
                    "supplemental": 4
                }
            },
            "energy_pricing": {
                "rate_per_kwh": 0.1,
                "meter_doubling": True
            }
        }
        
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def analyze_scenario_performance(self, scenario_ids: List[str], 
                                   operating_conditions: Dict[str, float]) -> Dict[str, Any]:
        """Analyze performance of multiple scenarios"""
        
        print(f"Analyzing {len(scenario_ids)} scenarios...")
        print(f"Operating Conditions: {operating_conditions}")
        
        # Get comparison results
        comparison_results = self.scenario_model.compare_scenarios(scenario_ids, operating_conditions)
        
        # Calculate additional metrics
        analysis_results = {
            'timestamp': self.timestamp,
            'operating_conditions': operating_conditions,
            'scenarios': comparison_results,
            'summary_metrics': self._calculate_summary_metrics(comparison_results),
            'energy_analysis': self._calculate_energy_analysis(comparison_results),
            'reliability_analysis': self._calculate_reliability_analysis(comparison_results)
        }
        
        return analysis_results
    
    def _calculate_summary_metrics(self, comparison_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate summary metrics across all scenarios"""
        
        summary = {
            'total_scenarios': len(comparison_results),
            'scenario_names': [],
            'total_capacities': [],
            'total_powers': [],
            'system_cops': [],
            'efficiency_ratios': [],
            'active_units': [],
            'total_units': []
        }
        
        for scenario_id, result in comparison_results.items():
            if result is not None:
                summary['scenario_names'].append(result['scenario_name'])
                summary['total_capacities'].append(result['system_metrics']['total_cooling_capacity_kw'])
                summary['total_powers'].append(result['system_metrics']['total_power_consumption_kw'])
                summary['system_cops'].append(result['system_metrics']['system_cop'])
                summary['efficiency_ratios'].append(result['system_metrics']['energy_efficiency_ratio'])
                summary['active_units'].append(result['system_metrics']['active_units'])
                summary['total_units'].append(result['system_metrics']['total_units'])
        
        return summary
    
    def _calculate_energy_analysis(self, comparison_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate energy consumption and cost analysis"""
        
        energy_analysis = {}
        
        for scenario_id, result in comparison_results.items():
            if result is not None:
                power_kw = result['system_metrics']['total_power_consumption_kw']
                capacity_kw = result['system_metrics']['total_cooling_capacity_kw']
                
                # Annual calculations (8760 hours)
                annual_hours = 8760
                annual_energy_kwh = power_kw * annual_hours
                annual_cost = annual_energy_kwh * self.data_center_specs['energy_pricing']['rate_per_kwh']
                
                # Monthly calculations
                monthly_energy_kwh = annual_energy_kwh / 12
                monthly_cost = annual_cost / 12
                
                energy_analysis[scenario_id] = {
                    'power_kw': power_kw,
                    'capacity_kw': capacity_kw,
                    'annual_energy_kwh': annual_energy_kwh,
                    'annual_cost': annual_cost,
                    'monthly_energy_kwh': monthly_energy_kwh,
                    'monthly_cost': monthly_cost,
                    'efficiency_cop': result['system_metrics']['system_cop']
                }
        
        return energy_analysis
    
    def _calculate_reliability_analysis(self, comparison_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate reliability and redundancy analysis"""
        
        reliability_analysis = {}
        
        for scenario_id, result in comparison_results.items():
            if result is not None:
                active_units = result['system_metrics']['active_units']
                total_units = result['system_metrics']['total_units']
                expected_uptime = result['reliability_metrics']['expected_uptime']
                redundancy_level = result['reliability_metrics']['redundancy_level']
                
                # Calculate redundancy factor
                redundancy_factor = active_units / total_units if total_units > 0 else 0
                
                # Calculate availability metrics
                availability_percent = expected_uptime * 100
                downtime_hours_per_year = (1 - expected_uptime) * 8760
                
                reliability_analysis[scenario_id] = {
                    'active_units': active_units,
                    'total_units': total_units,
                    'redundancy_factor': redundancy_factor,
                    'redundancy_level': redundancy_level,
                    'expected_uptime': expected_uptime,
                    'availability_percent': availability_percent,
                    'downtime_hours_per_year': downtime_hours_per_year
                }
        
        return reliability_analysis
    
    def create_comprehensive_analysis_plot(self, analysis_results: Dict[str, Any]) -> str:
        """Create comprehensive analysis plots"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create multi-panel analysis
        fig = plt.figure(figsize=(20, 16))
        
        # Define grid layout
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Extract data
        summary = analysis_results['summary_metrics']
        energy = analysis_results['energy_analysis']
        reliability = analysis_results['reliability_analysis']
        
        # 1. Capacity and Power Comparison
        ax1 = fig.add_subplot(gs[0, 0])
        x = np.arange(len(summary['scenario_names']))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, summary['total_capacities'], width, 
                        label='Cooling Capacity (kW)', color='#2E3440')
        bars2 = ax1.bar(x + width/2, summary['total_powers'], width, 
                        label='Power Consumption (kW)', color='#5E81AC')
        
        ax1.set_xlabel('Scenarios')
        ax1.set_ylabel('Power/Capacity (kW)')
        ax1.set_title('Capacity vs Power Consumption')
        ax1.set_xticks(x)
        ax1.set_xticklabels([name.split(':')[1].strip() for name in summary['scenario_names']], 
                           rotation=45, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Efficiency Comparison
        ax2 = fig.add_subplot(gs[0, 1])
        bars = ax2.bar(summary['scenario_names'], summary['system_cops'], color='#88C0D0')
        ax2.set_ylabel('System COP')
        ax2.set_title('Coefficient of Performance')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, summary['system_cops']):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # 3. Annual Energy Consumption
        ax3 = fig.add_subplot(gs[0, 2])
        annual_energies = [energy[scenario_id]['annual_energy_kwh'] 
                          for scenario_id in energy.keys()]
        scenario_labels = [analysis_results['scenarios'][scenario_id]['scenario_name'] 
                          for scenario_id in energy.keys()]
        
        bars = ax3.bar(scenario_labels, annual_energies, color='#A3BE8C')
        ax3.set_ylabel('Annual Energy (kWh)')
        ax3.set_title('Annual Energy Consumption')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, annual_energies):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(annual_energies)*0.01,
                    f'{value:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=8)
        
        # 4. Annual Energy Cost
        ax4 = fig.add_subplot(gs[1, 0])
        annual_costs = [energy[scenario_id]['annual_cost'] for scenario_id in energy.keys()]
        
        bars = ax4.bar(scenario_labels, annual_costs, color='#EBCB8B')
        ax4.set_ylabel('Annual Cost ($)')
        ax4.set_title('Annual Energy Cost')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, annual_costs):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(annual_costs)*0.01,
                    f'${value:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=8)
        
        # 5. Reliability Metrics
        ax5 = fig.add_subplot(gs[1, 1])
        availability_percents = [reliability[scenario_id]['availability_percent'] 
                               for scenario_id in reliability.keys()]
        
        bars = ax5.bar(scenario_labels, availability_percents, color='#BF616A')
        ax5.set_ylabel('Availability (%)')
        ax5.set_title('System Availability')
        ax5.tick_params(axis='x', rotation=45)
        ax5.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, availability_percents):
            ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # 6. Redundancy Analysis
        ax6 = fig.add_subplot(gs[1, 2])
        redundancy_factors = [reliability[scenario_id]['redundancy_factor'] 
                             for scenario_id in reliability.keys()]
        
        bars = ax6.bar(scenario_labels, redundancy_factors, color='#81A1C1')
        ax6.set_ylabel('Redundancy Factor')
        ax6.set_title('System Redundancy')
        ax6.tick_params(axis='x', rotation=45)
        ax6.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, redundancy_factors):
            ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # 7. Monthly Energy Comparison
        ax7 = fig.add_subplot(gs[2, 0])
        monthly_energies = [energy[scenario_id]['monthly_energy_kwh'] 
                           for scenario_id in energy.keys()]
        
        bars = ax7.bar(scenario_labels, monthly_energies, color='#D08770')
        ax7.set_ylabel('Monthly Energy (kWh)')
        ax7.set_title('Monthly Energy Consumption')
        ax7.tick_params(axis='x', rotation=45)
        ax7.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, monthly_energies):
            ax7.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(monthly_energies)*0.01,
                    f'{value:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=8)
        
        # 8. Efficiency vs Cost Scatter
        ax8 = fig.add_subplot(gs[2, 1])
        efficiencies = [energy[scenario_id]['efficiency_cop'] for scenario_id in energy.keys()]
        costs = [energy[scenario_id]['annual_cost'] for scenario_id in energy.keys()]
        
        scatter = ax8.scatter(efficiencies, costs, s=200, alpha=0.7, 
                             c=['#2E3440', '#5E81AC', '#88C0D0'])
        ax8.set_xlabel('System COP')
        ax8.set_ylabel('Annual Cost ($)')
        ax8.set_title('Efficiency vs Cost')
        ax8.grid(True, alpha=0.3)
        
        # Add labels to scatter points
        for i, (eff, cost) in enumerate(zip(efficiencies, costs)):
            ax8.annotate(f'Scenario {i+1}', (eff, cost), 
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        # 9. Summary Table
        ax9 = fig.add_subplot(gs[2, 2])
        ax9.axis('tight')
        ax9.axis('off')
        
        # Create summary table
        table_data = []
        for scenario_id in energy.keys():
            scenario_name = analysis_results['scenarios'][scenario_id]['scenario_name']
            capacity = energy[scenario_id]['capacity_kw']
            power = energy[scenario_id]['power_kw']
            cop = energy[scenario_id]['efficiency_cop']
            annual_cost = energy[scenario_id]['annual_cost']
            
            table_data.append([
                scenario_name.split(':')[1].strip(),
                f"{capacity:.1f}",
                f"{power:.1f}",
                f"{cop:.2f}",
                f"${annual_cost:,.0f}"
            ])
        
        table = ax9.table(cellText=table_data,
                         colLabels=['Scenario', 'Capacity (kW)', 'Power (kW)', 'COP', 'Annual Cost'],
                         cellLoc='center',
                         loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        
        # Style the table
        for i in range(len(table_data) + 1):
            for j in range(5):
                if i == 0:  # Header row
                    table[(i, j)].set_facecolor('#2E3440')
                    table[(i, j)].set_text_props(weight='bold', color='white')
                else:  # Data rows
                    if i % 2 == 0:
                        table[(i, j)].set_facecolor('#F0F0F0')
                    else:
                        table[(i, j)].set_facecolor('white')
        
        # Add title
        fig.suptitle('J1 Scenario Analysis - Comprehensive Performance Comparison', 
                    fontsize=16, weight='bold', y=0.98)
        
        # Save plot
        plot_file = self.output_dir / f"comprehensive_scenario_analysis_{timestamp}.png"
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(plot_file)
    
    def generate_analysis_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate comprehensive analysis report"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f"scenario_analysis_report_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(analysis_results, f, indent=2)
        
        return str(report_file)
    
    def run_comprehensive_analysis(self) -> Dict[str, str]:
        """Run comprehensive scenario analysis"""
        
        print("J1 Comprehensive Scenario Analysis")
        print("="*50)
        
        # Define scenarios to analyze
        scenario_ids = ['scenario_1', 'scenario_2', 'scenario_3']
        
        # Define operating conditions
        operating_conditions = {
            'ambient_temp_f': 75,
            'humidity_percent': 50,
            'load_percentage': 80
        }
        
        # Run analysis
        analysis_results = self.analyze_scenario_performance(scenario_ids, operating_conditions)
        
        # Generate outputs
        outputs = {}
        
        # Create comprehensive plot
        plot_file = self.create_comprehensive_analysis_plot(analysis_results)
        outputs['comprehensive_plot'] = plot_file
        print(f"Generated comprehensive analysis plot: {plot_file}")
        
        # Generate report
        report_file = self.generate_analysis_report(analysis_results)
        outputs['analysis_report'] = report_file
        print(f"Generated analysis report: {report_file}")
        
        # Print summary
        print("\n" + "="*50)
        print("Analysis Summary")
        print("="*50)
        
        for scenario_id, result in analysis_results['scenarios'].items():
            if result:
                print(f"\n{result['scenario_name']}:")
                print(f"  Capacity: {result['system_metrics']['total_cooling_capacity_kw']:.1f} kW")
                print(f"  Power: {result['system_metrics']['total_power_consumption_kw']:.1f} kW")
                print(f"  COP: {result['system_metrics']['system_cop']:.2f}")
                print(f"  Annual Cost: ${analysis_results['energy_analysis'][scenario_id]['annual_cost']:,.2f}")
                print(f"  Availability: {analysis_results['reliability_analysis'][scenario_id]['availability_percent']:.1f}%")
        
        return outputs

def main():
    """Main function for scenario analysis"""
    
    # Initialize analysis
    analyzer = ScenarioAnalysis()
    
    # Run comprehensive analysis
    outputs = analyzer.run_comprehensive_analysis()
    
    print("\n" + "="*50)
    print("Analysis Complete!")
    print("="*50)
    print(f"Outputs generated:")
    for output_type, file_path in outputs.items():
        print(f"  {output_type}: {file_path}")

if __name__ == "__main__":
    main() 