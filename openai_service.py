import os
from openai import OpenAI
from typing import List, Dict

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_text(text: str, filename: str = "") -> str:
    """
    Generate a summary of the provided text using OpenAI
    
    Args:
        text (str): Text content to summarize
        filename (str): Optional filename for context
        
    Returns:
        str: Generated summary
        
    Raises:
        Exception: If OpenAI API call fails
    """
    try:
        # Truncate text if too long (OpenAI has token limits)
        max_chars = 12000  # Conservative limit to stay within token limits
        if len(text) > max_chars:
            text = text[:max_chars] + "... [text truncated]"
        
        prompt = f"""Please provide a comprehensive summary of the following document{f' ({filename})' if filename else ''}. 

The summary should:
- Capture the main topics and key points
- Be well-structured with clear sections
- Include important details and findings
- Be approximately 200-400 words
- Use clear, professional language

Document content:
{text}"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert document analyzer and summarizer. Create clear, comprehensive summaries that capture the essence of documents while maintaining important details."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=600,
            temperature=0.3
        )
        
        summary = response.choices[0].message.content
        if summary:
            summary = summary.strip()
        
        if not summary:
            raise Exception("OpenAI returned an empty summary")
            
        return summary
        
    except Exception as e:
        raise Exception(f"Failed to generate summary: {str(e)}")

def synthesize_summaries(summaries: List[Dict]) -> str:
    """
    Create a comprehensive synthesis from multiple document summaries
    
    Args:
        summaries (List[Dict]): List of summary dictionaries with 'filename' and 'summary' keys
        
    Returns:
        str: Comprehensive synthesis
        
    Raises:
        Exception: If OpenAI API call fails
    """
    try:
        if not summaries:
            raise Exception("No summaries provided for synthesis")
        
        # Prepare the summaries text
        summaries_text = ""
        for i, summary_data in enumerate(summaries, 1):
            summaries_text += f"\n\nDocument {i}: {summary_data['filename']}\n"
            summaries_text += f"Summary: {summary_data['summary']}"
        
        prompt = f"""I have {len(summaries)} document summaries that I need you to synthesize. Please follow these exact formatting instructions:

1. Extract and understand the **main ideas, themes, and insights** from each document.
2. Create a structured synthesis that includes:
   - **Common themes** across all documents
   - **Key differences** in perspective, focus, or tone
   - **Outlier or unique ideas** that appear in only one or a few documents
   - A brief summary of each document individually

Format your output in **Markdown**, using headings, subheadings, and tables where appropriate to improve readability. Use concise, professional language.

Use this EXACT structure:

### 📌 Common Themes
List major insights or conclusions that appear across multiple documents.
**Theme 1:** Description
**Theme 2:** Description
**Theme 3:** Description

### 🔍 Key Differences
Use a table format to compare how different documents approach major themes.
| Theme / Topic        | Doc 1 Perspective | Doc 2 Perspective | Doc 3 Perspective |
|----------------------|-------------------|-------------------|-------------------|
| Theme A              | Summary           | Summary           | Summary           |
| Theme B              | Summary           | Summary           | Summary           |

### ⚠️ Outlier / Unique Themes
Highlight any ideas or approaches that appear in only one or two documents.
- Doc X uniquely emphasizes [idea]
- Doc Y presents a counterintuitive argument about [topic]

### 📄 Individual Document Summaries
#### Doc 1: [Filename]
- **Main Idea:** 
- **Key Points:** 
- **Tone/Perspective:** 

#### Doc 2: [Filename]
- **Main Idea:** 
- **Key Points:** 
- **Tone/Perspective:** 

Stay neutral, avoid repetition, and be precise. Assume your audience is analytical and values clarity over verbosity.

Here are the individual document summaries:
{summaries_text}"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert analyst who specializes in synthesizing information from multiple sources. Create comprehensive, well-structured analyses that reveal insights and connections across documents."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1200,
            temperature=0.3
        )
        
        synthesis = response.choices[0].message.content
        if synthesis:
            synthesis = synthesis.strip()
        
        if not synthesis:
            raise Exception("OpenAI returned an empty synthesis")
            
        return synthesis
        
    except Exception as e:
        raise Exception(f"Failed to create synthesis: {str(e)}")

def validate_api_key() -> bool:
    """
    Validate if the OpenAI API key is working
    
    Returns:
        bool: True if API key is valid, False otherwise
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        return True
    except:
        return False
