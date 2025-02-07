import React, { useState } from 'react';
import { FaChevronDown, FaChevronUp } from 'react-icons/fa';

const Dropdown = ({ label, items }) => {
  const [isOpen, setIsOpen ] = useState(false);

  return (
    <div 
      className="relative inline-block" 
      onMouseEnter={() => setIsOpen(true)} 
      onMouseLeave={() => setIsOpen(false)}
    >
      <button className={`flex items-center text-gray-600 hover:bg-gray-100 rounded-md px-3 py-1 font-medium focus:outline-none ${isOpen ? 'bg-gray-100' : ''} cursor-pointer`}>
        <span>{label}</span>
        <span className="ml-1 text-[10px]">{isOpen ? <FaChevronUp /> : <FaChevronDown />}</span>
      </button>
      {isOpen && (
        <div className="absolute top-6 left-0 mt-2 w-48 bg-white rounded-md shadow-sm z-10">
          <ul className="p-2">
            {items.map((item, index) => (
              <li key={index}>
                <a href={item.href} className="block px-2 py-1 rounded-md text-gray-600 hover:bg-gray-100">
                  {item.label}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Dropdown;