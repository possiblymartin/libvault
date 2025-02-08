import React, { useState } from 'react';
import axios from 'axios';

const AddArticle = ({ onAdd }) => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/api/process-url`,
        { url },
        { headers: { Authorization: `Bearer ${token}`}}
      );
      setUrl('');
      if (onAdd) onAdd();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mb-8 bg-white rounded-xl p-6 shadow-sm">
      <form onSubmit={handleSubmit} className="flex gap-4">
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Paste an article URL here..."
          className="flex-1 p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          required
        />
        <button type="submit" className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 cursor-pointer" disabled={loading}>
          {loading ? 'Processing...' : 'Summarize'}
        </button>
      </form>
    </div>
  )
}

export default AddArticle;