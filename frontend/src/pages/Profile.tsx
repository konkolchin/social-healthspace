export const Profile = () => {
  return (
    <div className="max-w-2xl mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Profile</h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Name</label>
          <p className="mt-1 text-gray-900">John Doe</p>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Email</label>
          <p className="mt-1 text-gray-900">john@example.com</p>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Bio</label>
          <p className="mt-1 text-gray-900">
            Health enthusiast and fitness coach with 10 years of experience.
          </p>
        </div>
      </div>
    </div>
  )
} 