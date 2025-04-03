import axios from 'axios';

interface User {
  id: string
  email: string
  name: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export interface RegisterResponse extends LoginResponse {}

export interface RegisterData {
  email: string
  password: string
  name: string
}

const API_URL = 'http://localhost:8000/api/v1';

// Create an axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  timeout: 10000, // 10 second timeout
  withCredentials: true,
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', {
      url: config.url,
      method: config.method,
      headers: config.headers,
      data: config.data
    });
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', {
      status: response.status,
      headers: response.headers,
      data: response.data
    });
    return response;
  },
  (error) => {
    console.error('API Response Error:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      headers: error.response?.headers
    });
    return Promise.reject(error);
  }
);

export const authService = {
  async login(email: string, password: string): Promise<LoginResponse> {
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);
      
      const response = await api.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        return response.data;
      } else {
        throw new Error('Invalid response format');
      }
    } catch (error: any) {
      if (error.response?.status === 401) {
        throw new Error('Invalid email or password');
      } else if (error.response?.status === 400) {
        throw new Error(error.response.data.detail || 'Invalid request');
      } else if (error.response?.status === 422) {
        throw new Error('Invalid login data format');
      } else if (!error.response) {
        throw new Error('Network error - please check your connection');
      } else {
        throw new Error(`Login failed: ${error.response?.data?.detail || error.message}`);
      }
    }
  },

  async register(data: RegisterData): Promise<RegisterResponse> {
    try {
      const response = await api.post('/auth/register', data);

      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        return response.data;
      } else {
        throw new Error('Invalid response format');
      }
    } catch (error: any) {
      if (error.response?.status === 400) {
        throw new Error(error.response.data.detail || 'Invalid registration data');
      } else if (error.response?.status === 409) {
        throw new Error('Email already registered');
      } else if (error.response?.status === 422) {
        const details = error.response.data.detail;
        if (Array.isArray(details)) {
          throw new Error(details.map((d: any) => d.msg).join(', '));
        }
        throw new Error('Invalid registration data format');
      } else if (!error.response) {
        throw new Error('Network error - please check your connection');
      } else {
        throw new Error(`Registration failed: ${error.response?.data?.detail || error.message}`);
      }
    }
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  getToken() {
    return localStorage.getItem('token');
  },

  isAuthenticated() {
    return !!localStorage.getItem('token');
  }
};