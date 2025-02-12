import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FaArrowRight } from "react-icons/fa6";


const SummarizeArticle = ({ isLoggedIn, userId }) => {
  const [url, setUrl] = useState('');
  const [summary, setSummary] = useState(null);
  const [fullArticle, setFullArticle] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasSummarized, setHasSummarized] = useState (
    localStorage.getItem("hasSummarized") === "true"
  );

  useEffect(() => {
    if (summary || fullArticle) {
      localStorage.setItem("hasSummarized", "true");
      setHasSummarized(true);
    }
  }, [summary, fullArticle]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isLoggedIn && hasSummarized) {
      setError("You must sign in to summarize more than one article.");
      return;
    }
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post("http://127.0.0.1:5001/summarize", {url});
      setSummary(response.data.summary);
      setFullArticle(response.data.full_article);

      if (isLoggedIn) {
        await axios.post("http://127.0.0.1:5001/save-article", {
          user_id: userId,
          url,
          summary: response.data.summary,
          full_article: response.data.full_article,
        });
      }
    } catch (err) {
      setError("Failed to fetch summary. Please try again")
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-screen p-4">
      <div className={`flex-grow p-4 ${summary ? "" : "justify-center items-center"}`}>
        {summary && (
          <div className="bg-gray-700 p-4 rounded-lg mb-4 text-left grayscale">
            <h2 className="font-bold text-lg text-gray-300">Summary:</h2>
            <ul className="list-disc list-inside text-gray-400">
              {summary.map((point, index) => (
                <li key={index}>(point)</li>
              ))}
            </ul>
          </div>
        )}

        {fullArticle && (
          <div className="bg-gray-800 p-4 rounded-lg text-gray-300 text-left grayscale">
            <h2 className="font-bold text-lg text-white">Full Article:</h2>
            <p className="whitespace-pre-wrap">{fullArticle}</p>
          </div>
        )}
      </div>

        <div className={`rounded-2xl bg-gray-800 ${summary ? "fixed bottom-0 left-0": "absolute top-1/2 transform -translate-y-1/2"} text-gray-300 grayscale p-3 w-180`}>
          <form className="justify-between flex" onSubmit={handleSubmit}>
            <input
              placeholder="Paste a link"
              className="w-full text-gray-300 resize-none overflow-hidden focus:ring-0 focus:outline-none"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <div className="justify-end">
              <button className="items-center align-middle justify-center rounded-full bg-gray-200 hover:opacity-75 p-2 cursor-pointer"><FaArrowRight className="text-gray-900" /></button>
            </div>
          </form>
        </div>
    </div>
  )
}

export default SummarizeArticle;