// Enhanced JavaScript for Kolam Generator

// Global variables
let currentSVG = '';
let currentAnalysis = null;
let animationFrames = [];
let animationInterval = null;
let currentFrame = 0;
let isAnimating = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
    initializeThemeToggle();
    initializePatternSelector();
    initializeUpload();
    initializeAnimation();
    initializeExport();
});

// Tab Navigation
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            document.getElementById(`${targetTab}-tab`).classList.add('active');
        });
    });
}

// Theme Toggle
function initializeThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    
    themeToggle.addEventListener('click', () => {
        const currentTheme = body.getAttribute('data-theme');
        if (currentTheme === 'dark') {
            body.removeAttribute('data-theme');
            themeToggle.textContent = '🌙 Dark Mode';
        } else {
            body.setAttribute('data-theme', 'dark');
            themeToggle.textContent = '☀️ Light Mode';
        }
    });
}

// Pattern Selector
function initializePatternSelector() {
    const patternSelect = document.getElementById('pattern');
    const descriptionElement = document.getElementById('pattern-description');
    
    patternSelect.addEventListener('change', () => {
        const selectedPattern = patternSelect.value;
        fetch(`/pattern_info/${selectedPattern}`)
            .then(response => response.json())
            .then(data => {
                descriptionElement.textContent = data.description;
            })
            .catch(error => {
                console.error('Error fetching pattern info:', error);
            });
    });
}

// Upload Functionality
function initializeUpload() {
    const uploadArea = document.getElementById('upload-area');
    const imageUpload = document.getElementById('image-upload');
    const uploadResult = document.getElementById('upload-result');
    const detectedPattern = document.getElementById('detected-pattern');

    uploadArea.addEventListener('click', () => {
        imageUpload.click();
    });

    imageUpload.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const imageData = e.target.result;
                processImage(imageData);
            };
            reader.readAsDataURL(file);
        }
    });

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#ff4081';
        uploadArea.style.backgroundColor = '#fff5f5';
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#e0e0e0';
        uploadArea.style.backgroundColor = '#fafafa';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#e0e0e0';
        uploadArea.style.backgroundColor = '#fafafa';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const imageData = e.target.result;
                    processImage(imageData);
                };
                reader.readAsDataURL(file);
            }
        }
    });
}

function processImage(imageData) {
    const uploadResult = document.getElementById('upload-result');
    const detectedPattern = document.getElementById('detected-pattern');
    
    uploadResult.style.display = 'block';
    detectedPattern.innerHTML = '<div class="loading"></div> Processing image...';

    console.log('Processing image, data length:', imageData.length);
    console.log('Image data preview:', imageData.substring(0, 100) + '...');

    fetch('/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            image: imageData
        })
    })
    .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        if (data.success) {
            let suggestionsHtml = '';
            if (data.suggested_patterns && data.suggested_patterns.length > 0) {
                suggestionsHtml = `
                    <div class="pattern-suggestions">
                        <h5>Suggested Kolam Patterns:</h5>
                        <div class="suggestion-buttons">
                            ${data.suggested_patterns.map(pattern => 
                                `<button class="btn-secondary suggestion-btn" onclick="generateSuggestedPattern('${pattern}')">${pattern.charAt(0).toUpperCase() + pattern.slice(1)}</button>`
                            ).join('')}
                        </div>
                    </div>
                `;
            }
            
            detectedPattern.innerHTML = `
                <div class="success-message">
                    <h4>Pattern Detected Successfully!</h4>
                    <p>Dots found: ${data.dots ? data.dots.length : 0}</p>
                    <p>Pattern type: ${data.pattern_info ? data.pattern_info.type : 'unknown'}</p>
                    <p>Complexity: ${data.pattern_info ? data.pattern_info.complexity.toFixed(2) : '0.00'}</p>
                    <p>Symmetry: ${data.pattern_info && data.pattern_info.symmetry ? 
                        (data.pattern_info.symmetry.horizontal ? 'Horizontal ✅' : 'Horizontal ❌') + ' | ' +
                        (data.pattern_info.symmetry.vertical ? 'Vertical ✅' : 'Vertical ❌') + ' | ' +
                        (data.pattern_info.symmetry.radial ? 'Radial ✅' : 'Radial ❌') : 'Unknown'}</p>
                </div>
                <div class="detected-svg">${data.svg || 'No SVG generated'}</div>
                ${suggestionsHtml}
            `;
        } else {
            detectedPattern.innerHTML = `
                <div class="error-message">
                    <h4>Error Processing Image</h4>
                    <p>${data.error || 'Unknown error occurred'}</p>
                    ${data.details ? `<p><small>Details: ${data.details}</small></p>` : ''}
                </div>
            `;
        }
    })
    .catch(error => {
        console.error('Upload error:', error);
        detectedPattern.innerHTML = `
            <div class="error-message">
                <h4>Error Processing Image</h4>
                <p>Failed to process the uploaded image: ${error.message}</p>
                <p><small>Check the browser console for more details.</small></p>
            </div>
        `;
    });
}

// Animation Functionality
function initializeAnimation() {
    const speedSlider = document.getElementById('speed-slider');
    const speedValue = document.getElementById('speed-value');
    
    speedSlider.addEventListener('input', (e) => {
        speedValue.textContent = `${e.target.value}x`;
    });
}

function generateAnimation() {
    const pattern = document.getElementById('pattern').value;
    const gridSize = document.getElementById('grid-size').value;
    
    const animationDisplay = document.getElementById('animation-display');
    animationDisplay.innerHTML = '<div class="loading"></div> Generating animation...';

    fetch('/animate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            pattern: pattern,
            grid_size: parseInt(gridSize),
            frame_count: 30
        })
    })
    .then(response => response.json())
    .then(data => {
        animationFrames = data.frames;
        animationDisplay.innerHTML = data.animated_svg;
        
        // Enable animation controls
        document.getElementById('play-btn').disabled = false;
        document.getElementById('reset-btn').disabled = false;
    })
    .catch(error => {
        animationDisplay.innerHTML = `
            <div class="error-message">
                <h4>Error Generating Animation</h4>
                <p>Failed to generate animation frames.</p>
            </div>
        `;
    });
}

function playAnimation() {
    if (animationFrames.length === 0) return;
    
    isAnimating = true;
    document.getElementById('play-btn').disabled = true;
    document.getElementById('pause-btn').disabled = false;
    
    const speed = parseFloat(document.getElementById('speed-slider').value);
    const frameInterval = 100 / speed; // Base interval is 100ms
    
    animationInterval = setInterval(() => {
        const animationDisplay = document.getElementById('animation-display');
        animationDisplay.innerHTML = animationFrames[currentFrame];
        currentFrame = (currentFrame + 1) % animationFrames.length;
    }, frameInterval);
}

function pauseAnimation() {
    isAnimating = false;
    clearInterval(animationInterval);
    document.getElementById('play-btn').disabled = false;
    document.getElementById('pause-btn').disabled = true;
}

function resetAnimation() {
    pauseAnimation();
    currentFrame = 0;
    const animationDisplay = document.getElementById('animation-display');
    if (animationFrames.length > 0) {
        animationDisplay.innerHTML = animationFrames[0];
    }
}

// Export Functionality
function initializeExport() {
    // Export functionality is handled by the export functions below
}

function exportPattern(formatType) {
    // Clone the current SVG from the display
    let svgElement = document.querySelector('.kolam-display svg');
    if (!svgElement) {
        alert("No pattern to export!");
        return;
    }

    // Deep clone so we can modify without affecting the on-screen SVG
    let cleanSVG = svgElement.cloneNode(true);

    // Remove grid lines and dots by class name
    // cleanSVG.querySelectorAll('.grid, .dot').forEach(el => el.remove());
    cleanSVG.querySelectorAll('.grid, .dot, .helper, #gridLayer').forEach(el => el.remove());

    // Convert the cleaned SVG element back to a string
    let svgString = new XMLSerializer().serializeToString(cleanSVG);

    // Get current pattern parameters
    const gridSize = document.getElementById('grid-size').value;
    const pattern = document.getElementById('pattern').value;
    
    // Send the clean SVG to the backend
    fetch('/export', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            svg: svgString,
            format: formatType,
            filename: 'kolam',
            grid_size: parseInt(gridSize),
            pattern: pattern
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            if (formatType === 'all' && data.files) {
                data.files.forEach(file => downloadFile(file));
            } else {
                downloadFile(data.filepath);
            }
        } else {
            alert("Export failed: " + data.error);
        }
    })
    .catch(err => {
        console.error(err);
        alert("Export failed: " + err);
    });
}
function exportAllFormats() {
    exportPattern('all');
}

function downloadFile(filepath) {
    const filename = filepath.split('/').pop();
    window.open(`/download/${filename}`, '_blank');
}

function downloadFile(filepath) {
    const filename = filepath.split('/').pop();
    window.open(`/download/${filename}`, '_blank');
}

function showExportResults(files) {
    const exportResults = document.getElementById('export-results');
    const exportFiles = document.getElementById('export-files');
    
    exportResults.style.display = 'block';
    exportFiles.innerHTML = `
        <h5>Files exported successfully:</h5>
        <ul>
            ${Object.entries(files).map(([type, path]) => 
                `<li><strong>${type.toUpperCase()}:</strong> <a href="/download/${path.split('/').pop()}" target="_blank">Download</a></li>`
            ).join('')}
        </ul>
    `;
}

function generateQRCode() {
    if (!currentSVG) {
        alert('Please generate a pattern first.');
        return;
    }

    const patternData = {
        svg: currentSVG,
        analysis: currentAnalysis,
        timestamp: new Date().toISOString()
    };

    fetch('/qr_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            pattern_data: JSON.stringify(patternData)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            downloadFile(data.qr_path);
        } else {
            alert(`QR Code generation failed: ${data.error}`);
        }
    })
    .catch(error => {
        alert('QR Code generation failed. Please try again.');
    });
}

function sharePattern() {
    if (!currentSVG) {
        alert('Please generate a pattern first.');
        return;
    }

    const patternData = {
        svg: currentSVG,
        analysis: currentAnalysis,
        timestamp: new Date().toISOString()
    };

    fetch('/share', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            pattern_data: patternData
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Copy to clipboard
            navigator.clipboard.writeText(data.url).then(() => {
                alert('Shareable link copied to clipboard!');
            }).catch(() => {
                prompt('Shareable link:', data.url);
            });
        } else {
            alert(`Sharing failed: ${data.error}`);
        }
    })
    .catch(error => {
        alert('Sharing failed. Please try again.');
    });
}

// Analysis Functions
function showSymmetryInfo(symmetryType) {
    fetch(`/symmetry_info/${symmetryType}`)
        .then(response => response.json())
        .then(data => {
            const modal = document.getElementById('symmetry-modal');
            const modalTitle = document.getElementById('modal-title');
            const modalContent = document.getElementById('modal-content');
            
            modalTitle.textContent = `${symmetryType.charAt(0).toUpperCase() + symmetryType.slice(1)} Symmetry`;
            modalContent.textContent = data.explanation;
            modal.style.display = 'flex';
        })
        .catch(error => {
            console.error('Error fetching symmetry info:', error);
        });
}

// Modal Functions
document.addEventListener('click', (e) => {
    const modal = document.getElementById('symmetry-modal');
    if (e.target === modal || e.target.classList.contains('close')) {
        modal.style.display = 'none';
    }
});

// Utility Functions
function showMessage(message, type = 'success') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `${type}-message`;
    messageDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(messageDiv, container.firstChild);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Store current SVG and analysis when page loads
document.addEventListener('DOMContentLoaded', function() {
    const svgElement = document.querySelector('.kolam-display svg');
    if (svgElement) {
        currentSVG = svgElement.outerHTML;
    }
    
    // Store analysis data if available
    const analysisData = document.querySelector('[data-analysis]');
    if (analysisData) {
        currentAnalysis = JSON.parse(analysisData.getAttribute('data-analysis'));
    }
});

// Animation Functions
function animatePattern() {
    // Switch to animate tab and generate animation
    document.querySelector('[data-tab="animate"]').click();
    setTimeout(() => {
        generateAnimation();
    }, 100);
}

// Pattern Suggestion Functions
function generateSuggestedPattern(patternType) {
    // Switch to generate tab
    document.querySelector('[data-tab="generate"]').click();
    
    // Set the pattern type
    const patternSelect = document.getElementById('pattern');
    patternSelect.value = patternType;
    
    // Trigger pattern description update
    const event = new Event('change');
    patternSelect.dispatchEvent(event);
    
    // Generate the pattern
    setTimeout(() => {
        document.getElementById('kolam-form').submit();
    }, 100);
}

// Batch Export and Sharing Functions
function batchExport() {
    const patterns = [];
    const gridSize = document.getElementById('grid-size').value;
    
    // Generate multiple patterns
    const patternTypes = ['basic', 'diamond', 'spiral', 'flower', 'lotus', 'rose', 'star', 'sunburst', 'mandala', 'compass'];
    
    showLoadingMessage('Generating patterns for batch export...');
    
    // Generate patterns one by one
    let completed = 0;
    const totalPatterns = patternTypes.length;
    
    patternTypes.forEach((patternType, index) => {
        setTimeout(() => {
            fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `grid_size=${gridSize}&pattern=${patternType}&include_analysis=false`
            })
            .then(response => response.text())
            .then(html => {
                // Extract SVG from response
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const svgElement = doc.querySelector('.kolam-display svg');
                
                if (svgElement) {
                    const svgString = new XMLSerializer().serializeToString(svgElement);
                    patterns.push({
                        svg: svgString,
                        metadata: {
                            pattern_type: patternType,
                            grid_size: parseInt(gridSize),
                            timestamp: new Date().toISOString()
                        }
                    });
                }
                
                completed++;
                if (completed === totalPatterns) {
                    performBatchExport(patterns);
                }
            })
            .catch(error => {
                console.error('Error generating pattern:', error);
                completed++;
                if (completed === totalPatterns) {
                    performBatchExport(patterns);
                }
            });
        }, index * 500); // Stagger requests
    });
}

function performBatchExport(patterns) {
    if (patterns.length === 0) {
        showErrorMessage('No patterns generated for batch export');
        return;
    }
    
    showLoadingMessage(`Exporting ${patterns.length} patterns...`);
    
    fetch('/batch_export', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            patterns: patterns,
            include_qr: true,
            include_shareable_link: true
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Download ZIP file
            if (data.results.zip_archive) {
                downloadFile(data.results.zip_archive);
            }
            
            // Show shareable links
            if (data.results.shareable_links && data.results.shareable_links.length > 0) {
                showShareableLinks(data.results.shareable_links);
            }
            
            showSuccessMessage(`Batch export completed! ${patterns.length} patterns exported.`);
        } else {
            showErrorMessage(`Batch export failed: ${data.error}`);
        }
    })
    .catch(error => {
        showErrorMessage(`Batch export error: ${error.message}`);
    });
}

function showShareableLinks(links) {
    const linksHtml = links.map((link, index) => 
        `<div class="shareable-link">
            <strong>Pattern ${index + 1}:</strong> 
            <a href="${link}" target="_blank">${link}</a>
            <button onclick="copyToClipboard('${link}')" class="copy-btn">Copy</button>
        </div>`
    ).join('');
    
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <h3>Shareable Links</h3>
            <div class="shareable-links">
                ${linksHtml}
            </div>
            <button onclick="closeModal()" class="btn-primary">Close</button>
        </div>
    `;
    
    document.body.appendChild(modal);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showSuccessMessage('Link copied to clipboard!');
    }).catch(err => {
        showErrorMessage('Failed to copy link');
    });
}

function closeModal() {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.remove();
    }
}

function createShareableLink() {
    const svgElement = document.querySelector('.kolam-display svg');
    if (!svgElement) {
        alert('No pattern to share!');
        return;
    }
    
    const svgString = new XMLSerializer().serializeToString(svgElement);
    const gridSize = document.getElementById('grid-size').value;
    const pattern = document.getElementById('pattern').value;
    
    const patternData = {
        svg: svgString,
        metadata: {
            pattern_type: pattern,
            grid_size: parseInt(gridSize),
            timestamp: new Date().toISOString()
        }
    };
    
    showLoadingMessage('Creating shareable link...');
    
    fetch('/share', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pattern_data: patternData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showShareableLink(data.shareable_link);
        } else {
            showErrorMessage(`Failed to create shareable link: ${data.error}`);
        }
    })
    .catch(error => {
        showErrorMessage(`Error creating shareable link: ${error.message}`);
    });
}

function showShareableLink(link) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <h3>Shareable Link Created!</h3>
            <div class="shareable-link">
                <p>Share this link with others to view your Kolam pattern:</p>
                <input type="text" value="${link}" readonly class="link-input">
                <button onclick="copyToClipboard('${link}')" class="copy-btn">Copy Link</button>
            </div>
            <button onclick="closeModal()" class="btn-primary">Close</button>
        </div>
    `;
    
    document.body.appendChild(modal);
}
function updateCurrentSVG(svgContent, analysisData) {
    currentSVG = svgContent;
    currentAnalysis = analysisData || null;
}
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.querySelector('.export-toggle');
    const menu = document.querySelector('.export-menu');
    toggle.addEventListener('click', () => {
        menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
    });
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.export-dropdown')) {
            menu.style.display = 'none';
        }
    });
});

function renderKolam(svgClean, svgWithGrid, analysisData) {
    document.querySelector('.kolam-display').innerHTML = svgWithGrid;
    updateCurrentSVG(svgClean, analysisData);
}

function getCleanSVG() {
    let svgClone = document.querySelector('.kolam-display svg').cloneNode(true);
    // Remove grid elements by class or id
    svgClone.querySelectorAll('.grid, .dot').forEach(el => el.remove());
    return svgClone.outerHTML;
}

const cleanSVG = getCleanSVG();
fetch('/export', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ svg: cleanSVG, format: formatType, filename: 'kolam' })
});