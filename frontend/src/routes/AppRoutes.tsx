import { Routes, Route } from 'react-router-dom'
import { ProtectedRoute } from '../components/ProtectedRoute'
import { Home } from '../pages/Home'
import { Login } from '../pages/Login'
import { Register } from '../pages/Register'
import { Profile } from '../pages/Profile'
import { Community } from '../pages/Community'
import { NotFound } from '../pages/NotFound'

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        }
      />
      <Route path="/community/:id" element={<Community />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
} 