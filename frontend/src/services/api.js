import axios from 'axios'

export const api = axios.create({
  baseURL: '/api', // Will be proxied to localhost:8000 by Vite
  headers: {
    'Content-Type': 'application/json'
  }
})

// Restaurant API functions
export const restaurantApi = {
  getAll: (params = {}) => api.get('/restaurants', { params }),
  getById: (id) => api.get(`/restaurants/${id}`),
  create: (data) => api.post('/restaurants', data),
  update: (id, data) => api.put(`/restaurants/${id}`, data),
  delete: (id) => api.delete(`/restaurants/${id}`),
  
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
  getUsers: () => api.get('/admin/users')
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