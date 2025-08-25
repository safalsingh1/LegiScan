from datetime import datetime
from database.vector_store import VectorStore
from services.synthesizer import Synthesizer
from timescale_vector import client
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# Initialize VectorStore
vec = VectorStore()

def clean_score_format(text):
    """Clean up the compliance score format from '71-100: Excellent Compliance' to '71/100'"""
    if "Compliance Score:" in text:
        try:
            # Extract the number from the text
            score = text.split(':')[1].strip()
            if '-' in score:
                score = score.split('-')[0].strip()  # Take the first number before the dash
            if ':' in score:
                score = score.split(':')[0].strip()  # Remove any remaining text after colon
            return f"Compliance Score: {score}/100"
        except:
            return text
    return text

def create_pdf_report(response, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    
    # Set margins to give more space for content
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    
    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Contract Analysis Report", ln=True, align='C')
    pdf.ln(10)
    
    # Main answer section
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Analysis Summary:", ln=True)
    pdf.set_font("Helvetica", "", 11)
    
    # Split answer into paragraphs and clean markdown
    paragraphs = response.answer.split('\n')
    for para in paragraphs:
        # Clean the paragraph of markdown characters
        cleaned_para = para.replace('**', '').replace('*', '').strip()
        if cleaned_para:  # Only process non-empty paragraphs
            # Clean up compliance score format if present
            cleaned_para = clean_score_format(cleaned_para)
            
            # Check if it's a header
            if any(header in cleaned_para for header in ["Compliance Report:", "Strengths:", "Areas for Improvement:", "Reasoning:", "Additional Information:"]):
                pdf.set_font("Helvetica", "B", 12)
                pdf.ln(5)
                pdf.cell(0, 10, cleaned_para, ln=True)
                pdf.set_font("Helvetica", "", 11)
            else:
                # Use multi_cell to handle line breaks properly
                pdf.multi_cell(0, 7, cleaned_para)
                pdf.ln(3)
    
    pdf.ln(10)
    
    # Thought process section
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Detailed Analysis:", ln=True)
    pdf.set_font("Helvetica", "", 11)
    
    for thought in response.thought_process:
        cleaned_thought = thought.replace('**', '').replace('*', '').strip()
        if cleaned_thought:  # Only process non-empty thoughts
            if cleaned_thought.endswith(':'):
                pdf.set_font("Helvetica", "B", 11)
                pdf.ln(5)
                pdf.multi_cell(0, 7, cleaned_thought)
                pdf.set_font("Helvetica", "", 11)
            else:
                if cleaned_thought.startswith('-'):
                    pdf.multi_cell(0, 7, f"  {cleaned_thought}")
                else:
                    pdf.multi_cell(0, 7, cleaned_thought)
            pdf.ln(3)
    
    # Context information
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Context Assessment:", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, f"Sufficient context available: {response.enough_context}")
    
    # Save the PDF
    pdf.output(filename)
