import React, { useEffect, useState } from 'react'
import { useAuth } from '../../context/AuthContext'
import { postService } from '../../services/postService'
import type { Post } from '../../types/community'
import { Link } from 'react-router-dom'

const MyPosts: React.FC = () => {
  const { user } = useAuth()
  const [posts, setPosts] = useState<Post[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchPosts = async () => {
      if (!user) return
      try {
        setLoading(true)
        const data = await postService.getUserPosts(user.id.toString())
        console.log('Posts data:', JSON.stringify(data, null, 2))
        setPosts(data)
        setError(null)
      } catch (err) {
        console.error('Error fetching posts:', err)
        setError('Failed to load posts. Please try again later.')
      } finally {
        setLoading(false)
      }
    }

    fetchPosts()
  }, [user])

  const handleDelete = async (postId: number) => {
    if (!window.confirm('Are you sure you want to delete this post?')) return
    try {
      await postService.deletePost(postId.toString())
      setPosts(posts.filter(post => post.id !== postId))
    } catch (err) {
      console.error('Error deleting post:', err)
      setError('Failed to delete post. Please try again later.')
    }
  }

  if (loading) return <div>Loading...</div>
  if (error) return <div className="text-red-500">{error}</div>

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">My Posts</h1>
        <Link
          to="/create-post"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Create New Post
        </Link>
      </div>
      {posts.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-500 mb-4">You haven't created any posts yet.</p>
          <Link
            to="/create-post"
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Create Your First Post
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {posts.map((post) => {
            console.log('Post data:', JSON.stringify(post, null, 2))
            return (
              <div key={post.id} className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h2 className="text-xl font-semibold mb-2">{post.title}</h2>
                    <p className="text-gray-600 mb-4">{post.content}</p>
                    {post.community_id ? (
                      <div className="mb-2">
                        <span className="text-sm text-gray-500">Posted in: </span>
                        {post.community ? (
                          <Link
                            to={`/communities/${post.community.slug}`}
                            className="text-blue-500 hover:underline"
                          >
                            {post.community.name}
                          </Link>
                        ) : (
                          <span className="text-blue-500">Community #{post.community_id}</span>
                        )}
                      </div>
                    ) : (
                      <div className="mb-2">
                        <span className="text-sm text-gray-500">Standalone post</span>
                      </div>
                    )}
                    <div className="text-sm text-gray-500">
                      Posted on {new Date(post.created_at).toLocaleDateString()}
                    </div>
                  </div>
                  <div className="flex flex-col items-end space-y-2">
                    <div className="flex space-x-2">
                      <span className="text-gray-500">
                        {post.likes_count} likes
                      </span>
                      <span className="text-gray-500">
                        {post.comments_count} comments
                      </span>
                    </div>
                    <div className="flex space-x-2">
                      <Link
                        to={`/posts/${post.id}/edit`}
                        className="text-blue-500 hover:text-blue-700"
                      >
                        Edit
                      </Link>
                      <button
                        onClick={() => handleDelete(post.id)}
                        className="text-red-500 hover:text-red-700"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default MyPosts