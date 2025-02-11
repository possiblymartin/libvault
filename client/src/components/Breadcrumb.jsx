import React from "react";
import { useLocation, Link } from "react-router-dom";

const Breadcrumb = () => {
	const location = useLocation();
	const paths = location.pathname.split("/").filter((path) => path);

	return (
		<nav className="p-3 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 rounded-md">
			<ul className="flex space-x-2 text-sm">
				<li>
					<Link to="/" className="hover:underline">
						Home
					</Link>
				</li>
				{paths.map((path, index) => {
					const fullPath = `/${paths.slice(0, index + 1).join("/")}`;
					return (
						<li key={fullPath} className="flex items-center">
							<span className="mx-1">/</span>
							<Link to={fullPath} className="hover:underline capitalize">
								{path.replace("-", " ")}
							</Link>
						</li>
					);
				})}
			</ul>
		</nav>
	);
};

export default Breadcrumb;
