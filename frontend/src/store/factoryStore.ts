/**
 * Factory Floor State Management
 */
import { create } from 'zustand'
import type { Agent, AgentTemplate, Connection, FactoryMetrics } from '@/types'
import { agentApi, marketplaceApi, monitoringApi } from '@/api/client'

interface FactoryState {
  // Data
  agents: Agent[]
  templates: AgentTemplate[]
  connections: Connection[]
  metrics: FactoryMetrics | null
  selectedAgent: Agent | null

  // UI State
  isCommandPaletteOpen: boolean
  viewMode: '2d' | '3d'
  zoom: number
  pan: { x: number; y: number }

  // Actions
  loadAgents: (userId: number) => Promise<void>
  loadTemplates: () => Promise<void>
  deployAgent: (templateId: number, position: { x: number; y: number }) => Promise<void>
  updateAgentPosition: (agentId: number, position: { x: number; y: number }) => void
  pauseAgent: (agentId: number) => Promise<void>
  resumeAgent: (agentId: number) => Promise<void>
  deleteAgent: (agentId: number) => Promise<void>
  selectAgent: (agent: Agent | null) => void

  // Connections
  addConnection: (fromId: number, toId: number) => void
  removeConnection: (connectionId: string) => void

  // UI
  toggleCommandPalette: () => void
  setViewMode: (mode: '2d' | '3d') => void
  setZoom: (zoom: number) => void
  setPan: (pan: { x: number; y: number }) => void

  // Metrics
  refreshMetrics: () => Promise<void>
}

export const useFactoryStore = create<FactoryState>((set, get) => ({
  // Initial State
  agents: [],
  templates: [],
  connections: [],
  metrics: null,
  selectedAgent: null,
  isCommandPaletteOpen: false,
  viewMode: '2d',
  zoom: 1,
  pan: { x: 0, y: 0 },

  // Load agents from API
  loadAgents: async (userId: number) => {
    try {
      const agents = await agentApi.getAgents(userId)
      set({ agents })
    } catch (error) {
      console.error('Failed to load agents:', error)
    }
  },

  // Load marketplace templates
  loadTemplates: async () => {
    try {
      const templates = await marketplaceApi.getTemplates()
      set({ templates })
    } catch (error) {
      console.error('Failed to load templates:', error)
    }
  },

  // Deploy new agent
  deployAgent: async (templateId: number, position: { x: number; y: number }) => {
    try {
      const userId = 1 // TODO: Get from auth
      const newAgent = await agentApi.deployAgent(templateId, userId)

      // Add position to agent
      const agentWithPosition = { ...newAgent, position }

      set((state) => ({
        agents: [...state.agents, agentWithPosition],
      }))

      // Update position in backend
      await agentApi.updateAgentPosition(newAgent.id, position)
    } catch (error) {
      console.error('Failed to deploy agent:', error)
    }
  },

  // Update agent position (drag & drop)
  updateAgentPosition: (agentId: number, position: { x: number; y: number }) => {
    set((state) => ({
      agents: state.agents.map((agent) =>
        agent.id === agentId ? { ...agent, position } : agent
      ),
    }))

    // Debounced API call (would add debounce in production)
    agentApi.updateAgentPosition(agentId, position).catch(console.error)
  },

  // Pause agent
  pauseAgent: async (agentId: number) => {
    try {
      await agentApi.pauseAgent(agentId)
      set((state) => ({
        agents: state.agents.map((agent) =>
          agent.id === agentId ? { ...agent, status: 'paused' } : agent
        ),
      }))
    } catch (error) {
      console.error('Failed to pause agent:', error)
    }
  },

  // Resume agent
  resumeAgent: async (agentId: number) => {
    try {
      await agentApi.resumeAgent(agentId)
      set((state) => ({
        agents: state.agents.map((agent) =>
          agent.id === agentId ? { ...agent, status: 'active' } : agent
        ),
      }))
    } catch (error) {
      console.error('Failed to resume agent:', error)
    }
  },

  // Delete agent
  deleteAgent: async (agentId: number) => {
    try {
      await agentApi.deleteAgent(agentId)
      set((state) => ({
        agents: state.agents.filter((agent) => agent.id !== agentId),
        selectedAgent: state.selectedAgent?.id === agentId ? null : state.selectedAgent,
      }))
    } catch (error) {
      console.error('Failed to delete agent:', error)
    }
  },

  // Select agent
  selectAgent: (agent: Agent | null) => {
    set({ selectedAgent: agent })
  },

  // Add connection between agents
  addConnection: (fromId: number, toId: number) => {
    const fromAgent = get().agents.find((a) => a.id === fromId)
    const toAgent = get().agents.find((a) => a.id === toId)

    if (!fromAgent || !toAgent) return

    const newConnection: Connection = {
      id: `${fromId}-${toId}`,
      from_agent_id: fromId,
      to_agent_id: toId,
      from_point: fromAgent.position,
      to_point: toAgent.position,
      status: 'active',
    }

    set((state) => ({
      connections: [...state.connections, newConnection],
    }))
  },

  // Remove connection
  removeConnection: (connectionId: string) => {
    set((state) => ({
      connections: state.connections.filter((c) => c.id !== connectionId),
    }))
  },

  // Toggle command palette
  toggleCommandPalette: () => {
    set((state) => ({
      isCommandPaletteOpen: !state.isCommandPaletteOpen,
    }))
  },

  // Set view mode
  setViewMode: (mode: '2d' | '3d') => {
    set({ viewMode: mode })
  },

  // Set zoom
  setZoom: (zoom: number) => {
    set({ zoom: Math.max(0.5, Math.min(2, zoom)) })
  },

  // Set pan
  setPan: (pan: { x: number; y: number }) => {
    set({ pan })
  },

  // Refresh metrics
  refreshMetrics: async () => {
    try {
      const metrics = await monitoringApi.getFactoryMetrics()
      set({ metrics })
    } catch (error) {
      console.error('Failed to refresh metrics:', error)
    }
  },
}))
