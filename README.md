
# Research Paper Analyzer

An AI-powered application for analyzing and extracting insights from research papers using Azure OpenAI services.

## Features

- **PDF Processing**: Extract and analyze content from research paper PDFs
- **AI-Powered Analysis**: Leverage Azure OpenAI for intelligent paper analysis
- **Key Insights Extraction**: Automatically identify methodology, results, and conclusions
- **Interactive Interface**: User-friendly web interface for uploading and analyzing papers
- **Structured Output**: Get organized summaries with key findings and contributions

## Prerequisites

- Python 3.8+
- Azure OpenAI API access
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd research-paper-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file
AZURE_OPENAI_ENDPOINT=<your-endpoint>
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_DEPLOYMENT_NAME=<your-deployment-name>
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Upload a research paper PDF

4. View the AI-generated analysis including:
    - Paper summary
    - Key methodologies
    - Main results
    - Conclusions and contributions

## Project Structure

```
research-paper-analyzer/
├── app.py              # Main application file
├── models/             # AI models and processing logic
├── static/             # Static assets (CSS, JS)
├── templates/          # HTML templates
├── uploads/            # Temporary PDF storage
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Technology Stack

- **Backend**: Flask/FastAPI
- **AI Service**: Azure OpenAI
- **PDF Processing**: PyPDF2/pdfplumber
- **Frontend**: HTML, CSS, JavaScript

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Specify your license here]

## Acknowledgments

- Azure OpenAI for AI capabilities
- [Other libraries and tools used]
