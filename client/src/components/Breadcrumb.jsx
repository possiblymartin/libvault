import React from 'react';
import { Link } from 'react-router-dom';

const Breadcrumb = ({ items }) => {
  return (
    <nav className="flex text-sm mb-4" aria-label="Breadcrumb">
      {items.map((item, index) => (
        <div key={index} className='flex items-center'>
          {item.href ? (
            <Link to={item.href} className='text-gray-600 hover:underline'>
              {item.name}
            </Link>
          ) : (
            <span className='text-gray-500'>{item.name}</span>
          )}
          {index < items.length - 1 && (
            <span className='mx-2 text-gray-500'>/</span>
          )}
        </div>
      ))}
    </nav>
  )
}

export default Breadcrumb;