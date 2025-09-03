#!/usr/bin/env python3
"""
Module 01.00 - J1 Journal 1 Cover Page
Michael Logan Maloney PhD Dissertation Notebook

Author: Michael Maloney
PhD Student - Penn State Architectural Engineering Department
Mechanical System Focus

J1 - The first Journal Paper. This will be the most important.
As much of the future work will look at this as a base.
"""

import sys
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def generate_j1_cover_page():
    """Generate a professional J1 cover page using LaTeX formatting like the abstract"""
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate PDF
    pdf_path = output_dir / f"journal_1_01.00_{timestamp}.pdf"
    
    # J1 Journal 1 Cover Page LaTeX template - Nice formatting like abstract
    latex_content = f"""
\\documentclass[12pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{times}}
\\usepackage{{setspace}}

\\doublespacing

\\begin{{document}}

\\vspace{{2cm}}

\\noindent\\Large\\textbf{{J1 - Working Title: An Optimal Load Allocation for a Heterogeneous Multi Unit CRAC System in Harrisburg Data Center Room}}

\\vspace{{2cm}}

\\noindent\\normalsize\\textit{{Report Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}}}

\\vspace{{1cm}}

\\noindent\\small\\textit{{Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}}

\\noindent\\small\\textit{{Module: 01.00 - J1 Journal 1}}

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
            print(f"✅ J1 cover page generated: {pdf_path}")
            return str(pdf_path)
        else:
            print(f"❌ LaTeX compilation failed: {result.stderr}")
            return generate_simple_j1_cover_page()
            
    except Exception as e:
        print(f"❌ LaTeX generation failed: {e}")
        return generate_simple_j1_cover_page()
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

def generate_simple_j1_cover_page():
    """Fallback simple cover page generation"""
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Simple text file as fallback
    text_path = output_dir / f"journal_1_01.00_{timestamp}.txt"
    
    content = f"""
================================================================================
J1 - WORKING TITLE: AN OPTIMAL LOAD ALLOCATION FOR MULTI CRAC FOR HARRISBURG DATA CENTER
================================================================================

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Module: 01.00 - J1 Journal 1

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
    
    print(f"✅ Simple J1 cover page generated: {text_path}")
    return str(text_path)

def main():
    """Main function to generate J1 cover page"""
    print("🎨 Generating J1 Journal 1 Cover Page...")
    
    try:
        output_file = generate_j1_cover_page()
        print(f"📄 J1 cover page created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating J1 cover page: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
