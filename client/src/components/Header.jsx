import React, { useState, useEffect } from 'react';
import Dropdown from './Dropdown';

const Header = () => {
  const [hasScrolled, setHasScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 0) {
        setHasScrolled(true);
      } else {
        setHasScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [])

  return (
    <header className={`sticky bg-white px-4 py-2 w-full text-md flex items-center justify-between z-50 transition-border ${hasScrolled ? 'border-b border-gray-300' : ''}`}>
      {/* Left Section */}
      <div className="flex items-center space-x-8">
        <div className="text-xl font-bold text-gray-800">libvault</div>
        <nav className="flex items-center space-x-2">
          <Dropdown
            label="Features"
            items={[
              {label: 'Summarize Articles', href:'/'},
            ]}
          />
          <Dropdown
            label="Pricing"
            items={[
              {label: 'Free Plan', href:'/'},
              {label: 'Pro Plan', href:'/'},
            ]}
          />
          <a href="/about" className="text-gray-600 hover:bg-gray-100 rounded-md px-3 py-1">
            About Us
          </a>
        </nav>
      </div>
      {/* Right Section */}
      <div>
        <a
          href="/login"
          className="px-3 py-2 bg-black text-white rounded-md text-sm hover:bg-gray-800">
            Log In
          </a>
      </div>
    </header>
  );
};

export default Header;