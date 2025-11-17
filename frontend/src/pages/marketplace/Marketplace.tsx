import { Link } from 'react-router-dom'
import { Store, Star, Download } from 'lucide-react'

const SAMPLE_AGENTS = [
  { id: 1, name: 'Email Auto-Responder', description: 'Automatically respond to customer emails', rating: 4.8, downloads: 1234, price: 'Free' },
  { id: 2, name: 'Lead Qualifier', description: 'Qualify leads automatically', rating: 4.9, downloads: 892, price: '$19' },
  { id: 3, name: 'Meeting Scheduler', description: 'Schedule meetings via email/chat', rating: 4.7, downloads: 654, price: '$29' },
]

export default function Marketplace() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
          <Store className="w-8 h-8 text-primary-600" />
          AI Agent Marketplace
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Discover and install pre-built AI agents
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {SAMPLE_AGENTS.map((agent) => (
          <Link key={agent.id} to={`/marketplace/${agent.id}`} className="card p-6 hover:shadow-lg transition-shadow">
            <h3 className="font-semibold text-lg text-gray-900 dark:text-white mb-2">
              {agent.name}
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              {agent.description}
            </p>
            <div className="flex items-center justify-between text-sm mb-4">
              <div className="flex items-center gap-1">
                <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
                <span>{agent.rating}</span>
              </div>
              <div className="flex items-center gap-1 text-gray-500">
                <Download className="w-4 h-4" />
                <span>{agent.downloads}</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-lg font-bold text-primary-600">{agent.price}</span>
              <button className="btn-primary">Install</button>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}
