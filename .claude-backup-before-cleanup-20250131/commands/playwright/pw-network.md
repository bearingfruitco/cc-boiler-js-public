# Browser Network Monitor

Monitor and debug network requests in the browser.

## Usage
```bash
/pw-network [options]

Options:
  --filter     Filter requests by: api|images|css|js|xhr|all
  --status     Filter by status code: 200|404|500|4xx|5xx
  --method     Filter by method: GET|POST|PUT|DELETE
  --watch      Keep monitoring (default: capture once)
  --export     Export to file
```

## Examples

```bash
# Monitor all network requests
/pw-network

# Watch API calls only
/pw-network --filter api --watch

# Find failed requests
/pw-network --status 4xx,5xx

# Monitor POST requests
/pw-network --method POST

# Export for analysis
/pw-network --export network-log.json
```

## Output Example

```
📡 Network Monitor
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

API Requests (12):
✅ GET  /api/user         200  45ms   1.2kb
✅ GET  /api/products     200  123ms  15.7kb
❌ POST /api/order        500  89ms   0.5kb
⚠️ GET  /api/inventory    404  23ms   0.2kb

Static Assets (24):
✅ /static/app.js        200  234ms  127kb
✅ /static/styles.css    200  89ms   45kb
✅ /images/hero.webp     200  345ms  234kb

Issues Found:
- Failed API: POST /api/order (500)
- Missing: GET /api/inventory (404)
- Slow: /images/hero.webp (345ms)

Total Requests: 36
Failed: 2
Warnings: 3
Total Size: 1.2MB
Total Time: 2.3s
```

## Advanced Features

### Request Details
```bash
# Inspect specific request
/pw-network --inspect "/api/order"

Request Details:
- Method: POST
- Status: 500
- Headers: {...}
- Payload: {"items": [...]}
- Response: {"error": "Out of stock"}
- Timing: DNS(5ms) + Connect(12ms) + TTFB(67ms)
```

### Performance Analysis
```bash
/pw-network --analyze performance

Performance Issues:
🔴 Large Resources:
   - app.bundle.js: 512kb (consider splitting)
   - hero-image.png: 2.1MB (optimize image)

🟡 Slow Requests:
   - /api/search: 1.2s (add caching)
   - /api/analytics: 890ms (defer)

🔵 Optimization Suggestions:
   - Enable gzip: Save ~40%
   - Add cache headers
   - Use CDN for static assets
```

### Mock Responses
```bash
# Test with mocked responses
/pw-network --mock "/api/order" --response '{"success": true}'

# Test error scenarios
/pw-network --mock "/api/user" --status 401
```

## Integration with Debugging

Works with other commands:
- `/pw-debug` - Debug failed requests
- `/pw-perf` - Analyze performance impact
- `/error-recovery browser` - Fix network issues

## Common Issues Detected

1. **CORS Errors**
   - Missing headers
   - Wrong origin
   - Credentials issue

2. **Failed API Calls**
   - 4xx client errors
   - 5xx server errors
   - Timeouts

3. **Performance Issues**
   - Large payloads
   - Slow endpoints
   - Missing caching

4. **Security Issues**
   - HTTP in production
   - Missing HTTPS
   - Exposed tokens

Monitor your app's network health! 📡
