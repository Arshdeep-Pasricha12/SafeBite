# SafeBite API Documentation

This document provides comprehensive API documentation for the SafeBite platform.

## Base URL
```
http://localhost:8000/api
```

## Authentication

SafeBite uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Authentication Endpoints

### Register User
**POST** `/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "role": "customer"
}
```

**Roles:** `customer`, `owner`, `admin`

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "customer",
  "created_at": "2026-07-29T10:30:00Z"
}
```

### Login
**POST** `/auth/login`

Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "role": "customer",
  "email": "user@example.com",
  "full_name": "John Doe"
}
```

## User Endpoints

### Get User Profile
**GET** `/users/profile`

Get current user's profile information.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "customer",
  "created_at": "2026-07-29T10:30:00Z"
}
```

## Restaurant Endpoints

### Get Restaurants
**GET** `/restaurants`

Retrieve list of restaurants with optional filtering.

**Query Parameters:**
- `owned` (boolean): Filter by owned restaurants (requires owner/admin role)
- `search` (string): Search term for name, cuisine, or city
- `city` (string): Filter by city
- `cuisine` (string): Filter by cuisine
- `sort_by` (string): Sort option (`safety_score_desc`, `safety_score_asc`, `name`)
- `skip` (int): Pagination offset (default: 0)
- `limit` (int): Results limit (default: 100)

**Response:** `200 OK`
```json
[
  {
    "id": "R0001",
    "name": "Loyal Inc Restaurant",
    "cuisine": "Biryani",
    "address": "H.No. 068, Natarajan Circle, Faridabad-258532",
    "city": "Patna",
    "state": "Bihar",
    "phone": "6105710122",
    "email": "restaurant1@safebite.demo",
    "description": "Welcome to Loyal Inc Restaurant! We serve authentic...",
    "opening_hours": "09:00 AM - 10:00 PM",
    "license_number": "FSSAI617994399708",
    "license_status": "Active",
    "restaurant_status": "Open",
    "safety_score": 71,
    "safety_rating": "Fair",
    "approval_status": "Approved",
    "owner_id": 2,
    "created_at": "2026-07-29T08:00:00Z",
    "images": [
      {
        "id": 1,
        "restaurant_id": "R0001",
        "image_url": "https://images.unsplash.com/photo-1668236543090-82eba5ee5976",
        "is_primary": true
      }
    ]
  }
]
```

### Get Restaurant Details
**GET** `/restaurants/{id}`

Get detailed information about a specific restaurant.

**Response:** `200 OK`
```json
{
  "id": "R0001",
  "name": "Loyal Inc Restaurant",
  "cuisine": "Biryani",
  "address": "H.No. 068, Natarajan Circle, Faridabad-258532",
  "city": "Patna",
  "state": "Bihar",
  "phone": "6105710122",
  "email": "restaurant1@safebite.demo",
  "description": "Welcome to Loyal Inc Restaurant! We serve authentic...",
  "opening_hours": "09:00 AM - 10:00 PM",
  "license_number": "FSSAI617994399708",
  "license_status": "Active",
  "restaurant_status": "Open",
  "safety_score": 71,
  "safety_rating": "Fair",
  "approval_status": "Approved",
  "owner_id": 2,
  "created_at": "2026-07-29T08:00:00Z",
  "images": [
    {
      "id": 1,
      "restaurant_id": "R0001",
      "image_url": "https://images.unsplash.com/photo-1668236543090-82eba5ee5976",
      "is_primary": true
    }
  ]
}
```

### Create Restaurant
**POST** `/restaurants`

Create a new restaurant listing (Owner/Admin only).

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "name": "Amazing Pizza Palace",
  "cuisine": "Italian",
  "address": "123 Main Street, Downtown",
  "city": "Mumbai",
  "state": "Maharashtra",
  "phone": "+91-9876543210",
  "email": "info@amazingpizza.com",
  "description": "Authentic Italian pizza and pasta...",
  "opening_hours": "11:00 AM - 11:00 PM",
  "license_number": "FSSAI123456789012",
  "license_status": "Active",
  "restaurant_status": "Open",
  "images": [
    {
      "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591",
      "is_primary": true
    }
  ]
}
```

**Response:** `201 Created`
```json
{
  "id": "R1002",
  "name": "Amazing Pizza Palace",
  "cuisine": "Italian",
  "address": "123 Main Street, Downtown",
  "city": "Mumbai",
  "state": "Maharashtra",
  "phone": "+91-9876543210",
  "email": "info@amazingpizza.com",
  "description": "Authentic Italian pizza and pasta...",
  "opening_hours": "11:00 AM - 11:00 PM",
  "license_number": "FSSAI123456789012",
  "license_status": "Active",
  "restaurant_status": "Open",
  "safety_score": 80,
  "safety_rating": "Good",
  "approval_status": "Pending",
  "owner_id": 15,
  "created_at": "2026-07-29T12:00:00Z",
  "images": [
    {
      "id": 2002,
      "restaurant_id": "R1002",
      "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591",
      "is_primary": true
    }
  ]
}
```

### Update Restaurant
**PUT** `/restaurants/{id}`

Update restaurant information (Owner of restaurant or Admin only).

**Headers:** `Authorization: Bearer <token>`

**Request Body:** (Partial updates supported)
```json
{
  "name": "Updated Restaurant Name",
  "description": "Updated description...",
  "opening_hours": "10:00 AM - 12:00 AM"
}
```

**Response:** `200 OK`
Returns updated restaurant object.

### Delete Restaurant
**DELETE** `/restaurants/{id}`

Delete a restaurant listing (Owner of restaurant or Admin only).

**Headers:** `Authorization: Bearer <token>`

**Response:** `204 No Content`

## Admin Endpoints

### Get Pending Restaurants
**GET** `/admin/pending-restaurants`

Get all restaurants awaiting approval (Admin only).

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
[
  {
    "id": "R1002",
    "name": "Amazing Pizza Palace",
    "cuisine": "Italian",
    "approval_status": "Pending",
    "created_at": "2026-07-29T12:00:00Z",
    ...
  }
]
```

### Approve Restaurant
**PUT** `/admin/restaurants/{id}/approve`

Approve a restaurant listing (Admin only).

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": "R1002",
  "name": "Amazing Pizza Palace",
  "approval_status": "Approved",
  ...
}
```

### Reject Restaurant
**PUT** `/admin/restaurants/{id}/reject`

Reject a restaurant listing (Admin only).

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": "R1002",
  "name": "Amazing Pizza Palace",
  "approval_status": "Rejected",
  ...
}
```

### Get All Users
**GET** `/admin/users`

Get list of all registered users (Admin only).

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "email": "admin@safebite.demo",
    "full_name": "System Administrator",
    "role": "admin",
    "created_at": "2026-07-29T08:00:00Z"
  },
  {
    "id": 2,
    "email": "customer@safebite.demo",
    "full_name": "Jane Customer",
    "role": "customer",
    "created_at": "2026-07-29T08:00:00Z"
  }
]
```

## Error Responses

### Authentication Errors
**401 Unauthorized**
```json
{
  "detail": "Could not validate credentials"
}
```

**403 Forbidden**
```json
{
  "detail": "Operation restricted to administrators only"
}
```

### Validation Errors
**400 Bad Request**
```json
{
  "detail": "A user with this email address already exists."
}
```

**422 Unprocessable Entity**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Not Found Errors
**404 Not Found**
```json
{
  "detail": "Restaurant not found"
}
```

## Rate Limiting & Pagination

### Pagination
Most list endpoints support pagination:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100, max: 1000)

### Filtering
Restaurant endpoints support multiple filters:
- Text search across name, cuisine, and city
- Exact match filters for city and cuisine
- Sorting by safety score or name

## Data Models

### Safety Ratings
Safety scores (0-100) are automatically mapped to ratings:
- **90-100**: Excellent
- **75-89**: Good  
- **60-74**: Fair
- **0-59**: Poor

### License Status Options
- `Active`: Valid license
- `Suspended`: Temporarily suspended
- `Expired`: License has expired
- `Under Review`: Being reviewed

### Restaurant Status Options
- `Open`: Currently operating
- `Temporarily Closed`: Closed temporarily
- `Permanently Closed`: Permanently shut down

### Approval Status Options
- `Pending`: Awaiting admin approval
- `Approved`: Approved and publicly visible
- `Rejected`: Rejected by admin

## Authentication Flow

1. **Register**: Create user account with role
2. **Login**: Receive JWT token
3. **Access Protected Routes**: Include token in Authorization header
4. **Token Expiry**: Tokens expire after 7 days, require re-login

## Best Practices

1. **Always validate tokens** on protected endpoints
2. **Handle token expiry** gracefully in frontend
3. **Use HTTPS** in production
4. **Sanitize user input** to prevent XSS
5. **Implement rate limiting** for production use
6. **Log security events** for monitoring

## Testing

Use the provided demo accounts for testing:
- **Admin**: admin@safebite.demo / adminpassword  
- **Customer**: customer@safebite.demo / password123
- **Owner**: Any restaurant email / password123

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation with Swagger UI.