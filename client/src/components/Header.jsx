import React, { useState, useEffect } from 'react';
import Dropdown from './Dropdown';
import Login from '../pages/Login'

const Header = () => {
  return (
    <header className="px-6 py-4 w-full text-md flex items-center justify-between">
      {/* Left Section */}
      <div className="flex items-center space-x-8">
        <div className="text-xl font-medium text-gray-300"><a href="/">libvault</a></div>
      </div>
      {/* Right Section */}
      <div className="space-x-2">
        <a
          href="/login"
          className="px-4 py-3 bg-gray-300 text-gray-900 grayscale rounded-full text-sm hover:opacity-95">
            Log In
          </a>
        <a
          href="/register" 
          className="px-4 py-3 bg-gray-900 grayscale border-1 border-gray-700 text-gray-300 rounded-full text-sm hover:bg-gray-800">
            Sign Up
          </a>
        
      </div>
    </header>
  );
};

export default Header;