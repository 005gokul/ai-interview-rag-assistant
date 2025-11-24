import axios from 'axios';

const API_URL = 'http://localhost:8001';

const api = axios.create({
    baseURL: API_URL,
});

export const checkHealth = () => api.get('/health');
export const uploadFile = (formData) => api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
});
export const ingestFiles = () => api.post('/ingest');
export const askQuestion = (question) => api.post('/ask', { question });
export const getAnalytics = () => api.get('/analytics');

export default api;
