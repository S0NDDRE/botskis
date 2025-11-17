/**
 * Billing Service
 * Handles all subscription, payment, and invoice operations
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class BillingService {
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
   * Get current subscription
   */
  async getSubscription() {
    return this.request('/api/v1/billing/subscription');
  }

  /**
   * Update subscription (upgrade/downgrade)
   */
  async updateSubscription(newPlan: string) {
    return this.request('/api/v1/billing/subscription', {
      method: 'PUT',
      body: JSON.stringify({ plan: newPlan }),
    });
  }

  /**
   * Cancel subscription
   */
  async cancelSubscription(reason: string) {
    return this.request('/api/v1/billing/subscription/cancel', {
      method: 'POST',
      body: JSON.stringify({ reason }),
    });
  }

  /**
   * Reactivate canceled subscription
   */
  async reactivateSubscription() {
    return this.request('/api/v1/billing/subscription/reactivate', {
      method: 'POST',
    });
  }

  /**
   * Get all payment methods
   */
  async getPaymentMethods() {
    return this.request('/api/v1/billing/payment-methods');
  }

  /**
   * Add new payment method
   */
  async addPaymentMethod(paymentMethodData: any) {
    return this.request('/api/v1/billing/payment-methods', {
      method: 'POST',
      body: JSON.stringify(paymentMethodData),
    });
  }

  /**
   * Set default payment method
   */
  async setDefaultPaymentMethod(paymentMethodId: string) {
    return this.request(`/api/v1/billing/payment-methods/${paymentMethodId}/default`, {
      method: 'PUT',
    });
  }

  /**
   * Remove payment method
   */
  async removePaymentMethod(paymentMethodId: string) {
    return this.request(`/api/v1/billing/payment-methods/${paymentMethodId}`, {
      method: 'DELETE',
    });
  }

  /**
   * Get invoice history
   */
  async getInvoices(limit: number = 12) {
    return this.request(`/api/v1/billing/invoices?limit=${limit}`);
  }

  /**
   * Get specific invoice
   */
  async getInvoice(invoiceId: string) {
    return this.request(`/api/v1/billing/invoices/${invoiceId}`);
  }

  /**
   * Download invoice PDF
   */
  async downloadInvoice(invoiceId: string) {
    const token = localStorage.getItem('auth_token');
    const response = await fetch(`${API_BASE_URL}/api/v1/billing/invoices/${invoiceId}/pdf`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to download invoice');
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `invoice-${invoiceId}.pdf`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }

  /**
   * Get usage statistics
   */
  async getUsage() {
    return this.request('/api/v1/billing/usage');
  }

  /**
   * Get available plans
   */
  async getPlans() {
    return this.request('/api/v1/billing/plans');
  }
}

export const billingService = new BillingService();
