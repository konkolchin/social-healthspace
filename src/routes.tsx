import { Routes, Route } from 'react-router-dom'
import TestPage from './TestPage'
import { CommunityList } from './components/communities/CommunityList';
import { CreateCommunity } from './components/communities/CreateCommunity';

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="*" element={<TestPage />} />
      <Route path="/communities" element={<CommunityList />} />
      <Route path="/communities/new" element={<CreateCommunity />} />
    </Routes>
  )
} 