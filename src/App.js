import React, { useState } from 'react';
import './App.css';
import { Document, Page, pdfjs } from 'react-pdf';

// Set up PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.js';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState('');
  const [rawLatex, setRawLatex] = useState('');
  const [pdfUrl, setPdfUrl] = useState(null);
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [downloadFile, setDownloadFile] = useState(null);
  const [downloadFileName, setDownloadFileName] = useState('');
  const [pdfDownloadUrl, setPdfDownloadUrl] = useState(null);
  const [pdfDownloadFileName, setPdfDownloadFileName] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [showWarningPopup, setShowWarningPopup] = useState(false);
  const [warningMessage, setWarningMessage] = useState('');
  
  // Backend API URL
  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  // PDF handling functions
  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
    setPageNumber(1);
  };

  const onDocumentLoadError = (error) => {
    console.error('Error loading PDF:', error);
    setWarningMessage('Error loading PDF document');
    setShowWarningPopup(true);
    setTimeout(() => setShowWarningPopup(false), 5000);
  };

  // Function to call backend API for conversion and compilation
  const convertAndCompile = async (textContent) => {
    try {
      const response = await fetch(`${API_BASE_URL}/convert`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: textContent
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Backend API error:', error);
      throw error;
    }
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setFileContent(''); // Clear content when new file is selected
      setRawLatex(''); // Clear LaTeX content
      setPdfUrl(null); // Clear PDF URL
      setNumPages(null); // Clear PDF pages
      setPageNumber(1); // Reset page number
      setDownloadFile(null); // Clear download file when new file is selected
      setDownloadFileName('');
      setPdfDownloadUrl(null); // Clear PDF download URL
      setPdfDownloadFileName(''); // Clear PDF download filename
      
      // Read and display file content immediately
      const reader = new FileReader();
      reader.onload = (e) => {
        setFileContent(e.target.result);
      };
      reader.readAsText(file);
    }
  };

  const handleTextChange = (event) => {
    setFileContent(event.target.value);
  };

  const handleUpload = async () => {
    if (!fileContent) {
      setFileContent('Please enter or select file content first');
      return;
    }

    setIsProcessing(true);
      setRawLatex('');
      setPdfUrl(null);
      setNumPages(null);
      setPageNumber(1);
      setPdfDownloadUrl(null);
      setPdfDownloadFileName('');
      setShowWarningPopup(false);
    
    try {
      // Call backend API for conversion and compilation
      const result = await convertAndCompile(fileContent);
      
      // Create a new Blob with the LaTeX content
      const blob = new Blob([result.latex_content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      
      // Generate filename for download
      const originalName = selectedFile?.name || 'output';
      const nameWithoutExt = originalName.replace(/\.[^/.]+$/, '');
      const newFileName = `${nameWithoutExt}.tex`;
      
      setDownloadFile(url);
      setDownloadFileName(newFileName);
      setRawLatex(result.latex_content);
      
      if (result.compilation.success) {
        // Compilation successful, show PDF
        if (result.pdf_url) {
          setPdfUrl(`${API_BASE_URL}${result.pdf_url}`);
          // Set PDF download URL and filename
          setPdfDownloadUrl(`${API_BASE_URL}${result.pdf_url}`);
          const originalName = selectedFile?.name || 'output';
          const nameWithoutExt = originalName.replace(/\.[^/.]+$/, '');
          setPdfDownloadFileName(`${nameWithoutExt}.pdf`);
        }
      } else {
        // Compilation failed, show raw LaTeX and warning popup
        setPdfUrl(null);
        setWarningMessage(`LaTeX compilation failed: ${result.compilation.error}`);
        setShowWarningPopup(true);
        
        // Auto-hide popup after 5 seconds
        setTimeout(() => {
          setShowWarningPopup(false);
        }, 5000);
      }
    } catch (error) {
      console.error('Error processing file:', error);
      setFileContent(`Error processing file: ${error.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownload = () => {
    if (downloadFile) {
      const link = document.createElement('a');
      link.href = downloadFile;
      link.download = downloadFileName;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const handlePdfDownload = () => {
    if (pdfDownloadUrl) {
      const link = document.createElement('a');
      link.href = pdfDownloadUrl;
      link.download = pdfDownloadFileName;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <div className="App">
      <div className="app-header">
        <h1>LaTeX Converter AI</h1>
      </div>
      <div className="app-container">
        {/* Left Sidebar */}
        <div className="sidebar">
          <div className="sidebar-content">
            <div className="file-input-container">
              <input
                type="file"
                id="file-upload"
                accept=".txt,.md"
                onChange={handleFileSelect}
                style={{ display: 'none' }}
              />
              <label htmlFor="file-upload" className="file-upload-button">
                📁 Choose Text File
              </label>
            </div>
            
            {selectedFile && (
              <div className="file-info">
                <h3>Selected File</h3>
                <p><strong>Name:</strong> {selectedFile.name}</p>
                <p><strong>Size:</strong> {(selectedFile.size / 1024).toFixed(2)} KB</p>
              </div>
            )}
            
            <button 
              className="convert-button"
              onClick={handleUpload}
              disabled={!fileContent || isProcessing}
            >
              {isProcessing ? '⏳ Processing...' : '🔄 Convert to LaTeX'}
            </button>
            
            {downloadFile && (
              <button 
                className="download-button"
                onClick={handleDownload}
              >
                💾 Download LaTeX File
              </button>
            )}
            
            {pdfDownloadUrl && (
              <button 
                className="download-button"
                onClick={handlePdfDownload}
              >
                💾 Download PDF File
              </button>
            )}
          </div>
        </div>

        {/* Right Text Viewer */}
        <div className="text-viewer">
          <div className="viewer-content">
            {isProcessing ? (
              <div className="loading-container">
                <div className="loading-spinner"></div>
                <div className="loading-text">Converting to LaTeX<span className="loading-dots">...</span></div>
                <div className="loading-subtext">
                  AI is analyzing your text and generating LaTeX code.<br />
                  This may take a few moments.
                </div>
              </div>
            ) : rawLatex ? (
              <div className="latex-split-view">
                <div className="latex-section">
                  <textarea 
                    className="text-content"
                    value={fileContent}
                    onChange={handleTextChange}
                    placeholder="Enter text or upload a file to convert to LaTeX..."
                  />
                </div>
                <div className="latex-output">
                  {pdfUrl ? (
                    <div className="pdf-viewer">
                      <div className="pdf-controls">
                        <button 
                          onClick={() => setPageNumber(Math.max(1, pageNumber - 1))}
                          disabled={pageNumber <= 1}
                        >
                          Previous
                        </button>
                        <span>
                          Page {pageNumber} of {numPages}
                        </span>
                        <button 
                          onClick={() => setPageNumber(Math.min(numPages, pageNumber + 1))}
                          disabled={pageNumber >= numPages}
                        >
                          Next
                        </button>
                      </div>
                      <Document
                        file={pdfUrl}
                        onLoadSuccess={onDocumentLoadSuccess}
                        onLoadError={onDocumentLoadError}
                        className="pdf-document"
                      >
                        <Page 
                          pageNumber={pageNumber} 
                          className="pdf-page"
                          renderTextLayer={true}
                          renderAnnotationLayer={true}
                        />
                      </Document>
                    </div>
                  ) : (
                    <pre>{rawLatex}</pre>
                  )}
                </div>
              </div>
            ) : (
              <textarea 
                className="text-content"
                value={fileContent}
                onChange={handleTextChange}
                placeholder="Enter text or upload a file to convert to LaTeX..."
                rows={30}
              />
            )}
          </div>
        </div>
      </div>
      
      {/* Warning Popup */}
      {showWarningPopup && (
        <div className="warning-popup">
          <div className="popup-content warning">
            <div className="popup-icon">
              ⚠️
            </div>
            <div className="popup-message">
              {warningMessage}
            </div>
            <button 
              className="popup-close"
              onClick={() => setShowWarningPopup(false)}
            >
              ×
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
