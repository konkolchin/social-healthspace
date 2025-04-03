import { Routes, Route, Navigate } from 'react-router-dom'
import LoginForm from './components/auth/LoginForm'
import RegisterForm from './components/auth/RegisterForm'
import Dashboard from './components/dashboard/Dashboard'
import CreatePost from './components/posts/CreatePost'
import MyPosts from './components/posts/MyPosts'
import ProtectedRoute from './components/auth/ProtectedRoute'
import { CommunityList } from './components/communities/CommunityList'
import { CreateCommunity } from './components/communities/CreateCommunity'

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginForm />} />
      <Route path="/register" element={<RegisterForm />} />
      
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
        path="/posts/my-posts" 
        element={
          <ProtectedRoute>
            <MyPosts />
          </ProtectedRoute>
        } 
      />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}