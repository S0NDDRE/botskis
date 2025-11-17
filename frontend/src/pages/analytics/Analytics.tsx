import { useQuery } from '@tanstack/react-query'
import { analyticsAPI } from '../../lib/api'
import { TrendingUp, DollarSign, Clock, Zap, Download } from 'lucide-react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function Analytics() {
  const { data: dashboardStats } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => analyticsAPI.getDashboardStats(),
  })

  const { data: savings } = useQuery({
    queryKey: ['cost-savings'],
    queryFn: () => analyticsAPI.getCostSavings(),
  })

  const stats = [
    {
      name: 'Total Cost Savings',
      value: `$${savings?.data?.total_savings || 0}`,
      icon: DollarSign,
      color: 'text-green-600',
      bg: 'bg-green-100 dark:bg-green-900/30'
    },
    {
      name: 'Time Saved',
      value: `${savings?.data?.time_saved_hours || 0}h`,
      icon: Clock,
      color: 'text-blue-600',
      bg: 'bg-blue-100 dark:bg-blue-900/30'
    },
    {
      name: 'Tasks Automated',
      value: dashboardStats?.data?.tasks_automated || 0,
      icon: Zap,
      color: 'text-purple-600',
      bg: 'bg-purple-100 dark:bg-purple-900/30'
    },
    {
      name: 'ROI',
      value: `${savings?.data?.roi_percentage || 0}%`,
      icon: TrendingUp,
      color: 'text-orange-600',
      bg: 'bg-orange-100 dark:bg-orange-900/30'
    },
  ]

  const usageData = dashboardStats?.data?.usage_trend || []
  const savingsData = savings?.data?.savings_by_month || []

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Analytics & Metrics
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Track your AI automation performance and ROI
          </p>
        </div>
        <button className="btn-secondary flex items-center gap-2">
          <Download className="w-4 h-4" />
          Export Report
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.name} className="card p-6">
            <div className="flex items-center gap-4">
              <div className={`${stat.bg} p-3 rounded-lg`}>
                <stat.icon className={`w-6 h-6 ${stat.color}`} />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stat.value}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Usage Trend */}
      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-6">Usage Trend</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={usageData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="tasks" stroke="#3B82F6" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Cost Savings */}
      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-6">Monthly Cost Savings</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={savingsData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="savings" fill="#10B981" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* ROI Calculation */}
      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-4">ROI Calculation</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-medium text-gray-700 dark:text-gray-300 mb-3">Before Mindframe</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Employees:</span>
                <span className="font-medium">{savings?.data?.before_employees || 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Hours/Week:</span>
                <span className="font-medium">{savings?.data?.before_hours || 0}h</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Cost/Month:</span>
                <span className="font-medium text-red-600">${savings?.data?.before_cost || 0}</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="font-medium text-gray-700 dark:text-gray-300 mb-3">After Mindframe</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Employees:</span>
                <span className="font-medium">{savings?.data?.after_employees || 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Hours/Week:</span>
                <span className="font-medium">{savings?.data?.after_hours || 0}h</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Cost/Month:</span>
                <span className="font-medium text-green-600">${savings?.data?.after_cost || 0}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6 p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
          <div className="flex items-center justify-between">
            <span className="text-lg font-semibold text-gray-900 dark:text-white">
              Total Monthly Savings:
            </span>
            <span className="text-3xl font-bold text-green-600">
              ${savings?.data?.monthly_savings || 0}
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}
