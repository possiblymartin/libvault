import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import Home from './pages/Home';
import Login from './pages/Login';

import PrivateRoute from './components/PrivateRoute';
import PublicRoute from './components/PublicRoute';

import './styles/App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          }
        />
        {/*
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
              </PrivateRoute>
            }
          />
        */}

        <Route path="/" element={<Home />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
