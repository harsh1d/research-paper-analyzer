"""
Enhanced Features Module
Adds summary generation, readability analysis, citation extraction, and more
"""

from transformers import pipeline
import re
from typing import Dict, Any, List
import textstat
from collections import Counter

class EnhancedFeatures:
    """
    Additional advanced features for research paper analysis
    """
    
    def __init__(self):
        """Initialize enhanced feature models"""
        print("Loading enhanced features...")
        
        # Summarization model
        try:
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1  # CPU
            )
        except Exception as e:
            print(f"Summarizer loading error: {e}")
            self.summarizer = None
        
        print("✓ Enhanced features loaded!")
    
    def generate_summary(self, text: str) -> Dict[str, Any]:
        """
        Generate multi-level summaries of the research paper
        
        Args:
            text: Full paper text
            
        Returns:
            Dictionary with different summary types
        """
        try:
            # Extract abstract if available
            abstract = self._extract_abstract(text)
            
            # Use abstract for summarization, or first 2000 words
            if abstract:
                source_text = abstract
            else:
                words = text.split()[:2000]
                source_text = ' '.join(words)
            
            # Clean text
            source_text = re.sub(r'\s+', ' ', source_text).strip()
            
            if len(source_text.split()) < 50:
                return {
                    "one_sentence": "Text too short for summarization",
                    "short_summary": "Text too short for summarization",
                    "executive_summary": "Text too short for summarization"
                }
            
            # Generate summaries of different lengths
            summaries = {}
            
            # One sentence summary (very short)
            if self.summarizer:
                try:
                    one_sent = self.summarizer(
                        source_text[:1024],
                        max_length=30,
                        min_length=15,
                        do_sample=False
                    )
                    summaries['one_sentence'] = one_sent[0]['summary_text']
                except:
                    summaries['one_sentence'] = self._extractive_summary(source_text, sentences=1)
            else:
                summaries['one_sentence'] = self._extractive_summary(source_text, sentences=1)
            
            # Short summary (3-4 sentences)
            if self.summarizer:
                try:
                    short = self.summarizer(
                        source_text[:1024],
                        max_length=100,
                        min_length=50,
                        do_sample=False
                    )
                    summaries['short_summary'] = short[0]['summary_text']
                except:
                    summaries['short_summary'] = self._extractive_summary(source_text, sentences=3)
            else:
                summaries['short_summary'] = self._extractive_summary(source_text, sentences=3)
            
            # Executive summary (paragraph)
            if self.summarizer:
                try:
                    exec_sum = self.summarizer(
                        source_text[:1024],
                        max_length=200,
                        min_length=100,
                        do_sample=False
                    )
                    summaries['executive_summary'] = exec_sum[0]['summary_text']
                except:
                    summaries['executive_summary'] = self._extractive_summary(source_text, sentences=5)
            else:
                summaries['executive_summary'] = self._extractive_summary(source_text, sentences=5)
            
            # Extract key findings
            summaries['key_findings'] = self._extract_key_findings(text)
            
            return summaries
            
        except Exception as e:
            print(f"Summary generation error: {e}")
            return {
                "one_sentence": "Summary generation failed",
                "short_summary": "Summary generation failed",
                "executive_summary": "Summary generation failed",
                "key_findings": []
            }
    
    def _extractive_summary(self, text: str, sentences: int = 3) -> str:
        """
        Simple extractive summarization fallback
        """
        # Split into sentences
        sents = re.split(r'[.!?]+', text)
        sents = [s.strip() for s in sents if len(s.strip()) > 20]
        
        # Return first N sentences
        return '. '.join(sents[:sentences]) + '.'
    
    def _extract_abstract(self, text: str) -> str:
        """Extract abstract section"""
        pattern = r"(?i)abstract[\s:]*(.{100,2000}?)(?=\n\n|\nintroduction|\nkeywords)"
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
        return ""
    
    def _extract_key_findings(self, text: str) -> List[str]:
        """Extract key findings from results/conclusion sections"""
        findings = []
        
        # Look for results section
        results_pattern = r"(?i)(results|findings|conclusion)[\s:]*(.{100,1500}?)(?=\n\n|discussion|references)"
        match = re.search(results_pattern, text)
        
        if match:
            results_text = match.group(2)
            # Split by common finding indicators
            sentences = re.split(r'[.!?]+', results_text)
            
            for sent in sentences:
                sent = sent.strip()
                # Look for findings indicators
                if any(keyword in sent.lower() for keyword in 
                       ['found', 'showed', 'demonstrated', 'revealed', 'indicated', 
                        'significant', 'suggests', 'evidence']):
                    if len(sent) > 30 and len(findings) < 5:
                        findings.append(sent + '.')
        
        return findings if findings else ["Key findings not extracted"]
    
    def analyze_readability(self, text: str) -> Dict[str, Any]:
        """
        Analyze text readability and complexity
        
        Args:
            text: Research paper text
            
        Returns:
            Readability metrics and scores
        """
        try:
            # Use first 5000 words for analysis
            sample = ' '.join(text.split()[:5000])
            
            # Calculate various readability scores
            flesch_reading = textstat.flesch_reading_ease(sample)
            flesch_kincaid = textstat.flesch_kincaid_grade(sample)
            smog = textstat.smog_index(sample)
            coleman_liau = textstat.coleman_liau_index(sample)
            automated_readability = textstat.automated_readability_index(sample)
            
            # Interpret Flesch Reading Ease
            if flesch_reading >= 90:
                interpretation = "Very Easy (5th grade)"
            elif flesch_reading >= 80:
                interpretation = "Easy (6th grade)"
            elif flesch_reading >= 70:
                interpretation = "Fairly Easy (7th grade)"
            elif flesch_reading >= 60:
                interpretation = "Standard (8th-9th grade)"
            elif flesch_reading >= 50:
                interpretation = "Fairly Difficult (10th-12th grade)"
            elif flesch_reading >= 30:
                interpretation = "Difficult (College)"
            else:
                interpretation = "Very Difficult (College Graduate)"
            
            # Academic level assessment
            avg_grade = (flesch_kincaid + smog + coleman_liau + automated_readability) / 4
            
            if avg_grade >= 16:
                academic_level = "Graduate/Professional"
            elif avg_grade >= 13:
                academic_level = "Undergraduate"
            elif avg_grade >= 9:
                academic_level = "High School"
            else:
                academic_level = "General Public"
            
            # Sentence and word statistics
            sentence_count = textstat.sentence_count(sample)
            word_count = textstat.lexicon_count(sample)
            avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
            
            # Syllable statistics
            syllable_count = textstat.syllable_count(sample)
            avg_syllables_per_word = syllable_count / word_count if word_count > 0 else 0
            
            return {
                "flesch_reading_ease": round(flesch_reading, 2),
                "flesch_kincaid_grade": round(flesch_kincaid, 2),
                "smog_index": round(smog, 2),
                "coleman_liau_index": round(coleman_liau, 2),
                "automated_readability_index": round(automated_readability, 2),
                "interpretation": interpretation,
                "academic_level": academic_level,
                "average_grade_level": round(avg_grade, 2),
                "sentence_count": sentence_count,
                "word_count": word_count,
                "average_sentence_length": round(avg_sentence_length, 2),
                "average_syllables_per_word": round(avg_syllables_per_word, 2)
            }
            
        except Exception as e:
            print(f"Readability analysis error: {e}")
            return {
                "error": "Readability analysis failed",
                "flesch_reading_ease": 0,
                "interpretation": "Analysis failed"
            }
    
    def extract_citations(self, text: str) -> Dict[str, Any]:
        """
        Extract citations and references from the paper
        
        Args:
            text: Research paper text
            
        Returns:
            Citation analysis results
        """
        try:
            # Find references section
            refs_pattern = r"(?i)(references|bibliography|works cited)[\s:]*(.+?)(?=\n\n\n|\Z)"
            match = re.search(refs_pattern, text, re.DOTALL)
            
            if not match:
                return {
                    "total_references": 0,
                    "references": [],
                    "citation_style": "Not detected",
                    "top_authors": []
                }
            
            references_text = match.group(2)
            
            # Split references by common patterns
            ref_list = re.split(r'\n(?=\[\d+\]|\d+\.|\w+,\s\w)', references_text)
            ref_list = [ref.strip() for ref in ref_list if len(ref.strip()) > 20]
            
            # Detect citation style
            citation_style = self._detect_citation_style(ref_list)
            
            # Extract author names
            authors = []
            for ref in ref_list[:50]:  # Analyze first 50 refs
                author_matches = re.findall(r'^([A-Z][a-z]+(?:,\s[A-Z]\.)?(?:\s[A-Z][a-z]+)?)', ref)
                if author_matches:
                    authors.append(author_matches[0])
            
            # Count author frequency
            author_freq = Counter(authors)
            top_authors = [{"author": author, "count": count} 
                          for author, count in author_freq.most_common(10)]
            
            # Extract years
            years = re.findall(r'\b(19\d{2}|20\d{2})\b', references_text)
            year_dist = Counter(years)
            
            return {
                "total_references": len(ref_list),
                "references": ref_list[:20],  # First 20 references
                "citation_style": citation_style,
                "top_authors": top_authors,
                "year_distribution": dict(year_dist.most_common(10)),
                "average_refs_per_section": round(len(ref_list) / 5, 2)  # Rough estimate
            }
            
        except Exception as e:
            print(f"Citation extraction error: {e}")
            return {
                "total_references": 0,
                "references": [],
                "citation_style": "Not detected",
                "top_authors": []
            }
    
    def _detect_citation_style(self, references: List[str]) -> str:
        """Detect citation style (APA, MLA, Chicago, IEEE)"""
        if not references:
            return "Unknown"
        
        sample = ' '.join(references[:5])
        
        # APA: Author, A. A. (Year). Title
        if re.search(r'\([12]\d{3}\)', sample):
            return "APA"
        
        # IEEE: [1] Author, "Title"
        if re.search(r'^\[\d+\]', sample):
            return "IEEE"
        
        # MLA: Author. "Title."
        if re.search(r'"\w+.*?"', sample):
            return "MLA"
        
        return "Unknown"
    
    def extract_research_questions(self, text: str) -> Dict[str, Any]:
        """
        Extract research questions and hypotheses
        
        Args:
            text: Research paper text
            
        Returns:
            Research questions and hypotheses
        """
        try:
            questions = []
            hypotheses = []
            
            # Look in introduction section
            intro_pattern = r"(?i)introduction[\s:]*(.{500,3000}?)(?=\n\n|method|literature)"
            intro_match = re.search(intro_pattern, text)
            
            search_text = intro_match.group(1) if intro_match else text[:3000]
            
            # Find research questions
            # Pattern 1: "research question is/are"
            rq_pattern1 = r"(?i)research question[s]?\s+(?:is|are)[\s:]+([^.?]+[?.])"
            questions.extend(re.findall(rq_pattern1, search_text))
            
            # Pattern 2: Direct questions
            direct_q = re.findall(r'([A-Z][^.!?]*\?)', search_text)
            questions.extend(direct_q[:3])
            
            # Find hypotheses
            hyp_pattern = r"(?i)(?:we hypothesize|hypothesis|hypothesized|we predict)[\s:]+([^.]+\.)"
            hypotheses.extend(re.findall(hyp_pattern, search_text))
            
            # Find objectives
            obj_pattern = r"(?i)(?:aim|objective|purpose|goal)[\s:]+(?:is|was|are|were)[\s:]+to\s+([^.]+\.)"
            objectives = re.findall(obj_pattern, search_text)
            
            return {
                "research_questions": questions[:5] if questions else ["Not explicitly stated"],
                "hypotheses": hypotheses[:5] if hypotheses else ["Not explicitly stated"],
                "objectives": objectives[:3] if objectives else ["Not explicitly stated"],
                "total_questions": len(questions),
                "total_hypotheses": len(hypotheses)
            }
            
        except Exception as e:
            print(f"Research question extraction error: {e}")
            return {
                "research_questions": ["Extraction failed"],
                "hypotheses": ["Extraction failed"],
                "objectives": ["Extraction failed"]
            }
    
    def calculate_quality_score(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall quality score based on various metrics
        
        Args:
            analysis_data: Complete analysis results
            
        Returns:
            Quality scores and assessment
        """
        try:
            scores = {}
            
            # Structure score (based on sections found)
            sections_found = len(analysis_data.get('section_analysis', {}).get('sections_found', []))
            structure_score = min((sections_found / 7) * 100, 100)
            scores['structure'] = round(structure_score, 2)
            
            # Clarity score (based on readability)
            readability = analysis_data.get('readability_analysis', {})
            flesch = readability.get('flesch_reading_ease', 50)
            # Academic papers should be moderately difficult (30-50 range is ideal)
            if 30 <= flesch <= 50:
                clarity_score = 100
            elif flesch < 30:
                clarity_score = 70 + (flesch / 30 * 30)
            else:
                clarity_score = 100 - ((flesch - 50) / 50 * 30)
            scores['clarity'] = round(max(0, clarity_score), 2)
            
            # Citation score (based on references)
            citations = analysis_data.get('citations_analysis', {})
            ref_count = citations.get('total_references', 0)
            # Ideal range: 20-60 references
            if 20 <= ref_count <= 60:
                citation_score = 100
            elif ref_count < 20:
                citation_score = (ref_count / 20) * 100
            else:
                citation_score = max(70, 100 - ((ref_count - 60) / 40 * 30))
            scores['citations'] = round(citation_score, 2)
            
            # Methodology score (based on confidence)
            methodology = analysis_data.get('methodology_classification', {})
            method_conf = methodology.get('confidence', 0)
            scores['methodology'] = round(method_conf, 2)
            
            # Overall quality score
            overall = (
                scores['structure'] * 0.25 +
                scores['clarity'] * 0.25 +
                scores['citations'] * 0.20 +
                scores['methodology'] * 0.30
            )
            
            # Quality rating
            if overall >= 85:
                rating = "Excellent"
            elif overall >= 70:
                rating = "Good"
            elif overall >= 55:
                rating = "Fair"
            else:
                rating = "Needs Improvement"
            
            return {
                "overall_score": round(overall, 2),
                "rating": rating,
                "component_scores": scores,
                "strengths": self._identify_strengths(scores),
                "improvements": self._identify_improvements(scores)
            }
            
        except Exception as e:
            print(f"Quality score calculation error: {e}")
            return {
                "overall_score": 0,
                "rating": "Unable to assess",
                "component_scores": {}
            }
    
    def _identify_strengths(self, scores: Dict[str, float]) -> List[str]:
        """Identify paper strengths"""
        strengths = []
        if scores.get('structure', 0) >= 80:
            strengths.append("Well-structured document with clear sections")
        if scores.get('clarity', 0) >= 75:
            strengths.append("Clear and readable writing style")
        if scores.get('citations', 0) >= 80:
            strengths.append("Comprehensive literature review")
        if scores.get('methodology', 0) >= 75:
            strengths.append("Clear and well-defined methodology")
        
        return strengths if strengths else ["Standard academic quality"]
    
    def _identify_improvements(self, scores: Dict[str, float]) -> List[str]:
        """Identify areas for improvement"""
        improvements = []
        if scores.get('structure', 0) < 60:
            improvements.append("Add missing standard sections (Abstract, Conclusion, etc.)")
        if scores.get('clarity', 0) < 60:
            improvements.append("Simplify complex sentences for better readability")
        if scores.get('citations', 0) < 60:
            improvements.append("Expand literature review with more references")
        if scores.get('methodology', 0) < 60:
            improvements.append("Provide more detailed methodology description")
        
        return improvements if improvements else ["Maintain current quality standards"]
