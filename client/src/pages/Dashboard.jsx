import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Outlet, useNavigate } from 'react-router-dom';
import AddArticle from './AddArticle';
import SettingsModal from '../components/SettingsModal';
import Sidebar from '../components/Sidebar';
import SearchModal from '../components/SearchModal';

const Dashboard = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const navigate = useNavigate();

  // First, fetch the categories (assumed not to include articles)
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(
          `${import.meta.env.VITE_API_BASE_URL}/api/categories`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setCategories(response.data);
      } catch (err) {
        console.error('Error fetching categories:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  // Once categories are loaded, fetch articles for each category if not already present.
  // We check that the first category does not have an "articles" property.
  useEffect(() => {
    if (!loading && categories.length > 0 && categories[0] && categories[0].articles === undefined) {
      const fetchArticlesForCategories = async () => {
        const token = localStorage.getItem('token');
        const updatedCategories = await Promise.all(
          categories.map(async (category) => {
            try {
              const response = await axios.get(
                `${import.meta.env.VITE_API_BASE_URL}/api/articles`,
                {
                  headers: { Authorization: `Bearer ${token}` },
                  params: { category: category.id },
                }
              );
              return { ...category, articles: response.data };
            } catch (err) {
              console.error('Error fetching articles for category', category.id, err);
              return { ...category, articles: [] };
            }
          })
        );
        setCategories(updatedCategories);
      };
      fetchArticlesForCategories();
    }
  }, [loading, categories]);

  const toggleSettingsModal = () => {
    setIsSettingsOpen(!isSettingsOpen);
  };

  const handleCollapseSidebar = () => {
    setIsSidebarCollapsed(!isSidebarCollapsed);
  };

  const handleSearch = () => {
    setIsSearchOpen(true);
  };

  const handleCloseSearch = () => {
    setIsSearchOpen(false);
  };

  const handleAddDashboard = () => {
    // For example, scroll to AddArticle or simply navigate
    navigate('/dashboard');
  };

  const handleNewCategory = () => {
    navigate('/new-category');
  };

  return (
    <div className="flex min-h-screen bg-gray-50 dark:bg-gray-900 grayscale">
      {/* Sidebar container: adjust width based on isSidebarCollapsed */}
      <div className={`transition-all duration-300 ${isSidebarCollapsed ? 'w-16' : 'w-64'}`}>
        <Sidebar 
          categories={categories}
          onCollapse={handleCollapseSidebar}
          onSearch={handleSearch}
          onAddDashboard={handleAddDashboard}
          onNewCategory={handleNewCategory}
          isCollapsed={isSidebarCollapsed}
        />
      </div>

      {/* Main Content Area */}
      <div className="flex-1 p-8">
        <AddArticle />
        <Outlet />
      </div>

      {isSettingsOpen && (
        <SettingsModal isOpen={isSettingsOpen} onClose={toggleSettingsModal} />
      )}

      {isSearchOpen && (
        <SearchModal isOpen={isSearchOpen} onClose={handleCloseSearch} />
      )}
    </div>
  );
};

export default Dashboard;
