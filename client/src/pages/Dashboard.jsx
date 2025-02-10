import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom';
import AddArticle from './AddArticle';
import SettingsModal from '../components/SettingsModal';

const Dashboard = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(
          `${import.meta.env.VITE_API_BASE_URL}/api/categories`,
          { headers: { Authorization: `Bearer ${token}`}}
        );
        setCategories(response.data);
      } catch (err) {
        console.error('Error fetching categories:', err);
      } finally {
        setLoading(false);
      }
    }

    fetchCategories();
  }, [])

  const toggleSettingsModal = () => {
    setIsSettingsOpen(!isSettingsOpen);
  };

  return (
  <div className="flex min-h-screen bg-gray-50 dark:bg-gray-900 grayscale">
    {/* Sidebar */}
    <div className="w-64 bg-white dark:bg-black border-r border-gray-200 dark:border-gray-600 p-4">
      <h2 className="text-lg font-semibold mb-4 text-black dark:text-gray-300">Categories</h2>
      <nav className="space-y-1">
        {categories.map((category) => (
          <NavLink
            key={category.id}
            to={`/category/${category.id}`}
            className={({ isActive }) => 
              `block px-4 py-2 rounded-lg  
              ${isActive ? 
                  'bg-blue-50 text-blue-600 dark:bg-gray-900 dark:text-gray-300 transition-all duration-200 ease-in-out' : 
                  'text-gray-600 dark:text-gray-400 hover:bg-gray-100 hover:dark:bg-gray-900 transition-all duration-200 ease-in-out'}`
            }
          >
            {category.name}
          </NavLink>
        ))}
      </nav>
      <button onClick={toggleSettingsModal} className="mt-6 w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition">
        Settings
      </button>
    </div>

    {/* Main Content */}
    <div className="flex-1 p-8">
      <AddArticle />
      <Outlet />
    </div>

    {isSettingsOpen && (
      <SettingsModal isOpen={isSettingsOpen} onClose={toggleSettingsModal} />
    )}
  </div>
  );
};

export default Dashboard;