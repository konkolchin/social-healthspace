import { useAuth } from '../../context/AuthContext'
import { useNavigate } from 'react-router-dom'

export default function Dashboard() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold">Social HealthSpace</h1>
            </div>
            <div className="flex items-center">
              <span className="text-gray-700 mr-4">Welcome, {user?.name}</span>
              <button
                onClick={handleLogout}
                className="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Quick Actions Card */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-6">
                <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
                <div className="mt-6 space-y-4">
                  <button 
                    onClick={() => navigate('/posts/create')} 
                    className="w-full bg-indigo-50 text-indigo-600 px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-100"
                  >
                    Create New Post
                  </button>
                  <button 
                    onClick={() => navigate('/posts/my')} 
                    className="w-full bg-indigo-50 text-indigo-600 px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-100"
                  >
                    View My Posts
                  </button>
                  <button 
                    onClick={() => navigate('/communities')} 
                    className="w-full bg-indigo-50 text-indigo-600 px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-100"
                  >
                    Browse Communities
                  </button>
                </div>
              </div>
            </div>

            {/* Profile Summary Card */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-6">
                <h3 className="text-lg font-medium text-gray-900">Profile Summary</h3>
                <dl className="mt-6 space-y-4">
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Email</dt>
                    <dd className="mt-1 text-sm text-gray-900">{user?.email}</dd>
                  </div>
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Member Since</dt>
                    <dd className="mt-1 text-sm text-gray-900">{new Date().toLocaleDateString()}</dd>
                  </div>
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Status</dt>
                    <dd className="mt-1 text-sm text-gray-900">Active</dd>
                  </div>
                </dl>
              </div>
            </div>

            {/* Activity Summary Card */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-6">
                <h3 className="text-lg font-medium text-gray-900">Activity Summary</h3>
                <dl className="mt-6 space-y-4">
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Total Posts</dt>
                    <dd className="mt-1 text-sm text-gray-900">0</dd>
                  </div>
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Comments</dt>
                    <dd className="mt-1 text-sm text-gray-900">0</dd>
                  </div>
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Last Activity</dt>
                    <dd className="mt-1 text-sm text-gray-900">Just now</dd>
                  </div>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}