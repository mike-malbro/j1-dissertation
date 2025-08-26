#!/usr/bin/env python3
"""
Submodule 1.0A: Abstract - SIMBUILD 2027 Conference Paper
J1 - Conference Paper 1 SIMBUILD 2027

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

SIMBUILD 2027 Conference Paper Abstract Generator
"""

# =============================================================================
# USER INPUTS - EDIT THESE VALUES MANUALLY
# =============================================================================

# CONFERENCE INFORMATION
CONFERENCE_NAME = "SIMBUILD 2027 Conference Paper"
CONFERENCE_YEAR = "2027"

# PAPER TITLE
WORKING_TITLE = "Multi-System Modeling of Data Center Cooling: Optimizing Control of Five CRAC Units for Energy Efficiency and Runtime in Harrisburg"

# AUTHOR INFORMATION
AUTHOR_NAME = "Michael Maloney"
AUTHOR_INSTITUTION = "Penn State Architectural Engineering Department"
AUTHOR_FOCUS = "Mechanical System Focus"

# ABSTRACT TEXT - Main abstract content
ABSTRACT_TEXT = """Effective data center cooling requires precise control of Computer Room Air Conditioning (CRAC) units to balance energy efficiency and equipment runtime. This paper employs Modelica to optimize a multi-CRAC system—one primary unit and four supplemental split air conditioners—for a 2N · 1 MW data center modeled after a reference facility located in Harrisburg, Pennsylvania. Current Models consider single type CRAC systems which may limit potential performance and reliability optimization of data centers. The Modelica model will contain a rule based optimization based on optimal performance for each CRAC Main and 4 Supplemental Units with rotation. Current Steady State Results indicate (15%) energy savings potential versus conventional control. This work can enhance future building performance research on heterogeneous equipment and systems in data centers."""

# ABSTRACT REQUIREMENTS ANALYSIS - The 5 key elements
ABSTRACT_REQUIREMENTS = {
    "current_state_of_art": "Current data center cooling models focus on single-type CRAC systems with conventional control strategies that prioritize either energy efficiency or equipment runtime, but not both simultaneously.",
    "deficiencies": "Existing models lack consideration of heterogeneous CRAC configurations and fail to optimize for both energy efficiency and equipment runtime in multi-unit systems.",
    "methods_applied": "Modelica-based modeling approach with rule-based optimization for a multi-CRAC system (1 primary + 4 supplemental units) with rotation strategies.",
    "results": "Current steady-state results indicate 15% energy savings potential versus conventional control methods.",
    "lasting_contribution": "This work establishes a framework for heterogeneous equipment optimization in data centers, enhancing future building performance research on multi-system configurations."
}

# TECHNICAL SPECIFICATIONS
TECHNICAL_SPECS = {
    "data_center": "2N · 1 MW facility in Harrisburg, Pennsylvania",
    "crac_configuration": "1 primary + 4 supplemental split air conditioners",
    "modeling_platform": "Modelica",
    "optimization_strategy": "Rule-based optimization with CRAC rotation",
    "energy_savings": "15% versus conventional control",
    "target_application": "Heterogeneous equipment and systems in data centers"
}

# MODULE INFORMATION
MODULE_ID = "01.0A"
MODULE_NAME = "Abstract"
MODULE_DESCRIPTION = "SIMBUILD 2027 Conference Paper Abstract"

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

def generate_simbuild_abstract():
    """Generate SIMBUILD 2027 Conference Paper abstract"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate PDF
    pdf_path = output_dir / f"abstract_{MODULE_ID}_{timestamp}.pdf"
    
    # SIMBUILD 2027 LaTeX template - Simplified to avoid syntax issues
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

\\normalsize\\textit{{{CONFERENCE_NAME}}}

\\vspace{{0.3cm}}

\\large\\textbf{{{WORKING_TITLE}}}

\\vspace{{0.3cm}}

\\normalsize\\textbf{{Author: {AUTHOR_NAME}}}

{AUTHOR_INSTITUTION}

{AUTHOR_FOCUS}

\\vspace{{0.5cm}}
\\end{{center}}

\\textbf{{Abstract:}}

\\vspace{{0.2cm}}

{ABSTRACT_TEXT}

\\vspace{{0.5cm}}

\\textbf{{Abstract Requirements Analysis:}}

\\vspace{{0.2cm}}

\\begin{{itemize}}[leftmargin=0.5in, itemsep=0.1cm]
\\item \\textbf{{Current State of the Art:}} {ABSTRACT_REQUIREMENTS['current_state_of_art']}
\\item \\textbf{{Deficiencies:}} {ABSTRACT_REQUIREMENTS['deficiencies']}
\\item \\textbf{{Methods Applied:}} {ABSTRACT_REQUIREMENTS['methods_applied']}
\\item \\textbf{{Results:}} {ABSTRACT_REQUIREMENTS['results']}
\\item \\textbf{{Lasting Contribution:}} {ABSTRACT_REQUIREMENTS['lasting_contribution']}
\\end{{itemize}}

\\vspace{{0.5cm}}

\\textbf{{Technical Specifications:}}

\\vspace{{0.2cm}}

\\begin{{itemize}}[leftmargin=0.5in, itemsep=0.1cm]
\\item \\textbf{{Data Center:}} {TECHNICAL_SPECS['data_center']}
\\item \\textbf{{CRAC Configuration:}} {TECHNICAL_SPECS['crac_configuration']}
\\item \\textbf{{Modeling Platform:}} {TECHNICAL_SPECS['modeling_platform']}
\\item \\textbf{{Optimization Strategy:}} {TECHNICAL_SPECS['optimization_strategy']}
\\item \\textbf{{Energy Savings:}} {TECHNICAL_SPECS['energy_savings']}
\\item \\textbf{{Target Application:}} {TECHNICAL_SPECS['target_application']}
\\end{{itemize}}

\\vspace{{0.5cm}}

\\begin{{center}}
\\small\\textit{{Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}}

\\small\\textit{{Module: {MODULE_ID} - {MODULE_NAME} ({CONFERENCE_NAME})}}
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
            print(f"✅ Generated SIMBUILD 2027 abstract: {pdf_path}")
            return str(pdf_path)
        else:
            print(f"❌ LaTeX compilation failed: {result.stderr}")
            return generate_simple_simbuild_abstract()
            
    except Exception as e:
        print(f"❌ LaTeX generation failed: {e}")
        return generate_simple_simbuild_abstract()
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

def generate_simple_simbuild_abstract():
    """Simple matplotlib fallback for SIMBUILD 2027 abstract"""
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
            
            # Conference info - properly positioned
            y_pos = TOP_MARGIN - LINE_HEIGHT
            plt.text(0.5, y_pos, CONFERENCE_NAME, 
                    fontsize=16, ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            # Paper title - properly positioned with spacing
            y_pos -= LINE_HEIGHT
            title_lines = textwrap.wrap(WORKING_TITLE, width=50)
            for line in title_lines:
                plt.text(0.5, y_pos, line, 
                        fontsize=18, weight='bold', ha='center', va='center',
                        color='black', fontfamily='Arial', transform=plt.gca().transAxes)
                y_pos -= LINE_HEIGHT
            
            # Author info - properly positioned
            y_pos -= SECTION_SPACING
            plt.text(0.5, y_pos, f"Author: {AUTHOR_NAME}", 
                    fontsize=14, weight='bold', ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            y_pos -= LINE_HEIGHT
            plt.text(0.5, y_pos, AUTHOR_INSTITUTION, 
                    fontsize=12, ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            y_pos -= LINE_HEIGHT
            plt.text(0.5, y_pos, AUTHOR_FOCUS, 
                    fontsize=12, ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
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
            
            # Abstract Requirements Analysis section
            y_pos -= SECTION_SPACING
            plt.text(0.5, y_pos, 'Abstract Requirements Analysis:', 
                    fontsize=14, weight='bold', ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            requirements = [
                f"• Current State of the Art: {ABSTRACT_REQUIREMENTS['current_state_of_art']}",
                f"• Deficiencies: {ABSTRACT_REQUIREMENTS['deficiencies']}",
                f"• Methods Applied: {ABSTRACT_REQUIREMENTS['methods_applied']}",
                f"• Results: {ABSTRACT_REQUIREMENTS['results']}",
                f"• Lasting Contribution: {ABSTRACT_REQUIREMENTS['lasting_contribution']}"
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
            
            # Technical Specifications section
            y_pos -= SECTION_SPACING
            plt.text(0.5, y_pos, 'Technical Specifications:', 
                    fontsize=14, weight='bold', ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            specs = [
                f"• Data Center: {TECHNICAL_SPECS['data_center']}",
                f"• CRAC Configuration: {TECHNICAL_SPECS['crac_configuration']}",
                f"• Modeling Platform: {TECHNICAL_SPECS['modeling_platform']}",
                f"• Optimization Strategy: {TECHNICAL_SPECS['optimization_strategy']}",
                f"• Energy Savings: {TECHNICAL_SPECS['energy_savings']}",
                f"• Target Application: {TECHNICAL_SPECS['target_application']}"
            ]
            
            y_pos -= LINE_HEIGHT
            for spec in specs:
                plt.text(0.5, y_pos, spec, 
                        fontsize=11, ha='center', va='center',
                        color='black', fontfamily='Arial', transform=plt.gca().transAxes)
                y_pos -= LINE_HEIGHT
            
            # Page number
            plt.text(0.5, 0.05, "3", fontsize=14, fontweight='normal',
                    ha='center', va='center', fontfamily='Arial', transform=plt.gca().transAxes)
            
            # Timestamp - properly positioned at bottom
            plt.text(0.5, 0.03, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 
                    fontsize=10, ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            # Module identifier
            plt.text(0.5, 0.01, f'Module: {MODULE_ID} - {MODULE_NAME} ({CONFERENCE_NAME})', 
                    fontsize=10, ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            pdf.savefig(fig, facecolor='white', bbox_inches='tight')
            plt.close(fig)
        
        print(f"✅ Generated SIMBUILD 2027 abstract: {pdf_path}")
        return str(pdf_path)
        
    except Exception as e:
        print(f"❌ All generation methods failed: {e}")
        return None

def main():
    """Main function to generate SIMBUILD 2027 abstract"""
    print("🎨 Generating SIMBUILD 2027 Conference Paper Abstract...")
    
    try:
        output_file = generate_simbuild_abstract()
        if output_file:
            print(f"📄 SIMBUILD 2027 abstract created successfully: {output_file}")
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