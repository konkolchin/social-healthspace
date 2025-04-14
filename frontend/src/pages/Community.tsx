import { useParams } from 'react-router-dom'

export const Community = () => {
  const { id } = useParams()

  return (
    <div className="max-w-4xl mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Community: {id}</h2>
      <div className="space-y-4">
        <div className="border-b pb-4">
          <h3 className="text-lg font-semibold mb-2">About this Community</h3>
          <p className="text-gray-600">
            This is a community for health professionals and enthusiasts to share knowledge and experiences.
          </p>
        </div>
        <div>
          <h3 className="text-lg font-semibold mb-2">Recent Posts</h3>
          <div className="space-y-4">
            <div className="p-4 border rounded-lg">
              <h4 className="font-medium">Post Title</h4>
              <p className="text-gray-600">Post content goes here...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 