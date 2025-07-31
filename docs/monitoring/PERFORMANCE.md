# Performance Monitoring Guide

> Comprehensive performance monitoring to ensure fast, responsive applications

## 🎯 Overview

This guide covers monitoring and optimizing performance across your entire stack - from Core Web Vitals to API response times and database queries.

## 📊 Key Metrics to Monitor

### Core Web Vitals (User Experience)

| Metric | Target | What It Measures |
|--------|--------|------------------|
| **LCP** (Largest Contentful Paint) | < 2.5s | Loading performance |
| **FID** (First Input Delay) | < 100ms | Interactivity |
| **CLS** (Cumulative Layout Shift) | < 0.1 | Visual stability |
| **TTFB** (Time to First Byte) | < 600ms | Server response time |
| **FCP** (First Contentful Paint) | < 1.8s | Perceived load speed |

### Application Metrics

- **API Response Times**: p50 < 200ms, p95 < 1s
- **Database Query Time**: < 100ms for 95% of queries
- **Bundle Size**: < 300KB compressed
- **Time to Interactive**: < 3.8s
- **Memory Usage**: < 128MB
- **Error Rate**: < 1%

## 🚀 Implementation

### 1. Vercel Analytics (Built-in)

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
```

### 2. Custom Performance Monitoring

```typescript
// lib/performance/monitor.ts
export class PerformanceMonitor {
  private static instance: PerformanceMonitor;
  private metrics: Map<string, number[]> = new Map();
  
  static getInstance() {
    if (!this.instance) {
      this.instance = new PerformanceMonitor();
    }
    return this.instance;
  }
  
  // Measure Core Web Vitals
  initWebVitals() {
    if (typeof window === 'undefined') return;
    
    // LCP
    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      const lastEntry = entries[entries.length - 1];
      this.record('lcp', lastEntry.startTime);
    }).observe({ entryTypes: ['largest-contentful-paint'] });
    
    // FID
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if ('processingStart' in entry) {
          const fid = entry.processingStart - entry.startTime;
          this.record('fid', fid);
        }
      }
    }).observe({ entryTypes: ['first-input'] });
    
    // CLS
    let clsValue = 0;
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) {
          clsValue += entry.value;
          this.record('cls', clsValue);
        }
      }
    }).observe({ entryTypes: ['layout-shift'] });
    
    // Custom metrics
    this.measureNavigationTiming();
  }
  
  // Record custom metrics
  record(metric: string, value: number) {
    if (!this.metrics.has(metric)) {
      this.metrics.set(metric, []);
    }
    this.metrics.get(metric)!.push(value);
    
    // Send to analytics
    this.reportMetric(metric, value);
  }
  
  // Measure API calls
  async measureAPI<T>(
    name: string,
    fn: () => Promise<T>
  ): Promise<T> {
    const start = performance.now();
    try {
      const result = await fn();
      const duration = performance.now() - start;
      this.record(`api_${name}`, duration);
      return result;
    } catch (error) {
      const duration = performance.now() - start;
      this.record(`api_${name}_error`, duration);
      throw error;
    }
  }
  
  // Report to analytics
  private reportMetric(metric: string, value: number) {
    // Report to your analytics service
    if (window.plausible) {
      window.plausible('performance', {
        props: {
          metric,
          value: Math.round(value),
          page: window.location.pathname,
        }
      });
    }
    
    // Also log to console in dev
    if (process.env.NODE_ENV === 'development') {
      console.log(`[Performance] ${metric}: ${value.toFixed(2)}ms`);
    }
  }
  
  // Get percentiles
  getPercentile(metric: string, percentile: number): number | null {
    const values = this.metrics.get(metric);
    if (!values || values.length === 0) return null;
    
    const sorted = [...values].sort((a, b) => a - b);
    const index = Math.ceil((percentile / 100) * sorted.length) - 1;
    return sorted[index];
  }
  
  // Navigation timing
  private measureNavigationTiming() {
    if (typeof window === 'undefined') return;
    
    window.addEventListener('load', () => {
      setTimeout(() => {
        const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
        
        // Key metrics
        this.record('ttfb', navigation.responseStart - navigation.requestStart);
        this.record('dom_load', navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart);
        this.record('window_load', navigation.loadEventEnd - navigation.loadEventStart);
        this.record('total_load', navigation.loadEventEnd - navigation.fetchStart);
      }, 0);
    });
  }
}

// Initialize on client
if (typeof window !== 'undefined') {
  const monitor = PerformanceMonitor.getInstance();
  monitor.initWebVitals();
}
```

### 3. API Performance Monitoring

```typescript
// lib/api/performance.ts
import { PerformanceMonitor } from '@/lib/performance/monitor';

const monitor = PerformanceMonitor.getInstance();

// Middleware for API routes
export function withPerformanceMonitoring(
  handler: Function,
  routeName: string
) {
  return async (req: Request, ...args: any[]) => {
    const start = performance.now();
    
    try {
      const response = await handler(req, ...args);
      const duration = performance.now() - start;
      
      // Record metrics
      monitor.record(`api_route_${routeName}`, duration);
      
      // Add timing header
      if (response instanceof Response) {
        response.headers.set('X-Response-Time', `${duration.toFixed(2)}ms`);
      }
      
      return response;
    } catch (error) {
      const duration = performance.now() - start;
      monitor.record(`api_route_${routeName}_error`, duration);
      throw error;
    }
  };
}

// Usage
export const GET = withPerformanceMonitoring(
  async (request: Request) => {
    // Your API logic
    return Response.json({ data: 'example' });
  },
  'get_users'
);
```

### 4. Database Query Monitoring

```typescript
// lib/db/performance.ts
import { db } from './client';
import { PerformanceMonitor } from '@/lib/performance/monitor';

const monitor = PerformanceMonitor.getInstance();

export function monitoredQuery<T>(
  queryName: string,
  queryFn: () => Promise<T>
): Promise<T> {
  return monitor.measureAPI(`db_${queryName}`, queryFn);
}

// Usage with Drizzle
export async function getUserById(id: string) {
  return monitoredQuery('get_user_by_id', async () => {
    return await db.query.users.findFirst({
      where: eq(users.id, id),
    });
  });
}

// Batch monitoring
export async function monitorBatchOperation<T>(
  operations: Array<() => Promise<T>>,
  batchName: string
): Promise<T[]> {
  const start = performance.now();
  
  try {
    const results = await Promise.all(
      operations.map((op, index) => 
        monitor.measureAPI(`${batchName}_${index}`, op)
      )
    );
    
    const duration = performance.now() - start;
    monitor.record(`batch_${batchName}`, duration);
    
    return results;
  } catch (error) {
    const duration = performance.now() - start;
    monitor.record(`batch_${batchName}_error`, duration);
    throw error;
  }
}
```

### 5. Component Performance Monitoring

```typescript
// hooks/useComponentPerformance.ts
import { useEffect, useRef } from 'react';
import { PerformanceMonitor } from '@/lib/performance/monitor';

export function useComponentPerformance(componentName: string) {
  const monitor = PerformanceMonitor.getInstance();
  const renderStart = useRef<number>();
  const hasMeasured = useRef(false);
  
  // Measure render time
  if (!renderStart.current) {
    renderStart.current = performance.now();
  }
  
  useEffect(() => {
    if (!hasMeasured.current) {
      const renderTime = performance.now() - renderStart.current!;
      monitor.record(`component_render_${componentName}`, renderTime);
      hasMeasured.current = true;
    }
    
    // Measure hydration time
    if (typeof window !== 'undefined') {
      const hydrationTime = performance.now();
      monitor.record(`component_hydration_${componentName}`, hydrationTime);
    }
  }, [componentName, monitor]);
  
  // Measure interaction time
  const measureInteraction = (interactionName: string) => {
    return (fn: Function) => {
      return async (...args: any[]) => {
        const start = performance.now();
        try {
          const result = await fn(...args);
          const duration = performance.now() - start;
          monitor.record(`interaction_${componentName}_${interactionName}`, duration);
          return result;
        } catch (error) {
          monitor.record(`interaction_${componentName}_${interactionName}_error`, 1);
          throw error;
        }
      };
    };
  };
  
  return { measureInteraction };
}

// Usage
function ExpensiveComponent() {
  const { measureInteraction } = useComponentPerformance('ExpensiveComponent');
  
  const handleClick = measureInteraction('button_click')(async () => {
    // Expensive operation
    await processData();
  });
  
  return <button onClick={handleClick}>Process</button>;
}
```

## 📈 Performance Budgets

### Setting Budgets

```typescript
// performance.config.ts
export const PERFORMANCE_BUDGETS = {
  // Page weight budgets
  bundles: {
    main: 250 * 1024,        // 250KB
    vendor: 150 * 1024,      // 150KB
    total: 500 * 1024,       // 500KB total
  },
  
  // Timing budgets
  timing: {
    fcp: 1800,               // 1.8s
    lcp: 2500,               // 2.5s
    tti: 3800,               // 3.8s
    fid: 100,                // 100ms
    cls: 0.1,                // 0.1
  },
  
  // API budgets
  api: {
    p50: 200,                // 200ms median
    p95: 1000,               // 1s 95th percentile
    p99: 2000,               // 2s 99th percentile
  },
  
  // Resource counts
  resources: {
    images: 20,
    scripts: 10,
    stylesheets: 5,
    fonts: 3,
  },
};

// Budget enforcement
export function checkPerformanceBudget(metrics: any) {
  const violations = [];
  
  // Check bundle sizes
  if (metrics.bundleSize > PERFORMANCE_BUDGETS.bundles.total) {
    violations.push({
      type: 'bundle_size',
      actual: metrics.bundleSize,
      budget: PERFORMANCE_BUDGETS.bundles.total,
    });
  }
  
  // Check Core Web Vitals
  if (metrics.lcp > PERFORMANCE_BUDGETS.timing.lcp) {
    violations.push({
      type: 'lcp',
      actual: metrics.lcp,
      budget: PERFORMANCE_BUDGETS.timing.lcp,
    });
  }
  
  return violations;
}
```

### Build-Time Budget Enforcement

```typescript
// scripts/check-bundle-size.ts
import { PERFORMANCE_BUDGETS } from '../performance.config';
import fs from 'fs';
import path from 'path';

const BUILD_DIR = '.next';

function getBundleSize(dir: string): number {
  let totalSize = 0;
  
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      totalSize += getBundleSize(filePath);
    } else if (file.endsWith('.js') || file.endsWith('.css')) {
      totalSize += stat.size;
    }
  }
  
  return totalSize;
}

const bundleSize = getBundleSize(BUILD_DIR);
const budgetViolation = bundleSize > PERFORMANCE_BUDGETS.bundles.total;

if (budgetViolation) {
  console.error(`❌ Bundle size budget exceeded!`);
  console.error(`   Budget: ${PERFORMANCE_BUDGETS.bundles.total / 1024}KB`);
  console.error(`   Actual: ${bundleSize / 1024}KB`);
  process.exit(1);
} else {
  console.log(`✅ Bundle size within budget: ${bundleSize / 1024}KB`);
}
```

## 🔍 Real User Monitoring (RUM)

### Custom RUM Implementation

```typescript
// lib/rum/index.ts
interface RUMConfig {
  sampleRate: number;
  endpoint: string;
  sessionTimeout: number;
}

class RealUserMonitoring {
  private config: RUMConfig;
  private sessionId: string;
  private metrics: any[] = [];
  private flushTimer?: NodeJS.Timeout;
  
  constructor(config: RUMConfig) {
    this.config = config;
    this.sessionId = this.getOrCreateSession();
    this.init();
  }
  
  private init() {
    if (typeof window === 'undefined') return;
    
    // Should we sample this session?
    if (Math.random() > this.config.sampleRate) return;
    
    // Web Vitals
    this.observeWebVitals();
    
    // Navigation
    this.observeNavigation();
    
    // Resources
    this.observeResources();
    
    // Errors
    this.observeErrors();
    
    // Flush periodically
    this.flushTimer = setInterval(() => this.flush(), 30000);
    
    // Flush on page hide
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) this.flush();
    });
  }
  
  private observeWebVitals() {
    // Use web-vitals library
    import('web-vitals').then(({ onCLS, onFID, onLCP, onFCP, onTTFB }) => {
      onCLS((metric) => this.addMetric('cls', metric));
      onFID((metric) => this.addMetric('fid', metric));
      onLCP((metric) => this.addMetric('lcp', metric));
      onFCP((metric) => this.addMetric('fcp', metric));
      onTTFB((metric) => this.addMetric('ttfb', metric));
    });
  }
  
  private observeNavigation() {
    // Page views
    let lastPath = window.location.pathname;
    const observer = new MutationObserver(() => {
      if (window.location.pathname !== lastPath) {
        this.addMetric('navigation', {
          from: lastPath,
          to: window.location.pathname,
          timestamp: Date.now(),
        });
        lastPath = window.location.pathname;
      }
    });
    
    observer.observe(document, { subtree: true, childList: true });
  }
  
  private observeResources() {
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.entryType === 'resource') {
          const resource = entry as PerformanceResourceTiming;
          
          // Only track slow resources
          if (resource.duration > 1000) {
            this.addMetric('slow_resource', {
              name: resource.name,
              duration: resource.duration,
              size: resource.transferSize,
              type: resource.initiatorType,
            });
          }
        }
      }
    });
    
    observer.observe({ entryTypes: ['resource'] });
  }
  
  private observeErrors() {
    window.addEventListener('error', (event) => {
      this.addMetric('js_error', {
        message: event.message,
        source: event.filename,
        line: event.lineno,
        column: event.colno,
        stack: event.error?.stack,
      });
    });
    
    window.addEventListener('unhandledrejection', (event) => {
      this.addMetric('unhandled_rejection', {
        reason: event.reason,
        promise: event.promise,
      });
    });
  }
  
  private addMetric(type: string, data: any) {
    this.metrics.push({
      type,
      data,
      timestamp: Date.now(),
      sessionId: this.sessionId,
      page: window.location.pathname,
      userAgent: navigator.userAgent,
    });
    
    // Flush if buffer is getting large
    if (this.metrics.length >= 50) {
      this.flush();
    }
  }
  
  private async flush() {
    if (this.metrics.length === 0) return;
    
    const metricsToSend = [...this.metrics];
    this.metrics = [];
    
    try {
      await fetch(this.config.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ metrics: metricsToSend }),
      });
    } catch (error) {
      // Re-add metrics on failure
      this.metrics.unshift(...metricsToSend);
    }
  }
  
  private getOrCreateSession(): string {
    const stored = sessionStorage.getItem('rum_session');
    if (stored) return stored;
    
    const sessionId = `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    sessionStorage.setItem('rum_session', sessionId);
    return sessionId;
  }
}

// Initialize RUM
export const rum = new RealUserMonitoring({
  sampleRate: 0.1, // 10% of sessions
  endpoint: '/api/rum',
  sessionTimeout: 30 * 60 * 1000, // 30 minutes
});
```

## 🚀 Optimization Strategies

### 1. Bundle Optimization

```typescript
// next.config.js
module.exports = {
  // Enable SWC minification
  swcMinify: true,
  
  // Optimize images
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 1080, 1200, 1920],
  },
  
  // Module federation for large apps
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['lodash', 'date-fns'],
  },
  
  // Webpack optimization
  webpack: (config, { isServer }) => {
    if (!isServer) {
      // Replace react with preact in production
      if (process.env.NODE_ENV === 'production') {
        Object.assign(config.resolve.alias, {
          'react': 'preact/compat',
          'react-dom': 'preact/compat',
        });
      }
    }
    
    return config;
  },
};
```

### 2. Code Splitting

```typescript
// Dynamic imports for heavy components
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Skeleton />,
  ssr: false,
});

// Route-based splitting
const AdminDashboard = lazy(() => import('./AdminDashboard'));

// Conditional loading
function ConditionalLoad({ shouldLoad, children }) {
  const [Component, setComponent] = useState(null);
  
  useEffect(() => {
    if (shouldLoad) {
      import('./ExpensiveComponent').then((mod) => {
        setComponent(() => mod.default);
      });
    }
  }, [shouldLoad]);
  
  if (!shouldLoad || !Component) return children;
  return <Component />;
}
```

### 3. Resource Hints

```typescript
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        {/* Preconnect to external domains */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="dns-prefetch" href="https://analytics.example.com" />
        
        {/* Preload critical resources */}
        <link
          rel="preload"
          href="/fonts/inter-var.woff2"
          as="font"
          type="font/woff2"
          crossOrigin="anonymous"
        />
        
        {/* Prefetch next page */}
        <link rel="prefetch" href="/dashboard" />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

## 📊 Performance Dashboard

### Creating a Performance Dashboard

```typescript
// app/admin/performance/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { PerformanceMonitor } from '@/lib/performance/monitor';

export default function PerformanceDashboard() {
  const [metrics, setMetrics] = useState<any>({});
  const monitor = PerformanceMonitor.getInstance();
  
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics({
        lcp: {
          p50: monitor.getPercentile('lcp', 50),
          p75: monitor.getPercentile('lcp', 75),
          p95: monitor.getPercentile('lcp', 95),
        },
        fid: {
          p50: monitor.getPercentile('fid', 50),
          p75: monitor.getPercentile('fid', 75),
          p95: monitor.getPercentile('fid', 95),
        },
        cls: {
          p50: monitor.getPercentile('cls', 50),
          p75: monitor.getPercentile('cls', 75),
          p95: monitor.getPercentile('cls', 95),
        },
        api: {
          p50: monitor.getPercentile('api_all', 50),
          p95: monitor.getPercentile('api_all', 95),
          p99: monitor.getPercentile('api_all', 99),
        },
      });
    }, 5000);
    
    return () => clearInterval(interval);
  }, [monitor]);
  
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Performance Dashboard</h1>
      
      <div className="grid grid-cols-3 gap-6">
        <MetricCard
          title="Largest Contentful Paint"
          metrics={metrics.lcp}
          unit="ms"
          thresholds={{ good: 2500, poor: 4000 }}
        />
        
        <MetricCard
          title="First Input Delay"
          metrics={metrics.fid}
          unit="ms"
          thresholds={{ good: 100, poor: 300 }}
        />
        
        <MetricCard
          title="Cumulative Layout Shift"
          metrics={metrics.cls}
          unit=""
          thresholds={{ good: 0.1, poor: 0.25 }}
        />
      </div>
      
      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-4">API Performance</h2>
        <div className="grid grid-cols-3 gap-6">
          <StatCard
            label="Median Response Time"
            value={`${metrics.api?.p50?.toFixed(0) || '-'}ms`}
            status={metrics.api?.p50 < 200 ? 'good' : 'warning'}
          />
          <StatCard
            label="95th Percentile"
            value={`${metrics.api?.p95?.toFixed(0) || '-'}ms`}
            status={metrics.api?.p95 < 1000 ? 'good' : 'warning'}
          />
          <StatCard
            label="99th Percentile"
            value={`${metrics.api?.p99?.toFixed(0) || '-'}ms`}
            status={metrics.api?.p99 < 2000 ? 'good' : 'poor'}
          />
        </div>
      </div>
    </div>
  );
}
```

## 🔧 Troubleshooting Performance Issues

### Common Issues and Solutions

1. **Slow Initial Load**
   - Check bundle size with `next build && next-bundle-analyzer`
   - Enable compression in Vercel
   - Lazy load non-critical components
   - Optimize images with next/image

2. **Poor Interactivity**
   - Reduce JavaScript execution time
   - Use React.memo for expensive components
   - Implement virtual scrolling for long lists
   - Debounce user inputs

3. **Layout Shifts**
   - Set explicit dimensions for images/videos
   - Reserve space for dynamic content
   - Avoid inserting content above existing content
   - Use CSS aspect-ratio for responsive media

4. **Slow API Responses**
   - Implement caching strategies
   - Use database indexes
   - Enable query result caching
   - Consider edge functions for geo-distribution

## 🎯 Best Practices

1. **Monitor Early and Often**
   - Set up monitoring before launch
   - Track performance in development
   - Create performance budgets
   - Regular performance reviews

2. **Focus on User Experience**
   - Prioritize metrics that users feel
   - Optimize for real devices
   - Test on slow connections
   - Consider international users

3. **Automate Performance Checks**
   - CI/CD performance tests
   - Automated budget enforcement
   - Performance regression alerts
   - Regular performance audits

## 🚀 Next Steps

1. Set up [RUM Dashboard](#rum-dashboard)
2. Configure [Performance Budgets](#performance-budgets)
3. Implement [Synthetic Monitoring](https://checkly.com)
4. Enable [CDN and Edge Caching](../deployment/CDN_SETUP.md)

---

**Remember**: Performance is a feature, not an afterthought. A fast site is a successful site.
