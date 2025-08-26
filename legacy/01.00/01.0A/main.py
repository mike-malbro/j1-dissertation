#!/usr/bin/env python3
"""
Submodule 1.0A: Abstract - Modern 2025 LaTeX Document Generator
J1 - Conference Paper 1 SIMBUILD 2027

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Modern Python LaTeX document generation using Jinja2 templates.
"""

import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from jinja2 import Template
import warnings
warnings.filterwarnings('ignore')

def generate_modern_latex_abstract():
    """Generate professional abstract using modern Python LaTeX approach"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # User's exact abstract text
    abstract_text = """Effective data center cooling requires precise control of Computer Room Air Conditioning (CRAC) units to balance energy efficiency and equipment runtime. This paper employs Modelica to optimize a multi-CRAC system—one primary unit and four supplemental split air conditioners—for a 2N · 1 MW data center modeled after a reference facility located in Harrisburg, Pennsylvania. Current Models consider single type CRAC systems which may limit potential performance and reliability optimization of data centers. The Modelica model will contain a rule based optimization based on optimal performance for each CRAC Main and 4 Supplemental Units with rotation. Current Steady State Results indicate (15%) energy savings potential versus conventional control. This work can enhance future building performance research on heterogeneous equipment and systems in data centers."""
    
    # Generate PDF
    pdf_path = output_dir / f"abstract_1.0A_{timestamp}.pdf"
    
    # Modern LaTeX template using Jinja2
    latex_template = r"""
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{times}
\usepackage{enumitem}
\usepackage{setspace}
\usepackage{color}

\doublespacing

\begin{document}

\begin{center}
\Large\textbf{ABSTRACT}

\vspace{0.5cm}

\normalsize\textit{SIMBUILD 2027 Conference Paper}

\vspace{0.3cm}

\large\textbf{Multi-System Modeling of Data Center Cooling:}

\textbf{Optimizing Control of Five CRAC Units for Energy Efficiency and Runtime in Harrisburg}

\vspace{0.3cm}

\normalsize\textbf{Author: Michael Maloney}

PhD Student - Penn State Architectural Engineering Department

Mechanical System Focus

\vspace{0.5cm}
\end{center}

\textbf{Abstract:}

\vspace{0.2cm}

{{ abstract_paragraphs }}

\vspace{0.5cm}

\textbf{Key Details:}

\vspace{0.2cm}

\begin{itemize}[leftmargin=0.5in, itemsep=0.1cm]
\item \textbf{Data Center:} 2N · 1 MW facility in Harrisburg, Pennsylvania
\item \textbf{CRAC Configuration:} 1 primary + 4 supplemental split air conditioners
\item \textbf{Methodology:} Modelica-based optimization
\item \textbf{Innovation:} Rule-based optimization with CRAC rotation
\item \textbf{Energy Savings:} 15\% versus conventional control
\item \textbf{Target:} Heterogeneous equipment and systems in data centers
\end{itemize}

\vspace{0.5cm}

\begin{center}
\small\textit{Generated: {{ timestamp }}}
\end{center}

\end{document}
"""
    
    # Split abstract into sentences and format properly
    sentences = abstract_text.split('. ')
    abstract_paragraphs = []
    
    for i, sentence in enumerate(sentences):
        if sentence.strip():
            # Add period back if it's not the last sentence
            if i < len(sentences) - 1:
                sentence = sentence + '.'
            abstract_paragraphs.append(sentence)
    
    # Join paragraphs with proper spacing
    formatted_abstract = ' '.join(abstract_paragraphs)
    
    # Render template
    template = Template(latex_template)
    latex_content = template.render(
        abstract_paragraphs=formatted_abstract,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
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
            print(f"✅ Generated modern LaTeX abstract: {pdf_path}")
            return str(pdf_path)
        else:
            print(f"❌ LaTeX compilation failed: {result.stderr}")
            return generate_simple_abstract()
            
    except Exception as e:
        print(f"❌ LaTeX generation failed: {e}")
        return generate_simple_abstract()
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

def generate_simple_abstract():
    """Simple matplotlib fallback for when LaTeX fails"""
    try:
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages
        import textwrap
        
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # User's exact abstract text
        abstract_text = """Effective data center cooling requires precise control of Computer Room Air Conditioning (CRAC) units to balance energy efficiency and equipment runtime. This paper employs Modelica to optimize a multi-CRAC system—one primary unit and four supplemental split air conditioners—for a 2N · 1 MW data center modeled after a reference facility located in Harrisburg, Pennsylvania. Current Models consider single type CRAC systems which may limit potential performance and reliability optimization of data centers. The Modelica model will contain a rule based optimization based on optimal performance for each CRAC Main and 4 Supplemental Units with rotation. Current Steady State Results indicate (15%) energy savings potential versus conventional control. This work can enhance future building performance research on heterogeneous equipment and systems in data centers."""
        
        # Generate PDF
        pdf_path = output_dir / f"abstract_1.0A_{timestamp}.pdf"
        
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
            plt.text(0.5, y_pos, 'SIMBUILD 2027 Conference Paper', 
                    fontsize=16, ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            # Paper title - properly positioned with spacing
            y_pos -= LINE_HEIGHT
            plt.text(0.5, y_pos, 'Multi-System Modeling of Data Center Cooling:', 
                    fontsize=18, weight='bold', ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            y_pos -= LINE_HEIGHT
            plt.text(0.5, y_pos, 'Optimizing Control of Five CRAC Units for Energy Efficiency and Runtime in Harrisburg', 
                    fontsize=18, weight='bold', ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            # Author info - properly positioned
            y_pos -= SECTION_SPACING
            plt.text(0.5, y_pos, 'Author: Michael Maloney', 
                    fontsize=14, weight='bold', ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            y_pos -= LINE_HEIGHT
            plt.text(0.5, y_pos, 'PhD Student - Penn State Architectural Engineering Department', 
                    fontsize=12, ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            y_pos -= LINE_HEIGHT
            plt.text(0.5, y_pos, 'Mechanical System Focus', 
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
            sentences = abstract_text.split('. ')
            
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
            
            # Key details section - properly positioned
            y_pos -= SECTION_SPACING
            plt.text(0.5, y_pos, 'Key Details:', 
                    fontsize=14, weight='bold', ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            key_details = [
                "• Data Center: 2N · 1 MW facility in Harrisburg, Pennsylvania",
                "• CRAC Configuration: 1 primary + 4 supplemental split air conditioners",
                "• Methodology: Modelica-based optimization",
                "• Innovation: Rule-based optimization with CRAC rotation",
                "• Energy Savings: 15% versus conventional control",
                "• Target: Heterogeneous equipment and systems in data centers"
            ]
            
            y_pos -= LINE_HEIGHT
            for detail in key_details:
                plt.text(0.5, y_pos, detail, 
                        fontsize=11, ha='center', va='center',
                        color='black', fontfamily='Arial', transform=plt.gca().transAxes)
                y_pos -= LINE_HEIGHT
            
            # Timestamp - properly positioned at bottom
            plt.text(0.5, 0.05, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 
                    fontsize=10, ha='center', va='center',
                    color='black', fontfamily='Arial', transform=plt.gca().transAxes)
            
            pdf.savefig(fig, facecolor='white', bbox_inches='tight')
            plt.close(fig)
        
        print(f"✅ Generated simple abstract: {pdf_path}")
        return str(pdf_path)
        
    except Exception as e:
        print(f"❌ All generation methods failed: {e}")
        return None

if __name__ == "__main__":
    generate_modern_latex_abstract() 