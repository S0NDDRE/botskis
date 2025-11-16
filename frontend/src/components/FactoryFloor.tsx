/**
 * FactoryFloor - Main canvas for visual agent management
 */
import { useEffect, useRef, useState } from 'react'
import { useDrop } from 'react-dnd'
import { motion } from 'framer-motion'
import { ZoomIn, ZoomOut, Maximize2 } from 'lucide-react'
import { AgentCard } from './AgentCard'
import { useFactoryStore } from '@/store/factoryStore'
import type { Agent } from '@/types'

export function FactoryFloor() {
  const {
    agents,
    connections,
    zoom,
    pan,
    setZoom,
    setPan,
    updateAgentPosition,
    deployAgent,
  } = useFactoryStore()

  const canvasRef = useRef<HTMLDivElement>(null)
  const [isPanning, setIsPanning] = useState(false)
  const [panStart, setPanStart] = useState({ x: 0, y: 0 })

  // Handle drop of new agent from template
  const [{ isOver }, drop] = useDrop(() => ({
    accept: ['TEMPLATE', 'AGENT'],
    drop: (item: any, monitor) => {
      const offset = monitor.getClientOffset()
      if (!offset || !canvasRef.current) return

      const rect = canvasRef.current.getBoundingClientRect()
      const x = (offset.x - rect.left - pan.x) / zoom
      const y = (offset.y - rect.top - pan.y) / zoom

      if (item.type === 'TEMPLATE') {
        // Deploy new agent from template
        deployAgent(item.id, { x, y })
      } else if (item.type === 'AGENT') {
        // Update existing agent position
        updateAgentPosition(item.id, { x, y })
      }
    },
    collect: (monitor) => ({
      isOver: monitor.isOver(),
    }),
  }))

  // Combine refs
  const setRefs = (element: HTMLDivElement) => {
    canvasRef.current = element
    drop(element)
  }

  // Zoom with mouse wheel
  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault()
    const delta = e.deltaY > 0 ? -0.1 : 0.1
    setZoom(zoom + delta)
  }

  // Pan with mouse drag
  const handleMouseDown = (e: React.MouseEvent) => {
    if (e.target === canvasRef.current) {
      setIsPanning(true)
      setPanStart({ x: e.clientX - pan.x, y: e.clientY - pan.y })
    }
  }

  const handleMouseMove = (e: React.MouseEvent) => {
    if (isPanning) {
      setPan({
        x: e.clientX - panStart.x,
        y: e.clientY - panStart.y,
      })
    }
  }

  const handleMouseUp = () => {
    setIsPanning(false)
  }

  // Draw connections between agents
  const renderConnections = () => {
    return connections.map((conn) => {
      const fromAgent = agents.find((a) => a.id === conn.from_agent_id)
      const toAgent = agents.find((a) => a.id === conn.to_agent_id)

      if (!fromAgent || !toAgent) return null

      const x1 = fromAgent.position.x + 128 // Center of agent card
      const y1 = fromAgent.position.y + 70
      const x2 = toAgent.position.x + 128
      const y2 = toAgent.position.y + 70

      return (
        <svg
          key={conn.id}
          className="absolute top-0 left-0 w-full h-full pointer-events-none"
          style={{ zIndex: 0 }}
        >
          <defs>
            <linearGradient id={`gradient-${conn.id}`} x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.5" />
              <stop offset="50%" stopColor="#8b5cf6" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.5" />
            </linearGradient>
          </defs>
          <motion.path
            d={`M ${x1} ${y1} Q ${(x1 + x2) / 2} ${(y1 + y2) / 2 - 50} ${x2} ${y2}`}
            stroke={`url(#gradient-${conn.id})`}
            strokeWidth="2"
            fill="none"
            strokeDasharray="5,5"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ duration: 1, ease: 'easeInOut' }}
          />
          {/* Animated dot moving along path */}
          <motion.circle
            r="4"
            fill="#3b82f6"
            animate={{
              offsetDistance: ['0%', '100%'],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: 'linear',
            }}
            style={{
              offsetPath: `path('M ${x1} ${y1} Q ${(x1 + x2) / 2} ${(y1 + y2) / 2 - 50} ${x2} ${y2}')`,
            }}
          />
        </svg>
      )
    })
  }

  return (
    <div className="relative w-full h-full overflow-hidden bg-factory-floor">
      {/* Grid background */}
      <div
        className="absolute inset-0"
        style={{
          backgroundImage: `
            linear-gradient(rgba(59, 130, 246, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(59, 130, 246, 0.1) 1px, transparent 1px)
          `,
          backgroundSize: `${40 * zoom}px ${40 * zoom}px`,
          backgroundPosition: `${pan.x}px ${pan.y}px`,
        }}
      />

      {/* Zoom controls */}
      <div className="absolute top-4 right-4 flex flex-col gap-2 z-10">
        <button
          onClick={() => setZoom(zoom + 0.1)}
          className="p-2 bg-factory-machine hover:bg-factory-active rounded-lg transition-colors"
        >
          <ZoomIn className="w-5 h-5 text-white" />
        </button>
        <button
          onClick={() => setZoom(zoom - 0.1)}
          className="p-2 bg-factory-machine hover:bg-factory-active rounded-lg transition-colors"
        >
          <ZoomOut className="w-5 h-5 text-white" />
        </button>
        <button
          onClick={() => {
            setZoom(1)
            setPan({ x: 0, y: 0 })
          }}
          className="p-2 bg-factory-machine hover:bg-factory-active rounded-lg transition-colors"
        >
          <Maximize2 className="w-5 h-5 text-white" />
        </button>
        <div className="text-center text-xs text-gray-400 mt-1">{Math.round(zoom * 100)}%</div>
      </div>

      {/* Drop zone indicator */}
      {isOver && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="absolute inset-0 border-4 border-dashed border-blue-500 bg-blue-500/10 pointer-events-none z-20"
        >
          <div className="flex items-center justify-center h-full">
            <div className="text-blue-400 text-2xl font-semibold">
              Drop here to deploy agent
            </div>
          </div>
        </motion.div>
      )}

      {/* Canvas */}
      <div
        ref={setRefs}
        className="relative w-full h-full cursor-grab active:cursor-grabbing"
        onWheel={handleWheel}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        style={{
          transform: `scale(${zoom})`,
          transformOrigin: '0 0',
        }}
      >
        {/* Connections */}
        {renderConnections()}

        {/* Agents */}
        <div className="relative w-full h-full" style={{ zIndex: 1 }}>
          {agents.map((agent) => (
            <AgentCard key={agent.id} agent={agent} />
          ))}
        </div>

        {/* Empty state */}
        {agents.length === 0 && !isOver && (
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center text-gray-500">
              <div className="text-6xl mb-4">🏭</div>
              <h3 className="text-xl font-semibold mb-2">Your Factory Floor is Empty</h3>
              <p className="text-sm">
                Drag agents from the sidebar to get started
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Stats overlay */}
      <div className="absolute bottom-4 left-4 bg-factory-machine/90 backdrop-blur-sm rounded-lg p-4 z-10">
        <div className="flex gap-6 text-sm">
          <div>
            <div className="text-gray-400">Total Agents</div>
            <div className="text-white font-semibold text-lg">{agents.length}</div>
          </div>
          <div>
            <div className="text-gray-400">Active</div>
            <div className="text-green-400 font-semibold text-lg">
              {agents.filter((a) => a.status === 'active').length}
            </div>
          </div>
          <div>
            <div className="text-gray-400">Errors</div>
            <div className="text-red-400 font-semibold text-lg">
              {agents.filter((a) => a.status === 'error').length}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
