"""
PDF Report Generator - FIXED VERSION
Creates professional analysis reports in PDF format with all features
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.colors import HexColor
from datetime import datetime
from typing import Dict, Any
import os

class PDFReportGenerator:
    """
    Generates formatted PDF reports for research paper analysis
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=HexColor('#2d3748'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=HexColor('#667eea'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=HexColor('#4a5568'),
            spaceAfter=6,
            spaceBefore=6,
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=HexColor('#2d3748'),
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
        
        # Info box style
        self.styles.add(ParagraphStyle(
            name='InfoBox',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=HexColor('#2d3748'),
            spaceAfter=6,
            leftIndent=20,
            fontName='Helvetica'
        ))
    
    def _sanitize_text(self, text):
        """Remove problematic characters from text"""
        if text is None:
            return ""
        text = str(text)
        # Remove or replace problematic characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        # Limit length
        if len(text) > 500:
            text = text[:497] + "..."
        return text
    
    def generate_report(self, analysis_data: Dict[str, Any], output_path: str):
        """
        Generate PDF report from analysis data
        
        Args:
            analysis_data: Dictionary containing analysis results
            output_path: Path where PDF will be saved
        """
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Container for PDF elements
            elements = []
            
            # Add header
            elements.extend(self._create_header(analysis_data))
            
            # Add document information
            elements.extend(self._create_document_info(analysis_data))
            
            # Add quality score (NEW)
            elements.extend(self._create_quality_section(analysis_data))
            
            # Add summary (NEW)
            elements.extend(self._create_summary_section(analysis_data))
            
            # Add topic classification
            elements.extend(self._create_topic_section(analysis_data))
            
            # Add contribution type
            elements.extend(self._create_contribution_section(analysis_data))
            
            # Add methodology
            elements.extend(self._create_methodology_section(analysis_data))
            
            # Add sentiment analysis
            elements.extend(self._create_sentiment_section(analysis_data))
            
            # Add readability (NEW)
            elements.extend(self._create_readability_section(analysis_data))
            
            # Add sections found
            elements.extend(self._create_sections_analysis(analysis_data))
            
            # Add citations (NEW)
            elements.extend(self._create_citations_section(analysis_data))
            
            # Add keywords
            elements.extend(self._create_keywords_section(analysis_data))
            
            # Add named entities
            elements.extend(self._create_entities_section(analysis_data))
            
            # Add research questions (NEW)
            elements.extend(self._create_research_questions_section(analysis_data))
            
            # Add footer
            elements.extend(self._create_footer())
            
            # Build PDF
            doc.build(elements)
            
            print(f"✅ PDF generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ PDF generation error: {str(e)}")
            raise Exception(f"PDF generation failed: {str(e)}")
    
    def _create_header(self, data: Dict[str, Any]) -> list:
        """Create report header"""
        elements = []
        
        # Title
        title = Paragraph("Research Paper Analysis Report", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.2 * inch))
        
        # Subtitle with filename
        filename = self._sanitize_text(data.get('filename', 'Unknown Document'))
        subtitle = Paragraph(f"<b>Document:</b> {filename}", self.styles['CustomBody'])
        elements.append(subtitle)
        
        # Date
        date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        date_para = Paragraph(f"<b>Generated:</b> {date_str}", self.styles['CustomBody'])
        elements.append(date_para)
        
        elements.append(Spacer(1, 0.3 * inch))
        
        # Horizontal line
        elements.append(self._create_line())
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_document_info(self, data: Dict[str, Any]) -> list:
        """Create document statistics section"""
        elements = []
        
        heading = Paragraph("Document Statistics", self.styles['CustomHeading'])
        elements.append(heading)
        
        stats = data.get('statistics', {})
        file_info = data.get('file_info', {})
        
        # Create statistics table
        stats_data = [
            ['Metric', 'Value'],
            ['Word Count', f"{stats.get('word_count', 0):,}"],
            ['Character Count', f"{stats.get('character_count', 0):,}"],
            ['File Type', str(file_info.get('type', 'N/A')).upper()],
            ['File Size', f"{file_info.get('size_kb', 0)} KB"],
        ]
        
        # Add pages if available
        if stats.get('estimated_pages') != 'N/A':
            stats_data.append(['Pages', str(stats.get('estimated_pages', 'N/A'))])
        
        table = Table(stats_data, colWidths=[3 * inch, 3 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f7fafc')),
            ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2d3748')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3 * inch))
        
        return elements
    
    def _create_quality_section(self, data: Dict[str, Any]) -> list:
        """Create quality score section"""
        elements = []
        
        quality = data.get('quality_score', {})
        
        if quality and quality.get('overall_score', 0) > 0:
            heading = Paragraph("Quality Assessment", self.styles['CustomHeading'])
            elements.append(heading)
            
            # Overall score
            score = quality.get('overall_score', 0)
            rating = quality.get('rating', 'N/A')
            
            score_para = Paragraph(
                f"<b>Overall Quality Score:</b> {score}/100 ({rating})",
                self.styles['InfoBox']
            )
            elements.append(score_para)
            elements.append(Spacer(1, 0.1 * inch))
            
            # Component scores
            components = quality.get('component_scores', {})
            if components:
                sub_heading = Paragraph("Component Scores:", self.styles['CustomSubHeading'])
                elements.append(sub_heading)
                
                for component, comp_score in components.items():
                    comp_para = Paragraph(
                        f"• {str(component).title()}: {comp_score}/100",
                        self.styles['InfoBox']
                    )
                    elements.append(comp_para)
            
            # Strengths
            strengths = quality.get('strengths', [])
            if strengths:
                elements.append(Spacer(1, 0.1 * inch))
                strength_heading = Paragraph("Strengths:", self.styles['CustomSubHeading'])
                elements.append(strength_heading)
                
                for strength in strengths[:3]:
                    strength_text = self._sanitize_text(strength)
                    strength_para = Paragraph(f"✓ {strength_text}", self.styles['InfoBox'])
                    elements.append(strength_para)
            
            # Improvements
            improvements = quality.get('improvements', [])
            if improvements:
                elements.append(Spacer(1, 0.1 * inch))
                improve_heading = Paragraph("Suggestions:", self.styles['CustomSubHeading'])
                elements.append(improve_heading)
                
                for improvement in improvements[:3]:
                    improve_text = self._sanitize_text(improvement)
                    improve_para = Paragraph(f"→ {improve_text}", self.styles['InfoBox'])
                    elements.append(improve_para)
            
            elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_summary_section(self, data: Dict[str, Any]) -> list:
        """Create AI summary section"""
        elements = []
        
        summary = data.get('summary', {})
        
        if summary and summary.get('one_sentence', '').strip() and \
           'failed' not in summary.get('one_sentence', '').lower():
            
            heading = Paragraph("AI-Generated Summary", self.styles['CustomHeading'])
            elements.append(heading)
            
            # One sentence
            one_sent_text = self._sanitize_text(summary.get('one_sentence', ''))
            if one_sent_text:
                one_sent = Paragraph(
                    f"<b>TLDR:</b> {one_sent_text}",
                    self.styles['InfoBox']
                )
                elements.append(one_sent)
                elements.append(Spacer(1, 0.1 * inch))
            
            # Executive summary
            exec_text = self._sanitize_text(summary.get('executive_summary', ''))
            if exec_text and 'failed' not in exec_text.lower():
                exec_para = Paragraph(
                    f"<b>Executive Summary:</b> {exec_text}",
                    self.styles['InfoBox']
                )
                elements.append(exec_para)
            
            # Key findings
            findings = summary.get('key_findings', [])
            if findings and isinstance(findings, list) and \
               findings[0] != "Key findings not extracted":
                elements.append(Spacer(1, 0.1 * inch))
                sub_heading = Paragraph("Key Findings:", self.styles['CustomSubHeading'])
                elements.append(sub_heading)
                
                for finding in findings[:3]:
                    finding_text = self._sanitize_text(finding)
                    if finding_text:
                        finding_para = Paragraph(f"• {finding_text}", self.styles['InfoBox'])
                        elements.append(finding_para)
            
            elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_readability_section(self, data: Dict[str, Any]) -> list:
        """Create readability analysis section"""
        elements = []
        
        readability = data.get('readability_analysis', {})
        
        if readability and 'error' not in readability:
            heading = Paragraph("Readability Analysis", self.styles['CustomHeading'])
            elements.append(heading)
            
            # Readability table
            read_data = [
                ['Metric', 'Score', 'Interpretation'],
                [
                    'Flesch Reading Ease',
                    str(readability.get('flesch_reading_ease', 'N/A')),
                    str(readability.get('interpretation', 'N/A'))[:40]
                ],
                [
                    'Grade Level',
                    str(readability.get('average_grade_level', 'N/A')),
                    str(readability.get('academic_level', 'N/A'))
                ],
                [
                    'Avg Sentence Length',
                    str(readability.get('average_sentence_length', 'N/A')),
                    'Words per sentence'
                ]
            ]
            
            table = Table(read_data, colWidths=[2.5 * inch, 1.5 * inch, 2.5 * inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f7fafc')),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_citations_section(self, data: Dict[str, Any]) -> list:
        """Create citations analysis section"""
        elements = []
        
        citations = data.get('citations_analysis', {})
        
        if citations and citations.get('total_references', 0) > 0:
            heading = Paragraph("Citation Analysis", self.styles['CustomHeading'])
            elements.append(heading)
            
            total_para = Paragraph(
                f"<b>Total References:</b> {citations.get('total_references', 0)}",
                self.styles['InfoBox']
            )
            elements.append(total_para)
            
            style_para = Paragraph(
                f"<b>Citation Style:</b> {citations.get('citation_style', 'Unknown')}",
                self.styles['InfoBox']
            )
            elements.append(style_para)
            
            # Top cited authors
            top_authors = citations.get('top_authors', [])
            if top_authors and isinstance(top_authors, list):
                elements.append(Spacer(1, 0.1 * inch))
                sub_heading = Paragraph("Most Cited Authors:", self.styles['CustomSubHeading'])
                elements.append(sub_heading)
                
                for author_data in top_authors[:5]:
                    if isinstance(author_data, dict):
                        author_name = self._sanitize_text(author_data.get('author', ''))
                        author_count = author_data.get('count', 0)
                        author_para = Paragraph(
                            f"• {author_name} (cited {author_count} times)",
                            self.styles['InfoBox']
                        )
                        elements.append(author_para)
            
            elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_research_questions_section(self, data: Dict[str, Any]) -> list:
        """Create research questions section"""
        elements = []
        
        rq = data.get('research_questions', {})
        
        if rq and isinstance(rq, dict):
            questions = rq.get('research_questions', [])
            hypotheses = rq.get('hypotheses', [])
            
            if (questions and questions[0] != "Not explicitly stated") or \
               (hypotheses and hypotheses[0] != "Not explicitly stated"):
                
                heading = Paragraph("Research Questions & Hypotheses", self.styles['CustomHeading'])
                elements.append(heading)
                
                # Research questions
                if questions and questions[0] != "Not explicitly stated":
                    sub_heading = Paragraph("Research Questions:", self.styles['CustomSubHeading'])
                    elements.append(sub_heading)
                    
                    for q in questions[:3]:
                        q_text = self._sanitize_text(q)
                        if q_text:
                            q_para = Paragraph(f"• {q_text}", self.styles['InfoBox'])
                            elements.append(q_para)
                
                # Hypotheses
                if hypotheses and hypotheses[0] != "Not explicitly stated":
                    elements.append(Spacer(1, 0.1 * inch))
                    sub_heading = Paragraph("Hypotheses:", self.styles['CustomSubHeading'])
                    elements.append(sub_heading)
                    
                    for h in hypotheses[:3]:
                        h_text = self._sanitize_text(h)
                        if h_text:
                            h_para = Paragraph(f"• {h_text}", self.styles['InfoBox'])
                            elements.append(h_para)
                
                elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_topic_section(self, data: Dict[str, Any]) -> list:
        """Create topic classification section"""
        elements = []
        
        heading = Paragraph("Topic Classification", self.styles['CustomHeading'])
        elements.append(heading)
        
        topic_data = data.get('topic_classification', {})
        
        # Primary topic
        primary = Paragraph(
            f"<b>Primary Topic:</b> {topic_data.get('primary_topic', 'N/A')}", 
            self.styles['InfoBox']
        )
        elements.append(primary)
        
        # Confidence
        confidence = Paragraph(
            f"<b>Confidence:</b> {topic_data.get('confidence', 0):.2f}%", 
            self.styles['InfoBox']
        )
        elements.append(confidence)
        
        # Secondary topics
        secondary_topics = topic_data.get('secondary_topics', [])
        if secondary_topics:
            elements.append(Spacer(1, 0.1 * inch))
            sub_heading = Paragraph("Related Topics:", self.styles['CustomSubHeading'])
            elements.append(sub_heading)
            
            for topic in secondary_topics[:3]:
                topic_para = Paragraph(
                    f"• {topic.get('topic', 'N/A')} ({topic.get('confidence', 0):.2f}%)",
                    self.styles['InfoBox']
                )
                elements.append(topic_para)
        
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_contribution_section(self, data: Dict[str, Any]) -> list:
        """Create contribution type section"""
        elements = []
        
        heading = Paragraph("Research Contribution Type", self.styles['CustomHeading'])
        elements.append(heading)
        
        contribution = data.get('contribution_type', {})
        
        contrib_para = Paragraph(
            f"<b>Type:</b> {contribution.get('contribution_type', 'N/A')}",
            self.styles['InfoBox']
        )
        elements.append(contrib_para)
        
        confidence_para = Paragraph(
            f"<b>Confidence:</b> {contribution.get('confidence', 0):.2f}%",
            self.styles['InfoBox']
        )
        elements.append(confidence_para)
        
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_methodology_section(self, data: Dict[str, Any]) -> list:
        """Create methodology section"""
        elements = []
        
        heading = Paragraph("Research Methodology", self.styles['CustomHeading'])
        elements.append(heading)
        
        methodology = data.get('methodology_classification', {})
        
        # Primary methodology
        primary = Paragraph(
            f"<b>Primary Method:</b> {methodology.get('primary_methodology', 'N/A')}",
            self.styles['InfoBox']
        )
        elements.append(primary)
        
        confidence = Paragraph(
            f"<b>Confidence:</b> {methodology.get('confidence', 0):.2f}%",
            self.styles['InfoBox']
        )
        elements.append(confidence)
        
        # Secondary methods
        secondary = methodology.get('secondary_methodologies', [])
        if secondary:
            elements.append(Spacer(1, 0.1 * inch))
            sub_heading = Paragraph("Additional Methods:", self.styles['CustomSubHeading'])
            elements.append(sub_heading)
            
            for method in secondary:
                method_para = Paragraph(
                    f"• {method.get('method', 'N/A')} ({method.get('confidence', 0):.2f}%)",
                    self.styles['InfoBox']
                )
                elements.append(method_para)
        
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_sentiment_section(self, data: Dict[str, Any]) -> list:
        """Create sentiment analysis section"""
        elements = []
        
        heading = Paragraph("Tone & Sentiment Analysis", self.styles['CustomHeading'])
        elements.append(heading)
        
        sentiment = data.get('sentiment_analysis', {})
        
        sentiment_para = Paragraph(
            f"<b>Sentiment:</b> {sentiment.get('sentiment', 'N/A')}",
            self.styles['InfoBox']
        )
        elements.append(sentiment_para)
        
        tone_para = Paragraph(
            f"<b>Academic Tone:</b> {sentiment.get('academic_tone', 'N/A')}",
            self.styles['InfoBox']
        )
        elements.append(tone_para)
        
        confidence_para = Paragraph(
            f"<b>Confidence:</b> {sentiment.get('confidence', 0):.2f}%",
            self.styles['InfoBox']
        )
        elements.append(confidence_para)
        
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_sections_analysis(self, data: Dict[str, Any]) -> list:
        """Create sections detection section"""
        elements = []
        
        heading = Paragraph("Document Structure", self.styles['CustomHeading'])
        elements.append(heading)
        
        sections = data.get('section_analysis', {})
        sections_found = sections.get('sections_found', [])
        
        total_para = Paragraph(
            f"<b>Sections Detected:</b> {sections.get('total_sections', 0)} of 7 standard sections",
            self.styles['InfoBox']
        )
        elements.append(total_para)
        
        if sections_found:
            elements.append(Spacer(1, 0.1 * inch))
            
            # Create sections list
            sections_text = ", ".join([s.title() for s in sections_found])
            sections_para = Paragraph(
                f"<b>Found:</b> {sections_text}",
                self.styles['InfoBox']
            )
            elements.append(sections_para)
        
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_keywords_section(self, data: Dict[str, Any]) -> list:
        """Create keywords section"""
        elements = []
        
        heading = Paragraph("Key Terms & Concepts", self.styles['CustomHeading'])
        elements.append(heading)
        
        keywords = data.get('keywords', [])
        
        if keywords:
            # Create keywords table
            keywords_data = [['Keyword', 'Relevance Score']]
            
            for kw in keywords[:15]:
                kw_text = self._sanitize_text(kw.get('keyword', ''))[:50]
                keywords_data.append([
                    kw_text,
                    f"{kw.get('relevance_score', 0):.2f}%"
                ])
            
            table = Table(keywords_data, colWidths=[4 * inch, 2 * inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f7fafc')),
                ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2d3748')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            elements.append(table)
        else:
            no_keywords = Paragraph("No keywords extracted.", self.styles['InfoBox'])
            elements.append(no_keywords)
        
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_entities_section(self, data: Dict[str, Any]) -> list:
        """Create named entities section"""
        elements = []
        
        entities = data.get('named_entities', {})
        
        if entities:
            heading = Paragraph("Named Entities", self.styles['CustomHeading'])
            elements.append(heading)
            
            for entity_type, entity_list in entities.items():
                if entity_list:
                    entities_text = ', '.join([self._sanitize_text(e)[:30] for e in entity_list[:5]])
                    type_para = Paragraph(
                        f"<b>{entity_type}:</b> {entities_text}",
                        self.styles['InfoBox']
                    )
                    elements.append(type_para)
            
            elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_footer(self) -> list:
        """Create report footer"""
        elements = []
        
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(self._create_line())
        elements.append(Spacer(1, 0.1 * inch))
        
        footer_text = Paragraph(
            "<i>This report was generated by Research Paper Analyzer - AI-Powered Academic Document Intelligence System</i>",
            self.styles['CustomBody']
        )
        elements.append(footer_text)
        
        tech_stack = Paragraph(
            "<i>Powered by: FastAPI, Transformers (BERT), spaCy, YAKE, ReportLab</i>",
            self.styles['CustomBody']
        )
        elements.append(tech_stack)
        
        return elements
    
    def _create_line(self):
        """Create horizontal line separator"""
        line_style = ParagraphStyle(
            'line',
            parent=self.styles['Normal'],
            textColor=HexColor('#e2e8f0'),
        )
        return Paragraph('<para borderWidth=1 borderColor="#e2e8f0"></para>', line_style)
