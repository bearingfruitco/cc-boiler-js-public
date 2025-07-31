# Logging Strategy Guide

> Structured logging for debugging, monitoring, and compliance in production environments

## 🎯 Overview

This guide covers implementing a comprehensive logging strategy that balances debugging capabilities with performance, security, and cost considerations.

## 📊 Logging Principles

1. **Structured Over Unstructured** - JSON logs for easy parsing
2. **Contextual Information** - Include request IDs, user IDs, session IDs
3. **Appropriate Levels** - Use correct log levels consistently
4. **Security First** - Never log sensitive data
5. **Cost Conscious** - Log what matters, archive what doesn't
6. **Performance Aware** - Async logging, minimal overhead

## 📝 Log Levels

| Level | Code | When to Use | Example |
|-------|------|-------------|---------|
| **Fatal** | 0 | Application crash | Database connection lost |
| **Error** | 1 | Errors requiring attention | Payment processing failed |
| **Warn** | 2 | Concerning but handled | Rate limit approaching |
| **Info** | 3 | Normal operations | User logged in |
| **Debug** | 4 | Development details | Function parameters |
| **Trace** | 5 | Detailed execution flow | Every function call |

## 🚀 Implementation

### 1. Structured Logger Setup

```typescript
// lib/logger/index.ts
import pino from 'pino';
import { randomUUID } from 'crypto';

// Development pretty printing
const developmentTransport = {
  target: 'pino-pretty',
  options: {
    colorize: true,
    ignore: 'pid,hostname',
    translateTime: 'HH:MM:ss',
  },
};

// Production configuration
const productionTransport = process.env.LOG_ENDPOINT ? {
  target: './lib/logger/transport',
  options: {
    endpoint: process.env.LOG_ENDPOINT,
    apiKey: process.env.LOG_API_KEY,
  },
} : undefined;

// Create logger instance
export const logger = pino({
  level: process.env.LOG_LEVEL || (process.env.NODE_ENV === 'production' ? 'info' : 'debug'),
  
  // Base configuration
  base: {
    env: process.env.NODE_ENV,
    region: process.env.VERCEL_REGION || 'unknown',
    version: process.env.NEXT_PUBLIC_APP_VERSION || 'unknown',
  },
  
  // Redact sensitive fields
  redact: {
    paths: [
      'password',
      'token',
      'authorization',
      'cookie',
      'api_key',
      'secret',
      'credit_card',
      'ssn',
      '*.password',
      '*.token',
      'headers.authorization',
      'headers.cookie',
    ],
    censor: '[REDACTED]',
  },
  
  // Serializers
  serializers: {
    error: pino.stdSerializers.err,
    request: (req) => ({
      id: req.id,
      method: req.method,
      url: req.url,
      query: req.query,
      params: req.params,
      headers: {
        'user-agent': req.headers['user-agent'],
        'content-type': req.headers['content-type'],
      },
    }),
    response: (res) => ({
      statusCode: res.statusCode,
      headers: res.getHeaders(),
    }),
  },
  
  // Transport
  transport: process.env.NODE_ENV === 'development' 
    ? developmentTransport 
    : productionTransport,
});

// Child logger factory
export function createLogger(context: string, metadata?: Record<string, any>) {
  return logger.child({
    context,
    requestId: randomUUID(),
    ...metadata,
  });
}

// Request logger middleware
export function requestLogger() {
  return (req: Request, res: Response, next: Function) => {
    const start = Date.now();
    const requestId = req.headers.get('x-request-id') || randomUUID();
    
    // Attach logger to request
    req.logger = logger.child({
      requestId,
      userId: req.user?.id,
      sessionId: req.session?.id,
    });
    
    // Log request
    req.logger.info({
      msg: 'Request started',
      request: req,
    });
    
    // Log response
    const originalSend = res.send;
    res.send = function(data) {
      const duration = Date.now() - start;
      
      req.logger.info({
        msg: 'Request completed',
        request: req,
        response: res,
        duration,
      });
      
      return originalSend.call(this, data);
    };
    
    next();
  };
}
```

### 2. Custom Transport for Log Aggregation

```typescript
// lib/logger/transport.ts
import build from 'pino-abstract-transport';
import { Transform } from 'stream';

export default async function (options: any) {
  const { endpoint, apiKey, batchSize = 100, flushInterval = 5000 } = options;
  
  let batch: any[] = [];
  let timer: NodeJS.Timeout;
  
  const flush = async () => {
    if (batch.length === 0) return;
    
    const logs = [...batch];
    batch = [];
    
    try {
      await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
        },
        body: JSON.stringify({ logs }),
      });
    } catch (error) {
      // Re-add logs on failure
      batch.unshift(...logs);
      console.error('Failed to send logs:', error);
    }
  };
  
  // Set up periodic flush
  timer = setInterval(flush, flushInterval);
  
  return build(async function (source) {
    const transform = new Transform({
      objectMode: true,
      transform(chunk, encoding, callback) {
        batch.push(JSON.parse(chunk));
        
        if (batch.length >= batchSize) {
          flush();
        }
        
        callback();
      },
    });
    
    source.pipe(transform);
    
    // Cleanup on exit
    process.on('exit', () => {
      clearInterval(timer);
      flush();
    });
  });
}
```

### 3. Context-Aware Logging

```typescript
// lib/logger/context.ts
import { AsyncLocalStorage } from 'async_hooks';
import { logger } from './index';

// Create async context storage
const asyncLocalStorage = new AsyncLocalStorage<Map<string, any>>();

// Context middleware
export function logContext(metadata: Record<string, any> = {}) {
  return (req: Request, res: Response, next: Function) => {
    const store = new Map();
    
    // Add request context
    store.set('requestId', req.headers.get('x-request-id') || randomUUID());
    store.set('userId', req.user?.id);
    store.set('sessionId', req.session?.id);
    store.set('path', req.url);
    
    // Add custom metadata
    Object.entries(metadata).forEach(([key, value]) => {
      store.set(key, value);
    });
    
    // Run request in context
    asyncLocalStorage.run(store, () => {
      next();
    });
  };
}

// Get contextual logger
export function getLogger(name: string) {
  const store = asyncLocalStorage.getStore();
  const context: Record<string, any> = {};
  
  if (store) {
    store.forEach((value, key) => {
      context[key] = value;
    });
  }
  
  return logger.child({ component: name, ...context });
}

// Usage in components/services
const log = getLogger('UserService');
log.info('User created', { email: user.email });
```

### 4. API Route Logging

```typescript
// app/api/users/route.ts
import { getLogger } from '@/lib/logger/context';

const log = getLogger('api.users');

export async function GET(request: Request) {
  const start = Date.now();
  
  try {
    log.debug('Fetching users', {
      query: Object.fromEntries(new URL(request.url).searchParams),
    });
    
    const users = await getUsersFromDatabase();
    
    log.info('Users fetched successfully', {
      count: users.length,
      duration: Date.now() - start,
    });
    
    return Response.json(users);
  } catch (error) {
    log.error('Failed to fetch users', {
      error: error.message,
      stack: error.stack,
      duration: Date.now() - start,
    });
    
    return Response.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  const log = getLogger('api.users.create');
  
  try {
    const data = await request.json();
    
    // Log without sensitive data
    log.info('Creating user', {
      email: data.email,
      // Don't log password!
    });
    
    const user = await createUser(data);
    
    log.info('User created', {
      userId: user.id,
      email: user.email,
    });
    
    return Response.json(user, { status: 201 });
  } catch (error) {
    if (error.code === 'P2002') {
      log.warn('Duplicate user attempt', {
        email: data.email,
        error: error.message,
      });
      
      return Response.json(
        { error: 'User already exists' },
        { status: 409 }
      );
    }
    
    log.error('Failed to create user', {
      error: error.message,
      code: error.code,
    });
    
    return Response.json(
      { error: 'Failed to create user' },
      { status: 500 }
    );
  }
}
```

### 5. Client-Side Logging

```typescript
// lib/logger/client.ts
interface ClientLog {
  level: 'error' | 'warn' | 'info' | 'debug';
  message: string;
  context?: Record<string, any>;
  timestamp: string;
  url: string;
  userAgent: string;
}

class ClientLogger {
  private queue: ClientLog[] = [];
  private flushTimer?: number;
  
  constructor(
    private endpoint: string = '/api/logs',
    private batchSize: number = 10,
    private flushInterval: number = 5000
  ) {
    this.startFlushing();
    this.setupErrorHandlers();
  }
  
  private log(level: ClientLog['level'], message: string, context?: Record<string, any>) {
    // Don't log in development console
    if (process.env.NODE_ENV === 'development') {
      console[level](message, context);
      return;
    }
    
    const log: ClientLog = {
      level,
      message,
      context,
      timestamp: new Date().toISOString(),
      url: window.location.href,
      userAgent: navigator.userAgent,
    };
    
    this.queue.push(log);
    
    if (this.queue.length >= this.batchSize) {
      this.flush();
    }
  }
  
  error(message: string, context?: Record<string, any>) {
    this.log('error', message, context);
  }
  
  warn(message: string, context?: Record<string, any>) {
    this.log('warn', message, context);
  }
  
  info(message: string, context?: Record<string, any>) {
    this.log('info', message, context);
  }
  
  debug(message: string, context?: Record<string, any>) {
    this.log('debug', message, context);
  }
  
  private async flush() {
    if (this.queue.length === 0) return;
    
    const logs = [...this.queue];
    this.queue = [];
    
    try {
      await fetch(this.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ logs }),
      });
    } catch (error) {
      // Re-add logs on failure (with limit)
      if (this.queue.length < this.batchSize * 2) {
        this.queue.unshift(...logs);
      }
    }
  }
  
  private startFlushing() {
    this.flushTimer = window.setInterval(() => {
      this.flush();
    }, this.flushInterval);
    
    // Flush on page unload
    window.addEventListener('beforeunload', () => {
      this.flush();
    });
  }
  
  private setupErrorHandlers() {
    // Global error handler
    window.addEventListener('error', (event) => {
      this.error('JavaScript error', {
        message: event.message,
        source: event.filename,
        line: event.lineno,
        column: event.colno,
        stack: event.error?.stack,
      });
    });
    
    // Promise rejection handler
    window.addEventListener('unhandledrejection', (event) => {
      this.error('Unhandled promise rejection', {
        reason: event.reason,
      });
    });
  }
}

// Export singleton instance
export const clientLogger = new ClientLogger();
```

### 6. Performance Logging

```typescript
// lib/logger/performance.ts
import { getLogger } from './context';

const perfLog = getLogger('performance');

export function logPerformance(name: string, fn: Function) {
  return async function (...args: any[]) {
    const start = performance.now();
    const startMemory = process.memoryUsage();
    
    try {
      const result = await fn.apply(this, args);
      const duration = performance.now() - start;
      const endMemory = process.memoryUsage();
      
      perfLog.info('Operation completed', {
        operation: name,
        duration,
        memory: {
          heapUsed: endMemory.heapUsed - startMemory.heapUsed,
          external: endMemory.external - startMemory.external,
        },
      });
      
      return result;
    } catch (error) {
      const duration = performance.now() - start;
      
      perfLog.error('Operation failed', {
        operation: name,
        duration,
        error: error.message,
      });
      
      throw error;
    }
  };
}

// Usage
const processData = logPerformance('processData', async (data: any[]) => {
  // Heavy processing
  return data.map(transform);
});
```

## 🔍 Log Aggregation Strategies

### 1. CloudFlare Workers Logging

```typescript
// workers/logger.ts
export default {
  async fetch(request: Request, env: Env) {
    const log = {
      timestamp: new Date().toISOString(),
      cf: request.cf,
      method: request.method,
      url: request.url,
      headers: Object.fromEntries(request.headers),
    };
    
    // Log to Workers Analytics Engine
    env.ANALYTICS.writeDataPoint({
      blobs: [log.url, log.method],
      doubles: [Date.now()],
      indexes: [log.cf?.colo as string],
    });
    
    // Forward to log aggregator
    await fetch(env.LOG_ENDPOINT, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.LOG_API_KEY}`,
      },
      body: JSON.stringify(log),
    });
    
    return new Response('OK');
  },
};
```

### 2. Vercel Functions Logging

```typescript
// lib/logger/vercel.ts
export function vercelLogger() {
  return {
    info: (message: string, meta?: any) => {
      console.log(JSON.stringify({
        level: 'info',
        message,
        ...meta,
        timestamp: new Date().toISOString(),
        runtime: 'vercel',
      }));
    },
    error: (message: string, error: Error, meta?: any) => {
      console.error(JSON.stringify({
        level: 'error',
        message,
        error: {
          message: error.message,
          stack: error.stack,
        },
        ...meta,
        timestamp: new Date().toISOString(),
        runtime: 'vercel',
      }));
    },
  };
}
```

## 📊 Log Analysis & Querying

### 1. Common Queries

```sql
-- Error rate by endpoint
SELECT 
  url,
  COUNT(*) as total_requests,
  SUM(CASE WHEN level = 'error' THEN 1 ELSE 0 END) as errors,
  (SUM(CASE WHEN level = 'error' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as error_rate
FROM logs
WHERE timestamp > NOW() - INTERVAL '1 hour'
GROUP BY url
ORDER BY error_rate DESC;

-- Slow API endpoints
SELECT 
  context->>'operation' as endpoint,
  AVG(duration) as avg_duration,
  MAX(duration) as max_duration,
  COUNT(*) as request_count
FROM logs
WHERE 
  context->>'operation' IS NOT NULL
  AND timestamp > NOW() - INTERVAL '1 hour'
GROUP BY context->>'operation'
HAVING AVG(duration) > 1000
ORDER BY avg_duration DESC;

-- User activity timeline
SELECT 
  DATE_TRUNC('hour', timestamp) as hour,
  COUNT(DISTINCT context->>'userId') as unique_users,
  COUNT(*) as total_actions
FROM logs
WHERE 
  context->>'userId' IS NOT NULL
  AND timestamp > NOW() - INTERVAL '24 hours'
GROUP BY hour
ORDER BY hour;
```

### 2. Log Retention Policies

```typescript
// scripts/log-retention.ts
const RETENTION_POLICIES = {
  error: 90,      // 90 days for errors
  warn: 30,       // 30 days for warnings
  info: 7,        // 7 days for info
  debug: 1,       // 1 day for debug
  trace: 0.25,    // 6 hours for trace
};

export async function enforceRetention() {
  for (const [level, days] of Object.entries(RETENTION_POLICIES)) {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);
    
    // Delete old logs
    await db.logs.deleteMany({
      where: {
        level,
        timestamp: { lt: cutoffDate },
      },
    });
    
    // Archive if needed
    if (days > 7) {
      await archiveLogs(level, cutoffDate);
    }
  }
}
```

## 🔒 Security Considerations

### 1. Sensitive Data Filtering

```typescript
// lib/logger/security.ts
const SENSITIVE_PATTERNS = [
  /\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/g,  // Credit cards
  /\b\d{3}-\d{2}-\d{4}\b/g,                        // SSN
  /Bearer\s+[A-Za-z0-9\-._~\+\/]+=*/g,             // Bearer tokens
  /password["\s]*[:=]["\s]*[^",}\s]+/gi,          // Passwords in JSON
];

export function sanitizeLogs(obj: any): any {
  if (typeof obj === 'string') {
    let sanitized = obj;
    for (const pattern of SENSITIVE_PATTERNS) {
      sanitized = sanitized.replace(pattern, '[REDACTED]');
    }
    return sanitized;
  }
  
  if (Array.isArray(obj)) {
    return obj.map(sanitizeLogs);
  }
  
  if (typeof obj === 'object' && obj !== null) {
    const sanitized: any = {};
    for (const [key, value] of Object.entries(obj)) {
      // Skip sensitive keys entirely
      if (['password', 'token', 'secret', 'apiKey'].includes(key)) {
        sanitized[key] = '[REDACTED]';
      } else {
        sanitized[key] = sanitizeLogs(value);
      }
    }
    return sanitized;
  }
  
  return obj;
}
```

### 2. Compliance Logging

```typescript
// lib/logger/compliance.ts
import { getLogger } from './context';

const auditLog = getLogger('audit');

export function logAuditEvent(
  action: string,
  resource: string,
  userId: string,
  result: 'success' | 'failure',
  metadata?: Record<string, any>
) {
  auditLog.info('Audit event', {
    action,
    resource,
    userId,
    result,
    metadata,
    timestamp: new Date().toISOString(),
    ip: metadata?.ip,
    userAgent: metadata?.userAgent,
  });
}

// Usage
logAuditEvent(
  'user.login',
  'auth',
  user.id,
  'success',
  { method: 'password' }
);

logAuditEvent(
  'data.export',
  'users',
  user.id,
  'success',
  { recordCount: 1000, format: 'csv' }
);
```

## 📈 Monitoring & Alerts

### 1. Log-Based Alerts

```typescript
// lib/logger/alerts.ts
interface AlertRule {
  name: string;
  query: string;
  threshold: number;
  window: string;
  action: (count: number) => void;
}

const ALERT_RULES: AlertRule[] = [
  {
    name: 'High Error Rate',
    query: 'level:error',
    threshold: 100,
    window: '5m',
    action: (count) => {
      notifySlack(`⚠️ High error rate: ${count} errors in 5 minutes`);
    },
  },
  {
    name: 'Authentication Failures',
    query: 'action:user.login AND result:failure',
    threshold: 10,
    window: '1m',
    action: (count) => {
      notifySecurityTeam(`🔒 ${count} failed login attempts in 1 minute`);
    },
  },
  {
    name: 'Slow API Response',
    query: 'duration:>5000',
    threshold: 50,
    window: '5m',
    action: (count) => {
      notifyOncall(`🐌 ${count} slow API responses (>5s) in 5 minutes`);
    },
  },
];
```

### 2. Log Metrics Dashboard

```typescript
// app/admin/logs/page.tsx
export default function LogsDashboard() {
  const [metrics, setMetrics] = useState({
    errorRate: 0,
    avgResponseTime: 0,
    activeUsers: 0,
    topErrors: [],
  });
  
  useEffect(() => {
    const fetchMetrics = async () => {
      const response = await fetch('/api/logs/metrics');
      const data = await response.json();
      setMetrics(data);
    };
    
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 30000);
    
    return () => clearInterval(interval);
  }, []);
  
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Logs Dashboard</h1>
      
      <div className="grid grid-cols-4 gap-4 mb-8">
        <MetricCard
          title="Error Rate"
          value={`${metrics.errorRate.toFixed(2)}%`}
          trend={metrics.errorRateTrend}
        />
        <MetricCard
          title="Avg Response Time"
          value={`${metrics.avgResponseTime.toFixed(0)}ms`}
          trend={metrics.responseTrend}
        />
        <MetricCard
          title="Active Users"
          value={metrics.activeUsers}
          trend={metrics.usersTrend}
        />
        <MetricCard
          title="Log Volume"
          value={formatBytes(metrics.logVolume)}
          trend={metrics.volumeTrend}
        />
      </div>
      
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Top Errors</h2>
        <ErrorsList errors={metrics.topErrors} />
      </div>
    </div>
  );
}
```

## 🎯 Best Practices

1. **Log Levels**
   - Use appropriate levels consistently
   - ERROR only for actionable issues
   - INFO for business events
   - DEBUG for development only

2. **Context is King**
   - Always include request ID
   - Add user/session context
   - Include relevant business data
   - Maintain context across async operations

3. **Performance**
   - Use async logging
   - Batch log shipments
   - Sample high-volume logs
   - Avoid logging in hot paths

4. **Security**
   - Never log passwords or tokens
   - Redact PII automatically
   - Separate audit logs
   - Encrypt logs in transit

5. **Cost Management**
   - Set retention policies
   - Use log sampling
   - Compress before storage
   - Monitor log volume

## 🚀 Next Steps

1. Implement [Distributed Tracing](https://opentelemetry.io)
2. Set up [Log Analysis](https://www.elastic.co/kibana)
3. Configure [Alert Rules](#monitoring--alerts)
4. Create [Custom Dashboards](#log-metrics-dashboard)

---

**Remember**: Logs are your window into production. Make them structured, secure, and actionable.
