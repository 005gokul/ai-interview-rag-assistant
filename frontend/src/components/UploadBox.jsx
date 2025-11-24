import React, { useState } from 'react';
import { uploadFile } from '../services/api';
import { Upload, CheckCircle, AlertCircle } from 'lucide-react';

const UploadBox = () => {
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState('idle'); // idle, uploading, success, error
    const [message, setMessage] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setStatus('idle');
        setMessage('');
    };

    const handleUpload = async () => {
        if (!file) return;
        setStatus('uploading');
        const formData = new FormData();
        formData.append('file', file);

        try {
            await uploadFile(formData);
            setStatus('success');
            setMessage('File uploaded and ingested successfully!');
        } catch (error) {
            setStatus('error');
            const errorMsg = error.response?.data?.detail || 'Upload failed. Please try again.';
            setMessage(errorMsg);
        }
    };

    return (
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg mb-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Upload size={20} /> Upload Documents
            </h2>
            <div className="flex flex-col gap-4">
                <input
                    type="file"
                    onChange={handleFileChange}
                    className="block w-full text-sm text-gray-400
                        file:mr-4 file:py-2 file:px-4
                        file:rounded-full file:border-0
                        file:text-sm file:font-semibold
                        file:bg-blue-600 file:text-white
                        hover:file:bg-blue-700"
                />
                <button
                    onClick={handleUpload}
                    disabled={!file || status === 'uploading'}
                    className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50 transition-colors"
                >
                    {status === 'uploading' ? 'Uploading...' : 'Upload & Ingest'}
                </button>

                {status === 'success' && (
                    <div className="text-green-400 flex items-center gap-2 mt-2">
                        <CheckCircle size={16} /> {message}
                    </div>
                )}
                {status === 'error' && (
                    <div className="text-red-400 flex items-center gap-2 mt-2">
                        <AlertCircle size={16} /> {message}
                    </div>
                )}
            </div>
        </div>
    );
};

export default UploadBox;
