import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [categories, setCategories] = useState([]);
  const [articles, setArticles] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [newCategoryName, setNewCategoryName] = useState('');
  const [showCategoryForm, setShowCategoryForm] = useState('');

  useEffect(() => {

  }, [])  

  const fetchCategories = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:5001/categories')
      setCategories(res.data);
    } catch (err) {
      console.error(err);
    };
  };

  const fetchArticles = async () => {
    try {
      const res = axios.get('http://127.0.0.1:5001/articles');
      setArticles(res.data);
    } catch (err) {
      console.error(err);
    };
  };

  const handleCategoryClick = (category) => {
    setSelectedCategory(category);
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleCreateCategory = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://127.0.0.1:5001/categories', {name: newCategoryName})
      setCategories([...categories, { id: res.data.category_id, name: newCategoryName }])
      setNewCategoryName('')
      setShowCategoryForm(false)
    } catch (err) {
      console.error(err);
    };
  };

  const filteredArticles = articles.filter(article => {
    const matchesCategory = selectedCategory ? article.category_id === selectedCategory.id : true
    const matchesSearch = article.title.toLowerCase().includes(searchTerm.toLowerCase())
    return matchesCategory && matchesSearch
  })

  return (
    <div className="flex">
      <aside className="w-64 bg-gray-800 text-white p-4">
        <h2 className="text-xl font-bold mb-4">Categories</h2>
        <ul>
          {categories.map(category => (
            <li
              key={category.id}
              className="mb-2 cursor-point"
              onClick={() => handleCategoryClick(category)}>
              {category.name}
            </li>
          ))}
        </ul>
        <button
          className="mt-4 gray-700 px-2 py-1 rounded"
          onClick={() => setShowCategoryForm(!showCategoryForm)}>
            {showCategoryForm ? 'Cancel' : 'Add Category'}
        </button>
        {showCategoryForm && (
          <form onSubmit={handleCreateCategory} className="mt-2">
            <input
              type="text"
              value={newCategoryName}
              onChange={(e) => setNewCategoryName(e.target.value)}
              placeholder="New category name"
              className="p-1 rounded text-gray-400"
              required
            />
            <button type="submit" className="ml-2 bg-gray-100 px-2 py-1 rounded">
              Create
            </button>
          </form>
        )}
      </aside>
      <main className='flex-1 p-4'>
        <div className="mb-4">
          <div>
            {filteredArticles.map(article => (
              <div key={article.id} className="p-4 border-b border-gray-300">
                <Link to={`/articles/${article.id}`} className="text-2xl font-bold">{article.title}</Link>
                <p>{article.summary}</p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;