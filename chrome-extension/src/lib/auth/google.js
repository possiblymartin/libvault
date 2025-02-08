export async function googleLogin() {
  const redirectURL = chrome.identity.getRedirectURL();

  const authUrl = new URL('https://accounts.google.com//o/oauth2/v2/auth');
  authUrl.searchParams.set('client_id', '149698113919-rpd86d561bljla4g8mqq0h4mi1p876h4.apps.googleusercontent.com');
  authUrl.searchParams.set('redirect_uri', redirectURL);
  authUrl.searchParams.set('response_type', 'code');
  authUrl.searchParams.set('scope', 'email profile');


  try {
    const responseUrl = await chrome.identity.launchWebAuthFlow({
      url: authUrl.toString(),
      interactive: true
    });

    const params = new URLSearchParams(new URL(responseUrl).search);
    const code = params.get('code');

    const tokens = await fetch('https://localhost:5001/api/auth/google', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code })
    }).then(res => res.json());
    
    // Store access token and user info
    await chrome.storage.local.set({
      accessToken: tokens.access_token,
      user: JSON.stringify(tokens.user)
    });

    return tokens.user;
  } catch (error) {
    console.error('Google login failed:', error);
    throw error;
  } 
}