import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { MapPin, Phone, Mail, Clock, Star, Shield, AlertTriangle, CheckCircle, Camera } from 'lucide-react';
import { restaurantApi } from '../services/api';
import InspectionHistory from '../components/InspectionHistory';

const RestaurantDetail = () => {
  const { id } = useParams();
  const [restaurant, setRestaurant] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('inspections'); // Default to inspections tab

  useEffect(() => {
    fetchRestaurant();
  }, [id]);

  const fetchRestaurant = async () => {
    try {
      setLoading(true);
      const response = await restaurantApi.getById(id);
      setRestaurant(response.data);
    } catch (err) {
      console.error('Error fetching restaurant:', err);
      setError('Restaurant not found');
    } finally {
      setLoading(false);
    }
  };

  const getSafetyBadgeColor = (rating) => {
    switch (rating?.toLowerCase()) {
      case 'excellent':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'good':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'fair':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'poor':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 80) return 'text-blue-600';
    if (score >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-6xl mx-auto">
          <div className="animate-pulse">
            <div className="h-64 bg-gray-200 rounded-lg mb-6"></div>
            <div className="h-8 bg-gray-200 rounded mb-4"></div>
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Restaurant Not Found</h1>
          <p className="text-gray-600">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section with Safety Score Prominence */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto p-8">
          <div className="grid md:grid-cols-3 gap-8">
            {/* Restaurant Image */}
            <div className="md:col-span-1">
              {restaurant.images && restaurant.images.length > 0 ? (
                <img
                  src={restaurant.images[0].image_url}
                  alt={restaurant.name}
                  className="w-full h-64 object-cover rounded-lg shadow-lg"
                />
              ) : (
                <div className="w-full h-64 bg-gray-200 rounded-lg flex items-center justify-center">
                  <Camera className="w-12 h-12 text-gray-400" />
                </div>
              )}
            </div>

            {/* Restaurant Info */}
            <div className="md:col-span-2">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h1 className="text-4xl font-bold text-gray-900 mb-2">{restaurant.name}</h1>
                  <p className="text-lg text-gray-600 mb-4">{restaurant.cuisine} Cuisine</p>
                  
                  <div className="flex items-center space-x-4 text-sm text-gray-600 mb-6">
                    <span className="flex items-center">
                      <MapPin className="w-4 h-4 mr-1" />
                      {restaurant.address}, {restaurant.city}, {restaurant.state}
                    </span>
                    <span className="flex items-center">
                      <Phone className="w-4 h-4 mr-1" />
                      {restaurant.phone}
                    </span>
                  </div>
                </div>

                {/* Safety Score - Big and Prominent */}
                <div className="text-center bg-white border-2 border-gray-200 rounded-xl p-6 shadow-lg">
                  <div className="mb-2">
                    <Shield className="w-8 h-8 mx-auto text-blue-600 mb-2" />
                    <div className="text-xs text-gray-500 uppercase tracking-wide font-semibold">
                      Safety Score
                    </div>
                  </div>
                  <div className={`text-4xl font-bold ${getScoreColor(restaurant.safety_score)} mb-2`}>
                    {restaurant.safety_score}
                  </div>
                  <div className={`px-3 py-1 rounded-full text-sm font-medium border ${getSafetyBadgeColor(restaurant.safety_rating)}`}>
                    {restaurant.safety_rating}
                  </div>
                </div>
              </div>

              {/* Quick Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-gray-50 rounded-lg">
                <div className="text-center">
                  <div className="text-lg font-semibold text-gray-900">
                    {restaurant.restaurant_status}
                  </div>
                  <div className="text-xs text-gray-500">Status</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-semibold text-gray-900">
                    {restaurant.license_status}
                  </div>
                  <div className="text-xs text-gray-500">License</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-semibold text-gray-900">
                    {restaurant.last_inspection_date ? 
                      new Date(restaurant.last_inspection_date).toLocaleDateString() : 'N/A'}
                  </div>
                  <div className="text-xs text-gray-500">Last Inspection</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-semibold text-gray-900">
                    {restaurant.previous_violations || 0}
                  </div>
                  <div className="text-xs text-gray-500">Total Violations</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-6xl mx-auto">
          <nav className="flex space-x-8 px-8">
            <button
              onClick={() => setActiveTab('inspections')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'inspections'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              🔍 Inspection History
            </button>
            <button
              onClick={() => setActiveTab('details')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'details'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              📋 Details
            </button>
            <button
              onClick={() => setActiveTab('violations')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'violations'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              ⚠️ Violation History
            </button>
          </nav>
        </div>
      </div>

      {/* Tab Content */}
      <div className="max-w-6xl mx-auto p-8">
        {activeTab === 'inspections' && (
          <div className="space-y-8">
            {/* Inspection History - THE STAR OF THE SHOW */}
            <InspectionHistory restaurantId={restaurant.id} />
          </div>
        )}

        {activeTab === 'details' && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Restaurant Details</h2>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Contact Information</h3>
                <div className="space-y-3">
                  <div className="flex items-center">
                    <Mail className="w-5 h-5 text-gray-400 mr-3" />
                    <span>{restaurant.email}</span>
                  </div>
                  <div className="flex items-center">
                    <Phone className="w-5 h-5 text-gray-400 mr-3" />
                    <span>{restaurant.phone}</span>
                  </div>
                  <div className="flex items-start">
                    <MapPin className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
                    <div>
                      <div>{restaurant.address}</div>
                      <div>{restaurant.city}, {restaurant.state}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Operating Hours</h3>
                <div className="flex items-center">
                  <Clock className="w-5 h-5 text-gray-400 mr-3" />
                  <span>{restaurant.opening_hours}</span>
                </div>

                <h3 className="text-lg font-semibold text-gray-900 mb-4 mt-6">License Information</h3>
                <div className="space-y-2">
                  <div>
                    <span className="text-gray-600">License Number:</span>
                    <span className="ml-2 font-medium">{restaurant.license_number}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Status:</span>
                    <span className="ml-2 font-medium">{restaurant.license_status}</span>
                  </div>
                </div>
              </div>
            </div>

            {restaurant.description && (
              <div className="mt-6 pt-6 border-t">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">About</h3>
                <p className="text-gray-600">{restaurant.description}</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'violations' && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Violation Summary</h2>
            
            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="bg-red-50 p-4 rounded-lg border border-red-200">
                <div className="text-2xl font-bold text-red-600 mb-1">
                  {restaurant.previous_violations || 0}
                </div>
                <div className="text-sm text-red-800">Total Violations</div>
              </div>
              <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                <div className="text-2xl font-bold text-yellow-600 mb-1">
                  {restaurant.violation_severity || 'N/A'}
                </div>
                <div className="text-sm text-yellow-800">Latest Severity</div>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                <div className="text-2xl font-bold text-blue-600 mb-1">
                  {restaurant.complaint_count || 0}
                </div>
                <div className="text-sm text-blue-800">Complaints</div>
              </div>
            </div>

            {restaurant.latest_violation && (
              <div className="p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-2">Latest Violation</h3>
                <p className="text-gray-700">{restaurant.latest_violation}</p>
                <div className="mt-2 text-sm text-gray-500">
                  Severity: {restaurant.violation_severity}
                </div>
              </div>
            )}

            <div className="mt-6 text-sm text-gray-600">
              <p>For detailed violation information, please check the Inspection History tab above.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RestaurantDetail;