/**
 * Main App Component - Enhanced with Theme & Animations
 */

import React, { useState } from 'react';
import axios from 'axios';
import { FiUpload, FiFile, FiCheckCircle, FiLoader } from 'react-icons/fi';
import './App.css';
import ResultsDashboard from './components/ResultsDashboard';
import ThemeToggle from './components/ThemeToggle';
import { useTheme } from './context/ThemeContext';

const API_URL = 'http://localhost:8000';

function App() {
  const { isDarkMode } = useTheme();
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [showFeatures, setShowFeatures] = useState(true);

  // Drag and drop handlers
  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      validateAndSetFile(droppedFile);
    }
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      validateAndSetFile(selectedFile);
    }
  };

  const validateAndSetFile = (selectedFile) => {
    const allowedTypes = ['.pdf', '.docx', '.txt'];
    const fileExtension = '.' + selectedFile.name.split('.').pop().toLowerCase();

    if (!allowedTypes.includes(fileExtension)) {
      setError(`Invalid file type. Please upload PDF, DOCX, or TXT files.`);
      return;
    }

    const maxSize = 50 * 1024 * 1024; // 50MB
    if (selectedFile.size > maxSize) {
      setError('File too large. Maximum size is 50MB.');
      return;
    }

    setFile(selectedFile);
    setError(null);
    setResults(null);
    setShowFeatures(false);
  };

const analyzeDocument = async () => {
  if (!file) return;

  setLoading(true);
  setError(null);
  setUploadProgress(0);

  const formData = new FormData();
  formData.append('file', file);

  try {
    // Simulate smooth progress
    const progressInterval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return 90;
        }
        return prev + 10;
      });
    }, 300);

    const response = await axios.post(`${API_URL}/api/analyze`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });

    clearInterval(progressInterval);
    setUploadProgress(100);
    
    // Show processing time
    const processingTime = response.data.processing_time;
    console.log(`✅ Analysis completed in ${processingTime}s`);
    
    setResults(response.data);
    
  } catch (err) {
    console.error('Analysis error:', err);
    setError(
      err.response?.data?.detail || 'Analysis failed. Please try again.'
    );
  } finally {
    setLoading(false);
  }
};


  const resetApp = () => {
    setFile(null);
    setResults(null);
    setError(null);
    setUploadProgress(0);
    setShowFeatures(true);
  };

  return (
    <div className={`App ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      {/* Animated Background */}
      <div className="animated-background">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
        <div className="gradient-orb orb-3"></div>
      </div>

      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo-icon">📚</div>
            <div>
              <h1 className="gradient-text">Research Paper Analyzer</h1>
              <p className="tagline">AI-Powered Academic Intelligence</p>
            </div>
          </div>
          <div className="header-actions">
            <ThemeToggle />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container">
        {!results ? (
          <>
            {/* Upload Section */}
            <div className="upload-section glass-card">
              <div
                className={`drop-zone ${isDragging ? 'dragging' : ''} ${
                  file ? 'has-file' : ''
                }`}
                onDragEnter={handleDragEnter}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
              >
                {!file ? (
                  <>
                    <div className="upload-icon-container">
                      <FiUpload className="upload-icon pulse" />
                    </div>
                    <h3>Drag & Drop Your Research Paper</h3>
                    <p className="upload-subtitle">
                      or click to browse files
                    </p>
                    <div className="file-types">
                      <span className="file-type-badge">PDF</span>
                      <span className="file-type-badge">DOCX</span>
                      <span className="file-type-badge">TXT</span>
                    </div>
                    <p className="file-limit">Maximum size: 50MB</p>
                  </>
                ) : (
                  <>
                    <div className="file-preview">
                      <FiFile className="file-icon" />
                      <div className="file-info-box">
                        <h3>{file.name}</h3>
                        <p className="file-size">
                          {(file.size / 1024).toFixed(2)} KB
                        </p>
                      </div>
                    </div>
                  </>
                )}

                <input
                  type="file"
                  id="file-input"
                  accept=".pdf,.docx,.txt"
                  onChange={handleFileSelect}
                  style={{ display: 'none' }}
                />
                <label htmlFor="file-input" className="browse-btn glass-button">
                  {file ? 'Change File' : 'Browse Files'}
                </label>
              </div>

              {file && (
                <div className="action-buttons slide-up">
                  <button
                    onClick={analyzeDocument}
                    className="analyze-btn primary-button"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <FiLoader className="spin" />
                        <span>Analyzing... {uploadProgress}%</span>
                      </>
                    ) : (
                      <>
                        <FiCheckCircle />
                        <span>Analyze Document</span>
                      </>
                    )}
                  </button>
                  <button onClick={resetApp} className="reset-btn secondary-button">
                    Clear
                  </button>
                </div>
              )}

              {loading && (
                <div className="progress-container slide-up">
                  <div className="progress-bar">
                    <div 
                      className="progress-fill"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                  <div className="progress-steps">
                    <div className={`step ${uploadProgress >= 25 ? 'active' : ''}`}>
                      <div className="step-circle">1</div>
                      <span>Uploading</span>
                    </div>
                    <div className={`step ${uploadProgress >= 50 ? 'active' : ''}`}>
                      <div className="step-circle">2</div>
                      <span>Extracting</span>
                    </div>
                    <div className={`step ${uploadProgress >= 75 ? 'active' : ''}`}>
                      <div className="step-circle">3</div>
                      <span>Analyzing</span>
                    </div>
                    <div className={`step ${uploadProgress === 100 ? 'active' : ''}`}>
                      <div className="step-circle">4</div>
                      <span>Complete</span>
                    </div>
                  </div>
                </div>
              )}

              {error && (
                <div className="error-message slide-up">
                  <span className="error-icon">⚠️</span>
                  {error}
                </div>
              )}
            </div>

            {/* Features Section */}
            {showFeatures && (
              <div className="features-section fade-in">
                <h2 className="section-title gradient-text">Powerful Analysis Features</h2>
                <div className="features-grid">
                  <div className="feature-card glass-card hover-lift">
                    <div className="feature-icon-box">🎯</div>
                    <h3>Topic Classification</h3>
                    <p>AI identifies research domain with 90%+ accuracy</p>
                  </div>
                  <div className="feature-card glass-card hover-lift">
                    <div className="feature-icon-box">✨</div>
                    <h3>AI Summarization</h3>
                    <p>Generate TLDR and executive summaries instantly</p>
                  </div>
                  <div className="feature-card glass-card hover-lift">
                    <div className="feature-icon-box">📊</div>
                    <h3>Quality Score</h3>
                    <p>Comprehensive quality assessment with insights</p>
                  </div>
                  <div className="feature-card glass-card hover-lift">
                    <div className="feature-icon-box">📖</div>
                    <h3>Readability Analysis</h3>
                    <p>Flesch score and grade level evaluation</p>
                  </div>
                  <div className="feature-card glass-card hover-lift">
                    <div className="feature-icon-box">🔬</div>
                    <h3>Methodology Detection</h3>
                    <p>Classify research approach and methods</p>
                  </div>
                  <div className="feature-card glass-card hover-lift">
                    <div className="feature-icon-box">📚</div>
                    <h3>Citation Analysis</h3>
                    <p>Extract references and citation patterns</p>
                  </div>
                  <div className="feature-card glass-card hover-lift">
                    <div className="feature-icon-box">🔑</div>
                    <h3>Keyword Extraction</h3>
                    <p>Identify key terms and scientific concepts</p>
                  </div>
                  <div className="feature-card glass-card hover-lift">
                    <div className="feature-icon-box">📥</div>
                    <h3>PDF Reports</h3>
                    <p>Download professional analysis reports</p>
                  </div>
                </div>
              </div>
            )}
          </>
        ) : (
          <ResultsDashboard results={results} onReset={resetApp} />
        )}
      </div>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <p>Powered by Transformers, BERT, spaCy & FastAPI</p>
          <div className="footer-links">
            <a href="#about">About</a>
            <a href="#docs">Documentation</a>
            <a href="#api">API</a>
          </div>
        </div>
      </footer>

      {/* Floating Action Button for Quick Actions */}
      {results && (
        <button className="fab" onClick={resetApp} title="New Analysis">
          <span className="fab-icon">+</span>
        </button>
      )}
    </div>
  );
}

export default App;
