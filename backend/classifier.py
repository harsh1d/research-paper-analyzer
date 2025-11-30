"""
NLP Classification Module - FIXED VERSION
Handles long texts by proper truncation and chunking
"""

from transformers import pipeline, AutoTokenizer
import torch
import yake
import spacy
from typing import List, Dict, Any
import re

class ResearchPaperClassifier:
    """
    Multi-task classifier for research papers
    Fixed to handle long texts properly
    """
    
    def __init__(self):
        """
        Initialize all classification pipelines
        Uses GPU if available, otherwise CPU
        """
        device = 0 if torch.cuda.is_available() else -1
        
        print("Initializing NLP models...")
        
        # Topic classification using zero-shot
        self.topic_classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=device,
            truncation=True,  # Enable truncation
            max_length=512    # Set max length
        )
        
        # Sentiment analysis
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=device,
            truncation=True,
            max_length=512
        )
        
        # Keyword extraction (YAKE - unsupervised)
        self.kw_extractor = yake.KeywordExtractor(
            lan="en",
            n=3,
            dedupLim=0.7,
            top=20,
            features=None
        )
        
        # spaCy for NER and linguistic analysis
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Downloading spaCy model...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        print("✓ All models loaded successfully!")
    
    def preprocess_text(self, text: str) -> str:
        """
        Clean and normalize text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep periods and commas
        text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
        return text.strip()
    
    def safe_truncate(self, text: str, max_words: int = 400) -> str:
        """
        Safely truncate text to avoid token length errors
        Uses word count as proxy for token count
        
        Args:
            text: Input text
            max_words: Maximum number of words (default 400 ≈ 500 tokens)
            
        Returns:
            Truncated text
        """
        words = text.split()
        if len(words) > max_words:
            return ' '.join(words[:max_words])
        return text
    
    def extract_abstract(self, text: str) -> str:
        """
        Try to extract abstract section for better classification
        Falls back to first N words if abstract not found
        """
        # Look for abstract section
        abstract_pattern = r"(?i)abstract[\s:]*(.{100,2000}?)(?=\n\n|\nintroduction|\nkeywords)"
        match = re.search(abstract_pattern, text)
        
        if match:
            return match.group(1).strip()
        
        # Fallback: return first 500 words
        return self.safe_truncate(text, max_words=500)
    
    def classify_topic(self, text: str) -> Dict[str, Any]:
        """
        Classify research paper into domain categories
        FIXED: Properly handles long texts
        
        Args:
            text: Research paper text
            
        Returns:
            Topic classification results with confidence scores
        """
        candidate_labels = [
            "artificial intelligence and machine learning",
            "healthcare and medicine",
            "finance and economics",
            "biology and life sciences",
            "engineering and technology",
            "physics and astronomy",
            "chemistry and materials science",
            "computer science and software",
            "environmental science",
            "social sciences and psychology"
        ]
        
        # Use abstract or first 400 words for classification
        sample_text = self.extract_abstract(text)
        sample_text = self.safe_truncate(sample_text, max_words=400)
        
        try:
            result = self.topic_classifier(
                sample_text,
                candidate_labels=candidate_labels,
                multi_label=False
            )
            
            return {
                "primary_topic": result["labels"][0],
                "confidence": round(result["scores"][0] * 100, 2),
                "secondary_topics": [
                    {"topic": result["labels"][i], "confidence": round(result["scores"][i] * 100, 2)}
                    for i in range(1, min(4, len(result["labels"])))
                ]
            }
        except Exception as e:
            print(f"Topic classification error: {e}")
            return {
                "primary_topic": "Unable to classify",
                "confidence": 0.0,
                "secondary_topics": []
            }
    
    def detect_sections(self, text: str) -> Dict[str, Any]:
        """
        Detect common research paper sections
        Uses pattern matching and section headers
        """
        sections = {
            "abstract": r"(?i)(abstract|summary)[\s:]*",
            "introduction": r"(?i)(introduction|background)[\s:]*",
            "methodology": r"(?i)(method|methodology|materials and methods|experimental setup)[\s:]*",
            "results": r"(?i)(results|findings)[\s:]*",
            "discussion": r"(?i)(discussion|analysis)[\s:]*",
            "conclusion": r"(?i)(conclusion|summary|future work)[\s:]*",
            "references": r"(?i)(references|bibliography|works cited)[\s:]*"
        }
        
        detected = {}
        lines = text.split('\n')
        
        for section_name, pattern in sections.items():
            for i, line in enumerate(lines):
                if re.match(pattern, line.strip()) and len(line.strip()) < 50:
                    # Extract content after header
                    start_idx = text.find(line)
                    snippet = text[start_idx:start_idx + 500].replace('\n', ' ')
                    detected[section_name] = {
                        "found": True,
                        "position": i,
                        "snippet": snippet[:200] + "..."
                    }
                    break
        
        return {
            "sections_found": list(detected.keys()),
            "total_sections": len(detected),
            "details": detected
        }
    
    def classify_methodology(self, text: str) -> Dict[str, Any]:
        """
        Classify research methodology type
        FIXED: Properly handles long texts
        """
        methodology_types = [
            "qualitative research",
            "quantitative research",
            "experimental study",
            "simulation and modeling",
            "survey and questionnaire",
            "case study",
            "literature review",
            "mixed methods"
        ]
        
        # Try to find methods section
        methods_pattern = r"(?i)(method|methodology)[\s:]*(.{100,2000}?)(?=\n\n|results|discussion)"
        match = re.search(methods_pattern, text)
        
        if match:
            methods_text = match.group(2)
        else:
            # Use middle portion of paper
            words = text.split()
            start = len(words) // 4
            methods_text = ' '.join(words[start:start + 400])
        
        methods_text = self.safe_truncate(methods_text, max_words=400)
        
        try:
            result = self.topic_classifier(
                methods_text,
                candidate_labels=methodology_types,
                multi_label=True
            )
            
            return {
                "primary_methodology": result["labels"][0],
                "confidence": round(result["scores"][0] * 100, 2),
                "secondary_methodologies": [
                    {"method": result["labels"][i], "confidence": round(result["scores"][i] * 100, 2)}
                    for i in range(1, min(3, len(result["labels"])))
                ]
            }
        except Exception as e:
            print(f"Methodology classification error: {e}")
            return {
                "primary_methodology": "Unable to classify",
                "confidence": 0.0,
                "secondary_methodologies": []
            }
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze overall tone and sentiment
        FIXED: Properly truncates text
        """
        # Use abstract or first portion
        sample = self.extract_abstract(text)
        sample = self.safe_truncate(sample, max_words=400)
        
        try:
            result = self.sentiment_analyzer(sample)[0]
            
            # Map sentiment to academic tone
            tone_mapping = {
                "POSITIVE": "Optimistic/Constructive",
                "NEGATIVE": "Critical/Cautionary"
            }
            
            return {
                "sentiment": result["label"],
                "confidence": round(result["score"] * 100, 2),
                "academic_tone": tone_mapping.get(result["label"], "Neutral/Analytical")
            }
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {
                "sentiment": "NEUTRAL",
                "confidence": 50.0,
                "academic_tone": "Neutral/Analytical"
            }
    
    def extract_keywords(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract important keywords using YAKE
        Handles long texts by using representative sample
        """
        # Use first 3000 words for keyword extraction
        sample_text = self.safe_truncate(text, max_words=3000)
        
        try:
            keywords = self.kw_extractor.extract_keywords(sample_text)
            
            return [
                {"keyword": kw[0], "relevance_score": round((1 - kw[1]) * 100, 2)}
                for kw in keywords[:15]
            ]
        except Exception as e:
            print(f"Keyword extraction error: {e}")
            return []
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """
        Extract named entities using spaCy
        """
        # Process first 50000 characters (spaCy limit)
        sample = text[:50000]
        
        try:
            doc = self.nlp(sample)
            
            entities = {}
            for ent in doc.ents:
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                if ent.text not in entities[ent.label_] and len(entities[ent.label_]) < 5:
                    entities[ent.label_].append(ent.text)
            
            return entities
        except Exception as e:
            print(f"Entity extraction error: {e}")
            return {}
    
    def classify_contribution_type(self, text: str) -> Dict[str, Any]:
        """
        Identify research contribution type
        FIXED: Properly handles long texts
        """
        contribution_types = [
            "literature review and survey",
            "original empirical research",
            "case study analysis",
            "comparative analysis",
            "theoretical framework",
            "experimental validation",
            "meta-analysis"
        ]
        
        # Use abstract and introduction
        sample = self.extract_abstract(text)
        sample = self.safe_truncate(sample, max_words=400)
        
        try:
            result = self.topic_classifier(
                sample,
                candidate_labels=contribution_types,
                multi_label=False
            )
            
            return {
                "contribution_type": result["labels"][0],
                "confidence": round(result["scores"][0] * 100, 2)
            }
        except Exception as e:
            print(f"Contribution classification error: {e}")
            return {
                "contribution_type": "Unable to classify",
                "confidence": 0.0
            }
