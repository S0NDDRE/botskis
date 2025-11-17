import { useQuery } from '@tanstack/react-query'
import { api } from '../../lib/api'
import { Link } from 'react-router-dom'
import { Bot, Plus, Play, Pause, Trash2 } from 'lucide-react'

export default function AIAgentList() {
  const { data: agents } = useQuery({
    queryKey: ['agents'],
    queryFn: () => api.get('/agents'),
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            AI Agents
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Manage your AI automation agents
          </p>
        </div>
        <Link to="/agents/create" className="btn-primary flex items-center gap-2">
          <Plus className="w-4 h-4" />
          Create Agent
        </Link>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { label: 'Total Agents', value: agents?.data?.length || 0 },
          { label: 'Active', value: agents?.data?.filter((a: any) => a.status === 'active').length || 0 },
          { label: 'Tasks Completed', value: '1,234' },
          { label: 'Success Rate', value: '98%' },
        ].map((stat) => (
          <div key={stat.label} className="card p-4">
            <p className="text-sm text-gray-600 dark:text-gray-400">{stat.label}</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
              {stat.value}
            </p>
          </div>
        ))}
      </div>

      {/* Agents List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents?.data?.map((agent: any) => (
          <div key={agent.id} className="card p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
                  <Bot className="w-6 h-6 text-primary-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white">
                    {agent.name}
                  </h3>
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    agent.status === 'active'
                      ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300'
                      : 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
                  }`}>
                    {agent.status}
                  </span>
                </div>
              </div>
            </div>

            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              {agent.description}
            </p>

            <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
              <span>Tasks: {agent.tasks_count || 0}</span>
              <span>Success: {agent.success_rate || 0}%</span>
            </div>

            <div className="flex gap-2">
              <Link to={`/agents/${agent.id}`} className="flex-1 btn-secondary text-center">
                View
              </Link>
              <button className="btn-secondary p-2">
                {agent.status === 'active' ? (
                  <Pause className="w-4 h-4" />
                ) : (
                  <Play className="w-4 h-4" />
                )}
              </button>
            </div>
          </div>
        ))}

        {(!agents?.data || agents.data.length === 0) && (
          <div className="col-span-3 text-center py-12">
            <Bot className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500 mb-4">No agents created yet</p>
            <Link to="/agents/create" className="btn-primary inline-flex items-center gap-2">
              <Plus className="w-4 h-4" />
              Create Your First Agent
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}
