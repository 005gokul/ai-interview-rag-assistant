import React, { useEffect, useState } from 'react';
import { getAnalytics } from '../services/api';
import { BarChart2, RefreshCw } from 'lucide-react';

const AnalyticsPanel = () => {
    const [records, setRecords] = useState([]);

    const fetchAnalytics = async () => {
        try {
            const res = await getAnalytics();
            setRecords(res.data);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        fetchAnalytics();
    }, []);

    return (
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-semibold flex items-center gap-2">
                    <BarChart2 size={20} /> Analytics
                </h2>
                <button
                    onClick={fetchAnalytics}
                    className="text-gray-400 hover:text-white transition-colors"
                >
                    <RefreshCw size={18} />
                </button>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm text-gray-400">
                    <thead className="bg-gray-700 text-gray-200 uppercase">
                        <tr>
                            <th className="px-4 py-3">Time</th>
                            <th className="px-4 py-3">Question</th>
                            <th className="px-4 py-3">Latency (s)</th>
                            <th className="px-4 py-3">Top Rerank Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {records.map((rec, idx) => (
                            <tr key={idx} className="border-b border-gray-700 hover:bg-gray-750">
                                <td className="px-4 py-3">
                                    {new Date(rec.timestamp * 1000).toLocaleTimeString()}
                                </td>
                                <td className="px-4 py-3 truncate max-w-xs" title={rec.question}>
                                    {rec.question}
                                </td>
                                <td className="px-4 py-3">{rec.latency.toFixed(3)}</td>
                                <td className="px-4 py-3">
                                    {rec.rerank_scores && rec.rerank_scores.length > 0
                                        ? Math.max(...rec.rerank_scores).toFixed(2)
                                        : 'N/A'}
                                </td>
                            </tr>
                        ))}
                        {records.length === 0 && (
                            <tr>
                                <td colSpan="4" className="px-4 py-3 text-center">No records found</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AnalyticsPanel;
