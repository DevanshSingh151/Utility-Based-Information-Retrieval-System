import React, { useState } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import DocumentUpload from './components/DocumentUpload';
import SearchSection from './components/SearchSection';
import ResultsPreview from './components/ResultsPreview';

/**
 * Main App Component
 * 
 * This is the root component that orchestrates all sections of the application.
 * It manages the overall layout and navigation between different sections.
 * 
 * For the first review, this is a single-page application with smooth scrolling
 * between sections. Later, this can be extended with React Router for multi-page navigation.
 */
function App() {
  // State to manage which section is currently active (for navigation highlighting)
  const [activeSection, setActiveSection] = useState('home');

  return (
    <div className="App">
      {/* Navigation bar - sticky at the top */}
      <Navbar activeSection={activeSection} setActiveSection={setActiveSection} />
      
      {/* Main content area with all sections */}
      <main className="main-content">
        {/* Landing/Hero Section */}
        <section id="home" className="section">
          <Hero />
        </section>

        {/* Document Upload Section */}
        <section id="upload" className="section">
          <DocumentUpload />
        </section>

        {/* Search Section */}
        <section id="search" className="section">
          <SearchSection />
        </section>

        {/* Results Preview Section */}
        <section id="results" className="section">
          <ResultsPreview />
        </section>
      </main>
    </div>
  );
}

export default App;
