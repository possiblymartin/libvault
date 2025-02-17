import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from './pages/Home';
import Login from "./pages/Login";
import Register from "./pages/Register";
import PrivateRoute from "./components/PrivateRoute";
import Dashboard from "./pages/Dashboard";

const App = () => {
	return (
		<Router>
				<div className="bg-gray-900 flex flex-col flex-1">
					<div className="flex-1 overflow-y-auto backdrop-grayscale">
						<Routes>
              <Route path="/" element={<Home />} />
              <Route path="/register" element={<Register />} />
              <Route path="/login" element={<Login />} />
              <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
						</Routes>
					</div>
				</div>
		</Router>
	);
};

export default App;
