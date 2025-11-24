import React from 'react';
import UploadBox from './components/UploadBox';
import ChatBox from './components/ChatBox';
import AnalyticsPanel from './components/AnalyticsPanel';

function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-8 text-center">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-green-400 bg-clip-text text-transparent">
            RAG Interview Prep
          </h1>
          <p className="text-gray-400 mt-2">Master your technical interviews with AI-powered insights</p>
        </header>

        <div className="grid grid-cols-1 gap-8">
          <UploadBox />
          <ChatBox />
          <AnalyticsPanel />
        </div>
      </div>
    </div>
  );
}

export default App;
