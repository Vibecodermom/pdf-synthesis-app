import streamlit as st
import tempfile
import os
from pdf_processor import extract_text_from_pdf
from openai_service import summarize_text, synthesize_summaries
from pdf_generator import create_summary_pdf
import io

# Configure page layout and styling
st.set_page_config(
    page_title="AI Document Synthesis",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling matching SlidesGO design
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 2rem;
        line-height: 1.5;
        max-width: 600px;
    }
    
    .hero-visual {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .upload-section {
        background: #f8fafc;
        padding: 2rem;
        border-radius: 16px;
        border: 2px dashed #d1d5db;
        margin: 2rem 0;
        text-align: center;
    }
    
    .action-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        margin: 2rem 0;
        color: white;
        text-align: center;
    }
    
    .file-item {
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .file-item:hover {
        transform: translateX(4px);
    }
    
    .stButton > button {
        background: #1f2937;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(31, 41, 55, 0.2);
    }
    
    .stButton > button:hover {
        background: #374151;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(31, 41, 55, 0.3);
    }
    
    .get-started-btn > button {
        background: #1f2937 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(31, 41, 55, 0.2) !important;
    }
    
    .get-started-btn > button:hover {
        background: #374151 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(31, 41, 55, 0.3) !important;
    }
    
    .success-message {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
    }
    
    .info-message {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: white;
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #667eea;
        background: #f8fafc;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Create header with modern layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h1 class="main-header">Free AI Document Synthesis</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Transform multiple PDF documents into comprehensive insights with AI. Upload your documents and get intelligent summaries, comparative analysis, and structured reports in seconds.</p>', unsafe_allow_html=True)
        
        # Get Started button with custom styling
        st.markdown('<div class="get-started-btn">', unsafe_allow_html=True)
        if st.button("Get started →", key="get_started", help="Start analyzing your documents"):
            st.session_state.show_upload = True
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Visual content matching the SlidesGO style
        st.markdown("""
        <div class="hero-visual">
            <h3 style="margin: 0; color: white; font-size: 1.5rem;">Document Analysis</h3>
            <p style="margin: 1rem 0; color: rgba(255,255,255,0.9); font-size: 0.95rem;">
                AI-powered synthesis and analysis
            </p>
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <span style="font-size: 0.9rem;">✨ Comprehensive insights from your documents</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Show upload section if Get Started was clicked or files are present
    if st.session_state.get("show_upload", False) or "uploaded_files" in st.session_state:
        st.markdown("---")
        
        # File upload section with modern styling
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown("### 📄 Upload Your Documents")
        st.markdown("Select multiple PDF files to analyze and synthesize")
        
        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type=['pdf'],
            accept_multiple_files=True,
            help="Select one or more PDF files to analyze and summarize",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files
            
            # Display uploaded files with modern styling
            st.markdown(f'<div class="success-message">✅ {len(uploaded_files)} file(s) uploaded successfully</div>', unsafe_allow_html=True)
            
            # File list
            st.markdown("**Uploaded Documents:**")
            for i, file in enumerate(uploaded_files, 1):
                st.markdown(f'<div class="file-item">{i}. <strong>{file.name}</strong> ({file.size:,} bytes)</div>', 
                           unsafe_allow_html=True)
            
            # Action section with gradient background
            st.markdown('<div class="action-section">', unsafe_allow_html=True)
            st.markdown("### 🚀 Generate AI Analysis")
            st.markdown("Transform your documents into structured insights with comprehensive synthesis")
            
            if st.button("Generate Summary", type="primary", use_container_width=True):
                process_files(uploaded_files)
            st.markdown('</div>', unsafe_allow_html=True)
        
        elif st.session_state.get("show_upload", False):
            st.markdown('<div class="info-message">📤 Select PDF files above to begin analysis</div>', unsafe_allow_html=True)
            
            # Show features with modern card styling
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                <div class="feature-card">
                    <h4 style="color: #1f2937; margin-bottom: 1rem;">🔍 Smart Analysis</h4>
                    <ul style="color: #6b7280; margin: 0; padding-left: 1rem;">
                        <li>Extract key themes</li>
                        <li>Identify differences</li>
                        <li>Find unique insights</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("""
                <div class="feature-card">
                    <h4 style="color: #1f2937; margin-bottom: 1rem;">📊 Structured Output</h4>
                    <ul style="color: #6b7280; margin: 0; padding-left: 1rem;">
                        <li>Common themes table</li>
                        <li>Comparative analysis</li>
                        <li>Individual summaries</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown("""
                <div class="feature-card">
                    <h4 style="color: #1f2937; margin-bottom: 1rem;">📄 Professional Reports</h4>
                    <ul style="color: #6b7280; margin: 0; padding-left: 1rem;">
                        <li>Downloadable PDF</li>
                        <li>Markdown formatting</li>
                        <li>Clean, readable layout</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

def process_files(uploaded_files):
    """Process uploaded PDF files and generate summary"""
    
    # Initialize progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Extract text from all PDFs
        status_text.text("📖 Extracting text from PDF files...")
        extracted_texts = []
        file_names = []
        
        for i, uploaded_file in enumerate(uploaded_files):
            # Update progress
            progress = (i + 1) / (len(uploaded_files) * 4)  # 4 total steps
            progress_bar.progress(progress)
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            try:
                # Extract text from PDF
                text = extract_text_from_pdf(tmp_file_path)
                if text.strip():
                    extracted_texts.append(text)
                    file_names.append(uploaded_file.name)
                else:
                    st.warning(f"⚠️ No readable text found in {uploaded_file.name}")
            except Exception as e:
                st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
            finally:
                # Clean up temporary file
                os.unlink(tmp_file_path)
        
        if not extracted_texts:
            st.error("❌ No readable text found in any of the uploaded PDFs")
            return
        
        # Step 2: Generate individual summaries
        status_text.text("🤖 Generating AI summaries for each document...")
        summaries = []
        
        for i, (text, filename) in enumerate(zip(extracted_texts, file_names)):
            # Update progress
            progress = (len(uploaded_files) + i + 1) / (len(uploaded_files) * 4)
            progress_bar.progress(progress)
            
            try:
                summary = summarize_text(text, filename)
                summaries.append({
                    'filename': filename,
                    'summary': summary,
                    'word_count': len(text.split())
                })
            except Exception as e:
                st.error(f"❌ Error summarizing {filename}: {str(e)}")
                return
        
        # Step 3: Create comprehensive synthesis
        status_text.text("🔄 Creating comprehensive synthesis...")
        progress_bar.progress(0.75)
        
        try:
            synthesis = synthesize_summaries(summaries)
        except Exception as e:
            st.error(f"❌ Error creating synthesis: {str(e)}")
            return
        
        # Step 4: Generate PDF
        status_text.text("📄 Generating downloadable PDF...")
        progress_bar.progress(0.9)
        
        try:
            pdf_buffer = create_summary_pdf(summaries, synthesis)
        except Exception as e:
            st.error(f"❌ Error generating PDF: {str(e)}")
            return
        
        # Complete
        progress_bar.progress(1.0)
        status_text.text("✅ Processing complete!")
        
        # Display results
        st.success("🎉 Summary generated successfully!")
        
        # Show preview of synthesis
        with st.expander("👀 Preview of Comprehensive Synthesis", expanded=True):
            st.markdown(synthesis)
        
        # Show individual summaries
        with st.expander("📑 Individual Document Summaries"):
            for i, summary_data in enumerate(summaries, 1):
                st.subheader(f"{i}. {summary_data['filename']}")
                st.write(f"**Original word count:** {summary_data['word_count']:,}")
                st.markdown(summary_data['summary'])
                st.divider()
        
        # Download button
        st.download_button(
            label="📥 Download Summary PDF",
            data=pdf_buffer.getvalue(),
            file_name="pdf_synthesis_summary.pdf",
            mime="application/pdf",
            type="primary"
        )
        
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")
    finally:
        # Clean up progress indicators
        progress_bar.empty()
        status_text.empty()

if __name__ == "__main__":
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        st.error("❌ OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        st.info("You can get an API key from: https://platform.openai.com/api-keys")
        st.stop()
    
    main()
