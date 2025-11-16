import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { agentsAPI } from '../../lib/api'
import { Bot, Activity, CheckCircle, XCircle } from 'lucide-react'

export default function AIAgentDetail() {
  const { agentId } = useParams()
  const { data: agent } = useQuery({
    queryKey: ['agent', agentId],
    queryFn: () => agentsAPI.getAgent(agentId!),
  })

  return (
    <div className="space-y-6">
      <div className="card p-6">
        <div className="flex items-start gap-4">
          <div className="w-16 h-16 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
            <Bot className="w-8 h-8 text-primary-600" />
          </div>
          <div className="flex-1">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              {agent?.data?.name}
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              {agent?.data?.description}
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card p-6">
          <Activity className="w-8 h-8 text-blue-600 mb-3" />
          <p className="text-sm text-gray-600 dark:text-gray-400">Tasks Completed</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {agent?.data?.tasks_completed || 0}
          </p>
        </div>
        <div className="card p-6">
          <CheckCircle className="w-8 h-8 text-green-600 mb-3" />
          <p className="text-sm text-gray-600 dark:text-gray-400">Success Rate</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {agent?.data?.success_rate || 0}%
          </p>
        </div>
        <div className="card p-6">
          <XCircle className="w-8 h-8 text-red-600 mb-3" />
          <p className="text-sm text-gray-600 dark:text-gray-400">Failures</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {agent?.data?.failures || 0}
          </p>
        </div>
      </div>
    </div>
  )
}
