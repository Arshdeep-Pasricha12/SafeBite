import axios from 'axios'

export const api = axios.create({
  baseURL: '/api', // Proxied to backend
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token interceptor from localStorage if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token') || localStorage.getItem('safebite_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Restaurant API functions
export const restaurantApi = {
  getAll: (params = {}) => api.get('/restaurants', { params }),
  getById: (id) => api.get(`/restaurants/${id}`),
  create: (data) => api.post('/restaurants', data),
  update: (id, data) => api.put(`/restaurants/${id}`, data),
  delete: (id) => api.delete(`/restaurants/${id}`),
  
  // Extension and Companion Demo Restaurant Matching
  match: (params = {}) => api.get('/restaurants/match', { params }),

  // Owner Correction Request and Dispute
  submitCorrectionRequest: (id, data) => api.post(`/restaurants/${id}/correction-request`, data),
  getCorrectionRequests: (id) => api.get(`/restaurants/${id}/correction-requests`),

  // Inspection endpoints
  getInspections: (restaurantId, params = {}) => 
    api.get(`/restaurants/${restaurantId}/inspections`, { params }),
  getInspectionDetails: (restaurantId, inspectionId) => 
    api.get(`/restaurants/${restaurantId}/inspections/${inspectionId}`)
}

// Admin API functions
export const adminApi = {
  getPendingRestaurants: () => api.get('/admin/pending-restaurants'),
  approveRestaurant: (id) => api.put(`/admin/restaurants/${id}/approve`),
  rejectRestaurant: (id) => api.put(`/admin/restaurants/${id}/reject`),
  getUsers: () => api.get('/admin/users'),
  getCorrectionRequests: (params = {}) => api.get('/admin/correction-requests', { params }),
  reviewCorrectionRequest: (id, data) => api.put(`/admin/correction-requests/${id}/review`, data)
}

// User API functions
export const userApi = {
  getProfile: () => api.get('/users/profile')
}

// Inspection API functions
export const inspectionApi = {
  getViolationCodes: (params = {}) => api.get('/violation-codes', { params }),
  getInspectors: () => api.get('/inspectors')
}