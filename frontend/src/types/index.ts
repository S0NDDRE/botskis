/**
 * Type definitions for Factory Floor
 */

export interface Agent {
  id: number
  name: string
  description: string
  type: string
  status: 'active' | 'paused' | 'error' | 'healing'
  position: { x: number; y: number }
  template_id: number
  config: Record<string, any>
  metrics?: AgentMetrics
  connections?: Connection[]
}

export interface AgentMetrics {
  runs_today: number
  success_rate: number
  avg_runtime: number
  last_run: string
  errors_today: number
}

export interface AgentTemplate {
  id: number
  name: string
  description: string
  category: string
  icon: string
  deployment_count: number
  rating: number
  is_featured: boolean
  is_popular: boolean
  features: string[]
  integrations: string[]
}

export interface Connection {
  id: string
  from_agent_id: number
  to_agent_id: number
  from_point: { x: number; y: number }
  to_point: { x: number; y: number }
  status: 'active' | 'inactive'
  data_flow_rate?: number
}

export interface FactoryMetrics {
  total_agents: number
  active_agents: number
  total_runs_today: number
  success_rate: number
  errors_today: number
  avg_response_time: number
}

export interface CommandAction {
  id: string
  label: string
  icon: string
  command: string
  action: () => void
  shortcut?: string
}

export interface HealthStatus {
  component: string
  status: 'healthy' | 'degraded' | 'down'
  response_time_ms: number
  last_check: string
}
