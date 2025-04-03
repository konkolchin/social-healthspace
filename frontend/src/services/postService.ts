export interface Post {
  id: string
  title: string
  content: string
  isAnnouncement: boolean
  authorId: string
  authorName: string
  createdAt: string
}

const getPosts = (): Post[] => {
  const posts = localStorage.getItem('posts')
  return posts ? JSON.parse(posts) : []
}

const storePosts = (posts: Post[]) => {
  localStorage.setItem('posts', JSON.stringify(posts))
}

export const postService = {
  async createPost(post: Omit<Post, 'id' | 'createdAt'>): Promise<Post> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000))

    const newPost: Post = {
      ...post,
      id: 'post-' + Date.now(),
      createdAt: new Date().toISOString()
    }

    const posts = getPosts()
    posts.push(newPost)
    storePosts(posts)

    return newPost
  },

  async getUserPosts(userId: string): Promise<Post[]> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500))

    const posts = getPosts()
    return posts
      .filter(post => post.authorId === userId)
      .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
  },

  async getAllPosts(): Promise<Post[]> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500))

    const posts = getPosts()
    return posts.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
  }
}