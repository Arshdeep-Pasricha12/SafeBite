import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { User, LogOut, Shield, Store } from 'lucide-react'

const Navbar = () => {
  const { user, logout, isAuthenticated, isAdmin, isOwner } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  const isActive = (path) => location.pathname === path

  return (
    <nav className="bg-white shadow-lg border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-safebite-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">S</span>
            </div>
            <span className="text-xl font-bold text-gray-800">SafeBite</span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            <Link 
              to="/restaurants" 
              className={`font-medium transition-colors duration-200 ${
                isActive('/restaurants') 
                  ? 'text-safebite-600' 
                  : 'text-gray-600 hover:text-safebite-600'
              }`}
            >
              Restaurants
            </Link>
            
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                {isOwner && (
                  <Link 
                    to="/owner/dashboard"
                    className={`flex items-center space-x-2 font-medium transition-colors duration-200 ${
                      isActive('/owner/dashboard')
                        ? 'text-safebite-600'
                        : 'text-gray-600 hover:text-safebite-600'
                    }`}
                  >
                    <Store size={18} />
                    <span>My Restaurants</span>
                  </Link>
                )}
                
                {isAdmin && (
                  <Link 
                    to="/admin/dashboard"
                    className={`flex items-center space-x-2 font-medium transition-colors duration-200 ${
                      isActive('/admin/dashboard')
                        ? 'text-safebite-600'
                        : 'text-gray-600 hover:text-safebite-600'
                    }`}
                  >
                    <Shield size={18} />
                    <span>Admin</span>
                  </Link>
                )}

                <div className="flex items-center space-x-2 text-gray-700">
                  <User size={18} />
                  <span className="font-medium">{user.full_name}</span>
                </div>

                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-2 text-gray-600 hover:text-red-600 transition-colors duration-200"
                >
                  <LogOut size={18} />
                  <span>Logout</span>
                </button>
              </div>
            ) : (
              <Link 
                to="/auth" 
                className="btn-primary"
              >
                Sign In
              </Link>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            {isAuthenticated ? (
              <button
                onClick={handleLogout}
                className="text-gray-600 hover:text-red-600 transition-colors duration-200"
              >
                <LogOut size={24} />
              </button>
            ) : (
              <Link to="/auth" className="btn-primary text-sm px-4 py-2">
                Sign In
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar