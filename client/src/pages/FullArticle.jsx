import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { FaExternalLinkAlt } from 'react-icons/fa';

const FullArticle = () => {
  const { articleId } = useParams();
  const navigate = useNavigate();
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(
          `${import.meta.env.VITE_API_BASE_URL}/api/articles/${articleId}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setArticle(response.data);
      } catch (err) {
        console.error('Error fetching article:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchArticle();
  }, [articleId]);

  if (loading) return <div className="p-8 text-gray-500">Loading article...</div>;
  if (!article) return <div className="p-8 text-red-500">Article not found</div>;

  return (
    <div className="min-h-screen bg-amber-50 dark:bg-black grayscale">
      <div className="max-w-3xl mx-auto px-4 py-8">
        {/* Header Section */}
        <div className="mb-8">
          <button
            onClick={() => navigate(-1)}
            className="text-gray-600 dark:text-gray-300 dark:hover:bg-gray-800 rounded p-1 mb-4 inline-flex items-center cursor-pointer"
          >
            ← Back to articles
          </button>
          <div className="flex items-center justify-between mb-4 space-x-4">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-300 flex-1 break-words pr-4">{article.title}</h1>
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 dark:text-gray-200 flex items-center gap-2 p-1 hover:bg-gray-800 rounded"
            >
              <FaExternalLinkAlt className="inline-block" />
              <span>Visit Original</span>
            </a>
          </div>
          <div className="border-b border-gray-200 dark:border-gray-600"></div>
        </div>

        {/* Content Section */}
        <div className="prose max-w-none">
          {/* Summary Section */}
          {article.summary && (
            <div className="mb-12 p-6 bg-gray-50 dark:bg-gray-800 rounded-xl grayscale">
              <h3 className="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-300">AI Summary</h3>
              <ul className="space-y-3 list-disc list-inside text-gray-600 dark:text-gray-300">
                {article.summary.split('\n').map((point, index) => (
                  <li key={index}>{point}</li>
                ))}
              </ul>
            </div>
          )}
          <div className="text-gray-700 dark:text-gray-400 whitespace-pre-line font-serif - text-lg leading-relaxed">
            {article.content.split('\n\n').map((paragraph, index) => (
              <p key={index} className="mb-4">
                {paragraph}
              </p>
            ))}
          </div>
          
        </div>
      </div>
    </div>
  );
};

export default FullArticle;
