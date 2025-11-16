import { useQuery } from '@tanstack/react-query'
import { voiceAPI } from '../../lib/api'
import { Phone, PhoneCall, Clock, TrendingUp } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function VoiceAIDashboard() {
  const { data: agents } = useQuery({
    queryKey: ['voice-agents'],
    queryFn: () => voiceAPI.getVoiceAgents(),
  })

  const stats = [
    { name: 'Voice Agents', value: agents?.data?.length || 0, icon: Phone },
    { name: 'Calls Today', value: '47', icon: PhoneCall },
    { name: 'Avg Duration', value: '3:24', icon: Clock },
    { name: 'Success Rate', value: '94%', icon: TrendingUp },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Voice AI Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Manage your AI phone agents
          </p>
        </div>
        <Link to="/voice/agents" className="btn-primary">
          Create Voice Agent
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.name} className="card p-6">
            <div className="flex items-center gap-4">
              <div className="bg-primary-100 dark:bg-primary-900/30 p-3 rounded-lg">
                <stat.icon className="w-6 h-6 text-primary-600" />
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

      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-4">Active Voice Agents</h2>
        <div className="space-y-4">
          {agents?.data?.map((agent: any) => (
            <div key={agent.id} className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
                  <Phone className="w-5 h-5 text-green-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white">{agent.name}</h3>
                  <p className="text-sm text-gray-500">{agent.phone_number}</p>
                </div>
              </div>
              <span className="px-3 py-1 bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300 rounded-full text-sm">
                Active
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
