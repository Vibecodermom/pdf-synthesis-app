# PDF Synthesis App

AI-powered PDF document synthesis application that analyzes multiple PDF files and generates comprehensive summaries with structured insights.

## Features

- Upload multiple PDF files simultaneously
- AI-powered document analysis using OpenAI GPT-4o
- Structured synthesis with common themes, key differences, and unique insights
- Professional PDF report generation
- Modern, responsive web interface

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```
4. Run the application:
```bash
streamlit run app.py
```

## Deployment

This app is designed for deployment on Streamlit Cloud. Simply:
1. Fork this repository
2. Connect it to Streamlit Cloud
3. Add your OpenAI API key in the secrets management
4. Deploy

## Usage

1. Upload one or more PDF files
2. Click "Generate Summary" 
3. Review the AI-generated synthesis
4. Download the comprehensive PDF report

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for AI processing