import api from './api';
import type { Post } from '../types/community';

export const postService = {
  createPost: async (post: Omit<Post, 'id' | 'created_at'>): Promise<Post> => {
    const response = await api.post('/posts/', post);
    return response.data;
  },

  getUserPosts: async (userId: string): Promise<Post[]> => {
    const response = await api.get(`/posts/user/${userId}`);
    return response.data;
  },

  getAllPosts: async (): Promise<Post[]> => {
    const response = await api.get('/posts/');
    return response.data;
  },

  getCommunityPosts: async (communityId: number): Promise<Post[]> => {
    const response = await api.get(`/posts/community/${communityId}`);
    return response.data;
  },

  deletePost: async (postId: string): Promise<void> => {
    await api.delete(`/posts/${postId}`);
  }
}; 