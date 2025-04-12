import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from './context/AuthContext'
import { Navbar } from './components/Navbar';
import AppRoutes from './routes/AppRoutes'

const queryClient = new QueryClient()

function App() {
  return (
    <BrowserRouter basename="/">
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <div className="min-h-screen bg-gray-100">
            <Navbar />
            <main className="container mx-auto px-4 py-8">
              <AppRoutes />
            </main>
          </div>
        </AuthProvider>
      </QueryClientProvider>
    </BrowserRouter>
  )
}

export default App