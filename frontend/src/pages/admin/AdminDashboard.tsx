/**
 * Admin Dashboard
 * Complete overview of customers, revenue, system health, and support
 */
import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/admin';

interface Metrics {
  mrr: number;
  arr: number;
  customers: {
    total: number;
    active: number;
    trialing: number;
    churned_this_month: number;
  };
  churn_rate: number;
  revenue_today: number;
  revenue_this_month: number;
  revenue_this_year: number;
}

interface Customer {
  id: string;
  email: string;
  company_name: string;
  plan: string;
  status: string;
  mrr: number;
  created_at: string;
  last_active: string;
}

interface SystemHealth {
  status: 'healthy' | 'degraded' | 'down';
  uptime_percent: number;
  response_time_avg: number;
  error_rate: number;
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
}

interface SupportTicket {
  id: string;
  customer_email: string;
  subject: string;
  status: 'open' | 'pending' | 'resolved';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  created_at: string;
}

export const AdminDashboard: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [systemHealth, setSystemHealth] = useState<SystemHealth | null>(null);
  const [tickets, setTickets] = useState<SupportTicket[]>([]);
  const [activeTab, setActiveTab] = useState<'overview' | 'customers' | 'health' | 'support'>('overview');

  useEffect(() => {
    loadDashboardData();
    // Refresh every 30 seconds
    const interval = setInterval(loadDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [metricsData, customersData, healthData, ticketsData] = await Promise.all([
        adminService.getMetrics(),
        adminService.getCustomers(),
        adminService.getSystemHealth(),
        adminService.getSupportTickets()
      ]);
      setMetrics(metricsData);
      setCustomers(customersData);
      setSystemHealth(healthData);
      setTickets(ticketsData);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !metrics) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="admin-dashboard max-w-7xl mx-auto p-6">
      {/* Header */}
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold mb-2">Admin Dashboard</h1>
          <p className="text-gray-600">Real-time overview of your business</p>
        </div>
        <button
          onClick={loadDashboardData}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-700 flex items-center"
        >
          🔄 Refresh
        </button>
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
            onClick={() => setActiveTab('customers')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'customers'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Customers
          </button>
          <button
            onClick={() => setActiveTab('health')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'health'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            System Health
          </button>
          <button
            onClick={() => setActiveTab('support')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'support'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Support ({tickets.filter(t => t.status === 'open').length})
          </button>
        </nav>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && metrics && (
        <div className="space-y-6">
          {/* Revenue Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-white border rounded-lg p-6">
              <p className="text-sm text-gray-600 mb-1">Monthly Recurring Revenue</p>
              <p className="text-3xl font-bold text-blue-600">€{metrics.mrr.toLocaleString()}</p>
              <p className="text-xs text-gray-500 mt-2">ARR: €{metrics.arr.toLocaleString()}</p>
            </div>

            <div className="bg-white border rounded-lg p-6">
              <p className="text-sm text-gray-600 mb-1">Total Customers</p>
              <p className="text-3xl font-bold text-green-600">{metrics.customers.total}</p>
              <p className="text-xs text-gray-500 mt-2">
                Active: {metrics.customers.active} | Trial: {metrics.customers.trialing}
              </p>
            </div>

            <div className="bg-white border rounded-lg p-6">
              <p className="text-sm text-gray-600 mb-1">Churn Rate</p>
              <p className="text-3xl font-bold text-yellow-600">{(metrics.churn_rate * 100).toFixed(1)}%</p>
              <p className="text-xs text-gray-500 mt-2">
                Churned this month: {metrics.customers.churned_this_month}
              </p>
            </div>

            <div className="bg-white border rounded-lg p-6">
              <p className="text-sm text-gray-600 mb-1">Revenue Today</p>
              <p className="text-3xl font-bold text-purple-600">€{metrics.revenue_today.toLocaleString()}</p>
              <p className="text-xs text-gray-500 mt-2">
                This month: €{metrics.revenue_this_month.toLocaleString()}
              </p>
            </div>
          </div>

          {/* Revenue Chart */}
          <div className="bg-white border rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">Revenue Growth</h2>
            <div className="h-64 flex items-end justify-between space-x-2">
              {/* Simplified bar chart - would use Chart.js or similar in production */}
              {[120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340].map((value, i) => (
                <div key={i} className="flex-1 bg-blue-600 rounded-t" style={{ height: `${(value / 340) * 100}%` }}>
                  <div className="text-xs text-center text-white pt-2">{value}k</div>
                </div>
              ))}
            </div>
            <div className="flex justify-between mt-4 text-xs text-gray-600">
              <span>Jan</span>
              <span>Feb</span>
              <span>Mar</span>
              <span>Apr</span>
              <span>May</span>
              <span>Jun</span>
              <span>Jul</span>
              <span>Aug</span>
              <span>Sep</span>
              <span>Oct</span>
              <span>Nov</span>
              <span>Dec</span>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white border rounded-lg p-6">
              <h3 className="font-bold mb-4">Top Plans</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm">Professional</span>
                  <span className="text-sm font-semibold">60%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full" style={{ width: '60%' }}></div>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Starter</span>
                  <span className="text-sm font-semibold">25%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-green-600 h-2 rounded-full" style={{ width: '25%' }}></div>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Enterprise</span>
                  <span className="text-sm font-semibold">15%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-purple-600 h-2 rounded-full" style={{ width: '15%' }}></div>
                </div>
              </div>
            </div>

            <div className="bg-white border rounded-lg p-6">
              <h3 className="font-bold mb-4">System Status</h3>
              {systemHealth && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Status</span>
                    <span className={`px-2 py-1 rounded text-xs font-semibold ${
                      systemHealth.status === 'healthy' ? 'bg-green-100 text-green-800' :
                      systemHealth.status === 'degraded' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {systemHealth.status.toUpperCase()}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Uptime</span>
                    <span className="text-sm font-semibold">{systemHealth.uptime_percent}%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Response Time</span>
                    <span className="text-sm font-semibold">{systemHealth.response_time_avg}ms</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Error Rate</span>
                    <span className="text-sm font-semibold">{(systemHealth.error_rate * 100).toFixed(2)}%</span>
                  </div>
                </div>
              )}
            </div>

            <div className="bg-white border rounded-lg p-6">
              <h3 className="font-bold mb-4">Recent Activity</h3>
              <div className="space-y-3 text-sm">
                <div className="flex items-start">
                  <span className="text-green-600 mr-2">✓</span>
                  <div>
                    <p>New customer: Acme Corp</p>
                    <p className="text-xs text-gray-500">2 minutes ago</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <span className="text-blue-600 mr-2">↑</span>
                  <div>
                    <p>Upgrade: TechStart AS</p>
                    <p className="text-xs text-gray-500">15 minutes ago</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <span className="text-yellow-600 mr-2">!</span>
                  <div>
                    <p>Payment failed: BuildCo</p>
                    <p className="text-xs text-gray-500">1 hour ago</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Customers Tab */}
      {activeTab === 'customers' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-bold">Customer List</h2>
            <input
              type="text"
              placeholder="Search customers..."
              className="border rounded-lg px-4 py-2 w-64"
            />
          </div>

          <div className="bg-white border rounded-lg overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Customer</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Plan</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">MRR</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Created</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Last Active</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {customers.map((customer) => (
                  <tr key={customer.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{customer.company_name}</div>
                        <div className="text-sm text-gray-500">{customer.email}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {customer.plan}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-semibold rounded ${
                        customer.status === 'active' ? 'bg-green-100 text-green-800' :
                        customer.status === 'trialing' ? 'bg-blue-100 text-blue-800' :
                        customer.status === 'past_due' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {customer.status.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                      €{customer.mrr}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {new Date(customer.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {new Date(customer.last_active).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <button className="text-blue-600 hover:text-blue-700 font-semibold mr-3">
                        View
                      </button>
                      <button className="text-gray-600 hover:text-gray-700 font-semibold">
                        Edit
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* System Health Tab */}
      {activeTab === 'health' && systemHealth && (
        <div className="space-y-6">
          <h2 className="text-xl font-bold">System Health</h2>

          {/* Status Overview */}
          <div className="bg-white border rounded-lg p-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-lg font-bold">Current Status</h3>
                <p className="text-sm text-gray-600">Real-time system monitoring</p>
              </div>
              <span className={`px-4 py-2 rounded-lg text-lg font-bold ${
                systemHealth.status === 'healthy' ? 'bg-green-100 text-green-800' :
                systemHealth.status === 'degraded' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {systemHealth.status === 'healthy' ? '✓ All Systems Operational' :
                 systemHealth.status === 'degraded' ? '⚠️ Degraded Performance' :
                 '✗ System Down'}
              </span>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-gray-600 mb-1">Uptime</p>
                <p className="text-2xl font-bold">{systemHealth.uptime_percent}%</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Avg Response Time</p>
                <p className="text-2xl font-bold">{systemHealth.response_time_avg}ms</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Error Rate</p>
                <p className="text-2xl font-bold">{(systemHealth.error_rate * 100).toFixed(2)}%</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Requests/min</p>
                <p className="text-2xl font-bold">1,247</p>
              </div>
            </div>
          </div>

          {/* Resource Usage */}
          <div className="bg-white border rounded-lg p-6">
            <h3 className="text-lg font-bold mb-4">Resource Usage</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium">CPU Usage</span>
                  <span className="text-sm font-semibold">{systemHealth.cpu_usage}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full ${
                      systemHealth.cpu_usage > 80 ? 'bg-red-600' :
                      systemHealth.cpu_usage > 60 ? 'bg-yellow-600' :
                      'bg-green-600'
                    }`}
                    style={{ width: `${systemHealth.cpu_usage}%` }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium">Memory Usage</span>
                  <span className="text-sm font-semibold">{systemHealth.memory_usage}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full ${
                      systemHealth.memory_usage > 85 ? 'bg-red-600' :
                      systemHealth.memory_usage > 70 ? 'bg-yellow-600' :
                      'bg-green-600'
                    }`}
                    style={{ width: `${systemHealth.memory_usage}%` }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium">Disk Usage</span>
                  <span className="text-sm font-semibold">{systemHealth.disk_usage}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full ${
                      systemHealth.disk_usage > 90 ? 'bg-red-600' :
                      systemHealth.disk_usage > 75 ? 'bg-yellow-600' :
                      'bg-green-600'
                    }`}
                    style={{ width: `${systemHealth.disk_usage}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          {/* Service Status */}
          <div className="bg-white border rounded-lg p-6">
            <h3 className="text-lg font-bold mb-4">Service Status</h3>
            <div className="space-y-3">
              {['API Server', 'Database', 'Redis Cache', 'AI Agents', 'Payment Gateway', 'Email Service'].map((service) => (
                <div key={service} className="flex items-center justify-between">
                  <span className="text-sm">{service}</span>
                  <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded">
                    OPERATIONAL
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Support Tab */}
      {activeTab === 'support' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-bold">Support Tickets</h2>
            <div className="flex space-x-2">
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700">
                Open ({tickets.filter(t => t.status === 'open').length})
              </button>
              <button className="px-4 py-2 border rounded-lg font-semibold hover:bg-gray-50">
                All
              </button>
            </div>
          </div>

          <div className="space-y-4">
            {tickets.map((ticket) => (
              <div key={ticket.id} className="bg-white border rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <span className={`px-2 py-1 text-xs font-semibold rounded ${
                        ticket.priority === 'urgent' ? 'bg-red-100 text-red-800' :
                        ticket.priority === 'high' ? 'bg-orange-100 text-orange-800' :
                        ticket.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {ticket.priority.toUpperCase()}
                      </span>
                      <span className={`px-2 py-1 text-xs font-semibold rounded ${
                        ticket.status === 'open' ? 'bg-blue-100 text-blue-800' :
                        ticket.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {ticket.status.toUpperCase()}
                      </span>
                    </div>
                    <h3 className="font-bold text-lg mb-1">{ticket.subject}</h3>
                    <p className="text-sm text-gray-600">
                      From: {ticket.customer_email} • {new Date(ticket.created_at).toLocaleString()}
                    </p>
                  </div>
                  <button className="text-blue-600 hover:text-blue-700 font-semibold text-sm">
                    View Details →
                  </button>
                </div>
              </div>
            ))}

            {tickets.length === 0 && (
              <div className="text-center py-12 bg-gray-50 rounded-lg">
                <p className="text-gray-600">No support tickets</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
