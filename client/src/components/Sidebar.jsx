import React from "react";
import { BsMenuButtonFill } from "react-icons/bs";
import { FaSearch } from "react-icons/fa";
import { FaBookBookmark } from "react-icons/fa6";
import { FaSwatchbook } from "react-icons/fa";

const Sidebar = ({
  categories = [],
  onCollapse,
  onSearch,
  onAddDashboard,
  onNewCategory,
  isCollapsed = false,
}) => {
  // Sort categories alphabetically by name.
  const sortedCategories = [...categories].sort((a, b) =>
    a.name.localeCompare(b.name)
  );

  return (
    <div className={`h-full flex flex-col bg-gray-100 dark:bg-gray-800 ${isCollapsed ? 'w-16' : 'w-64'}`}>
      {/* Top Bar */}
      <div className="flex items-center justify-between p-3 border-b border-gray-300 dark:border-gray-700">
        {/* Collapse button on the left */}
        <button onClick={onCollapse} className="text-2xl">
          <BsMenuButtonFill />
        </button>
        {/* On the right: Search and Dashboard buttons */}
        <div className="flex space-x-3">
          <button onClick={onSearch} className="text-xl">
            <FaSearch />
          </button>
          <button onClick={onAddDashboard} className="text-xl">
            <FaBookBookmark />
          </button>
        </div>
      </div>

      {/* New Category Button */}
      <div className="p-3 border-b border-gray-300 dark:border-gray-700">
        <button
          onClick={onNewCategory}
          className="flex items-center space-x-2 bg-blue-500 text-white px-3 py-2 rounded hover:bg-blue-600 transition-colors"
        >
          <FaSwatchbook />
          {!isCollapsed && <span>New Category</span>}
        </button>
      </div>

      {/* Scrollable Category List */}
      <div className="flex-1 overflow-y-auto p-3">
        {sortedCategories.map((category) => (
          <div key={category.id} className="mb-4">
            {/* Category name; hide if collapsed */}
            {!isCollapsed && (
              <h3 className="text-lg font-semibold mb-2">{category.name}</h3>
            )}
            {/* List of articles under the category */}
            <ul className="space-y-1">
              {category.articles &&
                category.articles.map((article) => (
                  <li key={article.id}>
                    <a
                      href={article.link}
                      className="block text-sm text-gray-700 dark:text-gray-300 hover:underline"
                      title={article.title}
                    >
                      {isCollapsed ? article.title.charAt(0) : article.title}
                    </a>
                  </li>
                ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
