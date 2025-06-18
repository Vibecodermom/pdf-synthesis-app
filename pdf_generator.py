from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import io
from typing import List, Dict

def create_summary_pdf(summaries: List[Dict], synthesis: str) -> io.BytesIO:
    """
    Generate a PDF document containing the synthesis and individual summaries
    
    Args:
        summaries (List[Dict]): List of summary dictionaries
        synthesis (str): Comprehensive synthesis text
        
    Returns:
        io.BytesIO: PDF content as bytes buffer
    """
    # Create a BytesIO buffer to hold the PDF
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.darkblue,
        alignment=1  # Center alignment
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=16,
        textColor=colors.darkgreen
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        leading=14
    )
    
    # Build the document content
    story = []
    
    # Title page
    story.append(Paragraph("PDF Document Synthesis Report", title_style))
    story.append(Spacer(1, 20))
    
    # Generate metadata
    current_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    story.append(Paragraph(f"Generated on: {current_date}", body_style))
    story.append(Paragraph(f"Number of documents analyzed: {len(summaries)}", body_style))
    story.append(Spacer(1, 30))
    
    # Document list
    story.append(Paragraph("Documents Analyzed:", section_style))
    for i, summary_data in enumerate(summaries, 1):
        story.append(Paragraph(f"{i}. {summary_data['filename']} ({summary_data['word_count']:,} words)", body_style))
    
    story.append(PageBreak())
    
    # Comprehensive synthesis section
    story.append(Paragraph("Comprehensive Synthesis", subtitle_style))
    story.append(Spacer(1, 12))
    
    # Split synthesis into paragraphs and add them
    synthesis_paragraphs = synthesis.split('\n\n')
    for para in synthesis_paragraphs:
        if para.strip():
            # Handle markdown-style headers
            if para.startswith('##'):
                header_text = para.replace('##', '').strip()
                story.append(Paragraph(header_text, section_style))
            elif para.startswith('#'):
                header_text = para.replace('#', '').strip()
                story.append(Paragraph(header_text, section_style))
            elif para.startswith('**') and para.endswith('**'):
                # Bold paragraph
                bold_text = para.replace('**', '').strip()
                story.append(Paragraph(f"<b>{bold_text}</b>", body_style))
            else:
                # Regular paragraph
                story.append(Paragraph(para.strip(), body_style))
    
    story.append(PageBreak())
    
    # Individual summaries section
    story.append(Paragraph("Individual Document Summaries", subtitle_style))
    story.append(Spacer(1, 12))
    
    for i, summary_data in enumerate(summaries, 1):
        # Document header
        story.append(Paragraph(f"Document {i}: {summary_data['filename']}", section_style))
        story.append(Paragraph(f"Original word count: {summary_data['word_count']:,} words", body_style))
        story.append(Spacer(1, 8))
        
        # Summary content
        summary_paragraphs = summary_data['summary'].split('\n\n')
        for para in summary_paragraphs:
            if para.strip():
                # Handle markdown-style formatting
                if para.startswith('##'):
                    header_text = para.replace('##', '').strip()
                    story.append(Paragraph(header_text, section_style))
                elif para.startswith('#'):
                    header_text = para.replace('#', '').strip()
                    story.append(Paragraph(header_text, section_style))
                elif para.startswith('**') and para.endswith('**'):
                    # Bold paragraph
                    bold_text = para.replace('**', '').strip()
                    story.append(Paragraph(f"<b>{bold_text}</b>", body_style))
                else:
                    # Regular paragraph
                    story.append(Paragraph(para.strip(), body_style))
        
        # Add separator between documents (except for the last one)
        if i < len(summaries):
            story.append(Spacer(1, 20))
            story.append(Paragraph("─" * 50, body_style))
            story.append(Spacer(1, 20))
    
    # Footer
    story.append(PageBreak())
    story.append(Spacer(1, 50))
    story.append(Paragraph("End of Report", ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=1  # Center alignment
    )))
    
    # Build the PDF
    try:
        doc.build(story)
        buffer.seek(0)
        return buffer
    except Exception as e:
        raise Exception(f"Error generating PDF: {str(e)}")

def clean_text_for_pdf(text: str) -> str:
    """
    Clean text to be safe for PDF generation
    
    Args:
        text (str): Raw text
        
    Returns:
        str: Cleaned text safe for PDF
    """
    if not text:
        return ""
    
    # Replace problematic characters
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('&', '&amp;')
    
    # Remove or replace other problematic characters
    text = text.replace('\r\n', '\n')
    text = text.replace('\r', '\n')
    
    return text
