import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { communityService } from '../../services/communityService';

export const CreateCommunity: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    is_private: false
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const community = await communityService.create(formData);
      navigate(`/communities/${community.slug}`);
    } catch (error) {
      console.error('Failed to create community:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-lg mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Create Community</h1>
      
      <div>
        <label className="block text-sm font-medium text-gray-700">
          Name
        </label>
        <input
          type="text"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">
          Description
        </label>
        <textarea
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          rows={4}
        />
      </div>

      <div className="flex items-center">
        <input
          type="checkbox"
          checked={formData.is_private}
          onChange={(e) => setFormData({ ...formData, is_private: e.target.checked })}
          className="rounded border-gray-300 text-blue-600"
        />
        <label className="ml-2 text-sm text-gray-700">
          Make this community private
        </label>
      </div>

      <div className="flex justify-end space-x-3">
        <button
          type="button"
          onClick={() => navigate('/communities')}
          className="px-4 py-2 border rounded text-gray-700 hover:bg-gray-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Create Community
        </button>
      </div>
    </form>
  );
};
