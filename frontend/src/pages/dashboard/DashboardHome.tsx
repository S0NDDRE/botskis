import { useQuery } from '@tanstack/react-query'
import { analyticsAPI } from '../../lib/api'
import { Bot, Phone, Shield, GraduationCap, TrendingUp, DollarSign } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function DashboardHome() {
  const { data: stats } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => analyticsAPI.getDashboardStats(),
  })

  const quickStats = [
    {
      name: 'AI Agents',
      value: stats?.data?.agents_count || 0,
      icon: Bot,
      color: 'bg-blue-500',
      link: '/agents'
    },
    {
      name: 'Voice AI Calls',
      value: stats?.data?.calls_count || 0,
      icon: Phone,
      color: 'bg-green-500',
      link: '/voice'
    },
    {
      name: 'Courses Completed',
      value: stats?.data?.courses_completed || 0,
      icon: GraduationCap,
      color: 'bg-purple-500',
      link: '/academy'
    },
    {
      name: 'Cost Savings',
      value: `$${stats?.data?.cost_savings || 0}`,
      icon: DollarSign,
      color: 'bg-emerald-500',
      link: '/analytics'
    }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Welcome back! =K
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Here's what's happening with your AI automation
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {quickStats.map((stat) => (
          <Link
            key={stat.name}
            to={stat.link}
            className="card p-6 hover:shadow-lg transition-shadow"
          >
            <div className="flex items-center gap-4">
              <div className={`${stat.color} p-3 rounded-lg text-white`}>
                <stat.icon className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stat.value}
                </p>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Create AI Agent */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-4">Create AI Agent</h3>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Generate a new AI agent in seconds using natural language
          </p>
          <Link to="/agents/create" className="btn-primary inline-block">
            Create Agent
          </Link>
        </div>

        {/* Start Learning */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-4">Mindframe Academy</h3>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Learn how to master AI automation from Lærling to CEO
          </p>
          <Link to="/academy" className="btn-primary inline-block">
            Start Learning
          </Link>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
        <div className="space-y-4">
          {stats?.data?.recent_activity?.map((activity: any, index: number) => (
            <div key={index} className="flex items-center gap-4 pb-4 border-b border-gray-200 dark:border-gray-700 last:border-0">
              <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
              <div className="flex-1">
                <p className="text-sm font-medium">{activity.title}</p>
                <p className="text-xs text-gray-500">{activity.time}</p>
              </div>
            </div>
          )) || (
            <p className="text-gray-500 text-center py-4">No recent activity</p>
          )}
        </div>
      </div>

      {/* Meta-AI Guardian Alert */}
      {stats?.data?.guardian_suggestions > 0 && (
        <div className="card p-6 border-l-4 border-orange-500">
          <div className="flex items-start gap-4">
            <Shield className="w-6 h-6 text-orange-500 flex-shrink-0" />
            <div className="flex-1">
              <h4 className="font-semibold text-gray-900 dark:text-white mb-1">
                Meta-AI Guardian Suggestions
              </h4>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                {stats.data.guardian_suggestions} optimization suggestions waiting for approval
              </p>
              <Link to="/guardian/approvals" className="text-sm text-orange-600 hover:underline">
                Review Suggestions ’
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
