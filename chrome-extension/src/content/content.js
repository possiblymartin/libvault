document.addEventListener('mouseover', function(e) {
  const target = e.target.closest('[data-content-type]') || e.target;
  target.style.outline = '2px solid #3B82F6';
});

document.addEventListener('mouseout', function(e) {
  e.target.style.outline = '';
});

// Capture element content on click
document.addEventListener('click', async function(e) {
  e.preventDefault();
  const target = e.target.closest('[data-content-type]') || e.target;
  
  const contentData = {
    html: target.outerHTML,
    text: target.innerText,
    position: target.getBoundingClientRect().toJSON(),
    url: window.location.href,
    timestamp: new Date().toISOString()
  };

  // Send to background service worker
  chrome.runtime.sendMessage({
    type: 'CAPTURE_CONTENT',
    data: contentData
  });
});
