import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register'; // New Register page
import CategoryArticles from './pages/CategoryArticles';
import FullArticle from './pages/FullArticle';
import ProfileView from './pages/ProfileView'; // Public profile view
import PrivateRoute from './components/PrivateRoute';
import PublicRoute from './components/PublicRoute';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
        <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />
        <Route path="/:username" element={<ProfileView />} /> {/* Public profile */}

        {/* Protected Dashboard Routes */}
        <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>}>
          <Route
            path="dashboard"
            element={
              <div className="text-gray-500 p-8">
                Select a category from the sidebar or add a new article
              </div>
            }
          />
          <Route path="category/:categoryId" element={<CategoryArticles />} />
        </Route>

        {/* Individual Article Detail */}
        <Route
          path="/articles/:articleId"
          element={<PrivateRoute><FullArticle /></PrivateRoute>}
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
