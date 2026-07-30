import { useState, useEffect } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { Search, Filter, MapPin, Star, Clock, Phone } from 'lucide-react'
import { restaurantApi } from '../services/api'

const RestaurantListing = () => {
  const [restaurants, setRestaurants] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchParams, setSearchParams] = useSearchParams()
  
  const [filters, setFilters] = useState({
    search: searchParams.get('search') || '',
    city: searchParams.get('city') || '',
    cuisine: searchParams.get('cuisine') || '',
    sort_by: 'safety_score_desc'
  })

  const [cities, setCities] = useState([])
  const [cuisines, setCuisines] = useState([])

  useEffect(() => {
    loadRestaurants()
  }, [filters])

  const loadRestaurants = async () => {
    setLoading(true)
    try {
      const params = {
        ...filters,
        limit: 50
      }
      
      // Remove empty filters
      Object.keys(params).forEach(key => {
        if (!params[key]) delete params[key]
      })

      const response = await restaurantApi.getAll(params)
      const data = response.data
      setRestaurants(data)

      // Extract unique cities and cuisines for filters
      const uniqueCities = [...new Set(data.map(r => r.city))].sort()
      const uniqueCuisines = [...new Set(data.map(r => r.cuisine))].sort()
      
      setCities(uniqueCities)
      setCuisines(uniqueCuisines)
    } catch (error) {
      console.error('Error loading restaurants:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value }
    setFilters(newFilters)
    
    // Update URL parameters
    const newParams = new URLSearchParams()
    Object.entries(newFilters).forEach(([k, v]) => {
      if (v) newParams.set(k, v)
    })
    setSearchParams(newParams)
  }

  const clearFilters = () => {
    setFilters({
      search: '',
      city: '',
      cuisine: '',
      sort_by: 'safety_score_desc'
    })
    setSearchParams({})
  }

  const getSafetyBadgeClass = (rating) => {
    switch (rating.toLowerCase()) {
      case 'excellent': return 'badge-excellent'
      case 'good': return 'badge-good'
      case 'fair': return 'badge-fair'
      case 'poor': return 'badge-poor'
      default: return 'badge-fair'
    }
  }

  const getStatusBadgeClass = (status) => {
    switch (status.toLowerCase()) {
      case 'open': return 'bg-green-100 text-green-800'
      case 'temporarily closed': return 'bg-yellow-100 text-yellow-800'
      case 'permanently closed': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Restaurant Directory</h1>
          <p className="text-gray-600">Discover safe and delicious restaurants with verified food safety standards</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar Filters */}
          <div className="lg:w-1/4">
            <div className="card p-6 sticky top-8">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-gray-900 flex items-center">
                  <Filter size={20} className="mr-2" />
                  Filters
                </h2>
                <button 
                  onClick={clearFilters}
                  className="text-sm text-safebite-600 hover:text-safebite-700"
                >
                  Clear All
                </button>
              </div>

              {/* Search */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
                <div className="relative">
                  <Search size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                  <input
                    type="text"
                    value={filters.search}
                    onChange={(e) => handleFilterChange('search', e.target.value)}
                    placeholder="Restaurant name, cuisine..."
                    className="input-field pl-10"
                  />
                </div>
              </div>

              {/* City Filter */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">City</label>
                <select
                  value={filters.city}
                  onChange={(e) => handleFilterChange('city', e.target.value)}
                  className="input-field"
                >
                  <option value="">All Cities</option>
                  {cities.map(city => (
                    <option key={city} value={city}>{city}</option>
                  ))}
                </select>
              </div>

              {/* Cuisine Filter */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Cuisine</label>
                <select
                  value={filters.cuisine}
                  onChange={(e) => handleFilterChange('cuisine', e.target.value)}
                  className="input-field"
                >
                  <option value="">All Cuisines</option>
                  {cuisines.map(cuisine => (
                    <option key={cuisine} value={cuisine}>{cuisine}</option>
                  ))}
                </select>
              </div>

              {/* Sort By */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
                <select
                  value={filters.sort_by}
                  onChange={(e) => handleFilterChange('sort_by', e.target.value)}
                  className="input-field"
                >
                  <option value="safety_score_desc">Safety Score (High to Low)</option>
                  <option value="safety_score_asc">Safety Score (Low to High)</option>
                  <option value="name">Name (A to Z)</option>
                </select>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:w-3/4">
            {/* Results Header */}
            <div className="flex items-center justify-between mb-6">
              <p className="text-gray-600">
                {loading ? 'Loading...' : `${restaurants.length} restaurants found`}
              </p>
            </div>

            {/* Loading State */}
            {loading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {[1, 2, 3, 4].map(i => (
                  <div key={i} className="card p-6 animate-pulse">
                    <div className="h-48 bg-gray-200 rounded-lg mb-4"></div>
                    <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                    <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                  </div>
                ))}
              </div>
            ) : restaurants.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-gray-400 mb-4">
                  <Search size={64} className="mx-auto" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No restaurants found</h3>
                <p className="text-gray-600">Try adjusting your filters or search terms</p>
              </div>
            ) : (
              /* Restaurant Grid */
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {restaurants.map((restaurant) => (
                  <Link
                    key={restaurant.id}
                    to={`/restaurants/${restaurant.id}`}
                    className="card hover:shadow-lg transition-shadow duration-200"
                  >
                    <div className="relative">
                      <img
                        src={restaurant.images?.[0]?.image_url || 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80'}
                        alt={restaurant.name}
                        className="w-full h-48 object-cover rounded-t-xl"
                      />
                      <div className="absolute top-4 right-4">
                        <span className={getSafetyBadgeClass(restaurant.safety_rating)}>
                          {restaurant.safety_rating}
                        </span>
                      </div>
                      <div className="absolute bottom-4 left-4">
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusBadgeClass(restaurant.restaurant_status)}`}>
                          {restaurant.restaurant_status}
                        </span>
                      </div>
                    </div>
                    
                    <div className="p-6">
                      <h3 className="font-bold text-xl text-gray-900 mb-2">{restaurant.name}</h3>
                      <p className="text-safebite-600 font-medium mb-2">{restaurant.cuisine}</p>
                      
                      <div className="flex items-start text-gray-600 mb-3">
                        <MapPin size={16} className="mr-2 mt-0.5 flex-shrink-0" />
                        <span className="text-sm">{restaurant.address}, {restaurant.city}, {restaurant.state}</span>
                      </div>
                      
                      <div className="flex items-center text-gray-600 mb-3">
                        <Phone size={16} className="mr-2" />
                        <span className="text-sm">{restaurant.phone}</span>
                      </div>

                      <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                        <div className="flex items-center space-x-3">
                          <div className="flex items-center space-x-1">
                            <Star size={16} className="text-yellow-400 fill-current" />
                            <span className="font-semibold text-gray-900">{restaurant.safety_score}</span>
                          </div>
                          <span className="text-gray-400">•</span>
                          <span className="text-sm text-gray-600">
                            {restaurant.inspection_result || 'No Inspection'}
                          </span>
                          {restaurant.last_inspection_date && (
                            <>
                              <span className="text-gray-400">•</span>
                              <span className="text-xs text-gray-500">
                                {new Date(restaurant.last_inspection_date).toLocaleDateString()}
                              </span>
                            </>
                          )}
                        </div>
                        <div className="flex items-center text-gray-500">
                          <Clock size={14} className="mr-1" />
                          <span className="text-xs">{restaurant.opening_hours || '9 AM - 10 PM'}</span>
                        </div>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default RestaurantListing