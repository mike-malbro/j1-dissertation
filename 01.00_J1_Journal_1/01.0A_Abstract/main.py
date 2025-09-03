#!/usr/bin/env python3
"""
Submodule 1.0A: Abstract - J1 Concept Development
J1 - Working Version to develop the J1 Concept on Paper

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

J1 Concept Development Abstract Generator
"""

# =============================================================================
# USER INPUTS - EDIT THESE VALUES MANUALLY
# =============================================================================

# PAPER INFORMATION
PAPER_TYPE = "Working Version to develop the J1 Concept on Paper"
PAPER_YEAR = "2025"

# PAPER TITLE
WORKING_TITLE = "J1 Working Title: An Optimal Load Allocation for a Heterogeneous Multi Unit CRAC System in Harrisburg Data Center Room"

# AUTHOR INFORMATION
AUTHOR_NAME = "Michael Maloney"
AUTHOR_INSTITUTION = "Penn State Architectural Engineering Department"
AUTHOR_FOCUS = "Mechanical System Focus"

# ABSTRACT TEXT - Main abstract content
ABSTRACT_TEXT = """Data center cooling demands efficient load distribution across Computer Room Air Conditioning (CRAC) units to achieve optimal energy use and balanced equipment runtime. This paper develops a Modelica-based framework for optimal load allocation in a heterogeneous multi-CRAC system—one primary unit and four supplemental split air conditioners—for a 2N · 1 MW data center modeled after a reference facility in Harrisburg, Pennsylvania. Existing models typically address uniform CRAC setups, limiting their ability to handle diverse unit configurations and simultaneous optimization of efficiency and reliability. The proposed approach implements a rule-based load allocation strategy that dynamically assigns cooling loads based on individual unit performance curves, incorporating rotation to even out runtime. Current steady-state results indicate a 15% improvement in energy efficiency compared to conventional controls."""

# ABSTRACT REQUIREMENTS ANALYSIS - The 5 key elements
ABSTRACT_REQUIREMENTS = {
    "current_state_of_art": "Current data center cooling models focus on uniform CRAC setups with conventional control strategies that limit their ability to handle diverse unit configurations.",
    "deficiencies": "Existing models lack the ability to simultaneously optimize efficiency and reliability in heterogeneous multi-CRAC systems.",
    "methods_applied": "Modelica-based framework with rule-based load allocation strategy that dynamically assigns cooling loads based on individual unit performance curves, incorporating rotation.",
    "results": "Current steady-state results indicate a 15% improvement in energy efficiency compared to conventional controls.",
    "lasting_contribution": "This work establishes a framework for optimal load allocation in heterogeneous multi-CRAC systems, enhancing data center cooling optimization capabilities."
}

# TECHNICAL SPECIFICATIONS
TECHNICAL_SPECS = {
    "data_center": "2N · 1 MW facility in Harrisburg, Pennsylvania",
    "crac_configuration": "1 primary + 4 supplemental split air conditioners",
    "modeling_platform": "Modelica",
    "optimization_strategy": "Rule-based load allocation with dynamic assignment and rotation",
    "energy_savings": "15% improvement versus conventional controls",
    "target_application": "Heterogeneous multi-CRAC systems in data centers"
}

# MODULE INFORMATION
MODULE_ID = "01.0A"
MODULE_NAME = "Abstract"
MODULE_DESCRIPTION = "J1 Concept Development Abstract"

# =============================================================================
# END USER INPUTS - DO NOT EDIT BELOW THIS LINE
# =============================================================================

import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from jinja2 import Template
import warnings
warnings.filterwarnings('ignore')

def generate_j1_abstract():
    """Generate J1 Concept Development abstract"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate PDF
    pdf_path = output_dir / f"abstract_{MODULE_ID}_{timestamp}.pdf"
    
    # J1 Concept Development LaTeX template
    latex_content = f"""
\\documentclass[12pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{times}}
\\usepackage{{enumitem}}
\\usepackage{{setspace}}
\\usepackage{{color}}

\\doublespacing

\\begin{{document}}

\\begin{{center}}
\\Large\\textbf{{ABSTRACT}}

\\vspace{{0.5cm}}

\\large\\textbf{{{WORKING_TITLE}}}

\\vspace{{0.5cm}}
\\end{{center}}

\\textbf{{Abstract:}}

\\vspace{{0.2cm}}

{ABSTRACT_TEXT}

\\vspace{{0.5cm}}

\\textbf{{Abstract Questions and Response:}}

\\vspace{{0.2cm}}

\\begin{{itemize}}[leftmargin=0.5in, itemsep=0.1cm]
\\item \\textbf{{What is the current state of the art:}} {ABSTRACT_REQUIREMENTS['current_state_of_art']}
\\item \\textbf{{What are its deficiencies:}} {ABSTRACT_REQUIREMENTS['deficiencies']}
\\item \\textbf{{What methods have been applied:}} {ABSTRACT_REQUIREMENTS['methods_applied']}
\\item \\textbf{{What are the results:}} {ABSTRACT_REQUIREMENTS['results']}
\\item \\textbf{{What is the lasting contribution of the submission:}} {ABSTRACT_REQUIREMENTS['lasting_contribution']}
\\end{{itemize}}

\\vspace{{0.5cm}}

\\begin{{center}}
\\small\\textit{{Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}}

\\small\\textit{{Module: {MODULE_ID} - {MODULE_NAME} ({MODULE_DESCRIPTION})}}
\\end{{center}}

\\end{{document}}
"""
    
    # LaTeX content is already generated with f-string above
    
    # Create temporary LaTeX file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
        f.write(latex_content)
        tex_file = f.name
    
    try:
        # Compile LaTeX to PDF using pdflatex
        result = subprocess.run([
            'pdflatex',
            '-interaction=nonstopmode',
            '-output-directory=' + str(output_dir),
            tex_file
        ], capture_output=True, text=True, timeout=60)
        
        # Look for the generated PDF in the output directory
        generated_pdf = output_dir / Path(tex_file).with_suffix('.pdf').name
        if generated_pdf.exists():
            generated_pdf.rename(pdf_path)
            print(f"✅ Generated J1 abstract: {pdf_path}")
            return str(pdf_path)
        else:
            print(f"❌ LaTeX compilation failed: {result.stderr}")
            return generate_simple_j1_abstract()
            
    except Exception as e:
        print(f"❌ LaTeX generation failed: {e}")
        return generate_simple_j1_abstract()
    finally:
        # Clean up temporary files
        try:
            Path(tex_file).unlink()
            aux_file = Path(tex_file).with_suffix('.aux')
            log_file = Path(tex_file).with_suffix('.log')
            if aux_file.exists():
                aux_file.unlink()
            if log_file.exists():
                log_file.unlink()
        except:
            pass

def generate_simple_j1_abstract():
    """Simple matplotlib fallback for J1 abstract"""
    try:
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages
        import textwrap
        
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate PDF
        pdf_path = output_dir / f"abstract_{MODULE_ID}_{timestamp}.pdf"
        
        with PdfPages(pdf_path) as pdf:
            # Create figure with proper margins
            fig = plt.figure(figsize=(8.5, 11))  # Letter size
            plt.axis('off')
            
            # Set font to Arial
            plt.rcParams['font.family'] = 'Arial'
            plt.rcParams['font.sans-serif'] = ['Arial']
            
            # Define proper spacing constants
            TOP_MARGIN = 0.95
            LINE_HEIGHT = 0.05
            SECTION_SPACING = 0.08
            
            # Title - properly positioned
            plt.text(0.5, TOP_MARGIN, 'ABSTRACT', 
                    fontsize=24, weight='bold', ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            # Paper title - properly positioned with spacing
            y_pos = TOP_MARGIN - LINE_HEIGHT
            title_lines = textwrap.wrap(WORKING_TITLE, width=50)
            for line in title_lines:
                plt.text(0.5, y_pos, line, 
                        fontsize=18, weight='bold', ha='center', va='center',
                        color='black', fontfamily='Arial', transform=plt.gca().transAxes)
                y_pos -= LINE_HEIGHT
            
            # Abstract section - properly positioned
            y_pos -= SECTION_SPACING
            plt.text(0.5, y_pos, 'Abstract:', 
                    fontsize=16, weight='bold', ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            # Abstract text with proper spacing and layout
            y_pos -= LINE_HEIGHT
            
            # Split into sentences and format each properly
            sentences = ABSTRACT_TEXT.split('. ')
            
            for i, sentence in enumerate(sentences):
                if sentence.strip():
                    # Add period back if it's not the last sentence
                    if i < len(sentences) - 1:
                        sentence = sentence + '.'
                    
                    # Wrap text to fit page width (60 characters for safety)
                    wrapped_text = textwrap.fill(sentence, width=60)
                    
                    # Split into lines and position each line with proper spacing
                    lines = wrapped_text.split('\n')
                    for line in lines:
                        if line.strip():  # Only add non-empty lines
                            plt.text(0.5, y_pos, line, 
                                    fontsize=12, ha='center', va='center',
                                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
                            y_pos -= LINE_HEIGHT
                    
                    # Add extra space between sentences
                    y_pos -= 0.02
            
            # Abstract Questions and Response section
            y_pos -= SECTION_SPACING
            plt.text(0.5, y_pos, 'Abstract Questions and Response:', 
                    fontsize=14, weight='bold', ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            requirements = [
                f"• What is the current state of the art: {ABSTRACT_REQUIREMENTS['current_state_of_art']}",
                f"• What are its deficiencies: {ABSTRACT_REQUIREMENTS['deficiencies']}",
                f"• What methods have been applied: {ABSTRACT_REQUIREMENTS['methods_applied']}",
                f"• What are the results: {ABSTRACT_REQUIREMENTS['results']}",
                f"• What is the lasting contribution of the submission: {ABSTRACT_REQUIREMENTS['lasting_contribution']}"
            ]
            
            y_pos -= LINE_HEIGHT
            for req in requirements:
                wrapped_req = textwrap.fill(req, width=70)
                lines = wrapped_req.split('\n')
                for line in lines:
                    if line.strip():
                        plt.text(0.5, y_pos, line, 
                                fontsize=11, ha='center', va='center',
                                color='black', fontfamily='Arial', transform=plt.gca().transAxes)
                        y_pos -= LINE_HEIGHT
                y_pos -= 0.02
            
            # Page number
            plt.text(0.5, 0.05, "4", fontsize=14, fontweight='normal',
                    ha='center', va='center', fontfamily='Arial', transform=plt.gca().transAxes)
            
            # Timestamp - properly positioned at bottom
            plt.text(0.5, 0.03, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 
                    fontsize=10, ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            # Module identifier
            plt.text(0.5, 0.01, f'Module: {MODULE_ID} - {MODULE_NAME} ({MODULE_DESCRIPTION})', 
                    fontsize=10, ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            pdf.savefig(fig, facecolor='white')
            plt.close(fig)
        
        print(f"✅ Generated J1 abstract: {pdf_path}")
        return str(pdf_path)
        
    except Exception as e:
        print(f"❌ All generation methods failed: {e}")
        return None

def main():
    """Main function to generate J1 abstract"""
    print("🎨 Generating J1 Concept Development Abstract...")
    
    try:
        output_file = generate_j1_abstract()
        if output_file:
            print(f"📄 J1 abstract created successfully: {output_file}")
            return True
        else:
            print("❌ Failed to generate abstract")
            return False
    except Exception as e:
        print(f"❌ Error generating abstract: {e}")
        return False

if __name__ == "__main__":
    success = main()
    import sys
    sys.exit(0 if success else 1) 