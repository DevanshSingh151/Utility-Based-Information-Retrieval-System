# Intelligent Utility-Based Information Retrieval System

## Project Overview

This is a frontend UI implementation for an **Artificial Intelligence semester project** focused on intelligent document retrieval using TF-IDF and BM25 algorithms.

The system provides a clean, professional interface for:
- Uploading documents (PDF, DOCX, TXT)
- Searching documents using natural language queries
- Viewing ranked search results

**Note:** This is the **first review version** - UI/UX only. No backend, database, or API integration yet.

## Tech Stack

- **React JS** (Functional Components)
- **HTML5**
- **CSS3** (Modern CSS with Flexbox/Grid)
- **No external UI libraries** (No Tailwind, Bootstrap, etc.)

## Project Structure

```
AI_web/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/         # React components
│   │   ├── Navbar.js      # Navigation bar
│   │   ├── Navbar.css
│   │   ├── Hero.js        # Landing/Hero section
│   │   ├── Hero.css
│   │   ├── DocumentUpload.js  # Document upload section
│   │   ├── DocumentUpload.css
│   │   ├── SearchSection.js   # Search interface
│   │   ├── SearchSection.css
│   │   ├── ResultsPreview.js  # Results display
│   │   └── ResultsPreview.css
│   ├── App.js             # Main app component
│   ├── App.css            # App styles
│   ├── index.js           # Entry point
│   └── index.css          # Global styles
├── package.json           # Dependencies
└── README.md             # This file
```

## Features

### 1. Landing Page (Hero Section)
- Clean project title and subtitle
- Brief description of the AI/NLP approach
- Feature highlights with icons

### 2. Document Upload Section
- Drag-and-drop upload area
- File browser button
- Support for PDF, DOCX, TXT files
- Visual feedback on drag-over
- Uploaded files list

### 3. Search Section
- Large, centered search bar
- Natural language query input
- Search button with icon
- Helpful search tips

### 4. Results Preview Section
- Card-based layout for results
- Document name, snippet preview
- Relevance score display (TF-IDF/BM25)
- Ranking indicators
- Mock data for demonstration

### 5. Navigation
- Sticky top navigation bar
- Smooth scroll between sections
- Active section highlighting
- Responsive design

## Installation & Setup

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Steps

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```

3. **Open your browser:**
   The app will automatically open at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

## Design Philosophy

- **Clean & Minimal:** Avoid clutter, focus on essential elements
- **Professional Academic Look:** Suitable for project reviews
- **Modern UI/UX:** Best practices for user experience
- **Responsive:** Works on desktop, tablet, and mobile
- **Subtle AI Theme:** Professional, not flashy

## Color Scheme

- **Primary:** Soft blue (#3498db)
- **Background:** Light grey (#f8f9fa)
- **Text:** Dark grey (#2c3e50)
- **Accents:** Subtle green/blue gradients
- **Cards:** White with soft shadows

## Code Quality

- Clean, well-commented code
- Meaningful component names
- Separate CSS files for each component
- Proper React functional components
- Ready for viva explanation

## Future Enhancements

This UI is designed to be easily extended with:
- MongoDB for document storage
- Flask API for backend processing
- Real TF-IDF and BM25 algorithm integration
- Actual document parsing and indexing
- Live search functionality

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Notes for Review

- All components are **UI-only** (no backend logic)
- Mock data is used in Results section
- File upload is simulated (no actual upload)
- Search button is functional but doesn't perform real search
- Code is well-commented for viva explanation

## Author

Semester Project - AI/ML Course

## License

Academic Project - For educational purposes only
