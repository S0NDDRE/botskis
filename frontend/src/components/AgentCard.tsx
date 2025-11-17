/**
 * AgentCard - Visual representation of an agent on the factory floor
 */
import { useDrag } from 'react-dnd'
import { motion } from 'framer-motion'
import { Play, Pause, Trash2, Settings, AlertCircle, CheckCircle, Loader } from 'lucide-react'
import type { Agent } from '@/types'
import { useFactoryStore } from '@/store/factoryStore'

interface AgentCardProps {
  agent: Agent
  onClick?: () => void
}

export function AgentCard({ agent, onClick }: AgentCardProps) {
  const { pauseAgent, resumeAgent, deleteAgent, selectAgent } = useFactoryStore()

  const [{ isDragging }, drag] = useDrag(() => ({
    type: 'AGENT',
    item: { id: agent.id, type: 'AGENT' },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }))

  const statusColors = {
    active: 'bg-factory-success border-green-500',
    paused: 'bg-factory-warning border-yellow-500',
    error: 'bg-factory-error border-red-500',
    healing: 'bg-factory-accent border-blue-500',
  }

  const statusIcons = {
    active: <CheckCircle className="w-4 h-4 text-green-400" />,
    paused: <Pause className="w-4 h-4 text-yellow-400" />,
    error: <AlertCircle className="w-4 h-4 text-red-400" />,
    healing: <Loader className="w-4 h-4 text-blue-400 animate-spin" />,
  }

  const handlePauseResume = (e: React.MouseEvent) => {
    e.stopPropagation()
    if (agent.status === 'active') {
      pauseAgent(agent.id)
    } else if (agent.status === 'paused') {
      resumeAgent(agent.id)
    }
  }

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation()
    if (confirm(`Delete agent "${agent.name}"?`)) {
      deleteAgent(agent.id)
    }
  }

  const handleClick = () => {
    selectAgent(agent)
    onClick?.()
  }

  return (
    <motion.div
      ref={drag}
      initial={{ scale: 0, rotate: -180 }}
      animate={{ scale: 1, rotate: 0 }}
      exit={{ scale: 0, rotate: 180 }}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={handleClick}
      className={`
        relative w-64 h-40 rounded-lg border-2 p-4 cursor-move
        backdrop-blur-sm shadow-lg transition-all
        ${statusColors[agent.status]}
        ${isDragging ? 'opacity-50' : 'opacity-100'}
      `}
      style={{
        position: 'absolute',
        left: agent.position.x,
        top: agent.position.y,
      }}
    >
      {/* Status indicator pulse */}
      {agent.status === 'active' && (
        <div className="absolute top-2 right-2">
          <div className="relative">
            <div className="w-3 h-3 bg-green-400 rounded-full"></div>
            <div className="absolute top-0 left-0 w-3 h-3 bg-green-400 rounded-full animate-ping"></div>
          </div>
        </div>
      )}

      {/* Agent info */}
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center gap-2">
          {statusIcons[agent.status]}
          <h3 className="text-white font-semibold text-sm truncate">{agent.name}</h3>
        </div>
      </div>

      <p className="text-gray-300 text-xs mb-3 line-clamp-2">{agent.description}</p>

      {/* Metrics */}
      {agent.metrics && (
        <div className="grid grid-cols-3 gap-2 mb-3">
          <div className="text-center">
            <div className="text-xs text-gray-400">Runs</div>
            <div className="text-sm text-white font-semibold">{agent.metrics.runs_today}</div>
          </div>
          <div className="text-center">
            <div className="text-xs text-gray-400">Success</div>
            <div className="text-sm text-white font-semibold">
              {agent.metrics.success_rate}%
            </div>
          </div>
          <div className="text-center">
            <div className="text-xs text-gray-400">Errors</div>
            <div className="text-sm text-white font-semibold">{agent.metrics.errors_today}</div>
          </div>
        </div>
      )}

      {/* Controls */}
      <div className="absolute bottom-3 right-3 flex gap-1">
        {agent.status !== 'error' && agent.status !== 'healing' && (
          <button
            onClick={handlePauseResume}
            className="p-1.5 bg-factory-machine hover:bg-factory-active rounded transition-colors"
            title={agent.status === 'active' ? 'Pause' : 'Resume'}
          >
            {agent.status === 'active' ? (
              <Pause className="w-3.5 h-3.5 text-white" />
            ) : (
              <Play className="w-3.5 h-3.5 text-white" />
            )}
          </button>
        )}
        <button
          onClick={() => selectAgent(agent)}
          className="p-1.5 bg-factory-machine hover:bg-factory-active rounded transition-colors"
          title="Settings"
        >
          <Settings className="w-3.5 h-3.5 text-white" />
        </button>
        <button
          onClick={handleDelete}
          className="p-1.5 bg-red-500/20 hover:bg-red-500/40 rounded transition-colors"
          title="Delete"
        >
          <Trash2 className="w-3.5 h-3.5 text-red-400" />
        </button>
      </div>

      {/* Connection points */}
      <div className="absolute -left-2 top-1/2 w-4 h-4 bg-blue-500 rounded-full border-2 border-factory-floor"></div>
      <div className="absolute -right-2 top-1/2 w-4 h-4 bg-blue-500 rounded-full border-2 border-factory-floor"></div>
    </motion.div>
  )
}
