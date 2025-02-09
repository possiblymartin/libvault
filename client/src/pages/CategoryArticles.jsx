import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

const CategoryArticles = () => {
  const [articles, setArticles] = useState([]);
  const { categoryId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(
          `${import.meta.env.VITE_API_BASE_URL}/api/articles`,
          { 
            headers: { Authorization: `Bearer ${token}` },
            params: { category: categoryId }
          }
        );
        
        // Ensure we're getting an array
        const data = Array.isArray(response.data) ? response.data : [];
        setArticles(data);
      } catch (err) {
        console.error('Error fetching articles:', err);
        setArticles([]); // Reset to empty array on error
      }
    };
    
    if (categoryId) fetchArticles();
  }, [categoryId]);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-black dark:text-gray-200">Articles</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Add array check before mapping */}
        {Array.isArray(articles) && articles.map((article) => (
          <div key={article.id} className="bg-white dark:bg-black rounded-xl shadow-sm hover:shadow-md transition-shadow p-6">
            <h3 className="text-lg text-black dark:text-gray-300 font-semibold mb-2">{article.title}</h3>
            <div className="space-y-2 mb-4">
              {/* Add optional chaining for summary */}
              {article?.summary?.split('\n')?.map((point, index) => (
                <p key={index} className="text-gray-600 dark:text-gray-400">• {point}</p>
              ))}
            </div>
            <a
              onClick={() => navigate(`/articles/${article.id}`)}
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-800 dark:text-gray-200 hover:bg-gray-800 p-1 rounded font-medium cursor-pointer"
            >
              View Full Article →
            </a>
          </div>
        ))}
      </div>
      {/* Show empty state */}
      {articles.length === 0 && (
        <div className="text-gray-500 text-center py-8">
          No articles found in this category
        </div>
      )}
    </div>
  );
};

export default CategoryArticles;
