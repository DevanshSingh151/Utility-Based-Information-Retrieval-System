import React, { useState } from 'react';
import './SearchSection.css';

/**
 * Search Section Component
 * 
 * Provides a clean, intuitive search interface.
 * Features a large, centered search bar with placeholder text.
 * 
 * Note: This is UI-only for the first review.
 * Later, this will connect to the backend API for actual search functionality.
 */
function SearchSection() {
  const [searchQuery, setSearchQuery] = useState('');

  // Handle search input change
  const handleInputChange = (e) => {
    setSearchQuery(e.target.value);
  };

  // Handle search button click (UI only)
  const handleSearch = (e) => {
    e.preventDefault();
    // UI only - no actual search functionality yet
    console.log('Search query:', searchQuery);
    // In future: This will trigger API call to backend
  };

  return (
    <div className="search-container">
      <div className="search-content">
        {/* Section Title */}
        <h2 className="section-title">Search Documents</h2>
        <p className="section-description">
          Enter your query in natural language to find relevant documents
        </p>

        {/* Search Form */}
        <form className="search-form" onSubmit={handleSearch}>
          <div className="search-wrapper">
            {/* Search Input */}
            <input
              type="text"
              className="search-input"
              placeholder="Search documents using natural language..."
              value={searchQuery}
              onChange={handleInputChange}
            />
            
            {/* Search Button */}
            <button type="submit" className="search-button">
              <span className="search-icon">🔍</span>
              <span className="search-button-text">Search</span>
            </button>
          </div>
        </form>

        {/* Search Tips */}
        <div className="search-tips">
          <p className="tips-title">Search Tips:</p>
          <ul className="tips-list">
            <li>Use natural language queries (e.g., "machine learning algorithms")</li>
            <li>Results are ranked by relevance using TF-IDF and BM25</li>
            <li>Try different phrasings for better results</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default SearchSection;
