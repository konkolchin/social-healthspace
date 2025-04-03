import api from './api';
import { Community, CommunityCreate, CommunityUpdate } from '../types/community';

export const communityService = {
  create: async (data: CommunityCreate) => {
    const response = await api.post<Community>('/communities/', data);
    return response.data;
  },

  list: async (search?: string) => {
    try {
      console.log('Making API request to /api/v1/communities/'); // Debug log
      const response = await api.get('/communities/', { 
        params: { search },
        headers: {
          'Content-Type': 'application/json',
          // Add auth header if needed
          ...(localStorage.getItem('token') && {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          })
        }
      });
      console.log('API Response:', response); // Debug log
      return response.data;
    } catch (error) {
      console.error('API Error:', error); // Debug log
      throw error;
    }
  },

  getMyCommunities: async () => {
    const response = await api.get<Community[]>('/communities/my');
    return response.data;
  },

  getBySlug: async (slug: string) => {
    const response = await api.get<Community>(`/communities/${slug}`);
    return response.data;
  },

  update: async (id: number, data: CommunityUpdate) => {
    const response = await api.put<Community>(`/communities/${id}`, data);
    return response.data;
  },

  join: async (id: number) => {
    const response = await api.post<Community>(`/communities/${id}/members`);
    return response.data;
  },

  leave: async (id: number) => {
    const response = await api.delete<Community>(`/communities/${id}/members`);
    return response.data;
  },

  delete: async (id: number) => {
    const response = await api.delete<Community>(`/communities/${id}`);
    return response.data;
  }
};
