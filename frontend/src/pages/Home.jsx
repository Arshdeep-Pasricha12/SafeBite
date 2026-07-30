import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Search, Shield, Users, MapPin, Star, Clock } from 'lucide-react'
import { restaurantApi } from '../services/api'

const Home = () => {
  const [searchTerm, setSearchTerm] = useState('')
  const [featuredRestaurants, setFeaturedRestaurants] = useState([])
  const [stats, setStats] = useState({
    totalRestaurants: 0,
    activeLicenses: 0,
    avgSafetyScore: 0
  })

  useEffect(() => {
    loadFeaturedRestaurants()
  }, [])

  const loadFeaturedRestaurants = async () => {
    try {
      const response = await restaurantApi.getAll({ 
        limit: 6, 
        sort_by: 'safety_score_desc' 
      })
      const restaurants = response.data
      setFeaturedRestaurants(restaurants)
      
      // Calculate basic stats
      const activeLicenses = restaurants.filter(r => r.license_status === 'Active').length
      const avgScore = restaurants.length > 0 
        ? Math.round(restaurants.reduce((sum, r) => sum + r.safety_score, 0) / restaurants.length)
        : 0
      
      setStats({
        totalRestaurants: restaurants.length,
        activeLicenses,
        avgSafetyScore: avgScore
      })
    } catch (error) {
      console.error('Error loading featured restaurants:', error)
    }
  }

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchTerm.trim()) {
      window.location.href = `/restaurants?search=${encodeURIComponent(searchTerm.trim())}`
    }
  }

  const topCuisines = [
    { name: 'North Indian', image: 'https://images.unsplash.com/photo-1585938338392-50a59990d4e5?auto=format&fit=crop&w=400&q=80' },
    { name: 'Chinese', image: 'https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=400&q=80' },
    { name: 'Italian', image: 'https://images.unsplash.com/photo-1533777857889-4be7c70b33f7?auto=format&fit=crop&w=400&q=80' },
    { name: 'Thai', image: 'https://images.unsplash.com/photo-1559311648-d46f4d8593d6?auto=format&fit=crop&w=400&q=80' },
    { name: 'Mexican', image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?auto=format&fit=crop&w=400&q=80' },
    { name: 'Japanese', image: 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=400&q=80' }
  ]

  const getSafetyBadgeClass = (rating) => {
    switch (rating.toLowerCase()) {
      case 'excellent': return 'badge-excellent'
      case 'good': return 'badge-good'
      case 'fair': return 'badge-fair'
      case 'poor': return 'badge-poor'
      default: return 'badge-fair'
    }
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-safebite-600 to-safebite-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Discover Safe & <span className="text-safebite-100">Delicious</span> Restaurants
            </h1>
            <p className="text-xl md:text-2xl mb-10 text-safebite-100 max-w-3xl mx-auto">
              Find restaurants with verified food safety standards and transparency you can trust
            </p>
            
            {/* Search Bar */}
            <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
              <div className="flex bg-white rounded-xl p-2 shadow-lg">
                <input
                  type="text"
                  placeholder="Search restaurants, cuisines, or locations..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="flex-1 px-4 py-3 text-gray-700 rounded-l-lg focus:outline-none"
                />
                <button 
                  type="submit"
                  className="bg-safebite-600 text-white px-6 py-3 rounded-r-lg hover:bg-safebite-700 transition-colors duration-200 flex items-center space-x-2"
                >
                  <Search size={20} />
                  <span>Search</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div className="p-6">
              <div className="flex items-center justify-center w-16 h-16 bg-safebite-100 rounded-full mx-auto mb-4">
                <Shield className="w-8 h-8 text-safebite-600" />
              </div>
              <h3 className="text-3xl font-bold text-gray-900 mb-2">{stats.activeLicenses}</h3>
              <p className="text-gray-600">Active Licensed Restaurants</p>
            </div>
            <div className="p-6">
              <div className="flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mx-auto mb-4">
                <Star className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-3xl font-bold text-gray-900 mb-2">{stats.avgSafetyScore}</h3>
              <p className="text-gray-600">Average Safety Score</p>
            </div>
            <div className="p-6">
              <div className="flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mx-auto mb-4">
                <Users className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-3xl font-bold text-gray-900 mb-2">{stats.totalRestaurants}+</h3>
              <p className="text-gray-600">Registered Restaurants</p>
            </div>
          </div>
        </div>
      </div>

      {/* Top Cuisines */}
      <div className="bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Explore Popular Cuisines
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {topCuisines.map((cuisine) => (
              <Link
                key={cuisine.name}
                to={`/restaurants?cuisine=${encodeURIComponent(cuisine.name)}`}
                className="group"
              >
                <div className="card p-6 text-center hover:scale-105 transition-transform duration-200">
                  <img
                    src={cuisine.image}
                    alt={cuisine.name}
                    className="w-16 h-16 rounded-full mx-auto mb-4 object-cover"
                  />
                  <h3 className="font-semibold text-gray-800 group-hover:text-safebite-600 transition-colors duration-200">
                    {cuisine.name}
                  </h3>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Featured Restaurants */}
      <div className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Featured Restaurants
            </h2>
            <p className="text-gray-600">Top-rated restaurants with excellent safety standards</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {featuredRestaurants.map((restaurant) => (
              <Link
                key={restaurant.id}
                to={`/restaurants/${restaurant.id}`}
                className="card hover:scale-105 transition-transform duration-200"
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
                </div>
                <div className="p-6">
                  <h3 className="font-bold text-xl text-gray-900 mb-2">{restaurant.name}</h3>
                  <p className="text-gray-600 mb-2">{restaurant.cuisine}</p>
                  <div className="flex items-center text-gray-500 mb-4">
                    <MapPin size={16} className="mr-1" />
                    <span>{restaurant.city}, {restaurant.state}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <div className="flex items-center space-x-1">
                        <Star size={16} className="text-yellow-400 fill-current" />
                        <span className="font-semibold">{restaurant.safety_score}</span>
                      </div>
                    </div>
                    <div className="flex items-center text-gray-500">
                      <Clock size={16} className="mr-1" />
                      <span className="text-sm">{restaurant.opening_hours || '9 AM - 10 PM'}</span>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
          
          <div className="text-center mt-12">
            <Link to="/restaurants" className="btn-primary">
              View All Restaurants
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home