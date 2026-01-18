import React from 'react';
import './Hero.css';

/**
 * Hero/Landing Section Component
 * 
 * This is the first section users see when they visit the application.
 * It introduces the project with a clean, professional design.
 * 
 * Features:
 * - Project title
 * - Descriptive subtitle explaining the AI/NLP approach
 * - Clean, centered layout
 * - Subtle visual elements
 */
function Hero() {
  return (
    <div className="hero-container">
      <div className="hero-content">
        {/* Main Title */}
        <h1 className="hero-title">
          Intelligent Utility-Based Information Retrieval
        </h1>
        
        {/* Subtitle with project details */}
        <p className="hero-subtitle">
          Using TF-IDF and BM25 Algorithms
        </p>
        
        {/* Description */}
        <p className="hero-description">
          An advanced document retrieval system powered by Natural Language Processing 
          and Information Retrieval techniques. Upload your documents and search through 
          them using intelligent ranking algorithms that understand context and relevance.
        </p>

        {/* Feature highlights */}
        <div className="hero-features">
          <div className="feature-item">
            <span className="feature-icon">📄</span>
            <span className="feature-text">Document Upload</span>
          </div>
          <div className="feature-item">
            <span className="feature-icon">🔍</span>
            <span className="feature-text">Natural Language Search</span>
          </div>
          <div className="feature-item">
            <span className="feature-icon">📊</span>
            <span className="feature-text">Ranked Results</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Hero;
