import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom';
import AddArticle from './AddArticle';

const Dashboard = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
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

  return (
  <div className="flex min-h-screen bg-gray-50">
    {/* Sidebar */}
    <div className="w-64 bg-white border-r border-gray-200 p-4">
      <h2 className="text-lg font-semibold mb-4">Categories</h2>
      <nav className="space-y-1">
        {categories.map((category) => (
          <NavLink
            key={category.id}
            to={`/category/${category.id}`}
            className={({ isActive }) => 
              `block px-4 py-2 rounded-lg ${isActive ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-100'}`
            }
          >
            {category.name}
          </NavLink>
        ))}
      </nav>
    </div>

    {/* Main Content */}
    <div className="flex-1 p-8">
      <AddArticle />
      <Outlet />
    </div>
  </div>
  );
};

export default Dashboard;