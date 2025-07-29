"""
API Documentation Template
"""

API_TEMPLATE = """# API: {endpoint_name}

<!-- GENERATED: endpoint-info -->
- **Method**: {method}
- **Path**: `/api/{path}`
- **Auth Required**: {auth_required}
<!-- END GENERATED -->

## Request

<!-- GENERATED: request-schema -->
### Headers
{headers_table}

### Body Schema
```typescript
{request_schema}
```

### Query Parameters
{query_params_table}
<!-- END GENERATED -->

## Response

<!-- GENERATED: response-schema -->
### Success Response (200)
```typescript
{success_response}
```

### Error Responses
{error_responses}
<!-- END GENERATED -->

## Examples

<!-- GENERATED: examples -->
### cURL
```bash
{curl_example}
```

### TypeScript
```typescript
{typescript_example}
```
<!-- END GENERATED -->

<!-- MANUAL: notes -->
## Implementation Notes

Add any custom notes here.
<!-- END MANUAL -->

<!-- GENERATED: metadata -->
---
*Last updated: {timestamp}*
*Source: {source_file}*
<!-- END GENERATED -->
"""
