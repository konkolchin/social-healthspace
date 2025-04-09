import React from 'react';
import { useAuth } from '../../context/AuthContext';

const Profile: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-2xl font-bold mb-4">Profile</h2>
      <div className="space-y-4">
        <div>
          <p className="text-gray-600">Email: {user?.email}</p>
        </div>
        <div>
          <p className="text-gray-600">Name: {user?.name}</p>
        </div>
      </div>
    </div>
  );
};

export default Profile; 