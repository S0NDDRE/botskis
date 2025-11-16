/**
 * API Client for Botskis Backend
 */
import axios from 'axios'
import type { Agent, AgentTemplate, FactoryMetrics, HealthStatus } from '@/types'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor for auth token (when we add it)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const agentApi = {
  // Get all agents for user
  async getAgents(userId: number): Promise<Agent[]> {
    const { data } = await api.get(`/api/v1/agents?user_id=${userId}`)
    return data
  },

  // Deploy new agent
  async deployAgent(templateId: number, userId: number, config?: any): Promise<Agent> {
    const { data } = await api.post(
      `/api/v1/agents/deploy?user_id=${userId}`,
      { template_id: templateId, custom_config: config }
    )
    return data
  },

  // Pause agent
  async pauseAgent(agentId: number): Promise<void> {
    await api.post(`/api/v1/agents/${agentId}/pause`)
  },

  // Resume agent
  async resumeAgent(agentId: number): Promise<void> {
    await api.post(`/api/v1/agents/${agentId}/resume`)
  },

  // Delete agent
  async deleteAgent(agentId: number): Promise<void> {
    await api.delete(`/api/v1/agents/${agentId}`)
  },

  // Update agent position (for drag & drop)
  async updateAgentPosition(agentId: number, position: { x: number; y: number }): Promise<void> {
    // Would need new endpoint in backend
    await api.patch(`/api/v1/agents/${agentId}`, { position })
  },
}

export const marketplaceApi = {
  // Get all templates
  async getTemplates(): Promise<AgentTemplate[]> {
    const { data } = await api.get('/api/v1/marketplace/templates')
    return data.templates
  },

  // Get featured templates
  async getFeatured(): Promise<AgentTemplate[]> {
    const { data } = await api.get('/api/v1/marketplace/featured')
    return data.templates
  },

  // Search templates
  async search(query: string): Promise<AgentTemplate[]> {
    const { data } = await api.get(`/api/v1/marketplace/search?q=${query}`)
    return data.templates
  },
}

export const monitoringApi = {
  // Get system health
  async getSystemHealth(): Promise<HealthStatus[]> {
    const { data } = await api.get('/api/v1/monitoring/health')
    return data.components
  },

  // Get factory metrics
  async getFactoryMetrics(): Promise<FactoryMetrics> {
    const { data } = await api.get('/metrics')
    // Transform to FactoryMetrics format
    return {
      total_agents: 0, // Would come from data
      active_agents: 0,
      total_runs_today: 0,
      success_rate: 0,
      errors_today: 0,
      avg_response_time: data.system_health?.average_response_time_ms || 0,
    }
  },
}

export default api
