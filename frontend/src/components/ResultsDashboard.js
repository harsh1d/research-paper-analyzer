/**
 * Results Dashboard Component
 * Displays comprehensive analysis results with PDF download
 */

import EnhancedResults from './EnhancedResults';


import React, { useState } from 'react';
import './ResultsDashboard.css';

function ResultsDashboard({ results, onReset }) {
  // State for PDF download
  const [downloading, setDownloading] = useState(false);

  // Destructure results data
  const {
    filename,
    file_info,
    statistics,
    topic_classification,
    section_analysis,
    methodology_classification,
    sentiment_analysis,
    keywords,
    named_entities,
    contribution_type,
  } = results;

const downloadPDF = async () => {
  setDownloading(true);
  
  try {
    console.log('🔄 Sending request to generate PDF...');
    
    const response = await fetch('http://localhost:8000/api/download-report', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(results),
    });

    console.log('📥 Response status:', response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('❌ Server error:', errorText);
      throw new Error(`Server returned ${response.status}: ${errorText}`);
    }

    // Get the blob
    const blob = await response.blob();
    console.log('📦 Blob size:', blob.size, 'bytes');
    
    if (blob.size === 0) {
      throw new Error('Generated PDF is empty');
    }
    
    // Create download link
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `analysis_report_${filename.replace(/\.[^/.]+$/, '')}.pdf`;
    document.body.appendChild(a);
    a.click();
    
    // Cleanup
    setTimeout(() => {
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    }, 100);
    
    console.log('✅ PDF downloaded successfully');
    alert('PDF report downloaded successfully!');
    
  } catch (error) {
    console.error('❌ PDF download error:', error);
    alert(`Failed to download PDF: ${error.message}`);
  } finally {
    setDownloading(false);
  }
};


  return (
    <div className="results-dashboard">
      {/* Header with Download Button */}
      <div className="results-header">
        <div>
          <h2>Analysis Results</h2>
          <p className="filename">{filename}</p>
        </div>
        <div className="header-buttons">
          <button 
            onClick={downloadPDF} 
            className="download-btn"
            disabled={downloading}
          >
            {downloading ? '⏳ Generating PDF...' : '📥 Download PDF Report'}
          </button>
          <button onClick={onReset} className="new-analysis-btn">
            New Analysis
          </button>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="stats-row">
        <div className="stat-card">
          <div className="stat-label">Word Count</div>
          <div className="stat-value">{statistics.word_count.toLocaleString()}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">File Size</div>
          <div className="stat-value">{file_info.size_kb} KB</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">File Type</div>
          <div className="stat-value">{file_info.type.toUpperCase()}</div>
        </div>
        {statistics.estimated_pages !== 'N/A' && (
          <div className="stat-card">
            <div className="stat-label">Pages</div>
            <div className="stat-value">{statistics.estimated_pages}</div>
          </div>
        )}
      </div>
<EnhancedResults results={results} />

      {/* Main Analysis Grid */}
      <div className="analysis-grid">
        <div className="analysis-grid">
        {/* Topic Classification */}
        <div className="result-card topic-card">
          <h3>🎯 Topic Classification</h3>
          <div className="topic-badge">{topic_classification.primary_topic}</div>
          <div className="confidence-bar">
            <div
              className="confidence-fill"
              style={{ width: `${topic_classification.confidence}%` }}
            />
          </div>
          <p className="confidence-text">
            Confidence: {topic_classification.confidence}%
          </p>

          <div className="secondary-topics">
            <h4>Related Topics:</h4>
            {topic_classification.secondary_topics.map((topic, idx) => (
              <div key={idx} className="secondary-topic">
                <span>{topic.topic}</span>
                <span className="topic-confidence">{topic.confidence}%</span>
              </div>
            ))}
          </div>
        </div>
        </div>

        {/* Contribution Type */}
        <div className="result-card">
          <h3>📝 Contribution Type</h3>
          <div className="contribution-type">
            {contribution_type.contribution_type}
          </div>
          <div className="confidence-bar">
            <div
              className="confidence-fill"
              style={{ width: `${contribution_type.confidence}%` }}
            />
          </div>
          <p className="confidence-text">
            Confidence: {contribution_type.confidence}%
          </p>
        </div>

        {/* Methodology Classification */}
        <div className="result-card">
          <h3>🔬 Methodology</h3>
          <div className="methodology-primary">
            {methodology_classification.primary_methodology}
          </div>
          <div className="confidence-bar">
            <div
              className="confidence-fill"
              style={{ width: `${methodology_classification.confidence}%` }}
            />
          </div>

          <div className="secondary-methods">
            {methodology_classification.secondary_methodologies.map(
              (method, idx) => (
                <div key={idx} className="method-item">
                  {method.method} ({method.confidence}%)
                </div>
              )
            )}
          </div>
        </div>

        {/* Sentiment Analysis */}
        <div className="result-card">
          <h3>💭 Tone & Sentiment</h3>
          <div className="sentiment-result">
            <div className="sentiment-label">{sentiment_analysis.sentiment}</div>
            <div className="academic-tone">{sentiment_analysis.academic_tone}</div>
          </div>
          <div className="confidence-bar">
            <div
              className="confidence-fill"
              style={{ width: `${sentiment_analysis.confidence}%` }}
            />
          </div>
          <p className="confidence-text">
            Confidence: {sentiment_analysis.confidence}%
          </p>
        </div>

        {/* Section Analysis */}
        <div className="result-card sections-card">
          <h3>📑 Document Sections</h3>
          <div className="sections-found">
            <p>
              Found {section_analysis.total_sections} of 7 standard sections
            </p>
          </div>
          <div className="sections-list">
            {section_analysis.sections_found.map((section, idx) => (
              <div key={idx} className="section-badge">
                ✓ {section}
              </div>
            ))}
          </div>
        </div>

        {/* Keywords */}
        <div className="result-card keywords-card">
          <h3>🔑 Key Terms & Phrases</h3>
          <div className="keywords-container">
            {keywords.slice(0, 12).map((kw, idx) => (
              <div key={idx} className="keyword-tag">
                <span className="keyword-text">{kw.keyword}</span>
                <span className="keyword-score">{kw.relevance_score}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Named Entities */}
        {Object.keys(named_entities).length > 0 && (
          <div className="result-card entities-card">
            <h3>🏷️ Named Entities</h3>
            <div className="entities-container">
              {Object.entries(named_entities).map(([type, entities]) => (
                <div key={type} className="entity-group">
                  <h4>{type}</h4>
                  <div className="entity-tags">
                    {entities.map((entity, idx) => (
                      <span key={idx} className="entity-tag">
                        {entity}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ResultsDashboard;
