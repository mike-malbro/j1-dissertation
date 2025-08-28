#!/usr/bin/env python3
"""
Module 00.00 - Cover Page Generation
Michael Logan Maloney PhD Dissertation Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

Professional cover page generation.
"""

import sys
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def generate_cover_page():
    """Generate a professional cover page using LaTeX formatting like the J1 Journal 1"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate PDF
    pdf_path = output_dir / f"cover_page_{timestamp}.pdf"
    
    # Main Cover Page LaTeX template - Nice formatting like J1 Journal 1
    latex_content = f"""
\\documentclass[12pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{times}}
\\usepackage{{setspace}}

\\doublespacing

\\begin{{document}}

\\vspace{{2cm}}

\\noindent\\Large\\textbf{{Report}}

\\vspace{{3cm}}

\\noindent\\normalsize\\textbf{{Author: Michael Logan Maloney}}

\\noindent\\normalsize\\textbf{{Position: PhD Student}}

\\noindent\\normalsize\\textbf{{Institution: Pennsylvania State University}}

\\noindent\\normalsize\\textbf{{Department: Architectural Engineering}}

\\noindent\\normalsize\\textbf{{Laboratory: Sustainable Buildings and Societies Laboratory (SBS Lab)}}

\\noindent\\normalsize\\textbf{{Advisor: Dr. Wangda Zuo}}

\\vspace{{2cm}}

\\noindent\\normalsize\\textit{{Report Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}}}

\\vspace{{1cm}}

\\noindent\\small\\textit{{Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}}

\\noindent\\small\\textit{{Module: 00.00 - Cover}}

\\end{{document}}
"""
    
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
            print(f"✅ Cover page generated: {pdf_path}")
            return str(pdf_path)
        else:
            print(f"❌ LaTeX compilation failed: {result.stderr}")
            return generate_simple_cover_page()
            
    except Exception as e:
        print(f"❌ LaTeX generation failed: {e}")
        return generate_simple_cover_page()
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

def generate_simple_cover_page():
    """Fallback simple cover page generation"""
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Simple text file as fallback
    text_path = output_dir / f"cover_page_{timestamp}.txt"
    
    content = f"""
================================================================================
REPORT
================================================================================

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Module: 00.00 - Cover

Author: Michael Logan Maloney
Position: PhD Student
Institution: Pennsylvania State University
Department: Architectural Engineering
Laboratory: Sustainable Buildings and Societies Laboratory (SBS Lab)
Advisor: Dr. Wangda Zuo

Report Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
"""
    
    with open(text_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Simple cover page generated: {text_path}")
    return str(text_path)

def main():
    """Main function to generate cover page"""
    print("🎨 Generating Main Cover Page...")
    
    try:
        output_file = generate_cover_page()
        print(f"📄 Main cover page created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating cover page: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 