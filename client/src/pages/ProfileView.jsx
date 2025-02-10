import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const ProfileView = () => {
  const { username } = useParams();
  const [profile, setProfile] = useState(null);
  const [articles, setArticles] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/${username}`);
        setProfile(response.data);
        setArticles(response.data.articles);
      } catch (err) {
        console.error(err);
        setError(err.response?.data?.error || 'Failed to load profile.');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [username]);

  if (loading) return <div className="p-8 text-gray-500">Loading profile...</div>;
  if (error) return <div className="p-8 text-red-500">{error}</div>;

  return (
    <div className="max-w-4xl mx-auto p-8">
      <div className="flex items-center mb-6">
        <img
          src={profile.avatar || '/default-avatar.png'}
          alt={`${profile.username}'s avatar`}
          className="w-16 h-16 rounded-full mr-4"
        />
        <div>
          <h1 className="text-2xl font-bold">{profile.full_name || profile.username}</h1>
          <p className="text-gray-600">@{profile.username}</p>
        </div>
      </div>
      <h2 className="text-xl font-semibold mb-4">Library</h2>
      {articles.length > 0 ? (
        <ul className="space-y-4">
          {articles.map((article) => (
            <li key={article.id} className="bg-white shadow rounded p-4">
              <h3 className="text-lg font-semibold">{article.title}</h3>
              <p className="text-gray-600">{article.summary}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500">No articles found.</p>
      )}
    </div>
  );
};

export default ProfileView;
