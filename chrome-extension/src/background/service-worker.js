import { auth } from '../lib/auth/auth.js';

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'GET_USER') {
    sendResponse(auth.currentUser);
  }
})

async function processContent(content) {
  try {
    const response = await fetch('http://localhost:5001/api/analyze-content', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${await getAuthToken()}`
      },
      body: JSON.stringify({ content })
    });

    const data = await response.json();

    if (data.error) {
      chrome.notifications.create({
        type: 'basic',
        title: 'Analysis Error',
        message: data.error
      });
      return null;
    }

    return data;
  } catch (error) {
    console.error('Processing error:', error);
    return null;
  }
}

async function getAuthToken() {
  return new Promise(resolve => {
    chrome.storage.local.get(['jwtToken'], result => {
      resolve(result.jwtToken || '');
    });
  });
}