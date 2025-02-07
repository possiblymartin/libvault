import React from 'react';
import Dropdown from './Dropdown';

const Header = () => {
  return (
    <header className="bg-white shadow-md px-4 py-2 flex items-center justify-between">
      {/* Left Section */}
      <div className="flex items-center space-x-8">
        <div className="text-xl font-bold text-gray-800">libvault</div>
        <nav className="flex items-center space-x-6">
          <Dropdown
            label="Features"
            items={[
              {label: 'Summarize Articles', href:'/'}
            ]}
          />
          <Dropdown
            label="Pricing"
            items={[
              {label: 'Free Plan', href:'/'},
              {label: 'Pro Plan', href:'/'}
            ]}
          />
          <a href="/about" className="text-gray-600 hover:text-blue-600">
            About Us
          </a>
        </nav>
      </div>
      {/* Right Section */}
      <div>
        <a
          href="/login"
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
            Log In
          </a>
      </div>
    </header>
  );
};

export default Header;