import streamlit as st
from similarity_search import vec, Synthesizer, create_pdf_report, clean_score_format
import base64
import PyPDF2
import io
import pandas as pd
import numpy as np


def chunk_text(text, chunk_size=8000):
    """Split text into chunks of specified size"""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def read_pdf(file):
    """Extract text from uploaded PDF file"""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def read_txt(file):
    """Read text from uploaded TXT file"""
    return file.getvalue().decode("utf-8")

def process_large_text(text):
    """Process large text in chunks and combine results"""
    chunks = chunk_text(text)
    all_results = []
    
    # Process each chunk
    progress_bar = st.progress(0)
    for i, chunk in enumerate(chunks):
        # Update progress bar
        progress = (i + 1) / len(chunks)
        progress_bar.progress(progress)
        
        # Search for each chunk
        results = vec.search(chunk, limit=3)
        all_results.append(results)
    
    # Combine results
    combined_results = pd.concat(all_results)
    
    # Convert any numpy arrays or lists to strings for deduplication
    for column in combined_results.columns:
        if hasattr(combined_results[column], 'dtype'):
            if 'object' in str(combined_results[column].dtype):
                combined_results[column] = combined_results[column].apply(
                    lambda x: str(x) if isinstance(x, (list, np.ndarray)) else x
                )
    
    # Drop duplicates based on content
    combined_results = combined_results.drop_duplicates(subset=['content'])
    
    # Take the first 3 results if more exist
    if len(combined_results) > 3:
        combined_results = combined_results.head(3)
    
    # Create metadata dictionary
    combined_results['metadata'] = combined_results.apply(
        lambda x: {
            'agreement_date': x['agreement_date'],
            'effective_date': x['effective_date'],
            'expiration_date': x['expiration_date']
        }, 
        axis=1
    )
    
    return combined_results

def get_pdf_download_link(pdf_path):
    """Generate a download link for the PDF file"""
    with open(pdf_path, "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="contract_analysis_report.pdf">Download PDF Report</a>'
        return href

def main():
    st.title("Contract Analysis System")
    
    # File upload section - allow multiple files
    uploaded_files = st.file_uploader("Upload Contract Documents", type=['pdf', 'txt'], accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                # Extract text based on file type
                if uploaded_file.type == "application/pdf":
                    contract_text = read_pdf(uploaded_file)
                    st.success(f"PDF file '{uploaded_file.name}' uploaded successfully!")
                else:  # txt file
                    contract_text = read_txt(uploaded_file)
                    st.success(f"TXT file '{uploaded_file.name}' uploaded successfully!")
                
                # Display the extracted text
                with st.expander(f"View Extracted Text for {uploaded_file.name}"):
                    st.text_area("Contract Text", contract_text, height=200)
                
                # Analyze button
                if st.button(f"Analyze Contract: {uploaded_file.name}"):
                    # Show a spinner while processing
                    with st.spinner(f'Analyzing contract: {uploaded_file.name}...'):
                        # Process the text in chunks
                        results = process_large_text(contract_text)
                        
                        # Generate response
                        response = Synthesizer.generate_response(
                            question=contract_text,
                            context=results[['content', 'metadata']]
                        )
                        
                        # Create PDF
                        pdf_filename = f"{uploaded_file.name}_analysis_report.pdf"
                        create_pdf_report(response, pdf_filename)
                        
                        # Display the report sections in Streamlit
                        st.header(f"Analysis Report for {uploaded_file.name}")
                        
                        # Display main answer with proper formatting
                        paragraphs = response.answer.split('\n')
                        for para in paragraphs:
                            cleaned_para = para.replace('**', '').replace('*', '').strip()
                            if cleaned_para:
                                # Clean up compliance score format if present
                                cleaned_para = clean_score_format(cleaned_para)
                                
                                if any(header in cleaned_para for header in 
                                      ["Compliance Report:", "Strengths:", "Areas for Improvement:", 
                                       "Reasoning:", "Additional Information:"]):
                                    st.subheader(cleaned_para)
                                else:
                                    st.write(cleaned_para)
                        
                        # Display thought process
                        st.subheader("Detailed Analysis")
                        for thought in response.thought_process:
                            cleaned_thought = thought.replace('**', '').replace('*', '').strip()
                            if cleaned_thought:
                                st.write(cleaned_thought)
                        
                        # Display context assessment
                        st.subheader("Context Assessment")
                        st.write(f"Sufficient context available: {response.enough_context}")
                        
                        # Add download button for PDF
                        st.markdown(get_pdf_download_link(pdf_filename), unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"Error processing file '{uploaded_file.name}': {str(e)}")

if __name__ == "__main__":
    main()