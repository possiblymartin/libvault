import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';

const ArticleDetail = () => {
  const { articleId } = useParams();
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(
          `${import.meta.env.VITE_API_BASE_URL}/api/articles/${articleId}`, {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        setArticle(response.data);
      } catch (err) {
        setError('Article not found');
      } finally {
        setLoading(false);
      }
    };
    fetchArticle();
  }, [artcileId]);

  if (loading) return <div className="p-4">Loading...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <Link to="/dashboard" className="text-blue-500 hover:underline">Back to Dashboard</Link>
      <h1 className="text-2xl font-bold mt-4">{article.title}</h1>
      <p className="text-gray-500 mt-2">{article.category}</p>
      <a
        href={article.url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-500 hover:underline block mt-2"
      >
        View Original Article
      </a>
      <div className="mt-6">
        <h2 className="text-xl font-semibold mb-2">Summary</h2>
        <p className="text-gray-700">{article.summary}</p>
      </div>
      <div className="mt-6">
        <h2 className="text-xl font-semibold mb-2">Full Content</h2>
        <p className="text-gray-700 whitespace-pre-wrap">{article.content}</p>
      </div>
    </div>
  );
};

export default ArticleDetail;