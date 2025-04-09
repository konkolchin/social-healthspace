import { Routes, Route, Navigate } from 'react-router-dom'
import LoginForm from './components/auth/LoginForm'
import RegisterForm from './components/auth/RegisterForm'
import Dashboard from './components/dashboard/Dashboard'
import CreatePost from './components/posts/CreatePost'
import MyPosts from './components/posts/MyPosts'
import PostsList from './components/posts/PostsList'
import ProtectedRoute from './components/auth/ProtectedRoute'
import { CommunityList } from './components/communities/CommunityList'
import { CreateCommunity } from './components/communities/CreateCommunity'
import { CommunityDetail } from './components/communities/CommunityDetail'
import Profile from './components/profile/Profile'

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginForm />} />
      <Route path="/register" element={<RegisterForm />} />
      
      {/* Public Routes */}
      <Route path="/posts" element={<PostsList />} />
      
      {/* Community Routes */}
      <Route 
        path="/communities" 
        element={
          <ProtectedRoute>
            <CommunityList />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/communities/new" 
        element={
          <ProtectedRoute>
            <CreateCommunity />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/communities/:slug" 
        element={
          <ProtectedRoute>
            <CommunityDetail />
          </ProtectedRoute>
        } 
      />
      
      <Route 
        path="/dashboard" 
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/posts/create" 
        element={
          <ProtectedRoute>
            <CreatePost />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/posts/my" 
        element={
          <ProtectedRoute>
            <MyPosts />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/profile" 
        element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        } 
      />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}