# API Specification - [Project Name]

## Overview

This document defines all API endpoints, request/response formats, authentication requirements, and integration guidelines.

## API Information

- **Base URL**: `https://api.[project-domain].com`
- **Version**: v1
- **Protocol**: HTTPS only
- **Format**: JSON (application/json)
- **Authentication**: Bearer token (JWT)

## Authentication

### Authentication Flow
```
1. User logs in via /auth/login
2. Receives JWT access token (expires in 1 hour)
3. Receives refresh token (expires in 30 days)
4. Includes access token in Authorization header
5. Refreshes token when expired via /auth/refresh
```

### Request Headers
```http
Authorization: Bearer <access_token>
Content-Type: application/json
X-Request-ID: <unique-request-id>
```

### Authentication Endpoints

#### POST /auth/login
Authenticate user and receive tokens.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "dGhpcyBpcyBhIHJlZnJl...",
  "expires_in": 3600,
  "token_type": "Bearer",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "profile": {
      "display_name": "John Doe"
    }
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}
```

#### POST /auth/refresh
Refresh access token using refresh token.

**Request:**
```json
{
  "refresh_token": "dGhpcyBpcyBhIHJlZnJl..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

#### POST /auth/logout
Invalidate current session.

**Request:**
```json
{
  "refresh_token": "dGhpcyBpcyBhIHJlZnJl..."
}
```

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

## Core Resources

### Users

#### GET /api/v1/users/me
Get current user's profile.

**Response (200 OK):**
```json
{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "profile": {
      "display_name": "John Doe",
      "avatar_url": "https://...",
      "metadata": {}
    },
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

#### PATCH /api/v1/users/me
Update current user's profile.

**Request:**
```json
{
  "profile": {
    "display_name": "Jane Doe",
    "metadata": {
      "preferences": {
        "theme": "dark"
      }
    }
  }
}
```

**Response (200 OK):**
```json
{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "profile": {
      "display_name": "Jane Doe",
      "avatar_url": "https://...",
      "metadata": {
        "preferences": {
          "theme": "dark"
        }
      }
    },
    "updated_at": "2024-01-15T11:00:00Z"
  }
}
```

### [Resource Name]

#### GET /api/v1/[resources]
List all [resources] with pagination and filtering.

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `limit` (integer): Items per page (default: 20, max: 100)
- `sort` (string): Sort field (default: created_at)
- `order` (string): Sort order - asc/desc (default: desc)
- `filter[field]` (string): Filter by field value

**Request:**
```
GET /api/v1/[resources]?page=1&limit=20&sort=created_at&order=desc&filter[status]=active
```

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Resource Name",
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  },
  "links": {
    "first": "/api/v1/[resources]?page=1&limit=20",
    "prev": null,
    "next": "/api/v1/[resources]?page=2&limit=20",
    "last": "/api/v1/[resources]?page=8&limit=20"
  }
}
```

#### GET /api/v1/[resources]/:id
Get single [resource] by ID.

**Response (200 OK):**
```json
{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Resource Name",
    "description": "Detailed description",
    "status": "active",
    "metadata": {},
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Resource with ID '123' not found"
  }
}
```

#### POST /api/v1/[resources]
Create new [resource].

**Request:**
```json
{
  "name": "New Resource",
  "description": "Resource description",
  "metadata": {}
}
```

**Response (201 Created):**
```json
{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "New Resource",
    "description": "Resource description",
    "status": "active",
    "metadata": {},
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

**Validation Error (400 Bad Request):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "name",
        "message": "Name is required"
      }
    ]
  }
}
```

#### PUT /api/v1/[resources]/:id
Update entire [resource].

**Request:**
```json
{
  "name": "Updated Resource",
  "description": "Updated description",
  "status": "active",
  "metadata": {}
}
```

**Response (200 OK):**
```json
{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Updated Resource",
    "description": "Updated description",
    "status": "active",
    "metadata": {},
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
  }
}
```

#### PATCH /api/v1/[resources]/:id
Partially update [resource].

**Request:**
```json
{
  "status": "inactive"
}
```

**Response (200 OK):**
```json
{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Updated Resource",
    "description": "Updated description",
    "status": "inactive",
    "metadata": {},
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T11:30:00Z"
  }
}
```

#### DELETE /api/v1/[resources]/:id
Delete [resource].

**Response (204 No Content):**
```
(empty body)
```

**Error Response (403 Forbidden):**
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "You don't have permission to delete this resource"
  }
}
```

## Batch Operations

### POST /api/v1/[resources]/batch
Perform batch operations on multiple resources.

**Request:**
```json
{
  "operation": "update",
  "resources": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "data": {
        "status": "active"
      }
    },
    {
      "id": "234e5678-e89b-12d3-a456-426614174001",
      "data": {
        "status": "inactive"
      }
    }
  ]
}
```

**Response (200 OK):**
```json
{
  "results": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "success": true
    },
    {
      "id": "234e5678-e89b-12d3-a456-426614174001",
      "success": false,
      "error": {
        "code": "RESOURCE_NOT_FOUND",
        "message": "Resource not found"
      }
    }
  ],
  "summary": {
    "total": 2,
    "successful": 1,
    "failed": 1
  }
}
```

## Webhooks

### Webhook Events
The API can send webhooks for the following events:

- `user.created` - New user registration
- `user.updated` - User profile updated
- `[resource].created` - New resource created
- `[resource].updated` - Resource updated
- `[resource].deleted` - Resource deleted

### Webhook Payload
```json
{
  "id": "evt_123e4567-e89b-12d3-a456-426614174000",
  "type": "resource.created",
  "created": "2024-01-15T10:30:00Z",
  "data": {
    "object": {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Resource Name",
      // ... full resource data
    }
  }
}
```

### Webhook Security
All webhooks include a signature header for verification:

```http
X-Webhook-Signature: sha256=<signature>
```

Verify signature using:
```javascript
const crypto = require('crypto');

function verifyWebhookSignature(payload, signature, secret) {
  const hash = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');
  
  return `sha256=${hash}` === signature;
}
```

## Rate Limiting

### Rate Limits
- **Anonymous**: 60 requests/hour
- **Authenticated**: 1000 requests/hour
- **Premium**: 10000 requests/hour

### Rate Limit Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642584000
```

### Rate Limit Exceeded (429 Too Many Requests)
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retry_after": 3600
  }
}
```

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": [
      {
        "field": "field_name",
        "message": "Field-specific error"
      }
    ],
    "request_id": "req_123e4567-e89b-12d3-a456-426614174000"
  }
}
```

### Common Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Missing or invalid authentication |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `CONFLICT` | 409 | Resource conflict (duplicate) |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

## Versioning

### API Versioning Strategy
- Version in URL path: `/api/v1/`, `/api/v2/`
- Backward compatibility maintained for 6 months
- Deprecation notices in headers: `X-API-Deprecation-Date`
- Migration guides provided for breaking changes

## SDK Support

### Official SDKs
- JavaScript/TypeScript: `npm install @[project]/sdk`
- Python: `pip install [project]-sdk`
- Ruby: `gem install [project]-sdk`

### SDK Example (JavaScript)
```javascript
import { [Project]Client } from '@[project]/sdk';

const client = new [Project]Client({
  apiKey: process.env.[PROJECT]_API_KEY
});

// List resources
const resources = await client.resources.list({
  page: 1,
  limit: 20,
  filter: { status: 'active' }
});

// Create resource
const newResource = await client.resources.create({
  name: 'New Resource',
  description: 'Description'
});

// Update resource
const updated = await client.resources.update('resource-id', {
  status: 'inactive'
});

// Delete resource
await client.resources.delete('resource-id');
```

## API Best Practices

### Request Guidelines
1. **Always include X-Request-ID** for tracing
2. **Use proper HTTP methods** (GET for read, POST for create, etc.)
3. **Include Content-Type header** for requests with body
4. **Handle rate limits gracefully** with exponential backoff
5. **Validate input client-side** to reduce API calls

### Response Handling
1. **Check HTTP status first** before parsing body
2. **Handle all error scenarios** including network errors
3. **Respect cache headers** for GET requests
4. **Parse pagination meta** for list endpoints
5. **Store and refresh tokens** appropriately

### Security Best Practices
1. **Never expose API keys** in client-side code
2. **Use HTTPS only** for all API calls
3. **Validate webhook signatures** before processing
4. **Implement request timeouts** (recommended: 30s)
5. **Log security events** for auditing

## Testing

### Test Environment
- **Base URL**: `https://api-test.[project-domain].com`
- **Test API Keys**: Available in dashboard
- **Rate Limits**: Same as production
- **Data Reset**: Daily at 00:00 UTC

### Postman Collection
Download our Postman collection for easy testing:
[Download Postman Collection](https://...)

### Example cURL Requests

#### Authentication
```bash
curl -X POST https://api.[project-domain].com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'
```

#### List Resources
```bash
curl -X GET "https://api.[project-domain].com/api/v1/resources?page=1&limit=10" \
  -H "Authorization: Bearer <access_token>"
```

#### Create Resource
```bash
curl -X POST https://api.[project-domain].com/api/v1/resources \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"New Resource","description":"Test"}'
```

## Changelog

### v1.0.0 (Current)
- Initial API release
- Core resource endpoints
- Authentication system
- Webhook support

### Upcoming (v1.1.0)
- GraphQL endpoint
- WebSocket support
- Batch operations
- Advanced filtering

## Support

### Documentation
- API Reference: https://docs.[project-domain].com/api
- SDK Docs: https://docs.[project-domain].com/sdk
- Status Page: https://status.[project-domain].com

### Contact
- Email: api-support@[project-domain].com
- Discord: [Discord invite link]
- GitHub: [GitHub repository]
