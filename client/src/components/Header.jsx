import React from 'react';
import Dropdown from './Dropdown';

const Header = () => {
  return (
    <header className="bg-white px-4 py-2 w-full flex items-center justify-between">
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
          className="px-4 py-2 bg-black text-white rounded-md hover:bg-gray-800">
            Log In
          </a>
      </div>
    </header>
  );
};

export default Header;