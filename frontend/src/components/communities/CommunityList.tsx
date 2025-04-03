import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { communityService } from '../../services/communityService';
import type { Community } from '../../types/community';

export const CommunityList: React.FC = () => {
  const [communities, setCommunities] = useState<Community[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadCommunities();
  }, []);

  const loadCommunities = async () => {
    try {
      setLoading(true);
      setError(null);
      console.log('Starting to fetch communities...'); // Debug log
      const data = await communityService.list();
      console.log('Received communities:', data); // Debug log
      setCommunities(data);
    } catch (err: any) {
      console.error('Error details:', err); // Debug log
      setError(err.response?.data?.detail || 'Failed to load communities');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
          <p className="text-gray-600">Loading communities...</p>
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
          <button
            onClick={loadCommunities}
            className="mt-2 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Communities</h1>
        <button
          onClick={() => navigate('/communities/new')}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
        >
          Create Community
        </button>
      </div>

      {communities.length === 0 ? (
        <div className="text-center bg-gray-50 rounded-lg p-8">
          <h2 className="text-xl font-semibold mb-2">No Communities Yet</h2>
          <p className="text-gray-600 mb-4">
            Be the first to create a community and start connecting with others!
          </p>
          <button
            onClick={() => navigate('/communities/new')}
            className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Create Your First Community
          </button>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {communities.map((community) => (
            <div 
              key={community.id} 
              className="border rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow bg-white"
            >
              <h2 className="text-xl font-semibold mb-2">{community.name}</h2>
              <p className="text-gray-600 mb-4 line-clamp-2">{community.description}</p>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-500">
                  {community.members_count} {community.members_count === 1 ? 'member' : 'members'}
                </span>
                <button
                  onClick={() => navigate(`/communities/${community.slug}`)}
                  className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
                >
                  View
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
