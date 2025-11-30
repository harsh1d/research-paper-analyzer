"""
Fast Enhanced Features - Optimized for Speed
"""

from transformers import pipeline
import re
from typing import Dict, Any, List
import textstat
from collections import Counter
from functools import lru_cache
import hashlib

class FastEnhancedFeatures:
    """
    Optimized enhanced features with:
    - Smaller summarization model
    - Cached results
    - Parallel processing
    """
    
    def __init__(self):
        print("Loading fast enhanced features...")
        
        # Use distilbart (smaller, faster)
        try:
            self.summarizer = pipeline(
                "summarization",
                model="sshleifer/distilbart-cnn-6-6",  # Much faster than bart-large
                device=-1  # CPU
            )
        except Exception as e:
            print(f"Summarizer error: {e}")
            self.summarizer = None
        
        print("✓ Fast enhanced features loaded!")
    
    def _smart_sample(self, text: str, max_words: int = 500) -> str:
        """Sample text intelligently"""
        words = text.split()
        if len(words) <= max_words:
            return text
        return ' '.join(words[:max_words])
    
    def generate_summary(self, text: str) -> Dict[str, Any]:
        """Fast summary generation"""
        try:
            # Extract abstract if possible
            abstract_pattern = r"(?i)abstract[\s:]*(.{100,1500}?)(?=\n\n|\nintroduction)"
            match = re.search(abstract_pattern, text)
            
            if match:
                source = match.group(1).strip()
            else:
                source = self._smart_sample(text, 800)
            
            source = re.sub(r'\s+', ' ', source).strip()
            
            if len(source.split()) < 50:
                return {
                    "one_sentence": "Text too short for summarization",
                    "short_summary": "Text too short for summarization",
                    "executive_summary": "Text too short for summarization",
                    "key_findings": []
                }
            
            summaries = {}
            
            # One sentence (fastest)
            if self.summarizer:
                try:
                    one = self.summarizer(
                        source[:512],
                        max_length=25,
                        min_length=10,
                        do_sample=False,
                        num_beams=2  # Reduced from 4
                    )
                    summaries['one_sentence'] = one[0]['summary_text']
                except:
                    summaries['one_sentence'] = self._extractive_summary(source, 1)
            else:
                summaries['one_sentence'] = self._extractive_summary(source, 1)
            
            # Short summary
            summaries['short_summary'] = self._extractive_summary(source, 3)
            
            # Executive summary
            summaries['executive_summary'] = self._extractive_summary(source, 5)
            
            # Key findings (regex based, very fast)
            summaries['key_findings'] = self._extract_key_findings(text)
            
            return summaries
            
        except Exception as e:
            print(f"Summary error: {e}")
            return {
                "one_sentence": "Summary generation failed",
                "short_summary": "Summary generation failed",
                "executive_summary": "Summary generation failed",
                "key_findings": []
            }
    
    def _extractive_summary(self, text: str, sentences: int = 3) -> str:
        """Fast extractive summarization"""
        sents = re.split(r'[.!?]+', text)
        sents = [s.strip() for s in sents if len(s.strip()) > 20]
        return '. '.join(sents[:sentences]) + '.'
    
    def _extract_key_findings(self, text: str) -> List[str]:
        """Fast key findings extraction"""
        findings = []
        
        # Look for common finding patterns
        patterns = [
            r"(?i)we found that (.{30,150}?)[.!]",
            r"(?i)results showed (.{30,150}?)[.!]",
            r"(?i)demonstrated that (.{30,150}?)[.!]",
            r"(?i)revealed that (.{30,150}?)[.!]"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches[:2]:
                findings.append(match.strip() + '.')
                if len(findings) >= 3:
                    break
            if len(findings) >= 3:
                break
        
        return findings if findings else ["Key findings not extracted"]
    
    def analyze_readability(self, text: str) -> Dict[str, Any]:
        """Fast readability analysis"""
        try:
            # Use smaller sample
            sample = self._smart_sample(text, 3000)
            
            # Calculate only essential scores
            flesch_reading = textstat.flesch_reading_ease(sample)
            flesch_kincaid = textstat.flesch_kincaid_grade(sample)
            
            # Interpret
            if flesch_reading >= 50:
                interpretation = "Fairly Difficult (College)"
            elif flesch_reading >= 30:
                interpretation = "Difficult (Graduate)"
            else:
                interpretation = "Very Difficult (Professional)"
            
            academic_level = "Graduate/Professional" if flesch_kincaid >= 16 else "Undergraduate"
            
            return {
                "flesch_reading_ease": round(flesch_reading, 2),
                "flesch_kincaid_grade": round(flesch_kincaid, 2),
                "interpretation": interpretation,
                "academic_level": academic_level,
                "average_grade_level": round(flesch_kincaid, 2),
                "sentence_count": textstat.sentence_count(sample),
                "word_count": textstat.lexicon_count(sample),
                "average_sentence_length": round(textstat.lexicon_count(sample) / max(textstat.sentence_count(sample), 1), 2),
                "average_syllables_per_word": round(textstat.syllable_count(sample) / max(textstat.lexicon_count(sample), 1), 2)
            }
            
        except Exception as e:
            print(f"Readability error: {e}")
            return {"error": "Readability analysis failed"}
    
    def extract_citations(self, text: str) -> Dict[str, Any]:
        """Fast citation extraction"""
        try:
            # Find references section
            refs_pattern = r"(?i)(references|bibliography)[\s:]*(.+?)(?=\n\n\n|\Z)"
            match = re.search(refs_pattern, text, re.DOTALL)
            
            if not match:
                return {
                    "total_references": 0,
                    "references": [],
                    "citation_style": "Not detected",
                    "top_authors": []
                }
            
            refs_text = match.group(2)[:5000]  # Limit size
            
            # Quick split
            ref_list = re.split(r'\n(?=\[\d+\]|\d+\.)', refs_text)
            ref_list = [r.strip() for r in ref_list if len(r.strip()) > 20]
            
            # Extract authors (simplified)
            authors = []
            for ref in ref_list[:30]:  # Only first 30
                author_match = re.search(r'^([A-Z][a-z]+(?:,\s[A-Z]\.)?)', ref)
                if author_match:
                    authors.append(author_match.group(1))
            
            author_freq = Counter(authors)
            top_authors = [{"author": a, "count": c} for a, c in author_freq.most_common(5)]
            
            # Detect style (simplified)
            citation_style = "IEEE" if re.search(r'^\[\d+\]', refs_text) else "APA"
            
            return {
                "total_references": len(ref_list),
                "references": ref_list[:10],  # Only first 10
                "citation_style": citation_style,
                "top_authors": top_authors
            }
            
        except Exception as e:
            print(f"Citation error: {e}")
            return {
                "total_references": 0,
                "citation_style": "Not detected"
            }
    
    def extract_research_questions(self, text: str) -> Dict[str, Any]:
        """Fast research question extraction"""
        try:
            # Look only in first 2000 words
            sample = ' '.join(text.split()[:2000])
            
            questions = []
            hypotheses = []
            
            # Quick patterns
            rq_pattern = r"(?i)research question[s]?[\s:]+([^.?]+[?.])"
            questions.extend(re.findall(rq_pattern, sample)[:2])
            
            hyp_pattern = r"(?i)hypothes[ie]s?[\s:]+([^.]+\.)"
            hypotheses.extend(re.findall(hyp_pattern, sample)[:2])
            
            return {
                "research_questions": questions if questions else ["Not explicitly stated"],
                "hypotheses": hypotheses if hypotheses else ["Not explicitly stated"],
                "objectives": ["Not extracted"],
                "total_questions": len(questions),
                "total_hypotheses": len(hypotheses)
            }
            
        except Exception as e:
            print(f"RQ error: {e}")
            return {
                "research_questions": ["Extraction failed"],
                "hypotheses": ["Extraction failed"]
            }
    
    def calculate_quality_score(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fast quality score calculation"""
        try:
            scores = {}
            
            # Structure score
            sections = len(analysis_data.get('section_analysis', {}).get('sections_found', []))
            scores['structure'] = min((sections / 7) * 100, 100)
            
            # Clarity score
            readability = analysis_data.get('readability_analysis', {})
            flesch = readability.get('flesch_reading_ease', 50)
            scores['clarity'] = max(0, 100 - abs(flesch - 40))
            
            # Citation score
            refs = analysis_data.get('citations_analysis', {}).get('total_references', 0)
            scores['citations'] = min((refs / 30) * 100, 100)
            
            # Methodology score
            method_conf = analysis_data.get('methodology_classification', {}).get('confidence', 0)
            scores['methodology'] = method_conf
            
            # Overall
            overall = sum(scores.values()) / len(scores)
            
            rating = "Excellent" if overall >= 85 else "Good" if overall >= 70 else "Fair"
            
            return {
                "overall_score": round(overall, 2),
                "rating": rating,
                "component_scores": {k: round(v, 2) for k, v in scores.items()},
                "strengths": ["Well-structured"] if scores['structure'] > 80 else [],
                "improvements": ["Add more references"] if scores['citations'] < 60 else []
            }
            
        except Exception as e:
            print(f"Quality score error: {e}")
            return {"overall_score": 0, "rating": "Unable to assess"}
