import React, { useState } from 'react';
import { askQuestion } from '../services/api';
import { Send, BookOpen, Layers } from 'lucide-react';

const ChatBox = () => {
    const [query, setQuery] = useState('');
    const [response, setResponse] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleAsk = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        setLoading(true);
        setResponse(null);
        try {
            const res = await askQuestion(query);
            setResponse(res.data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg mb-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Layers size={20} /> Interview Assistant
            </h2>

            <form onSubmit={handleAsk} className="flex gap-2 mb-6">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Ask about Java, SQL, DSA..."
                    className="flex-1 bg-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                    type="submit"
                    disabled={loading}
                    className="bg-green-600 hover:bg-green-700 text-white p-2 rounded transition-colors disabled:opacity-50"
                >
                    <Send size={20} />
                </button>
            </form>

            {loading && <div className="text-center text-gray-400 animate-pulse">Thinking...</div>}

            {response && (
                <div className="space-y-6">
                    <div className="bg-gray-700 p-4 rounded border-l-4 border-green-500">
                        <h3 className="font-bold text-lg mb-2">Answer:</h3>
                        <p className="whitespace-pre-wrap leading-relaxed">{response.answer}</p>
                    </div>

                    {response.citations && response.citations.length > 0 && (
                        <div className="bg-gray-700 p-4 rounded border-l-4 border-blue-500">
                            <h3 className="font-bold text-lg mb-2 flex items-center gap-2">
                                <BookOpen size={18} /> Citations
                            </h3>
                            <div className="space-y-4">
                                {response.citations.map((cite, idx) => (
                                    <div key={idx} className="text-sm bg-gray-800 p-3 rounded">
                                        <p className="italic text-gray-300 mb-1">"{cite.text.substring(0, 150)}..."</p>
                                        <div className="text-xs text-gray-500 flex justify-between mt-2">
                                            <span>Source: {cite.metadata.source}</span>
                                            <span>Score: {response.scores.rerank[idx]?.toFixed(2)}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default ChatBox;
