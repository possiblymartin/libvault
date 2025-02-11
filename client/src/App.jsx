import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from './pages/Home';
import PrivateRoute from "./components/PrivateRoute";

const App = () => {
	return (
		<Router>
				<div className="bg-gray-900 flex flex-col flex-1">
					<div className="flex-1 overflow-y-auto backdrop-grayscale">
						<Routes>
              <Route path="/" element={<Home />} />
						</Routes>
					</div>
				</div>
		</Router>
	);
};

export default App;
