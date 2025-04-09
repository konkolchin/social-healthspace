import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { postService } from '../../services/postService'
import { communityService } from '../../services/communityService'

interface PostFormData {
  title: string
  content: string
  isAnnouncement: boolean
  communityId?: number
}

interface Community {
  id: number
  name: string
  slug: string
}

export default function CreatePost() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [formData, setFormData] = useState<PostFormData>({
    title: '',
    content: '',
    isAnnouncement: false
  })
  const [communities, setCommunities] = useState<Community[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string>('')

  useEffect(() => {
    const fetchCommunities = async () => {
      try {
        const data = await communityService.list()
        console.log('Fetched communities:', data) // Debug log
        setCommunities(data)
      } catch (err) {
        console.error('Error fetching communities:', err)
        setError('Failed to load communities. Please try again later.')
      }
    }
    fetchCommunities()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      if (!user) throw new Error('User not authenticated')

      const postData = {
        title: formData.title,
        content: formData.content,
        is_announcement: formData.isAnnouncement,
        author_id: Number(user.id),
        community_id: formData.communityId,
        updated_at: new Date().toISOString(),
        likes_count: 0,
        comments_count: 0
      }

      console.log('Creating post with data:', postData) // Debug log
      await postService.createPost(postData)
      navigate('/posts/my-posts')
    } catch (err: any) {
      console.error('Error creating post:', err) // Debug log
      setError(err.message || 'Failed to create post')
    } finally {
      setIsLoading(false)
    }
  }

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' 
        ? (e.target as HTMLInputElement).checked 
        : name === 'communityId' 
          ? value ? Number(value) : undefined 
          : value
    }))
  }

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="relative px-4 py-10 bg-white mx-8 md:mx-0 shadow rounded-3xl sm:p-10">
          <div className="max-w-md mx-auto">
            <div className="divide-y divide-gray-200">
              <div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                <h2 className="text-2xl font-bold mb-8 text-center text-gray-900">Create New Post</h2>
                
                {error && (
                  <div className="bg-red-50 p-4 rounded-md mb-6">
                    <p className="text-sm text-red-600">{error}</p>
                  </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-6">
                  <div>
                    <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                      Title
                    </label>
                    <input
                      type="text"
                      id="title"
                      name="title"
                      required
                      value={formData.title}
                      onChange={handleChange}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                      placeholder="Enter post title"
                    />
                  </div>

                  <div>
                    <label htmlFor="content" className="block text-sm font-medium text-gray-700">
                      Content
                    </label>
                    <textarea
                      id="content"
                      name="content"
                      required
                      rows={5}
                      value={formData.content}
                      onChange={handleChange}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                      placeholder="Write your post content here..."
                    />
                  </div>

                  <div>
                    <label htmlFor="communityId" className="block text-sm font-medium text-gray-700">
                      Community (optional)
                    </label>
                    <select
                      id="communityId"
                      name="communityId"
                      value={formData.communityId || ''}
                      onChange={handleChange}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                    >
                      <option value="">Select a community</option>
                      {communities.map(community => (
                        <option key={community.id} value={community.id}>
                          {community.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id="isAnnouncement"
                      name="isAnnouncement"
                      checked={formData.isAnnouncement}
                      onChange={handleChange}
                      className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                    />
                    <label htmlFor="isAnnouncement" className="ml-2 block text-sm text-gray-700">
                      Mark as announcement
                    </label>
                  </div>

                  <div className="flex gap-4">
                    <button
                      type="button"
                      onClick={() => navigate('/dashboard')}
                      className="flex-1 bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      disabled={isLoading}
                      className="flex-1 bg-indigo-600 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-400"
                    >
                      {isLoading ? 'Creating...' : 'Create Post'}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}