import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import LoginRegister from './pages/LoginRegister'
import RestaurantListing from './pages/RestaurantListing'
import RestaurantDetail from './pages/RestaurantDetail'
import OwnerDashboard from './pages/OwnerDashboard'
import AdminDashboard from './pages/AdminDashboard'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/auth" element={<LoginRegister />} />
            <Route path="/restaurants" element={<RestaurantListing />} />
            <Route path="/restaurants/:id" element={<RestaurantDetail />} />
            <Route 
              path="/owner/dashboard" 
              element={
                <ProtectedRoute roles={['owner', 'admin']}>
                  <OwnerDashboard />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/admin/dashboard" 
              element={
                <ProtectedRoute roles={['admin']}>
                  <AdminDashboard />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App