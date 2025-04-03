import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { postService, Post } from '../../services/postService'

export default function MyPosts() {
  const navigate = useNavigate()
  const { user } = useAuth()
  const [posts, setPosts] = useState<Post[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string>('')

  useEffect(() => {
    const loadPosts = async () => {
      try {
        if (user?.id) {
          const userPosts = await postService.getUserPosts(user.id)
          setPosts(userPosts)
        }
      } catch (err: any) {
        setError(err.message || 'Failed to load posts')
      } finally {
        setIsLoading(false)
      }
    }

    loadPosts()
  }, [user?.id])

  return (
    <div className="min-h-screen bg-gray-100 py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-semibold text-gray-900">My Posts</h1>
          <button
            onClick={() => navigate('/posts/create')}
            className="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700"
          >
            Create New Post
          </button>
        </div>

        {error && (
          <div className="bg-red-50 p-4 rounded-md mb-6">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}

        {isLoading ? (
          <div className="text-center py-12">
            <p className="text-gray-500">Loading posts...</p>
          </div>
        ) : posts.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-gray-500">You haven't created any posts yet.</p>
            <button
              onClick={() => navigate('/posts/create')}
              className="mt-4 text-indigo-600 hover:text-indigo-500"
            >
              Create your first post
            </button>
          </div>
        ) : (
          <div className="space-y-6">
            {posts.map(post => (
              <div key={post.id} className="bg-white shadow rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">
                    {post.title}
                  </h2>
                  {post.isAnnouncement && (
                    <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">
                      Announcement
                    </span>
                  )}
                </div>
                <p className="text-gray-600 mb-4">{post.content}</p>
                <div className="flex justify-between items-center text-sm text-gray-500">
                  <span>Posted on {new Date(post.createdAt).toLocaleDateString()}</span>
                  <div className="space-x-4">
                    <button className="text-indigo-600 hover:text-indigo-500">Edit</button>
                    <button className="text-red-600 hover:text-red-500">Delete</button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}