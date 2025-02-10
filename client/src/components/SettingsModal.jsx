import React, { useState } from 'react';
import Modal from 'react-modal';
import axios from 'axios';

Modal.setAppElement('#root'); // Accessibility requirement

const SettingsModal = ({ isOpen, onClose }) => {
  const [formData, setFormData] = useState({
    username: '',
    full_name: '',
    avatar: '',
    is_library_public: false,
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const response = await axios.put(
        `${import.meta.env.VITE_API_BASE_URL}/api/users/profile`,
        formData,
        { headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` } }
      );
      setSuccess(response.data.message);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || 'Failed to update profile.');
    }
  };

  return (
    <Modal isOpen={isOpen} onRequestClose={onClose} style={{ content: { maxWidth: '500px', margin: 'auto' } }}>
      <h2 className="text-xl font-bold mb-4">Edit Profile</h2>
      {error && <p className="text-red-500">{error}</p>}
      {success && <p className="text-green-500">{success}</p>}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="block mb-1">Username</label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            className="w-full border rounded p-2"
          />
        </div>
        <div className="mb-3">
          <label className="block mb-1">Full Name</label>
          <input
            type="text"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            className="w-full border rounded p-2"
          />
        </div>
        <div className="mb-3">
          <label className="block mb-1">Avatar URL</label>
          <input
            type="text"
            name="avatar"
            value={formData.avatar}
            onChange={handleChange}
            className="w-full border rounded p-2"
          />
        </div>
        <div className="mb-3">
          <label className="flex items-center">
            <input
              type="checkbox"
              name="is_library_public"
              checked={formData.is_library_public}
              onChange={handleChange}
              className="mr-2"
            />
            Make library public
          </label>
        </div>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Save Changes
        </button>
      </form>
    </Modal>
  );
};

export default SettingsModal;
