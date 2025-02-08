export class AuthManager {
  constructor() {
    this.currentUser = null;
    chrome.storage.local.get(['user'], (result) => {
      this.currentUser = result.user ? JSON.parse(result.user) : null;
    });
  }
  async login(provider = 'google') {
    switch(provider) {
      case 'google':
        return this.googleLogin();
      default:
        throw new Error('Unsupported provider');
    }
  }

  async logout() {
    await chrome.storage.local.remove(['user', 'accessToken']);
    this.currentUser = null
  }

  async getAccessToken() {
    const { accessToken } = await chrome.storage.local.get('accessToken');
    return accessToken;
  }
}

export const auth = new AuthManager();
