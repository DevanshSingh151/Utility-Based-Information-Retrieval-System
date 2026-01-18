import React from 'react';
import './ResultsPreview.css';

/**
 * Results Preview Component
 * 
 * Displays search results in a card-based layout.
 * Shows document name, snippet preview, and relevance score.
 * 
 * Note: This component uses mock data for the first review.
 * Later, this will display actual search results from the backend API.
 * 
 * Design:
 * - Card-based layout (minimal design)
 * - Clear visual hierarchy
 * - Relevance scores displayed prominently
 * - Responsive grid layout
 */
function ResultsPreview() {
  // Mock data for demonstration (UI only)
  const mockResults = [
    {
      id: 1,
      documentName: 'Introduction to Machine Learning.pdf',
      snippet: 'Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data, identify patterns, and make decisions...',
      relevanceScore: 0.95,
      algorithm: 'TF-IDF'
    },
    {
      id: 2,
      documentName: 'Natural Language Processing Fundamentals.docx',
      snippet: 'Natural Language Processing (NLP) is a branch of artificial intelligence that helps computers understand, interpret, and manipulate human language. NLP combines computational linguistics with statistical, machine learning...',
      relevanceScore: 0.87,
      algorithm: 'BM25'
    },
    {
      id: 3,
      documentName: 'Information Retrieval Techniques.txt',
      snippet: 'Information retrieval is the process of obtaining information system resources that are relevant to an information need from a collection of those resources. Common techniques include vector space models, probabilistic models...',
      relevanceScore: 0.82,
      algorithm: 'TF-IDF'
    },
    {
      id: 4,
      documentName: 'Text Mining and Analysis.pdf',
      snippet: 'Text mining, also known as text data mining, is the process of deriving high-quality information from text. It involves the discovery of patterns and trends through means such as statistical pattern learning...',
      relevanceScore: 0.76,
      algorithm: 'BM25'
    },
    {
      id: 5,
      documentName: 'Search Algorithms Overview.docx',
      snippet: 'Search algorithms are fundamental to information retrieval systems. They help rank documents based on their relevance to user queries. Popular algorithms include TF-IDF, BM25, and vector space models...',
      relevanceScore: 0.71,
      algorithm: 'TF-IDF'
    }
  ];

  // Format relevance score as percentage
  const formatScore = (score) => {
    return (score * 100).toFixed(1);
  };

  return (
    <div className="results-container">
      <div className="results-content">
        {/* Section Title */}
        <h2 className="section-title">Search Results</h2>
        <p className="section-description">
          Documents ranked by relevance using TF-IDF and BM25 algorithms
        </p>

        {/* Results Count and Info */}
        <div className="results-header">
          <p className="results-count">
            Showing {mockResults.length} results
          </p>
          <p className="results-note">
            (Mock data for demonstration - UI only)
          </p>
        </div>

        {/* Results Grid */}
        <div className="results-grid">
          {mockResults.map((result) => (
            <div key={result.id} className="result-card">
              {/* Card Header with Score */}
              <div className="card-header">
                <div className="score-badge">
                  <span className="score-label">{result.algorithm}</span>
                  <span className="score-value">{formatScore(result.relevanceScore)}%</span>
                </div>
              </div>

              {/* Document Name */}
              <h3 className="document-name">{result.documentName}</h3>

              {/* Snippet Preview */}
              <p className="document-snippet">{result.snippet}</p>

              {/* Card Footer */}
              <div className="card-footer">
                <span className="rank-badge">Rank #{result.id}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Empty State (hidden when results exist) */}
        {mockResults.length === 0 && (
          <div className="empty-results">
            <p className="empty-text">No results found. Try a different search query.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ResultsPreview;
