import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FaArrowRight, FaSpinner } from "react-icons/fa6";


const SummarizeArticle = ({ isLoggedIn, userId }) => {
  // For the input view
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // For the article view
  const [summary, setSummary] = useState(null);
  const [fullArticle, setFullArticle] = useState(null);

  // Hold the article when the user is not logged in
  const [unsavedArticle, setUnsavedArticle] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isLoggedIn && unsavedArticle) {
      setError("You must sign in to summarize more than one article.");
      return;
    }
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post("http://127.0.0.1:5001/summarize", { url });

      setSummary(response.data.summary);
      setFullArticle(response.data.full_article);

      if (isLoggedIn) {
        await axios.post("http://127.0.0.1:5001/save-article", {
          user_id: userId,
          url,
          summary: response.data.summary,
          full_article: response.data.full_article
        });
      } else {
        setUnsavedArticle({
          url,
          summary: response.data.summary,
          fullArticle: response.data.full_article,
        })
      }
    } catch (err) {
      setError("Failed to fetch summary. Please try again");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    const saveUnsavedArticle = async () => {
      if (isLoggedIn && unsavedArticle) {
        try {
          await axios.post("http://127.0.0.1:5001/save-article", {
            user_id: userId,
            url: unsavedArticle.url,
            summary: unsavedArticle.summary,
            full_article: unsavedArticle.fullArticle,
          });

          setUnsavedArticle(null);
        } catch (err) {
          console.error("Failed to save unsaved article:", err);
        }
      }
    };
    saveUnsavedArticle();
  }, [isLoggedIn, unsavedArticle, userId]);

  if (summary && fullArticle) {
    return (
      <div className="flex flex-col p-4 text-left">
        <h1 className="text-3xl font-bold text-gray-300 mb-4">Summarized Article</h1>
        <div className="bg-gray-700 p-4 rounded-lg mb-4">
          <h2 className="font-bold text-lg text-white">AI Summary:</h2>
          <ul className="list-disc list-inside text-gray-300">
            {summary.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ul>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-gray-300 mb-4">
          <h2 className="font-bold text-lg text-white">Full Article:</h2>
          <p className="whitespace-pre-wrap">{fullArticle}</p>
        </div>
        {/* You can add additional features (annotations, editing, etc.) here */}
      </div>
    );
  }

  // Otherwise, show the input view.
  return (
    <div className="flex flex-col items-center justify-center">
      <h1 className="text-3xl font-semibold text-gray-300 mb-4">Summarize an article.</h1>
      <div className="w-full mx-auto">
        <form onSubmit={handleSubmit} className="flex bg-gray-800 grayscale p-3 rounded-2xl items-center w-[512px]">
          <input
            type="text"
            placeholder="Paste a link"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="flex-grow bg-transparent text-gray-300 focus:ring-0 focus:outline-none"
          />
          <button className="ml-2 bg-gray-200 hover:opacity-75 p-2 rounded-full">
            {loading ? (
              <FaSpinner className="text-gray-900 animate-spin" />
            ) : (
              <FaArrowRight className="text-gray-900" />
            )
            }
          </button>
        </form>
        {error && <p className="mt-2 text-red-500">{error}</p>}
      </div>
    </div>
  );

}

export default SummarizeArticle;