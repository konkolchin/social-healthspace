import axios from 'axios';
import { authService } from './authService';

// frontend/src/services/api.ts
const API_BASE_URL = import.meta.env.VITE_API_URL || "https://social-healthspace.fly.dev";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Or, if using fetch:
export const fetchFromApi = async (endpoint: string) => {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);
  return response.json();
};

// Add request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    // Log the request configuration
    console.log('Making request:', {
      url: config.url,
      method: config.method,
      headers: config.headers
    });

    const token = authService.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('Response received:', {
      status: response.status,
      data: response.data
    });
    return response;
  },
  async (error) => {
    console.error('Response error:', {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    });

    if (error.response?.status === 401) {
      // Clear auth data and redirect to login
      authService.logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
