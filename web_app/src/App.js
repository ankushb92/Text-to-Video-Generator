import React, { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [generatedVideos, setGeneratedVideos] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [processingHighRes, setProcessingHighRes] = useState(new Set());

  // Simulate video generation (replace with actual API call)
  const generateVideos = async () => {
    if (!prompt.trim()) return;
    
    setIsGenerating(true);
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Generate mock videos (replace with actual API response)
    const newVideos = Array.from({ length: 2 }, (_, index) => ({
      id: Date.now() + index,
      url: `https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4`,
      thumbnailUrl: `https://picsum.photos/400/300?random=${Date.now() + index}`,
      highResUrl: null,
      prompt: prompt,
      timestamp: new Date().toLocaleTimeString(),
      duration: '5s',
      resolution: '512x512'
    }));
    
    setGeneratedVideos(prev => [...newVideos, ...prev]);
    setIsGenerating(false);
    setPrompt('');
  };

  // Simulate high-res video generation (replace with actual API call)
  const generateHighRes = async (videoId) => {
    setProcessingHighRes(prev => new Set([...prev, videoId]));
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    // Update video with high-res version
    setGeneratedVideos(prev => 
      prev.map(video => 
        video.id === videoId 
          ? { 
              ...video, 
              highResUrl: `https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4`,
              resolution: '1024x1024'
            }
          : video
      )
    );
    
    setProcessingHighRes(prev => {
      const newSet = new Set(prev);
      newSet.delete(videoId);
      return newSet;
    });
  };

  return (
    <div className="App">
      <div className="App-header">
        <div className="hero-section">
          <h1 className="main-title">Text to Video Studio</h1>
          <p className="subtitle">Transform your words into stunning visual stories</p>
          <div className="title-glow"></div>
        </div>

        <div className="input-container">
          <div className="input-section">
            <label htmlFor="prompt" className="input-label">
              Describe your vision
            </label>
            <textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="A majestic dragon soaring through crystal caves with glowing crystals..."
              className="prompt-input"
              rows="4"
              disabled={isGenerating}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && e.ctrlKey) {
                  e.preventDefault();
                  generateVideos();
                }
              }}
            />
            <button
              onClick={generateVideos}
              disabled={isGenerating || !prompt.trim()}
              className={`generate-btn ${isGenerating ? 'generating' : ''}`}
            >
              {isGenerating ? (
                <div className="btn-content">
                  <div className="spinner"></div>
                  Crafting Magic...
                </div>
              ) : (
                <div className="btn-content">
                  <span className="btn-icon">🎬</span>
                  Generate Videos
                </div>
              )}
            </button>
          </div>
        </div>

        {generatedVideos.length > 0 && (
          <div className="videos-section">
            <h2 className="section-title">Your Creations</h2>
            
            <div className="videos-grid">
              {generatedVideos.map((video) => (
                <div key={video.id} className="video-card">
                  <div className="video-container">
                    <video
                      src={video.highResUrl || video.url}
                      controls
                      poster={video.thumbnailUrl}
                      className="video-player"
                      preload="metadata"
                    >
                      Your browser does not support the video tag.
                    </video>
                    <div className="video-overlay"></div>
                  </div>
                  
                  <div className="video-info">
                    <div className="prompt-display">
                      <p className="prompt-label">Prompt:</p>
                      <p className="prompt-text">{video.prompt}</p>
                    </div>
                    
                    <div className="video-meta">
                      <span className="meta-item">{video.timestamp}</span>
                      <span className="meta-separator">•</span>
                      <span className="meta-item">{video.duration}</span>
                      <span className="meta-separator">•</span>
                      <span className="meta-item">{video.resolution}</span>
                    </div>

                    <div className="video-actions">
                      <button
                        onClick={() => generateHighRes(video.id)}
                        disabled={processingHighRes.has(video.id) || video.highResUrl}
                        className={`action-btn enhance-btn ${
                          processingHighRes.has(video.id) ? 'processing' : ''
                        } ${video.highResUrl ? 'completed' : ''}`}
                      >
                        {processingHighRes.has(video.id) ? (
                          <div className="btn-content">
                            <div className="spinner small"></div>
                            Enhancing...
                          </div>
                        ) : video.highResUrl ? (
                          <div className="btn-content">
                            <span className="btn-icon">✨</span>
                            Enhanced
                          </div>
                        ) : (
                          <div className="btn-content">
                            <span className="btn-icon">🔥</span>
                            Enhance
                          </div>
                        )}
                      </button>
                      
                      <a
                        href={video.highResUrl || video.url}
                        download={`video-${video.id}.mp4`}
                        className="action-btn download-btn"
                      >
                        <span className="btn-icon">⬇️</span>
                        Download
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {generatedVideos.length === 0 && !isGenerating && (
          <div className="empty-state">
            <div className="empty-icon">🎭</div>
            <p className="empty-text">Ready to bring your imagination to life?</p>
            <p className="empty-subtext">Enter a prompt above to create your first video</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;