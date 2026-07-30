import { useState } from 'react'
import { X, Plus, Trash2 } from 'lucide-react'
import { restaurantApi } from '../services/api'

const CreateRestaurantModal = ({ onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    name: '',
    cuisine: '',
    address: '',
    city: '',
    state: '',
    phone: '',
    email: '',
    description: '',
    opening_hours: '09:00 AM - 10:00 PM',
    license_number: '',
    license_status: 'Active',
    restaurant_status: 'Open',
    images: []
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const cuisineOptions = [
    'North Indian', 'South Indian', 'Chinese', 'Italian', 'Thai', 'Mexican',
    'Japanese', 'Continental', 'Fast Food', 'Pizza', 'Burger', 'Cafe',
    'Desserts', 'Street Food', 'Seafood', 'BBQ', 'Korean', 'Lebanese',
    'Vegan', 'Bakery', 'Biryani', 'Maharashtrian', 'Andhra', 'Beverages'
  ]

  const stateOptions = [
    'Andhra Pradesh', 'Bihar', 'Delhi', 'Gujarat', 'Karnataka', 'Kerala',
    'Madhya Pradesh', 'Maharashtra', 'Punjab', 'Rajasthan', 'Tamil Nadu',
    'Telangana', 'Uttar Pradesh', 'West Bengal'
  ]

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleImageAdd = () => {
    setFormData({
      ...formData,
      images: [...formData.images, { image_url: '', is_primary: formData.images.length === 0 }]
    })
  }

  const handleImageChange = (index, value) => {
    const newImages = [...formData.images]
    newImages[index].image_url = value
    setFormData({ ...formData, images: newImages })
  }

  const handleImageRemove = (index) => {
    const newImages = formData.images.filter((_, i) => i !== index)
    // If we removed the primary image, make the first image primary
    if (newImages.length > 0 && formData.images[index].is_primary) {
      newImages[0].is_primary = true
    }
    setFormData({ ...formData, images: newImages })
  }

  const handlePrimaryChange = (index) => {
    const newImages = formData.images.map((img, i) => ({
      ...img,
      is_primary: i === index
    }))
    setFormData({ ...formData, images: newImages })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await restaurantApi.create(formData)
      onSuccess()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create restaurant')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-900">Create New Restaurant</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {/* Basic Information */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Basic Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Restaurant Name *</label>
                <input
                  type="text"
                  name="name"
                  required
                  value={formData.name}
                  onChange={handleInputChange}
                  className="input-field"
                  placeholder="Enter restaurant name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Cuisine *</label>
                <select
                  name="cuisine"
                  required
                  value={formData.cuisine}
                  onChange={handleInputChange}
                  className="input-field"
                >
                  <option value="">Select cuisine type</option>
                  {cuisineOptions.map(cuisine => (
                    <option key={cuisine} value={cuisine}>{cuisine}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Location */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Location</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Address *</label>
                <textarea
                  name="address"
                  required
                  value={formData.address}
                  onChange={handleInputChange}
                  className="input-field"
                  rows={2}
                  placeholder="Enter full address"
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">City *</label>
                  <input
                    type="text"
                    name="city"
                    required
                    value={formData.city}
                    onChange={handleInputChange}
                    className="input-field"
                    placeholder="Enter city"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">State *</label>
                  <select
                    name="state"
                    required
                    value={formData.state}
                    onChange={handleInputChange}
                    className="input-field"
                  >
                    <option value="">Select state</option>
                    {stateOptions.map(state => (
                      <option key={state} value={state}>{state}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Information */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Contact Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Phone *</label>
                <input
                  type="tel"
                  name="phone"
                  required
                  value={formData.phone}
                  onChange={handleInputChange}
                  className="input-field"
                  placeholder="Enter phone number"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email *</label>
                <input
                  type="email"
                  name="email"
                  required
                  value={formData.email}
                  onChange={handleInputChange}
                  className="input-field"
                  placeholder="Enter email address"
                />
              </div>
            </div>
          </div>

          {/* Business Details */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Business Details</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  className="input-field"
                  rows={3}
                  placeholder="Describe your restaurant (optional)"
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Opening Hours</label>
                  <input
                    type="text"
                    name="opening_hours"
                    value={formData.opening_hours}
                    onChange={handleInputChange}
                    className="input-field"
                    placeholder="e.g., 09:00 AM - 10:00 PM"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Restaurant Status</label>
                  <select
                    name="restaurant_status"
                    value={formData.restaurant_status}
                    onChange={handleInputChange}
                    className="input-field"
                  >
                    <option value="Open">Open</option>
                    <option value="Temporarily Closed">Temporarily Closed</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* License Information */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">License Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">License Number *</label>
                <input
                  type="text"
                  name="license_number"
                  required
                  value={formData.license_number}
                  onChange={handleInputChange}
                  className="input-field"
                  placeholder="Enter FSSAI license number"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">License Status</label>
                <select
                  name="license_status"
                  value={formData.license_status}
                  onChange={handleInputChange}
                  className="input-field"
                >
                  <option value="Active">Active</option>
                  <option value="Under Review">Under Review</option>
                  <option value="Suspended">Suspended</option>
                  <option value="Expired">Expired</option>
                </select>
              </div>
            </div>
          </div>

          {/* Images */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Restaurant Images</h3>
            <div className="space-y-4">
              {formData.images.map((image, index) => (
                <div key={index} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <input
                      type="url"
                      value={image.image_url}
                      onChange={(e) => handleImageChange(index, e.target.value)}
                      className="input-field"
                      placeholder="Enter image URL"
                    />
                  </div>
                  <div className="flex items-center space-x-2">
                    <label className="flex items-center space-x-2">
                      <input
                        type="radio"
                        name="primary_image"
                        checked={image.is_primary}
                        onChange={() => handlePrimaryChange(index)}
                        className="text-safebite-600"
                      />
                      <span className="text-sm text-gray-600">Primary</span>
                    </label>
                    <button
                      type="button"
                      onClick={() => handleImageRemove(index)}
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>
              ))}
              <button
                type="button"
                onClick={handleImageAdd}
                className="flex items-center space-x-2 text-safebite-600 hover:text-safebite-700 font-medium"
              >
                <Plus size={16} />
                <span>Add Image</span>
              </button>
              <p className="text-sm text-gray-500">
                Images are optional. If no images are provided, a default image based on cuisine will be used.
              </p>
            </div>
          </div>

          {/* Form Actions */}
          <div className="flex justify-end space-x-4 pt-6 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="btn-secondary"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Creating...
                </div>
              ) : (
                'Create Restaurant'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CreateRestaurantModal