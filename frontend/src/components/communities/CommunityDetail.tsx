import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Community, Post } from '../../types/community';
import { communityService } from '../../services/communityService';
import { postService } from '../../services/postService';
import './CommunityDetail.css';

export const CommunityDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  const [community, setCommunity] = useState<Community | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [newPost, setNewPost] = useState({ title: '', content: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const loadCommunity = async () => {
      if (!id) return;

      try {
        setLoading(true);
        setError(null);
        const data = await communityService.getBySlug(id);
        if (isMounted) {
          setCommunity(data);
          // Load community posts
          const communityPosts = await postService.getCommunityPosts(data.id);
          setPosts(communityPosts);
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err.response?.data?.detail || 'Failed to load community');
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    loadCommunity();

    return () => {
      isMounted = false;
    };
  }, [id]);

  const handleCreatePost = async () => {
    if (!community || !user) return;
    
    try {
      const postData: Omit<Post, 'id' | 'created_at'> = {
        title: newPost.title,
        content: newPost.content,
        community_id: community.id,
        author_id: Number(user.id),
        updated_at: new Date().toISOString(),
        likes_count: 0,
        comments_count: 0,
        author_name: user.name,
        is_announcement: false,
        is_liked: false
      };
      
      const createdPost = await postService.createPost(postData);
      setPosts([createdPost, ...posts]);
      setNewPost({ title: '', content: '' });
    } catch (err) {
      setError('Failed to create post');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
          <p className="text-gray-600">Loading community...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-4">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
          <strong className="font-bold">Error!</strong>
          <span className="block sm:inline"> {error}</span>
        </div>
      </div>
    );
  }

  if (!community) {
    return (
      <div className="container mx-auto p-4">
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded relative">
          Community not found
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h1 className="text-2xl font-bold mb-2">{community.name}</h1>
        <p className="text-gray-600 mb-4">{community.description}</p>
        <div className="flex items-center text-sm text-gray-500">
          <span>{community.members_count} members</span>
          {community.is_member ? (
            <button
              onClick={() => communityService.leave(community.id)}
              className="ml-4 text-red-600 hover:text-red-800"
            >
              Leave Community
            </button>
          ) : (
            <button
              onClick={() => communityService.join(community.id)}
              className="ml-4 text-blue-600 hover:text-blue-800"
            >
              Join Community
            </button>
          )}
        </div>
      </div>

      {/* Create Post Form */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <form onSubmit={handleCreatePost}>
          <div className="mb-4">
            <input
              type="text"
              value={newPost.title}
              onChange={(e) => setNewPost({ ...newPost, title: e.target.value })}
              placeholder="Post title"
              className="w-full p-2 border rounded-lg mb-4"
              required
            />
          </div>
          <textarea
            value={newPost.content}
            onChange={(e) => setNewPost({ ...newPost, content: e.target.value })}
            placeholder="Write a post..."
            className="w-full p-2 border rounded-lg mb-4"
            rows={4}
            required
          />
          {error && (
            <div className="mb-4 text-red-600">
              {error}
            </div>
          )}
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Post
          </button>
        </form>
      </div>

      {/* Posts List */}
      <div className="space-y-4">
        {posts.map((post) => (
          <div key={post.id} className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-2">{post.title}</h3>
            <p className="text-gray-800">{post.content}</p>
            <div className="mt-2 text-sm text-gray-500">
              Posted by {post.author_name} on {new Date(post.created_at).toLocaleDateString()}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}; 