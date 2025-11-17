/**
 * Admin Service
 * Handles all administrative operations
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class AdminService {
  private async request(endpoint: string, options: RequestInit = {}) {
    const token = localStorage.getItem('auth_token');
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Request failed');
    }

    return response.json();
  }

  /**
   * Get business metrics (MRR, ARR, churn, etc.)
   */
  async getMetrics() {
    return this.request('/api/v1/admin/metrics');
  }

  /**
   * Get all customers
   */
  async getCustomers(params?: {
    page?: number;
    limit?: number;
    status?: string;
    plan?: string;
    search?: string;
  }) {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, String(value));
        }
      });
    }
    return this.request(`/api/v1/admin/customers?${queryParams.toString()}`);
  }

  /**
   * Get specific customer details
   */
  async getCustomer(customerId: string) {
    return this.request(`/api/v1/admin/customers/${customerId}`);
  }

  /**
   * Update customer
   */
  async updateCustomer(customerId: string, data: any) {
    return this.request(`/api/v1/admin/customers/${customerId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  /**
   * Get system health metrics
   */
  async getSystemHealth() {
    return this.request('/api/v1/admin/system/health');
  }

  /**
   * Get detailed system metrics
   */
  async getSystemMetrics(timeRange: '1h' | '24h' | '7d' | '30d' = '24h') {
    return this.request(`/api/v1/admin/system/metrics?range=${timeRange}`);
  }

  /**
   * Get support tickets
   */
  async getSupportTickets(params?: {
    status?: 'open' | 'pending' | 'resolved';
    priority?: 'low' | 'medium' | 'high' | 'urgent';
    limit?: number;
  }) {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, String(value));
        }
      });
    }
    return this.request(`/api/v1/admin/support/tickets?${queryParams.toString()}`);
  }

  /**
   * Get specific ticket
   */
  async getTicket(ticketId: string) {
    return this.request(`/api/v1/admin/support/tickets/${ticketId}`);
  }

  /**
   * Update ticket status
   */
  async updateTicket(ticketId: string, data: { status?: string; priority?: string; notes?: string }) {
    return this.request(`/api/v1/admin/support/tickets/${ticketId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  /**
   * Get revenue analytics
   */
  async getRevenueAnalytics(timeRange: '7d' | '30d' | '90d' | '1y' = '30d') {
    return this.request(`/api/v1/admin/analytics/revenue?range=${timeRange}`);
  }

  /**
   * Get usage analytics
   */
  async getUsageAnalytics() {
    return this.request('/api/v1/admin/analytics/usage');
  }

  /**
   * Get churn analytics
   */
  async getChurnAnalytics() {
    return this.request('/api/v1/admin/analytics/churn');
  }

  /**
   * Export customer data
   */
  async exportCustomers(format: 'csv' | 'xlsx' = 'csv') {
    const token = localStorage.getItem('auth_token');
    const response = await fetch(`${API_BASE_URL}/api/v1/admin/export/customers?format=${format}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to export data');
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `customers-${new Date().toISOString()}.${format}`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }

  /**
   * Get activity log
   */
  async getActivityLog(params?: {
    page?: number;
    limit?: number;
    user_id?: string;
    action_type?: string;
  }) {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, String(value));
        }
      });
    }
    return this.request(`/api/v1/admin/activity-log?${queryParams.toString()}`);
  }

  /**
   * Get system alerts
   */
  async getAlerts(params?: { status?: 'active' | 'resolved'; severity?: 'low' | 'medium' | 'high' | 'critical' }) {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, String(value));
        }
      });
    }
    return this.request(`/api/v1/admin/alerts?${queryParams.toString()}`);
  }

  /**
   * Acknowledge/resolve alert
   */
  async resolveAlert(alertId: string) {
    return this.request(`/api/v1/admin/alerts/${alertId}/resolve`, {
      method: 'POST',
    });
  }
}

export const adminService = new AdminService();
