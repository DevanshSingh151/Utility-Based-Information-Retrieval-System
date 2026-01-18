import React, { useState } from 'react';
import './DocumentUpload.css';

/**
 * Document Upload Component
 * 
 * Provides a clean interface for users to upload documents.
 * Features drag-and-drop functionality (UI only for first review).
 * 
 * Supported file types: PDF, DOCX, TXT
 * 
 * Design:
 * - Column-style layout
 * - Large, clear upload area
 * - Visual feedback on drag-over
 * - Minimal borders and soft shadows
 */
function DocumentUpload() {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);

  // Handle drag and drop events (UI only - no actual upload)
  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    // UI only - simulate file handling
    const files = Array.from(e.dataTransfer.files);
    const validFiles = files.filter(file => {
      const extension = file.name.split('.').pop().toLowerCase();
      return ['pdf', 'docx', 'txt'].includes(extension);
    });

    if (validFiles.length > 0) {
      setUploadedFiles(prev => [...prev, ...validFiles.map(f => f.name)]);
    }
  };

  // Handle file input change
  const handleFileInput = (e) => {
    const files = Array.from(e.target.files);
    const validFiles = files.filter(file => {
      const extension = file.name.split('.').pop().toLowerCase();
      return ['pdf', 'docx', 'txt'].includes(extension);
    });

    if (validFiles.length > 0) {
      setUploadedFiles(prev => [...prev, ...validFiles.map(f => f.name)]);
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-content">
        {/* Section Title */}
        <h2 className="section-title">Upload Documents</h2>
        <p className="section-description">
          Upload your documents (PDF, DOCX, TXT) to build your searchable document collection
        </p>

        {/* Drag and Drop Area */}
        <div
          className={`upload-area ${isDragging ? 'dragging' : ''}`}
          onDragEnter={handleDragEnter}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="upload-icon">📁</div>
          <p className="upload-text">
            {isDragging ? 'Drop files here' : 'Drag and drop files here'}
          </p>
          <p className="upload-hint">or</p>
          
          {/* File Input Button */}
          <label htmlFor="file-input" className="upload-button">
            Browse Files
          </label>
          <input
            id="file-input"
            type="file"
            multiple
            accept=".pdf,.docx,.txt"
            onChange={handleFileInput}
            style={{ display: 'none' }}
          />
          
          <p className="upload-formats">Supported: PDF, DOCX, TXT</p>
        </div>

        {/* Uploaded Files List */}
        {uploadedFiles.length > 0 && (
          <div className="uploaded-files">
            <h3 className="files-title">Uploaded Files ({uploadedFiles.length})</h3>
            <ul className="files-list">
              {uploadedFiles.map((fileName, index) => (
                <li key={index} className="file-item">
                  <span className="file-icon">📄</span>
                  <span className="file-name">{fileName}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default DocumentUpload;
