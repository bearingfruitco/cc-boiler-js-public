/**
 * Supabase MCP Connector
 * Provides direct database operations for agents
 */

require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');

class SupabaseMCP {
  constructor() {
    this.client = null;
    this.connected = false;
  }

  async connect() {
    try {
      const url = process.env.SUPABASE_URL;
      const key = process.env.SUPABASE_SERVICE_KEY || process.env.SUPABASE_ANON_KEY;

      if (!url || !key) {
        throw new Error('Missing Supabase credentials');
      }

      this.client = createClient(url, key);
      this.connected = true;
      
      console.log('✅ Supabase MCP connected');
      return true;
    } catch (error) {
      console.error('❌ Supabase MCP connection failed:', error.message);
      return false;
    }
  }

  async testConnection() {
    if (!this.connected) {
      await this.connect();
    }

    try {
      // Test with a simple query
      const { data, error } = await this.client
        .from('_test_connection')
        .select('*')
        .limit(1);

      if (error && error.code !== 'PGRST116') {
        // PGRST116 is "table not found" which is OK for test
        throw error;
      }

      return {
        success: true,
        message: 'Supabase connection successful',
        capabilities: [
          'database:crud',
          'auth:management',
          'storage:files',
          'realtime:subscriptions',
          'rls:policies'
        ]
      };
    } catch (error) {
      return {
        success: false,
        message: error.message
      };
    }
  }

  // Database operations
  async query(table, options = {}) {
    const query = this.client.from(table);
    
    if (options.select) query.select(options.select);
    if (options.filter) {
      Object.entries(options.filter).forEach(([key, value]) => {
        query.eq(key, value);
      });
    }
    if (options.limit) query.limit(options.limit);
    if (options.order) query.order(options.order);
    
    return await query;
  }

  async insert(table, data) {
    return await this.client.from(table).insert(data);
  }

  async update(table, data, filter) {
    const query = this.client.from(table).update(data);
    Object.entries(filter).forEach(([key, value]) => {
      query.eq(key, value);
    });
    return await query;
  }

  async delete(table, filter) {
    const query = this.client.from(table).delete();
    Object.entries(filter).forEach(([key, value]) => {
      query.eq(key, value);
    });
    return await query;
  }

  // RLS operations
  async getRLSPolicies(table) {
    const { data, error } = await this.client.rpc('get_rls_policies', {
      table_name: table
    });
    return { data, error };
  }

  async createRLSPolicy(table, policy) {
    // Implementation for creating RLS policies
    const sql = `
      CREATE POLICY "${policy.name}" ON ${table}
      FOR ${policy.operation}
      TO ${policy.role}
      USING (${policy.using})
      WITH CHECK (${policy.withCheck});
    `;
    
    return await this.client.rpc('exec_sql', { sql });
  }

  // Auth operations
  async createUser(email, password, metadata = {}) {
    return await this.client.auth.admin.createUser({
      email,
      password,
      user_metadata: metadata
    });
  }

  async listUsers() {
    return await this.client.auth.admin.listUsers();
  }

  // Storage operations
  async uploadFile(bucket, path, file) {
    return await this.client.storage
      .from(bucket)
      .upload(path, file);
  }

  async downloadFile(bucket, path) {
    return await this.client.storage
      .from(bucket)
      .download(path);
  }

  // Realtime subscriptions
  subscribeToTable(table, callback) {
    return this.client
      .channel(`table-${table}`)
      .on('postgres_changes', 
        { event: '*', schema: 'public', table },
        callback
      )
      .subscribe();
  }
}

module.exports = SupabaseMCP;
