import React, { useEffect } from 'react';
import './Navbar.css';

/**
 * Navigation Bar Component
 * 
 * Provides sticky navigation at the top of the page.
 * Highlights the active section based on scroll position.
 * Uses smooth scrolling to navigate between sections.
 * 
 * Features:
 * - Sticky positioning (stays at top while scrolling)
 * - Active section highlighting
 * - Smooth scroll navigation
 * - Responsive design
 */
function Navbar({ activeSection, setActiveSection }) {
  // Handle scroll to update active section
  useEffect(() => {
    const handleScroll = () => {
      const sections = ['home', 'upload', 'search', 'results'];
      const scrollPosition = window.scrollY + 100;

      for (let i = sections.length - 1; i >= 0; i--) {
        const section = document.getElementById(sections[i]);
        if (section && section.offsetTop <= scrollPosition) {
          setActiveSection(sections[i]);
          break;
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [setActiveSection]);

  // Handle navigation click - smooth scroll to section
  const handleNavClick = (sectionId) => {
    const section = document.getElementById(sectionId);
    if (section) {
      section.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setActiveSection(sectionId);
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        {/* Project name/logo on the left */}
        <div className="navbar-brand" onClick={() => handleNavClick('home')}>
          <span className="brand-text">Intelligent Retrieval</span>
        </div>

        {/* Navigation links on the right */}
        <ul className="navbar-menu">
          <li>
            <button
              className={`nav-link ${activeSection === 'home' ? 'active' : ''}`}
              onClick={() => handleNavClick('home')}
            >
              Home
            </button>
          </li>
          <li>
            <button
              className={`nav-link ${activeSection === 'upload' ? 'active' : ''}`}
              onClick={() => handleNavClick('upload')}
            >
              Upload
            </button>
          </li>
          <li>
            <button
              className={`nav-link ${activeSection === 'search' ? 'active' : ''}`}
              onClick={() => handleNavClick('search')}
            >
              Search
            </button>
          </li>
          <li>
            <button
              className={`nav-link ${activeSection === 'results' ? 'active' : ''}`}
              onClick={() => handleNavClick('results')}
            >
              Results
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
