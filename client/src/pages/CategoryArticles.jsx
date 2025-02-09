import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

const CategoryArticles = () => {
  const [categories, setCategories] = useState([])
  const [articles, setArticles] = useState([]);
  const { categoryId } = useParams();
  const [loading, setLoading] = useState(true);
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

        // Ensure an array is set
        const data = Array.isArray(response.data) ? response.data : [];
        setArticles(data);
      } catch (err) {
        console.error('Error fetching articles:', err);
        setArticles([]);
      }
    };

    if (categoryId) fetchArticles();
  }, [categoryId]);

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
  
  const selectedCategory = categories.find(
    (c) => String(c.id) === categoryId
  );


  return (
    <div className="space-y-6">
      {selectedCategory ? (
        <h2 className="text-2xl font-bold text-black dark:text-gray-200">{selectedCategory.name}</h2>
      ) : loading ? (
        <h2 className="text-2xl font-bold text-black dark:text-gray-200">
          Loading Category...
        </h2>
      ) : null}
      <ul className="divide-y divide-gray-200 dark:divide-gray-800">
        {articles.map((article) => (
          <li key={article.id} className="py-4">
            <div className="flex flex-col">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                {article.title}
              </h3>
              <p className="mt-1 text-gray-600 dark:text-gray-400 line-clamp-2">
                {article.summary}
              </p>
              <div className="mt-3">
                <button 
                  onClick={() => navigate(`/articles/${article.id}`)}
                  className="text-blue-600 hover:underline"
                >
                  Read More →
                </button>
              </div>
            </div>
          </li>
        ))}
      </ul>
      {articles.length === 0 && (
        <div className="text-gray-500 text-center py-8">
          No articles found in this category
        </div>
      )}
    </div>
  );
};

export default CategoryArticles;
