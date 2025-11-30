"""
Vercel Serverless Entry Point
Lightweight version without heavy ML models
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import PyPDF2
from docx import Document
import io
import re
from collections import Counter

app = FastAPI(
    title="Research Paper Analyzer API - Serverless",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file_bytes):
    """Extract text from PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except:
        return ""

def extract_text_from_docx(file_bytes):
    """Extract text from DOCX"""
    try:
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join([para.text for para in doc.paragraphs])
    except:
        return ""

def simple_keyword_extraction(text):
    """Simple keyword extraction without ML"""
    # Remove common words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as'}
    
    # Extract words
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    words = [w for w in words if w not in stop_words]
    
    # Count frequency
    word_freq = Counter(words)
    
    # Return top 15
    return [{"keyword": word, "relevance_score": 90 - i*5} for i, (word, _) in enumerate(word_freq.most_common(15))]

def detect_sections(text):
    """Detect paper sections using regex"""
    sections = {
        "abstract": r"(?i)(abstract|summary)[\s:]*",
        "introduction": r"(?i)(introduction|background)[\s:]*",
        "methodology": r"(?i)(method|methodology)[\s:]*",
        "results": r"(?i)(results|findings)[\s:]*",
        "discussion": r"(?i)(discussion)[\s:]*",
        "conclusion": r"(?i)(conclusion)[\s:]*",
        "references": r"(?i)(references|bibliography)[\s:]*"
    }
    
    detected = []
    for section_name, pattern in sections.items():
        if re.search(pattern, text):
            detected.append(section_name)
    
    return {
        "sections_found": detected,
        "total_sections": len(detected),
        "details": {}
    }

def basic_topic_detection(text):
    """Basic topic detection using keyword matching"""
    topics = {
        "artificial intelligence": ["ai", "machine learning", "neural network", "deep learning", "algorithm"],
        "healthcare and medicine": ["patient", "medical", "clinical", "disease", "treatment", "healthcare"],
        "computer science": ["software", "programming", "algorithm", "computer", "data structure"],
        "biology": ["cell", "protein", "gene", "dna", "organism", "biological"],
        "physics": ["energy", "particle", "quantum", "force", "physics"],
        "chemistry": ["molecule", "chemical", "reaction", "compound", "synthesis"]
    }
    
    text_lower = text.lower()
    topic_scores = {}
    
    for topic, keywords in topics.items():
        score = sum(text_lower.count(kw) for kw in keywords)
        topic_scores[topic] = score
    
    # Get top topic
    top_topic = max(topic_scores, key=topic_scores.get)
    max_score = topic_scores[top_topic]
    confidence = min(100, (max_score / 10) * 100) if max_score > 0 else 50
    
    return {
        "primary_topic": top_topic,
        "confidence": round(confidence, 2),
        "secondary_topics": []
    }

@app.get("/")
async def root():
    return {
        "message": "Research Paper Analyzer API - Serverless Edition",
        "status": "running",
        "note": "Limited features on serverless. For full ML features, use dedicated hosting.",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/analyze")
async def analyze_paper(file: UploadFile = File(...)):
    """
    Lightweight analysis without heavy ML models
    """
    try:
        # Validate file
        allowed_extensions = ['.pdf', '.docx', '.txt']
        file_extension = '.' + file.filename.split('.')[-1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(400, f"Unsupported format. Use {', '.join(allowed_extensions)}")
        
        # Read file
        contents = await file.read()
        
        # Extract text
        if file_extension == '.pdf':
            text = extract_text_from_pdf(contents)
        elif file_extension == '.docx':
            text = extract_text_from_docx(contents)
        else:
            text = contents.decode('utf-8')
        
        if len(text.strip()) < 100:
            raise HTTPException(400, "Text too short")
        
        # Basic analysis
        word_count = len(text.split())
        char_count = len(text)
        
        # Get basic insights
        topic = basic_topic_detection(text)
        sections = detect_sections(text)
        keywords = simple_keyword_extraction(text)
        
        response = {
            "status": "success",
            "filename": file.filename,
            "file_info": {
                "type": file_extension,
                "size_kb": round(len(contents) / 1024, 2)
            },
            "statistics": {
                "word_count": word_count,
                "character_count": char_count
            },
            "topic_classification": topic,
            "section_analysis": sections,
            "keywords": keywords,
            "note": "This is a lightweight version. For full ML analysis with BERT, deploy on Render.com or Railway.app"
        }
        
        return JSONResponse(content=response)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Analysis failed: {str(e)}")

# Vercel requires this
handler = app
