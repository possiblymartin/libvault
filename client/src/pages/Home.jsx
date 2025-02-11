import React from 'react';
import MainLayout from '../layouts/MainLayout';
import SummarizeArticle from '../components/SummarizeArticle';

const Home = () => {
  return (
    <MainLayout>
      <div className="px-2 justify-center items-center text-gray-300 text-3xl font-semibold mb-6">
        Summarize an article.
      </div>
      <SummarizeArticle />
    </MainLayout>
  )
}

export default Home;