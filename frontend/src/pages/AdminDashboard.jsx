import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { CheckCircle, XCircle, Eye, Users, Clock, Star, Shield, AlertTriangle } from 'lucide-react'
import { adminApi, restaurantApi } from '../services/api'

const AdminDashboard = () => {
  const [pendingRestaurants, setPendingRestaurants] = useState([])
  const [users, setUsers] = useState([])
  const [allRestaurants, setAllRestaurants] = useState([])
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState({})
  const [activeTab, setActiveTab] = useState('pending')

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [pendingRes, usersRes, allRes] = await Promise.all([
        adminApi.getPendingRestaurants(),
        adminApi.getUsers(),
        restaurantApi.getAll({ limit: 100 })
      ])
      
      setPendingRestaurants(pendingRes.data)
      setUsers(usersRes.data)
      setAllRestaurants(allRes.data)
    } catch (error) {
      console.error('Error loading admin data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleApproveRestaurant = async (restaurantId) => {
    setActionLoading({ ...actionLoading, [restaurantId]: 'approving' })
    try {
      await adminApi.approveRestaurant(restaurantId)
      setPendingRestaurants(pendingRestaurants.filter(r => r.id !== restaurantId))
      // Refresh all restaurants to update the stats
      const allRes = await restaurantApi.getAll({ limit: 100 })
      setAllRestaurants(allRes.data)
    } catch (error) {
      console.error('Error approving restaurant:', error)
      alert('Failed to approve restaurant. Please try again.')
    } finally {
      setActionLoading({ ...actionLoading, [restaurantId]: null })
    }
  }

  const handleRejectRestaurant = async (restaurantId) => {
    setActionLoading({ ...actionLoading, [restaurantId]: 'rejecting' })
    try {
      await adminApi.rejectRestaurant(restaurantId)
      setPendingRestaurants(pendingRestaurants.filter(r => r.id !== restaurantId))
      // Refresh all restaurants to update the stats
      const allRes = await restaurantApi.getAll({ limit: 100 })
      setAllRestaurants(allRes.data)
    } catch (error) {
      console.error('Error rejecting restaurant:', error)
      alert('Failed to reject restaurant. Please try again.')
    } finally {
      setActionLoading({ ...actionLoading, [restaurantId]: null })
    }
  }

  const getSafetyBadgeClass = (rating) => {
    switch (rating?.toLowerCase()) {
      case 'excellent': return 'badge-excellent'
      case 'good': return 'badge-good'
      case 'fair': return 'badge-fair'
      case 'poor': return 'badge-poor'
      default: return 'badge-fair'
    }
  }

  const getRoleBadgeClass = (role) => {
    switch (role?.toLowerCase()) {
      case 'admin': return 'bg-purple-100 text-purple-800'
      case 'owner': return 'bg-blue-100 text-blue-800'
      case 'customer': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const stats = {
    totalUsers: users.length,
    totalRestaurants: allRestaurants.length,
    pendingApprovals: pendingRestaurants.length,
    approvedRestaurants: allRestaurants.filter(r => r.approval_status === 'Approved').length,
    avgSafetyScore: allRestaurants.length > 0 
      ? Math.round(allRestaurants.reduce((sum, r) => sum + r.safety_score, 0) / allRestaurants.length)
      : 0
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-safebite-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
          <p className="text-gray-600">Manage restaurant approvals and system overview</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
          <div className="card p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Users className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">{stats.totalUsers}</p>
                <p className="text-gray-600">Total Users</p>
              </div>
            </div>
          </div>
          <div className="card p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <Star className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">{stats.totalRestaurants}</p>
                <p className="text-gray-600">Restaurants</p>
              </div>
            </div>
          </div>
          <div className="card p-6">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <Clock className="w-6 h-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">{stats.pendingApprovals}</p>
                <p className="text-gray-600">Pending</p>
              </div>
            </div>
          </div>
          <div className="card p-6">
            <div className="flex items-center">
              <div className="p-2 bg-safebite-100 rounded-lg">
                <Shield className="w-6 h-6 text-safebite-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">{stats.approvedRestaurants}</p>
                <p className="text-gray-600">Approved</p>
              </div>
            </div>
          </div>
          <div className="card p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Star className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">{stats.avgSafetyScore}</p>
                <p className="text-gray-600">Avg Safety</p>
              </div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-8">
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab('pending')}
              className={`px-6 py-4 font-medium text-sm ${
                activeTab === 'pending'
                  ? 'text-safebite-600 border-b-2 border-safebite-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              Pending Approvals ({stats.pendingApprovals})
            </button>
            <button
              onClick={() => setActiveTab('users')}
              className={`px-6 py-4 font-medium text-sm ${
                activeTab === 'users'
                  ? 'text-safebite-600 border-b-2 border-safebite-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              User Management ({stats.totalUsers})
            </button>
            <button
              onClick={() => setActiveTab('restaurants')}
              className={`px-6 py-4 font-medium text-sm ${
                activeTab === 'restaurants'
                  ? 'text-safebite-600 border-b-2 border-safebite-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              All Restaurants ({stats.totalRestaurants})
            </button>
          </div>

          <div className="p-6">
            {/* Pending Approvals Tab */}
            {activeTab === 'pending' && (
              <div>
                {pendingRestaurants.length === 0 ? (
                  <div className="text-center py-8">
                    <CheckCircle size={48} className="mx-auto text-green-400 mb-4" />
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">All caught up!</h3>
                    <p className="text-gray-600">No restaurants pending approval at the moment.</p>
                  </div>
                ) : (
                  <div className="space-y-6">
                    {pendingRestaurants.map((restaurant) => (
                      <div key={restaurant.id} className="bg-gray-50 rounded-lg p-6 border border-gray-200">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-4 mb-4">
                              <img
                                src={restaurant.images?.[0]?.image_url || 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=100&q=80'}
                                alt={restaurant.name}
                                className="w-16 h-16 rounded-lg object-cover"
                              />
                              <div>
                                <h3 className="text-lg font-semibold text-gray-900">{restaurant.name}</h3>
                                <p className="text-safebite-600 font-medium">{restaurant.cuisine}</p>
                                <p className="text-gray-600 text-sm">{restaurant.city}, {restaurant.state}</p>
                              </div>
                            </div>
                            
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                              <div>
                                <span className="text-sm font-medium text-gray-700">Safety Score</span>
                                <div className="flex items-center space-x-2 mt-1">
                                  <span className="text-lg font-bold text-gray-900">{restaurant.safety_score}</span>
                                  <span className={getSafetyBadgeClass(restaurant.safety_rating)}>
                                    {restaurant.safety_rating}
                                  </span>
                                </div>
                              </div>
                              <div>
                                <span className="text-sm font-medium text-gray-700">License</span>
                                <p className="text-gray-900 font-mono text-sm mt-1">{restaurant.license_number}</p>
                                <p className="text-gray-600 text-xs">{restaurant.license_status}</p>
                              </div>
                              <div>
                                <span className="text-sm font-medium text-gray-700">Contact</span>
                                <p className="text-gray-900 text-sm mt-1">{restaurant.phone}</p>
                                <p className="text-gray-600 text-xs">{restaurant.email}</p>
                              </div>
                            </div>

                            {restaurant.description && (
                              <div className="mb-4">
                                <span className="text-sm font-medium text-gray-700">Description</span>
                                <p className="text-gray-600 text-sm mt-1 line-clamp-2">{restaurant.description}</p>
                              </div>
                            )}
                          </div>

                          <div className="flex flex-col space-y-2 ml-6">
                            <Link
                              to={`/restaurants/${restaurant.id}`}
                              className="flex items-center space-x-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
                            >
                              <Eye size={16} />
                              <span>View Details</span>
                            </Link>
                            
                            <button
                              onClick={() => handleApproveRestaurant(restaurant.id)}
                              disabled={actionLoading[restaurant.id]}
                              className="flex items-center space-x-2 px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 disabled:opacity-50"
                            >
                              {actionLoading[restaurant.id] === 'approving' ? (
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                              ) : (
                                <CheckCircle size={16} />
                              )}
                              <span>Approve</span>
                            </button>
                            
                            <button
                              onClick={() => handleRejectRestaurant(restaurant.id)}
                              disabled={actionLoading[restaurant.id]}
                              className="flex items-center space-x-2 px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 disabled:opacity-50"
                            >
                              {actionLoading[restaurant.id] === 'rejecting' ? (
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                              ) : (
                                <XCircle size={16} />
                              )}
                              <span>Reject</span>
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Users Tab */}
            {activeTab === 'users' && (
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">User</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Role</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Email</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Joined</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map((user) => (
                      <tr key={user.id} className="border-b border-gray-100 hover:bg-gray-50">
                        <td className="py-3 px-4">
                          <div className="flex items-center">
                            <div className="w-8 h-8 bg-safebite-100 rounded-full flex items-center justify-center mr-3">
                              <span className="text-safebite-600 font-semibold text-sm">
                                {user.full_name.split(' ').map(n => n[0]).join('')}
                              </span>
                            </div>
                            <span className="font-medium text-gray-900">{user.full_name}</span>
                          </div>
                        </td>
                        <td className="py-3 px-4">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRoleBadgeClass(user.role)}`}>
                            {user.role}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-gray-600">{user.email}</td>
                        <td className="py-3 px-4 text-gray-600">
                          {new Date(user.created_at).toLocaleDateString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* All Restaurants Tab */}
            {activeTab === 'restaurants' && (
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Restaurant</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Cuisine</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Location</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Safety Score</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Status</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-700">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {allRestaurants.map((restaurant) => (
                      <tr key={restaurant.id} className="border-b border-gray-100 hover:bg-gray-50">
                        <td className="py-3 px-4">
                          <div className="flex items-center">
                            <img
                              src={restaurant.images?.[0]?.image_url || 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=40&q=80'}
                              alt={restaurant.name}
                              className="w-10 h-10 rounded-lg object-cover mr-3"
                            />
                            <span className="font-medium text-gray-900">{restaurant.name}</span>
                          </div>
                        </td>
                        <td className="py-3 px-4 text-gray-600">{restaurant.cuisine}</td>
                        <td className="py-3 px-4 text-gray-600">{restaurant.city}, {restaurant.state}</td>
                        <td className="py-3 px-4">
                          <div className="flex items-center space-x-2">
                            <span className="font-semibold text-gray-900">{restaurant.safety_score}</span>
                            <span className={getSafetyBadgeClass(restaurant.safety_rating)}>
                              {restaurant.safety_rating}
                            </span>
                          </div>
                        </td>
                        <td className="py-3 px-4">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                            restaurant.approval_status === 'Approved' ? 'status-approved' :
                            restaurant.approval_status === 'Pending' ? 'status-pending' :
                            'status-rejected'
                          }`}>
                            {restaurant.approval_status}
                          </span>
                        </td>
                        <td className="py-3 px-4">
                          <Link
                            to={`/restaurants/${restaurant.id}`}
                            className="text-safebite-600 hover:text-safebite-700 font-medium text-sm"
                          >
                            View
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard