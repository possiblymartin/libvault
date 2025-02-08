import { googleLogin } from '../lib/auth/google.js';

document.addEventListener('DOMContentLoaded', () => {
  const loginButton = document.getElementById('login-btn');

  if (!loginButton) {
    console.error('Login button not found!');
    return; 
  }

  loginButton.addEventListener('click', async () => {
    try {
      const user = await googleLogin();
      console.log(`Logged in as ${user.email}`)
    } catch (error) {
      console.error('Login failed:', error);
    }
  });
});