import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Plus, Edit, Trash2, Star, MapPin, Clock, Eye, AlertCircle } from 'lucide-react'
import { restaurantApi } from '../services/api'
import { useAuth } from '../context/AuthContext'
import CreateRestaurantModal from '../components/CreateRestaurantModal'

const OwnerDashboard = () => {
  const { user } = useAuth()
  const [restaurants, setRestaurants] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadRestaurants()
  }, [])

  const loadRestaurants = async () => {
    try {
      setLoading(true)
      const response = await restaurantApi.getAll({ owned: true })
      setRestaurants(response.data)
    } catch (err) {
      console.error('Error loading restaurants:', err)
      setError('Failed to load your restaurants')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteRestaurant = async (restaurantId, restaurantName) => {
    if (window.confirm(`Are you sure you want to delete "${restaurantName}"? This action cannot be undone.`)) {
      try {
        await restaurantApi.delete(restaurantId)
        setRestaurants(restaurants.filter(r => r.id !== restaurantId))
      } catch (err) {
        console.error('Error deleting restaurant:', err)
        alert('Failed to delete restaurant. Please try again.')
      }
    }
  }

  const getStatusBadgeClass = (status) => {
    switch (status?.toLowerCase()) {
      case 'approved': return 'status-approved'
      case 'pending': return 'status-pending'
      case 'rejected': return 'status-rejected'
      default: return 'status-pending'
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

  const stats = {
    total: restaurants.length,
    approved: restaurants.filter(r => r.approval_status === 'Approved').length,
    pending: restaurants.filter(r => r.approval_status === 'Pending').length,
    rejected: restaurants.filter(r => r.approval_status === 'Rejected').length
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
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Restaurant Management</h1>
          <p className="text-gray-600">Manage your restaurant listings and track approval status</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Star className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
                <p className="text-gray-600">Total Restaurants</p>
              </div>
            </div>
          </div>
          <div className="card p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <Eye className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">{stats.approved}</p>
                <p className="text-gray-600">Approved</p>
              </div>
            </div>
          </div>
          <div className="card p-6">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <Clock className="w-6 h-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">{stats.pending}</p>
                <p className="text-gray-600">Pending</p>
              </div>
            </div>
          </div>
          <div className="card p-6">
            <div className="flex items-center">
              <div className="p-2 bg-red-100 rounded-lg">
                <AlertCircle className="w-6 h-6 text-red-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">{stats.rejected}</p>
                <p className="text-gray-600">Rejected</p>
              </div>
            </div>
          </div>
        </div>

        {/* Action Bar */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-gray-900">Your Restaurants</h2>
          <button
            onClick={() => setShowCreateModal(true)}
            className="btn-primary flex items-center space-x-2"
          >
            <Plus size={20} />
            <span>Add Restaurant</span>
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Restaurant List */}
        {restaurants.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <Star size={64} className="mx-auto" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No restaurants yet</h3>
            <p className="text-gray-600 mb-6">Create your first restaurant listing to get started</p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="btn-primary"
            >
              Create Restaurant
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {restaurants.map((restaurant) => (
              <div key={restaurant.id} className="card">
                <div className="relative">
                  <img
                    src={restaurant.images?.[0]?.image_url || 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80'}
                    alt={restaurant.name}
                    className="w-full h-48 object-cover rounded-t-xl"
                  />
                  <div className="absolute top-4 right-4">
                    <span className={getStatusBadgeClass(restaurant.approval_status)}>
                      {restaurant.approval_status}
                    </span>
                  </div>
                  <div className="absolute top-4 left-4">
                    <span className={getSafetyBadgeClass(restaurant.safety_rating)}>
                      {restaurant.safety_rating}
                    </span>
                  </div>
                </div>
                
                <div className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="font-bold text-xl text-gray-900 mb-1">{restaurant.name}</h3>
                      <p className="text-safebite-600 font-medium">{restaurant.cuisine}</p>
                    </div>
                    <div className="text-right">
                      <div className="flex items-center space-x-1 mb-1">
                        <Star size={16} className="text-yellow-400 fill-current" />
                        <span className="font-semibold">{restaurant.safety_score}</span>
                      </div>
                      <span className="text-sm text-gray-500">Safety Score</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center text-gray-600 mb-4">
                    <MapPin size={16} className="mr-2" />
                    <span className="text-sm">{restaurant.city}, {restaurant.state}</span>
                  </div>

                  <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                    <div className="flex items-center space-x-2">
                      <Link
                        to={`/restaurants/${restaurant.id}`}
                        className="text-safebite-600 hover:text-safebite-700 font-medium text-sm flex items-center"
                      >
                        <Eye size={16} className="mr-1" />
                        View
                      </Link>
                      <button className="text-gray-600 hover:text-safebite-600 font-medium text-sm flex items-center">
                        <Edit size={16} className="mr-1" />
                        Edit
                      </button>
                    </div>
                    <button 
                      onClick={() => handleDeleteRestaurant(restaurant.id, restaurant.name)}
                      className="text-red-600 hover:text-red-700 font-medium text-sm flex items-center"
                    >
                      <Trash2 size={16} className="mr-1" />
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Create Restaurant Modal */}
      {showCreateModal && (
        <CreateRestaurantModal
          onClose={() => setShowCreateModal(false)}
          onSuccess={() => {
            setShowCreateModal(false)
            loadRestaurants()
          }}
        />
      )}
    </div>
  )
}

export default OwnerDashboard