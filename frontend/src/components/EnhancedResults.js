/**
 * Enhanced Results Display Component
 * Shows Summary, Readability, Quality Score
 */

import React from 'react';
import './EnhancedResults.css';

function EnhancedResults({ results }) {
  const {
    summary,
    readability_analysis,
    citations_analysis,
    research_questions,
    quality_score
  } = results;

  return (
    <div className="enhanced-results">
      {/* Quality Score Banner */}
      {quality_score && (
        <div className="quality-banner">
          <div className="quality-score-circle">
            <div className="score-value">{quality_score.overall_score}</div>
            <div className="score-label">Quality Score</div>
          </div>
          <div className="quality-details">
            <h3>📊 {quality_score.rating}</h3>
            <div className="component-scores">
              {Object.entries(quality_score.component_scores || {}).map(([key, value]) => (
                <div key={key} className="mini-score">
                  <span className="score-name">{key}</span>
                  <div className="mini-bar">
                    <div className="mini-fill" style={{ width: `${value}%` }}></div>
                  </div>
                  <span className="score-num">{value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* AI Summary Section */}
      {summary && summary.one_sentence !== "Summary generation failed" && (
        <div className="result-card summary-card">
          <h3>✨ AI-Generated Summary</h3>
          
          <div className="summary-section">
            <div className="summary-label">📌 TLDR (One Sentence)</div>
            <p className="summary-text">{summary.one_sentence}</p>
          </div>

          <div className="summary-section">
            <div className="summary-label">📄 Executive Summary</div>
            <p className="summary-text">{summary.executive_summary}</p>
          </div>

          {summary.key_findings && summary.key_findings[0] !== "Key findings not extracted" && (
            <div className="summary-section">
              <div className="summary-label">🔍 Key Findings</div>
              <ul className="findings-list">
                {summary.key_findings.map((finding, idx) => (
                  <li key={idx}>{finding}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Readability Analysis */}
      {readability_analysis && !readability_analysis.error && (
        <div className="result-card readability-card">
          <h3>📖 Readability Analysis</h3>
          
          <div className="readability-score-main">
            <div className="read-score-circle">
              {readability_analysis.flesch_reading_ease}
            </div>
            <div className="read-interpretation">
              <div className="read-label">{readability_analysis.interpretation}</div>
              <div className="read-level">Academic Level: {readability_analysis.academic_level}</div>
            </div>
          </div>

          <div className="readability-stats">
            <div className="read-stat">
              <span className="stat-label">Grade Level</span>
              <span className="stat-value">{readability_analysis.average_grade_level}</span>
            </div>
            <div className="read-stat">
              <span className="stat-label">Avg Sentence Length</span>
              <span className="stat-value">{readability_analysis.average_sentence_length} words</span>
            </div>
            <div className="read-stat">
              <span className="stat-label">Sentence Count</span>
              <span className="stat-value">{readability_analysis.sentence_count}</span>
            </div>
          </div>
        </div>
      )}

      {/* Citations Analysis */}
      {citations_analysis && citations_analysis.total_references > 0 && (
        <div className="result-card citations-card">
          <h3>📚 Citation Analysis</h3>
          
          <div className="citations-summary">
            <div className="citation-stat-box">
              <div className="stat-number">{citations_analysis.total_references}</div>
              <div className="stat-text">Total References</div>
            </div>
            <div className="citation-stat-box">
              <div className="stat-number">{citations_analysis.citation_style}</div>
              <div className="stat-text">Citation Style</div>
            </div>
          </div>

          {citations_analysis.top_authors && citations_analysis.top_authors.length > 0 && (
            <>
              <h4 className="subsection-title">Most Cited Authors</h4>
              <div className="authors-list">
                {citations_analysis.top_authors.slice(0, 5).map((author, idx) => (
                  <div key={idx} className="author-item">
                    <span className="author-name">{author.author}</span>
                    <span className="author-count">{author.count} citations</span>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      )}

      {/* Research Questions */}
      {research_questions && (
        <div className="result-card questions-card">
          <h3>❓ Research Questions & Objectives</h3>
          
          {research_questions.research_questions && 
           research_questions.research_questions[0] !== "Not explicitly stated" && (
            <div className="questions-section">
              <h4>Research Questions:</h4>
              <ul className="questions-list">
                {research_questions.research_questions.map((q, idx) => (
                  <li key={idx}>{q}</li>
                ))}
              </ul>
            </div>
          )}

          {research_questions.hypotheses && 
           research_questions.hypotheses[0] !== "Not explicitly stated" && (
            <div className="questions-section">
              <h4>Hypotheses:</h4>
              <ul className="questions-list">
                {research_questions.hypotheses.map((h, idx) => (
                  <li key={idx}>{h}</li>
                ))}
              </ul>
            </div>
          )}

          {research_questions.objectives && 
           research_questions.objectives[0] !== "Not explicitly stated" && (
            <div className="questions-section">
              <h4>Objectives:</h4>
              <ul className="questions-list">
                {research_questions.objectives.map((o, idx) => (
                  <li key={idx}>{o}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default EnhancedResults;
