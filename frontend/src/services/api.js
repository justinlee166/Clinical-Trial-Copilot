import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes timeout for large files
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.detail || error.response.data?.message || 'Server error occurred';
      throw new Error(message);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('No response from server. Please check if the backend is running.');
    } else {
      // Something else happened
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
);

export const analyzePDF = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await api.post('/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    console.error('PDF Analysis Error:', error);
    throw error;
  }
};

export const getAnalysisStatus = async (analysisId) => {
  try {
    const response = await api.get(`/status/${analysisId}`);
    return response.data;
  } catch (error) {
    console.error('Status Check Error:', error);
    throw error;
  }
};

export const getAnalysisResults = async (analysisId) => {
  try {
    const response = await api.get(`/results/${analysisId}`);
    return response.data;
  } catch (error) {
    console.error('Results Fetch Error:', error);
    throw error;
  }
};

export const downloadFile = async (analysisId, fileType) => {
  try {
    const response = await api.get(`/download/${analysisId}/${fileType}`, {
      responseType: 'blob',
    });

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.download = `${fileType}_${analysisId}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);

    return true;
  } catch (error) {
    console.error('Download Error:', error);
    throw error;
  }
};

export const getHealthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health Check Error:', error);
    throw error;
  }
};

export default api;
