import { Redis } from '@upstash/redis';

// Initialize Redis client
export const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!,
});

// Type-safe cache operations
export const cache = {
  // Get a value from cache
  async get<T>(key: string): Promise<T | null> {
    try {
      const value = await redis.get<T>(key);
      return value;
    } catch (error) {
      console.error(`Cache get error for key ${key}:`, error);
      return null;
    }
  },

  // Set a value in cache with optional TTL (in seconds)
  async set<T>(key: string, value: T, ttl?: number): Promise<boolean> {
    try {
      if (ttl) {
        await redis.setex(key, ttl, value);
      } else {
        await redis.set(key, value);
      }
      return true;
    } catch (error) {
      console.error(`Cache set error for key ${key}:`, error);
      return false;
    }
  },

  // Delete a value from cache
  async delete(key: string): Promise<boolean> {
    try {
      const result = await redis.del(key);
      return result === 1;
    } catch (error) {
      console.error(`Cache delete error for key ${key}:`, error);
      return false;
    }
  },

  // Check if a key exists
  async exists(key: string): Promise<boolean> {
    try {
      const result = await redis.exists(key);
      return result === 1;
    } catch (error) {
      console.error(`Cache exists error for key ${key}:`, error);
      return false;
    }
  },

  // Increment a counter
  async increment(key: string, amount = 1): Promise<number | null> {
    try {
      const result = await redis.incrby(key, amount);
      return result;
    } catch (error) {
      console.error(`Cache increment error for key ${key}:`, error);
      return null;
    }
  },

  // Set multiple values at once
  async setMany(entries: Array<{ key: string; value: any; ttl?: number }>): Promise<boolean> {
    try {
      const pipeline = redis.pipeline();
      
      for (const { key, value, ttl } of entries) {
        if (ttl) {
          pipeline.setex(key, ttl, value);
        } else {
          pipeline.set(key, value);
        }
      }
      
      await pipeline.exec();
      return true;
    } catch (error) {
      console.error('Cache setMany error:', error);
      return false;
    }
  },

  // Get multiple values at once
  async getMany<T>(keys: string[]): Promise<(T | null)[]> {
    try {
      const pipeline = redis.pipeline();
      
      for (const key of keys) {
        pipeline.get(key);
      }
      
      const results = await pipeline.exec();
      return results.map(result => result[1] as T | null);
    } catch (error) {
      console.error('Cache getMany error:', error);
      return keys.map(() => null);
    }
  },
};

// Rate limiting helper
export async function checkRateLimit(
  identifier: string,
  limit: number,
  window: number // in seconds
): Promise<{ allowed: boolean; remaining: number; reset: number }> {
  const key = `rate_limit:${identifier}`;
  const now = Date.now();
  const windowStart = now - window * 1000;

  try {
    // Remove old entries
    await redis.zremrangebyscore(key, 0, windowStart);
    
    // Count current entries
    const count = await redis.zcard(key);
    
    if (count < limit) {
      // Add current request
      await redis.zadd(key, { score: now, member: now });
      await redis.expire(key, window);
      
      return {
        allowed: true,
        remaining: limit - count - 1,
        reset: Math.floor((now + window * 1000) / 1000),
      };
    }
    
    // Get oldest entry to determine reset time
    const oldest = await redis.zrange(key, 0, 0, { withScores: true });
    const reset = oldest.length > 0 
      ? Math.floor((oldest[0].score + window * 1000) / 1000)
      : Math.floor((now + window * 1000) / 1000);
    
    return {
      allowed: false,
      remaining: 0,
      reset,
    };
  } catch (error) {
    console.error('Rate limit check error:', error);
    // Allow on error to prevent blocking users
    return {
      allowed: true,
      remaining: limit,
      reset: Math.floor((now + window * 1000) / 1000),
    };
  }
}
