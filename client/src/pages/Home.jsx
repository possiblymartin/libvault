import React from 'react';
import MainLayout from '../layouts/MainLayout';
import SummarizeArticle from '../components/SummarizeArticle';

const Home = () => {
  return (
    <MainLayout>
      <div className="flex flex-col items-center justify-center text-center h-full">
        <SummarizeArticle />
      </div>
    </MainLayout>
  )
}

export default Home;