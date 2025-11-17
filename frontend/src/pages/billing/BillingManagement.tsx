/**
 * Billing Management UI
 * Self-service subscription, payment, and invoice management
 */
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { billingService } from '../../services/billing';

interface Subscription {
  id: string;
  plan: string;
  status: 'active' | 'canceled' | 'past_due' | 'trialing';
  amount: number;
  currency: string;
  interval: 'month' | 'year';
  current_period_start: string;
  current_period_end: string;
  cancel_at_period_end: boolean;
  trial_end?: string;
}

interface PaymentMethod {
  id: string;
  type: 'card' | 'vipps';
  last4?: string;
  brand?: string;
  exp_month?: number;
  exp_year?: number;
  phone?: string;
  is_default: boolean;
}

interface Invoice {
  id: string;
  number: string;
  amount: number;
  currency: string;
  status: 'paid' | 'pending' | 'failed';
  created: string;
  pdf_url: string;
}

export const BillingManagement: React.FC = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([]);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [activeTab, setActiveTab] = useState<'overview' | 'payment' | 'invoices' | 'cancel'>('overview');
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [showAddPaymentModal, setShowAddPaymentModal] = useState(false);
  const [showCancelModal, setShowCancelModal] = useState(false);

  useEffect(() => {
    loadBillingData();
  }, []);

  const loadBillingData = async () => {
    try {
      setLoading(true);
      const [subData, pmData, invData] = await Promise.all([
        billingService.getSubscription(),
        billingService.getPaymentMethods(),
        billingService.getInvoices()
      ]);
      setSubscription(subData);
      setPaymentMethods(pmData);
      setInvoices(invData);
    } catch (error) {
      console.error('Failed to load billing data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpgrade = async (newPlan: string) => {
    try {
      await billingService.updateSubscription(newPlan);
      await loadBillingData();
      setShowUpgradeModal(false);
    } catch (error) {
      console.error('Failed to upgrade:', error);
    }
  };

  const handleCancelSubscription = async (reason: string) => {
    try {
      await billingService.cancelSubscription(reason);
      await loadBillingData();
      setShowCancelModal(false);
    } catch (error) {
      console.error('Failed to cancel:', error);
    }
  };

  const handleSetDefaultPayment = async (paymentMethodId: string) => {
    try {
      await billingService.setDefaultPaymentMethod(paymentMethodId);
      await loadBillingData();
    } catch (error) {
      console.error('Failed to set default payment:', error);
    }
  };

  const handleRemovePayment = async (paymentMethodId: string) => {
    try {
      await billingService.removePaymentMethod(paymentMethodId);
      await loadBillingData();
    } catch (error) {
      console.error('Failed to remove payment:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="billing-management max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Billing & Subscription</h1>
        <p className="text-gray-600">Manage your subscription, payment methods, and invoices</p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex space-x-8">
          <button
            onClick={() => setActiveTab('overview')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'overview'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab('payment')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'payment'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Payment Methods
          </button>
          <button
            onClick={() => setActiveTab('invoices')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'invoices'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Invoices
          </button>
          <button
            onClick={() => setActiveTab('cancel')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'cancel'
                ? 'border-red-600 text-red-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Cancel Subscription
          </button>
        </nav>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && subscription && (
        <div className="space-y-6">
          {/* Current Plan */}
          <div className="bg-white border rounded-lg p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-xl font-bold mb-2">Current Plan</h2>
                <div className="flex items-center space-x-3">
                  <span className="text-3xl font-bold text-blue-600">{subscription.plan}</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    subscription.status === 'active' ? 'bg-green-100 text-green-800' :
                    subscription.status === 'trialing' ? 'bg-blue-100 text-blue-800' :
                    subscription.status === 'past_due' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {subscription.status.toUpperCase()}
                  </span>
                </div>
              </div>
              <button
                onClick={() => setShowUpgradeModal(true)}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-700"
              >
                Change Plan
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4 mt-6">
              <div>
                <p className="text-sm text-gray-600">Amount</p>
                <p className="text-lg font-semibold">
                  {subscription.currency.toUpperCase()} {(subscription.amount / 100).toFixed(2)} / {subscription.interval}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Next billing date</p>
                <p className="text-lg font-semibold">
                  {new Date(subscription.current_period_end).toLocaleDateString()}
                </p>
              </div>
              {subscription.trial_end && (
                <div>
                  <p className="text-sm text-gray-600">Trial ends</p>
                  <p className="text-lg font-semibold text-blue-600">
                    {new Date(subscription.trial_end).toLocaleDateString()}
                  </p>
                </div>
              )}
              {subscription.cancel_at_period_end && (
                <div className="col-span-2">
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                    <p className="text-sm text-yellow-800">
                      ⚠️ Your subscription will be canceled on {new Date(subscription.current_period_end).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Usage Stats */}
          <div className="bg-white border rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">Current Usage</h2>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm text-gray-600">AI Requests</span>
                  <span className="text-sm font-semibold">7,342 / 10,000</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full" style={{ width: '73%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm text-gray-600">Active Agents</span>
                  <span className="text-sm font-semibold">12 / 20</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-green-600 h-2 rounded-full" style={{ width: '60%' }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Payment Methods Tab */}
      {activeTab === 'payment' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-bold">Payment Methods</h2>
            <button
              onClick={() => setShowAddPaymentModal(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-700"
            >
              + Add Payment Method
            </button>
          </div>

          <div className="space-y-4">
            {paymentMethods.map((pm) => (
              <div key={pm.id} className="bg-white border rounded-lg p-4 flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gray-100 rounded flex items-center justify-center">
                    {pm.type === 'card' ? '💳' : '📱'}
                  </div>
                  <div>
                    {pm.type === 'card' ? (
                      <>
                        <p className="font-semibold">{pm.brand} •••• {pm.last4}</p>
                        <p className="text-sm text-gray-600">Expires {pm.exp_month}/{pm.exp_year}</p>
                      </>
                    ) : (
                      <>
                        <p className="font-semibold">Vipps</p>
                        <p className="text-sm text-gray-600">{pm.phone}</p>
                      </>
                    )}
                  </div>
                  {pm.is_default && (
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded">
                      DEFAULT
                    </span>
                  )}
                </div>
                <div className="flex space-x-2">
                  {!pm.is_default && (
                    <button
                      onClick={() => handleSetDefaultPayment(pm.id)}
                      className="text-blue-600 hover:text-blue-700 text-sm font-semibold"
                    >
                      Set as Default
                    </button>
                  )}
                  <button
                    onClick={() => handleRemovePayment(pm.id)}
                    className="text-red-600 hover:text-red-700 text-sm font-semibold"
                    disabled={pm.is_default}
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}

            {paymentMethods.length === 0 && (
              <div className="text-center py-12 bg-gray-50 rounded-lg">
                <p className="text-gray-600">No payment methods added yet</p>
                <button
                  onClick={() => setShowAddPaymentModal(true)}
                  className="mt-4 text-blue-600 hover:text-blue-700 font-semibold"
                >
                  Add your first payment method
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Invoices Tab */}
      {activeTab === 'invoices' && (
        <div className="space-y-6">
          <h2 className="text-xl font-bold">Invoice History</h2>

          <div className="bg-white border rounded-lg overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Action</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {invoices.map((invoice) => (
                  <tr key={invoice.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {invoice.number}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {new Date(invoice.created).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-semibold">
                      {invoice.currency.toUpperCase()} {(invoice.amount / 100).toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-semibold rounded ${
                        invoice.status === 'paid' ? 'bg-green-100 text-green-800' :
                        invoice.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {invoice.status.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <a
                        href={invoice.pdf_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-700 font-semibold"
                      >
                        Download PDF
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {invoices.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-600">No invoices yet</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Cancel Tab */}
      {activeTab === 'cancel' && (
        <div className="space-y-6">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <h2 className="text-xl font-bold text-red-800 mb-4">Cancel Subscription</h2>
            <p className="text-gray-700 mb-4">
              We're sorry to see you go! Before you cancel, please note:
            </p>
            <ul className="list-disc list-inside space-y-2 text-gray-700 mb-6">
              <li>You'll lose access to all AI agents</li>
              <li>Your data will be retained for 30 days, then deleted</li>
              <li>You can reactivate anytime during the 30-day period</li>
              <li>No refunds for unused time in current billing period</li>
            </ul>

            {!subscription?.cancel_at_period_end ? (
              <button
                onClick={() => setShowCancelModal(true)}
                className="bg-red-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-red-700"
              >
                Cancel My Subscription
              </button>
            ) : (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <p className="text-yellow-800 font-semibold">
                  Your subscription is already scheduled for cancellation on {new Date(subscription.current_period_end).toLocaleDateString()}
                </p>
                <button
                  onClick={async () => {
                    await billingService.reactivateSubscription();
                    await loadBillingData();
                  }}
                  className="mt-4 bg-green-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-green-700"
                >
                  Reactivate Subscription
                </button>
              </div>
            )}
          </div>

          {/* Alternatives */}
          <div className="bg-white border rounded-lg p-6">
            <h3 className="text-lg font-bold mb-4">Before you go, have you considered:</h3>
            <div className="space-y-3">
              <div className="flex items-start">
                <span className="text-2xl mr-3">💡</span>
                <div>
                  <p className="font-semibold">Downgrade to a smaller plan?</p>
                  <p className="text-sm text-gray-600">Pay less, keep essential features</p>
                </div>
              </div>
              <div className="flex items-start">
                <span className="text-2xl mr-3">⏸️</span>
                <div>
                  <p className="font-semibold">Pause your subscription?</p>
                  <p className="text-sm text-gray-600">Take a break, resume anytime</p>
                </div>
              </div>
              <div className="flex items-start">
                <span className="text-2xl mr-3">💬</span>
                <div>
                  <p className="font-semibold">Talk to our team?</p>
                  <p className="text-sm text-gray-600">We're here to help solve any issues</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Modals would go here - simplified for brevity */}
    </div>
  );
};

export default BillingManagement;
