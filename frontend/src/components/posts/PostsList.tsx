import React, { useEffect, useState } from 'react'
import { postService } from '../../services/postService'
import type { Post } from '../../types/community'
import { Link } from 'react-router-dom'

const PostsList: React.FC = () => {
  const [posts, setPosts] = useState<Post[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setLoading(true)
        const data = await postService.getAllPosts()
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
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div className="text-red-500">{error}</div>

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">All Posts</h1>
      {posts.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-500">No posts found.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {posts.map((post) => (
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
                    Posted by {post.author_name || 'Anonymous'} on {new Date(post.created_at).toLocaleDateString()}
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
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default PostsList 