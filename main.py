#!/usr/bin/env python3
"""
J1 PhD Dissertation Notebook - Main Orchestrator
Advanced Data Center Thermodynamic Modeling Framework

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus
Penn State Fellowship Recipient

This is the main orchestrator for the J1 PhD Dissertation Notebook - a comprehensive
data center thermodynamic modeling framework designed for PhD-level research.
Professional quality that meets Dr. Wangda Zuo approval level.

Target Audience: Dr. Wangda Zuo, Michael Weter (LBNL National Labs)
Goal: World's Latest and Greatest Data Center Thermodynamic Modeling Tool
Stage: Advanced Research - Building Foundation for 4-Year PhD Journey
"""

import os
import sys
import subprocess
import yaml
import json
import re
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import for PDF and image processing
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from PIL import Image as PILImage
except ImportError as e:
    print(f"⚠️ Warning: Some dependencies not available: {e}")

class J1PhDStudyOrchestrator:
    """J1 PhD Dissertation Notebook - Main Orchestrator for Advanced Research"""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.base_dir = Path(__file__).parent
        self.config_file = self.base_dir / config_file
        self.output_dir = self.base_dir / "output"
        self.data_dir = self.base_dir / "data"
        self.figures_dir = self.base_dir / "figures"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create directories
        for dir_path in [self.output_dir, self.data_dir, self.figures_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Clean output directory for fresh start
        self.clean_output_directory()
        
        # Load advanced configuration
        self.config = self.load_config()
        
        # Track generated PDFs for merging
        self.generated_pdfs = []
        self.module_results = {}
    
    def clean_output_directory(self):
        """Clean the output directory for a fresh start"""
        print("🧹 Cleaning output directory for fresh start...")
        
        if self.output_dir.exists():
            # Remove all files in output directory
            for file_path in self.output_dir.iterdir():
                if file_path.is_file():
                    try:
                        file_path.unlink()
                        print(f"   🗑️ Removed: {file_path.name}")
                    except Exception as e:
                        print(f"   ⚠️ Could not remove {file_path.name}: {e}")
        
        print("✅ Output directory cleaned")
        
        # Load dynamic module configuration from Google Sheet and module_inputs.json
        self.module_config = self.load_dynamic_module_config()
        
        # Import Google Sheet helper functions
        sys.path.append(str(self.base_dir / "0Z.00_Google_Sheet_Helper_Functions"))
        try:
            from google_drive_helpers import GoogleDriveHelpers
            self.google_helpers = GoogleDriveHelpers()
        except ImportError as e:
            print(f"⚠️ Warning: Google Drive helpers not available: {e}")
            self.google_helpers = None
        pass  # Module configuration now loaded dynamically
        
    def load_dynamic_module_config(self):
        """Load dynamic module configuration from module_inputs.json and Google Sheet"""
        print("🔄 Loading dynamic module configuration...")
        
        # Load from module_inputs.json
        module_inputs_file = self.base_dir / "module_inputs.json"
        if module_inputs_file.exists():
            with open(module_inputs_file, 'r') as f:
                module_data = json.load(f)
                print(f"✅ Loaded {len(module_data.get('modules', {}))} modules from module_inputs.json")
                return module_data.get('modules', {})
        else:
            print("⚠️ module_inputs.json not found, using empty configuration")
            return {}
    
    def load_config(self):
        """Load advanced configuration from YAML file"""
        if not self.config_file.exists():
            print(f"❌ Configuration file not found: {self.config_file}")
            return {}
            
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def print_j1_banner(self):
        """Print the J1 PhD Dissertation Notebook banner"""
        banner = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██╗   ██╗██╗  ██╗ - Ph.D. Study Engineers Notebook                        ║
║  ╚██╗ ██╔╝██║  ██║                                                           ║
║   ╚████╔╝ ███████║                                                           ║
║    ╚██╔╝  ██╔══██║                                                           ║
║     ██║   ██║  ██║                                                           ║
║     ╚═╝   ╚═╝  ╚═╝                                                           ║
║                                                                              ║
║  Modelica Modeling of Heterogeneous Data Center Cooling Systems              ║
║  J1 - An optimal load allocation for Multi CRAC System for Harrisburg DC    ║
║                                                                              ║
║  Author: Michael Logan Maloney                                              ║
║  Institution: Pennsylvania State University                                 ║
║  Department: Architectural Engineering                                      ║
║  Laboratory: Sustainable Buildings and Society Library (SBS Lab)           ║
║  Advisor: Dr. Wangda Zuo                                                    ║
║  Status: ADVANCED RESEARCH MODE ACTIVATED                                   ║
║                                                                              ║
║  Timestamp: {self.timestamp}                                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def execute_j1_module(self, module_id: str, module_info: dict) -> dict:
        """Execute a J1 module with professional academic standards"""
        try:
            module_path = self.base_dir / module_info['path']
            main_file = module_path / "main.py"
            
            if main_file.exists():
                print(f"🚀 Executing J1 module {module_id}: {module_info['name']}")
                
                # Execute the module
                result = subprocess.run(
                    [sys.executable, "main.py"],
                    capture_output=True,
                    text=True,
                    cwd=str(module_path)
                )
                
                if result.returncode == 0:
                    print(f"✅ J1 module {module_id} completed successfully")
                    
                    # Find generated PDFs
                    output_dir = module_path / "output"
                    pdf_files = []
                    if output_dir.exists():
                        pdf_files = list(output_dir.glob("*.pdf"))
                        if pdf_files:
                            print(f"   📄 Found {len(pdf_files)} PDF(s): {[f.name for f in pdf_files]}")
                    
                    return {
                        'success': True,
                        'output': result.stdout,
                        'pdf_files': pdf_files,
                        'module_id': module_id,
                        'module_name': module_info['name']
                    }
                else:
                    print(f"❌ J1 module {module_id} failed: {result.stderr}")
                    return {
                        'success': False,
                        'error': result.stderr,
                        'module_id': module_id,
                        'module_name': module_info['name']
                    }
            else:
                print(f"⚠️ Could not find main.py for module {module_id}")
                return {
                    'success': False,
                    'error': 'main.py not found',
                    'module_id': module_id,
                    'module_name': module_info['name']
                }
                
        except Exception as e:
            print(f"❌ Error executing J1 module {module_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'module_id': module_id,
                'module_name': module_info['name']
            }
    
    def collect_all_pdfs(self):
        """Collect the most recent PDF from each module"""
        all_pdfs = []
        
        for module_id, result in self.module_results.items():
            if result['success'] and result['pdf_files']:
                # Get the most recent PDF from this module
                most_recent_pdf = max(result['pdf_files'], key=lambda x: x.stat().st_mtime)
                all_pdfs.append(most_recent_pdf)
                print(f"   📄 Using most recent PDF for {module_id}: {most_recent_pdf.name}")
        
        return all_pdfs
    
    def create_j1_dissertation_pdf(self, pdf_files: list) -> str:
        """Create the J1 PhD Dissertation PDF with professional academic standards"""
        
        if not pdf_files:
            print("⚠️ No PDFs found - creating summary document instead")
            return self.create_j1_summary()
        
        # Sort PDFs by priority - ensure cover pages come first
        def get_pdf_priority(pdf_file):
            name = pdf_file.name.lower()
            if 'cover' in name:
                return 0  # Highest priority
            elif 'table_of_contents' in name:
                return 1  # Second priority
            elif '00.00' in name or '00.0' in name:
                return 2  # Cover module priority
            elif '01.00' in name or '01.0' in name:
                return 3  # Journal 1 priority
            elif '0r.00' in name or '0r.0' in name:
                return 4  # References priority
            elif '0z.00' in name or '0z.0' in name:
                return 5  # Google Sheet helpers priority
            else:
                return 999  # Default priority
        
        pdf_files.sort(key=get_pdf_priority)
        
        print(f"📄 Ph.D. Study Engineers Notebook found {len(pdf_files)} PDFs to compile")
        
        # Try to import PDF libraries (pypdf preserves hyperlinks better than PyPDF2)
        try:
            from pypdf import PdfMerger
            PDF_MERGER_AVAILABLE = True
            print("✅ Using pypdf for PDF merging (hyperlinks preserved)")
        except ImportError:
            try:
                from PyPDF2 import PdfMerger
                PDF_MERGER_AVAILABLE = True
                print("⚠️ Using PyPDF2 for PDF merging (hyperlinks may not be preserved)")
            except ImportError:
                PDF_MERGER_AVAILABLE = False
                print("⚠️ No PDF merger available - will create file list instead")
        
        try:
            from matplotlib.backends.backend_pdf import PdfPages
            import matplotlib.pyplot as plt
            MATPLOTLIB_AVAILABLE = True
        except ImportError:
            MATPLOTLIB_AVAILABLE = False
            print("⚠️ Matplotlib not available - will create text summary instead")
        
        if PDF_MERGER_AVAILABLE:
            return self.merge_pdfs_with_pypdf2(pdf_files)
        elif MATPLOTLIB_AVAILABLE:
            return self.create_pdf_with_matplotlib(pdf_files)
        else:
            return self.create_j1_summary()
    
    def merge_pdfs_with_pypdf2(self, pdf_files: list) -> str:
        """Merge PDFs using pypdf (preserves hyperlinks better than PyPDF2)"""
        try:
            # Try pypdf first, fallback to PyPDF2
            try:
                from pypdf import PdfMerger
                print("   🔗 Using pypdf (hyperlinks preserved)")
            except ImportError:
                from PyPDF2 import PdfMerger
                print("   ⚠️ Using PyPDF2 (hyperlinks may not be preserved)")
            
            merger = PdfMerger()
            
            # Add each PDF
            for pdf_file in pdf_files:
                if pdf_file.exists():
                    print(f"   📄 Adding: {pdf_file.name}")
                    merger.append(str(pdf_file))
                else:
                    print(f"   ⚠️ PDF not found: {pdf_file}")
            
            # Create J1 Dissertation PDF
            dissertation_pdf = self.output_dir / f"J1_DISSERTATION_{self.timestamp}.pdf"
            merger.write(str(dissertation_pdf))
            merger.close()
            
            print(f"✅ J1 Dissertation PDF created: {dissertation_pdf}")
            return str(dissertation_pdf)
            
        except Exception as e:
            print(f"❌ PDF merging failed: {e}")
            return self.create_j1_summary()
    
    def create_pdf_with_matplotlib(self, pdf_files: list) -> str:
        """Create PDF using matplotlib"""
        try:
            from matplotlib.backends.backend_pdf import PdfPages
            import matplotlib.pyplot as plt
            
            dissertation_pdf = self.output_dir / f"J1_DISSERTATION_{self.timestamp}.pdf"
            
            with PdfPages(dissertation_pdf) as pdf:
                # Title page
                fig = plt.figure(figsize=(12, 16))
                plt.axis('off')
                
                plt.text(0.5, 0.8, "J1 PhD DISSERTATION", fontsize=24, fontweight='bold', 
                        ha='center', va='center', color='darkblue')
                plt.text(0.5, 0.7, "Advanced Data Center Thermodynamic Modeling Framework", fontsize=16, 
                        ha='center', va='center', color='darkgreen')
                plt.text(0.5, 0.6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                        fontsize=14, ha='center', va='center')
                plt.text(0.5, 0.5, f"Total Modules: {len(self.module_config)}", 
                        fontsize=12, ha='center', va='center')
                plt.text(0.5, 0.4, f"Total PDFs: {len(pdf_files)}", 
                        fontsize=12, ha='center', va='center')
                
                pdf.savefig(fig, facecolor='white')
                plt.close(fig)
                
                # Add each PDF as an image
                for i, pdf_file in enumerate(pdf_files):
                    if pdf_file.exists():
                        try:
                            # This is a simplified approach - in practice you'd need to convert PDF to image
                            fig = plt.figure(figsize=(12, 8))
                            plt.text(0.5, 0.5, f"Module {i+1}: {pdf_file.name}", 
                                   fontsize=16, ha='center', va='center')
                            plt.title(f"PDF {i+1} of {len(pdf_files)}", fontsize=14)
                            pdf.savefig(fig, facecolor='white')
                            plt.close(fig)
                        except Exception as e:
                            print(f"   ⚠️ Could not add {pdf_file.name}: {e}")
            
            print(f"✅ ULTIMATE BOSS PDF created: {boss_pdf}")
            return str(boss_pdf)
            
        except Exception as e:
            print(f"❌ Matplotlib PDF creation failed: {e}")
            return self.create_j1_summary()
    
    def create_j1_summary(self) -> str:
        """Create a J1 PhD Dissertation summary document"""
        summary_file = self.output_dir / f"J1_DISSERTATION_SUMMARY_{self.timestamp}.txt"
        
        with open(summary_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("J1 PhD DISSERTATION COMPREHENSIVE REPORT SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Author: Michael Maloney\n")
            f.write("Institution: Penn State Architectural Engineering Department\n")
            f.write("Focus: Mechanical System Focus\n")
            f.write("Target: Dr. Wangda Zuo, Michael Weter (LBNL National Labs)\n\n")
            
            f.write("MODULE EXECUTION RESULTS:\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Module ID':<20} {'Status':<10} {'Path':<40} {'PDFs':<10}\n")
            f.write("-" * 80 + "\n")
            
            for module_id, result in self.module_results.items():
                status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
                
                # Get module path - check main modules first
                module_path = self.module_config.get(module_id, {}).get('path', '')
                
                # If not found in main modules, check submodules
                if not module_path:
                    for container_id, container_info in self.module_config.items():
                        if container_info.get('type') == 'container' and 'submodules' in container_info:
                            if module_id in container_info['submodules']:
                                module_path = container_info['submodules'][module_id]['path']
                                break
                
                # If still not found, show N/A
                if not module_path:
                    module_path = 'N/A'
                
                pdf_count = len(result.get('pdf_files', []))
                f.write(f"{module_id:<20} {status:<10} {module_path:<40} {pdf_count:<10}\n")
                
                # Add detailed info
                if result['success'] and result['pdf_files']:
                    f.write(f"    📄 PDFs: {[f.name for f in result['pdf_files']]}\n")
                elif not result['success']:
                    f.write(f"    ❌ Error: {result.get('error', 'Unknown error')}\n")
                f.write("\n")
            
            f.write("PDF FILES GENERATED:\n")
            f.write("-" * 40 + "\n")
            
            all_pdfs = self.collect_all_pdfs()
            for pdf_file in all_pdfs:
                f.write(f"📄 {pdf_file}\n")
        
        print(f"✅ J1 Dissertation Summary created: {summary_file}")
        return str(summary_file)
    
    def run_advanced_container_module(self, module_name: str, module_config: dict) -> bool:
        """Run an advanced container module with submodules"""
        print(f"   📁 Advanced Container Module with Submodules")
        
        metadata = module_config.get('metadata', {})
        if metadata:
            print(f"   Conference: {metadata.get('conference', 'N/A')}")
            print(f"   Paper Type: {metadata.get('paper_type', 'N/A')}")
            print(f"   Background: {metadata.get('background', 'N/A')}")
        
        submodules = module_config.get('submodules', {})
        if not submodules:
            print(f"   ⚠️  No submodules found")
            return True

        # Sort submodules by priority
        sorted_submodules = sorted(submodules.items(), key=lambda x: x[1].get('priority', 999))

        success = True
        for sub_name, sub_config in sorted_submodules:
            if sub_config.get('enabled', False):
                print(f"   └─ Running Advanced Submodule: {sub_name}")
                
                # Check for user input
                user_input = sub_config.get('user_input', {})
                if user_input:
                    print(f"   └─ User Input: {list(user_input.keys())}")
                
                # Check calculation type
                calc_type = sub_config.get('calculation_type', '')
                if calc_type:
                    print(f"   └─ Calculation Type: {calc_type}")
                
                sub_success = self.run_advanced_single_module(sub_name, sub_config, parent_dir=module_name)
                if not sub_success:
                    success = False
            else:
                print(f"   └─ Skipping disabled submodule: {sub_name}")
        
        return success
    
    def run_advanced_single_module(self, module_name: str, module_config: dict, parent_dir: str = None) -> bool:
        """Run an advanced single module with professional quality"""
        main_file = module_config.get('main_file')
        if not main_file:
            print(f"   ❌ No main file specified for {module_name}")
            return False
        
        # Determine module directory
        if parent_dir:
            module_dir = self.base_dir / parent_dir / module_name
        else:
            module_dir = self.base_dir / module_name
        
        if not module_dir.exists():
            print(f"   ❌ Module directory not found: {module_dir}")
            return False
        
        main_file_path = module_dir / main_file
        if not main_file_path.exists():
            print(f"   ❌ Main file not found: {main_file_path}")
            return False

        print(f"   📂 Directory: {module_dir}")
        print(f"   📄 Main file: {main_file}")
        
        # Check for professional requirements
        output_pattern = module_config.get('output_pattern', '')
        if output_pattern:
            print(f"   📊 Output Pattern: {output_pattern}")
        
        try:
            # Run from the base directory with proper Python path
            original_dir = os.getcwd()
            os.chdir(self.base_dir)
            
            # Set environment variables for professional quality
            env = os.environ.copy()
            env['PYTHONPATH'] = f"{self.base_dir}:{env.get('PYTHONPATH', '')}"
            env['J1_PROFESSIONAL_MODE'] = 'true'
            env['J1_TARGET_QUALITY'] = 'Dr. Wangda Zuo approval level'
            
            # Run the module script
            module_script = str(module_dir / main_file)
            print(f"   🔧 Running: python {module_script}")
            print(f"   🎯 Target Quality: Dr. Wangda Zuo approval level")
            
            result = subprocess.run(['python3', module_script],
                                  capture_output=True, text=True, timeout=300,
                                  env=env, cwd=self.base_dir)

            if result.returncode == 0:
                print(f"   ✅ Completed successfully - Professional quality")
                if result.stdout.strip():
                    print(f"   📤 Output: {result.stdout.strip()}")
                
                # Track generated PDFs for merging
                self.track_generated_pdfs(module_dir, output_pattern)
                
                return True
            else:
                print(f"   ❌ Failed - Not meeting professional standards")
                if result.stderr.strip():
                    print(f"   📤 Error: {result.stderr.strip()}")
                return False

        except subprocess.TimeoutExpired:
            print(f"   ⏰ Timed out - Professional standards not met")
            return False
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return False
        finally:
            os.chdir(original_dir)

    def track_generated_pdfs(self, module_dir: Path, output_pattern: str):
        """Track generated PDFs for comprehensive merging"""
        if not output_pattern:
            return
            
        # Find the latest PDF matching the pattern
        output_dir = module_dir / "output"
        if not output_dir.exists():
            return
            
        # Look for PDFs matching the pattern and get the most recent one
        if output_pattern:
            # Convert pattern to glob pattern (e.g., "cover_*.pdf" -> "cover_*.pdf")
            glob_pattern = output_pattern.replace("*", "*")
            pdf_files = list(output_dir.glob(glob_pattern))
        else:
            # Fallback: look for any PDF files
            pdf_files = list(output_dir.glob("*.pdf"))
        
        if pdf_files:
            # Get the most recent one
            latest_pdf = max(pdf_files, key=lambda x: x.stat().st_mtime)
            self.generated_pdfs.append(latest_pdf)
            print(f"   📄 Tracked for merging: {latest_pdf.name}")
        else:
            print(f"   ⚠️  No PDF files found matching pattern: {output_pattern}")
    
    def cleanup_old_files(self):
        """Aggressive cleanup of old files and reports to keep workspace completely clean"""
        print("🧹 Aggressive cleanup of old files and reports...")
        
        # Configuration for aggressive cleanup
        keep_latest_comprehensive = 1  # Keep only the latest comprehensive PDF
        keep_latest_module_outputs = 1  # Keep only the latest from each module type
        keep_latest_text_files = 1  # Keep only the latest text file
        keep_latest_json_files = 1  # Keep only the latest JSON file
        max_age_hours = 1  # Remove files older than 1 hour
        
        from datetime import datetime, timedelta
        cutoff_date = datetime.now() - timedelta(hours=max_age_hours)
        
        # 1. Aggressive cleanup of comprehensive PDFs (keep only the latest 1)
        pdf_files = list(self.output_dir.glob("j1_comprehensive_study_*.pdf"))
        if len(pdf_files) > keep_latest_comprehensive:
            pdf_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            for old_file in pdf_files[keep_latest_comprehensive:]:
                try:
                    old_file.unlink()
                    print(f"   🗑️  Removed old comprehensive PDF: {old_file.name}")
                except Exception as e:
                    print(f"   ⚠️  Could not remove {old_file.name}: {e}")
        
        # 2. Aggressive cleanup of text files (keep only the latest 1)
        txt_files = list(self.output_dir.glob("j1_comprehensive_study_*.txt"))
        if len(txt_files) > keep_latest_text_files:
            txt_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            for old_file in txt_files[keep_latest_text_files:]:
                try:
                    old_file.unlink()
                    print(f"   🗑️  Removed old text file: {old_file.name}")
                except Exception as e:
                    print(f"   ⚠️  Could not remove {old_file.name}: {e}")
        
        # 3. Aggressive cleanup of JSON data files (keep only the latest 1)
        json_files = list(self.output_dir.glob("*.json"))
        if len(json_files) > keep_latest_json_files:
            json_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            for old_file in json_files[keep_latest_json_files:]:
                try:
                    old_file.unlink()
                    print(f"   🗑️  Removed old JSON file: {old_file.name}")
                except Exception as e:
                    print(f"   ⚠️  Could not remove {old_file.name}: {e}")
        
        # 4. Aggressive cleanup of old module outputs (keep only latest 1)
        for module_dir in self.base_dir.rglob("*/output"):
            if module_dir.is_dir():
                # Clean PDF files
                pdf_files = list(module_dir.glob("*.pdf"))
                if len(pdf_files) > keep_latest_module_outputs:
                    # Group by base name (without timestamp)
                    pdf_groups = {}
                    for pdf in pdf_files:
                        # Extract base name more robustly
                        parts = pdf.stem.split('_')
                        if len(parts) >= 2:
                            base_name = '_'.join(parts[:-1])  # Everything except timestamp
                        else:
                            base_name = parts[0]
                        
                        if base_name not in pdf_groups:
                            pdf_groups[base_name] = []
                        pdf_groups[base_name].append(pdf)
                    
                    # Keep only the latest file from each group
                    for base_name, files in pdf_groups.items():
                        if len(files) > keep_latest_module_outputs:
                            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                            for old_file in files[keep_latest_module_outputs:]:
                                try:
                                    old_file.unlink()
                                    print(f"   🗑️  Removed old module output: {old_file.name}")
                                except Exception as e:
                                    print(f"   ⚠️  Could not remove {old_file.name}: {e}")
                
                # Clean PNG files (keep only latest 1)
                png_files = list(module_dir.glob("*.png"))
                if len(png_files) > 1:
                    png_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                    for old_file in png_files[1:]:
                        try:
                            old_file.unlink()
                            print(f"   🗑️  Removed old PNG file: {old_file.name}")
                        except Exception as e:
                            print(f"   ⚠️  Could not remove {old_file.name}: {e}")
        
        # 5. Remove all files older than 1 hour (very aggressive)
        all_files = list(self.output_dir.glob("*"))
        for file_path in all_files:
            if file_path.is_file():
                file_age = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_age < cutoff_date:
                    try:
                        file_path.unlink()
                        print(f"   🗑️  Removed old file (>{max_age_hours} hour): {file_path.name}")
                    except Exception as e:
                        print(f"   ⚠️  Could not remove {file_path.name}: {e}")
        
        # 6. Clean up empty output directories
        for output_dir in self.base_dir.rglob("*/output"):
            if output_dir.is_dir() and not any(output_dir.iterdir()):
                try:
                    output_dir.rmdir()
                    print(f"   🗑️  Removed empty directory: {output_dir}")
                except Exception as e:
                    print(f"   ⚠️  Could not remove empty directory {output_dir}: {e}")
        
        # 7. Remove any remaining old files with specific patterns
        old_patterns = [
            "j1_data_*.json",
            "project_summary_*.json", 
            "scenario_results_*.json",
            "temp_*.pdf",
            "temp_*.txt"
        ]
        
        for pattern in old_patterns:
            old_files = list(self.output_dir.glob(pattern))
            for old_file in old_files:
                try:
                    old_file.unlink()
                    print(f"   🗑️  Removed old pattern file: {old_file.name}")
                except Exception as e:
                    print(f"   ⚠️  Could not remove {old_file.name}: {e}")
        
        print("   ✅ Aggressive cleanup complete - workspace is completely clean!")
        print(f"   📊 Cleanup settings: Keep latest {keep_latest_comprehensive} comprehensive PDF, {keep_latest_module_outputs} module output, max age {max_age_hours} hour")
    
    def create_comprehensive_pdf(self) -> str:
        """Create comprehensive PDF from all generated outputs"""
        if not self.generated_pdfs:
            print("⚠️  No PDFs to merge")
            return ""
            
        comprehensive_pdf = self.output_dir / f"j1_comprehensive_study_{self.timestamp}.pdf"
        
        print(f"📄 Creating Comprehensive PDF: {comprehensive_pdf}")
        print(f"   📊 Merging {len(self.generated_pdfs)} PDF files")
        
        # Try to import pypdf first, then PyPDF2
        try:
            try:
                from pypdf import PdfMerger
                merger = PdfMerger()
                print("   🔗 Using pypdf (hyperlinks preserved)")
            except ImportError:
                import PyPDF2
                if hasattr(PyPDF2, 'PdfMerger'):
                    merger = PyPDF2.PdfMerger()
                    print("   ⚠️ Using PyPDF2 (hyperlinks may not be preserved)")
                else:
                    raise ImportError("PdfMerger not found")
                
                # Add PDFs in order
                for pdf_path in self.generated_pdfs:
                    if pdf_path.exists():
                        print(f"   📄 Adding: {pdf_path.name}")
                        merger.append(str(pdf_path))
                    else:
                        print(f"   ⚠️  PDF not found: {pdf_path}")
                
                # Write comprehensive PDF
                merger.write(str(comprehensive_pdf))
                merger.close()
                
                print(f"   ✅ Comprehensive PDF created: {comprehensive_pdf}")
                return str(comprehensive_pdf)
            else:
                print("   ⚠️  PyPDF2 available but PdfMerger not found - creating file list instead")
                self.create_pdf_list(comprehensive_pdf)
            return str(comprehensive_pdf)
            
        except ImportError:
            print("   ⚠️  PyPDF2 not available - creating file list instead")
            self.create_pdf_list(comprehensive_pdf)
            return str(comprehensive_pdf)
        except Exception as e:
            print(f"   ❌ Error creating comprehensive PDF: {e}")
            self.create_pdf_list(comprehensive_pdf)
            return str(comprehensive_pdf)
    
    def create_pdf_list(self, comprehensive_pdf: Path):
        """Create a text file listing all PDFs when PyPDF2 is not available"""
        pdf_list_file = comprehensive_pdf.with_suffix('.txt')
        
        with open(pdf_list_file, 'w') as f:
            f.write(f"J1 Comprehensive Study - {self.timestamp}\n")
            f.write("=" * 50 + "\n\n")
            f.write("Generated PDF Files:\n\n")
            
            for i, pdf_path in enumerate(self.generated_pdfs, 1):
                f.write(f"{i}. {pdf_path.name}\n")
                f.write(f"   Path: {pdf_path}\n")
                f.write(f"   Size: {pdf_path.stat().st_size} bytes\n\n")
        
        print(f"   📄 Created PDF list: {pdf_list_file}")
        
        # Also create a simple merged PDF using system tools if available
        try:
            import subprocess
            pdf_files = [str(pdf) for pdf in self.generated_pdfs if pdf.exists()]
            if pdf_files:
                # Use system pdftk or gs to merge PDFs
                cmd = ['gs', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', 
                       f'-sOutputFile={comprehensive_pdf}', '-f'] + pdf_files
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"   ✅ Created merged PDF using Ghostscript: {comprehensive_pdf}")
                else:
                    print(f"   ⚠️  Ghostscript failed: {result.stderr}")
        except Exception as e:
            print(f"   ⚠️  Could not create merged PDF: {e}")
    
    def execute_all_j1_modules(self):
        """Execute all J1 modules with professional academic standards"""
        print("\n🚀 Starting Ph.D. Study Engineers Notebook execution...")
        print("=" * 80)
        
        # Step 1: Download Google Drive assets first
        print("\n📥 STEP 1: Downloading Google Drive Assets...")
        self.download_google_drive_assets()
        
        # Filter only active modules and execute them
        active_modules = {k: v for k, v in self.module_config.items() if v.get('active', False)}
        print(f"📊 Found {len(active_modules)} active modules out of {len(self.module_config)} total modules")
        
        # Execute all active modules
        for module_id, module_info in active_modules.items():
            # Skip the main.py module to avoid infinite loop
            if module_id == 'main.py':
                print(f"\n📋 Skipping main.py module (orchestrator)")
                continue
                
            print(f"\n📋 Processing J1 module {module_id}: {module_info['name']}")
            
            # Execute main module
            result = self.execute_j1_module(module_id, module_info)
            self.module_results[module_id] = result
            
            # Execute submodules if this is a container
            if module_info.get('type') == 'container' and 'submodules' in module_info:
                print(f"📂 Processing submodules for {module_id}")
                
                for submodule_id, submodule_info in module_info['submodules'].items():
                    print(f"  📋 Processing submodule {submodule_id}: {submodule_info['name']}")
                    
                    submodule_result = self.execute_j1_module(submodule_id, submodule_info)
                    self.module_results[submodule_id] = submodule_result
        
        print("\n" + "=" * 80)
        print("🎉 Ph.D. Study Engineers Notebook execution completed!")
    
    def compile_j1_dissertation(self) -> str:
        """Compile the J1 PhD Dissertation with professional academic standards"""
        print("\n📄 Compiling Ph.D. Study Engineers Notebook...")
        
        # Collect all PDFs
        all_pdfs = self.collect_all_pdfs()
        
        # Create J1 Dissertation PDF with Google Drive assets integrated
        dissertation_pdf = self.create_enhanced_j1_dissertation_pdf(all_pdfs)
        
        # Print J1 summary
        successful_modules = [mid for mid, result in self.module_results.items() if result['success']]
        failed_modules = [mid for mid, result in self.module_results.items() if not result['success']]
        
        print("\n" + "=" * 80)
        print("🎯 Ph.D. STUDY ENGINEERS NOTEBOOK EXECUTION SUMMARY")
        print("=" * 80)
        print(f"📊 Total Modules Processed: {len(self.module_results)}")
        print(f"✅ Successful: {len(successful_modules)}")
        print(f"❌ Failed: {len(failed_modules)}")
        print(f"📄 PDFs Collected: {len(all_pdfs)}")
        print(f"📄 Ph.D. Study Engineers Notebook Output: {dissertation_pdf}")
        
        if failed_modules:
            print(f"\n❌ Failed Modules: {', '.join(failed_modules)}")
        else:
            print("\n🎉 ALL MODULES COMPLETED SUCCESSFULLY!")
        
        return dissertation_pdf
    
    def download_google_drive_assets(self):
        """Download Google Drive assets for all modules"""
        try:
            # Import Google Drive helpers
            sys.path.append(str(Path(__file__).parent / "0Z.00_Google_Sheet_Helper_Functions"))
            from google_drive_helpers import download_asset, get_asset_statistics
            
            print("   🔄 Initializing Google Drive download system...")
            
            # Read module_inputs.json to get download links
            module_inputs_file = Path("module_inputs.json")
            if module_inputs_file.exists():
                with open(module_inputs_file, 'r') as f:
                    module_data = json.load(f)
                
                downloaded_count = 0
                for module_id, module_info in module_data['modules'].items():
                    description = module_info.get('description', '')
                    
                    # Look for Google Drive links in descriptions
                    if 'https://docs.google.com' in description:
                        # Extract URL from description
                        import re
                        url_match = re.search(r'https://docs\.google\.com/[^\s]+', description)
                        if url_match:
                            url = url_match.group(0)
                            print(f"   📥 Downloading asset for {module_id}: {url}")
                            
                            # Download the asset
                            asset_path = download_asset(
                                url=url,
                                module_id=module_id,
                                filename=f"{module_id}_asset.png"
                            )
                            
                            if asset_path:
                                downloaded_count += 1
                                print(f"   ✅ Downloaded: {asset_path}")
                            else:
                                print(f"   ❌ Failed to download for {module_id}")
                
                if downloaded_count > 0:
                    stats = get_asset_statistics()
                    print(f"   📊 Downloaded {downloaded_count} assets. Total: {stats['total_assets']}")
                else:
                    print("   ⚠️ No Google Drive assets found to download")
            else:
                print("   ⚠️ module_inputs.json not found")
                
        except Exception as e:
            print(f"   ❌ Google Drive download failed: {e}")
    
    def integrate_google_drive_assets_into_pdf(self, pdf_path: Path) -> bool:
        """Integrate downloaded Google Drive assets into the main PDF report"""
        try:
            sys.path.append(str(Path(__file__).parent / "0Z.00_Google_Sheet_Helper_Functions"))
            from pdf_asset_integration import PDFAssetIntegrator
            
            print(f"   🔄 Integrating Google Drive assets into PDF...")
            
            integrator = PDFAssetIntegrator()
            summary = integrator.get_asset_summary()
            
            if summary['modules_with_assets']:
                # Create a new PDF with assets integrated
                assets_pdf = self.output_dir / f"J1_DISSERTATION_WITH_ASSETS_{self.timestamp}.pdf"
                
                # Create 8.5x11 page with assets
                with PdfPages(assets_pdf) as pdf:
                    # Title page
                    fig = plt.figure(figsize=(8.5, 11))
                    plt.axis('off')
                    plt.text(0.5, 0.8, "J1 PhD Dissertation Report", fontsize=24, 
                            ha='center', va='center', fontweight='bold')
                    plt.text(0.5, 0.7, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                            fontsize=14, ha='center', va='center')
                    plt.text(0.5, 0.6, f"Total Assets: {len(summary['modules_with_assets'])}", 
                            fontsize=12, ha='center', va='center')
                    pdf.savefig(fig, facecolor='white')
                    plt.close(fig)
                    
                    # Add each asset as a figure on 8.5x11 page
                    figure_number = 1
                    for module_id in summary['modules_with_assets']:
                        asset_path = integrator.get_asset_path(module_id)
                        if asset_path and asset_path.exists():
                            # Create 8.5x11 page with figure
                            fig = plt.figure(figsize=(8.5, 11))
                            
                            # Load and display image
                            img = PILImage.open(asset_path)
                            ax = plt.subplot(111)
                            ax.imshow(img)
                            ax.axis('off')
                            
                            # Add figure title
                            module_names = {
                                "01.0C": "Problem System Model",
                                "01.0B": "Graphical Abstract", 
                                "01.0A": "Abstract Visualization"
                            }
                            title = module_names.get(module_id, f"Figure {figure_number}")
                            plt.title(f"Figure {figure_number}: {title}", fontsize=16, fontweight='bold', pad=20)
                            
                            # Add caption
                            caption = integrator.create_figure_caption(module_id, f"Figure {figure_number}")
                            plt.figtext(0.5, 0.02, caption, fontsize=10, ha='center', va='bottom',
                                      bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8))
                            
                            pdf.savefig(fig, facecolor='white')
                            plt.close(fig)
                            
                            figure_number += 1
                
                print(f"   ✅ Created integrated PDF: {assets_pdf}")
                return True
            else:
                print("   ⚠️ No assets to integrate")
                return False
                
        except Exception as e:
            print(f"   ❌ Asset integration failed: {e}")
            return False
    
    def create_enhanced_j1_dissertation_pdf(self, pdf_files: list) -> str:
        """Create enhanced J1 dissertation PDF with Google Drive assets integrated"""
        if not pdf_files:
            print("⚠️ No PDFs found - creating summary document instead")
            return self.create_j1_summary()
        
        # Try different PDF creation methods (keeping original logic)
        try:
            from PyPDF2 import PdfMerger
            PDF_MERGER_AVAILABLE = True
        except ImportError:
            PDF_MERGER_AVAILABLE = False
            print("⚠️ PyPDF2 not available - will use matplotlib method")
        
        try:
            from matplotlib.backends.backend_pdf import PdfPages
            import matplotlib.pyplot as plt
            MATPLOTLIB_AVAILABLE = True
        except ImportError:
            MATPLOTLIB_AVAILABLE = False
            print("⚠️ Matplotlib not available - will create text summary instead")
        
        if PDF_MERGER_AVAILABLE:
            # Use original PDF merger but enhance with assets
            return self.merge_pdfs_with_assets(pdf_files)
        elif MATPLOTLIB_AVAILABLE:
            # Use original matplotlib method but enhance with assets
            return self.create_enhanced_pdf_with_matplotlib(pdf_files)
        else:
            return self.create_j1_summary()
    
    def merge_pdfs_with_assets(self, pdf_files: list) -> str:
        """Merge PDFs using PyPDF2 and add Google Drive assets"""
        try:
            from PyPDF2 import PdfMerger
            
            # Sort PDFs by priority (keeping original logic)
            def get_pdf_priority(pdf_file):
                name = pdf_file.name.lower()
                if 'cover' in name:
                    return 0  # Highest priority
                elif 'table_of_contents' in name:
                    return 1  # Second priority
                elif '00.00' in name or '00.0' in name:
                    return 2  # Cover module priority
                elif '01.00' in name or '01.0' in name:
                    return 3  # Journal 1 priority
                elif '0r.00' in name or '0r.0' in name:
                    return 4  # References priority
                elif '0z.00' in name or '0z.0' in name:
                    return 5  # Google Sheet helpers priority
                else:
                    return 999  # Default priority
            
            pdf_files.sort(key=get_pdf_priority)
            print(f"📄 Ph.D. Study Engineers Notebook found {len(pdf_files)} PDFs to compile")
            
            # Create the final dissertation PDF
            dissertation_pdf = self.output_dir / f"J1_DISSERTATION_{self.timestamp}.pdf"
            
            merger = PdfMerger()
            
            # Add each PDF (original content preserved)
            for pdf_file in pdf_files:
                if pdf_file.exists():
                    print(f"   📄 Adding: {pdf_file.name}")
                    merger.append(str(pdf_file))
                else:
                    print(f"   ⚠️ PDF not found: {pdf_file}")
            
            # Add Google Drive assets as additional pages
            try:
                sys.path.append(str(Path(__file__).parent / "0Z.00_Google_Sheet_Helper_Functions"))
                from pdf_asset_integration import PDFAssetIntegrator
                
                integrator = PDFAssetIntegrator()
                asset_summary = integrator.get_asset_summary()
                
                if asset_summary['modules_with_assets']:
                    print(f"   📄 Adding {len(asset_summary['modules_with_assets'])} Google Drive assets...")
                    
                    for i, module_id in enumerate(asset_summary['modules_with_assets'], 1):
                        asset_path = integrator.get_asset_path(module_id)
                        if asset_path and asset_path.exists():
                            # Create a simple PDF page for the asset
                            from matplotlib.backends.backend_pdf import PdfPages
                            import matplotlib.pyplot as plt
                            from PIL import Image as PILImage
                            
                                                                                        # Create temporary PDF for the asset
                            temp_pdf = self.output_dir / f"temp_asset_{module_id}.pdf"
                            
                            with PdfPages(temp_pdf) as pdf:
                                fig = plt.figure(figsize=(8.5, 11))
                                
                                # Load and display image
                                img = PILImage.open(asset_path)
                                ax = plt.subplot(111)
                                ax.imshow(img)
                                ax.axis('off')
                                
                                # Add figure title
                                module_names = {
                                    "01.0C": "Problem System Model",
                                    "01.0D": "Model Library Diagram",
                                    "01.0B": "Graphical Abstract", 
                                    "01.0A": "Abstract Visualization"
                                }
                                title = module_names.get(module_id, f"Figure {i}")
                                plt.title(f"Figure {i}: {title}", fontsize=16, fontweight='bold', pad=20)
                                
                                # Add caption
                                caption = integrator.create_figure_caption(module_id, f"Figure {i}")
                                plt.figtext(0.5, 0.02, caption, fontsize=10, ha='center', va='bottom',
                                          bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8))
                                
                                pdf.savefig(fig, facecolor='white')
                                plt.close(fig)
                            
                            # Add the asset PDF to the merger
                            merger.append(str(temp_pdf))
                            print(f"   ✅ Added Figure {i}: {title}")
                            
                            # Clean up temp file
                            temp_pdf.unlink()
                            
            except Exception as e:
                print(f"   ⚠️ Could not add Google Drive assets: {e}")
            
            # Write the final dissertation PDF
            merger.write(str(dissertation_pdf))
            merger.close()
            
            print(f"✅ Ph.D. Study Engineers Notebook PDF created: {dissertation_pdf}")
            return str(dissertation_pdf)
            
        except Exception as e:
            print(f"❌ PDF merging failed: {e}")
            return self.create_j1_summary()
    
    def create_enhanced_pdf_with_matplotlib(self, pdf_files: list) -> str:
        """Create enhanced PDF using matplotlib with original content + assets"""
        try:
            from matplotlib.backends.backend_pdf import PdfPages
            import matplotlib.pyplot as plt
            
            dissertation_pdf = self.output_dir / f"J1_DISSERTATION_{self.timestamp}.pdf"
            
            # Sort PDFs by priority (original logic)
            def get_pdf_priority(pdf_file):
                name = pdf_file.name.lower()
                if 'cover' in name:
                    return 0
                elif 'table_of_contents' in name:
                    return 1
                elif '00.00' in name or '00.0' in name:
                    return 2
                elif '01.00' in name or '01.0' in name:
                    return 3
                elif '0r.00' in name or '0r.0' in name:
                    return 4
                elif '0z.00' in name or '0z.0' in name:
                    return 5
                else:
                    return 999
            
            pdf_files.sort(key=get_pdf_priority)
            
            with PdfPages(dissertation_pdf) as pdf:
                # Create title page (enhanced but keeping professional style)
                fig = plt.figure(figsize=(8.5, 11))  # Standard letter size
                plt.axis('off')
                
                plt.text(0.5, 0.8, "Ph.D. Study Engineers Notebook", fontsize=24, fontweight='bold', 
                        ha='center', va='center')
                plt.text(0.5, 0.7, "Michael Logan Maloney", fontsize=18, 
                        ha='center', va='center')
                plt.text(0.5, 0.65, "Pennsylvania State University", fontsize=14, 
                        ha='center', va='center')
                plt.text(0.5, 0.6, "Architectural Engineering Department", fontsize=14, 
                        ha='center', va='center')
                plt.text(0.5, 0.55, "Sustainable Buildings and Society Library (SBS Lab)", fontsize=12, 
                        ha='center', va='center')
                plt.text(0.5, 0.5, "Modelica Modeling of Heterogeneous Data Center Cooling Systems", fontsize=12, 
                        ha='center', va='center')
                plt.text(0.5, 0.4, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                        fontsize=12, ha='center', va='center')
                plt.text(0.5, 0.35, f"Total Modules: {len(self.module_results)}", 
                        fontsize=12, ha='center', va='center')
                plt.text(0.5, 0.3, f"Total PDFs: {len(pdf_files)}", 
                        fontsize=12, ha='center', va='center')
                
                # Add Google Drive asset count
                try:
                    sys.path.append(str(Path(__file__).parent / "0Z.00_Google_Sheet_Helper_Functions"))
                    from pdf_asset_integration import PDFAssetIntegrator
                    integrator = PDFAssetIntegrator()
                    asset_summary = integrator.get_asset_summary()
                    plt.text(0.5, 0.25, f"Google Drive Assets: {len(asset_summary['modules_with_assets'])}", 
                            fontsize=12, ha='center', va='center')
                except:
                    pass
                
                plt.text(0.5, 0.2, "Advisor: Dr. Wangda Zuo", 
                        fontsize=10, ha='center', va='center', style='italic')
                
                pdf.savefig(fig, facecolor='white')
                plt.close(fig)
                
                # Add module summary pages (original content preserved)
                for i, pdf_file in enumerate(pdf_files):
                    if pdf_file.exists():
                        try:
                            fig = plt.figure(figsize=(8.5, 11))
                            plt.axis('off')
                            plt.text(0.5, 0.5, f"Module {i+1}: {pdf_file.name}", 
                                   fontsize=16, ha='center', va='center', fontweight='bold')
                            plt.text(0.5, 0.4, f"File: {pdf_file.name}", 
                                   fontsize=12, ha='center', va='center')
                            plt.text(0.5, 0.3, f"Size: {pdf_file.stat().st_size / 1024:.1f} KB", 
                                   fontsize=10, ha='center', va='center')
                            plt.title(f"PDF {i+1} of {len(pdf_files)}", fontsize=14)
                            pdf.savefig(fig, facecolor='white')
                            plt.close(fig)
                        except Exception as e:
                            print(f"   ⚠️ Could not add {pdf_file.name}: {e}")
                
                # Add Google Drive assets as figures
                try:
                    sys.path.append(str(Path(__file__).parent / "0Z.00_Google_Sheet_Helper_Functions"))
                    from pdf_asset_integration import PDFAssetIntegrator
                    
                    integrator = PDFAssetIntegrator()
                    asset_summary = integrator.get_asset_summary()
                    
                    if asset_summary['modules_with_assets']:
                        print(f"   📄 Adding {len(asset_summary['modules_with_assets'])} Google Drive assets...")
                        
                        for i, module_id in enumerate(asset_summary['modules_with_assets'], 1):
                            asset_path = integrator.get_asset_path(module_id)
                            if asset_path and asset_path.exists():
                                # Create figure page
                                fig = plt.figure(figsize=(8.5, 11))
                                
                                # Load and display image
                                img = PILImage.open(asset_path)
                                ax = plt.subplot(111)
                                ax.imshow(img)
                                ax.axis('off')
                                
                                # Add figure title
                                module_names = {
                                    "01.0C": "Problem System Model",
                                    "01.0D": "Model Library Diagram",
                                    "01.0B": "Graphical Abstract", 
                                    "01.0A": "Abstract Visualization"
                                }
                                title = module_names.get(module_id, f"Figure {i}")
                                plt.title(f"Figure {i}: {title}", fontsize=16, fontweight='bold', pad=20)
                                
                                # Add caption
                                caption = integrator.create_figure_caption(module_id, f"Figure {i}")
                                plt.figtext(0.5, 0.02, caption, fontsize=10, ha='center', va='bottom',
                                          bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8))
                                
                                pdf.savefig(fig, facecolor='white')
                                plt.close(fig)
                                print(f"   ✅ Added Figure {i}: {title}")
                        
                except Exception as e:
                    print(f"   ⚠️ Could not add Google Drive assets: {e}")
            
            print(f"✅ Enhanced Ph.D. Study Engineers Notebook PDF created: {dissertation_pdf}")
            return str(dissertation_pdf)
            
        except Exception as e:
            print(f"❌ Enhanced PDF creation failed: {e}")
            return self.create_j1_summary()
    

    
    def create_ultimate_unified_pdf(self) -> str:
        """Create ONE PDF TO RULE THEM ALL - Ultimate unified dissertation"""
        try:
            # Import necessary modules
            sys.path.append(str(Path(__file__).parent / "0Z.00_Google_Sheet_Helper_Functions"))
            from pdf_asset_integration import PDFAssetIntegrator
            
            print("   🔄 Creating Ultimate Unified PDF...")
            
            # Create the ultimate PDF filename
            ultimate_pdf = self.output_dir / f"ONE_PDF_TO_RULE_THEM_ALL_{self.timestamp}.pdf"
            
            # Initialize asset integrator
            integrator = PDFAssetIntegrator()
            asset_summary = integrator.get_asset_summary()
            
            with PdfPages(ultimate_pdf) as pdf:
                # PAGE 1: MASTER TITLE PAGE
                print("   📄 Creating Master Title Page...")
                fig = plt.figure(figsize=(8.5, 11))
                plt.axis('off')
                
                # Main title
                plt.text(0.5, 0.8, "ONE PDF TO RULE THEM ALL", fontsize=28, 
                        ha='center', va='center', fontweight='bold', color='darkred')
                
                # Subtitle
                plt.text(0.5, 0.7, "J1 PhD Dissertation Notebook", fontsize=20, 
                        ha='center', va='center', fontweight='bold')
                
                # Author info
                plt.text(0.5, 0.6, "Michael Logan Maloney", fontsize=16, 
                        ha='center', va='center')
                plt.text(0.5, 0.55, "Penn State Architectural Engineering Department", fontsize=14, 
                        ha='center', va='center')
                plt.text(0.5, 0.5, "Mechanical System Focus", fontsize=14, 
                        ha='center', va='center')
                
                # Generation info
                plt.text(0.5, 0.4, f"Report Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                        fontsize=12, ha='center', va='center')
                
                # Module count
                plt.text(0.5, 0.3, f"Total Modules: {len(self.module_results)}", fontsize=12, 
                        ha='center', va='center')
                plt.text(0.5, 0.25, f"Google Drive Assets: {len(asset_summary['modules_with_assets'])}", 
                        fontsize=12, ha='center', va='center')
                
                # Target audience
                plt.text(0.5, 0.15, "Target: Dr. Wangda Zuo, Michael Weter (LBNL National Labs)", 
                        fontsize=10, ha='center', va='center', style='italic')
                
                pdf.savefig(fig, facecolor='white')
                plt.close(fig)
                
                # PAGE 2: TABLE OF CONTENTS
                print("   📄 Creating Table of Contents...")
                fig = plt.figure(figsize=(8.5, 11))
                plt.axis('off')
                
                plt.text(0.5, 0.95, "TABLE OF CONTENTS", fontsize=20, 
                        ha='center', va='center', fontweight='bold')
                
                # Generate TOC from module results
                y_pos = 0.85
                page_num = 3  # Start after title and TOC pages
                
                for module_id, result in self.module_results.items():
                    if result['success']:
                        module_info = self.module_config.get(module_id, {})
                        module_name = module_info.get('name', module_id)
                        
                        plt.text(0.1, y_pos, f"{module_id}: {module_name}", fontsize=12, 
                                ha='left', va='center', fontweight='bold')
                        plt.text(0.8, y_pos, str(page_num), fontsize=12, 
                                ha='right', va='center')
                        
                        y_pos -= 0.05
                        page_num += 1
                        
                        # Add submodules if any
                        if module_info.get('type') == 'container' and 'submodules' in module_info:
                            for sub_id, sub_info in module_info['submodules'].items():
                                plt.text(0.15, y_pos, f"  {sub_id}: {sub_info['name']}", fontsize=10, 
                                        ha='left', va='center')
                                plt.text(0.8, y_pos, str(page_num), fontsize=10, 
                                        ha='right', va='center')
                                y_pos -= 0.04
                                page_num += 1
                
                pdf.savefig(fig, facecolor='white')
                plt.close(fig)
                
                # PAGE 3+: MODULE CONTENT PAGES
                print("   📄 Adding Module Content Pages...")
                for module_id, result in self.module_results.items():
                    if result['success']:
                        module_info = self.module_config.get(module_id, {})
                        module_name = module_info.get('name', module_id)
                        
                        # Create module page
                        fig = plt.figure(figsize=(8.5, 11))
                        plt.axis('off')
                        
                        # Module header
                        plt.text(0.5, 0.9, f"MODULE {module_id}", fontsize=18, 
                                ha='center', va='center', fontweight='bold')
                        plt.text(0.5, 0.85, module_name, fontsize=16, 
                                ha='center', va='center')
                        
                        # Module description
                        description = module_info.get('description', 'No description available')
                        # Wrap text for better display
                        wrapped_desc = self.wrap_text(description, 80)
                        y_pos = 0.75
                        for line in wrapped_desc.split('\n'):
                            plt.text(0.1, y_pos, line, fontsize=10, ha='left', va='top')
                            y_pos -= 0.04
                        
                        # Module status
                        plt.text(0.1, 0.6, f"Status: ✅ SUCCESS", fontsize=12, 
                                ha='left', va='center', color='green')
                        
                        # PDF files generated
                        if result.get('pdf_files'):
                            plt.text(0.1, 0.55, f"PDFs Generated: {len(result['pdf_files'])}", 
                                    fontsize=12, ha='left', va='center')
                            
                            # List recent PDFs
                            recent_pdfs = result['pdf_files'][-3:]  # Show last 3
                            y_pos = 0.5
                            for pdf_file in recent_pdfs:
                                plt.text(0.1, y_pos, f"  • {pdf_file.name}", fontsize=10, 
                                        ha='left', va='center')
                                y_pos -= 0.03
                        
                        pdf.savefig(fig, facecolor='white')
                        plt.close(fig)
                
                # ADD GOOGLE DRIVE ASSETS AS FIGURES
                print("   📄 Adding Google Drive Assets as Figures...")
                if asset_summary['modules_with_assets']:
                    for i, module_id in enumerate(asset_summary['modules_with_assets'], 1):
                        asset_path = integrator.get_asset_path(module_id)
                        if asset_path and asset_path.exists():
                            # Create figure page
                            fig = plt.figure(figsize=(8.5, 11))
                            
                            # Load and display image
                            img = PILImage.open(asset_path)
                            ax = plt.subplot(111)
                            ax.imshow(img)
                            ax.axis('off')
                            
                            # Add figure title
                            module_names = {
                                "01.0C": "Problem System Model",
                                "01.0B": "Graphical Abstract", 
                                "01.0A": "Abstract Visualization"
                            }
                            title = module_names.get(module_id, f"Figure {i}")
                            plt.title(f"Figure {i}: {title}", fontsize=16, fontweight='bold', pad=20)
                            
                            # Add caption
                            caption = integrator.create_figure_caption(module_id, f"Figure {i}")
                            plt.figtext(0.5, 0.02, caption, fontsize=10, ha='center', va='bottom',
                                      bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8))
                            
                            pdf.savefig(fig, facecolor='white')
                            plt.close(fig)
                
                # FINAL PAGE: EXECUTION SUMMARY
                print("   📄 Creating Execution Summary...")
                fig = plt.figure(figsize=(8.5, 11))
                plt.axis('off')
                
                plt.text(0.5, 0.9, "EXECUTION SUMMARY", fontsize=20, 
                        ha='center', va='center', fontweight='bold')
                
                # Summary statistics
                successful_modules = [mid for mid, result in self.module_results.items() if result['success']]
                failed_modules = [mid for mid, result in self.module_results.items() if not result['success']]
                
                y_pos = 0.8
                plt.text(0.1, y_pos, f"Total Modules Processed: {len(self.module_results)}", fontsize=14, 
                        ha='left', va='center', fontweight='bold')
                y_pos -= 0.05
                plt.text(0.1, y_pos, f"Successful: {len(successful_modules)}", fontsize=12, 
                        ha='left', va='center', color='green')
                y_pos -= 0.05
                plt.text(0.1, y_pos, f"Failed: {len(failed_modules)}", fontsize=12, 
                        ha='left', va='center', color='red' if failed_modules else 'green')
                y_pos -= 0.05
                plt.text(0.1, y_pos, f"Google Drive Assets: {len(asset_summary['modules_with_assets'])}", fontsize=12, 
                        ha='left', va='center')
                y_pos -= 0.05
                plt.text(0.1, y_pos, f"Total Pages: {len(self.module_results) + 3 + len(asset_summary['modules_with_assets'])}", fontsize=12, 
                        ha='left', va='center')
                
                # Module details
                y_pos -= 0.1
                plt.text(0.1, y_pos, "Module Details:", fontsize=14, 
                        ha='left', va='center', fontweight='bold')
                y_pos -= 0.05
                
                for module_id, result in self.module_results.items():
                    status = "✅" if result['success'] else "❌"
                    module_info = self.module_config.get(module_id, {})
                    module_name = module_info.get('name', module_id)
                    
                    plt.text(0.1, y_pos, f"{status} {module_id}: {module_name}", fontsize=10, 
                            ha='left', va='center')
                    y_pos -= 0.03
                
                # Final message
                plt.text(0.5, 0.1, "🎉 ONE PDF TO RULE THEM ALL - COMPLETE! 🎉", fontsize=16, 
                        ha='center', va='center', fontweight='bold', color='darkred')
                
                pdf.savefig(fig, facecolor='white')
                plt.close(fig)
            
            print(f"   ✅ Ultimate PDF created: {ultimate_pdf}")
            return str(ultimate_pdf)
            
        except Exception as e:
            print(f"   ❌ Ultimate PDF creation failed: {e}")
            # Fallback to original method
            return self.create_j1_dissertation_pdf(self.collect_all_pdfs())
    
    def wrap_text(self, text: str, width: int) -> str:
        """Wrap text to specified width for better display"""
        import textwrap
        return textwrap.fill(text, width=width)
    

def main():
    """Main function - ADVANCED RESEARCH MODE ACTIVATED"""
    orchestrator = J1PhDStudyOrchestrator()
    orchestrator.print_j1_banner()
    
    try:
        # Execute all J1 modules
        orchestrator.execute_all_j1_modules()
        
        # Compile the J1 PhD Dissertation
        dissertation_pdf = orchestrator.compile_j1_dissertation()
        
        print(f"\n🎉 Ph.D. STUDY ENGINEERS NOTEBOOK GENERATION COMPLETE!")
        print(f"📄 Ultimate Output: {dissertation_pdf}")
        print("🚀 ADVANCED RESEARCH MODE: SUCCESSFUL!")
        
    except Exception as e:
        print(f"❌ J1 PhD DISSERTATION ERROR: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
